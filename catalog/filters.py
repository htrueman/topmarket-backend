from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_id = filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            'category_id',
            'name',
            'vendor_code',
            'min_price',
            'max_price'
        ]

