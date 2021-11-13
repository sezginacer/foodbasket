from django.db import models


class ProductQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)
