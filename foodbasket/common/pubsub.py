from django.conf import settings
from django.utils.module_loading import import_string

from pubsub.base import PubSub


def get_pubsub() -> PubSub:
    config = settings.PUBSUB_CONFIG
    klass = import_string(config["class"])
    return klass(**config["options"])
