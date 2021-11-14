import sys

sys.path.append("..")  # in order to import from demo, pubsub & foodbasket modules.

from demo.service import FoodBasketDemoCustomerService  # noqa


def main():
    service = FoodBasketDemoCustomerService(email="cyaldiz@yspt.com", password="12345")
    service.order_flood()


if __name__ == "__main__":
    main()
