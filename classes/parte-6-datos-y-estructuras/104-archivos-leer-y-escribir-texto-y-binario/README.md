# Clase 104 — Archivos: leer y escribir texto y binario

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Procesar **contenido textual** como el de un archivo: leer una línea y extraer información (palabras, caracteres). Es el modelo de la lectura de archivos, aquí por la entrada estándar para poder verificarlo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Leer una línea completa con espacios.
2. Contar palabras y caracteres.
3. Relacionarlo con la lectura de archivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Leer contenido | Una línea con espacios |
| 2 | Contar palabras | Separar por espacios |
| 3 | Contar caracteres | Longitud del texto |

## 📖 Definiciones y características

- **Contenido de texto** — los caracteres de un archivo o entrada. Clave: se procesa línea a línea.
- **Palabra** — secuencia separada por espacios. Clave: se cuenta partiendo por espacios.
- **Carácter** — cada símbolo, incluidos los espacios. Clave: la longitud total.

## 🧩 Situación

Contar líneas, palabras o caracteres (como `wc`) es el 'hola mundo' del procesamiento de archivos. Aquí el contenido llega por stdin para poder verificar el resultado.

## 🧮 Modelo

- **Entrada** (stdin): una línea de texto (puede contener espacios)
- **Salida** (stdout): `palabras=<número de palabras> caracteres=<longitud incluyendo espacios>`
- **Regla:** palabras = partes por espacio; caracteres = longitud de la línea

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola mundo` | `palabras=2 caracteres=10` |
| `abc` | `palabras=1 caracteres=3` |
| `a b c d` | `palabras=4 caracteres=7` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER linea ; palabras <- partir por espacios ; caracteres <- longitud
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

linea = sys.stdin.readline().rstrip("\n")
palabras = len(linea.split())
print(f"palabras={palabras} caracteres={len(linea)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        int palabras = linea.trim().isEmpty() ? 0 : linea.trim().split("\\s+").length;
        System.out.println("palabras=" + palabras + " caracteres=" + linea.length());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
int palabras = linea.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
Console.WriteLine($"palabras={palabras} caracteres={linea.Length}");
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
	linea := strings.TrimRight(line, "\r\n")
	palabras := len(strings.Fields(linea))
	fmt.Printf("palabras=%d caracteres=%d\n", palabras, len(linea))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    let palabras = linea.split_whitespace().count();
    println!("palabras={} caracteres={}", palabras, linea.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char buf[4096];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    int caracteres = (int) strlen(buf);
    int palabras = 0, dentro = 0;
    for (int i = 0; buf[i]; i++) {
        if (isspace((unsigned char) buf[i])) {
            dentro = 0;
        } else if (!dentro) {
            dentro = 1;
            palabras++;
        }
    }
    printf("palabras=%d caracteres=%d\n", palabras, caracteres);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: longitud con length(); palabras con funciones de texto (ilustrativo).
WITH t(linea) AS (VALUES ('hola mundo'))
SELECT printf('palabras=%d caracteres=%d',
       length(linea) - length(replace(linea, ' ', '')) + 1, length(linea)) AS resultado
FROM t;
```

### PHP · `php main.php`

```php
<?php
$linea = rtrim(fgets(STDIN), "\r\n");
$palabras = $linea === "" ? 0 : count(preg_split('/\s+/', trim($linea)));
echo "palabras=$palabras caracteres=" . strlen($linea) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `split()` y `len()` (Python) vs. equivalentes por lenguaje. |
| Semántica | La longitud incluye los espacios; las palabras no. |
| Paradigmática | SQL cuenta con funciones de texto y agregación. |

## 🧬 El concepto en la familia

En Ruby `linea.split.size` y `linea.length`. El comando Unix `wc` hace justo esto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 104
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar espacios como palabras** → causa: palabras vacías → solución: partir por uno o más espacios
- **Olvidar quitar el salto de línea** → causa: un carácter de más → solución: recortar el `\n` final antes de contar

## ❓ Preguntas frecuentes

- **¿Por qué stdin y no un archivo?** Para poder verificar el resultado con casos; un archivo se leería igual, línea a línea.
- **¿Los caracteres incluyen espacios?** Sí: son parte del contenido; las palabras no.

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

> [⏮️ Clase 103](../../parte-6-datos-y-estructuras/103-propiedad-y-ciclo-de-vida-de-los-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 105 ⏭️](../../parte-6-datos-y-estructuras/105-json-serializacion-y-deserializacion/README.md)
