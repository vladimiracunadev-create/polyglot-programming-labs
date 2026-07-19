# Clase 127 — La pila (stack) y el marco de llamada

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **pila (stack) y el marco de llamada**: cada llamada a función crea un marco con sus variables; la recursión los apila. La profundidad de la recursión es cuántos marcos hay a la vez.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer la pila de llamadas.
2. Relacionar recursión con marcos apilados.
3. Explicar el desbordamiento de pila.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila de llamadas | Marcos de las funciones activas |
| 2 | Marco de llamada | Variables y retorno de una llamada |
| 3 | Profundidad | Cuántos marcos hay a la vez |

## 📖 Definiciones y características

- **Pila (stack)** — región de memoria para los marcos de llamada. Clave: LIFO, rápida.
- **Marco de llamada** — espacio de una llamada: parámetros, locales, dirección de retorno. Clave: se apila al llamar.
- **Desbordamiento de pila** — cuando hay demasiados marcos. Clave: recursión muy profunda lo causa.

## 🧩 Situación

Cada llamada recursiva apila un marco; sumar 1..n con recursión usa n marcos a la vez. Si n es enorme, la pila se desborda. La pila explica cómo el programa recuerda dónde volver.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (1 <= n <= 1000)
- **Salida** (stdout): `suma=<1+...+n> profundidad=<n>`
- **Regla:** suma recursiva; profundidad = número de marcos = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15 profundidad=5` |
| `3` | `suma=6 profundidad=3` |
| `1` | `suma=1 profundidad=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
sumar(n) = n + sumar(n-1) ; sumar(0) = 0 ; profundidad = n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

sys.setrecursionlimit(5000)


def sumar(n):
    return 0 if n == 0 else n + sumar(n - 1)


n = int(sys.stdin.readline())
print(f"suma={sumar(n)} profundidad={n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function sumar(n) {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function sumar(n: number): number {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long sumar(int n) {
        return n == 0 ? 0 : n + sumar(n - 1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("suma=" + sumar(n) + " profundidad=" + n);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Sumar(int n) => n == 0 ? 0 : n + Sumar(n - 1);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={Sumar(n)} profundidad={n}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func sumar(n int) int64 {
	if n == 0 {
		return 0
	}
	return int64(n) + sumar(n-1)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("suma=%d profundidad=%d\n", sumar(n), n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn sumar(n: i64) -> i64 {
    if n == 0 {
        0
    } else {
        n + sumar(n - 1)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} profundidad={}", sumar(n), n);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long sumar(long n) {
    return n == 0 ? 0 : n + sumar(n - 1);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld profundidad=%ld\n", sumar(n), n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: recursión con CTE (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d profundidad=%d', sum(i), max(i)) AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
function sumar($n) {
    return $n === 0 ? 0 : $n + sumar($n - 1);
}

$n = (int) trim(fgets(STDIN));
echo "suma=" . sumar($n) . " profundidad=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Función recursiva en cada lenguaje. |
| Semántica | Cada llamada apila un marco; el retorno lo desapila. |
| Paradigmática | SQL usa recursión con CTE, sin pila visible. |

## 🧬 El concepto en la familia

En Haskell la recursión es el modo natural de iterar; la recursión de cola puede optimizarse a un bucle.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 127
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Recursión sin caso base** → causa: desbordamiento de pila → solución: definir el caso base
- **Recursión demasiado profunda** → causa: límite de pila → solución: usar iteración o recursión de cola para n enorme

## ❓ Preguntas frecuentes

- **¿Por qué existe la pila?** Para recordar dónde volver y los datos locales de cada llamada.
- **¿Stack o heap?** La pila guarda marcos (rápida, automática); el heap, datos de vida flexible.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 126](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 128 ⏭️](../../parte-8-como-funcionan-los-lenguajes/128-el-heap-y-la-asignacion-dinamica/README.md)
