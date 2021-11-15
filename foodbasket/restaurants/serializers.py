from rest_framework import serializers

from foodbasket.products.models import Category, Product
from foodbasket.restaurants.models import Restaurant


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["name", "price", "category", "pk"]


class RestaurantListSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="get_absolute_url")

    class Meta:
        model = Restaurant
        fields = ["name", "uuid", "url"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name", "uuid"]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "uuid", "products"]


class RestaurantDetailSerializer(serializers.Serializer):  # noqa
    restaurant = RestaurantSerializer()
    popular_products = ProductSerializer(many=True)
    categories = CategorySerializer(many=True)
