# Clase 050 — Tipado estático vs. dinámico

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la diferencia entre **tipado estático** (el tipo se fija y comprueba al compilar) y **dinámico** (se resuelve al ejecutar). Sumar un entero con un real obliga, en los estáticos, a una conversión explícita que en los dinámicos ocurre sola.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Sumar valores de tipos distintos (entero + real).
2. Reconocer dónde hace falta convertir explícitamente.
3. Explicar estático vs. dinámico con un ejemplo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipado estático | El compilador conoce y comprueba los tipos |
| 2 | Tipado dinámico | El tipo se conoce al ejecutar |
| 3 | Promoción numérica | Entero que se convierte a real para operar |
| 4 | Errores en compilación vs. ejecución | Cuándo se detecta un tipo mal usado |

## 📖 Definiciones y características

- **Tipado estático** — los tipos se fijan y comprueban en compilación (Java, C#, Go, Rust, C). Clave: errores antes de ejecutar.
- **Tipado dinámico** — los tipos se resuelven en ejecución (Python, PHP, JS). Clave: flexible, errores más tarde.
- **Promoción** — convertir un entero a real para operar con otro real. Clave: en estáticos suele ser explícita.
- **Comprobación de tipos** — verificar que las operaciones son válidas para los tipos. Clave: estática o dinámica.

## 🧩 Situación

Sumar `2 + 3.5`: en Python simplemente da `5.5`; en Go debes convertir el entero a `float64` primero. La misma operación revela la filosofía de tipos de cada lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (a entero, b real)
- **Salida** (stdout): `suma=<a+b con 2 decimales>`
- **Regla:** suma = a + b (a entero promovido a real)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 3.5` | `suma=5.50` |
| `10 0.25` | `suma=10.25` |
| `0 0` | `suma=0.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a (entero), b (real)
ESCRIBIR "suma=" FORMATEAR(a+b, 2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

p = sys.stdin.readline().split()
a = int(p[0])
b = float(p[1])
print(f"suma={a + b:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
const a = parseInt(x, 10);
const b = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [x, y]: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const a: number = parseInt(x, 10);
const b: number = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
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
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        double b = Double.parseDouble(p[1]);
        System.out.printf(Locale.US, "suma=%.2f%n", a + b);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)}");
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
	b, _ := strconv.ParseFloat(f[1], 64)
	fmt.Printf("suma=%.2f\n", float64(a)+b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = v[0].parse().unwrap();
    let b: f64 = v[1].parse().unwrap();
    println!("suma={:.2}", a as f64 + b);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a;
    double b;
    if (scanf("%ld %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f\n", (double) a + b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL evalúa la expresión numérica de forma uniforme.
WITH pares(a, b) AS (VALUES (2, 3.5), (10, 0.25), (0, 0))
SELECT printf('suma=%.2f', a + b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $x;
$b = (float) $y;
printf("suma=%.2f\n", $a + $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Python/PHP suman directo; Go exige `float64(a)+b`. |
| Semántica | En estáticos el tipo del resultado se decide en compilación; en dinámicos, al ejecutar. |
| Paradigmática | SQL trata los números de forma uniforme en la expresión. |

## 🧬 El concepto en la familia

En Ruby `a + b` funciona por coerción numérica. En Haskell (estático fuerte) hace falta `fromIntegral a + b`, similar a Go pero más estricto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 050
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Sumar int y float sin convertir en Go/Rust** → causa: el compilador rechaza tipos mezclados → solución: convertir el entero a real explícitamente
- **Confiar en el tipo en un dinámico** → causa: un dato inesperado rompe en ejecución → solución: validar la entrada donde el compilador no ayuda

## ❓ Preguntas frecuentes

- **¿Cuál es mejor?** Estático atrapa errores antes; dinámico itera más rápido. Depende del proyecto.
- **¿Por qué Go obliga a convertir?** Para que la promoción sea visible y no haya conversiones silenciosas.

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

> [⏮️ Clase 049](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 051 ⏭️](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md)
