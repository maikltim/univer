# utils.py

from numba import cuda


def check_cuda():
    if not cuda.is_available():
        raise RuntimeError("CUDA недоступна. Проверьте драйвер и видеокарту.")
