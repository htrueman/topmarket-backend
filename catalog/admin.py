from django.contrib import admin
from .models import Category, Product, YMLTemplate, ProductUploadHistory, ProductImage, ProductImageURL
from import_export.admin import ImportExportActionModelAdmin
from catalog.resources import ProductResource

admin.site.register(Category)
# admin.site.register(YMLTemplate)
admin.site.register(ProductUploadHistory)


class ProductImageTabular(admin.TabularInline):
    model = ProductImage
    exclude = (
        'id',
    )
    extra = 0


class ProductImageURLTabular(admin.TabularInline):
    model = ProductImageURL
    exclude = (
        'id',
    )
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    inlines = (
        ProductImageTabular,
        ProductImageURLTabular
    )

    exclude = (
        'contractor_product',
    )
