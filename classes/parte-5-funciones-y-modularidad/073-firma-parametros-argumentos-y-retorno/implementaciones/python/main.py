import sys


def suma(a, b):
    return a + b


a, b = map(int, sys.stdin.readline().split())
print(f"suma={suma(a, b)}")
