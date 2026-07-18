import sys

a, b = map(int, sys.stdin.readline().split())
try:
    r = a // b
    print(f"resultado={r}")
except ZeroDivisionError:
    print("error=division por cero")
