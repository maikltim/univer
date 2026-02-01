import matplotlib.pyplot as plt

from config import *
from room import Room
from heater import Heater
from environment import Environment
from thermostat import Thermostat
from simulation import Simulation

room = Room(initial_temp=18)
heater = Heater(POWER_KW, PRICE_PER_KWH)
environment = Environment(T_ENV_MIN, T_ENV_MAX, ENV_PERIOD)
thermostat = Thermostat(HEATER_ON_TEMP, HEATER_OFF_TEMP)

sim = Simulation(room, heater, environment, thermostat)
data = sim.run()

plt.figure(figsize=(12, 6))
plt.plot(data["room_temp"], label="Температура в помещении")
plt.plot(data["env_temp"], label="Температура среды")
plt.xlabel("Время, мин")
plt.ylabel("Температура, °C")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(data["budget"], label="Остаток средств")
plt.xlabel("Время, мин")
plt.ylabel("Руб")
plt.legend()
plt.grid()
plt.show()
