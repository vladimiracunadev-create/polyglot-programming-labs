import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.reverse()
print("invertido=" + "-".join(str(x) for x in nums))
