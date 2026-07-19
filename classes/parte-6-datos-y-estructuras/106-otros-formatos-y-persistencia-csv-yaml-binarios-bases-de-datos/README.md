# Clase 106 — Otros formatos y persistencia: CSV, YAML, binarios, bases de datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con **persistencia y formatos tabulares**: CSV (valores separados por comas) es el formato más simple para guardar y compartir datos en tabla. Aquí se serializa una fila y se cuentan sus campos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Serializar valores a una línea CSV.
2. Contar los campos.
3. Reconocer CSV frente a JSON.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CSV | Valores separados por comas |
| 2 | Campo | Cada valor de la fila |
| 3 | Persistencia | Guardar datos en formato de texto |

## 📖 Definiciones y características

- **CSV** — formato tabular: filas de valores separados por comas. Clave: simple y universal.
- **Campo** — cada valor de una fila CSV. Clave: separado por el delimitador.
- **Persistencia** — guardar datos para recuperarlos después. Clave: archivos, bases de datos.

## 🧩 Situación

Exportar a Excel, cargar datos en una base, intercambiar tablas: el CSV es el mínimo común denominador. Una fila `1,2,3` con 3 campos es su unidad.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `csv=<valores separados por coma> campos=<cantidad>`
- **Regla:** csv = unir con coma ; campos = cantidad de valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `csv=1,2,3 campos=3` |
| `5` | `csv=5 campos=1` |
| `10 20` | `csv=10,20 campos=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; csv <- unir con , ; campos <- longitud
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = sys.stdin.read().split()
csv = ",".join(nums)
print(f"csv={csv} campos={len(nums)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        System.out.println("csv=" + String.join(",", nums) + " campos=" + nums.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"csv={string.Join(",", nums)} campos={nums.Length}");
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
	nums := strings.Fields(line)
	fmt.Printf("csv=%s campos=%d\n", strings.Join(nums, ","), len(nums))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    println!("csv={} campos={}", nums.join(","), nums.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[64];
    int campos = 0;
    printf("csv=");
    while (scanf("%63s", tok) == 1) {
        if (campos > 0) printf(",");
        printf("%s", tok);
        campos++;
    }
    printf(" campos=%d\n", campos);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: group_concat produce una fila CSV.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'csv=' || group_concat(x, ',') || printf(' campos=%d', count(*)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "csv=" . implode(",", $nums) . " campos=" . count($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `','.join(...)` (Python), `.join(',')` (JS), bucle (C). |
| Semántica | CSV real necesita escapar comas y comillas; aquí los datos son simples. |
| Paradigmática | SQL exporta/importa CSV con comandos del motor. |

## 🧬 El concepto en la familia

En Ruby `arr.join(',')`. Casi todos tienen una librería CSV que maneja comillas y saltos correctamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 106
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No escapar comas dentro de un campo** → causa: CSV corrupto → solución: usar una librería CSV para datos reales
- **Confundir campos con caracteres** → causa: contar mal → solución: los campos se separan por el delimitador

## ❓ Preguntas frecuentes

- **¿CSV o JSON?** CSV para tablas simples y planas; JSON para datos anidados y estructurados.
- **¿CSV siempre usa comas?** Casi siempre; algunos usan punto y coma o tabuladores según la configuración regional.

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

> [⏮️ Clase 105](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 107 ⏭️](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md)
