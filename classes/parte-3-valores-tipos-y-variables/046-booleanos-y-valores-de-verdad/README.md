# Clase 046 — Booleanos y valores de verdad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Dominar el álgebra booleana básica: **AND** (ambos), **OR** (alguno) y **NOT** (negación). Es la base de toda condición y decisión. Cada lenguaje representa e imprime los booleanos de forma propia (`true`/`True`), lo que obliga a normalizar la salida.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular AND, OR y NOT sobre valores booleanos.
2. Construir un booleano a partir de una entrada (0/1).
3. Normalizar la impresión de booleanos entre lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AND, OR, NOT | Las tres operaciones lógicas fundamentales |
| 2 | Representar la verdad | 0/1, true/false, según el lenguaje |
| 3 | Impresión de booleanos | true vs. True: hay que normalizar |
| 4 | Base de las condiciones | Todo if depende de un booleano |

## 📖 Definiciones y características

- **Booleano** — valor de verdad: verdadero o falso. Clave: resultado de comparaciones y condiciones.
- **AND (∧)** — verdadero solo si ambos lo son. Clave: conjunción.
- **OR (∨)** — verdadero si al menos uno lo es. Clave: disyunción.
- **NOT (¬)** — invierte el valor de verdad. Clave: negación.

## 🧩 Situación

"Si es fin de semana Y no llueve, salgo": toda decisión combina booleanos con AND/OR/NOT. Verlos aislados, con su tabla de verdad, prepara para las condiciones de la Parte 4.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (cada uno 0 o 1)
- **Salida** (stdout): `and=<true|false> or=<true|false> not_a=<true|false>`
- **Regla:** and = a ∧ b ; or = a ∨ b ; not_a = ¬a (con a,b interpretados como booleanos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 0` | `and=false or=true not_a=false` |
| `1 1` | `and=true or=true not_a=false` |
| `0 0` | `and=false or=false not_a=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ba <- (a != 0) ; bb <- (b != 0)
ESCRIBIR "and=" (ba Y bb) " or=" (ba O bb) " not_a=" (NO ba)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
ba, bb = a != 0, b != 0
tf = lambda x: "true" if x else "false"
print(f"and={tf(ba and bb)} or={tf(ba or bb)} not_a={tf(not ba)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [ai, bi] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a = ai !== 0;
const b = bi !== 0;
const tf = (x) => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [ai, bi]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a: boolean = ai !== 0;
const b: boolean = bi !== 0;
const tf = (x: boolean): string => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean a = Integer.parseInt(p[0]) != 0;
        boolean b = Integer.parseInt(p[1]) != 0;
        System.out.printf("and=%s or=%s not_a=%s%n", tf(a && b), tf(a || b), tf(!a));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
bool a = int.Parse(p[0]) != 0;
bool b = int.Parse(p[1]) != 0;
string Tf(bool x) => x ? "true" : "false";
Console.WriteLine($"and={Tf(a && b)} or={Tf(a || b)} not_a={Tf(!a)}");
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

func tf(x bool) string {
	if x {
		return "true"
	}
	return "false"
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	ai, _ := strconv.Atoi(f[0])
	bi, _ := strconv.Atoi(f[1])
	a, b := ai != 0, bi != 0
	fmt.Printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0] != 0, v[1] != 0);
    println!("and={} or={} not_a={}", tf(a && b), tf(a || b), tf(!a));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 1;
    a = a != 0;
    b = b != 0;
    printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene tipo booleano nativo: se expresa con CASE WHEN.
WITH pares(a, b) AS (VALUES (1, 0), (1, 1), (0, 0))
SELECT printf('and=%s or=%s not_a=%s',
       CASE WHEN a <> 0 AND b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN a <> 0 OR b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN NOT (a <> 0) THEN 'true' ELSE 'false' END) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = ((int) $a) !== 0;
$b = ((int) $b) !== 0;
$tf = fn($x) => $x ? "true" : "false";
printf("and=%s or=%s not_a=%s\n", $tf($a && $b), $tf($a || $b), $tf(!$a));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `and/or/not` (Python) vs. `&&/\|\|/!` (C/Java/JS/Go/Rust/PHP). |
| Semántica | C# imprime `True`/`False`; C no tiene tipo bool nativo hasta C99; se normaliza a minúsculas. |
| Paradigmática | SQL usa `CASE WHEN a<>0 AND b<>0 ...` en vez de un tipo booleano nativo. |

## 🧬 El concepto en la familia

En Ruby `a && b`, y `true`/`false` en minúscula por defecto. En Haskell son `&&`, `||`, `not`, con el tipo `Bool` explícito y valores `True`/`False`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 046
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True`/`False`** → causa: usar el formato por defecto de C#/Python → solución: normalizar a minúsculas con un ayudante `tf`
- **Confundir cortocircuito con bit a bit** → causa: usar `&`/`|` en vez de `&&`/`||` → solución: usar los operadores lógicos, no los de bits

## ❓ Preguntas frecuentes

- **¿`&&` y `&` son lo mismo?** No: `&&` es lógico con cortocircuito; `&` es bit a bit. Para booleanos, usa `&&`.
- **¿Qué es el cortocircuito?** En `a && b`, si `a` es falso no se evalúa `b`. Importa cuando `b` tiene efectos.

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

> [⏮️ Clase 045](../../parte-3-valores-tipos-y-variables/045-numeros-reales-punto-flotante-precision-y-decimales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 047 ⏭️](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md)
