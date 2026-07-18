import sys

score = int(sys.stdin.readline())
if score >= 90:
    nota = "A"
elif score >= 80:
    nota = "B"
elif score >= 70:
    nota = "C"
else:
    nota = "F"
print(f"nota={nota}")
