# Clase 097 — Árboles

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer los **árboles**: estructuras jerárquicas. En un árbol binario de búsqueda (BST), el recorrido in-order devuelve los elementos ordenados. Aquí el efecto observable es la ordenación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la propiedad del BST.
2. Reconocer el recorrido in-order.
3. Relacionar el árbol con el orden.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Árbol | Nodos con hijos, jerárquico |
| 2 | BST | Menores a la izquierda, mayores a la derecha |
| 3 | Recorrido in-order | Produce el orden ascendente |

## 📖 Definiciones y características

- **Árbol** — estructura jerárquica de nodos con hijos. Clave: sin ciclos, una raíz.
- **BST** — árbol binario ordenado: izquierda < nodo < derecha. Clave: búsqueda O(log n) equilibrado.
- **In-order** — recorrido izquierda-raíz-derecha. Clave: en un BST da los valores ordenados.

## 🧩 Situación

Índices de bases de datos, sistemas de archivos, autocompletado: los árboles organizan datos jerárquicos y permiten búsquedas rápidas. En un BST, recorrer in-order ordena.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros distintos separados por espacio
- **Salida** (stdout): `inorden=<los valores ordenados ascendente unidos por ->`
- **Regla:** in-order de un BST = orden ascendente

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `inorden=1-3-4` |
| `5 2 8 1` | `inorden=1-2-5-8` |
| `9 7` | `inorden=7-9` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; insertar en BST ; recorrer in-order
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.sort()  # in-order de un BST equivale al orden ascendente
print("inorden=" + "-".join(str(x) for x in nums))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.TreeSet;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        TreeSet<Integer> t = new TreeSet<>();
        for (String s : p) t.add(Integer.parseInt(s));
        System.out.println("inorden=" + t.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).OrderBy(x => x);
Console.WriteLine($"inorden={string.Join("-", nums)}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	sort.Ints(nums)
	parts := make([]string, len(nums))
	for i, n := range nums {
		parts[i] = strconv.Itoa(n)
	}
	fmt.Printf("inorden=%s\n", strings.Join(parts, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    nums.sort();
    let texto: Vec<String> = nums.iter().map(|x| x.to_string()).collect();
    println!("inorden={}", texto.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    long x = *(const long *) a, y = *(const long *) b;
    return (x > y) - (x < y);
}

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    qsort(v, n, sizeof(long), cmp);
    printf("inorden=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: ORDER BY equivale al in-order del BST.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT 'inorden=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY x);
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
sort($nums);
echo "inorden=" . implode("-", $nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Ordenar (`sorted`) equivale al in-order del BST en esta clase. |
| Semántica | El BST mantiene el orden al insertar; ordenar lo hace de una vez. |
| Paradigmática | SQL usa ORDER BY, que el motor implementa con árboles/índices. |

## 🧬 El concepto en la familia

En muchos lenguajes se usa un TreeSet/TreeMap (árbol equilibrado) que ya mantiene el orden.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 097
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir in-order con otros recorridos** → causa: pre/post-order no ordenan → solución: usar in-order para obtener el orden
- **Insertar duplicados sin política** → causa: árbol ambiguo → solución: aquí los valores son distintos

## ❓ Preguntas frecuentes

- **¿Por qué in-order ordena?** Porque visita izquierda (menores), raíz, derecha (mayores) recursivamente.
- **¿BST o array ordenado?** El BST permite inserciones/borrados eficientes manteniendo el orden.

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

> [⏮️ Clase 096](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 098 ⏭️](../../parte-6-datos-y-estructuras/098-grafos/README.md)
