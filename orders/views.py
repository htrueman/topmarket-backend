from rest_framework import viewsets
from rest_framework.response import Response

from users.permissions import IsPartner
from .models import Order
from .serializer import OrderSerializer, OrderCommentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsPartner,)
    http_method_names = ('get', 'patch',)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return OrderCommentSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.save()

        return Response(serializer.data)
