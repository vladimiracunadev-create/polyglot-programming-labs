# Clase 164 — Elegir el lenguaje correcto para cada componente

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la decisión clave del enfoque políglota: **elegir el lenguaje correcto para cada componente**. Según la naturaleza del componente (sistemas, web, datos), un lenguaje encaja mejor que otro.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Asociar un tipo de componente con un lenguaje.
2. Justificar la elección por la tarea.
3. Aplicar el criterio a un sistema real.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Elegir por componente | El mejor lenguaje para cada parte |
| 2 | Fortalezas | Qué destaca cada lenguaje |
| 3 | Sistema políglota | Varias elecciones coherentes |

## 📖 Definiciones y características

- **Idoneidad** — cuánto encaja un lenguaje con una tarea. Clave: rendimiento, ecosistema, plataforma.
- **Componente de sistemas** — cercano al hardware o de alto rendimiento. Clave: Rust/C encajan.
- **Componente web/datos** — interfaz interactiva o consulta de datos. Clave: TypeScript/SQL encajan.

## 🧩 Situación

Para un núcleo de rendimiento eliges Rust; para el frontend, TypeScript; para las consultas, SQL. Elegir por componente es lo que hace de un sistema políglota una decisión de ingeniería, no un capricho.

## 🧮 Modelo

- **Entrada** (stdin): una palabra: `sistemas`, `web` o `datos`
- **Salida** (stdout): `lenguaje=<Rust|TypeScript|SQL>`
- **Regla:** sistemas→Rust, web→TypeScript, datos→SQL

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `sistemas` | `lenguaje=Rust` |
| `web` | `lenguaje=TypeScript` |
| `datos` | `lenguaje=SQL` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo ; SEGUN tipo: recomendar lenguaje
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

tipo = sys.stdin.readline().strip()
rec = {"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
print(f"lenguaje={rec.get(tipo, 'Python')}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const tipo = readFileSync(0, "utf8").trim();
const rec = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const tipo: string = readFileSync(0, "utf8").trim();
const rec: Record<string, string> = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String tipo = br.readLine().trim();
        String r;
        switch (tipo) {
            case "sistemas": r = "Rust"; break;
            case "web": r = "TypeScript"; break;
            case "datos": r = "SQL"; break;
            default: r = "Python";
        }
        System.out.println("lenguaje=" + r);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string tipo = Console.In.ReadToEnd().Trim();
string r = tipo switch {
    "sistemas" => "Rust",
    "web" => "TypeScript",
    "datos" => "SQL",
    _ => "Python",
};
Console.WriteLine($"lenguaje={r}");
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
	tipo := strings.TrimSpace(line)
	rec := map[string]string{"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
	r, ok := rec[tipo]
	if !ok {
		r = "Python"
	}
	fmt.Printf("lenguaje=%s\n", r)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let tipo = s.trim();
    let r = match tipo {
        "sistemas" => "Rust",
        "web" => "TypeScript",
        "datos" => "SQL",
        _ => "Python",
    };
    println!("lenguaje={r}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    const char *r;
    if (strcmp(tipo, "sistemas") == 0) r = "Rust";
    else if (strcmp(tipo, "web") == 0) r = "TypeScript";
    else if (strcmp(tipo, "datos") == 0) r = "SQL";
    else r = "Python";
    printf("lenguaje=%s\n", r);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL recomienda con CASE.
WITH t(tipo) AS (VALUES ('sistemas'))
SELECT printf('lenguaje=%s', CASE tipo WHEN 'sistemas' THEN 'Rust' WHEN 'web' THEN 'TypeScript' WHEN 'datos' THEN 'SQL' ELSE 'Python' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$tipo = trim(fgets(STDIN));
$rec = ["sistemas" => "Rust", "web" => "TypeScript", "datos" => "SQL"];
echo "lenguaje=" . ($rec[$tipo] ?? "Python") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | switch/match/lookup en cada lenguaje. |
| Semántica | La recomendación se basa en las fortalezas de cada lenguaje. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

La elección por componente es la esencia del programa: cada lenguaje del núcleo brilla en su terreno.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 164
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Elegir por moda** → causa: usar la herramienta equivocada → solución: elegir por la tarea y el contexto
- **Un solo lenguaje para todo** → causa: forzar la uniformidad → solución: aceptar que lo políglota suele ser mejor

## ❓ Preguntas frecuentes

- **¿Y si el equipo solo sabe un lenguaje?** El talento disponible es un criterio legítimo y a menudo decisivo.
- **¿No es más simple un solo lenguaje?** A veces; pero elegir por componente aprovecha lo mejor de cada uno.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly).
- S. Newman — *Building Microservices* (2ª ed., O'Reilly).
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.).

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

> [⏮️ Clase 163](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 165 ⏭️](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md)
