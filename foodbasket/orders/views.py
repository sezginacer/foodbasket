from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from foodbasket.orders.serializers import OrderCompleteSerializer, OrderSerializer
from foodbasket.orders.service import OrderService


class OrderCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    request_serializer = OrderCompleteSerializer
    response_serializer = OrderSerializer
    service = OrderService()

    def post(self, request, *args, **kwargs):
        request_serializer = self.request_serializer(
            data=request.data, context={"request": request}
        )
        request_serializer.is_valid(raise_exception=True)
        order = self.service.create_order(**request_serializer.validated_data)

        response_serializer = self.response_serializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
