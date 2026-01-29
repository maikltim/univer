import numpy as np


def ode_rhs(ti, y, t, f, a, c, fs):
    idx = min(int(ti * fs), len(t) - 1)
    return (c[idx] - a[idx] * y) / (f[idx] + 1e-6)