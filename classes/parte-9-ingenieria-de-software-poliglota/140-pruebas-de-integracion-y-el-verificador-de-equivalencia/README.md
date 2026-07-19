# Clase 140 — Pruebas de integración y el verificador de equivalencia

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender las **pruebas de integración** y el **verificador de equivalencia**: en vez de una unidad aislada, se comprueba que dos partes (o dos implementaciones) producen el mismo resultado. Es exactamente lo que hace el CI de este curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comparar dos salidas.
2. Explicar prueba de integración vs. unitaria.
3. Relacionarlo con el verificador del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Integración | Varias partes juntas |
| 2 | Equivalencia | Mismos resultados |
| 3 | Verificador | Compara implementaciones |

## 📖 Definiciones y características

- **Prueba de integración** — verifica que varias partes funcionan juntas. Clave: más allá de la unidad.
- **Equivalencia** — dos implementaciones dan el mismo resultado. Clave: base del verificador.
- **Regresión** — un cambio rompe algo que funcionaba. Clave: las pruebas la detectan.

## 🧩 Situación

El verificador de este curso comprueba que las 10 implementaciones de una clase dan la misma salida. Aquí, en pequeño, se comparan dos resultados y se declara si son equivalentes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `x y` (dos resultados a comparar)
- **Salida** (stdout): `equivalente=<true|false>`
- **Regla:** equivalente si x == y

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `6 6` | `equivalente=true` |
| `5 7` | `equivalente=false` |
| `0 0` | `equivalente=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER x, y ; ESCRIBIR equivalente=(x==y)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

x, y = sys.stdin.readline().split()
print(f"equivalente={'true' if x == y else 'false'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
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
        System.out.println("equivalente=" + (p[0].equals(p[1]) ? "true" : "false"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"equivalente={(p[0] == p[1] ? "true" : "false")}");
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
	res := "false"
	if f[0] == f[1] {
		res = "true"
	}
	fmt.Printf("equivalente=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("equivalente={res}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char x[64], y[64];
    if (scanf("%63s %63s", x, y) != 2) return 1;
    printf("equivalente=%s\n", strcmp(x, y) == 0 ? "true" : "false");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara dos valores.
WITH t(x, y) AS (VALUES (6, 6))
SELECT printf('equivalente=%s', CASE WHEN x = y THEN 'true' ELSE 'false' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "equivalente=" . ($x === $y ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Comparación de igualdad en cada lenguaje. |
| Semántica | Se compara la salida observable, no la implementación. |
| Paradigmática | SQL compara con =. |

## 🧬 El concepto en la familia

El patrón 'mismas entradas → misma salida' es universal en pruebas de equivalencia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 140
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comparar implementaciones en vez de salidas** → causa: acoplamiento a detalles → solución: comparar el resultado observable
- **No fijar el formato** → causa: diferencias espurias → solución: normalizar la salida antes de comparar

## ❓ Preguntas frecuentes

- **¿Unitaria o integración?** Unitaria prueba una función; integración, varias juntas.
- **¿Qué garantiza el verificador?** Que las implementaciones son equivalentes, no que la prosa sea correcta.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 139](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 141 ⏭️](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md)
