from collections import defaultdict
from typing import Callable, Type

from django.utils.functional import cached_property

from pubsub.serializer import Serializer


class PubSub:
    """
    Subscription Usage
    >>> ps = PubSub()
    >>>
    >>> @ps.subscriber("a-channel")
    >>> def subscriber_a(msg_data):
    >>>     print(f"Here is the message arrived at a-channel: {msg_data}")
    >>>
    >>> @ps.subscriber("b-channel")
    >>> def subscriber_b(msg_data):
    >>>     print(f"Here is the message arrived at b-channel: {msg_data}")
    >>>
    >>> ps.start()
    """

    serializer_class: Type[Serializer] = None

    def __init__(self):
        super().__init__()
        self.registry = defaultdict(list)

    @cached_property
    def serializer(self) -> Serializer:
        return self.serializer_class()

    def publish(self, channel: str, data: dict) -> None:
        raise NotImplementedError

    def subscriber(self, channel: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.registry[channel].append(func)
            return func

        return decorator

    def start(self) -> None:
        # wait for messages
        raise NotImplementedError

    def serialize(self, data: dict):
        return self.serializer.serialize(data)

    def deserialize(self, raw: str):
        return self.serializer.deserialize(raw)
