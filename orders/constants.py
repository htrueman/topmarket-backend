from django.utils.translation import ugettext as _


class OrderCreateTypes:
    API = 1
    CALL_CENTER = 2
    SELLER_OFFICE = 3
    BASKET = 4

    CREATE_TYPES = (
        (API, _('API')),
        (CALL_CENTER, _('Колл-центр Розетки')),
        (SELLER_OFFICE, _('Кабинет продавца')),
        (BASKET, _('Через корзину')),
    )


class OrderStatuses:
    NEW_ORDER = 1
    DATA_CONFIRMED_AWAITING_SHIPMENT = 2
    SUBMITTED_TO_DELIVERY_SERVICE = 3
    DELIVERED = 4
    EXPECTS_AT_PICKUP_POINT = 5
    PACKAGE_RECEIVED = 6
    NOT_PROCESSED_BY_SELLER = 7
    SHIPPING_EXPIRED = 10
    DID_NOT_TAKE_THE_PARCEL = 11
    REFUSED_GOODS = 12
    CANCELED_BY_ADMIN = 13
    INCORRECT_TTN = 15
    OUT_OF_STOCK_OR_MARRIAGE = 16
    CANCEL_NOT_SATISFIED_WITH_THE_PAYMENT = 17
    COULD_NOT_CONTACT_CUSTOMER = 18
    RETURN = 19
    CANCEL_NOT_SATISFIED_WITH_THE_PRODUCT = 20
    CANCEL_NOT_SATISFIED_WITH_THE_DELIVERY = 24
    TEST_ORDER = 25
    PROCESSED_BY_MANAGER = 26
    REQUIRES_RETROFITTING = 27
    INCORRECT_CONTACT_DETAILS = 28
    CANCEL_INCORRECT_PRICE_ON_THE_WEBSITE = 29
    EXPIRED_RESERVE_PERIOD = 30
    CANCEL_ORDER_RESTORED = 31
    CANCEL_NOT_SATISFIED_WITH_ORDER_UNGROUPING = 32
    CANCEL_NOT_SATISFIED_WITH_THE_COST_OF_DELIVERY = 33
    CANCEL_NOT_SATISFIED_WITH_THE_CARRIER_THE_METHOD_OF_DELIVERY = 34
    CANCEL_DO_NOT_ARRANGE_THE_DELIVERY_TIME = 35
    CANCEL_THE_CLIENT_WANTS_TO_PAY_BY_BANK_TRANSFER_THE_SELLER_DOES_NOT_HAVE_SUCH_OPPORTUNITY = 36
    CANCEL_NOT_SATISFIED_WITH_PREPAYMENT = 37
    CANCEL_NOT_SATISFIED_WITH_THE_QUALITY_OF_THE_GOODS = 38
    CANCEL_THE_CHARACTERISTICS_OF_THE_PRODUCT_DID_NOT_FIT = 39
    CANCEL_CLIENT_CHANGED_HIS_MIND = 40
    CANCEL_BOUGHT_ON_ANOTHER_SITE = 41
    NOT_AVAILABLE = 42
    MARRIAGE = 43
    CANCEL_FAKE_ORDER = 44
    CANCELED_BY_BUYER = 45
    RESTORED_BY_CALLING = 46
    PROCESSING_BY_THE_MANAGER_1 = 47
    PROCESSING_BY_THE_MANAGER_2 = 48

    ORDER_STATUSES = (
         (NEW_ORDER, 'Новый заказ'),
         (DATA_CONFIRMED_AWAITING_SHIPMENT, 'Данные подтверждены. Ожидает отправки'),
         (SUBMITTED_TO_DELIVERY_SERVICE, 'Передан в службу доставки'),
         (DELIVERED, 'Доставляется'),
         (EXPECTS_AT_PICKUP_POINT, 'Ожидает в пункте самовывоза'),
         (PACKAGE_RECEIVED, 'Посылка получена'),
         (NOT_PROCESSED_BY_SELLER, 'Не обработан продавцом'),
         (SHIPPING_EXPIRED, 'Отправка просрочена'),
         (DID_NOT_TAKE_THE_PARCEL, 'Не забрал посылку'),
         (REFUSED_GOODS, 'Отказался от товара'),
         (CANCELED_BY_ADMIN, 'Отменен Администратором'),
         (INCORRECT_TTN, 'Некорректный ТТН'),
         (OUT_OF_STOCK_OR_MARRIAGE, 'Нет в наличии/брак'),
         (CANCEL_NOT_SATISFIED_WITH_THE_PAYMENT, 'Отмена. Не устраивает оплата'),
         (COULD_NOT_CONTACT_CUSTOMER, 'Не удалось связаться с покупателем'),
         (RETURN, 'Возврат'),
         (CANCEL_NOT_SATISFIED_WITH_THE_PRODUCT, 'Отмена. Не устраивает товар'),
         (CANCEL_NOT_SATISFIED_WITH_THE_DELIVERY, 'Отмена. Не устраивает доставка'),
         (TEST_ORDER, 'Тестовый заказ'),
         (PROCESSED_BY_MANAGER, 'Обрабатывается менеджером'),
         (REQUIRES_RETROFITTING, 'Требует доукомплектации'),
         (INCORRECT_CONTACT_DETAILS, 'Некорректные контактные данные'),
         (CANCEL_INCORRECT_PRICE_ON_THE_WEBSITE, 'Отмена. Некорректная цена на сайте'),
         (EXPIRED_RESERVE_PERIOD, 'Истек срок резерва'),
         (CANCEL_ORDER_RESTORED, 'Отмена. Заказ восстановлен'),
         (CANCEL_NOT_SATISFIED_WITH_ORDER_UNGROUPING, 'Отмена. Не устраивает разгруппировка заказа'),
         (CANCEL_NOT_SATISFIED_WITH_THE_COST_OF_DELIVERY, 'Отмена. Не устраивает стоимость доставки'),
         (CANCEL_NOT_SATISFIED_WITH_THE_CARRIER_THE_METHOD_OF_DELIVERY,
          'Отмена. Не устраивает перевозчик, способ доставки'),
         (CANCEL_DO_NOT_ARRANGE_THE_DELIVERY_TIME, 'Отмена. Не устраивают сроки доставки'),
         (CANCEL_THE_CLIENT_WANTS_TO_PAY_BY_BANK_TRANSFER_THE_SELLER_DOES_NOT_HAVE_SUCH_OPPORTUNITY,
          'Отмена. Клиент хочет оплату по безналу. У продавца нет такой возможности'),
         (CANCEL_NOT_SATISFIED_WITH_PREPAYMENT, 'Отмена. Не устраивает предоплата'),
         (CANCEL_NOT_SATISFIED_WITH_THE_QUALITY_OF_THE_GOODS, 'Отмена. Не устраивает качество товара'),
         (CANCEL_THE_CHARACTERISTICS_OF_THE_PRODUCT_DID_NOT_FIT,
          'Отмена. Не подошли характеристики товара (цвет,размер)'),
         (CANCEL_CLIENT_CHANGED_HIS_MIND, 'Отмена. Клиент передумал'),
         (CANCEL_BOUGHT_ON_ANOTHER_SITE, 'Отмена. Купил на другом сайте'),
         (NOT_AVAILABLE, 'Нет в наличии'),
         (MARRIAGE, 'Брак'),
         (CANCEL_FAKE_ORDER, 'Отмена. Фейковый заказ'),
         (CANCELED_BY_BUYER, 'Отменен покупателем'),
         (RESTORED_BY_CALLING, 'Восстановлен при прозвоне'),
         (PROCESSING_BY_THE_MANAGER_1, 'Обрабатывается менеджером (не удалось связаться 1-ый раз)'),
         (PROCESSING_BY_THE_MANAGER_2, 'Обрабатывается менеджером (не удалось связаться 2-ой раз)'),
    )


class OrderStatusGroups:
    IN_PROCESSING = 1
    SUCCESSFUL = 2
    UNSUCCESSFUL = 3

    STATUS_GROUPS = (
        (IN_PROCESSING, _('В обработке')),
        (SUCCESSFUL, _('Успешные')),
        (UNSUCCESSFUL, _('Неуспешные')),
    )


class CounterpartyProperties:
    RECIPIENT = 'recipient'
    SENDER = 'sender'

    COUNTERPARTY_PROPERTIES = (
        (RECIPIENT, _('Получатель')),
        (SENDER, _('Отправитель')),
    )
