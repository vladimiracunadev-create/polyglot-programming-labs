# Clase 155 — Por qué los sistemas reales son políglotas

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **por qué los sistemas reales son políglotas**: cada componente usa el lenguaje que mejor le sirve. Contar los componentes es la medida básica de un sistema hecho de piezas heterogéneas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar los componentes de un sistema.
2. Explicar por qué se combinan lenguajes.
3. Reconocer sistemas políglotas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema políglota | Varios lenguajes, un sistema |
| 2 | Componente | Una pieza con su lenguaje |
| 3 | Elegir por tarea | El mejor lenguaje para cada parte |

## 📖 Definiciones y características

- **Sistema políglota** — software compuesto por partes en distintos lenguajes. Clave: es lo normal en producción.
- **Componente** — pieza con una responsabilidad y su propio lenguaje. Clave: se integra con las demás.
- **Frontera** — el punto donde dos componentes se comunican. Clave: necesita un contrato claro.

## 🧩 Situación

Un producto real puede tener el frontend en TypeScript, el backend en Go, el núcleo numérico en Rust y los datos en SQL. Contar los componentes empieza a describir esa realidad políglota.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<cantidad>`
- **Regla:** contar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3` |
| `app` | `componentes=1` |
| `web api datos cache` | `componentes=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

comps = sys.stdin.read().split()
print(f"componentes={len(comps)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const comps = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${comps.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const comps: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${comps.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] comps = br.readLine().trim().split("\\s+");
        System.out.println("componentes=" + comps.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] comps = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"componentes={comps.Length}");
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
	comps := strings.Fields(line)
	fmt.Printf("componentes=%d\n", len(comps))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    println!("componentes={}", s.split_whitespace().count());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char t[256];
    int c = 0;
    while (scanf("%255s", t) == 1) c++;
    printf("componentes=%d\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL cuenta las filas (componentes).
WITH comps(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d', count(*)) AS resultado FROM comps;
```

### PHP · `php main.php`

```php
<?php
$comps = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($comps) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | Cada componente puede estar en otro lenguaje. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Casi todo sistema grande es políglota: se elige el lenguaje por componente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 155
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Un solo lenguaje para todo por dogma** → causa: usar la herramienta equivocada → solución: elegir por la tarea de cada componente
- **Fronteras sin contrato** → causa: integraciones frágiles → solución: definir contratos claros entre componentes

## ❓ Preguntas frecuentes

- **¿Por qué no un solo lenguaje?** Cada uno destaca en cosas distintas; combinarlos aprovecha lo mejor de cada uno.
- **¿No complica el mantenimiento?** Algo, pero contratos claros lo controlan; la ventaja suele compensar.

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

> [⏮️ Clase 154](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 156 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md)
