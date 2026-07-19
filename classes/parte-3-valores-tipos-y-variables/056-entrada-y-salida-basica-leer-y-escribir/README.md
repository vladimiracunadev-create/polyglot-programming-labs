# Clase 056 — Entrada y salida básica: leer y escribir

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la Parte 3 con lo más elemental: **leer de la entrada estándar y escribir en la salida estándar**. Todo el curso se apoya en este contrato (stdin → stdout), y aquí se ve desnudo en los 10 lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Leer una línea completa de stdin.
2. Escribir en stdout con un formato dado.
3. Reconocer el contrato stdin/stdout usado en todo el curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrada estándar (stdin) | El canal por defecto de entrada |
| 2 | Salida estándar (stdout) | El canal por defecto de salida |
| 3 | Leer una línea | Distinto de leer un token o un carácter |
| 4 | El contrato del curso | stdin → stdout, verificable |

## 📖 Definiciones y características

- **stdin** — canal de entrada estándar de un programa. Clave: de donde se leen los datos por defecto.
- **stdout** — canal de salida estándar. Clave: donde se escribe el resultado que se verifica.
- **Leer una línea** — obtener texto hasta el salto de línea. Clave: incluye espacios internos.
- **Eco** — devolver la entrada tal cual (con un prefijo). Clave: el ejemplo mínimo de E/S.

## 🧩 Situación

Todo programa de este curso lee de stdin y escribe en stdout; por eso el verificador puede comprobarlos a todos igual. El 'eco' es la forma más simple de ese contrato.

## 🧮 Modelo

- **Entrada** (stdin): una línea de texto
- **Salida** (stdout): `eco: <la línea leída>`
- **Regla:** salida = 'eco: ' + entrada

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `eco: hola` |
| `Polyglot` | `eco: Polyglot` |
| `123` | `eco: 123` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER linea
ESCRIBIR "eco: " linea
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

linea = sys.stdin.readline().rstrip("\n")
print(f"eco: {linea}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
console.log(`eco: ${linea}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
console.log(`eco: ${linea}`);
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
        System.out.println("eco: " + linea);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
Console.WriteLine($"eco: {linea}");
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
	line = strings.TrimRight(line, "\r\n")
	fmt.Printf("eco: %s\n", line)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    println!("eco: {linea}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[1024];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    printf("eco: %s\n", buf);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no lee stdin: se muestra el eco sobre una tabla de textos.
WITH lineas(x) AS (VALUES ('hola'), ('Polyglot'), ('123'))
SELECT printf('eco: %s', x) AS resultado
FROM lineas;
```

### PHP · `php main.php`

```php
<?php
$linea = rtrim(fgets(STDIN), "\r\n");
echo "eco: $linea\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `input()`/`readline` (Python), `readFileSync(0)` (JS), `fgets` (C). |
| Semántica | Hay que quitar el salto de línea final para que el eco sea exacto. |
| Paradigmática | SQL no lee stdin: se muestra el eco sobre una tabla de textos. |

## 🧬 El concepto en la familia

En Ruby `gets.chomp`. En Haskell `getLine`. En C++ `std::getline(std::cin, s)`. Todos leen una línea y recortan el salto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 056
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar el salto de línea pegado** → causa: no recortar el `\n` final → solución: usar trim/chomp/TrimSpace antes de imprimir
- **Leer un token en vez de la línea** → causa: perder el texto tras el primer espacio → solución: leer la línea completa cuando el dato puede tener espacios

## ❓ Preguntas frecuentes

- **¿stdin y un archivo son distintos?** Conceptualmente no: stdin es un flujo; puede venir del teclado o redirigido de un archivo.
- **¿Por qué el curso usa stdin/stdout?** Es el contrato común que permite verificar los 10 lenguajes con los mismos casos.

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

> [⏮️ Clase 055](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 057 ⏭️](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md)
