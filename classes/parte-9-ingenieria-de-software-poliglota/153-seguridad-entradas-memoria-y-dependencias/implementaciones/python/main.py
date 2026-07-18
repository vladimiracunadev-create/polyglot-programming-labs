import sys

w = sys.stdin.readline().strip()
seguro = w.isalnum()
print(f"seguro={'true' if seguro else 'false'}")
