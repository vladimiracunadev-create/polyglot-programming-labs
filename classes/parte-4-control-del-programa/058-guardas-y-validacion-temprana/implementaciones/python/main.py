import sys

edad = int(sys.stdin.readline())
if edad < 0:
    print("invalido")
elif edad < 18:
    print("menor")
else:
    print("adulto")
