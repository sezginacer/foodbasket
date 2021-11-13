from django.conf import settings
from django.db import transaction
from django.utils.module_loading import import_string


def _get_pubsub():
    config = settings.PUBSUB_CONFIG
    klass = import_string(config["class"])
    return klass(**config["options"])


def add_order_to_queue(instance, created=False, **kwargs):
    if not created:
        return

    from foodbasket.orders.serializers import OrderSerializer

    pubsub = _get_pubsub()
    serializer = OrderSerializer(instance)
    pubsub.publish(settings.ORDER_QUEUE, serializer.data)
    transaction.on_commit(lambda: pubsub.publish(settings.ORDER_QUEUE, serializer.data))
