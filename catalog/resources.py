from catalog.models import Product, Category
from import_export import resources, fields, widgets


class ProductResource(resources.ModelResource):
    category_id = fields.Field(
        column_name='category_id',
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
            'recommended_price',
            'extra_description',
            'age_group',
            'material',
        )

    def after_import_instance(self, instance, new, **kwargs):
        instance.user_id = kwargs.get('user_id')
        # instance.vendor_code = str(instance.vendor_code)
        super().after_import_instance(instance, new, **kwargs)


class RozetkaProductResource(resources.Resource):
    rozetka_product_id = fields.Field(
        column_name='ID товара в розетке',
        widget=widgets.CharWidget()
    )
    customer_product_id = fields.Field(
        column_name='ID товара у продавца',
        widget=widgets.CharWidget()
    )
    product_name = fields.Field(
        column_name='Название товара',
        widget=widgets.CharWidget()
    )
    uploader_status = fields.Field(
        column_name='Статус в uploader',
        widget=widgets.CharWidget()
    )
    rozetka_status = fields.Field(
        column_name='Статус в розетке',
        widget=widgets.CharWidget()
    )
    rozetka_sell_status = fields.Field(
        column_name='Sell-статус в розетке',
        widget=widgets.CharWidget()
    )
    rozetka_category_id = fields.Field(
        column_name='ID категории в розетке',
        widget=widgets.CharWidget()
    )
    rozetka_category_name = fields.Field(
        column_name='Название категории в розетке',
        widget=widgets.CharWidget()
    )
    customer_category_id = fields.Field(
        column_name='ID категории у продавца',
        widget=widgets.CharWidget()
    )
    customer_category_name = fields.Field(
        column_name='Название категории у продавца',
        widget=widgets.CharWidget()
    )
