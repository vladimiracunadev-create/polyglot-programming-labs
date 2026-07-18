import sys

tipo = sys.stdin.readline().strip()
rec = {"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
print(f"lenguaje={rec.get(tipo, 'Python')}")
