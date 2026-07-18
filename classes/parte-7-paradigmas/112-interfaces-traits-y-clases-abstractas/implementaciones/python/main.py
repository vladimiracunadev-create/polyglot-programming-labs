import sys


class Cuadrado:
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l * self.l


class Rectangulo:
    def __init__(self, a, b):
        self.a, self.b = a, b
    def area(self):
        return self.a * self.b


t = sys.stdin.readline().split()
f = Cuadrado(int(t[1])) if t[0] == "cuadrado" else Rectangulo(int(t[1]), int(t[2]))
print(f"area={f.area()}")
