import sys

a, b = map(int, sys.stdin.readline().split())
ba, bb = a != 0, b != 0
tf = lambda x: "true" if x else "false"
print(f"and={tf(ba and bb)} or={tf(ba or bb)} not_a={tf(not ba)}")
