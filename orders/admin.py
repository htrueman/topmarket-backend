from django.contrib import admin

from .models import Order, OrderUser, OrderDelivery, OrderItem, OrderSellerComment, OrderStatusHistoryItem, \
    ContractorOrder

admin.site.register(Order)
admin.site.register(OrderUser)
admin.site.register(OrderDelivery)
admin.site.register(OrderItem)
admin.site.register(OrderSellerComment)
admin.site.register(OrderStatusHistoryItem)
admin.site.register(ContractorOrder)
