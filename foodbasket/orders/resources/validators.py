from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from foodbasket.orders.enums import OrderStatus


class OrderStatusChangeValidator(object):
    requires_context = True

    def __call__(self, status, serializer_field):
        instance = serializer_field.parent.instance

        valid_change = status - instance.status == 1
        cancelled = (
            instance.status == OrderStatus.WAITING_APPROVE
            and status == OrderStatus.CANCELLED
        )

        if not (valid_change or cancelled):
            raise ValidationError(_("This is not a valid status change."))
