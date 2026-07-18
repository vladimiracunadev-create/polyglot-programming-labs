import sys

nums = [int(x) for x in sys.stdin.read().split()]
pares = [x for x in nums if x % 2 == 0]
print("pares=" + "-".join(str(x) for x in pares))
