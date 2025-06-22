import networkx as nx
import numpy as np
import random

# Создание симулированного графа (замените реальными данными из ВКонтакте)
# 51 узел (вы + 50 друзей), ~200 рёбер
G = nx.erdos_renyi_graph(n=51, p=0.154)
while nx.number_of_edges(G) < 190 or nx.number_of_edges(G) > 210:
    G = nx.erdos_renyi_graph(n=51, p=0.154)

# Это я
you = 0

# Расчет локального коэффициента кластеризации
local_cc = nx.clustering(G, you)
print(f"Локальный коэффициент кластеризации для вас: {local_cc:.4f}")

# Расчет среднего коэффициента кластеризации
avg_cc = nx.average_clustering(G)
print(f"Средний коэффициент кластеризации: {avg_cc:.4f}")

# Расчет средней длины пути
if nx.is_connected(G):
    avg_path_length = nx.average_shortest_path_length(G)
    print(f"Средняя длина пути: {avg_path_length:.4f}")
else:
    print("Граф несвязный; расчет для наибольшей компоненты связности")
    largest_cc = max(nx.connected_components(G), key=len)
    G_largest = G.subgraph(largest_cc)
    avg_path_length = nx.average_shortest_path_length(G_largest)
    print(f"Средняя длина пути (наибольшая компонента): {avg_path_length:.4f}")

# Сравнение со случайным графом
n = G.number_of_nodes()
avg_degree = sum(dict(G.degree()).values()) / n
L_random = np.log(n) / np.log(avg_degree)
print(f"Ожидаемая средняя длина пути в случайном графе: {L_random:.4f}")

# Средняя длина пути в полносвязном графе
L_complete = 1.0
print(f"Средняя длина пути в полносвязном графе: {L_complete:.4f}")

# Время диффузии информации
diffusion_time = avg_path_length * 0.5
print(f"Время распространения информации по кластеру: {diffusion_time:.2f} дней")