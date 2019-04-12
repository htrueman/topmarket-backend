from django.db import models


class Order(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    market_id = models.PositiveIntegerField()
    created = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_with_discount = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    cost_with_discount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField()
    status_group = models.PositiveSmallIntegerField()
    seller_comment_created = models.DateTimeField()
    current_seller_comment = models.TextField()
    comment = models.TextField()
    user_phone = models.CharField(max_length=32)
    from_warehouse = models.PositiveSmallIntegerField()
    ttn = models.CharField(max_length=32)
    total_quantity = models.PositiveSmallIntegerField()
    can_copy = models.BooleanField()
    created_type = models.PositiveSmallIntegerField()


class OrderUser(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    login = models.CharField(max_length=64)
    contact_fio = models.CharField(max_length=256)


class OrderDelivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_service_id = models.PositiveIntegerField()
    delivery_service_name = models.CharField(max_length=256)
    recipient_title = models.CharField(max_length=256)
    place_id = models.PositiveIntegerField()
    place_street = models.CharField(max_length=1024)
    place_number = models.CharField(max_length=32)
    place_house = models.CharField(max_length=32)
    place_flat = models.CharField(null=True, blank=True, max_length=64)
    cost = models.CharField(null=True, blank=True, max_length=64)
    city = models.CharField(max_length=256)
    delivery_method_id = models.PositiveIntegerField()
    ref_id = models.UUIDField()
    name_logo = models.CharField(max_length=32)


class OrderItemPhoto(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    url = models.URLField()


class OrderSellerComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField()


class OrderStatusHistoryItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status_id = models.PositiveIntegerField()
    created = models.DateTimeField()
