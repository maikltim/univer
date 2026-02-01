class Heater:
    def __init__(self, power_kw, price_per_kwh):
        self.power_kw = power_kw
        self.price_per_kwh = price_per_kwh
        self.is_on = False

    def energy_cost_per_minute(self):
        return (self.power_kw / 60) * self.price_per_kwh
