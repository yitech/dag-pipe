import time


class BaseNode:
    def __init__(self, name: str):
        self.name = name

    def run(self):
        print(f'print {self.name}')
        time.sleep(1)
        return 0
