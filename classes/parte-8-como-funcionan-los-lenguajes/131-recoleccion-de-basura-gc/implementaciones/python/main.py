import sys

n = int(sys.stdin.readline())
for _ in range(n):
    _tmp = object()  # temporal; sin referencia persistente, se recolecta
print(f"creados={n} estado=recolectado")
