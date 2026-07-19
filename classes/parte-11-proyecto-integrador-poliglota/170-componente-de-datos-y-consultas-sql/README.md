# Clase 170 — Componente de datos y consultas (SQL)

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construimos el **componente de datos**: la capa que almacena la información y responde consultas. Es la
**fuente de verdad** del sistema, y su lenguaje natural es SQL. Hoy implementamos la operación que mejor lo
caracteriza: la **agregación**, resumir muchos valores en uno (aquí, sumarlos), como hace un `SELECT
SUM(...)` sobre miles de filas.

Este componente encierra la diferencia paradigmática más profunda de todo el curso, y por eso merece
atención. Los otros nueve lenguajes del núcleo son **imperativos**: le dices a la máquina *cómo* hacer las
cosas, paso a paso. SQL es **declarativo**: describes *qué* quieres y el motor decide cómo obtenerlo. C. J.
Date, en *SQL and Relational Theory*, insiste en que esta no es una comodidad sintáctica sino un cambio de
modelo mental heredado del álgebra relacional: piensas en conjuntos, no en bucles. Entender la capa de
datos es entender que a veces el mejor código es el que **no** escribes, porque delegas el "cómo" a un motor
que optimiza mejor que tú.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Agregar un conjunto de datos resumiéndolo en un valor.
2. Explicar por qué la capa de datos es la fuente de verdad y por qué conviene delegarle la agregación.
3. Reconocer SQL como lenguaje declarativo y su contraste con los nueve imperativos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Capa de datos | Persiste y consulta: fuente de verdad |
| 2 | Agregación | Resume muchas filas en un valor |
| 3 | Consulta declarativa | Describes el qué; el motor resuelve el cómo |

## 📖 Definiciones y características

El **componente de datos** es la capa que almacena y consulta la información; es la fuente de verdad del
sistema, donde vive el estado que debe sobrevivir a todo lo demás. La **agregación** combina muchas filas en
un solo valor (`SUM`, `AVG`, `COUNT`): es el resumen de datos por excelencia. Una **consulta declarativa**
describe qué datos se quieren, no cómo obtenerlos, y es el rasgo distintivo de SQL.

La consecuencia práctica del modelo declarativo es enorme. Cuando escribes `SELECT SUM(x) FROM ventas`, no
dices "abre un cursor, recorre las filas, acumula": dices "quiero la suma", y el motor elige el plan de
ejecución —usar un índice, paralelizar, ordenar por lotes— según los datos que tenga. Newman, al hablar de
la propiedad de los datos en *Building Microservices*, subraya que cada servicio debe ser dueño de su
almacén y exponerlo solo por su API; la capa de datos no es un cajón compartido sino un componente con
fronteras, y SQL es cómo se le pregunta. Delegar la agregación a la base de datos —en vez de traer todas
las filas al backend y sumarlas allí— es una de las decisiones de rendimiento más rentables que existen.

## 🧩 Situación

El backend necesita "el total de ventas del mes". Tiene dos caminos. El malo: pedir a la base de datos las
cien mil filas, traerlas por la red al servicio y sumarlas en un bucle. El bueno: enviar `SELECT SUM(monto)
FROM ventas WHERE mes = ?` y recibir un solo número. El segundo mueve el cálculo a donde están los datos,
aprovecha los índices y transfiere un entero en vez de un torrente de filas. SQL es el lenguaje natural de
este componente precisamente porque fue diseñado para expresar ese "resume allí donde viven los datos" en
una línea declarativa.

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

## 🧪 Recorrido del código

El contrato ([`casos.json`](casos.json)) es una suma: de `10 20 30` sale `total=60`; de `5`, `total=5`.
Trivial en aritmética, pero es el caso perfecto para **ver** la frontera imperativo/declarativo, porque un
lenguaje la expresa de forma radicalmente distinta a los demás.

