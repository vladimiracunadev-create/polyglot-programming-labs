import sys

linea = sys.stdin.readline().rstrip("\n")
palabras = len(linea.split())
print(f"palabras={palabras} caracteres={len(linea)}")
