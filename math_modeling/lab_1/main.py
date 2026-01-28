import matplotlib.pyplot as plt
from signal_subsystem import SignalSubsystem

subsystem = SignalSubsystem()
t, signals = subsystem.generate()

plt.figure(figsize=(12, 7))
for i, sig in enumerate(signals):
    plt.plot(t, sig, label=f'Канал {i+1}')

plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.title("Выходные сигналы источника (N = 17)")
plt.legend()
plt.grid()
plt.show()