Los nueve imperativos recorren y acumulan, con más o menos azúcar. **Python** lo hace casi declarativo:

```python
nums = [int(x) for x in sys.stdin.read().split()]
print(f"total={sum(nums)}")
```

La comprensión de lista convierte los tokens en enteros y `sum()` los reduce. No ves el bucle, pero está
ahí: `sum` itera. **C** enseña ese bucle sin adornos —`while (scanf("%ld", &x) == 1) total += x;`—: lee un
número, lo suma, repite. Entre ambos, **Go** y **Java** escriben el `for` explícito acumulando en una
variable. Todos comparten el mismo modelo mental: "empieza en cero, recorre, acumula".

**SQL** rompe ese molde:

```sql
WITH datos(x) AS (VALUES (10), (20), (30))
SELECT printf('total=%d', sum(x)) AS resultado FROM datos;
```

Aquí no hay variable acumuladora, ni bucle, ni orden. `sum(x)` es una función de agregación que opera sobre
**todo el conjunto** `datos` a la vez; tú declaras "quiero la suma de la columna x" y el motor decide cómo
recorrerla. No lee de stdin como los otros —su entrada es la tabla—, por eso el verificador la marca como
*ilustrativa*. Esa es la lección de Date hecha código: nueve lenguajes te dan el "cómo" de la suma; SQL te
da solo el "qué", y ese salto es la diferencia paradigmática que este componente encarna.

## 🔬 Comparación

Sumar un conjunto es donde la distancia entre "decir cómo" y "decir qué" se ve con más claridad.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `sum()` (Python), `reduce` (JS), `.Sum()` (C#/LINQ), `for` (Go/Java), `while` (C): variaciones de acumular. |
| Semántica | Los imperativos mantienen una variable acumuladora y un orden de recorrido; SQL opera sobre el conjunto sin orden explícito. |
| Paradigmática | La diferencia central del curso: nueve lenguajes describen el **cómo** (recorrer y acumular); SQL declara el **qué** (`SELECT SUM(x)`) y delega el cómo al motor. |

Nota que C# con LINQ (`.Sum(x => ...)`) es un puente: trae el estilo declarativo al mundo imperativo. Ese
préstamo de ideas entre familias —tomar el "describe el qué" de SQL/funcional y llevarlo a C#— es la razón
por la que comparar lenguajes acelera el aprendizaje en vez de dispersarlo.

## 🧬 El concepto en la familia

Las bases de datos relacionales (PostgreSQL, SQLite, MySQL) y su SQL dominan este componente, pero la idea
de "agregación declarativa sobre un conjunto" reaparece en las *streams* de Java, LINQ en C#, `reduce` en
JS y las comprensiones de Python. Reconocer que todas son la misma operación —resumir una colección— es
transferir el concepto entre familias imperativa y declarativa.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 170
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Agregar en el backend lo que la BD hace mejor** → causa: traes todas las filas por la red y sumas en un bucle → solución: delegar la agregación a la base de datos con `SUM`/`AVG`/`GROUP BY`.
- **Consultas sin índices** → causa: el motor recorre toda la tabla en cada filtro → solución: indexar las columnas por las que filtras y ordenas.
- **Compartir la base de datos entre servicios** → causa: acoplamiento oculto por debajo de las APIs → solución: cada componente es dueño de su almacén y lo expone solo por su contrato (Newman).

## ❓ Preguntas frecuentes

- **¿Agregar en la BD o en el backend?** En la BD: mueve el cálculo a donde viven los datos, usa los índices y transfiere un valor en vez de miles de filas.
- **¿Por qué SQL para datos?** Porque es declarativo: describes el resultado y el motor elige el plan óptimo, algo casi imposible de igualar a mano.
- **¿El modelo declarativo aparece en otros lenguajes?** Sí: LINQ (C#), *streams* (Java), `reduce` (JS) y las comprensiones (Python) traen su espíritu al mundo imperativo.

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
