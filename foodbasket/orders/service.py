from django.db import transaction

from foodbasket.orders.models import Order, OrderItem


class OrderService(object):
    @transaction.atomic()
    def create_order(self, items, user, number, status, **kwargs):
        restaurant = items[0]["product"].restaurant
        order = Order(
            user=user, number=number, status=status, amount=0.00, restaurant=restaurant
        )
        order.save()

        order_items = [self._create_order_item(**item, order=order) for item in items]
        order.amount = sum(order_item.amount for order_item in order_items)
        order.save(update_fields=["amount"])
        return order

    def _create_order_item(  # noqa
        self, product, quantity, order, commit=True, **kwargs
    ):
        order_item = OrderItem(
            product=product,
            quantity=quantity,
            order=order,
            amount=product.price * quantity,
        )
        if commit:
            order_item.save()
        return order_item

    @transaction.atomic()
    def update_status(self, order, status):
        order.status = status
        order.save(update_fields=["status", "modified_date"])
        return order
