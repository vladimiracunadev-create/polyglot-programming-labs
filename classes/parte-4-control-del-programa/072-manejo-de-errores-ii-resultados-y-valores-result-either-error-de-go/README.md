# Clase 072 — Manejo de errores II: resultados y valores (Result/Either/error de Go)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Manejar errores con **valores** en vez de excepciones: `Result`/`Either` (Rust, Haskell), el par `(valor, error)` de Go, u `Option`. El error deja de ser un salto de flujo y pasa a ser un dato que se maneja explícitamente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar el error como un valor de retorno.
2. Manejar el resultado con match o comprobación.
3. Comparar excepciones con valores de error.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Errores como valores | El error es un dato, no un salto |
| 2 | Result / Either | Éxito o fallo tipado |
| 3 | El par (valor, error) de Go | Convención idiomática |
| 4 | Manejo explícito | No se puede ignorar por accidente |

## 📖 Definiciones y características

- **Result/Either** — tipo que contiene un valor de éxito o uno de error (Rust, Haskell). Clave: obliga a manejar ambos.
- **Valor de error** — devolver el error como dato en lugar de lanzarlo. Clave: flujo explícito.
- **Convención de Go** — devolver `(valor, error)` y comprobar `if err != nil`. Clave: errores visibles.
- **Manejo explícito** — el compilador o el estilo obligan a tratar el error. Clave: menos fallos silenciosos.

## 🧩 Situación

En Go y Rust el error no se lanza: se devuelve. `func div(a,b) (int, error)` obliga a comprobar `err` antes de usar el valor. El error se vuelve visible en la firma, no una sorpresa.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `ok=<a/b entera>` o `err=division` si b es 0
- **Regla:** si b != 0 → Ok(a/b); si b == 0 → Err(division)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `ok=5` |
| `7 0` | `err=division` |
| `8 4` | `ok=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
res <- dividir(a,b)  // devuelve Ok(v) o Err
SEGUN res: Ok(v)->"ok="v ; Err->"err=division"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def dividir(a, b):
    if b == 0:
        return (None, "division")
    return (a // b, None)


a, b = map(int, sys.stdin.readline().split())
valor, err = dividir(a, b)
if err is not None:
    print(f"err={err}")
else:
    print(f"ok={valor}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function dividir(a, b) {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log(r.err ? `err=${r.err}` : `ok=${r.ok}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

type Res = { ok: number } | { err: string };

function dividir(a: number, b: number): Res {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log("err" in r ? `err=${r.err}` : `ok=${r.ok}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    static Optional<Integer> dividir(int a, int b) {
        return b == 0 ? Optional.empty() : Optional.of(a / b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        Optional<Integer> r = dividir(a, b);
        System.out.println(r.isPresent() ? "ok=" + r.get() : "err=division");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

(int? ok, string err) Dividir(int a, int b) =>
    b == 0 ? (null, "division") : (a / b, null);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var (ok, err) = Dividir(a, b);
Console.WriteLine(err != null ? $"err={err}" : $"ok={ok}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func dividir(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("division")
	}
	return a / b, nil
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	res, err := dividir(a, b)
	if err != nil {
		fmt.Printf("err=%s\n", err)
	} else {
		fmt.Printf("ok=%d\n", res)
	}
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn dividir(a: i64, b: i64) -> Result<i64, String> {
    if b == 0 {
        Err("division".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    match dividir(v[0], v[1]) {
        Ok(r) => println!("ok={r}"),
        Err(e) => println!("err={e}"),
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C: se usa un valor de retorno para señalar el error (0 = ok, 1 = error). */
int dividir(long a, long b, long *out) {
    if (b == 0) return 1;
    *out = a / b;
    return 0;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    if (dividir(a, b, &r) != 0) {
        printf("err=division\n");
    } else {
        printf("ok=%ld\n", r);
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin tipo de error; se distingue el caso con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (8, 4))
SELECT CASE WHEN b = 0 THEN 'err=division'
            ELSE printf('ok=%d', a / b) END AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
function dividir($a, $b) {
    if ($b === 0) {
        return ["err" => "division"];
    }
    return ["ok" => intdiv($a, $b)];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = dividir((int) $a, (int) $b);
echo isset($r["err"]) ? "err={$r['err']}\n" : "ok={$r['ok']}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Result`/`match` (Rust) vs. `(v, err)` (Go) vs. if/else (otros). |
| Semántica | Rust/Go obligan a manejar el error; ignorarlo es visible o imposible. |
| Paradigmática | SQL usa CASE WHEN, sin tipo de error. |

## 🧬 El concepto en la familia

En Haskell `Either String Int` con `case`. En Kotlin, un `sealed class` o `Result`. Es el estilo opuesto a las excepciones de la clase anterior.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 072
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el error devuelto** → causa: usar un valor inválido → solución: comprobar siempre el error antes del valor (Go) o usar match (Rust)
- **Mezclar excepciones y valores sin criterio** → causa: manejo de errores inconsistente → solución: elegir un estilo por proyecto y ser coherente

## ❓ Preguntas frecuentes

- **¿Result o excepciones?** Result para errores esperables y explícitos; excepciones para lo verdaderamente excepcional.
- **¿Por qué Go no tiene excepciones?** Prefiere errores como valores para que el manejo sea explícito y visible.

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

> [⏮️ Clase 071](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 073 ⏭️](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md)
