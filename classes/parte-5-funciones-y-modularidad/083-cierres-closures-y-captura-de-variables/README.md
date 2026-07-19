# Clase 083 — Cierres (closures) y captura de variables

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **cierres (closures)**: funciones que capturan y recuerdan variables de su entorno. Un `sumador(base)` devuelve una función que suma `base` a lo que reciba, recordándolo entre llamadas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear un cierre que captura una variable.
2. Reusar el cierre en varias llamadas.
3. Explicar qué significa 'capturar el entorno'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Cierre (closure) | Función que recuerda su entorno |
| 2 | Captura | Recordar variables externas |
| 3 | Función que devuelve función | Fábricas de funciones |
| 4 | Estado encapsulado | El valor capturado persiste |

## 📖 Definiciones y características

- **Cierre** — función que captura variables de su entorno de definición. Clave: las recuerda al ejecutarse después.
- **Captura** — recordar una variable externa dentro del cierre. Clave: por valor o por referencia.
- **Función de orden superior** — la que devuelve o recibe funciones. Clave: fábrica de cierres.
- **Estado capturado** — el valor que el cierre conserva. Clave: como una variable privada.

## 🧩 Situación

`hacer_sumador(10)` devuelve una función que siempre suma 10. Llamarla con 1 da 11; con 2, 12. El cierre 'recuerda' el 10 sin que se lo vuelvas a pasar.

## 🧮 Modelo

- **Entrada** (stdin): un entero `base`
- **Salida** (stdout): `r1=<base+1> r2=<base+2>`
- **Regla:** sumar = λx. base + x ; r1 = sumar(1) ; r2 = sumar(2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `r1=11 r2=12` |
| `0` | `r1=1 r2=2` |
| `100` | `r1=101 r2=102` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER base
sumar <- hacer_sumador(base)   // captura base
ESCRIBIR "r1=" sumar(1) " r2=" sumar(2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def hacer_sumador(base):
    def sumar(x):
        return base + x
    return sumar


base = int(sys.stdin.readline())
sumar = hacer_sumador(base)
print(f"r1={sumar(1)} r2={sumar(2)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function hacerSumador(base) {
  return (x) => base + x;
}

const base = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function hacerSumador(base: number): (x: number) => number {
  return (x) => base + x;
}

const base: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    static IntUnaryOperator hacerSumador(int base) {
        return x -> base + x; // captura base (efectivamente final)
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int base = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator sumar = hacerSumador(base);
        System.out.println("r1=" + sumar.applyAsInt(1) + " r2=" + sumar.applyAsInt(2));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

Func<int, int> HacerSumador(int baseN) => x => baseN + x;

int b = int.Parse(Console.In.ReadToEnd().Trim());
var sumar = HacerSumador(b);
Console.WriteLine($"r1={sumar(1)} r2={sumar(2)}");
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

func hacerSumador(base int) func(int) int {
	return func(x int) int {
		return base + x
	}
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	base, _ := strconv.Atoi(strings.TrimSpace(line))
	sumar := hacerSumador(base)
	fmt.Printf("r1=%d r2=%d\n", sumar(1), sumar(2))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let base: i64 = s.trim().parse().unwrap();
    let sumar = |x: i64| base + x; // captura base
    println!("r1={} r2={}", sumar(1), sumar(2));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene cierres: el estado (base) se pasa como parámetro. */
long sumar(long base, long x) {
    return base + x;
}

int main(void) {
    long base;
    if (scanf("%ld", &base) != 1) return 1;
    printf("r1=%ld r2=%ld\n", sumar(base, 1), sumar(base, 2));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene cierres: se parametriza con valores en la consulta.
WITH bases(base) AS (VALUES (10), (0), (100))
SELECT printf('r1=%d r2=%d', base + 1, base + 2) AS resultado FROM bases;
```

### PHP · `php main.php`

```php
<?php
function hacerSumador($base) {
    return fn($x) => $base + $x;
}

$base = (int) trim(fgets(STDIN));
$sumar = hacerSumador($base);
echo "r1=" . $sumar(1) . " r2=" . $sumar(2) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `lambda`/`=>`/`\|x\|` para el cierre; C usa un puntero a función + parámetro. |
| Semántica | La mayoría captura el entorno; C no tiene cierres (se pasa el dato aparte). |
| Paradigmática | SQL no tiene cierres; se parametriza con valores en la consulta. |

## 🧬 El concepto en la familia

En Ruby los bloques y `lambda` capturan el entorno. En Haskell, la aplicación parcial produce cierres de forma natural.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 083
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capturar por referencia sin querer** → causa: el cierre ve cambios posteriores de la variable → solución: capturar por valor si necesitas fijar el estado
- **Esperar cierres en C** → causa: no existen → solución: pasar el estado como parámetro explícito

## ❓ Preguntas frecuentes

- **¿Cierre o clase?** Un cierre es como un objeto con un solo método y estado privado; a veces más ligero.
- **¿Qué captura, el valor o la variable?** Depende del lenguaje: por valor (copia) o por referencia (enlace vivo).

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

> [⏮️ Clase 082](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 084 ⏭️](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md)
