from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class OrderStatus(IntegerChoices):
    WAITING_APPROVE = 1, _("Waiting for Approve")
    APPROVED = 2, _("Approved")
    PREPARING = 3, _("Preparing")
    ON_THE_WAY = 4, _("On the Way")
    DELIVERED = 5, _("Delivered")
    CANCELLED = 6, _("Cancelled")
