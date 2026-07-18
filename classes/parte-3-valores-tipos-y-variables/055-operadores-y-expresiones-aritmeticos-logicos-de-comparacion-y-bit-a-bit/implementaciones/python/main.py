import sys

a, b = map(int, sys.stdin.readline().split())
print(f"suma={a + b} resta={a - b} mult={a * b} div={a // b} mod={a % b}")
