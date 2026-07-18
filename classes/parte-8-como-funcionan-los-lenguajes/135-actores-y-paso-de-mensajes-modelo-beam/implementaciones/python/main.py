import sys


class Acumulador:  # actor con estado propio
    def __init__(self):
        self.total = 0

    def recibir(self, mensaje):
        self.total += mensaje


nums = [int(x) for x in sys.stdin.read().split()]
actor = Acumulador()
for m in nums:
    actor.recibir(m)
print(f"total={actor.total}")
