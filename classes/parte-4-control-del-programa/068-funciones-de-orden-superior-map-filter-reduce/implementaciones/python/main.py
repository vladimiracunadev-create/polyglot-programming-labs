import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = [x * 2 for x in nums]
total = sum(doblados)
print(f"doblados={'-'.join(str(x) for x in doblados)} total={total}")
