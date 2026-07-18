import sys

pasos = [int(x) for x in sys.stdin.read().split()]
print(f"ci={'verde' if all(p == 1 for p in pasos) else 'rojo'}")
