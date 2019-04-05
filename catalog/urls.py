from django.urls import path
from catalog import views as catalog_view
from rest_framework.routers import DefaultRouter

app_name = 'catalog'

router = DefaultRouter()
router.register(r'added_products', catalog_view.ProductPartnerView, base_name='added_products')
router.register(r'my_products', catalog_view.ProductContractorView, base_name='my_products')

urlpatterns = router.urls

urlpatterns += [
    path('categories/', catalog_view.CategoryListView.as_view(), name='category_list'),
    path('categories/<str:slug>', catalog_view.CategoryRetrieveView.as_view(), name='category_retrieve'),
]
