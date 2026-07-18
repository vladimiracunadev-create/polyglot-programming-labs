import sys

n = int(sys.stdin.readline())
opcion = n if n > 0 else None
if opcion is not None:
    print(f"resultado={opcion * 2}")
else:
    print("resultado=nada")
