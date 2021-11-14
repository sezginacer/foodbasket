from django.urls import path

from foodbasket.restaurants.views import RestaurantDetailView, RestaurantListView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="list-restaurant"),
    path("<uuid>/", RestaurantDetailView.as_view(), name="detail-restaurant"),
]
