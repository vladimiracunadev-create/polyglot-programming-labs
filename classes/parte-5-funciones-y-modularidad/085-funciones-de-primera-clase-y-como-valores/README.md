# Clase 085 — Funciones de primera clase y como valores

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Tratar las funciones como **valores de primera clase**: guardarlas en variables y pasarlas como argumentos. `aplicar(suma, a, b)` ejecuta la función recibida; es la base de map/filter/reduce y de los callbacks.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Pasar una función como argumento.
2. Guardar una función en una variable.
3. Explicar 'valor de primera clase'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Primera clase | Las funciones son valores |
| 2 | Pasar funciones | Como cualquier argumento |
| 3 | Función de orden superior | Recibe otra función |
| 4 | Callbacks | El patrón detrás de eventos |

## 📖 Definiciones y características

- **Valor de primera clase** — algo que se puede guardar, pasar y devolver. Clave: las funciones lo son en casi todos los lenguajes.
- **Función de orden superior** — recibe o devuelve funciones. Clave: `aplicar(f, a, b)`.
- **Callback** — función pasada para ejecutarse después. Clave: base de eventos y asincronía.
- **Puntero a función** — en C, un valor que apunta a una función. Clave: su forma de primera clase.

## 🧩 Situación

`aplicar(suma, 3, 4)` da 7 y `aplicar(producto, 3, 4)` da 12, usando la misma función `aplicar`. Poder pasar la operación como dato es lo que hace posibles map, filter y los callbacks.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b> producto=<a*b>`
- **Regla:** aplicar(f, a, b) = f(a, b); con f = suma y f = producto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7 producto=12` |
| `5 5` | `suma=10 producto=25` |
| `0 9` | `suma=9 producto=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION aplicar(f, a, b): DEVOLVER f(a, b)
ESCRIBIR "suma=" aplicar(suma,a,b) " producto=" aplicar(producto,a,b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def suma(a, b):
    return a + b


def producto(a, b):
    return a * b


def aplicar(f, a, b):
    return f(a, b)


a, b = map(int, sys.stdin.readline().split())
print(f"suma={aplicar(suma, a, b)} producto={aplicar(producto, a, b)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const suma = (a, b) => a + b;
const producto = (a, b) => a * b;
const aplicar = (f, a, b) => f(a, b);

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

type Op = (a: number, b: number) => number;
const suma: Op = (a, b) => a + b;
const producto: Op = (a, b) => a * b;
const aplicar = (f: Op, a: number, b: number): number => f(a, b);

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntBinaryOperator;

public class Main {
    static int aplicar(IntBinaryOperator f, int a, int b) {
        return f.applyAsInt(a, b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        IntBinaryOperator suma = (x, y) -> x + y;
        IntBinaryOperator producto = (x, y) -> x * y;
        System.out.println("suma=" + aplicar(suma, a, b) + " producto=" + aplicar(producto, a, b));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int Aplicar(Func<int, int, int> f, int a, int b) => f(a, b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Func<int, int, int> suma = (x, y) => x + y;
Func<int, int, int> producto = (x, y) => x * y;
Console.WriteLine($"suma={Aplicar(suma, a, b)} producto={Aplicar(producto, a, b)}");
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

func suma(a, b int) int     { return a + b }
func producto(a, b int) int { return a * b }

func aplicar(f func(int, int) int, a, b int) int {
	return f(a, b)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	fields := strings.Fields(line)
	a, _ := strconv.Atoi(fields[0])
	b, _ := strconv.Atoi(fields[1])
	fmt.Printf("suma=%d producto=%d\n", aplicar(suma, a, b), aplicar(producto, a, b))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn producto(a: i64, b: i64) -> i64 {
    a * b
}

fn aplicar(f: fn(i64, i64) -> i64, a: i64, b: i64) -> i64 {
    f(a, b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={} producto={}", aplicar(suma, v[0], v[1]), aplicar(producto, v[0], v[1]));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long suma(long a, long b) { return a + b; }
long producto(long a, long b) { return a * b; }

long aplicar(long (*f)(long, long), long a, long b) {
    return f(a, b);
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld producto=%ld\n", aplicar(suma, a, b), aplicar(producto, a, b));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa operadores/funciones incorporadas, no funciones como valor.
WITH pares(a, b) AS (VALUES (3, 4), (5, 5), (0, 9))
SELECT printf('suma=%d producto=%d', a + b, a * b) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
$suma = fn($a, $b) => $a + $b;
$producto = fn($a, $b) => $a * $b;
function aplicar($f, $a, $b) {
    return $f($a, $b);
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
echo "suma=" . aplicar($suma, $a, $b) . " producto=" . aplicar($producto, $a, $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Pasar `suma` directamente (Python/JS/Go/Rust) vs. puntero a función (C) o interfaz funcional (Java). |
| Semántica | La función es un valor; se invoca con `f(a, b)`. |
| Paradigmática | SQL no pasa funciones; usa operadores/funciones incorporadas. |

## 🧬 El concepto en la familia

En Ruby se pasan `Proc`/bloques o `method(:suma)`. En Haskell pasar funciones es lo más natural del lenguaje.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 085
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Llamar la función en vez de pasarla** → causa: pasar `suma(a,b)` en lugar de `suma` → solución: pasar el nombre sin paréntesis
- **Firmas incompatibles** → causa: la de orden superior espera otra forma → solución: asegurar que la función pasada encaja con lo esperado

## ❓ Preguntas frecuentes

- **¿Callbacks son esto?** Sí: un callback es una función que pasas para que se ejecute más tarde.
- **¿C tiene funciones de primera clase?** Parcialmente: con punteros a función, aunque sin cierres.

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

> [⏮️ Clase 084](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 086 ⏭️](../../parte-5-funciones-y-modularidad/086-modulos-paquetes-y-espacios-de-nombres/README.md)
