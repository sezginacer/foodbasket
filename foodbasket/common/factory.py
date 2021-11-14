from factory import LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from foodbasket.orders.enums import OrderStatus
from foodbasket.orders.models import Order, OrderItem
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
    name = fuzzy.FuzzyText(length=49)

    class Meta:
        model = Restaurant


class CategoryFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=25)

    class Meta:
        model = Category


class ProductFactory(DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    category = SubFactory(CategoryFactory)
    name = fuzzy.FuzzyText(length=25)
    price = fuzzy.FuzzyDecimal(100)

    class Meta:
        model = Product


class OrderFactory(DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    user = SubFactory(UserFactory)
    number = fuzzy.FuzzyText(length=12, chars="0123456789")
    amount = fuzzy.FuzzyDecimal(100)
    status = fuzzy.FuzzyChoice(choices=OrderStatus.values)

    class Meta:
        model = Order


class OrderItemFactory(DjangoModelFactory):
    quantity = fuzzy.FuzzyChoice(choices=[1, 3, 5])
    amount = fuzzy.FuzzyDecimal(20)
    order = SubFactory(OrderFactory)
    product = SubFactory(ProductFactory)

    class Meta:
        model = OrderItem
