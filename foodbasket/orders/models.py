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
    number = models.CharField(max_length=12, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.IntegerField(choices=OrderStatus.choices, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, related_name="orders", on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        indexes = [
            models.Index(fields=['status', 'created_date']),
            models.Index(fields=['user', 'created_date']),
            models.Index(fields=['restaurant', 'status']),
        ]

    def __str__(self) -> str:
        return f"{self.number}"

    def clean(self):
        """Validate order data"""
        from django.core.exceptions import ValidationError
        
        if self.amount <= 0:
            raise ValidationError(_("Order amount must be greater than zero."))
        
        if not self.restaurant.is_active:
            raise ValidationError(_("Cannot create order for inactive restaurant."))

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """Check if order can transition to new status"""
        from foodbasket.orders.resources.validators import OrderStatusChangeValidator
        
        validator = OrderStatusChangeValidator()
        try:
            validator(new_status, None)
            return True
        except:
            return False

    @property
    def is_cancellable(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in [
            OrderStatus.WAITING_APPROVE,
            OrderStatus.APPROVED,
            OrderStatus.PREPARING,
            OrderStatus.ON_THE_WAY
        ]

    @property
    def is_completed(self) -> bool:
        """Check if order is in final state"""
        return self.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        unique_together = ["product", "order"]
        indexes = [
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self) -> str:
        return f"{self.order.number}"

    def clean(self):
        """Validate order item data"""
        from django.core.exceptions import ValidationError
        
        if self.quantity <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        
        if self.amount <= 0:
            raise ValidationError(_("Amount must be greater than zero."))
        
        if not self.product.is_active:
            raise ValidationError(_("Cannot add inactive product to order."))
        
        if not self.product.restaurant.is_active:
            raise ValidationError(_("Cannot add product from inactive restaurant."))

    def save(self, *args, **kwargs):
        """Override save to validate data"""
        self.clean()
        super().save(*args, **kwargs)


post_save.connect(publish_order, sender=Order)
