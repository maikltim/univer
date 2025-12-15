# main.py

from utils import check_cuda
from pi_calculation import calculate_pi_gpu


def main():
    check_cuda()

    pi, exec_time = calculate_pi_gpu()

    print("Результаты вычисления π (CUDA Монте-Карло)")
    print(f"π ≈ {pi}")
    print(f"Время выполнения: {exec_time:.4f} сек")


if __name__ == "__main__":
    main()
