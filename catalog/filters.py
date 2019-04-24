from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_id = filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all()
    )
    in_stock = filters.BooleanFilter(
        method='filter_in_stock'
    )
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'category_id',
            'name',
            'vendor_code',
            'min_price',
            'max_price',
            'in_stock'
        ]

    def filter_in_stock(self, queryset, name, value):
        print(value)
        if value:
            return queryset.filter(count__gte=1)
        if not value:
            return queryset.filter(count=0)
        return queryset
