from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from foodbasket.users.models import User
from foodbasket.utils.users import generate_username


class LoginSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):  # noqa
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField()
    username = serializers.CharField(
        max_length=150,
        default=generate_username,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def validate_password(self, password):  # noqa
        django_validate_password(password)
        return password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
