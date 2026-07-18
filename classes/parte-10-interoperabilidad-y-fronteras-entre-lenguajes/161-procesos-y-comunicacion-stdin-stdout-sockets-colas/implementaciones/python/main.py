import sys

nums = [int(x) for x in sys.stdin.read().split()]
recibido = 0
for m in nums:  # consumidor de la cola
    recibido += m
print(f"recibido={recibido}")
