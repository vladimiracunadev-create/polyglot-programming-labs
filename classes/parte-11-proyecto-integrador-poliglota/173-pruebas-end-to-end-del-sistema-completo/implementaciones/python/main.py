import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"e2e={'pasa' if a + b == esperado else 'falla'}")
