from rest_framework import generics, viewsets, permissions
from django.db import transaction
from catalog.serializers import CategorySerializer, ProductContractorSerializer, ProductPartnerSerializer
from catalog.models import Category, ProductContractor, ProductPartner, ProductPartnerImage, \
    ProductPartnerImageURL
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from catalog.filters import ProductContractorFilter, ProductPartnerFilter
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import get_object_or_404


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
    lookup_field = 'slug'


class ProductContractorView(viewsets.ModelViewSet):
    """
    Продукты, который загрузил себе на сервис юзер, как поставщик.
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser,)
    permission_classes = (permissions.AllowAny, )
    queryset = ProductContractor.objects.all()
    serializer_class = ProductContractorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductContractorFilter

    def get_queryset(self):
        return ProductContractor.objects.filter(contractor=self.request.user)


class ProductPartnerView(viewsets.ModelViewSet):
    """
    Продукты, которые добавил себе партнер от поставщиков.
    """
    parser_classes = (MultiPartParser, CamelCaseJSONParser, )
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProductPartnerSerializer
    http_method_names = ['get', 'put', 'patch', 'delete', ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductPartnerFilter

    def get_queryset(self):
        return ProductPartner.objects.filter(partner=self.request.user)

    @action(detail=False, methods=['get'])
    def copy_to_my_products(self, request, contractor_product_id, *args, **kwargs):
        contractor_prod = get_object_or_404(ProductContractor, pk=contractor_product_id)
        with transaction.atomic():
            partner_prod = ProductPartner(
                category=contractor_prod.category,
                slug=contractor_prod.slug,
                product_code=contractor_prod.product_code,
                name=contractor_prod.name,
                vendore_code=contractor_prod.vendor_code,
                brand=contractor_prod.brand,
                count=contractor_prod.count,
                description=contractor_prod.description,
                price=contractor_prod.price,
                availability=contractor_prod.availability,
            )
            partner_prod.save()

            contractor_imgs = contractor_prod.produductcontractorimage_set.all()

            if contractor_imgs:
                ProductPartnerImage.objects.bulk_create([
                    ProductPartnerImage(product_id=contractor_product_id, **img)
                    for img in contractor_imgs
                ])

            contractor_urls = contractor_prod.productcontractorimageurl_set.all()

            if contractor_urls:
                ProductPartnerImageURL.objects.bulk_create([
                    ProductPartnerImageURL(product_id=contractor_product_id, **url)
                    for url in contractor_urls
                ])

        return contractor_prod
