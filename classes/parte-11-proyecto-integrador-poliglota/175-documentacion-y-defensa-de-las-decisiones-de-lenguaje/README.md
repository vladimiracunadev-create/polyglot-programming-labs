# Clase 175 — Documentación y defensa de las decisiones de lenguaje

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Realizar la **documentación y la defensa de las decisiones de lenguaje**: explicar por qué cada componente usa su lenguaje y cómo encajan. Aquí se mide la documentación por su número de secciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Medir la cobertura de la documentación.
2. Explicar por qué documentar las decisiones.
3. Reconocer qué documentar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Documentación | Explicar el porqué |
| 2 | Defensa de decisiones | Justificar cada lenguaje |
| 3 | Secciones | Cobertura del documento |

## 📖 Definiciones y características

- **Documentación** — explicación escrita del sistema y sus decisiones. Clave: el porqué, no solo el qué.
- **Defensa de decisiones** — justificar por qué cada componente usa su lenguaje. Clave: hace revisables las elecciones.
- **Cobertura** — cuánto del sistema está documentado. Clave: una métrica de calidad.

## 🧩 Situación

Al cerrar el proyecto, se documenta: por qué Rust en el núcleo, TypeScript en el frontend, SQL en los datos, y cómo se comunican. Esa defensa razonada es lo que distingue una decisión de ingeniería de un capricho.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de secciones documentadas)
- **Salida** (stdout): `documentado=<n> secciones`
- **Regla:** informar el número de secciones

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `documentado=5 secciones` |
| `1` | `documentado=1 secciones` |
| `8` | `documentado=8 secciones` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR documentado=n secciones
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"documentado={n} secciones")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`documentado=${n} secciones`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`documentado=${n} secciones`);
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
        System.out.println("documentado=" + n + " secciones");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"documentado={n} secciones");
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
	fmt.Printf("documentado=%d secciones\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("documentado={n} secciones");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("documentado=%ld secciones\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL se documenta con comentarios; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('documentado=%d secciones', n) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "documentado=$n secciones\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | La documentación explica el porqué de las decisiones. |
| Paradigmática | SQL se documenta con comentarios y vistas. |

## 🧬 El concepto en la familia

Markdown, docstrings, ADR (Architecture Decision Records) documentan sistemas y decisiones.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 175
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Documentar el qué en vez del porqué** → causa: comentarios redundantes → solución: explicar las decisiones y sus razones
- **Documentación desactualizada** → causa: engaña más que ayuda → solución: mantenerla junto al código

## ❓ Preguntas frecuentes

- **¿Qué documentar?** Las decisiones y el porqué; el qué suele leerse en el código.
- **¿Qué es un ADR?** Un registro breve de una decisión de arquitectura y su justificación.

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

> [⏮️ Clase 174](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 176 ⏭️](../../parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)
