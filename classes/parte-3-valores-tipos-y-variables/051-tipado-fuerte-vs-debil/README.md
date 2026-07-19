# Clase 051 — Tipado fuerte vs. débil

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **tipado fuerte** (no mezcla tipos sin permiso) de **débil** (convierte soluto). El mismo `+` puede sumar números o concatenar texto: verlo lado a lado aclara por qué `'5' + '5'` puede ser `10` o `'55'` según el lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar suma numérica de concatenación de texto.
2. Explicar tipado fuerte vs. débil con `+`.
3. Producir ambos resultados de forma explícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Suma vs. concatenación | El mismo símbolo, dos operaciones |
| 2 | Tipado fuerte | No convierte tipos sin que lo pidas |
| 3 | Tipado débil | Convierte automáticamente (a veces sorprende) |
| 4 | El operador + | Sobrecargado en muchos lenguajes |

## 📖 Definiciones y características

- **Tipado fuerte** — no permite operar entre tipos incompatibles sin conversión (Python, Java). Clave: menos sorpresas.
- **Tipado débil** — convierte tipos automáticamente para operar (PHP, JS). Clave: `'5'+5` puede dar cosas raras.
- **Concatenación** — unir dos cadenas. Clave: en muchos lenguajes también con `+`.
- **Sobrecarga de operador** — un operador con distinto significado según los tipos. Clave: `+` suma o concatena.

## 🧩 Situación

En JavaScript `'5' + 5` da `'55'` (concatena) y `'5' - 5` da `0` (resta). Esa es la marca del tipado débil. Verlo explícito evita bugs difíciles de rastrear.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `suma=<n+n> texto=<n concatenado consigo mismo>`
- **Regla:** suma = n + n ; texto = str(n) ++ str(n)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=10 texto=55` |
| `3` | `suma=6 texto=33` |
| `12` | `suma=24 texto=1212` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR "suma=" (n+n) " texto=" (TEXTO(n) ++ TEXTO(n))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"suma={n + n} texto={str(n) + str(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${n + n} texto=${String(n) + String(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${n + n} texto=${String(n) + String(n)}`);
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
        String t = Integer.toString(n) + Integer.toString(n);
        System.out.printf("suma=%d texto=%s%n", n + n, t);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={n + n} texto={n.ToString() + n.ToString()}");
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
	s := strconv.Itoa(n)
	fmt.Printf("suma=%d texto=%s%s\n", n+n, s, s)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} texto={}{}", n + n, n, n);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld texto=%ld%ld\n", n + n, n, n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL concatena con || (no con +).
WITH nums(n) AS (VALUES (5), (3), (12))
SELECT printf('suma=%d texto=%s', n + n, n || n) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
printf("suma=%d texto=%s\n", $n + $n, (string) $n . (string) $n);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `str(n)+str(n)` (Python) vs. `n + "" + n` (Java) vs. `$n.$n` (PHP). |
| Semántica | Python (fuerte) exige `str(n)` para concatenar; JS/PHP (débil) convierten solos. |
| Paradigmática | SQL usa `\|\|` para concatenar y `+` no existe para texto. |

## 🧬 El concepto en la familia

En Ruby (fuerte) `n.to_s + n.to_s`. En JS (débil) `n + '' + n` concatena por coerción. Haskell (muy fuerte) obliga `show n ++ show n`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 051
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que `n + n` concatene** → causa: confundir suma con concatenación → solución: convertir a texto explícitamente para concatenar
- **Confiar en la coerción débil** → causa: resultados inesperados con `+` → solución: convertir de forma explícita para que la intención sea clara

## ❓ Preguntas frecuentes

- **¿Por qué `'5'+5` es `'55'` en JS?** Tipado débil: ante texto y número, `+` concatena convirtiendo el número a texto.
- **¿Python es fuerte o débil?** Fuerte: `'5' + 5` es un error; hay que convertir explícitamente.

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

> [⏮️ Clase 050](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 052 ⏭️](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md)
