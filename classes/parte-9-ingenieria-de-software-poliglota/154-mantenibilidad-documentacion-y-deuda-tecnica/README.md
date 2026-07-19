# Clase 154 — Mantenibilidad, documentación y deuda técnica

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la **mantenibilidad, la documentación y la deuda técnica**: medir la complejidad ayuda a mantener el código sano. Contar los módulos es una métrica básica; la deuda técnica crece cuando se ignora.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una métrica simple de estructura.
2. Explicar la deuda técnica.
3. Reconocer el valor de la documentación.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mantenibilidad | Facilidad de cambiar el código |
| 2 | Deuda técnica | El coste de los atajos |
| 3 | Métricas | Medir para gestionar |

## 📖 Definiciones y características

- **Mantenibilidad** — facilidad con que el código se entiende y modifica. Clave: reduce el coste futuro.
- **Deuda técnica** — coste acumulado de decisiones rápidas que habrá que pagar. Clave: crece si se ignora.
- **Documentación** — explicar el porqué del código. Clave: baja la barrera para mantenerlo.

## 🧩 Situación

Un sistema con muchos módulos poco documentados acumula deuda técnica: cada cambio cuesta más. Medir su estructura y documentar el porqué mantiene el proyecto sano a largo plazo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de módulos (palabras separadas por espacio)
- **Salida** (stdout): `complejidad=<número de módulos>`
- **Regla:** contar los módulos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `a b c` | `complejidad=3` |
| `x` | `complejidad=1` |
| `a b c d e` | `complejidad=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER módulos ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

mods = sys.stdin.read().split()
print(f"complejidad={len(mods)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const mods = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const mods: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] mods = br.readLine().trim().split("\\s+");
        System.out.println("complejidad=" + mods.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] mods = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"complejidad={mods.Length}");
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
	mods := strings.Fields(line)
	fmt.Printf("complejidad=%d\n", len(mods))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("complejidad={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("complejidad=%d\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: cuenta las filas (módulos).
WITH mods(nombre) AS (VALUES ('a'), ('b'), ('c'))
SELECT printf('complejidad=%d', count(*)) AS resultado FROM mods;
```

### PHP · `php main.php`

```php
<?php
$mods = preg_split('/\s+/', trim(fgets(STDIN)));
echo "complejidad=" . count($mods) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | La métrica estima la complejidad estructural. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

SonarQube y linters miden complejidad ciclomática, duplicación y deuda técnica automáticamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 154
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar la deuda técnica** → causa: el código se vuelve inmantenible → solución: pagarla en pequeñas dosis continuas
- **Documentar el qué en vez del porqué** → causa: comentarios redundantes → solución: explicar las decisiones, no repetir el código

## ❓ Preguntas frecuentes

- **¿Deuda técnica es siempre mala?** No: a veces es un préstamo consciente; el problema es no pagarla.
- **¿Qué documentar?** El porqué de las decisiones; el qué suele leerse en el código.

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

> [⏮️ Clase 153](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 155 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md)
