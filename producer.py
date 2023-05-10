import pika

def send_task(task):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=task,
                          properties=pika.BasicProperties(delivery_mode=2))
    print(f"Sent task: {task}")
    connection.close()

if __name__ == '__main__':
    for i in range(10):
        send_task(f"Example Task {i}")