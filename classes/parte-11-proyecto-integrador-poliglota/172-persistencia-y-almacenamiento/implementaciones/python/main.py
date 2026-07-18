import sys

clave, valor = sys.stdin.readline().split()
almacen = {}
almacen[clave] = valor
print(f"guardado={clave}={almacen[clave]}")
