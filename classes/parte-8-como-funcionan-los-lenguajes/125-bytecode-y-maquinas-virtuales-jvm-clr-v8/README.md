# Clase 125 — Bytecode y máquinas virtuales (JVM, CLR, V8)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **bytecode y las máquinas virtuales**: una VM ejecuta instրucciones simples sobre una pila. La notación polaca inversa (RPN) es exactamente cómo trabaja una VM de pila: apila operandos y aplica operadores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Evaluar RPN con una pila.
2. Relacionar RPN con las VM de pila.
3. Explicar qué es el bytecode.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Máquina de pila | Opera sobre una pila de valores |
| 2 | RPN | Operandos primero, operador después |
| 3 | Bytecode | Instrucciones simples para la VM |

## 📖 Definiciones y características

- **Bytecode** — código intermedio de instrucciones simples que ejecuta una VM. Clave: portable (JVM, CLR).
- **Máquina virtual de pila** — VM que opera apilando y desapilando valores. Clave: `push 3, push 4, add`.
- **RPN** — notación donde el operador va tras los operandos. Clave: `3 4 +` = 7.

## 🧩 Situación

La JVM y el CLR ejecutan bytecode sobre una pila: apilan operandos y aplican operadores. Evaluar '3 4 +' con una pila reproduce ese mecanismo en pequeño.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b op` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** apilar a y b; aplicar op; el tope es el resultado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 +` | `resultado=7` |
| `5 6 *` | `resultado=30` |
| `10 2 -` | `resultado=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA cada token: SI número, apilar; SI operador, desapilar 2, aplicar, apilar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b, op = sys.stdin.readline().split()
pila = [int(a), int(b)]
y = pila.pop()
x = pila.pop()
r = x + y if op == "+" else x - y if op == "-" else x * y
print(f"resultado={r}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila = [Number(a), Number(b)];
const y = pila.pop(), x = pila.pop();
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila: number[] = [Number(a), Number(b)];
const y = pila.pop()!, x = pila.pop()!;
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Deque<Long> pila = new ArrayDeque<>();
        pila.push(Long.parseLong(t[0]));
        pila.push(Long.parseLong(t[1]));
        long y = pila.pop(), x = pila.pop();
        long r = t[2].equals("+") ? x + y : t[2].equals("-") ? x - y : x * y;
        System.out.println("resultado=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pila = new Stack<long>();
pila.Push(long.Parse(t[0]));
pila.Push(long.Parse(t[1]));
long y = pila.Pop(), x = pila.Pop();
long r = t[2] switch { "+" => x + y, "-" => x - y, _ => x * y };
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
	x, _ := strconv.Atoi(t[0])
	y, _ := strconv.Atoi(t[1])
	var r int
	switch t[2] {
	case "+":
		r = x + y
	case "-":
		r = x - y
	default:
		r = x * y
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
    let mut pila: Vec<i64> = vec![t[0].parse().unwrap(), t[1].parse().unwrap()];
    let y = pila.pop().unwrap();
    let x = pila.pop().unwrap();
    let r = match t[2] {
        "+" => x + y,
        "-" => x - y,
        _ => x * y,
    };
    println!("resultado={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x, y;
    char op;
    if (scanf("%ld %ld %c", &x, &y, &op) != 3) return 1;
    long r = op == '+' ? x + y : op == '-' ? x - y : x * y;
    printf("resultado=%ld\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin pila explícita; evalúa la expresión.
WITH e(x, y, op) AS (VALUES (3, 4, '+'))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN x + y WHEN '-' THEN x - y ELSE x * y END) AS resultado
FROM e;
```

### PHP · `php main.php`

```php
<?php
[$a, $b, $op] = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = [(int) $a, (int) $b];
$y = array_pop($pila);
$x = array_pop($pila);
$r = $op === "+" ? $x + $y : ($op === "-" ? $x - $y : $x * $y);
echo "resultado=$r\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Una pila (lista) en cada lenguaje. |
| Semántica | La VM de pila es el mismo modelo que la JVM/CLR. |
| Paradigmática | SQL no tiene pila explícita; evalúa la expresión. |

## 🧬 El concepto en la familia

La JVM (bytecode Java) y el CLR (.NET) son máquinas de pila. Python también usa una VM de pila.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 125
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desapilar en orden equivocado** → causa: resta/división invertidas → solución: el primero desapilado es el segundo operando
- **Pila vacía al operar** → causa: expresión mal formada → solución: asumir RPN bien formada

## ❓ Preguntas frecuentes

- **¿Por qué VM de pila?** Simplicidad y portabilidad: las instrucciones no nombran registros.
- **¿RPN se usa de verdad?** Sí: calculadoras HP, PostScript y muchas VM internamente.

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

> [⏮️ Clase 124](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 126 ⏭️](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md)
