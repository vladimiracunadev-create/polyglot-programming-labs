# Clase 060 — Expresiones condicionales: ternario e if como expresión

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el **operador ternario** o el `if` como expresión: elegir un valor en una sola línea. En Rust y Kotlin el propio `if` devuelve valor; en C/Java/JS/PHP se usa `?:`.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Elegir un valor con el operador ternario.
2. Distinguir if-sentencia de if-expresión.
3. Escribir código conciso sin perder claridad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ternario ?: | Elegir un valor en una expresión |
| 2 | if como expresión | En Rust/Kotlin el if devuelve valor |
| 3 | Expresión vs. sentencia | Producir un valor vs. ejecutar una acción |
| 4 | Concisión | Una línea en vez de cuatro |

## 📖 Definiciones y características

- **Operador ternario** — `cond ? a : b`: elige a o b según la condición. Clave: expresión, no sentencia.
- **Expresión** — código que produce un valor. Clave: se puede asignar.
- **Sentencia** — código que ejecuta una acción. Clave: no siempre produce valor.
- **if-expresión** — un if que devuelve un valor (Rust, Kotlin). Clave: no necesita ternario aparte.

## 🧩 Situación

`max = a > b ? a : b` dice en una línea lo que un if/else diría en cuatro. Bien usado, el ternario es claro; abusado (anidado), se vuelve ilegible.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max = (a > b) ? a : b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
max <- SI a > b ENTONCES a SINO b
ESCRIBIR "max=" max
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
mx = a if a > b else b
print(f"max={mx}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx = a > b ? a : b;
console.log(`max=${mx}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx: number = a > b ? a : b;
console.log(`max=${mx}`);
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
        int mx = a > b ? a : b;
        System.out.println("max=" + mx);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
int mx = a > b ? a : b;
Console.WriteLine($"max={mx}");
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
	mx := b
	if a > b {
		mx = a
	}
	fmt.Printf("max=%d\n", mx)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mx = if v[0] > v[1] { v[0] } else { v[1] };
    println!("max={mx}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long mx = a > b ? a : b;
    printf("max=%ld\n", mx);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la función max() elige el mayor directamente.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$mx = $a > $b ? $a : $b;
echo "max=$mx\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a if a>b else b` (Python) vs. `a>b ? a : b` (C/Java/JS) vs. `if a>b {a} else {b}` (Rust). |
| Semántica | Python invierte el orden; Rust/Kotlin no tienen ternario porque el if ya es expresión. |
| Paradigmática | SQL usa `CASE WHEN` o `max(a,b)` directamente. |

## 🧬 El concepto en la familia

En Ruby `a > b ? a : b`. En Kotlin `if (a > b) a else b`, como Rust: el if es una expresión.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 060
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar ternarios en exceso** → causa: código ilegible → solución: usar if/else cuando hay más de dos ramas
- **Confundir el orden en Python** → causa: `a if cond else b` no es `cond ? a : b` → solución: recordar que la condición va en el medio en Python

## ❓ Preguntas frecuentes

- **¿Rust no tiene `?:`?** No: su `if` ya es una expresión que devuelve valor, así que no hace falta.
- **¿El ternario es más rápido?** No: es equivalente al if/else; es cuestión de concisión, no de velocidad.

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

> [⏮️ Clase 059](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 061 ⏭️](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md)
