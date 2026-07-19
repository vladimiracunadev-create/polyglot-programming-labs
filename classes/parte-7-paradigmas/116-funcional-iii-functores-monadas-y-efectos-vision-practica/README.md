# Clase 116 — Funcional III: functores, mónadas y efectos (visión práctica)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (III)**: functores y mónadas en su forma práctica. `Option`/`Maybe` envuelve 'hay valor' o 'no hay', y `map` aplica una función solo si hay valor, sin comprobaciones dispersas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Envolver un valor opcional.
2. Aplicar map sobre Option (functor).
3. Explicar la ventaja frente a null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Option/Maybe | Contenedor de 'quizá hay valor' |
| 2 | map sobre contenedor | Aplicar sin desenvolver |
| 3 | Functor | Algo sobre lo que se puede mapear |

## 📖 Definiciones y características

- **Functor** — contenedor sobre el que se puede aplicar `map` (Option, listas). Clave: transformar el contenido sin sacarlo.
- **Option/Maybe** — envuelve un valor presente (Some) o ausente (None). Clave: ausencia explícita y segura.
- **map sobre Option** — aplica la función si hay valor; si no, propaga la ausencia. Clave: sin ifs dispersos.

## 🧩 Situación

En vez de `if (x != null) usar(x)` por todas partes, `option.map(usar)` aplica la función solo si hay valor y propaga la ausencia. Menos ruido, menos errores de null.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>` si n>0 (hay valor), o `resultado=nada` si no
- **Regla:** Option(n si n>0).map(x → 2x)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=nada` |
| `-3` | `resultado=nada` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
opcion <- Some(n) SI n>0 SINO None ; ESCRIBIR opcion.map(x->2x) o 'nada'
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
opcion = n if n > 0 else None
if opcion is not None:
    print(f"resultado={opcion * 2}")
else:
    print("resultado=nada")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const opcion = n > 0 ? n : null;
console.log(opcion !== null ? `resultado=${opcion * 2}` : "resultado=nada");
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const opcion: number | null = n > 0 ? n : null;
console.log(opcion !== null ? `resultado=${opcion * 2}` : "resultado=nada");
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Optional<Integer> opcion = n > 0 ? Optional.of(n) : Optional.empty();
        Optional<Integer> r = opcion.map(x -> x * 2);
        System.out.println(r.map(x -> "resultado=" + x).orElse("resultado=nada"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int? opcion = n > 0 ? n : (int?) null;
int? r = opcion.HasValue ? opcion.Value * 2 : (int?) null;
Console.WriteLine(r.HasValue ? $"resultado={r.Value}" : "resultado=nada");
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
	if n > 0 {
		fmt.Printf("resultado=%d\n", n*2)
	} else {
		fmt.Println("resultado=nada")
	}
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let opcion: Option<i64> = if n > 0 { Some(n) } else { None };
    match opcion.map(|x| x * 2) {
        Some(r) => println!("resultado={r}"),
        None => println!("resultado=nada"),
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n > 0) {
        printf("resultado=%ld\n", n * 2);
    } else {
        printf("resultado=nada\n");
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL propaga NULL por las operaciones automáticamente.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT CASE WHEN n > 0 THEN printf('resultado=%d', n * 2) ELSE 'resultado=nada' END AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$opcion = $n > 0 ? $n : null;
echo $opcion !== null ? "resultado=" . ($opcion * 2) . "\n" : "resultado=nada\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Option`/`map` (Rust), `Optional` (Java), if/else (otros). |
| Semántica | El functor evita comprobar la ausencia en cada paso. |
| Paradigmática | SQL propaga NULL automáticamente por las operaciones. |

## 🧬 El concepto en la familia

En Haskell `fmap (*2) (Just n)`. En Kotlin, `?.let { it * 2 }` sobre un tipo nullable.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 116
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desenvolver sin comprobar** → causa: usar un valor ausente → solución: usar map/flatMap en vez de extraer a la fuerza
- **Confundir functor con mónada** → causa: map vs. flatMap → solución: map transforma; flatMap encadena operaciones que devuelven Option

## ❓ Preguntas frecuentes

- **¿Functor o mónada?** Functor solo mapea; la mónada además encadena (flatMap). Aquí basta map.
- **¿Por qué mejor que null?** El tipo obliga a considerar la ausencia; el null se cuela silenciosamente.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 115](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 117 ⏭️](../../parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md)
