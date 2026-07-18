import sys

a, b = map(int, sys.stdin.readline().split())
mx = a if a > b else b
print(f"max={mx}")
