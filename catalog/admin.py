from django.contrib import admin
from .models import Category, Product, YMLTemplate
from mptt.admin import MPTTModelAdmin


admin.site.register(Product)


class CategoryAdmin(MPTTModelAdmin):
    exclude = (
        'slug',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(YMLTemplate)
