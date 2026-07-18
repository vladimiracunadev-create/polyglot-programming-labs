import sys

a, b = map(int, sys.stdin.readline().split())
print(f"abi={'compatible' if a == b else 'incompatible'}")
