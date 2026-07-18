import sys

a, b, esperado = map(int, sys.stdin.readline().split())
print(f"test={'pasa' if a + b == esperado else 'falla'}")
