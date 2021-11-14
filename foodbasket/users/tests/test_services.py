from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from foodbasket.common.factory import UserFactory
from foodbasket.users.models import User
from foodbasket.users.service import AccountService


class AccountServiceTestCase(TestCase):
    def setUp(self):
        self.service = AccountService()

    def test_register(self):
        first_name = "John"
        last_name = "Doe"
        username = "john.doe"
        email = "john.doe@test.com"
        password = "12345"

        self.service.register(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        qs = User.objects.filter(email=email)
        self.assertEqual(qs.count(), 1)

        user = qs.get()
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)

    def test_authenticate(self):
        email = "test@test.com"
        password = "12345"
        user = UserFactory(email=email, password=make_password(password))

        credentials = {"email": email, "password": password}
        auth_user, token = self.service.authenticate(request=None, **credentials)
        self.assertIsNotNone(user)
        self.assertIsNotNone(token)
        self.assertEqual(auth_user, user)

    def test_authenticate_inactive_user(self):
        email = "test@test.com"
        password = "12345"
        UserFactory(email=email, password=make_password(password), is_active=False)

        credentials = {"email": email, "password": password}
        with self.assertRaises(AuthenticationFailed):
            self.service.authenticate(request=None, **credentials)

    def test_authenticate_wrong_password(self):
        email = "test@test.com"
        password = "12345"
        UserFactory(email=email, password=make_password(password), is_active=False)

        credentials = {"email": email, "password": "abcde"}
        with self.assertRaises(AuthenticationFailed):
            self.service.authenticate(request=None, **credentials)
