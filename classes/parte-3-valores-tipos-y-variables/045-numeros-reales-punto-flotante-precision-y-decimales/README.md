# Clase 045 — Números reales: punto flotante, precisión y decimales

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con números de punto flotante y su formateo. El foco: los reales son **aproximados** (`0.1 + 0.2` no es exactamente `0.3`), y por eso casi siempre se muestran con un número fijo de decimales usando un formato que fuerza la cultura (punto, no coma).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Operar con reales (suma y producto).
2. Formatear un real con un número fijo de decimales.
3. Explicar por qué el punto flotante es aproximado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Punto flotante | Representación aproximada de los reales |
| 2 | Formateo con decimales | Mostrar 2 decimales de forma consistente |
| 3 | Cultura/locale | Punto vs. coma decimal según el sistema |
| 4 | Redondeo | El formateo redondea; cuidado con los empates |

## 📖 Definiciones y características

- **Punto flotante** — representación binaria aproximada de números reales (IEEE 754). Clave: no todos los decimales son exactos.
- **Precisión** — cuántos dígitos significativos conserva un real. Clave: limitada; genera pequeños errores.
- **Formateo** — convertir el real a texto con N decimales. Clave: cómo se presenta el resultado.
- **Cultura invariante** — formato que usa el punto decimal sin importar el idioma del sistema. Clave: evita la coma decimal.

## 🧩 Situación

`0.1 + 0.2` da `0.30000000000000004` en casi todos los lenguajes. No es un bug: es cómo el hardware representa los reales. Por eso el dinero y los resultados se muestran con decimales fijos y formato controlado.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos reales)
- **Salida** (stdout): `suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`
- **Regla:** suma = a + b ; producto = a * b (ambos a 2 decimales)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.5 2.5` | `suma=4.00 producto=3.75` |
| `0.1 0.2` | `suma=0.30 producto=0.02` |
| `10 3` | `suma=13.00 producto=30.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "suma=" FORMATEAR(a+b,2) " producto=" FORMATEAR(a*b,2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(float, sys.stdin.readline().split())
print(f"suma={a + b:.2f} producto={a * b:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
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
        double a = Double.parseDouble(p[0]);
        double b = Double.parseDouble(p[1]);
        System.out.printf(Locale.US, "suma=%.2f producto=%.2f%n", a + b, a * b);
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
double a = double.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)} producto={(a * b).ToString("F2", inv)}");
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
	a, _ := strconv.ParseFloat(f[0], 64)
	b, _ := strconv.ParseFloat(f[1], 64)
	fmt.Printf("suma=%.2f producto=%.2f\n", a+b, a*b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<f64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={:.2} producto={:.2}", v[0] + v[1], v[0] * v[1]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    double a, b;
    if (scanf("%lf %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f producto=%.2f\n", a + b, a * b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL formatea reales con printf dentro de la consulta.
WITH pares(a, b) AS (VALUES (1.5, 2.5), (0.1, 0.2), (10, 3))
SELECT printf('suma=%.2f producto=%.2f', a + b, a * b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (float) $a;
$b = (float) $b;
printf("suma=%.2f producto=%.2f\n", $a + $b, $a * $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `%.2f` (Python/C/Go), `toFixed(2)` (JS), `F2` (C#), `{:.2}` (Rust). |
| Semántica | El locale puede imprimir coma; se fuerza el punto (Locale.US, InvariantCulture). |
| Paradigmática | SQL formatea con `printf('%.2f', ...)` dentro de la consulta. |

## 🧬 El concepto en la familia

En Ruby: `format('%.2f', x)`. En Haskell: `printf "%.2f" x` (de Text.Printf). El problema del punto flotante es idéntico en toda la familia porque todos usan IEEE 754.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 045
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ver `4,00` en vez de `4.00`** → causa: el locale usa coma decimal → solución: forzar cultura invariante (Locale.US / InvariantCulture)
- **Comparar reales con `==`** → causa: esperar igualdad exacta → solución: comparar con una tolerancia, o formatear antes de comparar

## ❓ Preguntas frecuentes

- **¿Por qué 0.1+0.2 no es 0.3?** 0.1 y 0.2 no tienen representación binaria exacta; el error se arrastra a la suma.
- **¿Cómo manejo dinero entonces?** Con decimales fijos y formateo, o con tipos decimales exactos donde el lenguaje los ofrezca.

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

> [⏮️ Clase 044](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 046 ⏭️](../../parte-3-valores-tipos-y-variables/046-booleanos-y-valores-de-verdad/README.md)
