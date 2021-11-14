from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status as http_status

from foodbasket.common.factory import UserFactory
from foodbasket.users.models import User


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse_lazy("register")

    def test_register(self):
        first_name = "John"
        last_name = "Doe"
        username = "john.doe"
        email = "john.doe@test.com"
        password = "12ads;11"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password,
        }
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=email).exists())

    def test_register_existing_username(self):
        username = "test"
        UserFactory(username=username)
        data = {
            "first_name": "John",
            "Doe": "Doe",
            "username": username,
            "email": "test@test.com",
            "password": "1213.as1.2",
        }
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn("username", response_data)
        self.assertEqual(response_data["username"][0], "This field must be unique.")

    def test_register_existing_email(self):
        email = "test@test.com"
        UserFactory(email=email)
        data = {
            "first_name": "John",
            "Doe": "Doe",
            "username": "username",
            "email": email,
            "password": "1213.as1.2",
        }
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn("email", response_data)
        self.assertEqual(response_data["email"][0], "This field must be unique.")

    def test_register_weak_password(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "john.do",
            "email": "test@test.com",
            "password": "1234",
        }
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertIn("password", response_data)
        self.assertIn(
            "This password is too short. It must contain at least 8 characters.",
            response_data["password"],
        )
        self.assertIn("This password is too common.", response_data["password"])
        self.assertIn("This password is entirely numeric.", response_data["password"])


class TokenViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse_lazy("token")

    def test_token(self):
        email = "test@test.com"
        password = "12.asd.13"
        UserFactory(email=email, password=make_password(password))

        data = {"email": email, "password": password}
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data.get("auth_token"))

    def test_token_fail(self):
        data = {"email": "email_that@does-not-even-exist.com", "password": "123sad.as"}
        response = self.client.post(
            self.url, data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)
