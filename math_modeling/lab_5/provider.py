from config import PRICE_PER_MB

class Provider:
    def __init__(self):
        self.income = 0

    def charge(self, user, traffic):
        cost = traffic * PRICE_PER_MB
        user.balance -= cost
        self.income += cost
        return cost
