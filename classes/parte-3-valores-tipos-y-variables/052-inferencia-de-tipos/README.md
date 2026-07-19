# Clase 052 — Inferencia de tipos

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la **inferencia de tipos**: el compilador deduce el tipo sin que lo anotes. Un producto de dos enteros basta para comparar `x = a*b` (Python), `var`/`:=` (C#/Go), `let` (Rust) frente a la anotación explícita de Java o C.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer dónde el lenguaje infiere el tipo.
2. Comparar inferencia con anotación explícita.
3. Escribir el mismo cálculo con y sin anotar tipos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inferencia | El compilador deduce el tipo del valor |
| 2 | Anotación explícita | El programador escribe el tipo |
| 3 | var/:=/let | Palabras de inferencia por lenguaje |
| 4 | Inferencia no es dinámico | El tipo sigue siendo fijo, solo no se escribe |

## 📖 Definiciones y características

- **Inferencia de tipos** — el compilador deduce el tipo a partir del valor. Clave: menos ruido, mismo tipado estático.
- **Anotación de tipo** — escribir el tipo explícitamente (`int x`). Clave: obligatoria donde no hay inferencia.
- **var / := / let** — formas de declarar con inferencia (C#, Go, Rust). Clave: el tipo se fija igual.
- **Estático con inferencia** — tipos fijos que no hace falta anotar. Clave: no confundir con dinámico.

## 🧩 Situación

`var total = a * b;` en C# infiere que `total` es entero. No es tipado dinámico: el tipo es fijo, solo no lo escribiste. Distinguir inferencia de dinamismo evita malentendidos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `producto=<a*b>`
- **Regla:** producto = a * b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `producto=12` |
| `0 9` | `producto=0` |
| `-2 5` | `producto=-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "producto=" (a*b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"producto={a * b}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`producto=${a * b}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`producto=${a * b}`);
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
        System.out.println("producto=" + (a * b));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var a = int.Parse(p[0]);
var b = int.Parse(p[1]);
Console.WriteLine($"producto={a * b}");
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
	producto := a * b
	fmt.Printf("producto=%d\n", producto)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let producto = v[0] * v[1];
    println!("producto={producto}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("producto=%ld\n", a * b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la expresión produce el valor sin declarar variables.
WITH pares(a, b) AS (VALUES (3, 4), (0, 9), (-2, 5))
SELECT printf('producto=%d', a * b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$producto = (int) $a * (int) $b;
printf("producto=%d\n", $producto);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `p = a*b` (Python), `p := a*b` (Go), `let p = a*b` (Rust), `int p = a*b` (Java/C). |
| Semántica | En Go/Rust/C# el tipo se infiere pero es fijo; en Java/C se anota. |
| Paradigmática | SQL no declara variables: la expresión produce el valor. |

## 🧬 El concepto en la familia

En Kotlin `val p = a * b` infiere. En C++ `auto p = a * b`. En Haskell la inferencia (Hindley-Milner) es total: casi nunca anotas tipos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 052
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que inferencia = dinámico** → causa: confundir no-anotar con no-tipar → solución: recordar que el tipo inferido es fijo y se comprueba
- **No anotar donde hace falta** → causa: Java/C exigen el tipo → solución: anotar cuando el lenguaje no infiere

## ❓ Preguntas frecuentes

- **¿La inferencia hace el código más lento?** No: ocurre en compilación; el binario es idéntico al anotado.
- **¿Siempre puede inferir?** No siempre; a veces el tipo es ambiguo y hay que anotar.

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

> [⏮️ Clase 051](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 053 ⏭️](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md)
