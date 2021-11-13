from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order, OrderItem
from foodbasket.products.models import Product
from foodbasket.utils.orders import generate_order_number


class OrderItemCompleteSerializer(serializers.Serializer):  # noqa
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True)
    )
    quantity = serializers.IntegerField(default=1, validators=[MinValueValidator(1)])


class OrderCompleteSerializer(serializers.Serializer):  # noqa
    number = serializers.HiddenField(default=generate_order_number)
    user = serializers.HiddenField(default=CurrentUserDefault())
    status = serializers.HiddenField(default=OrderStatus.WAITING_APPROVE)
    items = OrderItemCompleteSerializer(many=True, allow_empty=False)

    def validate_items(self, items):  # noqa
        products = [item["product"] for item in items]
        restaurant_ids = {product.restaurant_id for product in products}
        product_ids = {product.id for product in products}

        if len(restaurant_ids) > 1:
            raise serializers.ValidationError(
                _("All items must be from the same restaurant.")
            )
        if len(product_ids) != len(products):
            raise serializers.ValidationError(
                _("All items must be of different products.")
            )
        return items


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    restaurant = serializers.CharField(source="restaurant.name")

    class Meta:
        model = Product
        exclude = ("is_active",)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        exclude = ()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = ()
