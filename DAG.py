import time
import aio_pika
import pika  # RabbitMQ client library
import json
import queue

class BaseNode:
    def __init__(self, name: str):
        self.name = name
        self.neighbors = []
        self.indegree = 0

    def add_neighbor(self, node):
        self.neighbors.append(node)
        node.indegree += 1

    def run(self):
        print(f'Running {self.name}')
        time.sleep(1)
        return 1


class DAG:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: BaseNode):
        self.nodes.append(node)

    def add_edge(self, start_node: BaseNode, end_node: BaseNode):
        start_node.add_neighbor(end_node)

    def kahn_algorithm(self):
        # Setup RabbitMQ connection and channel
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # Declare task queue
        task_queue = connection.channel()
        task_queue.queue_declare(queue='task_queue', durable=True)

        # Declare result queue
        result_queue = connection.channel()
        result_queue.queue_declare(queue='result_queue', durable=True)

        # List of nodes with no incoming edges
        zero_indegree = [node for node in self.nodes if node.indegree == 0]

        for node in zero_indegree:
            message = node.name
            task_queue.basic_publish(exchange='',
                                     routing_key='task_queue',
                                     body=message,
                                     properties=pika.BasicProperties(
                                         delivery_mode=2,  # make message persistent
                                     ))

        def callback(ch, method, properties, body):
            result_dict = json.loads(body)
            print(f"Received result: {result_dict}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            node = [node for node in self.nodes if node.name == result_dict['name']][0]
            for neighbor in node.neighbors:
                neighbor.indegree -= 1
                if neighbor.indegree == 0:
                    message = neighbor.name
                    task_queue.basic_publish(exchange='',
                                             routing_key='task_queue',
                                             body=message,
                                             properties=pika.BasicProperties(
                                                 delivery_mode=2,  # make message persistent
                                             ))
        # Consume messages from queue
        result_queue.basic_qos(prefetch_count=1)
        result_queue.basic_consume(queue='result_queue', on_message_callback=callback)
        result_queue.start_consuming()

        # Close RabbitMQ connection
        connection.close()


def purge_queue(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    while method_frame:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        method_frame, header_frame, body = channel.basic_get(queue=queue_name)

    connection.close()

if __name__ == '__main__':
    purge_queue('task_queue')
    purge_queue('result_queue')
    # Create a Directed Acyclic Graph (DAG)
    dag = DAG()

    # Create some nodes
    node1 = BaseNode('Node 1')
    node2 = BaseNode('Node 2')
    node3 = BaseNode('Node 3')
    node4 = BaseNode('Node 4')

    # Add nodes to the DAG
    dag.add_node(node1)
    dag.add_node(node2)
    dag.add_node(node3)
    dag.add_node(node4)

    # Add edges
    dag.add_edge(node1, node2)
    dag.add_edge(node1, node3)
    dag.add_edge(node2, node4)
    dag.add_edge(node3, node4)

    # Run Kahn's algorithm
    dag.kahn_algorithm()
