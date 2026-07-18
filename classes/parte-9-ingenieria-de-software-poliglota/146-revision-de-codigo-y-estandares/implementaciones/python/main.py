import sys

w = sys.stdin.readline().strip()
valido = all("a" <= c <= "z" for c in w)
print(f"valido={'true' if valido else 'false'}")
