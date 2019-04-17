from rest_framework import viewsets
from users.permissions import IsPartner
from .models import Order
from .serializer import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsPartner,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
