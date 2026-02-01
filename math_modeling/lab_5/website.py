import random

class Website:
    def __init__(self, name):
        self.name = name

    def send_data(self):
        return random.randint(1, 10)
