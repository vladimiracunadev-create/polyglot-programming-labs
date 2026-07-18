import sys

n = int(sys.stdin.readline())
lista = []
for i in range(n, 0, -1):
    lista.append(i)
print("lista=" + "-".join(str(x) for x in lista))
