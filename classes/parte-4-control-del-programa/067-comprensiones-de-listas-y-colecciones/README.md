# Clase 067 — Comprensiones de listas y colecciones

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Filtrar una colección con una **comprensión** (list comprehension): construir una nueva lista seleccionando elementos que cumplen una condición, de forma declarativa y compacta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Filtrar una colección con una comprensión.
2. Expresar 'los que cumplen X' de forma declarativa.
3. Comparar la comprensión con el bucle equivalente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comprensión | Construir una lista describiéndola |
| 2 | Filtro | Quedarse con los que cumplen |
| 3 | Declarativo | Decir qué, no cómo |
| 4 | Comprensión vs. bucle | Más compacto y legible |

## 📖 Definiciones y características

- **Comprensión de lista** — expresión que construye una lista filtrando/transformando otra. Clave: declarativa y compacta.
- **Filtro** — condición que decide qué elementos entran. Clave: `if x % 2 == 0`.
- **Predicado** — condición booleana sobre cada elemento. Clave: define el filtro.
- **Estilo declarativo** — describir el resultado, no los pasos. Clave: menos ruido que el bucle.

## 🧩 Situación

Quedarse con los pedidos pagados, los usuarios activos, los números pares: filtrar es constante. La comprensión `[x for x in lista if x%2==0]` dice justo eso en una línea.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `pares=<los pares unidos por -, en orden>`
- **Regla:** pares = [x ∈ lista : x par]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `pares=2-4` |
| `10 15 20` | `pares=10-20` |
| `6 7 8` | `pares=6-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
pares <- [x EN lista SI x es par]
ESCRIBIR "pares=" UNIR(pares, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
pares = [x for x in nums if x % 2 == 0]
print("pares=" + "-".join(str(x) for x in pares))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares: number[] = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        String pares = Arrays.stream(p)
                .map(Integer::parseInt)
                .filter(x -> x % 2 == 0)
                .map(String::valueOf)
                .collect(Collectors.joining("-"));
        System.out.println("pares=" + pares);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pares = p.Select(int.Parse).Where(x => x % 2 == 0);
Console.WriteLine($"pares={string.Join("-", pares)}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var pares []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			pares = append(pares, strconv.Itoa(n))
		}
	}
	fmt.Printf("pares=%s\n", strings.Join(pares, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let pares: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| x.to_string())
        .collect();
    println!("pares={}", pares.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("pares=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: filtra con WHERE.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'pares=' || group_concat(x, '-') AS resultado FROM nums WHERE x % 2 = 0;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pares = array_filter($nums, fn($x) => (int) $x % 2 === 0);
echo "pares=" . implode("-", $pares) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[x for x in l if x%2==0]` (Python) vs. `l.filter(...)` (JS/Rust) vs. bucle (C). |
| Semántica | La comprensión crea una lista nueva; el original no cambia. |
| Paradigmática | SQL filtra con `WHERE x % 2 = 0`. |

## 🧬 El concepto en la familia

En Ruby `lista.select { |x| x.even? }`. En Haskell `[x | x <- xs, even x]`, de donde Python tomó la idea.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 067
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar la lista mientras la recorres** → causa: resultados imprevisibles → solución: construir una lista nueva con la comprensión
- **Confundir filtrar con transformar** → causa: cambiar valores en vez de seleccionarlos → solución: filtrar mantiene los elementos; map los transforma

## ❓ Preguntas frecuentes

- **¿Comprensión o filter?** Equivalentes; la comprensión es más legible en Python, `filter` en JS/Rust.
- **¿Es más lento que un bucle?** No de forma significativa; suele ser igual o más rápido y más claro.

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

> [⏮️ Clase 066](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 068 ⏭️](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md)
