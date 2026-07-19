# Clase 149 — Diseño y arquitectura comparada

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **diseño y la arquitectura**: un sistema se organiza en capas o componentes con responsabilidades claras. Contar las capas es la medida más básica de su estructura.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar las capas de una arquitectura.
2. Explicar la separación de responsabilidades.
3. Reconocer estilos arquitectónicos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arquitectura | Estructura de alto nivel |
| 2 | Capa/componente | Responsabilidad definida |
| 3 | Separación de responsabilidades | Cada parte hace una cosa |

## 📖 Definiciones y características

- **Arquitectura** — estructura de alto nivel de un sistema y sus componentes. Clave: guía las decisiones grandes.
- **Capa** — grupo de componentes con una responsabilidad (presentación, lógica, datos). Clave: separa preocupaciones.
- **Acoplamiento** — grado de dependencia entre componentes. Clave: bajo acoplamiento facilita el cambio.

## 🧩 Situación

Un sistema típico tiene capas: web (interfaz), api (lógica), datos (persistencia). Nombrar y contar las capas es el primer paso para razonar sobre su arquitectura.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de capas (palabras separadas por espacio)
- **Salida** (stdout): `capas=<cantidad>`
- **Regla:** contar los nombres de capa

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `web api datos` | `capas=3` |
| `cli` | `capas=1` |
| `web api datos cache` | `capas=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER capas ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

capas = sys.stdin.read().split()
print(f"capas={len(capas)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const capas = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const capas: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] capas = br.readLine().trim().split("\\s+");
        System.out.println("capas=" + capas.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] capas = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"capas={capas.Length}");
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
	capas := strings.Fields(line)
	fmt.Printf("capas=%d\n", len(capas))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("capas={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("capas=%d\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: cuenta las filas (capas).
WITH capas(nombre) AS (VALUES ('web'), ('api'), ('datos'))
SELECT printf('capas=%d', count(*)) AS resultado FROM capas;
```

### PHP · `php main.php`

```php
<?php
$capas = preg_split('/\s+/', trim(fgets(STDIN)));
echo "capas=" . count($capas) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | Cada capa aísla una responsabilidad. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Arquitecturas en capas, hexagonal, microservicios: todas organizan componentes con responsabilidades.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 149
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capas con responsabilidades mezcladas** → causa: difícil de mantener → solución: una responsabilidad por capa
- **Alto acoplamiento** → causa: un cambio propaga a todo → solución: definir contratos claros entre capas

## ❓ Preguntas frecuentes

- **¿Cuántas capas?** Las que el problema justifique; ni de más ni de menos.
- **¿Capas o microservicios?** Capas dentro de un proceso; microservicios los separan en servicios.

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

> [⏮️ Clase 148](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 150 ⏭️](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md)
