from rest_framework import generics, viewsets, permissions, status
from django.db import transaction
from catalog.serializers import CategorySerializer, ProductSerializer
from catalog.models import Category, Product, ProductImage, ProductImageURL
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from catalog.filters import ProductFilter
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


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


class ProductView(viewsets.ModelViewSet):
    """
    Продукты
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser, )
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductFilter

    @action(detail=True, methods=['post'], serializer_class=None)
    def copy_to_my_products(self, request, pk, **kwargs):
        contractor_prod = get_object_or_404(Product, pk=pk)
        with transaction.atomic():
            partner_prod = Product(
                user=request.user,
                contractor_product=contractor_prod,
                category=contractor_prod.category,
                name=contractor_prod.name,
                vendor_code=contractor_prod.vendor_code,
                brand=contractor_prod.brand,
                count=contractor_prod.count,
                description=contractor_prod.description,
                price=contractor_prod.price,
                availability=contractor_prod.availability,
            )
            partner_prod.save()

            contractor_imgs = contractor_prod.productimage_set.all()

            if contractor_imgs:
                ProductImage.objects.bulk_create([
                    ProductImage(product_id=pk, **img)
                    for img in contractor_imgs
                ])

            contractor_urls = contractor_prod.productimageurl_set.all()

            if contractor_urls:
                ProductImageURL.objects.bulk_create([
                    ProductImageURL(product_id=pk, **url)
                    for url in contractor_urls
                ])
        return Response(
            status=status.HTTP_201_CREATED,
        )


class YMLHandlerViewSet(viewsets.ViewSet):
    pass
