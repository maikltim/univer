# pi_calculation.py

import numpy as np
import time
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states

from config import N_POINTS, THREADS_PER_BLOCK, RANDOM_SEED
from cuda_kernel import monte_carlo_kernel


def calculate_pi_gpu():
    blocks = (N_POINTS + THREADS_PER_BLOCK - 1) // THREADS_PER_BLOCK

    results = np.zeros(N_POINTS, dtype=np.int32)
    rng_states = create_xoroshiro128p_states(N_POINTS, seed=RANDOM_SEED)

    start = time.time()
    monte_carlo_kernel[blocks, THREADS_PER_BLOCK](rng_states, results, N_POINTS)
    cuda.synchronize()
    end = time.time()

    pi = 4.0 * results.sum() / N_POINTS
    return pi, end - start
