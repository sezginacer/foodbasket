from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.authtoken.models import Token

from foodbasket.common.factory import ProductFactory, RestaurantFactory, UserFactory


class RestaurantResourceTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_list(self):
        url = reverse("restaurant-list")
        [RestaurantFactory() for _ in range(16)]
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("count"))
        self.assertEqual(response_data.get("count"), 16)
        self.assertIsNotNone(response_data.get("results"))

    def test_detail(self):
        restaurant = RestaurantFactory()
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        for field in ["created_date", "modified_date", "name", "uuid", "is_active"]:
            self.assertIn(field, response_data)

    def test_update(self):
        restaurant = RestaurantFactory()
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        data = {"name": "Mc. Donald's"}
        response = self.client.put(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        restaurant.refresh_from_db()
        self.assertEqual(restaurant.name, "Mc. Donald's")

        data = {"name": "Burger King"}
        response = self.client.patch(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        restaurant.refresh_from_db()
        self.assertEqual(restaurant.name, "Burger King")

    def test_delete(self):
        restaurant = RestaurantFactory()
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

        restaurant = RestaurantFactory()
        ProductFactory(restaurant=restaurant)

        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        detail = response_data.get("detail", "")
        self.assertIn("There are some references to it:", detail)

    def test_create(self):
        url = reverse("restaurant-list")
        data = {"name": "Burger King"}
        response = self.client.post(
            url, data=data, content_type="application/json", **self.auth_headers
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
