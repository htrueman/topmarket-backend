import requests
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.conf import settings

from news.models import TimeStampedModel
from orders.constants import OrderCreateTypes, OrderStatusGroups, OrderStatuses, CounterpartyProperties
from users.tasks import send_email_task


class Order(models.Model):
    rozetka_id = models.PositiveIntegerField()
    market_id = models.PositiveIntegerField()
    created = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_with_discount = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    cost_with_discount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=OrderStatuses.ORDER_STATUSES)
    status_group = models.PositiveSmallIntegerField(choices=OrderStatusGroups.STATUS_GROUPS)
    seller_comment_created = models.DateTimeField(null=True, blank=True)
    current_seller_comment = models.TextField()
    comment = models.TextField()
    user_phone = models.CharField(max_length=32)
    from_warehouse = models.PositiveSmallIntegerField()
    ttn = models.CharField(max_length=32, null=True)
    total_quantity = models.PositiveSmallIntegerField()
    can_copy = models.BooleanField()
    created_type = models.PositiveSmallIntegerField(choices=OrderCreateTypes.CREATE_TYPES)

    last_update = models.DateTimeField(auto_now=True)
    system_comment = models.TextField(blank=True)

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    products = models.ManyToManyField('catalog.Product', blank=True)

    def __str__(self):
        return '{}, {}, {}'.format(
            self.created,
            dict(OrderCreateTypes.CREATE_TYPES)[self.created_type],
            dict(OrderStatuses.ORDER_STATUSES)[self.status]
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__pk = self.pk

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.__pk and self.status_group == OrderStatusGroups.IN_PROCESSING:
            mail_subject = 'Новый заказ на rozetka.ua'
            message = render_to_string('new_order_email.html', {
                'domain': settings.HOST_NAME,
                'order_id': self.id
            })
            data = {
                'to_emails': [self.user.email, ],
                'subject': mail_subject,
                'html_content': message
            }
            send_email_task.delay(**data)

    class Meta:
        verbose_name = _('Заказ партнера')
        verbose_name_plural = _('Заказы партнеров')


class ContractorOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    contractor = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=OrderStatuses.ORDER_STATUSES)
    products = models.ManyToManyField('catalog.Product', blank=True)

    payer_type = models.CharField(null=True, blank=True, max_length=64, default='Recipient')  # Значение из справочника Тип плательщика
    payment_method = models.CharField(null=True, blank=True, max_length=64, default='Cash')  # Значение из справочника Форма оплаты
    date = models.DateField(null=True, blank=True)
    cargo_type = models.CharField(null=True, blank=True, max_length=64)  # Значение из справочника Тип груза
    volume_general = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    weight = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    service_type = models.CharField(null=True, blank=True, max_length=64)  # Значение из справочника Технология доставки
    seats_amount = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.PositiveSmallIntegerField(null=True, blank=True)

    city_sender = models.UUIDField(null=True, blank=True)
    sender = models.UUIDField(null=True, blank=True)
    sender_address = models.UUIDField(null=True, blank=True)
    contact_sender = models.UUIDField(null=True, blank=True)
    senders_phone = models.CharField(null=True, blank=True)

    city_recipient = models.UUIDField(null=True, blank=True)
    recipient = models.UUIDField(null=True, blank=True)
    recipient_address = models.UUIDField(null=True, blank=True)
    contact_recipient = models.UUIDField(null=True, blank=True)
    recipients_phone = models.CharField(null=True, blank=True, max_length=64)

    class Meta:
        verbose_name = _('Заказ поставщика')
        verbose_name_plural = _('Заказы поставщиков')

    def __str__(self):
        return '{}'.format(self.order)


