import sys

recolectados = []


def al_evento(i):
    recolectados.append(i)


n = int(sys.stdin.readline())
for i in range(1, n + 1):
    al_evento(i)
print("eventos=" + "-".join(str(x) for x in recolectados))
