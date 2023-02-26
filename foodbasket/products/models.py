import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from foodbasket.common.model import BaseModel
from foodbasket.products.managers import ProductQuerySet
from foodbasket.restaurants.models import Restaurant


class Category(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self) -> str:
        return f"{self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, related_name="products", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_active = models.BooleanField(default=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = ["name", "restaurant"]

    def __str__(self) -> str:
        return f"{self.name}"
