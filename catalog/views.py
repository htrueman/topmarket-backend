from rest_framework import generics, viewsets, permissions, status
from django.db import transaction
from django.db import IntegrityError
from catalog.serializers import CategorySerializer, ProductSerializer, YMLHandlerSerializer, \
    ProductUploadHistorySerializer, ProductListIdSerializer
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

from users.models import Company, MyStore


class ClientAccessPermission(permissions.BasePermission):
    message = 'Check if both Company and MyStore added to user.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and Company.objects.filter(user=request.user).exists()
                and MyStore.objects.filter(user=request.user).exists())


class CategoryListView(generics.ListAPIView):
    """
    Список категорий
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()


class CategoryRetrieveView(generics.RetrieveAPIView):
    """
    Описание категории
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


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
        return Product.objects.filter(
            user=self.request.user,
            contractor_product=None,
        )


class ProductPartnerViewSet(viewsets.ModelViewSet):
    """
    Продукты партнера
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser, )
    permission_classes = (IsPartner, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductFilter

    @action(detail=False, methods=['post'], serializer_class=ProductListIdSerializer)
    def copy_to_my_products(self, request, **kwargs):
        prod_list_id = request.data['product_list_ids']
        with transaction.atomic():
            for prod_id in prod_list_id:
                contractor_prod = get_object_or_404(Product, pk=prod_id)
                partner_prod = Product(
                    category=contractor_prod.category,
                    user=request.user,
                    product_type=contractor_prod.product_type,
                    brand=contractor_prod.brand,
                    name=contractor_prod.name,
                    variety_type=contractor_prod.variety_type,
                    vendor_code=contractor_prod.vendor_code,
                    warranty_duration=contractor_prod.warranty_duration,
                    vendor_country=contractor_prod.vendor_country,
                    box_size=contractor_prod.box_size,
                    count=contractor_prod.count,
                    description=contractor_prod.description,
                    extra_description=contractor_prod.extra_description,
                    age_group=contractor_prod.age_group,
                    material=contractor_prod.material,
                    price=contractor_prod.price,
                    contractor_product=contractor_prod,
                )
                try:
                    partner_prod.save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        return Response(
                            status=status.HTTP_409_CONFLICT,
                        )

                contractor_imgs = contractor_prod.productimage_set.all()

                if contractor_imgs:
                    ProductImage.objects.bulk_create([
                        ProductImage(product_id=prod_id, **img)
                        for img in contractor_imgs
                    ])

                contractor_urls = contractor_prod.productimageurl_set.all()

                if contractor_urls:
                    ProductImageURL.objects.bulk_create([
                        ProductImageURL(product_id=prod_id, **url)
                        for url in contractor_urls
                    ])
        return Response(
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['get'])
    def products_by_contractors(self, request, *args, **kwargs):
        queryset = Product.products_by_contractors.exclude(
            user=request.user
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
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
    """
    Wrong method in swagger.
    Use postman.
    For post method, u must set in body field "xls_field".
    """

    parser_classes = (parsers.MultiPartParser, parsers.FormParser, )
    queryset = ProductUploadHistory.objects.all()
    serializer_class = ProductUploadHistorySerializer
    http_method_names = ('post', )
    permission_classes = (IsPartner, )

    def perform_create(self, serializer):
        input_file = self.request.FILES['xls_file']
        if input_file.content_type in (
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ):
            serializer.save(
                user=self.request.user,
                xls_file=input_file,
            )
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status_response, headers=headers)
