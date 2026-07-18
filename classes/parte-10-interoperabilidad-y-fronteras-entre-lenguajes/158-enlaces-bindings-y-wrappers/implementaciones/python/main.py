import sys


def doble(x):
    return x * 2


def wrapper(x):  # adapta y formatea el resultado
    return f"wrap({doble(x)})"


n = int(sys.stdin.readline())
print(f"envuelto={wrapper(n)}")
