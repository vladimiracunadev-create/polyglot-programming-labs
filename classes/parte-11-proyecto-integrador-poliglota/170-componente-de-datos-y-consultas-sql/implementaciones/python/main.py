import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"total={sum(nums)}")
