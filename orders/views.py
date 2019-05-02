from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from orders.constants import OrderStatuses
from users.permissions import IsPartner, IsContractor
from .models import Order, ContractorOrder
from .serializer import OrderSerializer, OrderUpdateSerializer, ContractorOrderSerializer, \
    ContractorOrderUpdateSerializer


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


class ContractorOrderFilter(OrderFilter):
    id = filters.NumberFilter(field_name="id", lookup_expr='contains')
    min_date = filters.DateTimeFilter(field_name="order__created", lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="order__created", lookup_expr='lte')
    status = filters.ChoiceFilter(field_name="order__status", choices=OrderStatuses.ORDER_STATUSES)
    user_fio = filters.CharFilter(field_name="order__orderuser__contact_fio", lookup_expr='icontains')
    user_phone = filters.CharFilter(field_name="order__user_phone", lookup_expr='icontains')
    status_group = filters.NumberFilter(field_name='order__status_group', lookup_expr='exact')

    class Meta:
        model = ContractorOrder
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
            return OrderUpdateSerializer
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

    @action(detail=True, methods=['GET'])
    def pass_to_contractor(self, request, *args, **kwargs):
        order = self.get_object()
        contractor_to_products_dict = defaultdict(list)
        for product in order.products.all():
            if product.contractor_product:
                contractor_to_products_dict[product.contractor_product.user.pk].append(product.id)

        statuses = []
        for key, value in contractor_to_products_dict.items():
            try:
                contractor_oder = ContractorOrder.objects.get(
                    order=order
                )
                contractor_oder.status = order.status
                contractor_oder.contractor_id = key
                contractor_oder.products.add(*value)
                contractor_oder.save()
            except ContractorOrder.DoesNotExist:
                contractor_oder = ContractorOrder.objects.create(
                    order=order,
                    status=order.status,
                    contractor_id=key
                )
            contractor_oder.products.add(*value)
            statuses.append(contractor_oder.status)

        return Response({'statuses': statuses})


class ContractorOrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsContractor,)
    http_method_names = ('get', 'patch',)
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ContractorOrderFilter

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ContractorOrderUpdateSerializer
        return ContractorOrderSerializer

    def get_queryset(self):
        return ContractorOrder.objects.filter(contractor=self.request.user)
