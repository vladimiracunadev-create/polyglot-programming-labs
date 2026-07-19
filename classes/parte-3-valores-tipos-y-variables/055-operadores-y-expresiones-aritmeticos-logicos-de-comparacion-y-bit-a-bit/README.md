# Clase 055 — Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una expresión como `a + b * c` esconde más decisiones de las que parece. ¿Se multiplica antes de sumar? ¿En qué orden se evalúan `a`, `b` y `c`? ¿Qué pasa si `b` es una llamada con efecto colateral? Los operadores son los ladrillos de toda expresión, y las reglas que los gobiernan —precedencia, asociatividad, orden de evaluación— deciden qué calcula realmente tu código. Sebesta dedica un capítulo entero a esto porque es una fuente sorprendentemente rica de errores sutiles y de diferencias entre lenguajes.

El ejercicio de esta clase se centra en los **cinco aritméticos** (`+ - * / %`) sobre dos enteros positivos, porque ahí vive la trampa más famosa: la división entera y el módulo. `7 / 2` da `3`, no `3.5`, cuando ambos operandos son enteros en C, Java o Go; Python separa esa operación en `//` (entera) y `/` (real) para evitar la ambigüedad. Y el módulo con negativos es un campo minado: `-7 % 3` da `2` en Python (signo del divisor) pero `-1` en C y Java (signo del dividendo). Por eso el contrato usa solo positivos: para que las diez implementaciones coincidan y la diferencia quede como advertencia, no como fallo del verificador.

Aunque el código sea aritmético, el título abarca las otras tres familias que conviene tener presentes: los **de comparación** (`==`, `<`, `>=`), los **lógicos** con evaluación en cortocircuito (`&&`, `||`, que dejan de evaluar en cuanto el resultado está decidido, como analiza Scott) y los **bit a bit** (`&`, `|`, `^`, `<<`, `>>`), que operan sobre la representación binaria. Todos comparten el mismo esqueleto de reglas —precedencia y asociatividad— y todos pueden esconder efectos colaterales cuando un operando modifica estado al evaluarse.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Aplicar los cinco operadores aritméticos básicos.
2. Distinguir división entera de división real.
3. Reconocer que el módulo con negativos varía entre lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Operadores aritméticos | +, -, *, / y % |
| 2 | División entera | Descarta la parte decimal |
| 3 | Módulo (resto) | Lo que sobra de la división |
| 4 | Precedencia | El orden en que se evalúan |

## 📖 Definiciones y características

- **Operador** — símbolo que combina valores para producir otro (+, *, %). Clave: bloque de las expresiones.
- **División entera** — cociente sin decimales. Clave: `7/2 = 3`, no 3.5.
- **Módulo** — resto de la división entera. Clave: `7 % 2 = 1`.
- **Precedencia** — el orden de evaluación (`*` antes que `+`). Clave: los paréntesis mandan.

## 🧩 Situación

Repartir 7 caramelos entre 2 niños: cada uno recibe 3 (división entera) y sobra 1 (módulo). Estos operadores están en todo cálculo; sus reglas con negativos son una trampa clásica entre lenguajes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros positivos, b != 0)
- **Salida** (stdout): `suma=<a+b> resta=<a-b> mult=<a*b> div=<a/b entera> mod=<a%b>`
- **Regla:** las cinco operaciones aritméticas sobre a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 3` | `suma=13 resta=7 mult=30 div=3 mod=1` |
| `20 4` | `suma=24 resta=16 mult=80 div=5 mod=0` |
| `7 2` | `suma=9 resta=5 mult=14 div=3 mod=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR suma, resta, mult, división entera y módulo
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"suma={a + b} resta={a - b} mult={a * b} div={a // b} mod={a % b}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${a + b} resta=${a - b} mult=${a * b} div=${Math.trunc(a / b)} mod=${a % b}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${a + b} resta=${a - b} mult=${a * b} div=${Math.trunc(a / b)} mod=${a % b}`);
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
        System.out.printf("suma=%d resta=%d mult=%d div=%d mod=%d%n", a + b, a - b, a * b, a / b, a % b);
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
Console.WriteLine($"suma={a + b} resta={a - b} mult={a * b} div={a / b} mod={a % b}");
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
	fmt.Printf("suma=%d resta=%d mult=%d div=%d mod=%d\n", a+b, a-b, a*b, a/b, a%b)
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
    println!("suma={} resta={} mult={} div={} mod={}", a + b, a - b, a * b, a / b, a % b);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld resta=%ld mult=%ld div=%ld mod=%ld\n", a + b, a - b, a * b, a / b, a % b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL evalúa las operaciones aritméticas en la consulta (/ entre enteros es división entera).
WITH pares(a, b) AS (VALUES (10, 3), (20, 4), (7, 2))
SELECT printf('suma=%d resta=%d mult=%d div=%d mod=%d', a + b, a - b, a * b, a / b, a % b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
printf("suma=%d resta=%d mult=%d div=%d mod=%d\n", $a + $b, $a - $b, $a * $b, intdiv($a, $b), $a % $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `//` (Python) vs. `/` entre enteros (C/Java/Go); `%` en casi todos. |
| Semántica | Con negativos, el módulo difiere: Python da signo del divisor; C/Java, del dividendo. |
| Paradigmática | SQL evalúa la expresión aritmética en la propia consulta. |

## 🧬 El concepto en la familia

En Ruby `a / b` es entero si ambos lo son, como C. En Haskell `div` y `mod` (y `quot`/`rem` con otra regla de signo).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 055
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar decimales de `/` entre enteros** → causa: en C/Java la división de enteros trunca → solución: usar reales si quieres decimales, o `//` en Python
- **Asumir el mismo módulo con negativos** → causa: Python y C difieren en el signo del resto → solución: usar entradas positivas o conocer la regla de cada lenguaje

## ❓ Preguntas frecuentes

- **¿`7/2` es 3 o 3.5?** Entre enteros, 3 (división entera). Con un real, 3.5.
- **¿Por qué el módulo varía con negativos?** Cada lenguaje elige el signo del resto; por eso aquí usamos positivos.

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

> [⏮️ Clase 054](../../parte-3-valores-tipos-y-variables/054-mutabilidad-e-inmutabilidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 056 ⏭️](../../parte-3-valores-tipos-y-variables/056-entrada-y-salida-basica-leer-y-escribir/README.md)
