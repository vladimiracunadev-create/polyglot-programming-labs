import sys

# Declaración e inicialización a partir de la entrada.
a, b = sys.stdin.readline().split()
a, b = int(a), int(b)

# Asignación múltiple: intercambio sin variable temporal.
a, b = b, a

print(f"a={a} b={b}")
