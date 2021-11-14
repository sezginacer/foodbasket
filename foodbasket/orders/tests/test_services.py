from unittest.mock import patch

from django.test import TestCase

from foodbasket.common.factory import ProductFactory, UserFactory
from foodbasket.common.orders import generate_order_number
from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order
from foodbasket.orders.service import OrderService


class OrderServiceTestCase(TestCase):
    def setUp(self):
        self.service = OrderService()

    @patch("foodbasket.orders.receivers.get_pubsub")
    def test_create_order(self, m):
        user = UserFactory()
        number = generate_order_number()
        product_1, product_2 = ProductFactory(), ProductFactory()
        status = OrderStatus.WAITING_APPROVE
        data = {
            "user": user,
            "number": number,
            "status": status,
            "items": [
                {"product": product_1, "quantity": 1},
                {"product": product_2, "quantity": 2},
            ],
        }
        self.service.create_order(**data)
        order = Order.objects.filter(number=number).first()

        self.assertIsNotNone(order)
        self.assertEqual(order.user_id, user.id)
        self.assertEqual(order.status, status)

        self.assertEqual(order.order_items.count(), 2)

        order_item_1 = order.order_items.filter(product=product_1).first()
        self.assertIsNotNone(order_item_1)
        self.assertEqual(order_item_1.quantity, 1)
        self.assertEqual(order_item_1.amount, product_1.price * order_item_1.quantity)

        order_item_2 = order.order_items.filter(product=product_2).first()
        self.assertIsNotNone(order_item_2)
        self.assertEqual(order_item_2.quantity, 2)
        self.assertEqual(order_item_2.amount, product_2.price * order_item_2.quantity)

        self.assertEqual(order.amount, order_item_1.amount + order_item_2.amount)

        # as mocking signal receiver itself does not work (possibly due to module/path/reference)
        # test get_pubsub (that the receiver calls) called.
        self.assertTrue(m.called)
