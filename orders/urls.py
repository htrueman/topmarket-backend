from rest_framework.routers import DefaultRouter
from . import views

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, base_name='orders')
router.register(r'orders_contractor', views.ContractorOrderViewSet, base_name='orders_contractor')

urlpatterns = router.urls
