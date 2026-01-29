import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from sources import generate_sources
from ode_model import ode_rhs

T = 10
fs = 1000 
t = np.linspace(0, T, int(T * fs))

f, a, c = generate_sources(t)

solution = solve_ivp(
    lambda ti, y: ode_rhs(ti, y, t, f, a, c, fs),
    [t[0], t[-1]],
    y0=[0],
    t_eval=t 
)

plt.figure(figsize=(10, 5))
plt.plot(t, solution.y[0])
plt.title("Решение дифференциального уравнения (N = 17)")
plt.xlabel("t, c")
plt.ylabel("y(t)")
plt.grid()
plt.show()