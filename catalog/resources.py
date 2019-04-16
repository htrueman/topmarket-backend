from catalog.models import Product
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'vendor_code',
            'product_type',
            'brand',
            'variety_type',
            'warranty_duration',
            'vendor_country',
            'box_size',
            'count',
            'description',
            'price',
            'extra_description',
            'age_group',
            'material',
        )

    def after_import_instance(self, instance, new, **kwargs):
        instance.user_id = kwargs.get('user_id')
        super().after_import_instance(instance, new, **kwargs)

