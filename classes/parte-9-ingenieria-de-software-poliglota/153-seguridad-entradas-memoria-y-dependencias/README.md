# Clase 153 — Seguridad: entradas, memoria y dependencias

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **seguridad**: validar y sanear las entradas para evitar inyecciones y datos maliciosos. Comprobar que una entrada es alfanumérica es una validación básica que cierra muchos ataques.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Validar una entrada contra un conjunto permitido.
2. Explicar por qué no confiar en la entrada.
3. Reconocer riesgos de seguridad comunes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación de entrada | No confiar en lo externo |
| 2 | Saneamiento | Limpiar datos peligrosos |
| 3 | Inyección | Datos que se ejecutan como código |

## 📖 Definiciones y características

- **Validación de entrada** — comprobar que los datos cumplen lo esperado antes de usarlos. Clave: primera defensa.
- **Saneamiento** — eliminar o escapar caracteres peligrosos. Clave: evita inyecciones.
- **Inyección** — datos maliciosos que el programa interpreta como comando (SQL, shell). Clave: causa frecuente de brechas.

## 🧩 Situación

Un campo que debería ser un nombre recibe `'; DROP TABLE`. Validar que solo contiene caracteres alfanuméricos rechaza la entrada maliciosa antes de que cause daño.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (entrada a validar)
- **Salida** (stdout): `seguro=<true|false>` (true si es alfanumérica)
- **Regla:** seguro si todos los caracteres son letras o dígitos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `abc` | `seguro=true` |
| `a;b` | `seguro=false` |
| `hola123` | `seguro=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER entrada ; seguro <- todos los caracteres alfanuméricos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
seguro = w.isalnum()
print(f"seguro={'true' if seguro else 'false'}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
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
        boolean seguro = w.matches("[A-Za-z0-9]+");
        System.out.println("seguro=" + (seguro ? "true" : "false"));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool seguro = w.Length > 0 && w.All(char.IsLetterOrDigit);
Console.WriteLine($"seguro={(seguro ? "true" : "false")}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"unicode"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	seguro := len(w) > 0
	for _, c := range w {
		if !unicode.IsLetter(c) && !unicode.IsDigit(c) {
			seguro = false
		}
	}
	res := "false"
	if seguro {
		res = "true"
	}
	fmt.Printf("seguro=%s\n", res)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let seguro = !w.is_empty() && w.chars().all(|c| c.is_ascii_alphanumeric());
    println!("seguro={}", if seguro { "true" } else { "false" });
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int seguro = 1;
    for (int i = 0; w[i]; i++) {
        if (!isalnum((unsigned char) w[i])) seguro = 0;
    }
    printf("seguro=%s\n", seguro ? "true" : "false");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se evita la inyección con consultas parametrizadas; aquí, validación por patrón.
WITH t(w) AS (VALUES ('abc'))
SELECT printf('seguro=%s', CASE WHEN w GLOB '*[^A-Za-z0-9]*' THEN 'false' ELSE 'true' END) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
$seguro = ctype_alnum($w);
echo "seguro=" . ($seguro ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | isalnum/regex en cada lenguaje. |
| Semántica | Se valida contra una lista blanca (más seguro que una negra). |
| Paradigmática | SQL usa consultas parametrizadas para evitar inyección. |

## 🧬 El concepto en la familia

Toda plataforma web valida entradas; las consultas parametrizadas evitan la inyección SQL.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 153
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en la entrada del usuario** → causa: inyecciones y corrupción → solución: validar y sanear siempre
- **Lista negra en vez de blanca** → causa: olvidar un caso peligroso → solución: permitir solo lo conocido (lista blanca)

## ❓ Preguntas frecuentes

- **¿Validar en cliente o servidor?** En ambos, pero la validación del servidor es la que cuenta.
- **¿Cómo evitar inyección SQL?** Con consultas parametrizadas, nunca concatenando la entrada.

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

> [⏮️ Clase 152](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 154 ⏭️](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md)
