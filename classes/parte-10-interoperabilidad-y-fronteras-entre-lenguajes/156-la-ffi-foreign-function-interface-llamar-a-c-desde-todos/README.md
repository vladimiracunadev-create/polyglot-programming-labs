# Clase 156 — La FFI (Foreign Function Interface): llamar a C desde todos

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **FFI (Foreign Function Interface)**: el mecanismo para llamar a código escrito en otro lenguaje, típicamente C. Casi todos los lenguajes pueden llamar a C, lo que hace de C el 'idioma común' entre lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la FFI.
2. Reconocer por qué C es el puente universal.
3. Llamar a una función 'externa'.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | FFI | Llamar a otro lenguaje |
| 2 | C como puente | Casi todos llaman a C |
| 3 | Enlace | Unir con la librería externa |

## 📖 Definiciones y características

- **FFI** — interfaz para llamar a funciones de otro lenguaje. Clave: reutilizar librerías nativas.
- **Función externa** — definida en otro lenguaje (C) y llamada desde el tuyo. Clave: se declara su firma.
- **C como lingua franca** — casi todos los lenguajes exponen una FFI hacia C. Clave: puente universal.

## 🧩 Situación

Python usa librerías numéricas en C, Ruby extensiones en C, la JVM llama a C con JNI. La FFI hacia C conecta ecosistemas; por eso duplicar un número 'en C' se puede invocar desde cualquier lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** llamar a doble(n) 'externo'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
declarar doble (externa) ; ESCRIBIR doble(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doble(x):  # simula una función externa (FFI hacia C)
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2; // función 'externa' vía FFI
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
    static long doble(long x) { return x * 2; } // simula JNI hacia C

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

long Doble(long x) => x * 2; // simula P/Invoke hacia C

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

func doble(x int64) int64 { return x * 2 } // simula cgo hacia C

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2 // en un caso real, una funcion externa con extern "C"
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(long x) { return x * 2; } /* la funcion nativa en C */

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL llama a funciones definidas por el usuario; aqui, la expresion.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doble($x) { return $x * 2; } // simula una extension en C

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | ctypes/cffi (Python), extern (Rust/C), JNI (Java). |
| Semántica | La FFI cruza la frontera de lenguaje con una convención de llamada. |
| Paradigmática | SQL llama a funciones definidas por el usuario. |

## 🧬 El concepto en la familia

ctypes (Python), extern "C" (Rust/C++), JNI (Java), cgo (Go): todos hacia C.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 156
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Firmas incompatibles en la FFI** → causa: corrupción o caídas → solución: declarar exactamente los tipos que espera C
- **Ignorar la gestión de memoria a través de la frontera** → causa: fugas o dobles liberaciones → solución: acordar quién libera qué

## ❓ Preguntas frecuentes

- **¿Por qué C?** Su ABI simple y estable lo hace el mínimo común denominador.
- **¿Toda FFI es hacia C?** Mayormente; también hay puentes directos entre algunos lenguajes.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

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

> [⏮️ Clase 155](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 157 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md)
