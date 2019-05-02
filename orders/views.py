from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from orders.constants import OrderStatuses
from users.permissions import IsPartner
from .models import Order
from .serializer import OrderSerializer, OrderCommentSerializer


class OrderFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr='contains')
    min_date = filters.DateTimeFilter(field_name="created", lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="created", lookup_expr='lte')
    status = filters.ChoiceFilter(field_name="status", choices=OrderStatuses.ORDER_STATUSES)
    user_fio = filters.CharFilter(field_name="orderuser__contact_fio", lookup_expr='icontains')
    user_phone = filters.CharFilter(field_name="user_phone", lookup_expr='icontains')
    status_group = filters.NumberFilter(field_name='status_group', lookup_expr='exact')

    class Meta:
        model = Order
        fields = (
            'id',
            'min_date',
            'max_date',
            'status',
            'user_fio',
            'user_phone',
            'status_group',
        )


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsPartner,)
    http_method_names = ('get', 'patch',)
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = OrderFilter

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

    @action(detail=True, methods=['POST'])
    def pass_to_contractor(self):
        pass
