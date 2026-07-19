# Clase 132 — RAII, propiedad y préstamos (Rust/C++)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **RAII, propiedad y préstamos** como alternativa al GC. En Rust, un valor tiene un dueño y puede prestarse para leerlo sin copiarlo ni transferir la propiedad; se libera determinísticamente al salir del ámbito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar propiedad y préstamo.
2. Leer un valor prestado sin poseerlo.
3. Contrastar RAII con el GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Propiedad | Un dueño por valor |
| 2 | Préstamo | Usar sin poseer |
| 3 | RAII | Liberar al salir del ámbito |

## 📖 Definiciones y características

- **RAII** — la vida del recurso se ata a la del objeto dueño. Clave: liberación determinista, sin GC.
- **Propiedad** — cada valor tiene un dueño responsable de liberarlo. Clave: base de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.

## 🧩 Situación

Rust libera memoria sin recolector: el dueño la libera al salir del ámbito (RAII) y los préstamos permiten leer sin copiar. El resultado es memoria segura sin pausas de GC.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** prestar n a una función que devuelve 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
prestar n (referencia) a doble(&n) ; ESCRIBIR resultado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doble(x):
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + doble(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Doble(long x) => x * 2;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
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

func doble(x int64) int64 { return x * 2 }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: &i64) -> i64 {
    *x * 2 // préstamo: se lee sin tomar la propiedad
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(&n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(const long *x) {
    return *x * 2; /* se accede por referencia sin copiar */
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(&n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone propiedad de memoria; se calcula el resultado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doble($x) {
    return $x * 2;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `&valor` (Rust/C++) vs. paso normal en los demás. |
| Semántica | Rust libera determinísticamente sin GC; el préstamo no copia. |
| Paradigmática | SQL no expone propiedad de memoria. |

## 🧬 El concepto en la familia

C++ tiene RAII y referencias; Rust lo lleva más lejos comprobando los préstamos en compilación.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 132
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Prestar y mover a la vez (Rust)** → causa: conflicto de préstamos → solución: elegir prestar o mover, no ambos a la vez
- **Depender del GC donde hay RAII** → causa: esperar pausas donde no las hay → solución: aprovechar la liberación determinista

## ❓ Preguntas frecuentes

- **¿RAII o GC?** RAII da liberación predecible sin pausas; el GC da comodidad. Distintos compromisos.
- **¿Prestar copia el dato?** No: un préstamo es una referencia; no duplica.

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

> [⏮️ Clase 131](../../parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura-gc/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 133 ⏭️](../../parte-8-como-funcionan-los-lenguajes/133-concurrencia-procesos-hilos-y-memoria-compartida/README.md)
