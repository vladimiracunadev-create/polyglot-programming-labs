import sys


def cuadrado(n):
    return n * n  # pura: sin efectos secundarios


n = int(sys.stdin.readline())
print(f"puro={cuadrado(n)}")
