import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.authtoken.models import Token

from foodbasket.common.factory import OrderFactory, OrderItemFactory, UserFactory
from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order


class OrderResourceTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        for _ in range(10):
            order = OrderFactory(status=OrderStatus.WAITING_APPROVE)
            for __ in range(random.randint(1, 4)):
                OrderItemFactory(order=order)

    def test_list(self):
        url = reverse("order-list")
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("count"))
        self.assertEqual(response_data.get("count"), 10)
        self.assertIsNotNone(response_data.get("results"))

    def test_detail(self):
        order = Order.objects.last()
        url = reverse("order-detail", kwargs={"number": order.number})

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        for field in ["created_date", "modified_date", "number", "amount", "status"]:
            self.assertIn(field, response_data)

    def test_update(self):
        order = Order.objects.last()
        url = reverse("order-detail", kwargs={"number": order.number})

        data = {"status": OrderStatus.APPROVED}
        response = self.client.put(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

        old_status = order.status
        self.assertEqual(old_status, OrderStatus.WAITING_APPROVE)

        response = self.client.patch(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.APPROVED)

    def test_delete(self):
        order = Order.objects.last()
        url = reverse("order-detail", kwargs={"number": order.number})
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create(self):
        url = reverse("order-list")
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)


class StatusViewTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}
        for _ in range(15):
            OrderFactory()

    def test_status(self):
        url = reverse("status")
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_results = {s["status"]: s["orders"] for s in response.json()}
        for status in OrderStatus:
            count = Order.objects.filter(status=status).count()
            self.assertEqual(count, response_results.get(status.label))
