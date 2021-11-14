from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from foodbasket.users.models import User
from foodbasket.users.resources.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["first_name", "last_name", "email", "is_staff"]
    ordering_fields = ["date_joined"]
