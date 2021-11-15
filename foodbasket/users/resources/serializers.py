from rest_framework import serializers

from foodbasket.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "groups", "user_permissions"]
