import sys

t = sys.stdin.readline().split()
if t[0] == "cuadrado":
    area = int(t[1]) ** 2
else:  # rectangulo
    area = int(t[1]) * int(t[2])
print(f"area={area}")
