from django.conf import settings
from django.db.models import Count, Prefetch, Q, QuerySet, Sum

from foodbasket.orders.enums import OrderStatus
from foodbasket.products.models import Category, Product
from foodbasket.restaurants.models import Restaurant


class RestaurantService:
    def get_popular_products(  # noqa
        self, restaurant: Restaurant, limit: int | None = None
    ) -> QuerySet[Product]:
        limit = limit or settings.RESTAURANT_DETAIL_POPULAR_PRODUCTS_LIMIT

        popular_products = (
            Product.objects.alias(
                total_quantity_sold=Sum(
                    "order_items__quantity",
                    filter=Q(order_items__order__status__in=[OrderStatus.DELIVERED]),
                )
            )
            .actives()
            .filter(restaurant=restaurant, total_quantity_sold__gt=0)
            .order_by("-total_quantity_sold", "-created_date")[:limit]
        )
        return popular_products

    def get_categories_with_products(  # noqa
        self, restaurant: Restaurant
    ) -> QuerySet[Restaurant]:
        categorized_products = (
            Category.objects.alias(
                product_count=Count(
                    "products",
                    filter=Q(products__restaurant=restaurant, products__is_active=True),
                )
            )
            .filter(product_count__gt=0)
            .prefetch_related(
                Prefetch(
                    "products",
                    queryset=Product.objects.alias(
                        total_quantity_sold=Sum(
                            "order_items__quantity",
                            filter=Q(
                                order_items__order__status__in=[OrderStatus.DELIVERED]
                            ),
                        )
                    )
                    .actives()
                    .filter(restaurant=restaurant)
                    .order_by("-total_quantity_sold"),
                )
            )
            .order_by("-product_count", "-created_date")
        )
        return categorized_products
