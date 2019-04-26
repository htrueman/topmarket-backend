from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.conf import settings

from orders.constants import OrderCreateTypes, OrderStatusGroups, OrderStatuses
from users.tasks import send_email_task


class Order(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
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
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')


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


class OrderItemPhoto(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    url = models.URLField()

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
