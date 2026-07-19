# Clase 170 — Componente de datos y consultas (SQL)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de datos y consultas** (SQL): la capa de persistencia responde consultas. Aquí agrega (suma) un conjunto de valores, como haría una consulta de agregación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Agregar un conjunto de datos.
2. Explicar el rol de la capa de datos.
3. Reconocer SQL como su lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Capa de datos | Persistencia y consultas |
| 2 | Agregación | Resumir muchos en uno |
| 3 | Consulta | Pedir datos declarativamente |

## 📖 Definiciones y características

- **Componente de datos** — la capa que almacena y consulta la información. Clave: fuente de verdad del sistema.
- **Agregación** — combinar muchas filas en un valor (SUM, AVG). Clave: resumen de datos.
- **Consulta declarativa** — describir qué datos se quieren, no cómo obtenerlos. Clave: propio de SQL.

## 🧩 Situación

El backend pide 'el total de ventas': la capa de datos ejecuta una consulta de agregación (`SELECT SUM(...)`) y devuelve el número. SQL es el lenguaje natural de este componente.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (valores a agregar)
- **Salida** (stdout): `total=<suma de los valores>`
- **Regla:** total = suma de los valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 20 30` | `total=60` |
| `5` | `total=5` |
| `1 2 3 4` | `total=10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER valores ; total <- suma ; ESCRIBIR total
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"total={sum(nums)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`total=${nums.reduce((a, b) => a + b, 0)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`total=${nums.reduce((a, b) => a + b, 0)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long total = 0;
        for (String s : p) total += Integer.parseInt(s);
        System.out.println("total=" + total);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

long total = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"total={total}");
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
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		total += n
	}
	fmt.Printf("total=%d\n", total)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let total: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("total={total}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long total = 0, x;
    while (scanf("%ld", &x) == 1) total += x;
    printf("total=%ld\n", total);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: agregacion declarativa con SUM.
WITH datos(x) AS (VALUES (10), (20), (30))
SELECT printf('total=%d', sum(x)) AS resultado FROM datos;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "total=" . array_sum($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Suma en el núcleo; SUM en SQL. |
| Semántica | La agregación resume el conjunto. |
| Paradigmática | SQL es declarativo: SELECT SUM(x). |

## 🧬 El concepto en la familia

Bases de datos relacionales (PostgreSQL, SQLite) y sus consultas SQL dominan este componente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 170
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Agregar en el backend lo que la BD hace mejor** → causa: traer todos los datos → solución: delegar la agregación a la base de datos
- **Consultas sin índices** → causa: lentitud → solución: indexar las columnas de filtrado/orden

## ❓ Preguntas frecuentes

- **¿Agregar en la BD o en el backend?** En la BD: es más eficiente y evita mover datos.
- **¿Por qué SQL para datos?** Es declarativo y el motor optimiza las consultas.

## 🔗 Referencias

**Libros de la parte:**

- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- M. Nygard — *Release It!* (2ª ed., Pragmatic Bookshelf).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

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

> [⏮️ Clase 169](../../parte-11-proyecto-integrador-poliglota/169-componente-web-frontend-js-ts/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 171 ⏭️](../../parte-11-proyecto-integrador-poliglota/171-componente-de-automatizacion-scripting/README.md)
