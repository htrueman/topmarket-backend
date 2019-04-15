from django.contrib import admin
from .models import Category, Product, YMLTemplate, ProductUploadHistory
from import_export.admin import ImportExportActionModelAdmin
from catalog.resources import ProductResource
#admin.site.register(Product)

admin.site.register(Category)
admin.site.register(YMLTemplate)
admin.site.register(ProductUploadHistory)


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
