import sys

a, b, c = map(int, sys.stdin.readline().split())
arr = [a, b, c]
print(f"suma={sum(arr)} max={max(arr)}")
