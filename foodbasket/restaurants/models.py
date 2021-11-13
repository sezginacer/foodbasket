import uuid
from django.db import models
from django.urls import reverse

from foodbasket.utils.model import BaseModel


class Restaurant(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("restaurant-detail", kwargs={"uuid": self.uuid})
