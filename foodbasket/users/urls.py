from django.urls import path

from foodbasket.users.views import RegisterView, TokenView

urlpatterns = [
    path("token/", TokenView.as_view(), name="token"),
    path("register/", RegisterView.as_view(), name="register"),
]
