from collections import defaultdict

from django.utils.functional import cached_property


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

    serializer_class = None

    def __init__(self):
        super().__init__()
        self.registry = defaultdict(list)

    @cached_property
    def serializer(self):
        return self.serializer_class()

    def publish(self, channel, data):
        raise NotImplementedError

    def subscriber(self, channel):
        def decorator(func):
            self.registry[channel].append(func)
            return func

        return decorator

    def start(self):
        # wait for messages
        raise NotImplementedError

    def serialize(self, data):
        return self.serializer.serialize(data)

    def deserialize(self, raw):
        return self.serializer.deserialize(raw)
