import sys

n = int(sys.stdin.readline())
match n:
    case _ if n > 0:
        signo = "positivo"
    case _ if n < 0:
        signo = "negativo"
    case _:
        signo = "cero"
print(f"signo={signo}")
