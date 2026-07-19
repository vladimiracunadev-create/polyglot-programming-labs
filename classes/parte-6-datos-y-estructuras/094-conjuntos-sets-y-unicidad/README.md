# Clase 094 — Conjuntos (sets) y unicidad

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **conjunto (set)**: una colección sin duplicados. Contar los valores únicos es la operación natural del conjunto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Eliminar duplicados con un conjunto.
2. Contar elementos distintos.
3. Reconocer que el conjunto no tiene orden garantizado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Conjunto | Colección sin duplicados |
| 2 | Unicidad | Cada valor una vez |
| 3 | Pertenencia | Comprobar si algo está |

## 📖 Definiciones y características

- **Conjunto** — colección de elementos únicos (set, HashSet). Clave: sin duplicados.
- **Unicidad** — propiedad de no repetir. Clave: añadir un existente no hace nada.
- **Pertenencia** — comprobar si un elemento está, en O(1) típico. Clave: uso habitual del set.

## 🧩 Situación

¿Cuántos usuarios distintos entraron? ¿Cuántas etiquetas únicas hay? El conjunto elimina duplicados y responde al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `unicos=<cantidad de valores distintos>`
- **Regla:** unicos = |conjunto(lista)|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3 3 3` | `unicos=3` |
| `5 5 5` | `unicos=1` |
| `1 2 3 4` | `unicos=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; conjunto <- SET(lista) ; ESCRIBIR |conjunto|
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"unicos={len(set(nums))}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> s = new HashSet<>();
        for (String x : p) s.add(Integer.parseInt(x));
        System.out.println("unicos=" + s.size());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"unicos={p.Select(int.Parse).Distinct().Count()}");
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
	set := make(map[int]struct{})
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("unicos=%d\n", len(set))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let set: HashSet<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("unicos={}", set.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int unicos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) unicos++;
    }
    printf("unicos=%d\n", unicos);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COUNT(DISTINCT x).
WITH nums(x) AS (VALUES (1), (2), (2), (3), (3), (3))
SELECT printf('unicos=%d', count(DISTINCT x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "unicos=" . count(array_unique($nums)) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `set(x)` (Python), `new Set` (JS), `HashSet` (Java/Rust/C#). |
| Semántica | El conjunto no garantiza orden; C lo simula con un bucle. |
| Paradigmática | SQL usa `COUNT(DISTINCT x)`. |

## 🧬 El concepto en la familia

En Ruby `lista.uniq.size`. En Go, un `map[int]struct{}` hace de conjunto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 094
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden en un conjunto** → causa: esperar los elementos ordenados → solución: usar una lista/ordenar si necesitas orden
- **Contar con bucles O(n²) sin necesidad** → causa: lento en listas grandes → solución: usar un conjunto con pertenencia O(1)

## ❓ Preguntas frecuentes

- **¿El conjunto conserva el orden?** En general no; algunos lenguajes tienen variantes ordenadas.
- **¿Conjunto o lista?** Conjunto si te importa la unicidad y la pertenencia rápida.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 093](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 095 ⏭️](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md)
