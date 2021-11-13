from django.urls import path

from foodbasket.restaurants.views import RestaurantDetailView, RestaurantListView

urlpatterns = [
    path("", RestaurantListView.as_view({"get": "list"}), name="restaurant-list"),
    path(
        "<uuid>/",
        RestaurantDetailView.as_view({"get": "retrieve"}),
        name="restaurant-detail",
    ),
]
