from rest_framework import serializers

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order
from foodbasket.orders.resources.validators import OrderStatusUpdateValidator


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ()


class OrderStatusUpdateSerializer(serializers.Serializer):  # noqa
    status = serializers.ChoiceField(
        choices=OrderStatus.choices, validators=[OrderStatusUpdateValidator()]
    )


class StatusSerializer(serializers.Serializer):  # noqa
    status = serializers.CharField(source="status.label")
    orders = serializers.IntegerField()
