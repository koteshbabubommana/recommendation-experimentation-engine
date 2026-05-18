import json
import os
from app.utils.logger import logger

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class EventProducer:
    def __init__(self):
        self.producer = None

        if KafkaProducer:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
            except Exception:
                self.producer = None

    def publish_event(self, topic: str, event: dict):
        if not self.producer:
            logger.info("Kafka unavailable. Event simulated: %s", event)
            return False

        self.producer.send(topic, event)
        self.producer.flush()
        return True


event_producer = EventProducer()