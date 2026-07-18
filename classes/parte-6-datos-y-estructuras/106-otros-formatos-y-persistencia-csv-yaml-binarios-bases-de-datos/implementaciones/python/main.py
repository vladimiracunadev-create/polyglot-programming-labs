import sys

nums = sys.stdin.read().split()
csv = ",".join(nums)
print(f"csv={csv} campos={len(nums)}")
