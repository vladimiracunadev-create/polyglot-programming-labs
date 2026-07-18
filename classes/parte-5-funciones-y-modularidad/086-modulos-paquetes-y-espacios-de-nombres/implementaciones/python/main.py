import sys


class matematicas:  # actúa como un espacio de nombres
    @staticmethod
    def doble(n):
        return 2 * n


n = int(sys.stdin.readline())
print(f"resultado={matematicas.doble(n)}")
