from dataclasses import dataclass


@dataclass()
class BaseNode:
    name: str

    def run(self):
        print(f'This is {self.name}')
        return 0

