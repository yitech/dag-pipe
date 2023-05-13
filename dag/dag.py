from dataclasses import dataclass
from typing import Dict, Type
from node import BaseNode


@dataclass
class DAG:
    nodes: Dict[str, Type[BaseNode]]

    def add_node(self, node: Type[BaseNode]):
        self.nodes.update({node.name: node})

    def add_edge(self, start_node: Type[BaseNode], end_node: Type[BaseNode]):
        start_node.add_neighbor(end_node)
