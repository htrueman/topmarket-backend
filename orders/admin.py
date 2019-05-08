from django.contrib import admin

from .models import Order, OrderUser, OrderDelivery, OrderItem, OrderSellerComment, OrderStatusHistoryItem, \
    ContractorOrder

admin.site.register(ContractorOrder)


class OrderUserTabular(admin.TabularInline):
    model = OrderUser
    fields = (
        'email',
        'login',
        'contact_fio',
        'rozetka_id',
    )
    extra = 0


class OrderDeliveryTabular(admin.TabularInline):
    model = OrderDelivery
    fields = (
        'delivery_service_id',
        'delivery_service_name',
        'recipient_title',
        'place_id',
        'place_street',
        'place_number',
        'place_house',
        'place_flat',
        'cost',
        'city',
        'delivery_method_id',
        'ref_id',
        'name_logo',
    )
    extra = 0


class OrderItemTabular(admin.TabularInline):
    model = OrderItem
    fields = (
        'product_id',
        'image_url',
        'quantity',
        'name',
        'price',
        'system_product',
    )
    extra = 0


class OrderSellerCommentTabular(admin.TabularInline):
    model = OrderSellerComment
    fields = (
        'comment',
        'created',
    )
    extra = 0


class OrderStatusHistoryItemTabular(admin.TabularInline):
    model = OrderStatusHistoryItem
    fields = (
        'status_id',
        'created',
    )
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        OrderUserTabular,
        OrderDeliveryTabular,
        OrderItemTabular,
        OrderSellerCommentTabular,
        OrderStatusHistoryItemTabular,
    )
