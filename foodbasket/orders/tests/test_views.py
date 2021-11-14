from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status as http_status
from rest_framework.authtoken.models import Token

from foodbasket.common.factory import ProductFactory, RestaurantFactory, UserFactory
from foodbasket.orders.enums import OrderStatus


class OrderCompleteViewTestTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.inactive_user = UserFactory(is_active=False)
        self.order_complete_url = reverse_lazy("order-complete")

    def generate_successful_order_data(self):  # noqa
        restaurant = RestaurantFactory()
        product_1 = ProductFactory(restaurant=restaurant)
        product_2 = ProductFactory(restaurant=restaurant)
        data = {
            "items": [
                {"product": product_1.pk, "quantity": 1},
                {"product": product_2.pk, "quantity": 2},
            ],
        }
        return data

    def get_auth_headers(self, user):  # noqa
        token, _ = Token.objects.get_or_create(user=user)
        return {"HTTP_AUTHORIZATION": f"Token {user.auth_token.key}"}

    def send_complete_order_request(self, data, user=None):
        user = user or self.user
        response = self.client.post(
            self.order_complete_url,
            data=data,
            content_type="application/json",
            **self.get_auth_headers(user),
        )
        return response

    def test_order_complete_with_inactive_user(self):
        data = self.generate_successful_order_data()
        response = self.send_complete_order_request(data=data, user=self.inactive_user)
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)

    def test_order_complete_without_items(self):
        response = self.send_complete_order_request(data={})
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("items", response_data)
        self.assertIn("This field is required.", response_data["items"])

    def test_order_complete_multiple_restaurant_products(self):
        product_1 = ProductFactory()
        product_2 = ProductFactory()
        data = {
            "items": [
                {"product": product_1.pk, "quantity": 1},
                {"product": product_2.pk, "quantity": 2},
            ],
        }
        self.assertNotEqual(product_1.restaurant_id, product_2.restaurant_id)

        response = self.send_complete_order_request(data)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn("items", response_data)
        self.assertIn(
            "Each item must be from the same restaurant.", response_data["items"]
        )

    def test_order_complete_with_inactive_product_and_restaurant(self):
        product_1 = ProductFactory(is_active=False)
        product_2 = ProductFactory(restaurant__is_active=False)
        data = {
            "items": [
                {"product": product_1.pk, "quantity": 1},
                {"product": product_2.pk, "quantity": 1},
            ]
        }
        response = self.send_complete_order_request(data)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn("items", data)

        self.assertEqual(len(response_data["items"]), 2)
        self.assertIn("product", response_data["items"][0])
        self.assertIn("product", response_data["items"][1])

    def test_order_complete_success(self):
        data = self.generate_successful_order_data()
        response = self.send_complete_order_request(data=data)
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("number"))
        self.assertIsNotNone(response_data.get("amount"))
        self.assertEqual(response_data.get("status"), OrderStatus.WAITING_APPROVE)

        order_items = response_data.get("order_items")
        self.assertIsNotNone(order_items)
        self.assertEqual(len(order_items), 2)

        self.assertSetEqual(
            set([item["product"]["id"] for item in order_items]),
            set([item["product"] for item in data["items"]]),
        )
