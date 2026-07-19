# Clase 138 — Depuración: cómo se diagnostica en cada runtime

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la **depuración**: cómo se diagnostica un programa. Inspeccionar el valor de las variables (aquí, el número y sus potencias) es lo que hace un depurador al pausar la ejecución.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Inspeccionar el estado de un cálculo.
2. Explicar qué hace un depurador.
3. Nombrar los depuradores por runtime.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Depuración | Encontrar y entender fallos |
| 2 | Inspección de variables | Ver los valores en un punto |
| 3 | Puntos de ruptura | Pausar la ejecución |

## 📖 Definiciones y características

- **Depurador** — herramienta para pausar, inspeccionar y avanzar un programa (gdb, lldb, pdb). Clave: ver el estado real.
- **Punto de ruptura** — lugar donde el depurador pausa la ejecución. Clave: para inspeccionar ahí.
- **Inspección** — examinar el valor de las variables en un momento. Clave: la base del diagnóstico.

## 🧩 Situación

Cuando un resultado sorprende, se pausa en un punto de ruptura y se inspeccionan las variables. Mostrar el número, su cuadrado y su cubo simula esa inspección del estado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `valor=<n> cuadrado=<n²> cubo=<n³>`
- **Regla:** inspeccionar n, n² y n³

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `valor=3 cuadrado=9 cubo=27` |
| `2` | `valor=2 cuadrado=4 cubo=8` |
| `5` | `valor=5 cuadrado=25 cubo=125` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n, n*n, n*n*n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"valor={n} cuadrado={n * n} cubo={n * n * n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("valor=" + n + " cuadrado=" + (n * n) + " cubo=" + (n * n * n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"valor={n} cuadrado={n * n} cubo={n * n * n}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("valor=%d cuadrado=%d cubo=%d\n", n, n*n, n*n*n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("valor={} cuadrado={} cubo={}", n, n * n, n * n * n);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("valor=%ld cuadrado=%ld cubo=%ld\n", n, n * n, n * n * n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se inspeccionan los valores calculados.
WITH nums(n) AS (VALUES (3), (2), (5))
SELECT printf('valor=%d cuadrado=%d cubo=%d', n, n * n, n * n * n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "valor=$n cuadrado=" . ($n * $n) . " cubo=" . ($n * $n * $n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Idéntica: calcular potencias. |
| Semántica | Cada runtime tiene su depurador (pdb, gdb, lldb, el del IDE). |
| Paradigmática | SQL se depura con EXPLAIN y consultas de prueba. |

## 🧬 El concepto en la familia

gdb/lldb (C/C++/Rust), pdb (Python), el depurador de la JVM y de .NET, y los integrados en los IDE.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 138
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depurar cambiando al azar** → causa: no observar el estado → solución: inspeccionar variables en puntos clave
- **Llenar el código de prints y olvidarlos** → causa: ruido y regresiones → solución: preferir el depurador o quitar los prints al terminar

## ❓ Preguntas frecuentes

- **¿print o depurador?** El print es rápido; el depurador permite inspeccionar sin recompilar y avanzar paso a paso.
- **¿Cómo se depura SQL?** Con EXPLAIN (plan de ejecución) y consultas de prueba sobre subconjuntos.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 137](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 139 ⏭️](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md)
