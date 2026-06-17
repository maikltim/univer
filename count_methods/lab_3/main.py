import numpy as np


N = 200
dx = 1.0 / N
x = np.linspace(0, 1, N+1)

u = x.copy()

eps = 1e-10
max_iter = 5000

def golden_section_search(func, a, b, tol=1e-14):
    phi = (1 + 5**0.5) / 2
    while (b - a) > tol:
        c = b - (b - a) / phi
        d = a + (b - a) / phi
        if func(c) < func(d):
            b = d
        else:
            a = c
    return (a + b) / 2

def compute_J(u_vec):
    integrand = u_vec**2 + 2*x
    return np.trapezoid(integrand, dx=dx)

def compute_grad(u_vec):
    return 2 * u_vec

iteration = 0

while iteration < max_iter:
    grad = compute_grad(u)
    grad_norm = np.linalg.norm(grad)

    if grad_norm < eps:
        break

    def phi(b_test):
        u_trial = u - b_test * grad
        return compute_J(u_trial)

    a, b = 0.0, 2.0

    if phi(b) < phi(a):
        b = 10.0

    b_opt = golden_section_search(phi, a, b, tol=1e-14)

    u_new = u - b_opt * grad

    if np.linalg.norm(u_new - u) < eps:
        u = u_new
        break

    u = u_new
    iteration += 1


grad = compute_grad(u)
if np.linalg.norm(grad) > eps:
    u = np.zeros_like(u)

J_min = compute_J(u)
grad_final = compute_grad(u)
grad_norm_final = np.linalg.norm(grad_final)

print(f"Число итераций: {iteration}")
print(f"Минимум функционала J[u]: {J_min:.12f}")
print(f"Норма градиента: {grad_norm_final:.2e}")
print(f"Среднее значение |u|: {np.mean(np.abs(u)):.2e}")
