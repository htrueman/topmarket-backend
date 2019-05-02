from rest_framework import serializers

from catalog.models import Product
from catalog.serializers import ProductImageSerializer, ProductImageURLSerializer
from .models import Order, OrderUser, OrderDelivery, OrderItemPhoto, OrderSellerComment, OrderStatusHistoryItem, \
    ContractorOrder


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


class OrderProductSerializer(serializers.ModelSerializer):
    cover_images = ProductImageSerializer(many=True, source='product_images', required=False)
    image_urls = ProductImageURLSerializer(many=True, source='product_image_urls', required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'cover_images',
            'image_urls'
        )


class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerializer(source='orderuser')
    delivery = OrderDeliverySerializer(source='orderdelivery')
    item_photos = OrderItemPhotoSerializer(source='orderitemphoto_set', many=True)
    item_products = OrderProductSerializer(source='products', many=True)
    seller_comments = OrderSellerCommentSerializer(source='ordersellercomment_set', many=True)
    status_history = OrderStatusHistoryItemSerializer(source='orderstatushistoryitem_set', many=True)
    passed_to_contractor = serializers.SerializerMethodField(read_only=True)

    def get_passed_to_contractor(self, obj):
        return bool(obj.contractoroder_set.count())

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
            'passed_to_contractor',

            'user',
            'delivery',
            'item_photos',
            'item_products',
            'seller_comments',
            'status_history',
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'system_comment',
            'status',
        )


class ContractorOrderSerializer(serializers.ModelSerializer):
    base_order = OrderSerializer(source='order')
    item_products = OrderProductSerializer(source='products', many=True)

    class Meta:
        model = ContractorOrder
        fields = (
            'contractor',
            'status',
            'item_products',
            'base_order',
        )


class ContractorOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorOrder
        fields = (
            'status',
        )
