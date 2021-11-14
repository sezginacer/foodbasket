from django.conf import settings
from django.utils.module_loading import import_string


def get_pubsub():
    config = settings.PUBSUB_CONFIG
    klass = import_string(config["class"])
    return klass(**config["options"])
