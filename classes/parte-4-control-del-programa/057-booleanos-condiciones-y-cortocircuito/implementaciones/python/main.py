import sys

n = int(sys.stdin.readline())
tf = lambda x: "true" if x else "false"
pos = n > 0
par = n % 2 == 0
print(f"positivo={tf(pos)} par={tf(par)} ambos={tf(pos and par)}")
