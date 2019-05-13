from rest_framework import serializers

from catalog.models import Product
from catalog.serializers import ProductImageSerializer, ProductImageURLSerializer
from .models import Order, OrderUser, OrderDelivery, OrderItem, OrderSellerComment, OrderStatusHistoryItem, \
    ContractorOrder, NovaPoshtaDeliveryHistoryItem


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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product_id',
            'image_url',
            'quantity',
            'name',
            'price',
            'system_product',
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


class ContractorNovaPoshtaDeliveryHistoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovaPoshtaDeliveryHistoryItem
        fields = (
            'status',
            'status_code',
            'created',
            'updated',
        )


class NovaPoshtaDeliveryHistoryItemSerializer(serializers.ModelSerializer):
    nova_poshta_delivery_history = ContractorNovaPoshtaDeliveryHistoryItemSerializer(
        source='novaposhtadeliveryhistoryitem_set',
        many=True
    )

    class Meta:
        model = ContractorOrder
        fields = (
            'id',
            'nova_poshta_delivery_history',
        )


class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerializer(source='orderuser')
    delivery = OrderDeliverySerializer(source='orderdelivery')
    items = OrderItemSerializer(source='orderitem_set', many=True)
    seller_comments = OrderSellerCommentSerializer(source='ordersellercomment_set', many=True)
    status_history = OrderStatusHistoryItemSerializer(source='orderstatushistoryitem_set', many=True)
    passed_to_contractor = serializers.SerializerMethodField(read_only=True)
    contractor_nova_poshta_delivery_history = NovaPoshtaDeliveryHistoryItemSerializer(
        source='contractororder_set',
        many=True
    )

    def get_passed_to_contractor(self, obj):
        return ContractorOrder.objects.filter(order=obj).exists()

    class Meta:
        model = Order
        fields = (
            'id',
            'rozetka_id',
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
            'items',
            'contractor_nova_poshta_delivery_history',

            'user',
            'delivery',
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
    nova_poshta_delivery_history = ContractorNovaPoshtaDeliveryHistoryItemSerializer(
        source='novaposhtadeliveryhistoryitem_set',
        many=True
    )

    class Meta:
        model = ContractorOrder
        fields = (
            'contractor',
            'status',
            'item_products',
            'base_order',
            'nova_poshta_delivery_history',
        )


class ContractorOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorOrder
        fields = (
            'status',
        )
