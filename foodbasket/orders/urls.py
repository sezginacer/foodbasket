from django.urls import path

from foodbasket.orders.views import OrderCompleteView

urlpatterns = [
    path("complete/", OrderCompleteView.as_view(), name="order-complete"),
]
