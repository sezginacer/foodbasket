from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from foodbasket.common.model import BaseModel
from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.receivers import publish_order
from foodbasket.products.models import Product
from foodbasket.restaurants.models import Restaurant


class Order(BaseModel):
    number = models.CharField(max_length=12, unique=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    status = models.IntegerField(choices=OrderStatus.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.PROTECT
    )
    restaurant = models.ForeignKey(
        Restaurant, related_name="orders", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.number}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        unique_together = ["product", "order"]

    def __str__(self):
        return f"{self.order.number}"


post_save.connect(publish_order, sender=Order)
