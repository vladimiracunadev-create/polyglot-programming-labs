# Clase 048 — Cadenas: representación, inmutabilidad e interpolación

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con **cadenas**: leer texto, interpolarlo en un saludo y medir su longitud. Verás que la longitud puede significar 'bytes' o 'caracteres' según el lenguaje (aquí, ASCII, coinciden).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Interpolar una variable de texto en una cadena.
2. Obtener la longitud de una cadena.
3. Reconocer la inmutabilidad de las cadenas donde aplica.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interpolación | Insertar valores dentro de una cadena |
| 2 | Longitud | Cuántos caracteres tiene |
| 3 | Inmutabilidad | En muchos lenguajes la cadena no se modifica, se recrea |
| 4 | Bytes vs. caracteres | La longitud puede medir distinto |

## 📖 Definiciones y características

- **Cadena** — secuencia de caracteres. Clave: el tipo para todo texto.
- **Interpolación** — insertar el valor de una variable dentro de una cadena. Clave: `f"...{x}"`, `${x}`, etc.
- **Longitud** — número de unidades (caracteres/bytes) de la cadena. Clave: en ASCII coinciden.
- **Inmutabilidad de cadenas** — en Java, C#, Python las cadenas no se modifican in situ. Clave: se crea una nueva.

## 🧩 Situación

Saludar por nombre y contar caracteres son de las operaciones más comunes. Cómo se interpola y cómo se mide la longitud revela decisiones de diseño de cada lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `hola=<palabra> longitud=<número de caracteres>`
- **Regla:** longitud = |palabra|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `hola=Ada longitud=3` |
| `Bo` | `hola=Bo longitud=2` |
| `polyglot` | `hola=polyglot longitud=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w
ESCRIBIR "hola=" w " longitud=" LONGITUD(w)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
print(f"hola={w} longitud={len(w)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
console.log(`hola=${w} longitud=${w.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`hola=${w} longitud=${w.length}`);
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
        System.out.println("hola=" + w + " longitud=" + w.length());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"hola={w} longitud={w.Length}");
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
	fmt.Printf("hola=%s longitud=%d\n", w, len(w))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    println!("hola={} longitud={}", w, w.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[256];
    if (scanf("%255s", buf) != 1) return 1;
    printf("hola=%s longitud=%d\n", buf, (int) strlen(buf));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: length(w) cuenta los caracteres de una cadena.
WITH palabras(w) AS (VALUES ('Ada'), ('Bo'), ('polyglot'))
SELECT printf('hola=%s longitud=%d', w, length(w)) AS resultado
FROM palabras;
```

### PHP · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
printf("hola=%s longitud=%d\n", $w, strlen($w));
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `len(w)` (Python), `w.length` (JS/Java), `len(w)` (Go, bytes), `w.len()` (Rust, bytes). |
| Semántica | En Go/Rust `len` cuenta bytes; en Java/JS cuenta unidades UTF-16 (aquí ASCII: igual). |
| Paradigmática | SQL usa la función `length(w)` sobre una columna. |

## 🧬 El concepto en la familia

En Ruby `w.length`. En Haskell `length w`. En C++ `w.size()`. Todos miden lo mismo en ASCII; difieren con Unicode multibyte.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 048
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir que longitud = caracteres siempre** → causa: olvidar Unicode multibyte → solución: en Go/Rust `len` es bytes; usar el conteo de caracteres si hace falta
- **Modificar una cadena in situ** → causa: esperar mutación en Java/Python → solución: recordar que la cadena es inmutable: se crea una nueva

## ❓ Preguntas frecuentes

- **¿Por qué las cadenas son inmutables?** Seguridad y optimización (compartir, hashear). Modificar crea una copia.
- **¿`len` en Go da caracteres?** Da bytes; para caracteres Unicode se usa `utf8.RuneCountInString`.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

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

> [⏮️ Clase 047](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 049 ⏭️](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md)
