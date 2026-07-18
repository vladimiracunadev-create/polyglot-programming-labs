import sys


def doble(x):  # simula una función externa (FFI hacia C)
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
