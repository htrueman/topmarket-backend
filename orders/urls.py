from rest_framework.routers import DefaultRouter
from . import views

app_name = 'orders'

router = DefaultRouter()
router.register(r'', views.OrderViewSet, base_name='orders')

urlpatterns = router.urls
