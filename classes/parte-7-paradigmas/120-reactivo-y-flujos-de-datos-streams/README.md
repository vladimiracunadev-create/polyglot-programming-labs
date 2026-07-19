# Clase 120 — Reactivo y flujos de datos (streams)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **reactivo / de flujos (streams)**: procesar datos como una corriente que pasa por operadores (filtrar, mapear) encadenados. Aquí un flujo filtra pares y los duplica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar operadores sobre un flujo.
2. Filtrar y transformar en pipeline.
3. Reconocer el estilo reactivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Flujo (stream) | Datos como corriente |
| 2 | Operadores encadenados | filter, map, … |
| 3 | Pipeline | El dato fluye por pasos |

## 📖 Definiciones y características

- **Flujo/stream** — secuencia de datos procesada por etapas. Clave: filter/map encadenados.
- **Operador** — etapa que transforma el flujo (filter, map). Clave: se encadenan.
- **Reactivo** — reaccionar a datos que llegan con el tiempo. Clave: streams y observables.

## 🧩 Situación

Procesar eventos que llegan, filas de un archivo grande o mensajes en tiempo real: el estilo de flujos encadena operadores (filtrar → transformar) sin materializar todo a la vez.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `stream=<pares duplicados, unidos por ->`
- **Regla:** flujo: filtrar pares, luego map x → 2x

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `stream=4-8` |
| `2 4` | `stream=4-8` |
| `6 7 8` | `stream=12-16` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
flujo(lista) |> filtrar(par) |> mapear(x->2x) |> recolectar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
stream = [x * 2 for x in nums if x % 2 == 0]
print("stream=" + "-".join(str(x) for x in stream))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const stream = nums.filter((x) => x % 2 === 0).map((x) => x * 2);
console.log(`stream=${stream.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const stream = nums.filter((x) => x % 2 === 0).map((x) => x * 2);
console.log(`stream=${stream.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        String r = Arrays.stream(p).map(Integer::parseInt)
                .filter(x -> x % 2 == 0).map(x -> x * 2)
                .map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("stream=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var stream = p.Select(int.Parse).Where(x => x % 2 == 0).Select(x => x * 2);
Console.WriteLine($"stream={string.Join("-", stream)}");
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
	var stream []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			stream = append(stream, strconv.Itoa(n*2))
		}
	}
	fmt.Printf("stream=%s\n", strings.Join(stream, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let stream: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| (x * 2).to_string())
        .collect();
    println!("stream={}", stream.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("stream=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x * 2);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: WHERE + SELECT es un pipeline declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'stream=' || group_concat(x * 2, '-') AS resultado FROM nums WHERE x % 2 = 0;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$stream = array_map(fn($x) => $x * 2, array_filter($nums, fn($x) => $x % 2 === 0));
echo "stream=" . implode("-", $stream) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `.filter().map()` (JS/Rust), Streams (Java), LINQ (C#), generadores (Python). |
| Semántica | Los operadores se encadenan; el dato fluye por el pipeline. |
| Paradigmática | SQL encadena WHERE + SELECT, un pipeline declarativo. |

## 🧬 El concepto en la familia

En Java, la API Streams; en el frontend, RxJS y observables son puro estilo reactivo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 120
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Materializar todo en cada paso** → causa: gasto de memoria → solución: encadenar operadores perezosos cuando se pueda
- **Orden de operadores equivocado** → causa: resultado distinto → solución: filtrar antes de mapear si conviene

## ❓ Preguntas frecuentes

- **¿Stream o bucle?** El stream es más declarativo y componible; el bucle da control fino.
- **¿Reactivo es solo frontend?** No: también backend (Reactor, Akka Streams) y procesamiento de datos.

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

> [⏮️ Clase 119](../../parte-7-paradigmas/119-orientado-a-eventos-y-callbacks/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 121 ⏭️](../../parte-7-paradigmas/121-concurrente-hilos-tareas-y-canales/README.md)
