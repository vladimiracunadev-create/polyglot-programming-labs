# Clase 082 — Alcance (scope) y sombreado (shadowing)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **alcance (scope)** de las variables y el **sombreado (shadowing)**: dónde vive una variable y qué pasa cuando una interna reusa el nombre de una externa. Al salir del bloque, reaparece la externa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el alcance de bloque.
2. Predecir el efecto del sombreado.
3. Distinguir la variable interna de la externa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Alcance (scope) | Dónde es visible una variable |
| 2 | Bloque | La región que delimita el alcance |
| 3 | Sombreado | Reusar un nombre en un bloque interno |
| 4 | Restauración | Al salir, vuelve la externa |

## 📖 Definiciones y características

- **Alcance** — región del código donde una variable es visible. Clave: de bloque en la mayoría.
- **Sombreado** — una variable interna con el mismo nombre oculta a la externa. Clave: dentro del bloque.
- **Bloque** — conjunto de sentencias con su propio alcance. Clave: `{ ... }`.
- **Vida de la variable** — cuánto existe. Clave: termina al salir de su alcance.

## 🧩 Situación

Dentro de un bloque defines `x` con el mismo nombre que una `x` externa: dentro vale lo interno, fuera vuelve lo externo. No entenderlo lleva a 'por qué mi variable no cambió'.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `interno=<n+10> externo=<n>`
- **Regla:** externo x = n; en un bloque interno x = n+10; al salir, x = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `interno=15 externo=5` |
| `0` | `interno=10 externo=0` |
| `-3` | `interno=7 externo=-3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; x <- n
BLOQUE: x_interno <- x + 10 ; imprimir interno
imprimir externo (x sigue siendo n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
x = n
# Python no crea alcance de bloque: se usa otra variable para el 'interno'.
x_interno = x + 10
print(f"interno={x_interno} externo={x}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const x = n;
{
  const x = n + 10; // sombrea a la externa dentro del bloque
  console.log(`interno=${x} externo=${n}`);
}
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const x: number = n;
{
  const x: number = n + 10;
  console.log(`interno=${x} externo=${n}`);
}
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
        int x = n;
        {
            int xInterno = x + 10; // Java no permite re-declarar x en el bloque
            System.out.println("interno=" + xInterno + " externo=" + x);
        }
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int x = n;
{
    int xInterno = x + 10;
    Console.WriteLine($"interno={xInterno} externo={x}");
}
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
	x := n // externo
	interno := 0
	{
		x := x + 10 // sombrea a la externa en este bloque
		interno = x
	}
	fmt.Printf("interno=%d externo=%d\n", interno, x)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let x = n;
    {
        let x = n + 10; // sombreado idiomático en Rust
        println!("interno={x} externo={n}");
    }
    let _ = x;
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long x = n;
    {
        long x = n + 10; /* sombrea a la externa dentro del bloque */
        printf("interno=%ld externo=%ld\n", x, n);
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa alias/subconsultas para acotar nombres.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT printf('interno=%d externo=%d', n + 10, n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$x = $n;
// PHP no tiene alcance de bloque: se usa otra variable.
$xInterno = $x + 10;
echo "interno=$xInterno externo=$x\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bloques `{ }` (C/Java/JS/Rust) vs. indentación (Python). |
| Semántica | Rust permite `let` que sombrea; Python no tiene alcance de bloque para `if`/`for`. |
| Paradigmática | SQL usa alias/subconsultas para acotar nombres. |

## 🧬 El concepto en la familia

En Kotlin y Rust el sombreado con `val`/`let` es idiomático. En Python las variables de un `if` no crean un nuevo alcance.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 082
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que la interna cambió la externa** → causa: confundir sombreado con reasignación → solución: recordar que la interna es otra variable en su bloque
- **Usar una variable fuera de su alcance** → causa: error de 'no definida' → solución: declararla en el alcance donde la necesitas

## ❓ Preguntas frecuentes

- **¿Sombrear es mala práctica?** Puede confundir, pero en Rust/Kotlin es idiomático para transformar un valor manteniendo el nombre.
- **¿Python tiene alcance de bloque?** No para if/for; sí para funciones. Las variables 'se escapan' del bloque.

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

> [⏮️ Clase 081](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 083 ⏭️](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md)
