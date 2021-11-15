from django.db.models import Count, Prefetch
from django.utils import timezone
from rest_framework import mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from foodbasket.common.mixins import MultiSerializerViewSetMixin
from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order, OrderItem
from foodbasket.orders.resources.serializers import (
    OrderSerializer,
    OrderUpdateSerializer,
    StatusSerializer,
)


class OrderViewSet(
    MultiSerializerViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "patch"]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    serializer_classes = {"update": OrderUpdateSerializer}
    filterset_fields = ["status", "user__email", "restaurant__name"]
    ordering_fields = ["created_date", "modified_date", "amount"]
    queryset = (
        Order.objects.all()
        .order_by("-created_date")
        .select_related("user")
        .prefetch_related(
            Prefetch(
                "order_items",
                queryset=OrderItem.objects.select_related(
                    "product", "product__category", "product__restaurant"
                ),
            )
        )
    )
    lookup_field = "number"
    lookup_url_kwarg = "number"


class StatusView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):  # noqa
        qs = (
            Order.objects.filter(created_date__date=timezone.now().date())
            .values("status")
            .annotate(orders=Count("pk"))
        )
        counts = {count["status"]: count["orders"] for count in qs}
        data = [
            {"status": status, "orders": counts.get(status, 0)}
            for status in OrderStatus
        ]
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)
