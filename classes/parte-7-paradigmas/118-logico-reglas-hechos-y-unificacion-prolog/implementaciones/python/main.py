import sys

a, b = map(int, sys.stdin.readline().split())
es_divisor = b % a == 0
print(f"divisor={'true' if es_divisor else 'false'}")
