import uuid

from django.core.validators import MinValueValidator
from django.db import models

from foodbasket.restaurants.models import Restaurant
from foodbasket.utils.model import BaseModel


class Category(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.PROTECT
    )
    restaurant = models.ForeignKey(
        Restaurant, related_name="products", on_delete=models.PROTECT
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
