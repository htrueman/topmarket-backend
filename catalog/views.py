from rest_framework import generics, viewsets, permissions, status
from django.db import transaction
from catalog.serializers import CategorySerializer, ProductSerializer, ProductUploadFileSerializer
from catalog.models import Category, Product, ProductImage, ProductImageURL, ProductUploadFile
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from catalog.filters import ProductFilter
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import parsers
from catalog.tasks import load_products_from_xls

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


class ProductImportViewSet(viewsets.ModelViewSet):
    """
    Wrong method in swagger.
    Use postman.
    For post method, u must set in body field "file".
    """

    parser_classes = (parsers.MultiPartParser, parsers.FormParser, )
    queryset = ProductUploadFile.objects.all()
    serializer_class = ProductUploadFileSerializer
    http_method_names = ('post')
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        file = self.request.data.get('file')
        if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            serializer.save(
                owner=self.request.user,
                file=file,
            )
            data = {
                'user_id': self.request.user.id,
                'file': file
                # 'file': serializer.data.get('file'),
            }

            # load_products_from_xls.apply_async(kwargs=data)
            load_products_from_xls(**data)
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status_response, headers=headers)
