import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = list(map(lambda x: x * 2, nums))
print("doblados=" + "-".join(str(x) for x in doblados))
