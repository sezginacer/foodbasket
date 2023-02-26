import django_filters as filters

from foodbasket.orders.models import Order


class OrderFilter(filters.rest_framework.FilterSet):
    email = filters.CharFilter(field_name="user__email", lookup_expr="iexact")
    restaurant = filters.CharFilter(field_name="restaurant__name", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = ["status", "email", "restaurant"]
