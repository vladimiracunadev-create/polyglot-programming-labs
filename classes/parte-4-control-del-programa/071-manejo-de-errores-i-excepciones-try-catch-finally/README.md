# Clase 071 — Manejo de errores I: excepciones (try/catch/finally)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Manejar errores con **excepciones** (`try`/`catch`/`finally`): separar el camino feliz del manejo del error. Dividir por cero es el caso clásico que dispara una excepción en varios lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Capturar una excepción con try/catch.
2. Distinguir el flujo normal del de error.
3. Reconocer qué lenguajes lanzan y cuáles no.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Excepción | Un error que interrumpe el flujo |
| 2 | try/catch | Intentar y capturar el fallo |
| 3 | finally | Código que corre pase lo que pase |
| 4 | Lanzar vs. comprobar | No todos lanzan en /0 |

## 📖 Definiciones y características

- **Excepción** — objeto que representa un error y desvía el flujo. Clave: se captura con try/catch.
- **try** — bloque que puede fallar. Clave: envuelve la operación arriesgada.
- **catch** — bloque que maneja la excepción. Clave: el plan B ante el error.
- **finally** — bloque que se ejecuta siempre (haya error o no). Clave: liberar recursos.

## 🧩 Situación

Dividir entre cero es un error clásico. En Java, C#, Python y PHP la división entera por cero lanza una excepción; capturarla evita que el programa termine abruptamente.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `resultado=<a/b entera>` o `error=division por cero` si b es 0
- **Regla:** si b != 0 → a/b (entera); si b == 0 → mensaje de error

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `resultado=5` |
| `7 0` | `error=division por cero` |
| `9 3` | `resultado=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
INTENTAR: r <- a/b ; ESCRIBIR "resultado=" r
CAPTURAR division_por_cero: ESCRIBIR "error=division por cero"
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
try:
    r = a // b
    print(f"resultado={r}")
except ZeroDivisionError:
    print("error=division por cero")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
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
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        try {
            int r = a / b;
            System.out.println("resultado=" + r);
        } catch (ArithmeticException e) {
            System.out.println("error=division por cero");
        }
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
try {
    int r = a / b;
    Console.WriteLine($"resultado={r}");
} catch (DivideByZeroException) {
    Console.WriteLine("error=division por cero");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	// Go no usa excepciones: comprueba antes de dividir.
	if b == 0 {
		fmt.Println("error=division por cero")
	} else {
		fmt.Printf("resultado=%d\n", a/b)
	}
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0], v[1]);
    // Rust no usa excepciones: checked_div devuelve Option.
    match a.checked_div(b) {
        Some(r) => println!("resultado={r}"),
        None => println!("error=division por cero"),
    }
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene excepciones: comprobar antes de dividir. */
    if (b == 0) {
        printf("error=division por cero\n");
    } else {
        printf("resultado=%ld\n", a / b);
    }
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: evita el error comprobando el divisor con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (9, 3))
SELECT CASE WHEN b = 0 THEN 'error=division por cero'
            ELSE printf('resultado=%d', a / b) END AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
try {
    $r = intdiv($a, $b);
    echo "resultado=$r\n";
} catch (DivisionByZeroError $e) {
    echo "error=division por cero\n";
}
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `try/except` (Python), `try/catch` (Java/C#/JS/PHP). |
| Semántica | Java/C#/Python/PHP lanzan en /0 entero; JS da Infinity (hay que comprobar); Go/Rust no usan excepciones. |
| Paradigmática | SQL evita el error con CASE WHEN b=0. |

## 🧬 El concepto en la familia

En Ruby `begin/rescue/ensure`. En Kotlin `try/catch/finally`, como Java. Go y Rust prefieren valores de error (siguiente clase).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 071
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capturar todo con un catch vacío** → causa: ocultar errores reales → solución: capturar solo lo esperado y actuar
- **Asumir que /0 siempre lanza** → causa: en JS da Infinity, no excepción → solución: comprobar el divisor o el resultado según el lenguaje

## ❓ Preguntas frecuentes

- **¿Excepciones o valores de error?** Excepciones para lo excepcional; valores (Result) para errores esperables. La siguiente clase compara.
- **¿Para qué el finally?** Para liberar recursos (archivos, conexiones) ocurra o no un error.

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

> [⏮️ Clase 070](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 072 ⏭️](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md)
