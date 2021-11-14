from django.conf import settings
from django.db import transaction

from foodbasket.common.pubsub import get_pubsub


def publish_order(instance, created=False, **kwargs):
    if not created:
        return

    from foodbasket.orders.serializers import OrderSerializer

    pubsub = get_pubsub()
    serializer = OrderSerializer(instance)
    transaction.on_commit(
        lambda: pubsub.publish(settings.ORDER_PUBSUB_CHANNEL, serializer.data)
    )
