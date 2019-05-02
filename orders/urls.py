from rest_framework.routers import DefaultRouter
from . import views

app_name = 'orders'

router = DefaultRouter()
router.register(r'', views.OrderViewSet, base_name='orders')
router.register(r'contractor', views.ContractorOrderViewSet, base_name='contractor_orders')

urlpatterns = router.urls
