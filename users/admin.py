from django.contrib import admin

from catalog.models import Product
from .models import CustomUser, Company, MyStore, CompanyPitch, Passport, ActivityAreas, ServiceIndustry, CompanyType, \
    HeaderPhoneNumber, FooterPhoneNumber, Navigation, StoreSliderImage, UkraineStatistic, Certificate, TaxPayer, \
    PayerRegister, PayerCertificate
from django.contrib.auth.models import Group

# admin.site.register(ServiceIndustry)
# admin.site.register(ActivityAreas)
# admin.site.register(CompanyType)

admin.site.unregister(Group)


class AdminProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name_plural = 'Администраторы'
        verbose_name = 'Администратор'


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
    list_display = [
        'email',
        'last_name',
        'first_name',
        'user_pocket',
        'phone',
        'date_joined',
        'verified',
    ]
    fields = (
        # 'manager',
        'role',
        'user_pocket',
        'last_name',
        'first_name',
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
    )

    list_editable = [
        'verified',
    ]

    readonly_fields = (
        'date_joined',
    )

    search_fields = (
        'last_name',
        'first_name',
        'email',
        'phone',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='PARTNER')


class ContractorProductTabularInline(admin.TabularInline):
    model = Product

    fields = (
        'id',
        'name',
        'brand',
        'category',
        'product_type',
        'variety_type',
        'vendor_code',
        'warranty_duration',
        'vendor_country',
        'box_size',
        'count',
        'price',
        'recommended_price',
        'description',
        'contractor_product',
        'rozetka_id',
    )

    readonly_fields = fields

    can_delete = False

    show_full_result_count = True

    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ContractorProxy)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'last_name',
        'first_name',
        'phone',
        'verified',
        'date_joined',
        'products_count',
        'percent_for_partners',
    ]

    fields = (
        # 'manager',
        'role',
        'user_pocket',
        'last_name',
        'first_name',
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
        # 'product_percent',
    )

    readonly_fields = (
        'products_count',
        'date_joined',
    )

    list_editable = [
        'verified',
        # 'product_percent',
    ]

    inlines = [
        ContractorProductTabularInline,
    ]

    search_fields = (
        'last_name',
        'first_name',
        'email',
        'phone',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='CONTRACTOR')


@admin.register(AdminProxy)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'last_name',
        'first_name',
        'phone',
        'date_joined',
        'verified',
        'products_count',
    ]
    fields = (
        # 'manager',
        'role',
        'user_pocket',
        'last_name',
        'first_name',
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
        return super().get_queryset(request).filter(is_staff=True)


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


class UkraineStatisticTabular(admin.TabularInline):
    model = UkraineStatistic
    fields = (
        'uk_doc',
    )
    extra = 0


class CertificateTabular(admin.TabularInline):
    model = Certificate
    fields = (
        'cert_doc',
    )
    extra = 0


class TaxPayerTabular(admin.TabularInline):
    model = TaxPayer
    fields = (
        'tax_doc',
    )
    extra = 0


class PayerRegisterTabular(admin.TabularInline):
    model = PayerRegister
    fields = (
        'payer_reg_doc',
    )
    extra = 0


class PayerCertificateTabular(admin.TabularInline):
    model = PayerCertificate
    fields = (
        'payer_cert_doc',
    )
    extra = 0


@admin.register(Company)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (
        CompanyPitchTabular,
        PassportTabular,
        UkraineStatisticTabular,
        CertificateTabular,
        TaxPayerTabular,
        PayerRegisterTabular,
        PayerCertificateTabular,
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
