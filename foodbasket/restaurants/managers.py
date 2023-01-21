import typing

from django.db import models
from django.db.models import QuerySet

if typing.TYPE_CHECKING:
    from foodbasket.restaurants.models import Restaurant


class RestaurantQuerySet(models.QuerySet):
    def actives(self) -> QuerySet["Restaurant"]:
        return self.filter(is_active=True)
