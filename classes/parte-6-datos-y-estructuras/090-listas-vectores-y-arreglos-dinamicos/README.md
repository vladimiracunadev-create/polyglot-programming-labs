# Clase 090 — Listas, vectores y arreglos dinámicos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar una **lista/vector dinámico**: una secuencia que crece y encoge. Invertirla ejercita el recorrido y la construcción de una nueva secuencia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir y recorrer una lista dinámica.
2. Invertir el orden de los elementos.
3. Distinguir lista dinámica de arreglo fijo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lista dinámica | Crece según haga falta |
| 2 | Invertir | Recorrer al revés |
| 3 | Redimensionar | Añadir/quitar elementos |

## 📖 Definiciones y características

- **Lista/vector dinámico** — arreglo que cambia de tamaño (list, Vec, ArrayList). Clave: flexible.
- **append** — añadir un elemento al final. Clave: operación base.
- **Inversión** — producir la secuencia en orden contrario. Clave: primero pasa a último.

## 🧩 Situación

Cuando no sabes cuántos elementos habrá (líneas de un archivo, respuestas de un usuario), la lista dinámica es la elección natural.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `invertido=<elementos en orden inverso unidos por ->`
- **Regla:** invertido = reverse(lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `invertido=3-2-1` |
| `5` | `invertido=5` |
| `10 20 30 40` | `invertido=40-30-20-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; invertir ; ESCRIBIR unidos por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.reverse()
print("invertido=" + "-".join(str(x) for x in nums))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> nums = new ArrayList<>();
        for (String s : p) nums.add(Integer.parseInt(s));
        Collections.reverse(nums);
        System.out.println("invertido=" + nums.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).Reverse();
Console.WriteLine($"invertido={string.Join("-", nums)}");
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
	for i, j := 0, len(f)-1; i < j; i, j = i+1, j-1 {
		f[i], f[j] = f[j], f[i]
	}
	fmt.Printf("invertido=%s\n", strings.Join(f, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<&str> = s.split_whitespace().collect();
    nums.reverse();
    println!("invertido={}", nums.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: invierte con ORDER BY sobre la posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'invertido=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY pos DESC);
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$nums = array_reverse($nums);
echo "invertido=" . implode("-", $nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list[::-1]` (Python), `.reverse()` (JS/Rust), `Collections.reverse` (Java). |
| Semántica | Algunos invierten en sitio (mutando); otros crean una lista nueva. |
| Paradigmática | SQL invierte con ORDER BY descendente sobre una posición. |

## 🧬 El concepto en la familia

En Ruby `lista.reverse`. En Go se invierte con un bucle de índices intercambiando extremos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 090
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir invertir en sitio con crear copia** → causa: modificar el original sin querer → solución: elegir según necesites conservar el original
- **Bucle de intercambio mal** → causa: invertir de más y volver al inicio → solución: intercambiar solo hasta la mitad

## ❓ Preguntas frecuentes

- **¿Lista o arreglo?** Lista si el tamaño varía; arreglo fijo si es constante.
- **¿Invertir es caro?** Es O(n): hay que tocar cada elemento una vez.

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

> [⏮️ Clase 089](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 091 ⏭️](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md)
