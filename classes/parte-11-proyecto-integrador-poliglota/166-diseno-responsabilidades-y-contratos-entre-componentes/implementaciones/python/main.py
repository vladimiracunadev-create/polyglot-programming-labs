import sys

a, b = sys.stdin.readline().split()
print(f"contrato={'compatible' if a == b else 'incompatible'}")
