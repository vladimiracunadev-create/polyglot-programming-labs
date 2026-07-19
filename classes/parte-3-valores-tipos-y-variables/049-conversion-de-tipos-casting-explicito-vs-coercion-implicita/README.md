# Clase 049 — Conversión de tipos: casting explícito vs. coerción implícita

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **conversión explícita** (casting) de **coerción implícita**. Convertir un texto a real, y ese real a entero (truncando), muestra cómo cada lenguaje exige o realiza la conversión.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Convertir texto a número.
2. Convertir un real a entero por truncamiento.
3. Diferenciar casting explícito de coerción implícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | De texto a número | Parsear la entrada |
| 2 | Truncamiento | Quitar la parte decimal hacia cero |
| 3 | Casting explícito | El programador ordena la conversión |
| 4 | Coerción implícita | El lenguaje convierte solo |

## 📖 Definiciones y características

- **Conversión (casting)** — cambiar el tipo de un valor explícitamente. Clave: `int(x)`, `(long)f`.
- **Coerción** — conversión automática que hace el lenguaje. Clave: fuente de sorpresas en los débilmente tipados.
- **Truncamiento** — descartar la parte decimal hacia cero. Clave: distinto de redondear.
- **Parseo** — interpretar un texto como un número. Clave: primer paso de casi toda entrada.

## 🧩 Situación

Un formulario entrega '3.7' como texto. Para calcular hay que convertirlo a número, y quizá a entero. Cada lenguaje exige un grado distinto de explicitud, y truncar no es redondear.

## 🧮 Modelo

- **Entrada** (stdin): un número real como texto
- **Salida** (stdout): `entero=<parte entera truncada> real=<valor con 2 decimales>`
- **Regla:** entero = truncar(real) ; real formateado a 2 decimales

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3.7` | `entero=3 real=3.70` |
| `5.0` | `entero=5 real=5.00` |
| `8.9` | `entero=8 real=8.90` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER texto
real <- A_REAL(texto)
entero <- TRUNCAR(real)
ESCRIBIR "entero=" entero " real=" FORMATEAR(real,2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

f = float(sys.stdin.readline().strip())
print(f"entero={int(f)} real={f:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const f = parseFloat(readFileSync(0, "utf8").trim());
console.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const f: number = parseFloat(readFileSync(0, "utf8").trim());
console.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);
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
        double f = Double.parseDouble(br.readLine().trim());
        System.out.printf(Locale.US, "entero=%d real=%.2f%n", (long) f, f);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
double f = double.Parse(Console.In.ReadToEnd().Trim(), inv);
Console.WriteLine($"entero={(long)f} real={f.ToString("F2", inv)}");
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
	f, _ := strconv.ParseFloat(strings.TrimSpace(line), 64)
	fmt.Printf("entero=%d real=%.2f\n", int64(f), f)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let f: f64 = s.trim().parse().unwrap();
    println!("entero={} real={:.2}", f as i64, f);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    double f;
    if (scanf("%lf", &f) != 1) return 1;
    printf("entero=%ld real=%.2f\n", (long) f, f);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: CAST(x AS INTEGER) trunca hacia cero.
WITH nums(x) AS (VALUES (3.7), (5.0), (8.9))
SELECT printf('entero=%d real=%.2f', CAST(x AS INTEGER), x) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$f = (float) trim(fgets(STDIN));
printf("entero=%d real=%.2f\n", (int) $f, $f);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `int(f)` (Python), `Math.trunc` (JS), `(long)f` (Java/C/C#), `f as i64` (Rust). |
| Semántica | El truncamiento va hacia cero; no confundir con redondeo (`round`). |
| Paradigmática | SQL usa `CAST(x AS INTEGER)`. |

## 🧬 El concepto en la familia

En Ruby `f.to_i` trunca. En Haskell `truncate f`. En C++ `static_cast<long>(f)`. Todos truncan hacia cero (para positivos, igual que floor).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 049
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir truncar con redondear** → causa: esperar 4 de 3.7 → solución: usar la conversión a entero (trunca), no round
- **Sumar texto y número** → causa: olvidar convertir la entrada → solución: parsear siempre el texto antes de operar

## ❓ Preguntas frecuentes

- **¿Truncar y floor son lo mismo?** Para positivos sí; para negativos no (trunc va a cero, floor hacia abajo).
- **¿Qué es coerción implícita?** Que el lenguaje convierta sin pedirlo (p. ej. PHP suma '3'+4). Puede sorprender.

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

> [⏮️ Clase 048](../../parte-3-valores-tipos-y-variables/048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 050 ⏭️](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md)
