import sys


def dividir(a, b):
    if b == 0:
        return (None, "division")
    return (a // b, None)


a, b = map(int, sys.stdin.readline().split())
valor, err = dividir(a, b)
if err is not None:
    print(f"err={err}")
else:
    print(f"ok={valor}")
