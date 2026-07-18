import sys


def potencia(base, exp=2):
    r = 1
    for _ in range(exp):
        r *= base
    return r


t = sys.stdin.readline().split()
base = int(t[0])
if len(t) > 1:
    print(f"resultado={potencia(base, int(t[1]))}")
else:
    print(f"resultado={potencia(base)}")
