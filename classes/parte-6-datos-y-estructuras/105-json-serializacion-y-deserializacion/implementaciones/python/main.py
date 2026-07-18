import sys

t = sys.stdin.readline().split()
nombre, edad = t[0], int(t[1])
print(f'{{"nombre": "{nombre}", "edad": {edad}}}')
