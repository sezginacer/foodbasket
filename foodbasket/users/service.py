from django.contrib.auth import authenticate as django_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from foodbasket.users.models import User


class AccountService:
    def authenticate(self, request, **credentials):
        user = django_authenticate(request, **credentials)
        if not user:
            raise AuthenticationFailed()

        return user, self._get_auth_token(user)

    def _get_auth_token(self, user):  # noqa
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def register(self, first_name, last_name, email, password, username):  # noqa
        user = User(
            first_name=first_name, last_name=last_name, email=email, username=username
        )
        user.set_password(password)
        user.save()
        return user
