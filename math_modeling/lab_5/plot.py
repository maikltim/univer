import matplotlib.pyplot as plt

from user import User
from website import Website
from provider import Provider
from simulation import Simulation
from network_graph import build_network
from config import SIMULATION_TIME

users = [
    User("User1", 100),
    User("User2", 80),
    User("User3", 120),
]

websites = [
    Website("SiteA"),
    Website("SiteB"),
]

provider = Provider()

sim = Simulation(users, provider, websites)
sim.run(SIMULATION_TIME)

names = [u.name for u in users]
traffic = [u.traffic_used for u in users]
balances = [u.balance for u in users]

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.bar(names, traffic)
plt.title("Использованный трафик (МБ)")
plt.ylabel("МБ")
plt.grid(axis="y")

plt.subplot(1, 2, 2)
plt.bar(names, balances)
plt.title("Остаток средств")
plt.ylabel("руб")
plt.grid(axis="y")

plt.tight_layout()
plt.show()
