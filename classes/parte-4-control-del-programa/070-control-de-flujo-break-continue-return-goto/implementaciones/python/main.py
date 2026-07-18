import sys

n = int(sys.stdin.readline())
d = 2
while d <= n:
    if n % d == 0:
        break
    d += 1
print(f"primer_divisor={d}")
