import sys

n = int(sys.stdin.readline())
x = n
# Python no crea alcance de bloque: se usa otra variable para el 'interno'.
x_interno = x + 10
print(f"interno={x_interno} externo={x}")
