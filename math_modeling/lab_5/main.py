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

G = build_network(users, provider, websites)

sim = Simulation(users, provider, websites)
sim.run(SIMULATION_TIME)

print("Результаты моделирования:")
for u in users:
    print(f"{u.name}: остаток {u.balance:.2f} руб, трафик {u.traffic_used} МБ")

print(f"Доход провайдера: {provider.income:.2f} руб")
