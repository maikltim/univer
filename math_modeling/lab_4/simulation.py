from config import *

class Simulation:
    def __init__(self, room, heater, environment, thermostat):
        self.room = room
        self.heater = heater
        self.environment = environment
        self.thermostat = thermostat
        self.budget = MAX_BUDGET

        self.history = {
            "room_temp": [],
            "env_temp": [],
            "heater": [],
            "budget": []
        }

    def run(self):
        for t in range(TOTAL_MINUTES):
            env_temp = self.environment.temperature(t)

            self.thermostat.control(self.room.temperature, self.heater)

            if self.heater.is_on:
                self.room.heat(KN)
                self.budget -= self.heater.energy_cost_per_minute()
            else:
                self.room.cool(KO)

            self.history["room_temp"].append(self.room.temperature)
            self.history["env_temp"].append(env_temp)
            self.history["heater"].append(int(self.heater.is_on))
            self.history["budget"].append(self.budget)

            if self.budget <= 0:
                print(f"Средства закончились на {t / 1440:.2f} дне")
                break

        return self.history
