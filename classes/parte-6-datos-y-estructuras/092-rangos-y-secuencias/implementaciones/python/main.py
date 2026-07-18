import sys

a, b = map(int, sys.stdin.readline().split())
r = list(range(a, b + 1))
print(f"rango={'-'.join(str(x) for x in r)} suma={sum(r)}")
