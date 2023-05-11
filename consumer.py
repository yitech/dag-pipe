import pika
import json
import time
from datetime import datetime
from DAG import BaseNode

# Setup RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare 'task_queue'
channel.queue_declare(queue='task_queue', durable=True)

# Setup connection to other RabbitMQ service for results
other_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
other_channel = other_connection.channel()
other_channel.queue_declare(queue='result_queue', durable=True)

def callback(ch, method, properties, body):
    node_name = body.decode()
    node = BaseNode(node_name)
    start_time = datetime.now()
    result = node.run()
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()

    print(f" [x] Received {node_name}, run result: {result}, elapsed time: {elapsed_time}s")

    result_dict = {
        'name': node_name,
        'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
        'elapsed_time': elapsed_time,
        'result': result
    }

    # Publish result to other RabbitMQ service
    other_channel.basic_publish(
        exchange='',
        routing_key='result_queue',
        body=json.dumps(result_dict),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
