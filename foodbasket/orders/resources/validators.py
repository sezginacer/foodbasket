from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import Field

from foodbasket.orders.enums import OrderStatus


class OrderStatusChangeValidator:
    requires_context = True

    def __call__(self, status: OrderStatus, serializer_field: Field) -> None:
        instance = serializer_field.parent.instance

        change_valid = (status - instance.status) in [
            (OrderStatus.APPROVED - OrderStatus.WAITING_APPROVE),  # step-by-step update
            (OrderStatus.CANCELLED - OrderStatus.WAITING_APPROVE),  # cancel
        ]

        if not change_valid:
            raise ValidationError(_("This is not a valid status change."))
