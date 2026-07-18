import sys

n = int(sys.stdin.readline())
acc = 0
pasos = []
for i in range(1, n + 1):
    acc += i
    pasos.append(acc)
print("traza=" + "-".join(str(x) for x in pasos))
