from catalog.models import Product, Category
from import_export import resources, fields, widgets


class ProductResource(resources.ModelResource):
    category_id = fields.Field(
        column_name='category',
        attribute='category',
        widget=widgets.ForeignKeyWidget(Category, )
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category_id',
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
