import sys


def suma(a, b):
    return a + b


def producto(a, b):
    return a * b


def aplicar(f, a, b):
    return f(a, b)


a, b = map(int, sys.stdin.readline().split())
print(f"suma={aplicar(suma, a, b)} producto={aplicar(producto, a, b)}")
