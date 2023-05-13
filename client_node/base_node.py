from dataclasses import dataclass, field
from typing import List, Type


@dataclass()
class BaseNode:
    name: str
    neighbors: List['BaseNode'] = field(default_factory=list)

    def add_neighbor(self, node: 'BaseNode'):
        self.neighbors.append(node)

    def run(self):
        print(f'This is {self.name}')
        print(f'Next node have')
        return 0

