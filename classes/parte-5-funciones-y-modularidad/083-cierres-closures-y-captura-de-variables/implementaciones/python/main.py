import sys


def hacer_sumador(base):
    def sumar(x):
        return base + x
    return sumar


base = int(sys.stdin.readline())
sumar = hacer_sumador(base)
print(f"r1={sumar(1)} r2={sumar(2)}")
