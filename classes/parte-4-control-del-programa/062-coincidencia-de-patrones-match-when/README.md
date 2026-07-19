# Clase 062 — Coincidencia de patrones: match / when

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **coincidencia de patrones** (`match`/`when`) para decidir según la forma o el rango de un valor. Es más expresiva y segura que el switch clásico: obliga a cubrir todos los casos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar con match/when o su equivalente.
2. Usar guardas dentro de los patrones.
3. Explicar por qué el match exhaustivo es más seguro.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Coincidencia de patrones | Decidir por la forma del valor |
| 2 | Guardas en patrones | Condiciones dentro del caso |
| 3 | Exhaustividad | Cubrir todos los casos, obligatorio en Rust |
| 4 | match vs. switch | Más expresivo y sin caída |

## 📖 Definiciones y características

- **Coincidencia de patrones** — elegir una rama según la estructura o el rango de un valor. Clave: más potente que el switch.
- **Exhaustividad** — el compilador exige cubrir todos los casos (Rust). Clave: evita olvidos.
- **Guarda de patrón** — condición extra dentro de un caso (`n if n>0`). Clave: refina el patrón.
- **match** — construcción de coincidencia de patrones (Rust, Python 3.10+). Clave: sin fallthrough.

## 🧩 Situación

Clasificar el signo con `match` deja explícitos los tres casos (positivo, negativo, cero). En Rust, si olvidas uno, el programa no compila: la exhaustividad te protege.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `signo=<positivo|negativo|cero>`
- **Regla:** n>0→positivo; n<0→negativo; n==0→cero

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `signo=positivo` |
| `-3` | `signo=negativo` |
| `0` | `signo=cero` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
COINCIDIR n: (>0)->positivo ; (<0)->negativo ; (0)->cero
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
match n:
    case _ if n > 0:
        signo = "positivo"
    case _ if n < 0:
        signo = "negativo"
    case _:
        signo = "cero"
print(f"signo={signo}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo: string = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
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
        String signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
        System.out.println("signo=" + signo);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string signo = n switch {
    > 0 => "positivo",
    < 0 => "negativo",
    _ => "cero",
};
Console.WriteLine($"signo={signo}");
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
	var signo string
	switch {
	case n > 0:
		signo = "positivo"
	case n < 0:
		signo = "negativo"
	default:
		signo = "cero"
	}
	fmt.Printf("signo=%s\n", signo)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let signo = match n {
        n if n > 0 => "positivo",
        n if n < 0 => "negativo",
        _ => "cero",
    };
    println!("signo={signo}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
    printf("signo=%s\n", signo);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: coincidencia por rango con CASE WHEN.
WITH nums(n) AS (VALUES (5), (-3), (0))
SELECT printf('signo=%s',
       CASE WHEN n > 0 THEN 'positivo' WHEN n < 0 THEN 'negativo' ELSE 'cero' END) AS resultado
FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$signo = match (true) {
    $n > 0 => "positivo",
    $n < 0 => "negativo",
    default => "cero",
};
echo "signo=$signo\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `match` con guardas (Rust/Python) vs. if/else (C/Java) que no tienen match nativo clásico. |
| Semántica | Rust exige exhaustividad; C/Java no avisan si falta un caso. |
| Paradigmática | SQL expresa la clasificación con CASE WHEN. |

## 🧬 El concepto en la familia

En Kotlin `when { n > 0 -> ... }`. En Haskell se usan guardas: `signo n | n > 0 = ...`. Todos favorecen cubrir cada caso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 062
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar un caso sin cubrir** → causa: comportamiento indefinido o error → solución: en Rust el compilador obliga; en otros, añadir el caso por defecto
- **Usar == con reales para 'cero'** → causa: imprecisión del punto flotante → solución: aquí son enteros; con reales, comparar con tolerancia

## ❓ Preguntas frecuentes

- **¿match es solo de Rust?** No: Python 3.10+ tiene `match`, Kotlin `when`, Scala `match`, Haskell guardas/patrones.
- **¿Por qué es más seguro que switch?** Puede exigir exhaustividad y no tiene fallthrough accidental.

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

> [⏮️ Clase 061](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 063 ⏭️](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md)
