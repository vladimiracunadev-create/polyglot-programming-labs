import sys


def divmod2(a, b):
    return a // b, a % b


a, b = map(int, sys.stdin.readline().split())
q, r = divmod2(a, b)
print(f"cociente={q} resto={r}")
