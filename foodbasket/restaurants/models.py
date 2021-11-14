import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from foodbasket.common.model import BaseModel
from foodbasket.restaurants.managers import RestaurantQuerySet


class Restaurant(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    objects = RestaurantQuerySet.as_manager()

    class Meta:
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("restaurant-detail", kwargs={"uuid": self.uuid})
