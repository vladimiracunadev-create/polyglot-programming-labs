import sys

a, b = map(int, sys.stdin.readline().split())
script = "a + b"  # el script embebido
resultado = eval(script, {}, {"a": a, "b": b})
print(f"resultado={resultado}")
