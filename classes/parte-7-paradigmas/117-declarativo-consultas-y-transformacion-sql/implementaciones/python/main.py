import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma_pares={sum(x for x in nums if x % 2 == 0)}")
