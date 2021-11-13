from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from foodbasket.products.models import Category, Product
from foodbasket.products.resources.serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
