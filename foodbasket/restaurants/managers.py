from django.db import models


class RestaurantQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)
