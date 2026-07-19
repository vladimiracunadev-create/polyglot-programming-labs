# Clase 076 — Parámetros variádicos

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Definir una función **variádica**: acepta un número variable de argumentos. Es lo que hay detrás de `print(...)` o `sum(...)`. Cada lenguaje lo expresa con `*args`, `...`, `params` o slices.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función que acepta N argumentos.
2. Recorrer los argumentos variádicos.
3. Reconocer la sintaxis de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Función variádica | Número variable de argumentos |
| 2 | Recolectar en una colección | Los argumentos llegan como lista/slice |
| 3 | Sintaxis por lenguaje | *args, ..., params[] |
| 4 | Usos comunes | print, sum, format |

## 📖 Definiciones y características

- **Función variádica** — acepta un número variable de argumentos. Clave: `sum(1,2,3,...)`.
- ***args / ...** — sintaxis para recolectar argumentos variables. Clave: llegan como colección.
- **Empaquetar** — reunir los argumentos sueltos en una lista. Clave: dentro de la función.
- **Desempaquetar** — expandir una lista en argumentos sueltos. Clave: la operación inversa.

## 🧩 Situación

`printf`, `sum`, `max` aceptan cuantos argumentos quieras. Una función variádica los recibe como una colección y los procesa; es la base de muchas utilidades.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma(...nums) = Σ nums

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20 30 40` | `suma=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(...nums): DEVOLVER Σ nums
LEER lista ; ESCRIBIR "suma=" suma(lista)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def suma(*nums):
    total = 0
    for n in nums:
        total += n
    return total


nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma={suma(*nums)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function suma(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function suma(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long suma(int... nums) {
        long total = 0;
        for (int n : nums) total += n;
        return total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        System.out.println("suma=" + suma(nums));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

long Suma(params int[] nums) => nums.Sum(x => (long) x);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(p.Select(int.Parse).ToArray())}");
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

func suma(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("suma=%d\n", suma(nums...))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(nums: &[i64]) -> i64 {
    nums.iter().sum()
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(&nums));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    /* C variádico real usa stdarg.h; aquí sumamos leyendo la entrada. */
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega filas, no argumentos variádicos.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function suma(...$nums) {
    return array_sum($nums);
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "suma=" . suma(...$nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `*nums` (Python), `...nums` (JS/Java), `nums ...int` (Go), `&[i64]` (Rust). |
| Semántica | Los argumentos se recolectan en una colección dentro de la función. |
| Paradigmática | SQL agrega filas con SUM(), no argumentos. |

## 🧬 El concepto en la familia

En Ruby `def suma(*nums)`. En C, `stdarg.h` con `va_list` (más manual).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 076
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir empaquetar con desempaquetar** → causa: pasar una lista donde se esperan sueltos → solución: usar el operador de expansión (`*`, `...`) al desempaquetar
- **Olvidar el caso de cero argumentos** → causa: error o suma indefinida → solución: que la función maneje la lista vacía (suma 0)

## ❓ Preguntas frecuentes

- **¿Variádica o pasar una lista?** Variádica para llamadas cómodas; lista cuando ya la tienes construida.
- **¿C tiene variádicas?** Sí, con `stdarg.h`, pero es más manual y propenso a errores.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 075](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 077 ⏭️](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md)
