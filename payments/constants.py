from django.utils.translation import ugettext as _


class TransactionTypes:
    LIQPAY = 1
    INVOICE = 2

    TRANSACTION_TYPES = (
        (LIQPAY, _('Liq Pay')),
        (INVOICE, _('Счет фактура'))
    )


class TransactionSources:
    BASE_POCKET = 1
    FULL_POCKET = 2
    RECHARGE_BALANCE = 3
    UNBALANCE = 4
    CHARGING_ORDER = 5
    WITHDRAWALS_ORDER = 6

    TRANSACTION_SOURCES = (
        (BASE_POCKET, _('Покупка базового пакета')),
        (FULL_POCKET, _('Покупка полного пакета')),
        (RECHARGE_BALANCE, _('Пополнение баланса')),
        (UNBALANCE, _('Вывод средств')),
        (CHARGING_ORDER, _('Перевод денег на баланс после успешного заказа')),
        (WITHDRAWALS_ORDER, _('Списание денег с баланса после успешного заказа')),
    )

