import redis

from pubsub.base import PubSub
from pubsub.serializer import JsonSerializer


class RedisPubSub(PubSub):
    serializer_class = JsonSerializer

    def __init__(self, host="localhost", port=6379, db=1):
        super().__init__()
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def publish(self, channel, data):
        self.r.publish(channel, self.serialize(data))

    def start(self):
        p = self.r.pubsub()
        p.psubscribe(*self.registry)
        for message in p.listen():
            if message.get("type") != "pmessage":
                continue

            channel = message.get("channel")
            data = message.get("data") or ""
            message_data = self.deserialize(data)
            for subscriber in self.registry.get(channel.decode(), []):
                subscriber(message_data)
