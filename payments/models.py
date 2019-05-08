from django.db import models
from catalog.models import TimeStampedModel
from django.contrib.auth import get_user_model
from .constants import TransactionTypes, TransactionSources
from django.utils.translation import ugettext as _

User = get_user_model()

# TODO: Дописать поля для LiqPay
# https://www.liqpay.ua/documentation/api/callback


class PaymentTransaction(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='payment_transactions',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    trans_type = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=TransactionTypes.TRANSACTION_TYPES
    )
    source = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=TransactionSources.TRANSACTION_SOURCES
    )

    status = models.CharField(
        max_length=256,
        null=True, blank=True,
        verbose_name=_('Статус платежа')
    )

    err_description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Описание ошибок')
    )

    is_valid_signature = models.BooleanField(
        default=True,
        verbose_name=_('Проверка сигнатуры')
    )

    class Meta:
        verbose_name = _('Транзакция оплаты')
        verbose_name_plural = _('Транзакции оплат')

    def __str__(self):
        return self.user.get_full_name()

