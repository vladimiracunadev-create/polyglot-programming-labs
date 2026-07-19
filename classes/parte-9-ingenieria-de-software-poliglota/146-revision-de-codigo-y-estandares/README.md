# Clase 146 — Revisión de código y estándares

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar la **revisión de código y los estándares**: un linter comprueba automáticamente convenciones (nombres, formato). Aquí se valida que un identificador esté en minúsculas, como haría una regla de estilo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Validar una convención de nombres.
2. Explicar el papel del linter.
3. Reconocer el valor de los estándares.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estándar de estilo | Reglas compartidas |
| 2 | Linter | Verifica automáticamente |
| 3 | Revisión de código | Segundo par de ojos |

## 📖 Definiciones y características

- **Estándar de código** — convenciones acordadas (nombres, formato). Clave: consistencia en el equipo.
- **Linter** — herramienta que detecta violaciones de estilo y errores probables. Clave: automatiza la revisión.
- **Revisión de código** — otra persona revisa el cambio antes de integrarlo. Clave: calidad y difusión de conocimiento.

## 🧩 Situación

En muchos proyectos, los identificadores van en minúsculas. Un linter marca 'Total' como violación. Automatizar estas reglas evita discusiones y mantiene el código uniforme.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (identificador, solo letras)
- **Salida** (stdout): `valido=<true|false>` (true si está todo en minúsculas)
- **Regla:** valido si todos los caracteres son minúsculas

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `total` | `valido=true` |
| `Total` | `valido=false` |
| `abc` | `valido=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER palabra ; valido <- todos los caracteres en minúscula
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
valido = all("a" <= c <= "z" for c in w)
print(f"valido={'true' if valido else 'false'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        boolean valido = w.matches("[a-z]+");
        System.out.println("valido=" + (valido ? "true" : "false"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool valido = w.Length > 0 && w.All(c => c >= 'a' && c <= 'z');
Console.WriteLine($"valido={(valido ? "true" : "false")}");
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
	w := strings.TrimSpace(line)
	valido := len(w) > 0
	for _, c := range w {
		if c < 'a' || c > 'z' {
			valido = false
		}
	}
	res := "false"
	if valido {
		res = "true"
	}
	fmt.Printf("valido=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let valido = !w.is_empty() && w.chars().all(|c| c.is_ascii_lowercase());
    println!("valido={}", if valido { "true" } else { "false" });
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int valido = 1;
    for (int i = 0; w[i]; i++) {
        if (w[i] < 'a' || w[i] > 'z') valido = 0;
    }
    printf("valido=%s\n", valido ? "true" : "false");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara con la versión en minúsculas.
WITH t(w) AS (VALUES ('total'))
SELECT printf('valido=%s', CASE WHEN w = lower(w) THEN 'true' ELSE 'false' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
$valido = preg_match('/^[a-z]+$/', $w) === 1;
echo "valido=" . ($valido ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | islower/comparación de caracteres en cada lenguaje. |
| Semántica | La regla se comprueba carácter a carácter. |
| Paradigmática | SQL compara con lower(). |

## 🧬 El concepto en la familia

ESLint, Ruff, Clippy, gofmt/govet aplican reglas de estilo automáticamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 146
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Reglas de estilo manuales** → causa: inconsistencia → solución: delegar en el linter
- **Ignorar los avisos del linter** → causa: bugs latentes → solución: resolverlos o justificarlos

## ❓ Preguntas frecuentes

- **¿Linter o revisión humana?** Ambos: el linter automatiza lo mecánico; la revisión, el criterio.
- **¿Por qué estándares?** Un código uniforme se lee y mantiene mejor.

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

> [⏮️ Clase 145](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 147 ⏭️](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md)
