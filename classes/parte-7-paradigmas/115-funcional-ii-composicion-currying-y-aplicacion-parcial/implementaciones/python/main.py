import sys


def doblar(x):
    return x * 2


def incrementar(x):
    return x + 1


n = int(sys.stdin.readline())
print(f"resultado={incrementar(doblar(n))}")
