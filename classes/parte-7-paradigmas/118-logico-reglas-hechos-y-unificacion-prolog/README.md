# Clase 118 — Lógico: reglas, hechos y unificación (Prolog)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Asomarse al paradigma **lógico** (Prolog): en vez de calcular paso a paso, se declaran hechos y reglas y se consulta si algo se cumple. Aquí la regla `es_divisor(a, b)` es verdadera si a divide a b.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Expresar una relación como regla lógica.
2. Consultar si la relación se cumple.
3. Contrastar lógico con imperativo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Programación lógica | Hechos y reglas |
| 2 | Regla | Relación que se cumple o no |
| 3 | Consulta | Preguntar por la verdad de algo |

## 📖 Definiciones y características

- **Lógico** — paradigma en el que se declaran hechos y reglas y se consultan (Prolog). Clave: el motor deduce.
- **Regla** — relación condicional entre términos. Clave: `es_divisor(A,B) :- B mod A =:= 0`.
- **Consulta** — pregunta al sistema sobre si algo se cumple. Clave: devuelve verdadero/falso o soluciones.

## 🧩 Situación

En Prolog no dices cómo comprobar la divisibilidad: declaras la regla y preguntas `es_divisor(3, 12)`. El motor responde. Es el estilo de los sistemas expertos y el razonamiento.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros, a != 0)
- **Salida** (stdout): `divisor=<true|false>` (¿a divide a b?)
- **Regla:** divisor = (b mod a == 0)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 12` | `divisor=true` |
| `5 12` | `divisor=false` |
| `4 12` | `divisor=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
REGLA es_divisor(a,b) SI b mod a == 0 ; CONSULTAR es_divisor(a,b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
es_divisor = b % a == 0
print(f"divisor={'true' if es_divisor else 'false'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`divisor=${b % a === 0 ? "true" : "false"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`divisor=${b % a === 0 ? "true" : "false"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static boolean esDivisor(long a, long b) {
        return b % a == 0;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(p[0]);
        long b = Long.parseLong(p[1]);
        System.out.println("divisor=" + (esDivisor(a, b) ? "true" : "false"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(p[0]);
long b = long.Parse(p[1]);
Console.WriteLine($"divisor={(b % a == 0 ? "true" : "false")}");
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
	res := "false"
	if b%a == 0 {
		res = "true"
	}
	fmt.Printf("divisor=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let res = if v[1] % v[0] == 0 { "true" } else { "false" };
    println!("divisor={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("divisor=%s\n", b % a == 0 ? "true" : "false");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL (declarativo, primo del lógico): la condición como CASE.
WITH pares(a, b) AS (VALUES (3, 12), (5, 12), (4, 12))
SELECT printf('divisor=%s', CASE WHEN b % a = 0 THEN 'true' ELSE 'false' END) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "divisor=" . ((int) $b % (int) $a === 0 ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | En los del núcleo es un `if (b % a == 0)`; en Prolog, una regla. |
| Semántica | El lógico deduce; los imperativos comprueban. |
| Paradigmática | SQL (declarativo) es primo del lógico: describe condiciones. |

## 🧬 El concepto en la familia

En Prolog: `es_divisor(A, B) :- 0 is B mod A.` y la consulta `?- es_divisor(3, 12).`. Datalog es un subconjunto para datos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 118
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir lógico con imperativo** → causa: querer controlar el cómo → solución: declarar la relación y consultar
- **División por cero en la regla** → causa: a = 0 → solución: aquí a != 0

## ❓ Preguntas frecuentes

- **¿Dónde se usa Prolog?** IA simbólica, sistemas expertos, análisis de lenguaje, verificación.
- **¿SQL es lógico?** Es declarativo, primo cercano; describe condiciones sobre datos.

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

> [⏮️ Clase 117](../../parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 119 ⏭️](../../parte-7-paradigmas/119-orientado-a-eventos-y-callbacks/README.md)
