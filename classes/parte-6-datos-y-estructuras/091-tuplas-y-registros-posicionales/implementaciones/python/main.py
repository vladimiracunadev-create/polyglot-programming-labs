import sys

a, b = map(int, sys.stdin.readline().split())
t = (a, b)
t = (t[1], t[0])
print(f"tupla=({t[0]}, {t[1]})")
