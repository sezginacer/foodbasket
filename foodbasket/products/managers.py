import typing

from django.db import models
from django.db.models import QuerySet

if typing.TYPE_CHECKING:
    from foodbasket.products.models import Product


class ProductQuerySet(models.QuerySet):
    def actives(self) -> QuerySet["Product"]:
        return self.filter(is_active=True)
