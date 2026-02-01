class Thermostat:
    def __init__(self, t_on, t_off):
        self.t_on = t_on
        self.t_off = t_off

    def control(self, room_temp, heater):
        if room_temp <= self.t_on:
            heater.is_on = True
        elif room_temp >= self.t_off:
            heater.is_on = False
