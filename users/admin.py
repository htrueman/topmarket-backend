from django.contrib import admin
from .models import CustomUser, Company, MyStore, CompanyPitch, Passport, ActivityAreas, ServiceIndustry, CompanyType, \
    HeaderPhoneNumber, FooterPhoneNumber, Navigation, StoreSliderImage

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(CompanyPitch)
admin.site.register(Passport)
admin.site.register(ServiceIndustry)
admin.site.register(ActivityAreas)
admin.site.register(CompanyType)


class HeaderPhoneNumberTabular(admin.TabularInline):
    model = HeaderPhoneNumber
    fields = (
        'number',
    )
    extra = 0


class FooterPhoneNumberTabular(admin.TabularInline):
    model = FooterPhoneNumber
    fields = (
        'number',
    )
    extra = 0


class NavigationTabular(admin.TabularInline):
    model = Navigation
    fields = (
        'navigation',
    )
    extra = 0


class StoreSliderImageTabular(admin.TabularInline):
    model = StoreSliderImage
    fields = (
        'image',
    )
    extra = 0


@admin.register(MyStore)
class MyStoreAdmin(admin.ModelAdmin):
    inlines = (
        HeaderPhoneNumberTabular,
        FooterPhoneNumberTabular,
        NavigationTabular,
        StoreSliderImageTabular
    )
