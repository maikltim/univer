import numpy as np 

def generate_sources(t):
    
    f = np.heaviside(t - 2, 1) + 1
    a = np.sin(2 * np.pi * t)
    c = np.random.normal(0, 1, len(t))
    
    return f, a, c