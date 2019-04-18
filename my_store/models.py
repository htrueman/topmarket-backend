from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

# Мой магазин
from users.constants import DOMEN, CALL_BACK


class MyStore(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    domain_subdomain = models.CharField(max_length=2, choices=DOMEN, blank=True, null=True, verbose_name=_('Домен/поддомен'))
    domain_name = models.URLField(max_length=200, null=True, blank=True, verbose_name=_('Имя домена'))
    call_back = models.CharField(max_length=3, choices=CALL_BACK, null=True, blank=True, verbose_name=_('Функция Сall-back'))
    facebook = models.URLField(max_length=200, null=True, blank=True, verbose_name=_('Facebook'))
    instagram = models.URLField(max_length=200, null=True, blank=True, verbose_name=_('Instagram'))
    linkedin = models.URLField(max_length=200, null=True, blank=True, verbose_name=_('Linkedin'))
    top_sales = models.BooleanField(default=False, verbose_name='Топ продаж')
    no_items = models.BooleanField(default=False, verbose_name='Без товара')
    logo = models.ImageField(upload_to='users/company_logo', null=True, blank=True, verbose_name=_('Логотип'))

    @property
    def get_url(self):
        if self.domain_subdomain:
            return 'https://{}/'.format(self.domain_name)


class HeaderPhoneNumber(models.Model):

    store = models.ForeignKey('MyStore', on_delete=models.CASCADE, related_name='header_phones', null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Номер телефона для хедера'))


class FooterPhoneNumber(models.Model):

    store = models.ForeignKey('MyStore', on_delete=models.CASCADE, related_name='footer_phones', null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Номер телефона для футера'))


class Navigation(models.Model):
    store = models.OneToOneField('MyStore', on_delete=models.CASCADE, related_name='navigations', null=True, blank=True)
    navigation = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Раздел навигации'))


class StoreSliderURL(models.Model):
    store = models.ForeignKey(MyStore, on_delete=models.CASCADE, related_name='slider_urls')
    image = models.URLField(null=True, blank=True, verbose_name='Картинка для слайдера')


class LogoWithPhones(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    logo = models.URLField(null=True, blank=True)
    shop_name = models.CharField(max_length=40, null=True, blank=True, verbose_name=_('Название магазина'))
    first_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Контакт'))
    second_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Контакт'))

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)


class SocialNetwork(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    facebook = models.URLField(max_length=100, null=True, blank=True)
    instagram = models.URLField(max_length=100, null=True, blank=True)
    twitter = models.URLField(max_length=100, null=True, blank=True)
    google = models.URLField(max_length=100, null=True, blank=True)


class DeliveryAndPayment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Заголовок'))
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))


class HowToUse(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Заголовок'))
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))


class Contacts(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))


class AboutUs(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=40, null=True, blank=True, verbose_name=_('Заголовок'))
    image = models.ImageField(upload_to='shop/about_us', null=True, blank=True)
    text = models.TextField(null=True, blank=True, verbose_name=_('Текст'))
