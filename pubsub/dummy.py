import time

from pubsub.base import PubSub


class DummyPubSub(PubSub):
    def publish(self, queue, data):
        pass

    def start(self):
        while True:
            time.sleep(60 * 60)
