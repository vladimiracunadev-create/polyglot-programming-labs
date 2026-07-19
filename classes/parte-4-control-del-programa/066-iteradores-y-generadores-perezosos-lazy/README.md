# Clase 066 — Iteradores y generadores perezosos (lazy)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Producir una secuencia bajo demanda, la idea detrás de los **iteradores y generadores perezosos**: calcular los valores uno a uno en lugar de tener toda la lista de antemano.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar una secuencia de longitud n.
2. Reconocer la evaluación perezosa (lazy).
3. Distinguir generar de tener ya calculado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Generar bajo demanda | Producir valores al pedirlos |
| 2 | Perezoso (lazy) | No calcular hasta que se necesita |
| 3 | Iterador | Objeto que entrega el siguiente valor |
| 4 | take n | Tomar solo los primeros n |

## 📖 Definiciones y características

- **Iterador** — objeto que produce valores uno a uno. Clave: no necesita toda la colección en memoria.
- **Generador** — función que produce una secuencia perezosa (yield). Clave: calcula al vuelo.
- **Evaluación perezosa** — calcular un valor solo cuando se pide. Clave: permite secuencias infinitas.
- **take** — tomar los primeros n de una secuencia. Clave: corta lo infinito.

## 🧩 Situación

Los pares no tienen fin. Con un generador perezoso pides 'los primeros n' sin construir una lista infinita: cada valor se calcula cuando lo necesitas. Es como abrir el grifo solo lo justo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `pares=<2-4-...-2n>`
- **Regla:** pares_i = 2·i para i de 1 a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `pares=2-4-6` |
| `1` | `pares=2` |
| `5` | `pares=2-4-6-8-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA i de 1 a n: emitir 2*i
ESCRIBIR "pares=" UNIR(emitidos, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
pares = (2 * i for i in range(1, n + 1))
print("pares=" + "-".join(str(x) for x in pares))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares: number[] = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append("-");
            sb.append(2 * i);
        }
        System.out.println("pares=" + sb);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var pares = Enumerable.Range(1, n).Select(i => 2 * i);
Console.WriteLine($"pares={string.Join("-", pares)}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var sb strings.Builder
	for i := 1; i <= n; i++ {
		if i > 1 {
			sb.WriteString("-")
		}
		sb.WriteString(strconv.Itoa(2 * i))
	}
	fmt.Printf("pares=%s\n", sb.String())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pares: Vec<String> = (1..=n).map(|i| (2 * i).to_string()).collect();
    println!("pares={}", pares.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("pares=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", 2 * i);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: genera los pares con un CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE pares(i, v) AS (
    VALUES (1, 2)
    UNION ALL SELECT i + 1, (i + 1) * 2 FROM pares WHERE i < 5
)
SELECT 'pares=' || group_concat(v, '-') AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$pares = [];
for ($i = 1; $i <= $n; $i++) {
    $pares[] = 2 * $i;
}
echo "pares=" . implode("-", $pares) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(2*i for i in ...)` (Python) vs. `(1..=n).map(...)` (Rust) vs. bucle (C/Java). |
| Semántica | Python/Rust generan perezosamente; C/Java construyen la lista al vuelo. |
| Paradigmática | SQL genera con un CTE recursivo. |

## 🧬 El concepto en la familia

En Ruby `(1..n).map { |i| i*2 }` o un `Enumerator` perezoso. En Haskell `take n [2,4..]` sobre una lista infinita.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 066
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Construir una lista infinita entera** → causa: memoria agotada → solución: generar perezosamente y tomar solo n
- **Olvidar el separador en n=1** → causa: un guion sobrante → solución: unir con el separador, no anteponerlo

## ❓ Preguntas frecuentes

- **¿Qué gana la pereza?** Trabajar con secuencias enormes o infinitas usando solo lo que consumes.
- **¿Python genera perezoso?** Sí, con generadores (`yield`) y expresiones generadoras `( ... for ... )`.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 065](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 067 ⏭️](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md)
