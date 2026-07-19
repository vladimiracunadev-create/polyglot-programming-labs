# Clase 145 — Git y control de versiones para proyectos políglotas

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir **Git y el control de versiones**: el historial es una secuencia de commits (instantáneas con mensaje). Contar los commits es la operación básica sobre ese historial.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar los commits de un historial.
2. Explicar qué es un commit.
3. Reconocer el valor del versionado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Commit | Instantánea con mensaje |
| 2 | Historial | Secuencia de commits |
| 3 | Ramas | Líneas de desarrollo |

## 📖 Definiciones y características

- **Git** — sistema de control de versiones distribuido. Clave: historial completo en cada copia.
- **Commit** — instantánea del proyecto con un mensaje. Clave: unidad del historial.
- **Rama** — línea de desarrollo paralela. Clave: trabajar sin pisar la principal.

## 🧩 Situación

Cada cambio importante se registra como un commit con su mensaje. El historial permite volver atrás, ver quién cambió qué y colaborar sin sobrescribir el trabajo ajeno.

## 🧮 Modelo

- **Entrada** (stdin): una línea con mensajes de commit (palabras separadas por espacio)
- **Salida** (stdout): `commits=<cantidad>`
- **Regla:** contar los mensajes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `fix add refactor` | `commits=3` |
| `init` | `commits=1` |
| `a b c d` | `commits=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER mensajes ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

msgs = sys.stdin.read().split()
print(f"commits={len(msgs)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const msgs = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const msgs: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] msgs = br.readLine().trim().split("\\s+");
        System.out.println("commits=" + msgs.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] msgs = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"commits={msgs.Length}");
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
	msgs := strings.Fields(line)
	fmt.Printf("commits=%d\n", len(msgs))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("commits={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("commits=%d\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: cuenta las filas (commits).
WITH commits(msg) AS (VALUES ('fix'), ('add'), ('refactor'))
SELECT printf('commits=%d', count(*)) AS resultado FROM commits;
```

### PHP · `php main.php`

```php
<?php
$msgs = preg_split('/\s+/', trim(fgets(STDIN)));
echo "commits=" . count($msgs) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | Cada commit es una instantánea inmutable. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Git es el estándar; Mercurial y otros comparten el modelo de instantáneas versionadas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 145
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Commits enormes y sin mensaje claro** → causa: historial ilegible → solución: commits pequeños con mensajes descriptivos
- **Commitear archivos generados** → causa: ruido en el repo → solución: usar .gitignore

## ❓ Preguntas frecuentes

- **¿Cada cuánto commitear?** Cuando tienes un cambio coherente y funcional.
- **¿Git es solo para código?** No: sirve para cualquier texto versionable (docs, configuración).

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

> [⏮️ Clase 144](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 146 ⏭️](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md)
