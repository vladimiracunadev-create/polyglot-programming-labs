import sys

sys.setrecursionlimit(5000)


def sumar(n):
    return 0 if n == 0 else n + sumar(n - 1)


n = int(sys.stdin.readline())
print(f"suma={sumar(n)} profundidad={n}")
