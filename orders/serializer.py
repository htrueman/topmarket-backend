from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'market_id',
            'created',
            'amount',
            'amount_with_discount',
            'cost',
            'cost_with_discount',
            'status',
            'status_group',
            'seller_comment_created',
            'current_seller_comment',
            'comment',
            'user_phone',
            'from_warehouse',
            'ttn',
            'total_quantity',
            'can_copy',
            'created_type',
            'products',
            'last_update',
        )
