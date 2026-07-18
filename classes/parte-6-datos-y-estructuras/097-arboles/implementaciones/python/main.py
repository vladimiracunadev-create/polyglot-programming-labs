import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.sort()  # in-order de un BST equivale al orden ascendente
print("inorden=" + "-".join(str(x) for x in nums))
