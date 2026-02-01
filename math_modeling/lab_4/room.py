class Room:
    def __init__(self, initial_temp):
        self.temperature = initial_temp

    def heat(self, kn):
        self.temperature += kn

    def cool(self, ko):
        self.temperature -= ko
