from django.contrib import admin
from .models import Category, ProductContractor, ProductPartner
from mptt.admin import MPTTModelAdmin


admin.site.register(ProductContractor)
admin.site.register(ProductPartner)


class CategoryAdmin(MPTTModelAdmin):
    exclude = (
        'slug',
    )


admin.site.register(Category, CategoryAdmin)

