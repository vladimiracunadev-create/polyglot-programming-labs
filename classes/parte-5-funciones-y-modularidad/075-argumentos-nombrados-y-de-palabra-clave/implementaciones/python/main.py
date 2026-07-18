import sys


def punto(x, y):
    return f"punto(x={x}, y={y})"


a, b = map(int, sys.stdin.readline().split())
print(punto(x=a, y=b))
