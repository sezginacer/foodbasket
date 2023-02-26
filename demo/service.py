import random
import time

import requests


class FoodBasketDemoService:
    def __init__(self, email, password, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.email = email
        self._password = password
        self._token = None

    def _set_auth_token(self):
        url = f"{self.base_url}/users/token/"
        data = {"email": self.email, "password": self._password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        auth_token = response.json().get("auth_token")
        self._token = auth_token

    def _get_auth_headers(self):  # noqa
        if not self._token:
            self._set_auth_token()
        return {"Authorization": f"Token {self._token}"}


class FoodBasketDemoAdminService(FoodBasketDemoService):
    def update_order(self, order_number, **update):
        url = f"{self.base_url}/api/v1/orders/{order_number}/"
        response = requests.patch(url, json=update, headers=self._get_auth_headers())
        return response.ok


class FoodBasketDemoCustomerService(FoodBasketDemoService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._products = None

    def _fetch_products(self):
        url = f"{self.base_url}/restaurants/?limit=10"
        response = requests.get(url)
        response.raise_for_status()

        restaurant = random.choice(response.json()["results"])
        url = f"{self.base_url}{restaurant['url']}"
        response = requests.get(url)
        response.raise_for_status()

        categories = response.json()["categories"]
        category = random.choice(categories)

        self._products = category["products"]

    def _get_products(self):
        return self._products or self._fetch_products() or self._products

    def create_order(self):
        url = f"{self.base_url}/orders/complete/"
        items = []

        products = self._get_products()
        for product in random.sample(products, k=random.randint(1, len(products))):
            items.append({"product": product["pk"], "quantity": random.randint(1, 3)})

        response = requests.post(url, json={"items": items}, headers=self._get_auth_headers())
        response.raise_for_status()
        print(f"Order ({response.json()['number']}) created.")

    def _empty_products(self):
        self._products = None

    def order_flood(self):
        while True:
            self.create_order()
            s = random.randint(3, 8)
            print(f"sleeping {s} seconds..")
            time.sleep(s)

            if random.randint(1, 4) == 4:
                self._empty_products()  # empty products to select new random restaurant & category
