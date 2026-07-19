# Clase 069 — Recursión y recursión de cola

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una función **recursiva**: que se llama a sí misma con un caso base y un caso recursivo. Fibonacci es el ejemplo clásico; también sirve para hablar de eficiencia y de recursión de cola.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una función recursiva con caso base.
2. Traducir una definición recursiva a código.
3. Reconocer el coste de la recursión ingenua.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Recursión | Una función que se llama a sí misma |
| 2 | Caso base | Dónde para la recursión |
| 3 | Caso recursivo | Reducir hacia el caso base |
| 4 | Coste | Fibonacci ingenuo es exponencial |

## 📖 Definiciones y características

- **Recursión** — técnica en que una función se invoca a sí misma. Clave: necesita un caso base.
- **Caso base** — el que se resuelve sin recursión. Clave: evita la recursión infinita.
- **Caso recursivo** — reduce el problema hacia el caso base. Clave: debe acercarse a él.
- **Recursión de cola** — la llamada recursiva es lo último que se hace. Clave: algunos lenguajes la optimizan.

## 🧩 Situación

Fibonacci se define recursivamente: F(n)=F(n-1)+F(n-2). Traducirlo a código es directo, pero la versión ingenua repite cálculos: un buen punto para hablar de eficiencia (Parte 3, clase 045 de complejidad).

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 30)
- **Salida** (stdout): `fib=<F(n)>`
- **Regla:** F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `fib=55` |
| `1` | `fib=1` |
| `0` | `fib=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION fib(n): SI n<2 DEVOLVER n ; SINO DEVOLVER fib(n-1)+fib(n-2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


n = int(sys.stdin.readline())
print(f"fib={fib(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function fib(n: number): number {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long fib(int n) {
        return n < 2 ? n : fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("fib=" + fib(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"fib={Fib(n)}");
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

func fib(n int) int64 {
	if n < 2 {
		return int64(n)
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("fib=%d\n", fib(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn fib(n: i64) -> i64 {
    if n < 2 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("fib={}", fib(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long fib(long n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("fib=%ld\n", fib(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: Fibonacci con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE fib(i, a, b) AS (
    VALUES (0, 0, 1)
    UNION ALL SELECT i + 1, b, a + b FROM fib WHERE i < 10
)
SELECT printf('fib=%d', a) AS resultado FROM fib WHERE i = 10;
```

### PHP · `php main.php`

```php
<?php
function fib($n) {
    return $n < 2 ? $n : fib($n - 1) + fib($n - 2);
}

$n = (int) trim(fgets(STDIN));
echo "fib=" . fib($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def fib` (Python), `func fib` (Go), `fn fib` (Rust) — todas se auto-invocan igual. |
| Semántica | La pila de llamadas crece con la profundidad; ojo con el desbordamiento en recursiones profundas. |
| Paradigmática | SQL expresa la recursión con un CTE recursivo, no con funciones. |

## 🧬 El concepto en la familia

En Ruby `def fib(n); n < 2 ? n : fib(n-1)+fib(n-2); end`. En Haskell la recursión es el modo natural de iterar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 069
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar el caso base** → causa: recursión infinita → desbordamiento de pila → solución: definir siempre el caso que corta la recursión
- **Recursión ingenua para n grande** → causa: coste exponencial → solución: usar memoización o una versión iterativa (aquí n<=30)

## ❓ Preguntas frecuentes

- **¿La recursión es peor que el bucle?** No en general; para Fibonacci ingenuo sí. Con memoización o cola, es eficiente.
- **¿Qué es la recursión de cola?** Cuando la llamada recursiva es la última operación; permite optimizarla como un bucle.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 068](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 070 ⏭️](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md)
