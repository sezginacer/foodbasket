from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import Field

from foodbasket.orders.enums import OrderStatus


class OrderStatusChangeValidator:
    requires_context = True

    # Define valid status transitions
    VALID_TRANSITIONS = {
        OrderStatus.WAITING_APPROVE: [OrderStatus.APPROVED, OrderStatus.CANCELLED],
        OrderStatus.APPROVED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.ON_THE_WAY, OrderStatus.CANCELLED],
        OrderStatus.ON_THE_WAY: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
        OrderStatus.DELIVERED: [],  # Final state
        OrderStatus.CANCELLED: [],  # Final state
    }

    def __call__(self, status: OrderStatus, serializer_field: Field) -> None:
        instance = serializer_field.parent.instance
        
        if not instance:
            return  # New instance, no validation needed

        current_status = instance.status
        new_status = status

        # Check if transition is valid
        if new_status not in self.VALID_TRANSITIONS.get(current_status, []):
            valid_transitions = [s.label for s in self.VALID_TRANSITIONS.get(current_status, [])]
            raise ValidationError(
                _("Invalid status transition from '{current}' to '{new}'. "
                  "Valid transitions: {valid}").format(
                    current=current_status.label,
                    new=new_status.label,
                    valid=", ".join(valid_transitions) if valid_transitions else "None"
                )
            )
