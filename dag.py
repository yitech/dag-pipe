from collections import deque
from node import Node

class DAG:
    def __init__(self):
        self.nodes = []
        self.indegree = {}

    def add_node(self, node):
        self.nodes.append(node)
        self.indegree[node] = 0

    def add_edge(self, node1, node2):
        node1.neighbor.append(node2)
        self.indegree[node2] += 1

    def find_nodes_with_no_incoming_edges(self):
        return [node for node in self.nodes if self.indegree[node] == 0]
