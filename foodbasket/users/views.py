from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from foodbasket.users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from foodbasket.users.service import AccountService


class TokenView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    throttle_scope = "token"

    service = AccountService()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, token = self.service.authenticate(request, **serializer.validated_data)
        return Response({"auth_token": token.key})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    register_serializer = RegisterSerializer
    response_serializer = UserSerializer
    throttle_scope = "register"

    service = AccountService()

    def post(self, request, *args, **kwargs):
        register_serializer = self.register_serializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)

        user = self.service.register(**register_serializer.validated_data)
        response_serializer = self.response_serializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
