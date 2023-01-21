from typing import Tuple

from django.contrib.auth import authenticate as django_authenticate
from django.http.request import HttpRequest as DjangoRequest
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request as DrfRequest

from foodbasket.users.models import User


class AccountService:
    def authenticate(
        self, request: DjangoRequest | DrfRequest, **credentials
    ) -> Tuple[User, Token]:
        user = django_authenticate(request, **credentials)
        if not user:
            raise AuthenticationFailed()

        return user, self._get_auth_token(user)

    def _get_auth_token(self, user: User) -> Token:  # noqa
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def register(
        self, first_name: str, last_name: str, email: str, password: str, username: str
    ) -> User:  # noqa
        user = User(
            first_name=first_name, last_name=last_name, email=email, username=username
        )
        user.set_password(password)
        user.save()
        return user
