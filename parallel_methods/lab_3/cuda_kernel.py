# cuda_kernel.py

from numba import cuda
from numba.cuda.random import xoroshiro128p_uniform_float32


@cuda.jit
def monte_carlo_kernel(rng_states, results, n):
    idx = cuda.grid(1)
    if idx < n:
        x = xoroshiro128p_uniform_float32(rng_states, idx)
        y = xoroshiro128p_uniform_float32(rng_states, idx)

        if x * x + y * y <= 1.0:
            results[idx] = 1
        else:
            results[idx] = 0
