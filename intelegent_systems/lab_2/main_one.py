from itertools import combinations
import heapq


def calculate_payback(K, C, N):
    """Вычисление срока окупаемости."""
    
    return K / (365 * C * N)


def find_optimal_plan_bruteforce(investments, costs, max_budget, min_pms, min_mso, n_trains=10):
    """Поиск оптимального плана методом частичного перебора."""
    n = len(investments)
    best_plan = None    
    best_payback = float('inf')
    
    for r in range(1, n + 1):
        for subset in combinations(range(n), r):
            total_cost = sum(investments[i] for i in subset)
            total_pms = sum(investments[i] for i in subset if i in [0, 1, 4]) # ПМС-219 (1,2,5 в списке)
            total_mso = sum(investments[i] for i in subset if i in [2, 3, 5]) # МСО-219 (3,4,6 в списке)
            total_payback = sum(calculate_payback(investments[i], costs[i], n_trains) for i in subset)
            
            if total_cost <= max_budget and total_pms >= min_pms and total_mso >= min_mso:
                if total_payback < best_payback:
                    best_payback = total_payback
                    best_plan = subset
                    
    return best_plan, best_payback


# Входные данные (вариант 1)
investments = [821250, 1825000, 1186250, 5475000, 8942500, 2628000]
costs = [150, 200, 250, 300, 350, 400]
max_budget = 12000000
min_pms = 3000000
min_mso = 4500000

best_plan_bruteforce, best_payback_bruteforce = find_optimal_plan_bruteforce(investments, costs, max_budget, min_pms, min_mso)
print("Оптимальный план (метод частичного перебора):", best_plan_bruteforce)
print("Срок окупаемости:", round(best_payback_bruteforce, 2), "лет")


