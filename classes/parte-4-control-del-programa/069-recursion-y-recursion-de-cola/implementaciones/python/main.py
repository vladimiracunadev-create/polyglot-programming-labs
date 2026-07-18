import sys


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


n = int(sys.stdin.readline())
print(f"fib={fib(n)}")