class NovaPoshtaCounterparty(models.Model):
    contractor = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    first_name = models.CharField(
        max_length=256,
        verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=256,
        verbose_name=_('Фамилия')
    )
    middle_name = models.CharField(
        max_length=256,
        verbose_name=_('Отчество')
    )
    phone = models.CharField(
        max_length=50,
        verbose_name=_('Телефон')
    )
    email = models.EmailField(verbose_name=_('Емейл'))
    counterparty_type = models.CharField(default='PrivatePerson', max_length=256)
    counterparty_property = models.CharField(
        max_length=64,
        choices=CounterpartyProperties.COUNTERPARTY_PROPERTIES,
        default=CounterpartyProperties.RECIPIENT
    )

    nova_poshta_id = models.UUIDField(null=True, blank=True)

    def sync_counterparty(self):
        if self.contractor.nova_poshta_api_key:
            url = 'https://api.novaposhta.ua/v2.0/json/'
            headers = {
                'Content-Type': 'application/json'
            }
            request_body = {
                "apiKey": self.contractor.nova_poshta_api_key,
                "modelName": "Counterparty",
                "calledMethod": "save",
                "methodProperties": {
                    "FirstName": self.first_name,
                    "MiddleName": self.middle_name,
                    "LastName": self.last_name,
                    "Phone": self.phone,
                    "Email": self.email,
                    "CounterpartyType": self.counterparty_type,
                    "CounterpartyProperty": self.counterparty_property
                }
            }

            r = requests.Request("POST", url, headers=headers, json=request_body)
            prep = r.prepare()
            s = requests.Session()
            resp = s.send(prep)
            r.encoding = 'utf-8'
            res = resp.json()

            if res['success']:
                self.nova_poshta_id = res['data'][0]['Ref']
                self.save()

                request_body = {
                    "apiKey": self.contractor.nova_poshta_api_key,
                    "modelName": "Address",
                    "calledMethod": "save",
                    "methodProperties": {
                        "CounterpartyRef": self.nova_poshta_id,
                        "StreetRef": "d4450bdb-0a58-11de-b6f5-001d92f78697",
                        "BuildingNumber": "7",
                        "Flat": "2"
                    }
                }

                r1 = requests.Request("POST", url, headers=headers, json=request_body)
                prep1 = r1.prepare()
                s1 = requests.Session()
                resp1 = s1.send(prep1)
                r1.encoding = 'utf-8'
                res1 = resp1.json()

                if res1['success']:
                    pass


class NovaPoshtaDeliveryHistoryItem(TimeStampedModel):
    contractor_order = models.ForeignKey(ContractorOrder, on_delete=models.CASCADE)

    status = models.CharField(max_length=512)
    status_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{}'.format(self.contractor_order)


class OrderUser(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    login = models.CharField(max_length=64, null=True)
    contact_fio = models.CharField(max_length=256)
    rozetka_id = models.PositiveIntegerField()

    def __str__(self):
        return '{}, {}'.format(self.order.id, self.email)

    class Meta:
        verbose_name = _('Покупатель')
        verbose_name_plural = _('Покупатели')


class OrderDelivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_service_id = models.PositiveIntegerField()
    delivery_service_name = models.CharField(max_length=256)
    recipient_title = models.CharField(max_length=256)
    place_id = models.PositiveIntegerField(null=True, blank=True)
    place_street = models.CharField(max_length=1024, null=True)
    place_number = models.CharField(max_length=32, null=True, blank=True)
    place_house = models.CharField(max_length=32, null=True)
    place_flat = models.CharField(null=True, blank=True, max_length=64)
    cost = models.CharField(null=True, blank=True, max_length=64)
    city = models.CharField(max_length=256, null=True)
    delivery_method_id = models.PositiveIntegerField()
    ref_id = models.UUIDField(null=True, blank=True)
    name_logo = models.CharField(max_length=32)

    def __str__(self):
        return '{}, {}'.format(self.order.id, self.delivery_service_name)

    class Meta:
        verbose_name = _('Доставка')
        verbose_name_plural = _('Доставки')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product_id = models.PositiveIntegerField()
    image_url = models.URLField()
    quantity = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    system_product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'ID заказа: {}, ID продукта: {}'.format(self.order.id, self.product_id)

    class Meta:
        verbose_name = _('Фото товара')
        verbose_name_plural = _('Фото товара')


class OrderSellerComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField()

    def __str__(self):
        return '{}, {}'.format(self.order.id, self.created)

    class Meta:
        verbose_name = _('Комментарий продавца')
        verbose_name_plural = _('Комментарии продавца')


class OrderStatusHistoryItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status_id = models.PositiveIntegerField(choices=OrderStatuses.ORDER_STATUSES)
    created = models.DateTimeField()

    def __str__(self):
        return '{}, {}'.format(self.order.id, dict(OrderStatuses.ORDER_STATUSES)[self.status_id])

    class Meta:
        verbose_name = _('Элемент истории заказа')
        verbose_name_plural = _('История заказа')
