# Clase 158 — Enlaces (bindings) y wrappers

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender los **enlaces (bindings) y wrappers**: una capa que adapta una librería nativa a un uso cómodo e idiomático en tu lenguaje. El wrapper traduce entre la frontera y tu código.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Envolver una función con un wrapper.
2. Explicar qué añade un binding.
3. Reconocer bindings comunes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Binding | Puente a una librería nativa |
| 2 | Wrapper | Adapta a un uso idiomático |
| 3 | Adaptación | Traducir entre fronteras |

## 📖 Definiciones y características

- **Binding** — capa que expone una librería de otro lenguaje en el tuyo. Clave: reutilizar sin reescribir.
- **Wrapper** — función que envuelve otra, adaptando su interfaz. Clave: uso más cómodo o seguro.
- **Adaptación** — traducir tipos y convenciones entre la librería nativa y tu código. Clave: ocultar la frontera.

## 🧩 Situación

Una librería de imágenes en C se expone en Python con un binding; el wrapper convierte tipos y hace la API pythónica. Aquí el wrapper duplica y presenta el resultado envuelto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `envuelto=wrap(<2n>)`
- **Regla:** wrapper que aplica doble y formatea

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `envuelto=wrap(10)` |
| `0` | `envuelto=wrap(0)` |
| `7` | `envuelto=wrap(14)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
r <- doble(n) ; ESCRIBIR 'wrap(' + r + ')'
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doble(x):
    return x * 2


def wrapper(x):  # adapta y formatea el resultado
    return f"wrap({doble(x)})"


n = int(sys.stdin.readline())
print(f"envuelto={wrapper(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const wrapper = (x) => `wrap(${doble(x)})`;

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const wrapper = (x: number): string => `wrap(${doble(x)})`;

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; }
    static String wrapper(long x) { return "wrap(" + doble(x) + ")"; }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("envuelto=" + wrapper(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Doble(long x) => x * 2;
string Wrapper(long x) => $"wrap({Doble(x)})";

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"envuelto={Wrapper(n)}");
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
func wrapper(x int64) string { return fmt.Sprintf("wrap(%d)", doble(x)) }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("envuelto=%s\n", wrapper(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2
}

fn wrapper(x: i64) -> String {
    format!("wrap({})", doble(x))
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("envuelto={}", wrapper(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(long x) { return x * 2; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("envuelto=wrap(%ld)\n", doble(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa vistas para envolver; aqui, la expresion formateada.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('envuelto=wrap(%d)', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doble($x) { return $x * 2; }
function wrapper($x) { return "wrap(" . doble($x) . ")"; }

$n = (int) trim(fgets(STDIN));
echo "envuelto=" . wrapper($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Una función que envuelve a otra en cada lenguaje. |
| Semántica | El wrapper adapta tipos y convenciones de la frontera. |
| Paradigmática | SQL usa vistas para envolver consultas. |

## 🧬 El concepto en la familia

PyBind11, node-gyp, JNA, cbindgen generan bindings entre lenguajes y C/C++.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 158
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Wrapper que filtra detalles de la frontera** → causa: abstracción con fugas → solución: ocultar la complejidad de la interoperabilidad
- **No manejar errores de la librería nativa** → causa: caídas inesperadas → solución: traducir los errores al modelo de tu lenguaje

## ❓ Preguntas frecuentes

- **¿Binding o reescribir?** El binding reutiliza código probado; reescribir cuesta y arriesga.
- **¿Wrapper añade coste?** Un poco, pero la comodidad y seguridad suelen compensar.

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

> [⏮️ Clase 157](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 159 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md)
