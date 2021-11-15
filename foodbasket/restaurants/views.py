from django.db.models import Count, Q
from rest_framework import generics, permissions
from rest_framework.response import Response

from foodbasket.orders.enums import OrderStatus
from foodbasket.restaurants.models import Restaurant
from foodbasket.restaurants.serializers import (
    RestaurantDetailSerializer,
    RestaurantListSerializer,
)
from foodbasket.restaurants.service import RestaurantService


class RestaurantListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = (
        Restaurant.objects.actives()
        .alias(
            order_count=Count(
                "orders", filter=Q(orders__status__in=[OrderStatus.DELIVERED])
            )
        )
        .order_by("-order_count", "-created_date")
    )
    serializer_class = RestaurantListSerializer
    filterset_fields = ["name"]
    ordering_fields = ["name"]


class RestaurantDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Restaurant.objects.actives()
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
