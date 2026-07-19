# Clase 152 — Rendimiento y perfilado (profiling)

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **rendimiento y el perfilado (profiling)**: medir dónde se gasta el tiempo o cuántas operaciones se hacen para optimizar con datos, no por intuición. Contar las operaciones de una suma es un perfilado en miniatura.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar las operaciones de un algoritmo.
2. Explicar el perfilado.
3. Relacionar operaciones con complejidad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Perfilado | Medir dónde se gasta el coste |
| 2 | Conteo de operaciones | Cuánto trabajo se hace |
| 3 | Optimizar con datos | No por intuición |

## 📖 Definiciones y características

- **Perfilado** — medir el uso de tiempo/recursos de un programa. Clave: optimizar con evidencia.
- **Operación** — unidad de trabajo (una suma, una comparación). Clave: contarlas estima el coste.
- **Cuello de botella** — la parte que domina el coste. Clave: optimizar ahí primero.

## 🧩 Situación

Antes de optimizar, se perfila: ¿dónde se gasta el tiempo? Contar operaciones (aquí, n sumas para sumar 1..n) revela la complejidad y guía las mejoras hacia donde importan.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `operaciones=<n> resultado=<1+...+n>`
- **Regla:** sumar 1..n contando cada suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `operaciones=5 resultado=15` |
| `1` | `operaciones=1 resultado=1` |
| `3` | `operaciones=3 resultado=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
ops <- 0 ; suma <- 0 ; PARA i de 1 a n: suma+=i ; ops++
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
ops = 0
suma = 0
for i in range(1, n + 1):
    suma += i
    ops += 1
print(f"operaciones={ops} resultado={suma}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
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
        long ops = 0, suma = 0;
        for (int i = 1; i <= n; i++) {
            suma += i;
            ops += 1;
        }
        System.out.println("operaciones=" + ops + " resultado=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long ops = 0, suma = 0;
for (int i = 1; i <= n; i++) {
    suma += i;
    ops += 1;
}
Console.WriteLine($"operaciones={ops} resultado={suma}");
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
	ops, suma := 0, 0
	for i := 1; i <= n; i++ {
		suma += i
		ops++
	}
	fmt.Printf("operaciones=%d resultado=%d\n", ops, suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut ops = 0i64;
    let mut suma = 0i64;
    for i in 1..=n {
        suma += i;
        ops += 1;
    }
    println!("operaciones={ops} resultado={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long ops = 0, suma = 0;
    for (long i = 1; i <= n; i++) {
        suma += i;
        ops++;
    }
    printf("operaciones=%ld resultado=%ld\n", ops, suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se perfila con EXPLAIN; aquí, conteo y suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('operaciones=%d resultado=%d', count(*), sum(i)) AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$ops = 0;
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
    $ops++;
}
echo "operaciones=$ops resultado=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contador de operaciones en el bucle. |
| Semántica | El conteo estima el coste (O(n) aquí). |
| Paradigmática | SQL se perfila con EXPLAIN. |

## 🧬 El concepto en la familia

perf, valgrind (C), cProfile (Python), pprof (Go), el profiler de la JVM/.NET miden el rendimiento real.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 152
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Optimizar sin medir** → causa: atacar lo que no es el cuello de botella → solución: perfilar primero
- **Micro-optimizar lo irrelevante** → causa: esfuerzo desperdiciado → solución: optimizar el cuello de botella real

## ❓ Preguntas frecuentes

- **¿Contar operaciones o cronometrar?** El conteo estima la complejidad; el cronómetro mide el tiempo real.
- **¿Perfilar en desarrollo o producción?** Ambos: en desarrollo para iterar; en producción para casos reales.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 151](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 153 ⏭️](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md)
