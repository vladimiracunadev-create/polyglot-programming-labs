import sys

nums = [int(x) for x in sys.stdin.read().split()]
stream = [x * 2 for x in nums if x % 2 == 0]
print("stream=" + "-".join(str(x) for x in stream))
