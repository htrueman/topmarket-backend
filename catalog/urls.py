from django.urls import path
from catalog import views as catalog_view
from rest_framework.routers import DefaultRouter

app_name = 'catalog'

router = DefaultRouter()
router.register(r'contractor_products', catalog_view.ProductContractorViewSet, base_name='contractor_products')
router.register(r'products_upload', catalog_view.ProductImportViewSet, base_name='product_uploads')
router.register(r'yml-handler', catalog_view.YMLHandlerViewSet, base_name='yml_handler')
router.register(r'partner_products', catalog_view.ProductPartnerViewSet, base_name='partner_products')
urlpatterns = router.urls

urlpatterns += [
    path('categories/', catalog_view.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:id>', catalog_view.CategoryRetrieveView.as_view(), name='category_retrieve'),
]
