import sys

# Literales y constantes: los valores se leen y se nombran.
precio_str, cantidad_str, descuento_str = sys.stdin.readline().split()

PRECIO_UNITARIO = float(precio_str)   # tipo dinámico, inferido en tiempo de ejecución
CANTIDAD = int(cantidad_str)
DESCUENTO = float(descuento_str)

subtotal = PRECIO_UNITARIO * CANTIDAD
total = subtotal * (1 - DESCUENTO)

print(f"Total: {total:.2f}")
