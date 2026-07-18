import sys

nums = [int(x) for x in sys.stdin.read().split()]
maximo = nums[0]
for x in nums:  # consumidor
    if x > maximo:
        maximo = x
print(f"max={maximo}")
