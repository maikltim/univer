import math


def f(x):
    return x**5 - 2*x**3 + x - 10

def df(x):
    
    return 5*x**4 - 6*x**2 + 1

epsilon = 1e-4  # Точность


def bisection_method(a, b, eps):
    if f(a) * f(b) >= 0:
        return None, 0  
    
    iterations = 0
    while (b - a) / 2 > eps:
        c = (a + b) / 2
        if f(c) == 0:
            return c, iterations + 1
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iterations += 1
    
    root = (a + b) / 2
    return root, iterations


# Преобразуем уравнение: x = (2x^3 - x + 10)^(1/5)
def phi(x):
    return (2*x**3 - x + 10)**(1/5)

def iteration_method(x0, eps, max_iter=1000):
    x_prev = x0
    iterations = 0
    
    for _ in range(max_iter):
        x_curr = phi(x_prev)
        iterations += 1
        if abs(x_curr - x_prev) < eps:
            return x_curr, iterations
        x_prev = x_curr
        
    return x_prev, iterations


def newton_method(x0, eps, max_iter=1000):
    x = x0
    iterations = 0
    
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if dfx == 0:
            break
            
        x_new = x - fx / dfx
        iterations += 1
        
        if abs(x_new - x) < eps:
            return x_new, iterations
            
        x = x_new
        
    return x, iterations


def secant_method(x0, x1, eps, max_iter=1000):
    x_prev = x0
    x_curr = x1
    iterations = 0
    
    for _ in range(max_iter):
        fx_prev = f(x_prev)
        fx_curr = f(x_curr)
        
        if fx_curr - fx_prev == 0:
            break
            
        # Формула секущих
        x_next = x_curr - fx_curr * (x_curr - x_prev) / (fx_curr - fx_prev)
        iterations += 1
        
        if abs(x_next - x_curr) < eps:
            return x_next, iterations
            
        x_prev = x_curr
        x_curr = x_next
        
    return x_curr, iterations

if __name__ == "__main__":
    print(f"Решение уравнения: x^5 - 2x^3 + x - 10 = 0")
    print(f"Точность (epsilon): {epsilon}\n")

    # Параметры для методов
    a, b = 1.0, 2.0       # Отрезок для бисекции
    x0_iter = 1.5         # Начальное приближение для итераций
    x0_newton = 2.0       # Начальное приближение для Ньютона
    x0_sec, x1_sec = 1.0, 2.0 # Два начальных приближения для секущих

    # Вычисления
    res_bis, iter_bis = bisection_method(a, b, epsilon)
    res_iter, iter_iter = iteration_method(x0_iter, epsilon)
    res_newt, iter_newt = newton_method(x0_newton, epsilon)
    res_sec, iter_sec = secant_method(x0_sec, x1_sec, epsilon)

    # Вывод результатов
    print(f"{'Метод':<25} | {'Корень (x)':<12} | {'Итераций':<8}")
    print("-" * 55)
    print(f"{'Бисекции':<25} | {res_bis:<12.6f} | {iter_bis:<8}")
    print(f"{'Простой итерации':<25} | {res_iter:<12.6f} | {iter_iter:<8}")
    print(f"{'Ньютона':<25} | {res_newt:<12.6f} | {iter_newt:<8}")
    print(f"{'Секущих':<25} | {res_sec:<12.6f} | {iter_sec:<8}")

    # Проверка значения функции в найденных корнях
    print("\nПроверка f(x) в найденных точках (должно быть близко к 0):")
    print(f"f({res_bis:.6f}) = {f(res_bis):.2e}")
    print(f"f({res_iter:.6f}) = {f(res_iter):.2e}")
    print(f"f({res_newt:.6f}) = {f(res_newt):.2e}")
    print(f"f({res_sec:.6f}) = {f(res_sec):.2e}")
