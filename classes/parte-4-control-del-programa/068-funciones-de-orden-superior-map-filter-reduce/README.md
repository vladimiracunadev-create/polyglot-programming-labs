# Clase 068 — Funciones de orden superior: map, filter, reduce

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Combinar las tres funciones de orden superior clásicas: **map** (transformar cada elemento), **filter** (seleccionar) y **reduce** (combinar en un valor). Aquí se usan map y reduce sobre una lista.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección con map.
2. Combinar una colección con reduce.
3. Encadenar operaciones de orden superior.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | map | Transformar cada elemento |
| 2 | reduce | Combinar en un solo valor |
| 3 | Funciones de orden superior | Reciben otra función |
| 4 | Encadenar | map y luego reduce |

## 📖 Definiciones y características

- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: transforma sin mutar.
- **reduce** — combina todos los elementos en un valor (suma, producto). Clave: acumula.
- **Función de orden superior** — recibe o devuelve otra función. Clave: base del estilo funcional.
- **Encadenamiento** — conectar operaciones (map → reduce). Clave: pipeline de datos.

## 🧩 Situación

Calcular el total de una factura con IVA: `map` aplica el IVA a cada línea y `reduce` las suma. map/filter/reduce son el lenguaje común del procesamiento de datos.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por -> total=<suma de los doblados>`
- **Regla:** doblados = map(x→2x) ; total = reduce(+, doblados)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6 total=12` |
| `5` | `doblados=10 total=10` |
| `2 4` | `doblados=4-8 total=12` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
doblados <- MAP(x -> 2x, lista)
total <- REDUCE(+, doblados)
ESCRIBIR "doblados=" UNIR(doblados,"-") " total=" total
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = [x * 2 for x in nums]
total = sum(doblados)
print(f"doblados={'-'.join(str(x) for x in doblados)} total={total}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
const total = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
const total: number = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> doblados = Arrays.stream(p)
                .map(Integer::parseInt)
                .map(x -> x * 2)
                .collect(Collectors.toList());
        int total = doblados.stream().mapToInt(Integer::intValue).sum();
        String s = doblados.stream().map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + s + " total=" + total);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2).ToList();
int total = doblados.Sum();
Console.WriteLine($"doblados={string.Join("-", doblados)} total={total}");
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
	var doblados []string
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		d := n * 2
		doblados = append(doblados, strconv.Itoa(d))
		total += d
	}
	fmt.Printf("doblados=%s total=%d\n", strings.Join(doblados, "-"), total)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<i64> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap() * 2)
        .collect();
    let total: i64 = doblados.iter().sum();
    let texto: Vec<String> = doblados.iter().map(|x| x.to_string()).collect();
    println!("doblados={} total={}", texto.join("-"), total);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x, total = 0;
    int primero = 1;
    printf("doblados=");
    long primeros[1024];
    int k = 0;
    while (scanf("%ld", &x) == 1) {
        primeros[k++] = x * 2;
    }
    for (int i = 0; i < k; i++) {
        if (!primero) printf("-");
        printf("%ld", primeros[i]);
        total += primeros[i];
        primero = 0;
    }
    printf(" total=%ld\n", total);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el 'map' va en el SELECT y el 'reduce' con SUM().
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') || printf(' total=%d', sum(x * 2)) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$doblados = array_map(fn($x) => (int) $x * 2, $nums);
$total = array_reduce($doblados, fn($a, $b) => $a + $b, 0);
echo "doblados=" . implode("-", $doblados) . " total=$total\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map`/`sum` (Python) vs. `.map().reduce()` (JS) vs. `.iter().map().sum()` (Rust). |
| Semántica | map/reduce no mutan la lista original; devuelven valores nuevos. |
| Paradigmática | SQL hace el 'map' en el SELECT y el 'reduce' con SUM(). |

## 🧬 El concepto en la familia

En Ruby `lista.map { |x| x*2 }.sum`. En Haskell `sum (map (*2) xs)`, el origen de este estilo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 068
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mutar dentro del map** → causa: efectos secundarios inesperados → solución: usar map para transformar, sin cambiar estado externo
- **Confundir map con for-each** → causa: map devuelve una colección; for-each no → solución: usar map cuando quieres el resultado transformado

## ❓ Preguntas frecuentes

- **¿reduce es lo mismo que un bucle de suma?** Sí en esencia; reduce lo expresa de forma declarativa y reutilizable.
- **¿Y filter?** Selecciona elementos; aquí no se usó, pero completa el trío map/filter/reduce.

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

> [⏮️ Clase 067](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 069 ⏭️](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md)
