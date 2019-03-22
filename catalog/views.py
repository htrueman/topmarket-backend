from rest_framework import generics, viewsets, status
from catalog.serializers import CategorySerializer, ProductSerializer
from catalog.models import Category, Product
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()


class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]

    @action(detail=True, methods=['POST'], serializer_class=None)
    def add_to_my_products(self, request, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.partners.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=None)
    def remove_from_my_products(self, request, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.partners.remove(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def my_products_from_contractors(self, request, pk=None, **kwargs):
        user = request.user
        queryset = user.product_set.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    