import sys


def doblar(caja):
    caja[0] *= 2  # modifica el contenido compartido


n = int(sys.stdin.readline())
antes = n
caja = [n]
doblar(caja)
print(f"antes={antes} despues={caja[0]}")
