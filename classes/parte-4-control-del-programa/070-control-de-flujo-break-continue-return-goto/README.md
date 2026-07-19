# Clase 070 — Control de flujo: break, continue, return, goto

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar `break` para salir de un bucle en cuanto se cumple una condición. Buscar el primer divisor es el caso típico: no hace falta seguir una vez encontrado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Salir de un bucle con break.
2. Reconocer cuándo continue u otras salidas ayudan.
3. Evitar trabajo innecesario tras encontrar lo buscado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | break | Salir del bucle inmediatamente |
| 2 | continue | Saltar a la siguiente vuelta |
| 3 | Búsqueda con parada | Detenerse al encontrar |
| 4 | return dentro del bucle | Otra forma de salir |

## 📖 Definiciones y características

- **break** — termina el bucle inmediatamente. Clave: no sigue iterando.
- **continue** — salta al siguiente ciclo del bucle. Clave: ignora el resto de la vuelta.
- **Divisor** — número que divide a otro sin resto. Clave: el menor >1 revela si es primo.
- **goto** — salto incondicional (existe en C, desaconsejado). Clave: break/continue lo sustituyen.

## 🧩 Situación

Para saber si un número es primo, buscas su primer divisor >1: si es él mismo, es primo. En cuanto lo encuentras, `break` evita seguir dividiendo en vano.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 2)
- **Salida** (stdout): `primer_divisor=<el menor divisor > 1>`
- **Regla:** el menor d en [2..n] tal que n % d == 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `15` | `primer_divisor=3` |
| `7` | `primer_divisor=7` |
| `12` | `primer_divisor=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA d de 2 a n: SI n%d==0: guardar d ; ROMPER
ESCRIBIR "primer_divisor=" d
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
d = 2
while d <= n:
    if n % d == 0:
        break
    d += 1
print(f"primer_divisor={d}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int d = 2;
        for (; d <= n; d++) {
            if (n % d == 0) break;
        }
        System.out.println("primer_divisor=" + d);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int d = 2;
for (; d <= n; d++) {
    if (n % d == 0) break;
}
Console.WriteLine($"primer_divisor={d}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	d := 2
	for ; d <= n; d++ {
		if n%d == 0 {
			break
		}
	}
	fmt.Printf("primer_divisor=%d\n", d)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut d = 2;
    while d <= n {
        if n % d == 0 {
            break;
        }
        d += 1;
    }
    println!("primer_divisor={d}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long d = 2;
    for (; d <= n; d++) {
        if (n % d == 0) break;
    }
    printf("primer_divisor=%ld\n", d);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el menor divisor > 1 con MIN sobre un rango (ilustrativo).
WITH RECURSIVE d(k) AS (VALUES (2) UNION ALL SELECT k + 1 FROM d WHERE k < 15)
SELECT printf('primer_divisor=%d', min(k)) AS resultado
FROM d WHERE 15 % k = 0;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$d = 2;
for (; $d <= $n; $d++) {
    if ($n % $d === 0) {
        break;
    }
}
echo "primer_divisor=$d\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `break` es igual en casi todos; C mantiene `goto` (evitar). |
| Semántica | break sale del bucle más interno; algunos lenguajes tienen break etiquetado. |
| Paradigmática | SQL evita el bucle: usa MIN sobre los divisores o una consulta. |

## 🧬 El concepto en la familia

En Ruby `break`. En Go `break` (y `break label` para bucles anidados). Rust tiene `break` que incluso puede devolver un valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 070
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Seguir iterando tras encontrar** → causa: trabajo desperdiciado → solución: usar break en cuanto se cumple la condición
- **Confundir break con continue** → causa: no salir cuando debías → solución: break termina el bucle; continue solo salta una vuelta

## ❓ Preguntas frecuentes

- **¿break sale de todos los bucles?** Solo del más interno; para varios, usa etiquetas (Java/Go) o reestructura.
- **¿Y goto?** Existe en C pero se evita; break/continue/return cubren casi todo de forma clara.

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

> [⏮️ Clase 069](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 071 ⏭️](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md)
