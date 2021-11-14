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
    filterset_fields = ["name"]
    ordering_fields = ["name", "created_date", "modified_date"]


class ProductViewSet(ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["name", "category__name", "restaurant__name", "is_active"]
    ordering_fields = ["name", "created_date", "modified_date", "price"]
