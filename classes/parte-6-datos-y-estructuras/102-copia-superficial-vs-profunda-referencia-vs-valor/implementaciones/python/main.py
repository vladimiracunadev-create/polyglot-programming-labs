import sys

nums = [int(x) for x in sys.stdin.read().split()]
copia = list(nums)  # copia superficial (aquí basta, son enteros)
copia[-1] = 99
print(f"original={'-'.join(map(str, nums))} copia={'-'.join(map(str, copia))}")
