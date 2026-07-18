import sys

nums = [int(x) for x in sys.stdin.read().split()]
suma = 0
for x in nums:
    suma += x
print(f"suma={suma}")
