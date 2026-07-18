import sys

n = int(sys.stdin.readline())
real = float(n)
par = "true" if n % 2 == 0 else "false"
print(f"entero={n} real={real:.1f} par={par}")
