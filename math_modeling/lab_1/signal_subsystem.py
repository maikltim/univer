import numpy as np

class SignalSubsystem:
    def __init__(self, N=17, T=10, fs=1000):
        self.N = N
        self.T = T
        self.fs = fs
        self.t = np.linspace(0, T, int(T * fs))

        self.Kkan = 5
        self.Kdiap = 2

        self.kKD = [
            [1, 2],
            [5, 6],
            [9, 10],
            [13, 14],
            [17, 18]
        ]

    def signal_by_Z(self, Z, t):
        if Z == 1:
            return np.random.normal(0, 1, len(t))
        elif Z == 3:
            return np.random.uniform(-1, 1, len(t))
        elif Z == 4:
            return np.heaviside(t, 1)
        elif Z == 6:
            return np.sign(np.sin(10 * t))
        elif Z == 7:
            return t
        elif Z == 9:
            return np.sin(2 * np.pi * t * t)
        elif Z == 10:
            return np.random.randn(len(t))
        elif Z == 11:
            return np.sin(2 * np.pi * 2 * t)
        else:
            return np.zeros(len(t))

    def generate(self):
        signals = []
        dt = self.T / self.Kdiap

        for k in range(self.Kkan):      
            channel = np.zeros_like(self.t)

            for d in range(self.Kdiap):
                t1 = d * dt
                t2 = (d + 1) * dt
                idx = (self.t >= t1) & (self.t < t2)

                Z = ((k + 1) + (d + 1) + self.N + self.kKD[k][d]) % 12
                channel[idx] = self.signal_by_Z(Z, self.t[idx])

            signals.append(channel)

        return self.t, signals
