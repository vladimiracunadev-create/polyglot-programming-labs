import sys


class Perro:
    def sonido(self):
        return "guau"


class Gato:
    def sonido(self):
        return "miau"


class Vaca:
    def sonido(self):
        return "muu"


tipo = sys.stdin.readline().strip()
animales = {"perro": Perro(), "gato": Gato(), "vaca": Vaca()}
print(f"sonido={animales[tipo].sonido()}")
