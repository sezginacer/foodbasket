import django_filters as filters

from foodbasket.users.models import User


class UserFilter(filters.rest_framework.FilterSet):
    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")
    email = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "is_staff", "is_active"]
