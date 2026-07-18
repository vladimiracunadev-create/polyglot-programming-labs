import sys

n = int(sys.stdin.readline())
f = 1
for i in range(1, n + 1):
    f *= i
print(f"factorial={f}")
