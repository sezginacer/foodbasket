from django.conf import settings
from django.db.models import Sum, Q, Count, Prefetch

from foodbasket.orders.enums import OrderStatus
from foodbasket.products.models import Product, Category


class RestaurantService(object):
    def get_popular_products(self, restaurant, limit=None):  # noqa
        limit = limit or settings.RESTAURANT_DETAIL_POPULAR_PRODUCTS_LIMIT

        popular_products = (
            Product.objects.alias(
                total_quantity_sold=Sum(
                    "order_items__quantity",
                    filter=Q(order_items__order__status__in=[OrderStatus.DELIVERED]),
                )
            )
            .filter(restaurant=restaurant, is_active=True, total_quantity_sold__gt=0)
            .order_by("-total_quantity_sold", "-created_date")[:limit]
        )
        return popular_products

    def get_categories_with_products(self, restaurant):  # noqa
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
                    .filter(restaurant=restaurant, is_active=True)
                    .order_by("-total_quantity_sold"),
                )
            )
            .order_by("-product_count", "-created_date")
        )
        return categorized_products
