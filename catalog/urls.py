from django.urls import path
from catalog import views as catalog_view
from rest_framework.routers import DefaultRouter

app_name = 'catalog'

router = DefaultRouter()
router.register(r'products', catalog_view.ProductView, base_name='added_products')

urlpatterns = router.urls

urlpatterns += [
    path('categories/', catalog_view.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:id>', catalog_view.CategoryRetrieveView.as_view(), name='category_retrieve'),
]
