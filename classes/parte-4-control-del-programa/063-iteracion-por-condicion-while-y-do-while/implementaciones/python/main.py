import sys

n = int(sys.stdin.readline())
suma = 0
i = 1
while i <= n:
    suma += i
    i += 1
print(f"suma={suma}")
