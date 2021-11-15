import django_filters as filters

from foodbasket.restaurants.models import Restaurant


class RestaurantFilter(filters.rest_framework.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Restaurant
        fields = ["name", "is_active"]
