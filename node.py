class Node:
    def __init__(self, name):
        self.name = name
        self.neighbor = []

    def run(self):
        import time
        time.sleep(1)
        return self.name

