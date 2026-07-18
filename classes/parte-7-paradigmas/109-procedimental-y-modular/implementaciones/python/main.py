import sys


def promedio(lista):
    return sum(lista) // len(lista)


nums = [int(x) for x in sys.stdin.read().split()]
print(f"promedio={promedio(nums)}")
