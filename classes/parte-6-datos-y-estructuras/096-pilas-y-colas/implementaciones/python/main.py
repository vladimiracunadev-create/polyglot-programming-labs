import sys

nums = [int(x) for x in sys.stdin.read().split()]
pila = "-".join(str(x) for x in reversed(nums))
cola = "-".join(str(x) for x in nums)
print(f"pila={pila} cola={cola}")
