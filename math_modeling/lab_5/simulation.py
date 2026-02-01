import random

class Simulation:
    def __init__(self, users, provider, websites):
        self.users = users
        self.provider = provider
        self.websites = websites

    def run(self, steps):
        for step in range(steps):
            user = random.choice(self.users)
            site = random.choice(self.websites)

            traffic = user.request(site)
            self.provider.charge(user, traffic)
