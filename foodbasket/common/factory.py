from factory import LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order
from foodbasket.products.models import Category, Product
from foodbasket.restaurants.models import Restaurant
from foodbasket.users.models import User


class UserFactory(DjangoModelFactory):
    username = fuzzy.FuzzyText(length=15)
    first_name = fuzzy.FuzzyText(length=15)
    last_name = fuzzy.FuzzyText(length=15)
    email = LazyAttribute(lambda obj: "%s@example.com" % obj.username)

    class Meta:
        model = User


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant


class OrderFactory(DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    user = SubFactory(UserFactory)
    number = fuzzy.FuzzyText(length=12, chars="0123456789")
    amount = fuzzy.FuzzyDecimal(10000)
    status = fuzzy.FuzzyChoice(choices=list(map(int, OrderStatus)))

    class Meta:
        model = Order


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category


class ProductFactory(DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    category = SubFactory(CategoryFactory)
    name = fuzzy.FuzzyText(length=25)
    price = fuzzy.FuzzyDecimal(10000)

    class Meta:
        model = Product