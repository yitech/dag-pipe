import time
import pika  # RabbitMQ client library
import json

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
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)

        # List of nodes with no incoming edges
        zero_indegree = [node for node in self.nodes if node.indegree == 0]

        while zero_indegree:
            # Get node with no incoming edges
            node = zero_indegree.pop(0)

            # Run the node and push to RabbitMQ
            # node.run()
            message = node.name
            channel.basic_publish(exchange='',
                                  routing_key='task_queue',
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode = 2,  # make message persistent
                                  ))

            # Decrease indegree of neighbors
            for neighbor in node.neighbors:
                neighbor.indegree -= 1
                if neighbor.indegree == 0:
                    zero_indegree.append(neighbor)

        # Close RabbitMQ connection
        connection.close()


if __name__ == '__main__':
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


    def callback(ch, method, properties, body):
        result_dict = json.loads(body)
        print(f"Received result: {result_dict}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # Setup RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue='result_queue', durable=True)

    # Consume messages from queue
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='result_queue', on_message_callback=callback)

    print(' [*] Waiting for results. To exit press CTRL+C')
    channel.start_consuming()