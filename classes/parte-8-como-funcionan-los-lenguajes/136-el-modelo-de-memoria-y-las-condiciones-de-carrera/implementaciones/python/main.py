import sys

n = int(sys.stdin.readline())
cuenta = 0
for _ in range(n):  # sección crítica protegida (aquí, secuencial)
    cuenta += 1
print(f"cuenta={cuenta}")
