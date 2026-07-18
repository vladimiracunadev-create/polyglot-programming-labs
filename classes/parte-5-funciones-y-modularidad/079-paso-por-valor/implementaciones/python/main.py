import sys


def doblar(x):
    x = x * 2  # modifica la copia local
    return x


n = int(sys.stdin.readline())
local = doblar(n)
print(f"original={n} local={local}")
