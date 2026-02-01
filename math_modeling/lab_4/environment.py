import math

class Environment:
    def __init__(self, t_min, t_max, period):
        self.t_min = t_min
        self.t_max = t_max
        self.period = period

    def temperature(self, t_minute):
        avg = (self.t_max + self.t_min) / 2
        amp = (self.t_max - self.t_min) / 2
        return avg + amp * math.sin(2 * math.pi * t_minute / self.period)
