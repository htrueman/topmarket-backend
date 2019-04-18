from django.contrib import admin

from .models import Order, OrderUser, OrderDelivery, OrderItemPhoto, OrderSellerComment, OrderStatusHistoryItem

admin.site.register(Order)
admin.site.register(OrderUser)
admin.site.register(OrderDelivery)
admin.site.register(OrderItemPhoto)
admin.site.register(OrderSellerComment)
admin.site.register(OrderStatusHistoryItem)
