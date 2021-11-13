from django.db.models import Prefetch, Count
from django.utils import timezone
from rest_framework import mixins, permissions, status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order, OrderItem
from foodbasket.orders.resources.serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,
    StatusSerializer,
)
from foodbasket.orders.service import OrderService
from foodbasket.utils.mixins import MultiSerializerViewSetMixin


class OrderViewSet(
    MultiSerializerViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderSerializer
    serializer_classes = {
        "update_status": OrderStatusUpdateSerializer,
    }
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

    service = OrderService()

    @action(methods=["PATCH"], detail=True, url_path="update-status")
    def update_status(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.service.update_status(order, **serializer.validated_data)
        return Response(status=http_status.HTTP_204_NO_CONTENT)


class StatusView(APIView):
    permission_classes = (permissions.AllowAny,)  #  (permissions.IsAdminUser,)
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
