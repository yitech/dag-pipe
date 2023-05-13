from dataclasses import dataclass
from node import BaseNode
import pika
import uuid
import time

@dataclass
class TestNode(BaseNode):

    def __post_init__(self):
        # Setup RabbitMQ connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.name))
        self.channel = self.connection.channel()

    def callback(self, ch, method, properties, body):
        # Print self.name and wait len(self.name) seconds
        print(self.name)
        time.sleep(len(self.name))

        # Send a response back using the reply_to and correlation_id properties
        self.channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=str(self.name)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        # Create a unique correlation id
        correlation_id = str(uuid.uuid4())

        # Declare a queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue

        # Register the callback function with the queue
        self.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=self.callback,
            auto_ack=True)

        # Send a message to the queue
        self.channel.basic_publish(
            exchange='',
            routing_key=self.name,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=correlation_id,
            ),
            body='')

        # Start consuming from the queue
        while True:
            self.connection.process_data_events()
            if self.name:
                break
