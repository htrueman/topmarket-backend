from rest_framework import serializers

from .models import Order, OrderUser, OrderDelivery, OrderItemPhoto, OrderSellerComment, OrderStatusHistoryItem


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUser
        fields = (
            'email',
            'login',
            'contact_fio',
        )


class OrderDeliverySerializer(serializers.ModelSerializer):
    class Meta:
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


class OrderItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemPhoto
        fields = (
            'product_id',
            'url'
        )


class OrderSellerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSellerComment
        fields = (
            'comment',
            'created',
        )


class OrderStatusHistoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistoryItem
        fields = (
            'status_id',
            'created',
        )


class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerializer(source='orderuser')
    delivery = OrderDeliverySerializer(source='orderdelivery')
    item_photos = OrderItemPhotoSerializer(source='orderitemphoto_set', many=True)
    seller_comments = OrderSellerCommentSerializer(source='ordersellercomment_set', many=True)
    status_history = OrderStatusHistoryItemSerializer(source='orderstatushistoryitem_set', many=True)

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

            'user',
            'delivery',
            'item_photos',
            'seller_comments',
            'status_history',
        )


class OrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'system_comment',
        )
