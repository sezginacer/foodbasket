from django.urls import path

from foodbasket.restaurants.views import RestaurantDetailView, RestaurantListView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant-list"),
    path("<uuid>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
]
