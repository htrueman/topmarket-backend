from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
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


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set', required=False)
    image_urls = ProductImageURLSerializer(many=True, source='productimageurl_set', required=False)

    class Meta:
        model = Product
        fields = (
            'category',
            'name',
            'vendor_code',
            'brand',
            'count',
            'description',
            'price',
            'images',
            'image_urls',
        )

    def create(self, validated_data):
        print(validated_data)
        try:
            images_data = validated_data.pop('productimage_set')
        except KeyError:
            images_data = None

        try:
            image_urls_data = validated_data.pop('productimageurl_set')
        except KeyError:
            image_urls_data = None
        product = Product.objects.create(**validated_data)
        with transaction.atomic():
            if images_data:
                for image_data in images_data:
                    ProductImage.objects.create(product=product, **image_data)
            if image_urls_data:
                for image_url_data in image_urls_data:
                    ProductImageURL.objects.create(product=product, **image_url_data)
        return product

    def update(self, instance, validated_data):
        try:
            images_data = validated_data.pop('productimage_set')
        except KeyError:
            images_data = None

        try:
            image_urls_data = validated_data.pop('productimageurl_set')
        except KeyError:
            image_urls_data = None

        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            # save product image instances
            if images_data:
                images_list = []
                for image_data in images_data:
                    image, _ = ProductImage.objects.get_or_create(
                        image=image_data['image'],
                        product=instance
                    )
                    images_list.append(image)
                instance.productimages = images_list

            # save product image url instances
            if image_urls_data:
                urls_list = []
                for image_url_data in image_urls_data:
                    url, _ = ProductImageURL.objects.get_or_create(
                        url=image_url_data['url'],
                        product=instance,
                    )
                    urls_list.append(url)
                instance.productimageurls = urls_list

            instance.save()
        return instance










        # instance.category = validated_data.get('category', instance.category)
        # instance.name = validated_data.get('name', instance.name)
        # instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        # instance.count = validated_data.get('count', instance.count)
        # instance.price = validated_data.get('price', instance.price)
        # instance.description = validated_data.get('description', )