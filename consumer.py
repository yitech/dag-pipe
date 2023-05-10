import pika
import time

def process_task(task):
    # Add your task processing logic here
    print(f"Processing task: {task}")
    time.sleep(1)  # simulate task processing time
    return 0

def on_message(channel, method, properties, body):
    task = body.decode()
    result = process_task(task)
    print(f"Task done, result: {result}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=on_message)

print("Waiting for tasks...")
channel.start_consuming()
