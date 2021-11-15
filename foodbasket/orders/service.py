from django.db import transaction

from foodbasket.orders.models import Order, OrderItem


class OrderService:
    @transaction.atomic()
    def create_order(self, items, user, number, status, **kwargs):
        order = Order(user=user, number=number, status=status)
        order_items = [self.make_order_item(order=order, **item) for item in items]
        order.amount = sum(order_item.amount for order_item in order_items)
        order.restaurant = order_items[0].product.restaurant
        order.save()
        OrderItem.objects.bulk_create(order_items)
        return order

    def make_order_item(self, product, quantity, order):  # noqa
        return OrderItem(
            product=product,
            quantity=quantity,
            order=order,
            amount=product.price * quantity,
        )
