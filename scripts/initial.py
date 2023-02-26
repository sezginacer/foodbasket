from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from foodbasket.products.models import Category, Product
from foodbasket.restaurants.models import Restaurant
from foodbasket.users.models import User

categories = [
    {"name": "Döner/Kebap", "uuid": "02457146-d4e1-4786-8090-60eba993c1c2"},
    {"name": "Ev Yemekleri", "uuid": "662ee573-55d4-4107-abad-842908e0312a"},
    {"name": "Fast-Food", "uuid": "77217e0f-7c68-4237-8ec5-8a3494cd4b2c"},
]
restaurants = [
    {"name": "Süper Dönerci", "uuid": "4669decf-8505-47c0-af86-8a1446dd02b2"},
    {
        "name": "Harika Ev Yemekleri",
        "uuid": "2974b6c5-6b12-4f3e-a705-92e799db8939",
    },
    {"name": "Bizim Büfe", "uuid": "b043c421-84d5-4c07-bfe3-5a5b751c1ddd"},
]
products = [
    {
        "name": "Döner",
        "price": 18,
        "category": "Döner/Kebap",
        "restaurant": "Süper Dönerci",
    },
    {
        "name": "İskender",
        "price": 35,
        "category": "Döner/Kebap",
        "restaurant": "Süper Dönerci",
    },
    {
        "name": "Etibol İskender",
        "price": 45,
        "category": "Döner/Kebap",
        "restaurant": "Süper Dönerci",
    },
    {
        "name": "Kuru Fasülye",
        "price": 12,
        "category": "Ev Yemekleri",
        "restaurant": "Harika Ev Yemekleri",
    },
    {
        "name": "Pilav",
        "price": 10,
        "category": "Ev Yemekleri",
        "restaurant": "Harika Ev Yemekleri",
    },
    {
        "name": "Mercibek Çorbası",
        "price": 15,
        "category": "Ev Yemekleri",
        "restaurant": "Harika Ev Yemekleri",
    },
    {
        "name": "Goralı",
        "price": 11,
        "category": "Fast-Food",
        "restaurant": "Bizim Büfe",
    },
    {
        "name": "Dilli Kaşarlı",
        "price": 13,
        "category": "Fast-Food",
        "restaurant": "Bizim Büfe",
    },
    {
        "name": "Yengen",
        "price": 15,
        "category": "Fast-Food",
        "restaurant": "Bizim Büfe",
    },
]
users = [
    {
        "first_name": "Admin",
        "last_name": "Admin",
        "email": "admin@admin.com",
        "username": "admin",
        "password": "12345",
        "is_staff": True,
        "auth_token": "607a43a38913b55941d872c3eba107e5e19690c4",
    },
    {
        "first_name": "Uğur",
        "last_name": "Özi",
        "email": "uozy@yspt.com",
        "username": "ugur.ozi",
        "password": "12345",
        "auth_token": "984000329965c46bb54043776f5438f500538340",
    },
    {
        "first_name": "Cenk",
        "last_name": "Yaldız",
        "email": "cyaldiz@yspt.com",
        "username": "cenk.yaldiz",
        "password": "12345",
        "auth_token": "a7a5881bc0807982cf6af5d83866ade7d6bd4471",
    },
    {
        "first_name": "Selin",
        "last_name": "Simge",
        "email": "ssimge@yspt.com",
        "username": "selin.simge",
        "password": "12345",
        "auth_token": "edf5c43db06c17a1fb84bfd478cf1ae5e6d832fd",
    },
]


def check(model):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # if any instance of that model does not exists, then create.
            if not model.objects.exists():
                return func(*args, **kwargs)

        return wrapper

    return decorator


@check(Category)
def create_categories():
    Category.objects.bulk_create([Category(**c) for c in categories])
    print("categories.. done")


@check(Restaurant)
def create_restaurants():
    Restaurant.objects.bulk_create([Restaurant(**r) for r in restaurants])
    print("restaurants.. done")


@check(Product)
def create_products():
    products_ = []
    for p in products:
        category = Category.objects.only("pk").get(name=p.pop("category"))
        restaurant = Restaurant.objects.only("pk").get(name=p.pop("restaurant"))
        products_.append(Product(category_id=category.pk, restaurant_id=restaurant.pk, **p))
    Product.objects.bulk_create(products_)
    print("products.. done")


@check(User)
def create_users():
    users_ = []
    tokens = []
    for u in users:
        password = make_password(u.pop("password"))
        auth_token = u.pop("auth_token")
        user = User(password=password, **u)
        users_.append(user)
        tokens.append(Token(user=user, key=auth_token))
    User.objects.bulk_create(users_)
    Token.objects.bulk_create(tokens)
    print("users.. done")


def run():
    create_categories()
    create_restaurants()
    create_products()
    create_users()
