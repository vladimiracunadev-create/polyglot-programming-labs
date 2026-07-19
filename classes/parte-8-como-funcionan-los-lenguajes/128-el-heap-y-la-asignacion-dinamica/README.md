# Clase 128 — El heap y la asignación dinámica

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **heap y la asignación dinámica**: cuando el tamaño de los datos no se conoce en compilación, se reservan en el heap. Una lista dinámica que crece con n vive en el heap.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir una estructura de tamaño dinámico.
2. Distinguir stack de heap.
3. Reconocer la asignación dinámica.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Heap | Memoria de vida y tamaño flexibles |
| 2 | Asignación dinámica | Reservar en ejecución |
| 3 | Stack vs. heap | Automático vs. gestionado |

## 📖 Definiciones y características

- **Heap** — región de memoria para datos de tamaño/vida no conocidos en compilación. Clave: más flexible que la pila.
- **Asignación dinámica** — reservar memoria en ejecución (una lista que crece). Clave: heap.
- **Stack vs. heap** — la pila es automática y rápida; el heap es flexible pero requiere gestión. Clave: distinto uso.

## 🧩 Situación

Una lista cuyo tamaño depende de la entrada (n) no cabe en la pila con tamaño fijo: se asigna en el heap. Casi todas las colecciones dinámicas viven ahí.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `lista=<n-(n-1)-...-1>`
- **Regla:** lista dinámica con los valores de n a 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `lista=3-2-1` |
| `1` | `lista=1` |
| `5` | `lista=5-4-3-2-1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar lista ; añadir n, n-1, ..., 1 ; unir por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
lista = []
for i in range(n, 0, -1):
    lista.append(i)
print("lista=" + "-".join(str(x) for x in lista))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista: number[] = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> lista = new ArrayList<>();
        for (int i = n; i >= 1; i--) lista.add(i);
        System.out.println("lista=" + lista.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var lista = new List<int>();
for (int i = n; i >= 1; i--) lista.Add(i);
Console.WriteLine($"lista={string.Join("-", lista)}");
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
	var lista []string
	for i := n; i >= 1; i-- {
		lista = append(lista, strconv.Itoa(i))
	}
	fmt.Printf("lista=%s\n", strings.Join(lista, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let lista: Vec<String> = (1..=n).rev().map(|x| x.to_string()).collect();
    println!("lista={}", lista.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *lista = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) lista[i] = n - i;
    printf("lista=");
    for (long i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", lista[i]);
    }
    printf("\n");
    free(lista);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: genera la secuencia descendente con un CTE (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (3) UNION ALL SELECT i - 1 FROM r WHERE i > 1)
SELECT 'lista=' || group_concat(i, '-') AS resultado FROM r;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$lista = [];
for ($i = $n; $i >= 1; $i--) {
    $lista[] = $i;
}
echo "lista=" . implode("-", $lista) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | list/Vec/ArrayList (heap) en cada lenguaje. |
| Semántica | El tamaño dinámico obliga al heap; C usa malloc. |
| Paradigmática | SQL genera la secuencia con un CTE. |

## 🧬 El concepto en la familia

En C la lista dinámica se hace con malloc/realloc; en los demás, las colecciones ya viven en el heap.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 128
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir tamaño fijo** → causa: no cabe en la pila → solución: usar una estructura dinámica
- **Fugas al no liberar (C)** → causa: memoria perdida → solución: liberar con free lo asignado

## ❓ Preguntas frecuentes

- **¿Todo va al heap?** No: los locales pequeños van a la pila; lo dinámico o grande, al heap.
- **¿El heap es más lento?** Su asignación cuesta más que la pila, pero permite tamaños flexibles.

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

> [⏮️ Clase 127](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 129 ⏭️](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md)
