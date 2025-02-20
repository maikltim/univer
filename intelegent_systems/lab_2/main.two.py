from itertools import combinations
import heapq

def calculate_payback(K, C, N):
    """Вычисление срока окупаемости."""
    
    return K / (365 * C * N)



def find_optimal_plan_astar(investments, costs, max_budget, min_pms, min_mso, n_trains=10):
    """Поиск оптимального плана с использованием алгоритма A*."""
    
    heap = []
    heapq.heappush(heap, (0, [], 0, 0, 0))
    best_plan = None
    best_payback = float('inf')
    
    while heap:
        payback, plan, cost, pms, mso = heapq.heappop(heap)
        
        if cost > max_budget or pms < min_pms or mso < min_mso:
            continue
        
        if payback < best_payback:
            best_payback = payback
            best_plan = plan
            
        for i in range(len(investments)):
            if i not in plan:
                new_plan = plan + [i]
                new_cost = cost + investments[i]
                new_pms = pms + (investments[i] if i in [0, 1, 4] else 0)
                new_mso = mso + (investments[i] if i in [2, 3, 5] else 0)
                new_payback = sum(calculate_payback(investments[j], costs[j], n_trains) for j in new_plan)
                heapq.heappush(heap, (new_payback, new_plan, new_cost, new_pms, new_mso))
                
    return best_plan, best_payback
            
        

# Входные данные (вариант 1)
investments = [821250, 1825000, 1186250, 5475000, 8942500, 2628000]
costs = [150, 200, 250, 300, 350, 400]
max_budget = 12000000
min_pms = 3000000
min_mso = 4500000

best_plan_astar, best_payback_astar = find_optimal_plan_astar(investments, costs, max_budget, min_pms, min_mso)
print("Оптимальный план (алгоритм A*):", best_plan_astar)
print("Срок окупаемости:", round(best_payback_astar, 2), "лет")