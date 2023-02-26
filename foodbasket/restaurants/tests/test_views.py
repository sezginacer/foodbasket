import random

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse_lazy
from factory import fuzzy
from rest_framework import status as http_status

from foodbasket.common.factory import (
    CategoryFactory,
    ProductFactory,
    RestaurantFactory,
    UserFactory,
)
from foodbasket.common.orders import generate_order_number
from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.service import OrderService
from foodbasket.restaurants.models import Restaurant


class RestaurantListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse_lazy("list-restaurant")
        categories = [CategoryFactory() for _ in range(3)]
        restaurants = [RestaurantFactory() for _ in range(8)]
        for _ in range(20):
            ProductFactory(
                category=fuzzy.FuzzyChoice(choices=categories),
                restaurant=fuzzy.FuzzyChoice(choices=restaurants),
            )

    def test_restaurant_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data.get("count"), Restaurant.objects.actives().count())
        self.assertIsNotNone(response_data.get("results"))

        for result in response_data["results"]:
            self.assertIsNotNone("name", result.get("name"))
            self.assertIsNotNone("uuid", result.get("name"))
            self.assertIsNotNone("url", result.get("name"))


class RestaurantDetailViewTestCase(TestCase):
    def setUp(self):
        self.order_service = OrderService()
        restaurant = RestaurantFactory()
        self.url = restaurant.get_absolute_url()

        categories = [CategoryFactory() for _ in range(3)]
        users = [UserFactory() for _ in range(10)]
        products = [
            ProductFactory(
                restaurant=restaurant,
                category=fuzzy.FuzzyChoice(choices=categories),
            )
            for _ in range(20)
        ]

        for _ in range(30):
            products_ = random.sample(products, random.randint(1, 3))
            user = random.choice(users)
            number = generate_order_number()
            items = [{"product": product, "quantity": random.randint(1, 5)} for product in products_]
            self.order_service.create_order(items, user, number, status=random.choice(OrderStatus.values))

    @override_settings(RESTAURANT_DETAIL_POPULAR_PRODUCTS_LIMIT=3)
    def test_restaurant_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIn("restaurant", response_data)
        popular_products = response_data.get("popular_products")
        categories = response_data.get("categories")

        self.assertIsNotNone(popular_products)
        self.assertIsNotNone(categories)
        for category in categories:
            self.assertIsNotNone(category.get("name"))
            self.assertIsNotNone(category.get("products"))

        self.assertGreaterEqual(settings.RESTAURANT_DETAIL_POPULAR_PRODUCTS_LIMIT, len(popular_products))
