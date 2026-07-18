import sys

estrategia, a, b = sys.stdin.readline().split()
a, b = int(a), int(b)
ops = {"suma": a + b, "resta": a - b, "producto": a * b}
print(f"resultado={ops[estrategia]}")
