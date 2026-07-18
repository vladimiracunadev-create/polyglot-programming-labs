import sys

nums = [int(x) for x in sys.stdin.read().split()]
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
print(f"cuenta={freq[nums[0]]}")
