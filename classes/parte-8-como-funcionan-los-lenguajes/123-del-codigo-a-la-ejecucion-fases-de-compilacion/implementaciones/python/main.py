import sys

a, op, b = sys.stdin.readline().split()
a, b = int(a), int(b)
if op == "+":
    r = a + b
elif op == "-":
    r = a - b
else:
    r = a * b
print(f"resultado={r}")
