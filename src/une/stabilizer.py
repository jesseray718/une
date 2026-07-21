"""
Minimal stabilizer simulator (Clifford circuits).
"""
from typing import List

class StabilizerState:
    def __init__(self, n: int):
        self.n = n
        self.x = [[0]*n for _ in range(n)]
        self.z = [[0]*n for _ in range(n)]
        self.phase = [0]*n
        for i in range(n):
            self.z[i][i] = 1

    def h(self, q: int):
        for i in range(self.n):
            self.x[i][q], self.z[i][q] = self.z[i][q], self.x[i][q]

    def s(self, q: int):
        for i in range(self.n):
            if self.x[i][q]:
                self.z[i][q] ^= 1

    def cnot(self, c: int, t: int):
        for i in range(self.n):
            self.x[i][t] ^= self.x[i][c]
            self.z[i][c] ^= self.z[i][t]

    def measure_z(self, q: int) -> int:
        for i in range(self.n):
            if self.x[i][q]:
                return 0
        return 0

    def dump(self):
        for i in range(self.n):
            pauli = ""
            for q in range(self.n):
                if self.x[i][q] and self.z[i][q]: pauli += "Y"
                elif self.x[i][q]: pauli += "X"
                elif self.z[i][q]: pauli += "Z"
                else: pauli += "I"
            print(f"g{i}: {pauli}")

print("=== Stabilizer Simulator loaded ===")
