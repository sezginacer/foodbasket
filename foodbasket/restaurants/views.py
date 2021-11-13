from django.conf import settings
from django.db.models import Prefetch, Count, Q, Sum, OuterRef, Exists
from rest_framework import mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order
from foodbasket.products.models import Product, Category
from foodbasket.restaurants.models import Restaurant
from foodbasket.restaurants.serializers import (
    RestaurantDetailSerializer,
    RestaurantListSerializer,
)
from foodbasket.restaurants.service import RestaurantService


class RestaurantListView(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = (
        Restaurant.objects.all()
        .alias(
            order_count=Count(
                "orders", filter=Q(orders__status__in=[OrderStatus.DELIVERED])
            )
        )
        .filter(is_active=True)
        .order_by("-order_count", "-created_date")
    )
    serializer_class = RestaurantListSerializer


class RestaurantDetailView(mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    lookup_url_kwarg = "uuid"
    lookup_field = "uuid"

    service = RestaurantService()

    def retrieve(self, request, *args, **kwargs):
        restaurant = self.get_object()
        popular_products = self.service.get_popular_products(restaurant)
        categorized_products = self.service.get_categories_with_products(restaurant)
        data = {
            "restaurant": restaurant,
            "popular_products": popular_products,
            "categories": categorized_products,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)
