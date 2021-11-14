from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.authtoken.models import Token

from foodbasket.common.factory import UserFactory


class UserResourceTestCase(TestCase):
    def setUp(self):
        user = UserFactory(is_staff=True)
        token = Token.objects.create(user=user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

    def test_list(self):
        url = reverse("user-list")
        [UserFactory() for _ in range(18)]
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("count"))
        self.assertEqual(response_data.get("count"), 18 + 1)  # +1 initial user (setUp)
        self.assertIsNotNone(response_data.get("results"))

    def test_detail(self):
        user = UserFactory()
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        for field in [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
        ]:
            self.assertIn(field, response_data)

    def test_update(self):
        user = UserFactory()
        url = reverse("user-detail", kwargs={"pk": user.id})

        data = {"first_name": "John"}
        response = self.client.put(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            url, data=data, **self.auth_headers, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        user = UserFactory()
        url = reverse("user-detail", kwargs={"pk": user.id})

        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create(self):
        url = reverse("user-list")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "password": "12345",
            "email": "john.doe@test.com",
        }
        response = self.client.post(
            url, data=data, content_type="application/json", **self.auth_headers
        )
        self.assertEqual(response.status_code, http_status.HTTP_405_METHOD_NOT_ALLOWED)
