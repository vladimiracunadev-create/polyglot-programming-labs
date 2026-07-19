# Clase 167 — Componente CLI (lenguaje de sistemas)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente CLI** del sistema (idóneo para un lenguaje de sistemas): una interfaz de línea de comandos que recibe un comando y argumentos. Aquí se parsea el comando y se cuentan sus argumentos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Parsear una invocación de CLI.
2. Separar comando de argumentos.
3. Explicar el rol del componente CLI.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CLI | Interfaz de línea de comandos |
| 2 | Comando y argumentos | Qué hacer y con qué |
| 3 | Parseo | Interpretar la invocación |

## 📖 Definiciones y características

- **Componente CLI** — interfaz por terminal del sistema. Clave: automatizable y componible.
- **Comando** — la acción a ejecutar (el primer token). Clave: selecciona qué hacer.
- **Argumento** — dato que modifica la acción. Clave: se cuentan tras el comando.

## 🧩 Situación

La CLI del sistema recibe `run a b`: el comando es `run` y hay 2 argumentos. Parsear bien la invocación es la base de cualquier herramienta de línea de comandos, a menudo escrita en Go o Rust.

## 🧮 Modelo

- **Entrada** (stdin): una línea `comando arg1 arg2 ...` (al menos el comando)
- **Salida** (stdout): `comando=<comando> args=<número de argumentos>`
- **Regla:** primer token = comando; resto = argumentos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `run a b` | `comando=run args=2` |
| `build` | `comando=build args=0` |
| `deploy x y z` | `comando=deploy args=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens ; comando <- tokens[0] ; args <- tokens - 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

t = sys.stdin.read().split()
print(f"comando={t[0]} args={len(t) - 1}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        System.out.println("comando=" + t[0] + " args=" + (t.length - 1));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"comando={t[0]} args={t.Length - 1}");
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
	t := strings.Fields(line)
	fmt.Printf("comando=%s args=%d\n", t[0], len(t)-1)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    println!("comando={} args={}", t[0], t.len() - 1);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char comando[64], t[64];
    if (scanf("%63s", comando) != 1) return 1;
    int args = 0;
    while (scanf("%63s", t) == 1) args++;
    printf("comando=%s args=%d\n", comando, args);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene CLI; se ilustra con valores.
WITH t(comando, args) AS (VALUES ('run', 2))
SELECT printf('comando=%s args=%d', comando, args) AS resultado FROM t;
```

### PHP · `php main.php`

```php
<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
echo "comando={$t[0]} args=" . (count($t) - 1) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Separar el primer token del resto en cada lenguaje. |
| Semántica | El comando decide la acción; los argumentos, los datos. |
| Paradigmática | SQL no tiene CLI de argumentos; se consulta. |

## 🧬 El concepto en la familia

clap (Rust), cobra (Go), argparse (Python), commander (JS) construyen CLIs robustas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 167
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No validar los argumentos** → causa: errores al ejecutar → solución: comprobar cantidad y tipo de argumentos
- **Mensajes de ayuda ausentes** → causa: CLI difícil de usar → solución: ofrecer --help y errores claros

## ❓ Preguntas frecuentes

- **¿Qué lenguaje para una CLI?** Go y Rust por sus binarios únicos y rápidos; Python para scripts.
- **¿Argumentos posicionales o con nombre?** Nombrados (--flag) para claridad; posicionales para lo esencial.

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

> [⏮️ Clase 166](../../parte-11-proyecto-integrador-poliglota/166-diseno-responsabilidades-y-contratos-entre-componentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 168 ⏭️](../../parte-11-proyecto-integrador-poliglota/168-componente-de-api-servicio-backend/README.md)
