# Clase 142 — Registro (logging) y observabilidad

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **registro (logging) y la observabilidad**: dejar rastros de lo que hace el programa para poder diagnosticarlo en producción, donde no hay depurador. Un log con nivel y datos es la unidad básica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Emitir un registro con nivel.
2. Explicar la observabilidad.
3. Distinguir niveles de log.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Logging | Dejar rastros de la ejecución |
| 2 | Nivel | INFO, WARN, ERROR |
| 3 | Observabilidad | Entender el sistema desde fuera |

## 📖 Definiciones y características

- **Log** — mensaje que registra un evento del programa. Clave: diagnóstico en producción.
- **Nivel de log** — gravedad del mensaje (DEBUG, INFO, WARN, ERROR). Clave: filtrar el ruido.
- **Observabilidad** — capacidad de entender el estado interno desde las salidas (logs, métricas, trazas). Clave: operar en producción.

## 🧩 Situación

En producción no puedes pausar el programa; te guías por los logs. Un registro estructurado ('[INFO] procesados=5') permite saber qué pasó sin estar delante.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (elementos procesados)
- **Salida** (stdout): `log=[INFO] procesados=<n>`
- **Regla:** emitir un registro de nivel INFO con el conteo

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `log=[INFO] procesados=5` |
| `0` | `log=[INFO] procesados=0` |
| `3` | `log=[INFO] procesados=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR log de nivel INFO con procesados=n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"log=[INFO] procesados={n}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`log=[INFO] procesados=${n}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("log=[INFO] procesados=" + n);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"log=[INFO] procesados={n}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("log=[INFO] procesados=%d\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("log=[INFO] procesados={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("log=[INFO] procesados=%ld\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: registro con una tabla/consulta de auditoría.
WITH t(n) AS (VALUES (5))
SELECT printf('log=[INFO] procesados=%d', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "log=[INFO] procesados=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | logging (Python), console/log4j (JS/Java), slog (Go). |
| Semántica | El nivel permite filtrar; el formato estructurado facilita el análisis. |
| Paradigmática | SQL registra con tablas de auditoría. |

## 🧬 El concepto en la familia

log4j/SLF4J (Java), logging (Python), Serilog (.NET), zap/slog (Go): mismo concepto de niveles.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 142
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Loggear demasiado** → causa: ruido que oculta lo importante → solución: usar niveles y registrar lo relevante
- **Loggear datos sensibles** → causa: fuga de información → solución: no registrar contraseñas ni datos personales

## ❓ Preguntas frecuentes

- **¿Log o depurador?** El depurador para desarrollo; el log para producción.
- **¿Qué es observabilidad?** Logs, métricas y trazas que permiten entender el sistema en marcha.

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

> [⏮️ Clase 141](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 143 ⏭️](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md)
