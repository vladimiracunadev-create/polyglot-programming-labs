import sys

nums = [int(x) for x in sys.stdin.read().split()]
aristas = len(nums) // 2
nodos = len(set(nums))
print(f"aristas={aristas} nodos={nodos}")
