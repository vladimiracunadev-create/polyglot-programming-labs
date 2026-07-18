import sys


class Cuenta:
    def __init__(self):
        self._saldo = 0  # privado por convención

    def depositar(self, monto):
        self._saldo += monto

    def saldo(self):
        return self._saldo


n = int(sys.stdin.readline())
c = Cuenta()
c.depositar(n)
c.depositar(n)
print(f"saldo={c.saldo()}")
