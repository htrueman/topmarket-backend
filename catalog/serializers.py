import datetime

from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from catalog.models import Category, Product, ProductImage, ProductImageURL, YMLTemplate, ProductUploadHistory
from users.utils import CustomBase64Field, valid_url_extension


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


class CategoryListSerializer(serializers.ModelSerializer):
    is_have_children = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'parent',
            'is_have_children',
        )


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
    image_decoded = CustomBase64Field(source='image', required=False)

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


class ProductListIdSerializer(serializers.ModelSerializer):
    product_list_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Product.products_by_contractors.all(),
    )

    class Meta:
        model = Product
        fields = (
            'product_list_ids',
        )


class ProductSerializer(serializers.ModelSerializer):
    cover_images = ProductImageSerializer(many=True, source='product_images', required=False)
    image_urls = ProductImageURLSerializer(many=True, source='product_image_urls', required=False)

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
        cover_images_data = validated_data.pop('product_images', None)
        image_urls = validated_data.pop('product_image_urls', None)
        # print(self.validated_data)
        with transaction.atomic():
            product = Product.objects.create(**validated_data, user=self.context['request'].user)
            if cover_images_data:
                ProductImage.objects.bulk_create([
                    ProductImage(product=product, **image_data)
                    for image_data in cover_images_data
                ])
            if image_urls:
                ProductImageURL.objects.bulk_create([
                    ProductImageURL(product=product, **url_data)
                    for url_data in image_urls
                ])
            return product

    def update(self, instance, validated_data):
        print(validated_data)
        cover_images_data = validated_data.pop('product_images', None)
        image_urls = validated_data.pop('product_image_urls', None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if cover_images_data:
                for cover_data in cover_images_data:
                    cover_id = cover_data.get('id', None)
                    image_data = cover_data.get('')
                    if cover_id:
                        is_url_field = valid_url_extension(image_data)
                        if is_url_field is not True:
                            ProductImage.objects.filter(id=cover_id).delete()
                    else:
                        if type(image_data) == ContentFile:
                            ProductImage.objects.create(company=instance, image=image_data)
            if image_urls:
                instance.product_image_urls.all().delete()
                ProductImageURL.objects.bulk_create([
                    ProductImageURL(product=instance, **image_url)
                    for image_url in image_urls
                ])
            instance.save()
            return instance


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
            'created',
            'is_uploaded',
            'errors',
        )
        read_only_fields = (
            'created',
            'is_uploaded',
            'errors',
        )

