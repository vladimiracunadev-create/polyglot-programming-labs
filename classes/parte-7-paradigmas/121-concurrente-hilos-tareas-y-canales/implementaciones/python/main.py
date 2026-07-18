import sys

nums = [int(x) for x in sys.stdin.read().split()]
# Visión concurrente: dividir en dos mitades y combinar.
medio = len(nums) // 2
parcial1 = sum(nums[:medio])
parcial2 = sum(nums[medio:])
print(f"suma={parcial1 + parcial2}")
