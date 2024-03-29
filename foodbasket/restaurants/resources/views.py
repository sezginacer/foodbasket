from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from foodbasket.restaurants.models import Restaurant
from foodbasket.restaurants.resources.filters import RestaurantFilter
from foodbasket.restaurants.resources.serializers import RestaurantSerializer


class RestaurantViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_class = RestaurantFilter
    ordering_fields = ["name", "created_date", "modified_date"]
