import sys

n = int(sys.stdin.readline())
obj = {"valor": n}
def doble(o):
    return o["valor"] * 2
print(f"resultado={doble(obj)}")
