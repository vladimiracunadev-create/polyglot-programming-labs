# Clase 123 — Del código a la ejecución: fases de compilación

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver las **fases de compilación** en miniatura: separar la entrada en tokens (léxico), reconocer su estructura (sintáctico) y calcular el resultado (evaluación). Todo compilador o intérprete hace esto a mayor escala.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Separar una entrada en tokens.
2. Interpretar la estructura de una expresión.
3. Nombrar las fases de compilación.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Análisis léxico | De texto a tokens |
| 2 | Análisis sintáctico | Reconocer la estructura |
| 3 | Evaluación | Producir el resultado |

## 📖 Definiciones y características

- **Análisis léxico (lexer)** — divide el texto en tokens. Clave: '3 + 4' → [3, +, 4].
- **Análisis sintáctico (parser)** — reconoce la estructura de los tokens. Clave: expresión = número op número.
- **Evaluación** — calcula el resultado a partir de la estructura. Clave: aplica el operador.

## 🧩 Situación

Cuando compilas o ejecutas código, el lenguaje primero lo tokeniza, luego lo parsea y por fin lo evalúa o traduce. Este mini-evaluador muestra esas fases con una operación simple.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a op b` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** aplicar el operador a los dos operandos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 + 4` | `resultado=7` |
| `10 - 2` | `resultado=8` |
| `5 * 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
TOKENIZAR ; RECONOCER (num op num) ; EVALUAR
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, op, b = sys.stdin.readline().split()
a, b = int(a), int(b)
if op == "+":
    r = a + b
elif op == "-":
    r = a - b
else:
    r = a * b
print(f"resultado={r}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[0]), b = Long.parseLong(t[2]);
        long r = t[1].equals("+") ? a + b : t[1].equals("-") ? a - b : a * b;
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[0]), b = long.Parse(t[2]);
long r = t[1] switch { "+" => a + b, "-" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[0])
	b, _ := strconv.Atoi(t[2])
	var r int
	switch t[1] {
	case "+":
		r = a + b
	case "-":
		r = a - b
	default:
		r = a * b
	}
	fmt.Printf("resultado=%d\n", r)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[0].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[1] {
        "+" => a + b,
        "-" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    char op;
    if (scanf("%ld %c %ld", &a, &op, &b) != 3) return 1;
    long r = op == '+' ? a + b : op == '-' ? a - b : a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL evalúa la expresión según el operador con CASE.
WITH e(a, op, b) AS (VALUES (3, '+', 4))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN a + b WHEN '-' THEN a - b ELSE a * b END) AS resultado
FROM e;
```

### PHP · `php main.php`

```php
<?php
[$a, $op, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$r = $op === "+" ? $a + $b : ($op === "-" ? $a - $b : $a * $b);
echo "resultado=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Cada lenguaje tokeniza y evalúa a su manera. |
| Semántica | Las fases son universales: lexer, parser, evaluador. |
| Paradigmática | SQL evalúa expresiones en la consulta. |

## 🧬 El concepto en la familia

Todo compilador (gcc, javac, rustc) y todo intérprete (CPython, V8) sigue estas fases.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 123
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar léxico con sintaxis** → causa: confundir tokens con estructura → solución: separar las fases mentalmente
- **Operador no soportado** → causa: caso sin manejar → solución: cubrir los operadores esperados

## ❓ Preguntas frecuentes

- **¿Compilar es solo estas fases?** Son el núcleo; hay más (optimización, generación de código).
- **¿Un intérprete parsea?** Sí: también tokeniza y parsea antes de ejecutar.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 122](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 124 ⏭️](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md)
