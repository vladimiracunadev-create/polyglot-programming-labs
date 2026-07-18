import sys

t = sys.stdin.read().split()
indice = int(t[0])
lista = [int(x) for x in t[1:]]
print(f"valor={lista[indice]}")
