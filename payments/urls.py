from django.urls import path
from rest_framework.routers import DefaultRouter

from payments import views as pay_views

app_name = 'payments'

router = DefaultRouter()
# router.register(r'transactions', pay_views.PaymentTransactionViewSet, base_name='payment_transactions')

urlpatterns = [
    path('pay/', pay_views.LiqPayPocketBuyView.as_view(), name='pay_view'),
    path('pay-callback/', pay_views.LiqPayPocketCallBackView.as_view(), name='pay_callback'),
] # + router.urls

