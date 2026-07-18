import sys


class Recurso:
    def __init__(self, valor):
        self.valor = valor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # aquí se liberaría


n = int(sys.stdin.readline())
with Recurso(n) as r:
    valor = r.valor
print(f"valor={valor} estado=liberado")
