"""foodbasket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from foodbasket.orders.resources.views import OrderViewSet, StatusView
from foodbasket.products.resources.views import CategoryViewSet, ProductViewSet
from foodbasket.restaurants.resources.views import RestaurantViewSet
from foodbasket.users.resources.views import UserViewSet

router = SimpleRouter()
router.register("orders", OrderViewSet)
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("restaurants", RestaurantViewSet)
router.register("users", UserViewSet)

api_urls = router.urls + [
    path("status/", StatusView.as_view(), name="status"),
]

urlpatterns = [
    path("users/", include("foodbasket.users.urls")),
    path("products/", include("foodbasket.products.urls")),
    path("restaurants/", include("foodbasket.restaurants.urls")),
    path("orders/", include("foodbasket.orders.urls")),
    path("api/v1/", include(api_urls)),
]
