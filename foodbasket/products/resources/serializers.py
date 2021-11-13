from rest_framework import serializers

from foodbasket.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()
