import sys

codigo = int(sys.stdin.readline())
nombres = {1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion"}
print(f"error={nombres.get(codigo, 'desconocido')}")
