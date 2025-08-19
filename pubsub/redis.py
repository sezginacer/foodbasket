import logging
import redis
from typing import Optional

from pubsub.base import PubSub
from pubsub.serializer import JsonSerializer

logger = logging.getLogger(__name__)


class RedisPubSub(PubSub):
    serializer_class = JsonSerializer

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 1, 
                 max_retries: int = 3, retry_delay: float = 1.0):
        super().__init__()
        self.host = host
        self.port = port
        self.db = db
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._redis_client: Optional[redis.StrictRedis] = None
        self._pubsub_client: Optional[redis.client.PubSub] = None

    @property
    def redis_client(self) -> redis.StrictRedis:
        if self._redis_client is None:
            self._redis_client = redis.StrictRedis(
                host=self.host, 
                port=self.port, 
                db=self.db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
        return self._redis_client

    def publish(self, channel: str, data: dict) -> None:
        try:
            serialized_data = self.serialize(data)
            self.redis_client.publish(channel, serialized_data)
            logger.debug(f"Published message to channel {channel}")
        except redis.RedisError as e:
            logger.error(f"Failed to publish message to channel {channel}: {e}")
            raise

    def start(self) -> None:
        try:
            self._pubsub_client = self.redis_client.pubsub()
            self._pubsub_client.psubscribe(*self.registry)
            
            logger.info(f"Starting Redis PubSub listener on {self.host}:{self.port}")
            
            for message in self._pubsub_client.listen():
                if message.get("type") != "pmessage":
                    continue

                try:
                    channel = message.get("channel")
                    data = message.get("data") or ""
                    
                    if not data:
                        continue
                        
                    message_data = self.deserialize(data)
                    
                    for subscriber in self.registry.get(channel.decode(), []):
                        try:
                            subscriber(message_data)
                        except Exception as e:
                            logger.error(f"Error in subscriber for channel {channel}: {e}")
                            
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except redis.RedisError as e:
            logger.error(f"Redis connection error: {e}")
            raise
        except KeyboardInterrupt:
            logger.info("PubSub listener stopped by user")
        finally:
            if self._pubsub_client:
                self._pubsub_client.close()

    def close(self) -> None:
        """Close Redis connections"""
        if self._pubsub_client:
            self._pubsub_client.close()
        if self._redis_client:
            self._redis_client.close()
