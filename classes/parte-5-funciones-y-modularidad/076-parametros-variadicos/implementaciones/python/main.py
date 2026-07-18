import sys


def suma(*nums):
    total = 0
    for n in nums:
        total += n
    return total


nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma={suma(*nums)}")
