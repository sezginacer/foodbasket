from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.authtoken.models import Token

from foodbasket.common.factory import (
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    RestaurantFactory,
    UserFactory,
)


class ProductResourceTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_list(self):
        url = reverse("product-list")
        [ProductFactory() for _ in range(12)]
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("count"))
        self.assertEqual(response_data.get("count"), 12)
        self.assertIsNotNone(response_data.get("results"))

    def test_detail(self):
        product = ProductFactory()
        url = reverse("product-detail", kwargs={"pk": product.id})

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        for field in [
            "created_date",
            "modified_date",
            "name",
            "category",
            "price",
            "restaurant",
        ]:
            self.assertIn(field, response_data)

    def test_update(self):
        product = ProductFactory()
        url = reverse("product-detail", kwargs={"pk": product.id})

        next_category = CategoryFactory()
        data = {
            "name": "Steak",
            "price": "45.00",
            "category": next_category.id,
            "restaurant": product.restaurant.id,
        }
        response = self.client.put(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "Steak")
        self.assertEqual(product.price, Decimal("45.00"))
        self.assertEqual(product.category_id, next_category.id)

        data = {"name": "Steak Burger"}
        response = self.client.patch(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "Steak Burger")

    def test_delete(self):
        product = ProductFactory()
        url = reverse("product-detail", kwargs={"pk": product.id})

        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

        product = ProductFactory()
        order = OrderFactory()
        OrderItemFactory(order=order, product=product)

        url = reverse("product-detail", kwargs={"pk": product.id})
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        detail = response_data.get("detail", "")
        self.assertIn("There are some references to it:", detail)

    def test_create(self):
        url = reverse("product-list")
        category = CategoryFactory()
        restaurant = RestaurantFactory()
        data = {
            "name": "Pizza",
            "category": category.id,
            "restaurant": restaurant.id,
            "price": "59.90",
        }
        response = self.client.post(
            url, data=data, content_type="application/json", **self.auth_headers
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)


class CategoryResourceTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_list(self):
        url = reverse("category-list")
        [CategoryFactory() for _ in range(14)]
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("count"))
        self.assertEqual(response_data.get("count"), 14)
        self.assertIsNotNone(response_data.get("results"))

    def test_detail(self):
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"pk": category.id})

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        for field in ["created_date", "modified_date", "name", "uuid"]:
            self.assertIn(field, response_data)

    def test_update(self):
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"pk": category.id})

        data = {"name": "Far East Kitchen"}
        response = self.client.put(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, "Far East Kitchen")

        data = {"name": "Cookies"}
        response = self.client.patch(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, "Cookies")

    def test_delete(self):
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"pk": category.id})

        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

        category = CategoryFactory()
        ProductFactory(category=category)

        url = reverse("category-detail", kwargs={"pk": category.id})
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        detail = response_data.get("detail", "")
        self.assertIn("There are some references to it:", detail)

    def test_create(self):
        url = reverse("category-list")
        data = {"name": "Soup"}
        response = self.client.post(
            url, data=data, content_type="application/json", **self.auth_headers
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
