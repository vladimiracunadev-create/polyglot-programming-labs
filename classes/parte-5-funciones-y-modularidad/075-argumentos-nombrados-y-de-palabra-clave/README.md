# Clase 075 — Argumentos nombrados y de palabra clave

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **argumentos nombrados** (por palabra clave): pasar los valores indicando a qué parámetro corresponden, mejorando la legibilidad y permitiendo cualquier orden. No todos los lenguajes los tienen.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Pasar argumentos por nombre.
2. Explicar la ventaja de legibilidad y orden libre.
3. Reconocer lenguajes sin argumentos nombrados.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Argumento nombrado | Se indica el parámetro por su nombre |
| 2 | Orden libre | No depende de la posición |
| 3 | Legibilidad | Queda claro qué es cada valor |
| 4 | Soporte por lenguaje | Python/C# sí; Java/Go no |

## 📖 Definiciones y características

- **Argumento nombrado** — se pasa indicando el parámetro (`y=4`). Clave: claridad y orden libre.
- **Argumento posicional** — se pasa por su posición. Clave: depende del orden.
- **Palabra clave** — el nombre del parámetro usado al llamar (Python `**kwargs`). Clave: base de los nombrados.
- **Legibilidad de la llamada** — entender qué es cada valor sin ver la firma. Clave: menos errores.

## 🧩 Situación

`crear(ancho=800, alto=600)` se lee mejor que `crear(800, 600)`: nadie se pregunta cuál es cuál. Los argumentos nombrados evitan confundir el orden de parámetros parecidos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros: x, y)
- **Salida** (stdout): `punto(x=<a>, y=<b>)`
- **Regla:** punto(x=a, y=b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `punto(x=3, y=4)` |
| `0 -2` | `punto(x=0, y=-2)` |
| `5 5` | `punto(x=5, y=5)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR punto(x=a, y=b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def punto(x, y):
    return f"punto(x={x}, y={y})"


a, b = map(int, sys.stdin.readline().split())
print(punto(x=a, y=b))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// JS simula argumentos nombrados con un objeto.
function punto({ x, y }) {
  return `punto(x=${x}, y=${y})`;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function punto({ x, y }: { x: number; y: number }): string {
  return `punto(x=${x}, y=${y})`;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene argumentos nombrados: se pasan por posición.
    static String punto(int x, int y) {
        return "punto(x=" + x + ", y=" + y + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println(punto(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string Punto(int x, int y) => $"punto(x={x}, y={y})";

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine(Punto(x: int.Parse(p[0]), y: int.Parse(p[1])));
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

// Go no tiene argumentos nombrados: se usan structs con campos nombrados.
type Punto struct {
	X, Y int
}

func (p Punto) String() string {
	return fmt.Sprintf("punto(x=%d, y=%d)", p.X, p.Y)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Println(Punto{X: a, Y: b})
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn punto(x: i64, y: i64) -> String {
    format!("punto(x={x}, y={y})")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("{}", punto(v[0], v[1]));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene argumentos nombrados: posicionales. */
    printf("punto(x=%ld, y=%ld)\n", a, b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL nombra columnas, análogo a nombrar argumentos.
WITH puntos(x, y) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('punto(x=%d, y=%d)', x, y) AS resultado FROM puntos;
```

### PHP · `php main.php`

```php
<?php
function punto($x, $y) {
    return "punto(x=$x, y=$y)";
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
// PHP 8 admite argumentos nombrados.
echo punto(x: (int) $a, y: (int) $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `punto(x=a, y=b)` (Python/C#) vs. posicional (Java/Go/C). |
| Semántica | Con nombres el orden es libre; sin ellos, importa la posición. |
| Paradigmática | SQL nombra las columnas, algo análogo a nombrar argumentos. |

## 🧬 El concepto en la familia

En Ruby con argumentos de palabra clave: `punto(x: a, y: b)`. Kotlin permite `punto(x = a, y = b)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 075
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en el orden con parámetros parecidos** → causa: intercambiar x e y → solución: usar argumentos nombrados donde el lenguaje los ofrezca
- **Asumir nombres en Java/Go** → causa: no existen → solución: documentar bien o usar objetos/structs con campos nombrados

## ❓ Preguntas frecuentes

- **¿Qué lenguajes tienen nombrados?** Python, C#, Kotlin, Ruby, Swift. Java y Go no de forma nativa.
- **¿Y si no los hay?** Se usan structs/objetos con campos nombrados para lograr claridad.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 074](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 076 ⏭️](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md)
