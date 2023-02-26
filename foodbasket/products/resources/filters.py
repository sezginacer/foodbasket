import django_filters as filters

from foodbasket.products.models import Category, Product


class ProductFilter(filters.rest_framework.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    restaurant = filters.CharFilter(field_name="restaurant__name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name", "category", "restaurant", "is_active"]


class CategoryFilter(filters.rest_framework.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name"]
