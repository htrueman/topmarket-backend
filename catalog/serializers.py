from django.core.exceptions import ObjectDoesNotExist
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from catalog.models import Category, Product, ProductImage, ProductImageURL


class RecursiveField(serializers.BaseSerializer):

    def to_representation(self, instance):
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(instance, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Object {} does not exist'.format(Model().__class__.__name__)
            )
        return instance


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    subcategories = RecursiveField(
        source='children',
        many=True, required=False,
    )
    slug = serializers.SlugField(allow_unicode=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'slug',
            'name',
            'subcategories',
        )

    def validate(self, attrs):
        name = attrs.get('name', None)
        subcategories = attrs.get('children', None)

        if not name and not subcategories:
            raise serializers.ValidationError(
                'Enter subcategory for association.'
            )
        return attrs


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            'image',
        )


class ProductImageURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImageURL
        fields = (
            'url',
        )


class ProductSerializer(WritableNestedModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set', required=False)
    image_urls = ProductImageURLSerializer(many=True, source='productimageurl_set', required=False)

    class Meta:
        model = Product
        fields = (
            'category',
            'name',
            'vendor_code',
            'product_code',
            'contractor_product',
            'brand',
            'count',
            'description',
            'price',
            'availability',
            'images',
            'image_urls',
        )
