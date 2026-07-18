import sys

n = int(sys.stdin.readline())
viejo = n * 2
nuevo = n + n
eq = "true" if viejo == nuevo else "false"
print(f"equivalente={eq} resultado={nuevo}")
