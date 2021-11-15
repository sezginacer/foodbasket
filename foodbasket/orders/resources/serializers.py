from rest_framework import serializers

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order
from foodbasket.orders.resources.validators import OrderStatusChangeValidator


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = []


class OrderUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=OrderStatus.choices, validators=[OrderStatusChangeValidator()]
    )

    class Meta:
        model = Order
        fields = ["status"]


class StatusSerializer(serializers.Serializer):  # noqa
    status = serializers.CharField(source="status.label")
    orders = serializers.IntegerField()
