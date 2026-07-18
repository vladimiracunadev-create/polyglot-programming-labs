import sys

s = sys.stdin.readline().strip()
longitud = len(s)  # Python comparte la referencia (GC), no hay 'move'.
print(f"movido={s} longitud={longitud}")
