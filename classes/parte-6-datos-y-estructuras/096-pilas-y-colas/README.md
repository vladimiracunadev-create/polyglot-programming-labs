# Clase 096 — Pilas y colas

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **pila (LIFO)** de **cola (FIFO)**: dos formas de ordenar la salida. La pila devuelve el último que entró; la cola, el primero.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular una pila y una cola.
2. Explicar LIFO frente a FIFO.
3. Reconocer sus usos típicos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila (LIFO) | Último en entrar, primero en salir |
| 2 | Cola (FIFO) | Primero en entrar, primero en salir |
| 3 | push/pop, enqueue/dequeue | Sus operaciones |

## 📖 Definiciones y características

- **Pila** — estructura LIFO: se saca el último añadido. Clave: deshacer, llamadas.
- **Cola** — estructura FIFO: se saca el primero añadido. Clave: turnos, tareas.
- **LIFO/FIFO** — orden de salida. Clave: define la estructura.

## 🧩 Situación

La pila modela el 'deshacer' y la pila de llamadas; la cola modela una fila de impresión o de tareas. La misma entrada sale en orden opuesto según la estructura.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `pila=<orden LIFO> cola=<orden FIFO>`
- **Regla:** pila = inverso(lista); cola = lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `pila=3-2-1 cola=1-2-3` |
| `5` | `pila=5 cola=5` |
| `1 2 3 4` | `pila=4-3-2-1 cola=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; pila <- sacar en LIFO ; cola <- sacar en FIFO
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
pila = "-".join(str(x) for x in reversed(nums))
cola = "-".join(str(x) for x in nums)
print(f"pila={pila} cola={cola}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
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
        String[] p = br.readLine().trim().split("\\s+");
        List<String> l = new ArrayList<>();
        for (String s : p) l.add(s);
        List<String> rev = new ArrayList<>(l);
        java.util.Collections.reverse(rev);
        System.out.println("pila=" + String.join("-", rev) + " cola=" + String.join("-", l));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string pila = string.Join("-", p.Reverse());
string cola = string.Join("-", p);
Console.WriteLine($"pila={pila} cola={cola}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	rev := make([]string, len(f))
	for i, x := range f {
		rev[len(f)-1-i] = x
	}
	fmt.Printf("pila=%s cola=%s\n", strings.Join(rev, "-"), strings.Join(f, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    let mut rev = nums.clone();
    rev.reverse();
    println!("pila={} cola={}", rev.join("-"), nums.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("pila=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf(" cola=");
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
-- SQL: orden descendente (pila) y ascendente (cola) por posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'pila=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos DESC))
     || ' cola=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos ASC)) AS resultado;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = implode("-", array_reverse($nums));
$cola = implode("-", $nums);
echo "pila=$pila cola=$cola\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `append`/`pop` (Python), `push`/`shift` (JS), `Deque` (Java). |
| Semántica | La pila saca por el final; la cola por el frente. |
| Paradigmática | SQL ordena por la posición ascendente o descendente. |

## 🧬 El concepto en la familia

En Go una pila/cola se hace con un slice. En C++ `std::stack` y `std::queue`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 096
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir el extremo de salida** → causa: pila y cola invertidas → solución: pila saca por el final; cola por el frente
- **Usar shift/remove(0) en listas grandes** → causa: coste O(n) → solución: usar una estructura de cola eficiente (deque)

## ❓ Preguntas frecuentes

- **¿Pila o cola?** Pila para LIFO (deshacer, recursión); cola para FIFO (turnos, tareas).
- **¿La recursión usa pila?** Sí: la pila de llamadas es una pila real del programa.

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

> [⏮️ Clase 095](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 097 ⏭️](../../parte-6-datos-y-estructuras/097-arboles/README.md)
