from django.urls import path
from catalog import views as catalog_view
from rest_framework.routers import DefaultRouter

app_name = 'catalog'

router = DefaultRouter()
router.register(r'contractor_products', catalog_view.ProductContractorViewSet, base_name='contractor_products')
router.register(r'products_upload', catalog_view.ProductImportViewSet, base_name='product_uploads')
router.register(r'yml-handler', catalog_view.YMLHandlerViewSet, base_name='yml_handler')
router.register(r'partner_products', catalog_view.ProductPartnerViewSet, base_name='partner_products')
router.register(r'categories', catalog_view.CategoryViewSet, base_name='categories')
urlpatterns = router.urls

