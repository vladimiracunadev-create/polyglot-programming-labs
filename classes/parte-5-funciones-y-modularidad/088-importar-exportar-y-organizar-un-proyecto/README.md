# Clase 088 — Importar, exportar y organizar un proyecto

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte usando la **biblioteca estándar**: importar y usar funciones ya provistas por el lenguaje (aquí, valor absoluto). Organizar un proyecto también es saber qué reutilizar en vez de reescribir.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Importar una función de la biblioteca estándar.
2. Reconocer qué ya viene resuelto.
3. Explicar import/include/use en cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Biblioteca estándar | Lo que trae el lenguaje |
| 2 | Importar | Traer una función incorporada |
| 3 | No reinventar | Reutilizar lo que existe |
| 4 | Organizar el proyecto | Estructura e imports |

## 📖 Definiciones y características

- **Biblioteca estándar** — conjunto de módulos incluidos con el lenguaje. Clave: funciones listas para usar.
- **Importar/incluir** — traer un módulo o cabecera (`import`, `#include`, `use`). Clave: acceder a sus funciones.
- **Valor absoluto** — distancia a cero, siempre no negativa. Clave: `abs(-5) = 5`.
- **Reutilización** — usar código existente en vez de reescribir. Clave: menos errores.

## 🧩 Situación

El valor absoluto ya está en la biblioteca estándar de todos los lenguajes. Saber importarlo y usarlo, en vez de escribir tu propio `if x<0`, es parte de organizar bien un proyecto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `abs=<|n|>`
- **Regla:** abs(n) = |n|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `abs=5` |
| `3` | `abs=3` |
| `0` | `abs=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR abs de la biblioteca
LEER n ; ESCRIBIR "abs=" abs(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"abs={abs(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
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
        System.out.println("abs=" + Math.abs(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"abs={Math.Abs(n)}");
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
	if n < 0 {
		n = -n
	}
	fmt.Printf("abs=%d\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("abs={}", n.abs());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("abs=%ld\n", labs(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: abs() incorporado.
WITH nums(n) AS (VALUES (-5), (3), (0))
SELECT printf('abs=%d', abs(n)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "abs=" . abs($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `abs()` (Python built-in), `Math.abs` (JS/Java), `#include <stdlib.h>` (C), `n.abs()` (Rust). |
| Semántica | La función estándar maneja los casos; no hay que reimplementarla. |
| Paradigmática | SQL usa `abs()` incorporado. |

## 🧬 El concepto en la familia

En Ruby `n.abs`. En Go `math.Abs` opera con float; para enteros se usa una función propia o un condicional.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 088
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Reimplementar lo que ya existe** → causa: más código y más bugs → solución: buscar primero en la biblioteca estándar
- **Olvidar el import/include** → causa: función no encontrada → solución: importar el módulo correcto (math, stdlib)

## ❓ Preguntas frecuentes

- **¿Siempre usar la estándar?** Para lo común, sí: está probada y optimizada.
- **¿Go no tiene abs de enteros?** `math.Abs` es para float; para int se usa un condicional o una función propia.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 087](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 089 ⏭️](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md)
