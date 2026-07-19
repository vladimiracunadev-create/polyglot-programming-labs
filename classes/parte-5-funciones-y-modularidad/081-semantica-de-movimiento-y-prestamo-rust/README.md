# Clase 081 — Semántica de movimiento y préstamo (Rust)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **semántica de movimiento y préstamo** de Rust: un valor tiene un dueño; se puede **prestar** (borrow) para leerlo sin copiar, o **mover** (move) transfiriendo la propiedad. Otros lenguajes copian o comparten referencias con GC.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar propiedad, préstamo y movimiento.
2. Leer un valor prestado sin copiarlo.
3. Comparar el modelo de Rust con el de los lenguajes con GC.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Propiedad (ownership) | Cada valor tiene un dueño |
| 2 | Préstamo (borrow) | Usar sin poseer |
| 3 | Movimiento (move) | Transferir la propiedad |
| 4 | Alternativas | Copia o GC en otros lenguajes |

## 📖 Definiciones y características

- **Propiedad** — cada valor tiene un único dueño responsable de liberarlo. Clave: base de la seguridad de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.
- **Movimiento** — transferir la propiedad a otra variable. Clave: la original deja de ser válida.
- **Copia vs. GC** — otros lenguajes copian o rastrean referencias con recolector. Clave: modelo distinto.

## 🧩 Situación

En Rust, medir la longitud del texto lo **presta** (`&s`); luego imprimirlo lo **mueve**. El compilador garantiza que nadie use un valor movido. Otros lenguajes lo resuelven con GC o copiando.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII)
- **Salida** (stdout): `movido=<palabra> longitud=<len>`
- **Regla:** longitud por préstamo; el texto se muestra tras moverse

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `movido=Ada longitud=3` |
| `Bo` | `movido=Bo longitud=2` |
| `hola` | `movido=hola longitud=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; len <- longitud(prestar w)
mostrar(mover w)
ESCRIBIR "movido=" w " longitud=" len
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

s = sys.stdin.readline().strip()
longitud = len(s)  # Python comparte la referencia (GC), no hay 'move'.
print(f"movido={s} longitud={longitud}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const s = readFileSync(0, "utf8").trim();
const longitud = s.length; // JS usa GC: la cadena sigue disponible.
console.log(`movido=${s} longitud=${longitud}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const s: string = readFileSync(0, "utf8").trim();
const longitud: number = s.length;
console.log(`movido=${s} longitud=${longitud}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine().trim();
        int longitud = s.length(); // GC: sin propiedad ni move.
        System.out.println("movido=" + s + " longitud=" + longitud);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string s = Console.In.ReadToEnd().Trim();
int longitud = s.Length; // GC: la cadena permanece.
Console.WriteLine($"movido={s} longitud={longitud}");
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
	s := strings.TrimSpace(line)
	longitud := len(s) // GC: sin propiedad explícita.
	fmt.Printf("movido=%s longitud=%d\n", s, longitud)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn longitud(s: &str) -> usize {
    s.len() // préstamo: se lee sin tomar la propiedad
}

fn mostrar(s: String) {
    // move: 'mostrar' se vuelve dueña de la cadena
    let len = s.len();
    println!("movido={s} longitud={len}");
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).unwrap();
    let s = buf.trim().to_string();
    let _ = longitud(&s); // se presta
    mostrar(s); // se mueve
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[256];
    if (scanf("%255s", s) != 1) return 1;
    /* C: gestión manual; aquí no se copia ni se mueve, se usa directamente. */
    int longitud = (int) strlen(s);
    printf("movido=%s longitud=%d\n", s, longitud);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene propiedad de memoria: opera sobre datos.
WITH palabras(s) AS (VALUES ('Ada'), ('Bo'), ('hola'))
SELECT printf('movido=%s longitud=%d', s, length(s)) AS resultado FROM palabras;
```

### PHP · `php main.php`

```php
<?php
$s = trim(fgets(STDIN));
$longitud = strlen($s); // PHP usa GC por conteo de referencias.
echo "movido=$s longitud=$longitud\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `&s` (préstamo) y move implícito en Rust; los demás copian o comparten referencia. |
| Semántica | Rust invalida el valor movido en compilación; con GC el valor sigue vivo mientras se use. |
| Paradigmática | SQL no tiene propiedad de memoria: opera sobre datos. |

## 🧬 El concepto en la familia

C++ tiene semántica de movimiento (`std::move`) y referencias, cercana a Rust pero sin comprobación en compilación. Java/Go/Python usan GC.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 081
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor tras moverlo (Rust)** → causa: el compilador lo rechaza → solución: prestar (`&`) si necesitas seguir usándolo
- **Asumir move en lenguajes con GC** → causa: allí no existe → solución: recordar que el GC mantiene el valor vivo mientras haya referencias

## ❓ Preguntas frecuentes

- **¿Por qué Rust mueve?** Para garantizar un único dueño y liberar memoria sin GC ni errores de uso tras liberar.
- **¿Prestar copia?** No: un préstamo es una referencia; no duplica el dato.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 080](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 082 ⏭️](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md)
