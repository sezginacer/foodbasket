import time

from pubsub.base import PubSub


class DummyPubSub(PubSub):
    def publish(self, channel: str, data: dict) -> None:
        pass

    def start(self) -> None:
        while True:
            time.sleep(60 * 60)
