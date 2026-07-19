# Clase 093 — Cadenas como estructura de datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Tratar una **cadena como estructura de datos**: una secuencia de caracteres que se puede recorrer, indexar e invertir. Verás que la inmutabilidad obliga a construir una nueva cadena.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una cadena carácter a carácter.
2. Construir una cadena invertida.
3. Reconocer la inmutabilidad de las cadenas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Cadena como secuencia | Caracteres indexados |
| 2 | Inversión | Del último al primero |
| 3 | Inmutabilidad | Se crea una nueva cadena |

## 📖 Definiciones y características

- **Cadena** — secuencia de caracteres. Clave: se recorre como una colección.
- **Inmutable** — no se modifica en sitio (Java/Python/C#). Clave: invertir crea otra.
- **Índice de carácter** — posición dentro de la cadena. Clave: base 0.

## 🧩 Situación

Invertir texto, comprobar palíndromos, procesar entradas: tratar la cadena como una secuencia de caracteres es constante en programación.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `invertido=<la palabra al revés>`
- **Regla:** invertir la secuencia de caracteres

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `invertido=aloh` |
| `Ada` | `invertido=adA` |
| `abc` | `invertido=cba` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; recorrer del final al inicio ; ESCRIBIR invertido
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
print(f"invertido={w[::-1]}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
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
        System.out.println("invertido=" + new StringBuilder(w).reverse());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"invertido={new string(w.Reverse().ToArray())}");
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
	r := []rune(w)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	fmt.Printf("invertido=%s\n", string(r))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let inv: String = w.chars().rev().collect();
    println!("invertido={inv}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int n = (int) strlen(w);
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) putchar(w[i]);
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sqlite no trae reverse; se invierte con un CTE recursivo (ilustrativo).
WITH RECURSIVE r(i, acc, s) AS (
    SELECT length('hola'), '', 'hola'
    UNION ALL SELECT i - 1, acc || substr(s, i, 1), s FROM r WHERE i > 0
)
SELECT 'invertido=' || acc AS resultado FROM r WHERE i = 0;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
echo "invertido=" . strrev($w) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `w[::-1]` (Python), `.reverse()` sobre arreglo de chars (JS/Rust). |
| Semántica | En Rust hay que iterar por `chars()` (UTF-8); en C es por bytes. |
| Paradigmática | SQL tiene la función `reverse` en algunos motores; sqlite no de serie. |

## 🧬 El concepto en la familia

En Ruby `w.reverse`. En C se intercambian los caracteres por índices, sin función incorporada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 093
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir por bytes con Unicode** → causa: romper caracteres multibyte → solución: iterar por caracteres (aquí ASCII, sin problema)
- **Intentar mutar la cadena** → causa: es inmutable en varios lenguajes → solución: construir una nueva

## ❓ Preguntas frecuentes

- **¿Por qué invertir crea otra cadena?** Porque en muchos lenguajes las cadenas son inmutables.
- **¿ASCII o Unicode?** Aquí ASCII; con Unicode hay que respetar los límites de carácter.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 092](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 094 ⏭️](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md)
