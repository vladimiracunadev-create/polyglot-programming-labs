import sys

a, b, op = sys.stdin.readline().split()
pila = [int(a), int(b)]
y = pila.pop()
x = pila.pop()
r = x + y if op == "+" else x - y if op == "-" else x * y
print(f"resultado={r}")
