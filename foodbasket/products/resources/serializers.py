from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from foodbasket.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []


class ProductSerializer(serializers.ModelSerializer):
    def validate_restaurant(self, restaurant):
        if self.instance and self.instance.restaurant != restaurant:
            raise serializers.ValidationError(_("Restaurant can not be changed."))
        return restaurant

    class Meta:
        model = Product
        exclude = []
