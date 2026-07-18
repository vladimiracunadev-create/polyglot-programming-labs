import sys
from dataclasses import dataclass


@dataclass
class Persona:
    nombre: str
    edad: int


t = sys.stdin.readline().split()
p = Persona(t[0], int(t[1]))
print(f"Persona(nombre={p.nombre}, edad={p.edad})")
