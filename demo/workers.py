import random
import sys
import time

sys.path.append("..")  # in order to import from demo, pubsub & foodbasket modules.

from demo.service import FoodBasketDemoAdminService  # noqa
from foodbasket.orders.enums import OrderStatus  # noqa
from pubsub.redis import RedisPubSub  # noqa

BOARD = "orders"
COOKING = "cooking"
CARRIER = "carry"
CASHIER = "cashier"

ps = RedisPubSub()

service = FoodBasketDemoAdminService(email="admin@admin.com", password="12345")


@ps.subscriber(BOARD)
def approve_or_reject(data):
    time.sleep(1)
    order_number = data["number"]

    approve = random.randint(1, 20) != 10  # reject 5% of incoming orders
    if approve:
        succeeded = service.update_order(order_number, status=OrderStatus.APPROVED)
        if succeeded:
            ps.publish(COOKING, data)
            print(f"Order ({order_number}) approved.")
        return

    succeeded = service.update_order(order_number, status=OrderStatus.CANCELLED)
    if succeeded:
        print(f"Order ({order_number}) cancelled.")


@ps.subscriber(COOKING)
def prepare(data):
    order_number = data["number"]
    time.sleep(3)
    succeeded = service.update_order(order_number, status=OrderStatus.PREPARING)
    if succeeded:
        ps.publish(CARRIER, data)
        print(f"Order ({order_number}) prepared.")


@ps.subscriber(CARRIER)
def carry(data):
    order_number = data["number"]
    succeeded = service.update_order(order_number, status=OrderStatus.ON_THE_WAY)
    time.sleep(3)
    if succeeded:
        ps.publish(CASHIER, data)
        print(f"Order ({order_number}) on the way.")


@ps.subscriber(CASHIER)
def delivered(data):
    order_number = data["number"]
    succeeded = service.update_order(order_number, status=OrderStatus.DELIVERED)
    if succeeded:
        print(f"Order ({order_number}) delivered.")


if __name__ == "__main__":
    ps.start()
