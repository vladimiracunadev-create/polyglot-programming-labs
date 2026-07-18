import sys

n = int(sys.stdin.readline())
ops = 0
suma = 0
for i in range(1, n + 1):
    suma += i
    ops += 1
print(f"operaciones={ops} resultado={suma}")
