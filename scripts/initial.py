from django.contrib.auth.hashers import make_password
from django.db import transaction

from foodbasket.products.models import Product, Category
from foodbasket.restaurants.models import Restaurant
from foodbasket.users.models import User

categories = [
    {"name": "Döner/Kebap"},
    {"name": "Ev Yemekleri"},
    {"name": "Fast-Food"},
]
restaurants = [
    {"name": "Süper Dönerci"},
    {"name": "Harika Ev Yemekleri"},
    {"name": "Bizim Büfe"},
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
    },
    {
        "first_name": "Uğur",
        "last_name": "Özi",
        "email": "uozy@yspt.com",
        "username": "ugur.ozi",
        "password": "12345",
    },
    {
        "first_name": "Cenk",
        "last_name": "Yaldız",
        "email": "cyaldiz@yspt.com",
        "username": "cenk.yaldiz",
        "password": "12345",
    },
    {
        "first_name": "Selin",
        "last_name": "Simge",
        "email": "ssimge@yspt.com",
        "username": "selin.simge",
        "password": "12345",
    },
]


def run():
    with transaction.atomic():
        Category.objects.bulk_create([Category(**c) for c in categories])
        Restaurant.objects.bulk_create([Restaurant(**r) for r in restaurants])

        products_ = []
        for p in products:
            category = Category.objects.only("pk").get(name=p.pop("category"))
            restaurant = Restaurant.objects.only("pk").get(name=p.pop("restaurant"))
            products_.append(
                Product(category_id=category.pk, restaurant_id=restaurant.pk, **p)
            )
        Product.objects.bulk_create(products_)

        users_ = []
        for u in users:
            password = make_password(u.pop("password"))
            users_.append(User(password=password, **u))
        User.objects.bulk_create(users_)

    print("Database initialized successfully..")
