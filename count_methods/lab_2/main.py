import numpy as np
import matplotlib.pyplot as plt


def f(xy):
    """Целевая функция (Розенброка)"""
    x, y = xy
    return (1 - x)**2 + 100 * (y - x**2)**2

def grad_f(xy):
    """Градиент функции"""
    x, y = xy
    df_dx = -2 * (1 - x) - 400 * x * (y - x**2)
    df_dy = 200 * (y - x**2)
    return np.array([df_dx, df_dy])

def hessian_f(xy):
    """Матрица Гессе (вторые производные)"""
    x, y = xy
    h11 = 2 - 400 * y + 1200 * x**2
    h12 = -400 * x
    h22 = 200
    
    return np.array([[h11, h12], [h12, h22]])

# 2. Метод наискорейшего спуска с поиском шага (Бисекция) 

def find_step_size_bisection(x_curr, direction, eps_step=1e-10):
    """
    Находит оптимальный шаг b_k минимизируя phi(b) = f(x + b * direction)
    методом дихотомии.
    """
    a, b = 0.0, 1.0
    while f(x_curr + b * direction) < f(x_curr + a * direction):
        b *= 2
        if b > 1e6: 
            return 0.1
    
    iterations = 0
    max_iter = 100
    while (b - a) > eps_step and iterations < max_iter:
        mid = (a + b) / 2
        c = (a + mid) / 2
        d = (mid + b) / 2
        
        fc = f(x_curr + c * direction)
        fd = f(x_curr + d * direction)
        
        if fc < fd:
            b = d
        else:
            a = c
        iterations += 1
        
    return (a + b) / 2

def gradient_descent_method(start_point, eps=1e-13, max_iter=1000):
    trajectory = [start_point.copy()]
    x = start_point.copy()
    
    for i in range(max_iter):
        g = grad_f(x)
        
        if np.linalg.norm(g) < eps:
            break
            
        direction = -g  
        
        step = find_step_size_bisection(x, direction)
        x_new = x + step * direction
        
        trajectory.append(x_new.copy())
        x = x_new
        
        if abs(f(x) - f(trajectory[-2])) < eps:
            break

    return np.array(trajectory)

# 3. Метод Ньютона

def newton_method(start_point, eps=1e-13, max_iter=100):
    trajectory = [start_point.copy()]
    x = start_point.copy()
    
    for i in range(max_iter):
        g = grad_f(x)
        H = hessian_f(x)
        
        try:
            p = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            print("Матрица Гессе вырождена, прерываем метод Ньютона.")
            break
        
        step_len = 1.0 
        
        x_new = x + step_len * p
        trajectory.append(x_new.copy())
        
        if np.linalg.norm(p) < eps or np.linalg.norm(g) < eps:
            break
            
        x = x_new

    return np.array(trajectory)

#  4. Визуализация 

def plot_results(grad_traj, newton_traj):
    x_vals = np.linspace(-1.5, 2.5, 400)
    y_vals = np.linspace(-0.5, 3.5, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = (1 - X)**2 + 100 * (Y - X**2)**2
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    contour = plt.contour(X, Y, Z, levels=np.logspace(-1, 3, 20), cmap='viridis', alpha=0.7)
    plt.clabel(contour, inline=True, fontsize=8)
    
    plt.plot(grad_traj[:4, 0], grad_traj[:4, 1], 'ro-', linewidth=2, markersize=8, label='Градиентный спуск (первые 3 шага)')
    plt.scatter([1], [1], color='green', s=100, marker='*', label='Минимум (1, 1)')
    plt.title('Метод наискорейшего спуска')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.subplot(1, 2, 2)
    contour = plt.contour(X, Y, Z, levels=np.logspace(-1, 3, 20), cmap='plasma', alpha=0.7)
    plt.clabel(contour, inline=True, fontsize=8)
    
    plt.plot(newton_traj[:4, 0], newton_traj[:4, 1], 'bo-', linewidth=2, markersize=8, label='Метод Ньютона (первые 3 шага)')
    plt.scatter([1], [1], color='green', s=100, marker='*', label='Минимум (1, 1)')
    plt.title('Метод Ньютона')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 5. Запуск и вывод результатов

if __name__ == "__main__":
    epsilon = 1e-13
    start_point = np.array([-1.2, 1.0]) 
    
    print(f"Начало оптимизации из точки: {start_point}")
    print(f"Точность: {epsilon}\n")
    
    grad_trajectory = gradient_descent_method(start_point, epsilon)
    newton_trajectory = newton_method(start_point, epsilon)
    
    print("--- Результаты метода наискорейшего спуска ---")
    print(f"Найдено решение: {grad_trajectory[-1]}")
    print(f"Значение функции: {f(grad_trajectory[-1])}")
    print(f"Количество итераций: {len(grad_trajectory)-1}")
    print(f"Норма градиента в конце: {np.linalg.norm(grad_f(grad_trajectory[-1]))}\n")
    
    print("--- Результаты метода Ньютона ---")
    print(f"Найдено решение: {newton_trajectory[-1]}")
    print(f"Значение функции: {f(newton_trajectory[-1])}")
    print(f"Количество итераций: {len(newton_trajectory)-1}")
    print(f"Норма градиента в конце: {np.linalg.norm(grad_f(newton_trajectory[-1]))}\n")

    plot_results(grad_trajectory, newton_trajectory)
