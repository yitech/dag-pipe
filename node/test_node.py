from dataclasses import dataclass
from node import BaseNode
import pika


@dataclass
class TestNode(BaseNode):

    def __post_init__(self):
        # Setup RabbitMQ connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.name))
        self.channel = self.connection.channel()

    def callback(self):
