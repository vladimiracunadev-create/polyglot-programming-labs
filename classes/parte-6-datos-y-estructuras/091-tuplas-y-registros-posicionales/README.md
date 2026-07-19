# Clase 091 — Tuplas y registros posicionales

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **tuplas**: agrupar un número fijo de valores, posiblemente de tipos distintos, sin definir una clase. Se accede por posición y se desestructuran fácilmente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear y desestructurar una tupla.
2. Acceder a los componentes por posición.
3. Distinguir tupla de lista.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tupla | Grupo fijo y ordenado |
| 2 | Componentes | Acceso por posición |
| 3 | Desestructuración | Repartir en variables |

## 📖 Definiciones y características

- **Tupla** — grupo ordenado de valores de tamaño fijo. Clave: liviana, sin definir un tipo.
- **Componente** — cada elemento de la tupla, por posición. Clave: `.0`, `[0]`.
- **Registro posicional** — estructura cuyos campos se identifican por orden. Clave: la tupla lo es.

## 🧩 Situación

Devolver coordenadas `(x, y)`, un par clave/valor, o un resultado con dos partes: la tupla agrupa sin la ceremonia de una clase.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `tupla=(<b>, <a>)` (componentes intercambiados)
- **Regla:** (a, b) → (b, a)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `tupla=(4, 3)` |
| `0 -2` | `tupla=(-2, 0)` |
| `5 5` | `tupla=(5, 5)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER (a, b) ; intercambiar ; ESCRIBIR (b, a)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
t = (a, b)
t = (t[1], t[0])
print(f"tupla=({t[0]}, {t[1]})")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t: [number, number] = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Par(int a, int b) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Par t = new Par(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        Par s = new Par(t.b(), t.a());
        System.out.println("tupla=(" + s.a() + ", " + s.b() + ")");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
(int a, int b) t = (int.Parse(p[0]), int.Parse(p[1]));
t = (t.b, t.a);
Console.WriteLine($"tupla=({t.a}, {t.b})");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	a, b = b, a
	fmt.Printf("tupla=(%d, %d)\n", a, b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let t: (i64, i64) = (v[0], v[1]);
    let t = (t.1, t.0);
    println!("tupla=({}, {})", t.0, t.1);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene tuplas: se usa una struct. */
    struct Par { long a, b; } t = { b, a };
    printf("tupla=(%ld, %ld)\n", t.a, t.b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una fila con varias columnas es una tupla.
WITH pares(a, b) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('tupla=(%d, %d)', b, a) AS resultado FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$t = [(int) $b, (int) $a];
echo "tupla=({$t[0]}, {$t[1]})\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(a, b)` (Python/Rust/Go pares), arreglo (JS), record (Java). |
| Semántica | Rust/Python tienen tuplas nativas; Java usa records/objetos. |
| Paradigmática | SQL: una fila con varias columnas es una tupla. |

## 🧬 El concepto en la familia

En Ruby `[a, b]` funciona como tupla. En Haskell `(a, b)` es una tupla nativa con `fst`/`snd`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 091
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir tupla con lista** → causa: esperar que crezca → solución: la tupla tiene tamaño fijo
- **Acceder a un índice inexistente** → causa: error de posición → solución: respetar el número de componentes

## ❓ Preguntas frecuentes

- **¿Tupla o clase?** Tupla para agrupaciones pequeñas y anónimas; clase cuando los campos merecen nombre.
- **¿Las tuplas son inmutables?** En muchos lenguajes sí (Python, Rust): no se cambian tras crearlas.

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

> [⏮️ Clase 090](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 092 ⏭️](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md)
