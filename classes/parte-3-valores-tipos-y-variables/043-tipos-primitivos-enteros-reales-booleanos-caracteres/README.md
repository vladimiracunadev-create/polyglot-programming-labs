# Clase 043 — Tipos primitivos: enteros, reales, booleanos, caracteres

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver los tipos primitivos en acción: el mismo número tratado como **entero**, convertido a **real** y evaluado como **booleano**. Cada lenguaje formatea y convierte de forma propia, pero el concepto de 'tipo primitivo' es universal.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir entero, real y booleano como tipos primitivos.
2. Convertir un entero a real y formatearlo con decimales.
3. Producir un valor booleano a partir de una condición.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entero | Número sin parte fraccionaria |
| 2 | Real (punto flotante) | Número con decimales; se formatea explícitamente |
| 3 | Booleano | Verdadero o falso, resultado de una condición |
| 4 | Formato de salida | true/false y decimales difieren entre lenguajes |

## 📖 Definiciones y características

- **Tipo primitivo** — tipo básico incorporado al lenguaje (entero, real, booleano, carácter). Clave: bloque elemental de todo dato.
- **Entero** — número sin decimales, de tamaño fijo en los estáticos. Clave: aritmética exacta.
- **Real** — número en coma flotante. Clave: aproximado; se formatea con un número de decimales.
- **Booleano** — valor de verdad (verdadero/falso). Clave: gobierna las decisiones del programa.

## 🧩 Situación

Un mismo `4` puede verse como entero (`4`), como real (`4.0`) o dar lugar a un booleano (`4 es par → true`). Reconocer que el valor es uno y los tipos son lentes distintas es clave.

## 🧮 Modelo

- **Entrada** (stdin): una línea `n` (un entero)
- **Salida** (stdout): `entero=<n> real=<n con 1 decimal> par=<true|false>`
- **Regla:** real = (double) n ; par = (n módulo 2 == 0)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `entero=4 real=4.0 par=true` |
| `7` | `entero=7 real=7.0 par=false` |
| `0` | `entero=0 real=0.0 par=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
real <- CONVERTIR_A_REAL(n)
par <- (n MOD 2 == 0)
ESCRIBIR "entero=" n " real=" FORMATEAR(real,1) " par=" par
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
real = float(n)
par = "true" if n % 2 == 0 else "false"
print(f"entero={n} real={real:.1f} par={par}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const par = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const par: string = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String par = (n % 2 == 0) ? "true" : "false";
        System.out.printf(Locale.US, "entero=%d real=%.1f par=%s%n", n, (double) n, par);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
int n = int.Parse(Console.In.ReadToEnd().Trim(), inv);
string par = (n % 2 == 0) ? "true" : "false";
Console.WriteLine($"entero={n} real={((double)n).ToString("F1", inv)} par={par}");
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
	par := "false"
	if n%2 == 0 {
		par = "true"
	}
	fmt.Printf("entero=%d real=%.1f par=%s\n", n, float64(n), par)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let par = if n % 2 == 0 { "true" } else { "false" };
    println!("entero={n} real={:.1} par={par}", n as f64);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *par = (n % 2 == 0) ? "true" : "false";
    printf("entero=%ld real=%.1f par=%s\n", n, (double) n, par);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene un tipo booleano nativo universal: se usa CASE WHEN.
WITH nums(n) AS (VALUES (4), (7), (0))
SELECT printf('entero=%d real=%.1f par=%s', n, n,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$par = ($n % 2 === 0) ? "true" : "false";
printf("entero=%d real=%.1f par=%s\n", $n, (float) $n, $par);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El formato de real (`%.1f`, `toFixed(1)`, `F1`) y de booleano varían. |
| Semántica | C#/Go escriben `True`/`true` distinto: hay que forzar minúsculas para igualar. |
| Paradigmática | SQL expresa el booleano con `CASE WHEN`, no con un tipo booleano nativo universal. |

## 🧬 El concepto en la familia

En Ruby `4.to_f` da el real y `4.even?` el booleano. En Haskell los tipos son explícitos (`Int`, `Double`, `Bool`) y la conversión es una función (`fromIntegral`).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 043
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True` con mayúscula** → causa: el `ToString` de C# capitaliza los booleanos → solución: formatear el booleano a minúsculas manualmente
- **Esperar `4` en vez de `4.0`** → causa: olvidar el formato de real → solución: formatear con el número de decimales fijado por el contrato

## ❓ Preguntas frecuentes

- **¿`4` y `4.0` son el mismo valor?** Matemáticamente sí; para el tipo del lenguaje, no: uno es entero y otro real.
- **¿Por qué C# escribe True/False?** Su `bool.ToString()` capitaliza; por eso se formatea a minúsculas para el contrato.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

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

> [⏮️ Clase 042](../../parte-3-valores-tipos-y-variables/042-declaracion-asignacion-e-inicializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 044 ⏭️](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md)
