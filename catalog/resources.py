from catalog.models import Product
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
