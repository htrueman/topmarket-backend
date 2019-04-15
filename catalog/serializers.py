import datetime

from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from catalog.models import Category, Product, ProductImage, ProductImageURL, YMLTemplate, ProductUploadHistory


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

    class Meta:
        model = Category
        fields = (
            'id',
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
    image_decoded = Base64ImageField(source='image', required=False)

    class Meta:
        model = ProductImage
        fields = (
            'image_decoded',
        )


class ProductImageURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImageURL
        fields = (
            'url',
        )


class ProductSerializer(serializers.ModelSerializer):
    cover_images = ProductImageSerializer(many=True, source='productimage_set', required=False)
    image_urls = ProductImageURLSerializer(many=True, source='productimageurl_set', required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'vendor_code',
            'contractor_product',
            'brand',
            'count',
            'description',
            'price',
            'cover_images',
            'image_urls',
        )

    def create(self, validated_data):
        cover_images_data = validated_data.pop('productimage_set', None)
        image_url = validated_data.pop('productimageurl_set', None)
        # print(self.validated_data)
        product = Product.objects.create(**validated_data, user=self.context['request'].user)
        if cover_images_data:
            ProductImage.objects.bulk_create([
                ProductImage(product=product, **image_data)
                for image_data in cover_images_data
            ])
        if image_url:
            ProductImageURL.objects.bulk_create([
                ProductImageURL(product=product, **url_data)
                for url_data in image_url
            ])
        return product


class YMLHandlerSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)

    class Meta:
        model = YMLTemplate
        fields = (
            'template',
            'yml_type',
            'product_ids',
        )
        read_only_fields = ('template',)

    def validate_product_ids(self, val):
        existing_product_ids = set(Product.objects.filter(pk__in=val).values_list('pk', flat=True))
        non_existing_product_ids = set(val) - existing_product_ids
        if non_existing_product_ids:
            raise ValidationError(
                _('Продукты с этими id не существуют: ') + ', '.join([str(item) for item in non_existing_product_ids]))
        return val

    def validate_user(self, user, yml_type):
        if YMLTemplate.objects.filter(user=user, yml_type=yml_type).exists():
            raise ValidationError({
                'user': _('Для пользователя {} уже создан YML файл данного типа.'.format(user.email))})

    def create(self, validated_data):
        self.validate_user(validated_data['user'], validated_data['yml_type'])
        product_ids = validated_data.pop('product_ids')
        yml_template = super().create(validated_data)
        yml_template.products.add(*product_ids)
        yml_template = self.render_yml_file(yml_template, validated_data['user'].mystore, yml_template.products.all())
        return yml_template

    def update(self, instance, validated_data):
        product_ids = validated_data.pop('product_ids')
        yml_template = super().update(instance, validated_data)
        yml_template.products.remove(*yml_template.products.all().values_list('pk', flat=True))
        yml_template.products.add(*product_ids)
        yml_template = self.render_yml_file(yml_template, validated_data['user'].mystore, yml_template.products.all())
        return yml_template

    @staticmethod
    def render_yml_file(yml_template, store, products):
        category_dict = products.values('category__pk', 'category__name')
        context = {
            'categories': category_dict,
            'products': products,
            'current_datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'store': store,
        }
        content = render_to_response('rozetka.xml', context).content
        yml_template.template.save('rozetka.xml', ContentFile(content), save=True)
        return yml_template


class ProductUploadHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductUploadHistory
        fields = (
            'xls_file',
        )
