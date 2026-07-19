# Clase 114 — Funcional I: inmutabilidad y funciones puras

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (I)**: inmutabilidad y funciones puras. Transformar una lista con `map` produce una lista nueva sin alterar la original ni usar estado mutable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección sin mutarla.
2. Reconocer la inmutabilidad.
3. Usar map en lugar de un bucle con estado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inmutabilidad | No modificar, crear nuevo |
| 2 | map | Transformar cada elemento |
| 3 | Sin estado mutable | Sin acumuladores |

## 📖 Definiciones y características

- **Funcional** — paradigma basado en funciones puras e inmutabilidad. Clave: sin efectos ni estado mutable.
- **Inmutabilidad** — los datos no cambian; las transformaciones crean nuevos. Clave: más seguro.
- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: no muta.

## 🧩 Situación

En vez de recorrer y mutar, el estilo funcional describe la transformación: 'la lista de los dobles'. La original queda intacta, lo que evita errores por estado compartido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por ->`
- **Regla:** doblados = map(x → 2x, lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6` |
| `5` | `doblados=10` |
| `2 4` | `doblados=4-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblados <- MAP(x -> 2x, lista) ; ESCRIBIR unidos por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = list(map(lambda x: x * 2, nums))
print("doblados=" + "-".join(str(x) for x in doblados))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
console.log(`doblados=${doblados.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
console.log(`doblados=${doblados.join("-")}`);
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
        String r = Arrays.stream(p).map(Integer::parseInt).map(x -> x * 2)
                .map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2);
Console.WriteLine($"doblados={string.Join("-", doblados)}");
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
	var doblados []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		doblados = append(doblados, strconv.Itoa(n*2))
	}
	fmt.Printf("doblados=%s\n", strings.Join(doblados, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<String> = s
        .split_whitespace()
        .map(|x| (x.parse::<i64>().unwrap() * 2).to_string())
        .collect();
    println!("doblados={}", doblados.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("doblados=");
    while (scanf("%ld", &x) == 1) {
        if (!primero) printf("-");
        printf("%ld", x * 2);
        primero = 0;
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la transformación va en el SELECT, sin mutar.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$doblados = array_map(fn($x) => $x * 2, $nums);
echo "doblados=" . implode("-", $doblados) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map` (Python/JS/Rust), streams (Java), LINQ Select (C#). |
| Semántica | No muta la lista original; devuelve otra. |
| Paradigmática | SQL transforma en el SELECT, sin mutar. |

## 🧬 El concepto en la familia

En Haskell `map (*2) xs` es el ejemplo puro. Casi todos ofrecen map.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 114
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mutar dentro del map** → causa: efecto secundario → solución: mantener la transformación pura
- **Confundir map con for-each** → causa: map devuelve; for-each no → solución: usar map cuando quieres el resultado

## ❓ Preguntas frecuentes

- **¿Map es más lento que un bucle?** Generalmente comparable; y evita errores de estado.
- **¿Inmutabilidad no gasta memoria?** Crea nuevos datos, pero permite compartir y razonar mejor.

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

> [⏮️ Clase 113](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 115 ⏭️](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md)
