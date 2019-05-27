from django.contrib import admin
from .models import CustomUser, Company, MyStore, CompanyPitch, Passport, ActivityAreas, ServiceIndustry, CompanyType, \
    HeaderPhoneNumber, FooterPhoneNumber, Navigation, StoreSliderImage

admin.site.register(ServiceIndustry)
admin.site.register(ActivityAreas)
admin.site.register(CompanyType)


class PartnerUserProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class ContractorProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


@admin.register(PartnerUserProxy)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'manager',
        'role',
        'user_pocket',
        'first_name',
        'last_name',
        'patronymic',
        'email',
        'phone',
        'web_site',
        'date_joined',
        'is_staff',
        'is_active',
        'username',
        'avatar',
        'verified',
        'rozetka_username',
        'rozetka_password',
        'rozetka_old_orders_imported',
        'nova_poshta_api_key',
        'organizational_legal_form_of_the_company',
        'organization',
        'edpnou',
        'vat_payer_certificate',
        'bank_name',
        'mfi',
        'checking_account',
        'available_products_count',
        'products_count',
    )

    readonly_fields = (
        'date_joined',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='PARTNER')


@admin.register(ContractorProxy)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'manager',
        'role',
        'user_pocket',
        'first_name',
        'last_name',
        'patronymic',
        'email',
        'phone',
        'web_site',
        'date_joined',
        'is_staff',
        'is_active',
        'username',
        'avatar',
        'verified',
        'rozetka_username',
        'rozetka_password',
        'rozetka_old_orders_imported',
        'nova_poshta_api_key',
        'organizational_legal_form_of_the_company',
        'organization',
        'edpnou',
        'vat_payer_certificate',
        'bank_name',
        'mfi',
        'checking_account',
        'available_products_count',
        'products_count',
    )

    readonly_fields = (
        'products_count',
        'date_joined',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='CONTRACTOR')


class CompanyPitchTabular(admin.TabularInline):
    model = CompanyPitch
    fields = (
        'who_are_you',
        'guru',
        'for_whom',
        'difference',
        'good_partner',
        'future',
    )
    extra = 0


class PassportTabular(admin.TabularInline):
    model = Passport
    fields = (
        'pass_doc',
    )
    extra = 0


@admin.register(Company)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (
        CompanyPitchTabular,
        PassportTabular,
    )


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
