from rest_framework import generics, viewsets, permissions, status
from django.db import transaction
from django.db import IntegrityError

from catalog.constants import ProductUploadFileTypes
from catalog.serializers import CategorySerializer, ProductSerializer, YMLHandlerSerializer, \
    ProductUploadHistorySerializer, ProductListIdSerializer, CategoryListSerializer
from catalog.models import Category, Product, ProductImage, ProductImageURL, YMLTemplate, ProductUploadHistory
from users.permissions import IsPartner, IsContractor
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from catalog.filters import ProductFilter
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import parsers
from django.core.files.base import ContentFile
from users.models import Company, MyStore


class ClientAccessPermission(permissions.BasePermission):
    message = 'Check if both Company and MyStore added to user.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and Company.objects.filter(user=request.user).exists()
                and MyStore.objects.filter(user=request.user).exists())


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CategorySerializer
    http_method_names = ['get', ]
    queryset = Category.objects.root_nodes()
    pagination_class = None

    @action(detail=False, methods=['get'], serializer_class=CategoryListSerializer)
    def first_level(self, request, *args, **kwargs):
        queryset = Category.objects.filter(
            level=0
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @action(detail=True, methods=['get'], serializer_class=CategoryListSerializer)
    def children(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs.get('pk'))
        queryset = category.get_children()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


class ProductContractorViewSet(viewsets.ModelViewSet):
    """
    Продукты поставщика
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser,)
    permission_classes = (IsContractor, )
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.products_by_contractors.filter(
            user=self.request.user
        )

    @action(detail=False, methods=['get'], serializer_class=CategorySerializer)
    def contractor_categories(self, request, *args, **kwargs):
        queryset = Category.objects.filter(
            product__in=self.get_queryset()
        ).get_ancestors(include_self=False)

        print(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @action(detail=False, methods=['get'], serializer_class=ProductUploadHistorySerializer, filterset_class=None)
    def upload_history(self, request, *args, **kwargs):
        queryset = ProductUploadHistory.objects.filter(
            user=self.request.user
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @action(detail=False, methods=['post'], serializer_class=ProductListIdSerializer)
    def delete_list_of_products(self, request, *args, **kwargs):
        product_list_id = request.data.get('product_list_ids', None)
        self.get_queryset().filter(id__in=product_list_id).delete()
        return Response(
            status=status.HTTP_200_OK,
        )


class ProductPartnerViewSet(viewsets.ModelViewSet):
    """
    Продукты партнера
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser, )
    permission_classes = (IsPartner, )
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.products_by_partners.filter(
            user=self.request.user,
        )

    @action(detail=False, methods=['post'], serializer_class=ProductListIdSerializer)
    def copy_to_my_products(self, request, **kwargs):
        prod_list_id = request.data['product_list_ids']
        with transaction.atomic():
            for prod_id in prod_list_id:
                new_partner_product = get_object_or_404(Product, pk=prod_id)
                new_partner_product.id = None
                new_partner_product.user = self.request.user
                new_partner_product.contractor_product_id = prod_id
                try:
                    new_partner_product.save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        return Response(
                            status=status.HTTP_409_CONFLICT,
                        )
                contractor_prod = Product.objects.get(pk=prod_id)
                contractor_imgs = contractor_prod.product_images.all()
                if contractor_imgs:
                    for img in contractor_imgs:
                        img.id = None
                        img.product_id = new_partner_product.id
                        picture_copy = ContentFile(img.image.read())
                        new_picture_name = str(new_partner_product.name) + str(new_partner_product.id) + '-' + img.image.name.split('/')[-1]
                        img.image.save(new_picture_name, picture_copy)
                        img.save()

                contractor_urls = contractor_prod.product_image_urls.all()

                if contractor_urls:
                    for url in contractor_urls:
                        url.id = None
                        url.product_id = new_partner_product.id
                        url.save()

        return Response(
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'])
    def products_by_contractors(self, request, *args, **kwargs):
        partner_products = self.get_queryset().values_list('contractor_product__id', flat=True)
        queryset = Product.products_by_contractors.exclude(
            id__in=partner_products
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @action(detail=False, methods=['post'], serializer_class=ProductListIdSerializer)
    def delete_list_of_products(self, request, *args, **kwargs):
        product_list_id = request.data.get('product_list_ids', None)
        print(self.get_queryset())
        self.get_queryset().filter(id__in=product_list_id).delete()
        return Response(
            status=status.HTTP_200_OK,
        )


class YMLHandlerViewSet(viewsets.ModelViewSet):
    serializer_class = YMLHandlerSerializer
    permission_classes = (IsPartner, )
    lookup_field = 'yml_type'

    def get_queryset(self):
        return YMLTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProductImportViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, )
    queryset = ProductUploadHistory.objects.all()
    serializer_class = ProductUploadHistorySerializer
    http_method_names = ('post', )
    permission_classes = (IsContractor, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
