import sys


def mayor(a, b):
    return a if a > b else b


a, b = map(int, sys.stdin.readline().split())
print(f"max={mayor(a, b)}")
