# Clase 148 — Entrega y despliegue

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **entrega y el despliegue**: llevar el artefacto probado a producción. Etiquetar la versión (p. ej. `v1.2.3`) es parte de una entrega ordenada y trazable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Etiquetar una versión para desplegar.
2. Explicar entrega vs. despliegue.
3. Reconocer el valor de la trazabilidad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrega | Preparar para publicar |
| 2 | Despliegue | Poner en producción |
| 3 | Etiqueta de versión | Trazabilidad |

## 📖 Definiciones y características

- **Entrega continua** — mantener el software siempre listo para desplegar. Clave: releases frecuentes y seguras.
- **Despliegue** — poner una versión en producción. Clave: puede ser manual o automático (CD).
- **Etiqueta (tag)** — marca de una versión en el historial (v1.2.3). Clave: trazabilidad.

## 🧩 Situación

Tras pasar el CI, se etiqueta la versión (`v1.2.3`) y se despliega. La etiqueta permite saber exactamente qué código está en producción y volver atrás si hace falta.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `desplegado=v<versión>`
- **Regla:** prefijar la versión con 'v'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `desplegado=v1.2.3` |
| `0.9.0` | `desplegado=v0.9.0` |
| `2.1.5` | `desplegado=v2.1.5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; ESCRIBIR 'desplegado=v' + version
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

version = sys.stdin.readline().strip()
print(f"desplegado=v{version}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String version = br.readLine().trim();
        System.out.println("desplegado=v" + version);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string version = Console.In.ReadToEnd().Trim();
Console.WriteLine($"desplegado=v{version}");
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
	version := strings.TrimSpace(line)
	fmt.Printf("desplegado=v%s\n", version)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let version = s.trim();
    println!("desplegado=v{version}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("desplegado=v%s\n", version);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: concatena el prefijo con ||.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'desplegado=v' || v AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$version = trim(fgets(STDIN));
echo "desplegado=v$version\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Concatenación en cada lenguaje. |
| Semántica | La etiqueta identifica la versión desplegada. |
| Paradigmática | SQL concatena con \|\|. |

## 🧬 El concepto en la familia

Git tags, releases de GitHub, y las herramientas de CD (Argo, Spinnaker) gestionan despliegues versionados.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 148
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desplegar sin etiquetar** → causa: no saber qué hay en producción → solución: etiquetar cada release
- **Desplegar sin pasar el CI** → causa: romper producción → solución: desplegar solo lo que está verde

## ❓ Preguntas frecuentes

- **¿Entrega o despliegue continuo?** Entrega deja el software listo; despliegue continuo lo publica automáticamente.
- **¿Por qué el prefijo 'v'?** Convención común para distinguir etiquetas de versión.

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

> [⏮️ Clase 147](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 149 ⏭️](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md)
