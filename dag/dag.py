from dataclasses import dataclass
from typing import Dict, Type
from node import BaseNode


@dataclass
class DAG:
    nodes: Dict[str, Type[BaseNode]]

    def add_node(self, node: Type[BaseNode]):
        self.nodes.update({node.name: node})

    def add_edge(self, start: str, end: str):
        self.nodes[start].add_neighbor(self.nodes[end])
