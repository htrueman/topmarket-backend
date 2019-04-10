from django.contrib import admin
from .models import Category, Product, YMLTemplate, ProductUploadFile
from import_export.admin import ImportExportActionModelAdmin

#admin.site.register(Product)

admin.site.register(Category)
admin.site.register(YMLTemplate)
admin.site.register(ProductUploadFile)

@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    pass
    # fields = (
    #     'id',
    #     ''
    # )