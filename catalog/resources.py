from catalog.models import Product
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'vendor_code',
            'product_type',
            'brand',
            'count',
            'description',
            'price',
        )

    def after_import_instance(self, instance, new, **kwargs):
        instance.user_id = kwargs.get('user_id')
        super().after_import_instance(instance, new, **kwargs)

