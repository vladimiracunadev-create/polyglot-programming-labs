import sys
import asyncio


async def doble(x):
    return x * 2


async def main():
    n = int(sys.stdin.readline())
    resultado = await doble(n)
    print(f"resultado={resultado}")


asyncio.run(main())
