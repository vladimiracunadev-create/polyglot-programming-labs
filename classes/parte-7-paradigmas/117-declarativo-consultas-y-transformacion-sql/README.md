# Clase 117 — Declarativo: consultas y transformación (SQL)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **declarativo**: describir *qué* resultado se quiere, no *cómo* obtenerlo. Sumar los pares se expresa como 'la suma de los que son pares', dejando el cómo al lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Expresar un cálculo de forma declarativa.
2. Combinar filtro y agregación.
3. Contrastar con el estilo imperativo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarativo | Describir el resultado |
| 2 | Filtro + agregación | Seleccionar y combinar |
| 3 | SQL como declarativo | WHERE + SUM |

## 📖 Definiciones y características

- **Declarativo** — paradigma que describe el resultado deseado, no los pasos. Clave: el motor decide el cómo.
- **Filtro** — seleccionar los elementos que cumplen una condición. Clave: `WHERE`, `filter`.
- **Agregación** — combinar varios valores en uno (suma). Clave: `SUM`, `reduce`.

## 🧩 Situación

'La suma de los pedidos pagados', 'el total de las ventas del mes': el estilo declarativo describe el resultado. SQL es su máximo exponente: `SELECT SUM(x) WHERE ...`.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma_pares=<suma de los pares>`
- **Regla:** suma de los x tales que x es par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma_pares=6` |
| `2 4 6` | `suma_pares=12` |
| `1 3 5` | `suma_pares=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma_pares <- SUMA(FILTRAR(par, lista))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma_pares={sum(x for x in nums if x % 2 == 0)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const suma = nums.filter((x) => x % 2 === 0).reduce((a, b) => a + b, 0);
console.log(`suma_pares=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const suma = nums.filter((x) => x % 2 === 0).reduce((a, b) => a + b, 0);
console.log(`suma_pares=${suma}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long suma = Arrays.stream(p).mapToInt(Integer::parseInt).filter(x -> x % 2 == 0).sum();
        System.out.println("suma_pares=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = p.Select(int.Parse).Where(x => x % 2 == 0).Sum(x => (long) x);
Console.WriteLine($"suma_pares={suma}");
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
	suma := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			suma += n
		}
	}
	fmt.Printf("suma_pares=%d\n", suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let suma: i64 = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .sum();
    println!("suma_pares={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) suma += x;
    }
    printf("suma_pares=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: WHERE + SUM, puro estilo declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma_pares=%d', COALESCE(sum(x), 0)) AS resultado FROM nums WHERE x % 2 = 0;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$suma = array_sum(array_filter($nums, fn($x) => $x % 2 === 0));
echo "suma_pares=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `sum(x for x in l if x%2==0)` (Python), `filter+reduce` (JS), `WHERE+SUM` (SQL). |
| Semántica | Se describe el resultado; el cómo queda implícito. |
| Paradigmática | El imperativo recorrería y acumularía a mano. |

## 🧬 El concepto en la familia

En Haskell `sum (filter even xs)`. SQL es el declarativo por excelencia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 117
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar el cómo con el qué** → causa: perder la claridad declarativa → solución: describir el resultado, dejar el cómo al lenguaje
- **Olvidar el caso sin pares** → causa: esperar error en vez de 0 → solución: la suma vacía es 0

## ❓ Preguntas frecuentes

- **¿Declarativo siempre es mejor?** Es más legible para transformaciones de datos; el imperativo da más control fino.
- **¿SQL es declarativo?** Sí, el ejemplo canónico: describes el resultado, no el algoritmo.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 116](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 118 ⏭️](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md)
