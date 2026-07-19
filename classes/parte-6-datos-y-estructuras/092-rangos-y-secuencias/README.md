# Clase 092 — Rangos y secuencias

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **rangos y secuencias**: describir una serie de valores consecutivos sin listarlos. Los rangos alimentan bucles y comprensiones de forma expresiva.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar un rango inclusivo.
2. Sumar los valores del rango.
3. Reconocer rangos inclusivos vs. exclusivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Rango | Serie de valores consecutivos |
| 2 | Inclusivo/exclusivo | Si incluye el extremo |
| 3 | Secuencia perezosa | No se materializa entera |

## 📖 Definiciones y características

- **Rango** — intervalo de valores consecutivos (`2..5`). Clave: describe sin enumerar.
- **Inclusivo** — incluye el extremo final. Clave: `1..=n` en Rust, `range` en Python es exclusivo.
- **Secuencia** — serie ordenada de valores. Clave: puede ser perezosa.

## 🧩 Situación

`for i in 1..=100` recorre cien valores sin crear una lista de cien. Los rangos son la forma idiomática de iterar por posiciones.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros, a <= b)
- **Salida** (stdout): `rango=<a-...-b> suma=<suma del rango>`
- **Regla:** rango [a..b] y su suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 5` | `rango=2-3-4-5 suma=14` |
| `1 1` | `rango=1 suma=1` |
| `3 6` | `rango=3-4-5-6 suma=18` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; generar a..b ; sumar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
r = list(range(a, b + 1))
print(f"rango={'-'.join(str(x) for x in r)} suma={sum(r)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r: number[] = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        StringBuilder sb = new StringBuilder();
        long suma = 0;
        for (int i = a; i <= b; i++) {
            if (i > a) sb.append("-");
            sb.append(i);
            suma += i;
        }
        System.out.println("rango=" + sb + " suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var r = Enumerable.Range(a, b - a + 1).ToList();
Console.WriteLine($"rango={string.Join("-", r)} suma={r.Sum()}");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	var parts []string
	suma := 0
	for i := a; i <= b; i++ {
		parts = append(parts, strconv.Itoa(i))
		suma += i
	}
	fmt.Printf("rango=%s suma=%d\n", strings.Join(parts, "-"), suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let r: Vec<i64> = (v[0]..=v[1]).collect();
    let suma: i64 = r.iter().sum();
    let texto: Vec<String> = r.iter().map(|x| x.to_string()).collect();
    println!("rango={} suma={}", texto.join("-"), suma);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long suma = 0;
    printf("rango=");
    for (long i = a; i <= b; i++) {
        if (i > a) printf("-");
        printf("%ld", i);
        suma += i;
    }
    printf(" suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: rango con CTE recursivo (ilustrativo, 2..5).
WITH RECURSIVE r(i) AS (VALUES (2) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT 'rango=' || group_concat(i, '-') || printf(' suma=%d', sum(i)) AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = range((int) $a, (int) $b);
echo "rango=" . implode("-", $r) . " suma=" . array_sum($r) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `range(a, b+1)` (Python), `a..=b` (Rust), bucle (C/Java/Go). |
| Semántica | Python `range` es exclusivo del final; Rust distingue `..` y `..=`. |
| Paradigmática | SQL genera rangos con CTE recursivo. |

## 🧬 El concepto en la familia

En Ruby `(a..b)` es inclusivo, `(a...b)` exclusivo. En Kotlin `a..b` es inclusivo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 092
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Error por el extremo (off-by-one)** → causa: incluir o excluir de más → solución: tener claro si el rango incluye el final
- **Materializar rangos enormes** → causa: gasto de memoria → solución: iterar perezosamente cuando se pueda

## ❓ Preguntas frecuentes

- **¿Rango inclusivo o exclusivo?** Depende del lenguaje; conócelo para no equivocar el extremo.
- **¿Rango consume memoria?** En Python/Rust es perezoso; no crea la lista completa.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 091](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 093 ⏭️](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md)
