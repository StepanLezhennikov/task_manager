import json
from enum import Enum

from kafka import KafkaProducer

from task_manager import settings


class TOPICS(str, Enum):
    TASK_CREATED = "task.create"
    TASK_UPDATED = "task.update"
    TASK_DELETED = "task.delete"
    PROJECT_CREATED = "project.create"
    PROJECT_DELETED = "project.delete"
    USER_ADDED = "user.create"
    USER_DELETED = "user.delete"


class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_message(self, message, topic):
        try:
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
