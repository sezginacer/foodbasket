import typing

from django.conf import settings
from django.db import transaction

from foodbasket.common.pubsub import get_pubsub

if typing.TYPE_CHECKING:
    from foodbasket.orders.models import Order


def publish_order(instance: "Order", created: bool = False, **kwargs) -> None:
    if not created:
        return

    from foodbasket.orders.serializers import OrderSerializer

    pubsub = get_pubsub()
    serializer = OrderSerializer(instance)
    transaction.on_commit(lambda: pubsub.publish(settings.ORDER_PUBSUB_CHANNEL, serializer.data))
