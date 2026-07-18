import sys

n = int(sys.stdin.readline())
pares = (2 * i for i in range(1, n + 1))
print("pares=" + "-".join(str(x) for x in pares))
