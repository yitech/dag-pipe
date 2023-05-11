from .dag import DAG
from .node import Node
from .consumer import consume
import pika

def main():
    dag = DAG()
    # Add your nodes and edges here

    nodes_without_incoming_edges = dag.find_nodes_with_no_incoming_edges()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')

    for node in nodes_without_incoming_edges:
        channel.basic_publish(exchange='', routing_key='my_queue', body=node.name)

    consume('my_queue')
