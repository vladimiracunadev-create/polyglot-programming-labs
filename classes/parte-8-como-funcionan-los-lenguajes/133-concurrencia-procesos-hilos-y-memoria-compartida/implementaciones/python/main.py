import sys

nums = sys.stdin.read().split()
cuenta = 0
for _ in nums:
    cuenta += 1  # acumulador compartido
print(f"cuenta={cuenta}")
