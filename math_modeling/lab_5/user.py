class User:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.traffic_used = 0

    def request(self, website):
        data = website.send_data()
        self.traffic_used += data
        return data
