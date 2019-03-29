from rest_framework import generics, viewsets, status
from catalog.serializers import CategorySerializer, ProductContractorSerializer, ProductPartnerSerializer
from catalog.models import Category, ProductContractor, ProductPartner, ProductPartnerImage, \
    ProductPartnerImageURL, ProductContractorImage
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()


class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class ProductContractorView(viewsets.ModelViewSet):
    queryset = ProductContractor.objects.all()
    serializer_class = ProductContractorSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]


class ProductPartnerView(viewsets.ModelViewSet):
    queryset = ProductPartner.objects.all()
    serializer_class = ProductPartnerSerializer

    @action(detail=True, methods=['post'])
    def copy_to_my_products(self, request, pk):
        contractor_prod = ProductContractor.objects.get(pk=pk)
        partner_prod = ProductPartner(
            category=contractor_prod.category,
            slug=contractor_prod.slug,
            name=contractor_prod.name,
            vendore_code=contractor_prod.vendore_code,
            brand=contractor_prod.brand,
            count=contractor_prod.count,
            description=contractor_prod.description,
            price=contractor_prod.price,
        )
        partner_prod.save()

        contractor_img = contractor_prod.produductcontractorimage_set.all()

        partner_img = []
        for image in contractor_img:
            partner_img.append(ProductContractorImage(
                image=image,
                product_id=pk
            ))
        ProductPartnerImage.objects.bulk_create(partner_img)

        contractor_url = contractor_prod.productcontractorimageurl_set.all()

        partner_url = []
        for url in contractor_url:
            partner_url.append(ProductPartnerImageURL(
                url=url,
                product_id=pk
            ))
        ProductPartnerImageURL.objects.bulk_create(partner_url)

        return contractor_prod
