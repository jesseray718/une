"""
Minimal state-vector quantum circuit simulator (pure Python).
"""
import cmath, math
from typing import List

class QuantumState:
    def __init__(self, n_qubits: int):
        self.n = n_qubits
        self.N = 1 << n_qubits
        self.amp = [0j] * self.N
        self.amp[0] = 1.0 + 0j

    def _apply_1q(self, gate, q: int):
        new = [0j] * self.N
        for i in range(self.N):
            bit = (i >> q) & 1
            i0 = i & ~(1 << q)
            i1 = i0 | (1 << q)
            if bit == 0:
                new[i0] += gate[0][0] * self.amp[i0] + gate[0][1] * self.amp[i1]
                new[i1] += gate[1][0] * self.amp[i0] + gate[1][1] * self.amp[i1]
        self.amp = new

    def h(self, q: int):
        s = 1 / math.sqrt(2)
        self._apply_1q([[s, s], [s, -s]], q)

    def x(self, q: int):
        self._apply_1q([[0, 1], [1, 0]], q)

    def z(self, q: int):
        self._apply_1q([[1, 0], [0, -1]], q)

    def cnot(self, c: int, t: int):
        new = [0j] * self.N
        for i in range(self.N):
            if (i >> c) & 1:
                j = i ^ (1 << t)
                new[j] = self.amp[i]
            else:
                new[i] = self.amp[i]
        self.amp = new

    def measure_all(self) -> str:
        idx = max(range(self.N), key=lambda i: abs(self.amp[i]))
        return format(idx, f"0{self.n}b")

    def probs(self) -> List[float]:
        return [abs(a)**2 for a in self.amp]

print("=== Quantum State-Vector Simulator loaded ===")
