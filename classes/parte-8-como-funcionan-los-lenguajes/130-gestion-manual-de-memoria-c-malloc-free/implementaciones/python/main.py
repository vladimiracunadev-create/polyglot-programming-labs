import sys

n = int(sys.stdin.readline())
arr = [0] * n  # el runtime gestiona la memoria
for i in range(n):
    arr[i] = i + 1
print(f"reservado={n} suma={sum(arr)}")
