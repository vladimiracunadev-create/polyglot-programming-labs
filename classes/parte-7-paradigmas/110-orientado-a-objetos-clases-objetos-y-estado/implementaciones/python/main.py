import sys


class Contador:
    def __init__(self):
        self.cuenta = 0

    def incrementar(self):
        self.cuenta += 1


n = int(sys.stdin.readline())
c = Contador()
for _ in range(n):
    c.incrementar()
print(f"cuenta={c.cuenta}")
