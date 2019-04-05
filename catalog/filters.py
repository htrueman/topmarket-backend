from django_filters import rest_framework as filters
from .models import ProductContractor, ProductPartner, Category


class ProductContractorFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_q = filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all()
    )

    class Meta:
        model = ProductContractor
        fields = [
            'category_q',
            'name',
            'availability',
            'vendor_code',
            'product_code',
            'min_price',
            'max_price'
        ]


class ProductPartnerFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = ProductPartner
        fields = [
            'category',
            'name',
            'availability',
            'vendor_code',
            'product_code',
            'min_price',
            'max_price'
        ]
