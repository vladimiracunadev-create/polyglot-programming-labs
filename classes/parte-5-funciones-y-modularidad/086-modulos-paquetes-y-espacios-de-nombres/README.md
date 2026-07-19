# Clase 086 — Módulos, paquetes y espacios de nombres

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Organizar el código en **módulos** (o paquetes/espacios de nombres): agrupar funciones relacionadas y usarlas con un prefijo o importándolas. Es lo que evita que un proyecto grande sea un solo archivo caótico.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Agrupar funciones en un módulo/espacio de nombres.
2. Invocar una función de otro módulo.
3. Reconocer import/require/use por lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Módulo | Agrupa código relacionado |
| 2 | Espacio de nombres | Evita choques de nombres |
| 3 | Importar | Traer lo que se necesita |
| 4 | Organización | Un proyecto no es un solo archivo |

## 📖 Definiciones y características

- **Módulo** — unidad que agrupa funciones/tipos relacionados. Clave: organización y reutilización.
- **Espacio de nombres** — prefijo que evita colisiones de nombres. Clave: `math.sqrt` vs. `otro.sqrt`.
- **Importar** — traer un módulo al alcance actual (import/require/use). Clave: acceder a su contenido.
- **Encapsulación de módulo** — exponer solo lo público. Clave: oculta detalles internos.

## 🧩 Situación

En un proyecto real, las utilidades matemáticas viven en un módulo, las de red en otro. Se importan donde hacen falta. Aquí, una función `doble` en un espacio propio se usa desde el principal.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** modulo.doble(n) = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `-4` | `resultado=-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR modulo
LEER n ; ESCRIBIR "resultado=" modulo.doble(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class matematicas:  # actúa como un espacio de nombres
    @staticmethod
    def doble(n):
        return 2 * n


n = int(sys.stdin.readline())
print(f"resultado={matematicas.doble(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// Objeto usado como módulo/espacio de nombres.
const matematicas = {
  doble: (n) => 2 * n,
};

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

namespace matematicas {
  export function doble(n: number): number {
    return 2 * n;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Clase de utilidades como espacio de nombres.
    static class Matematicas {
        static int doble(int n) {
            return 2 * n;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + Matematicas.doble(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

// En C# las sentencias top-level deben preceder a las declaraciones de tipo.
int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Matematicas.Doble(n)}");

static class Matematicas {
    public static int Doble(int n) => 2 * n;
}
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

// En un proyecto real 'doble' viviría en otro paquete; aquí simula el módulo.
func doble(n int) int {
	return 2 * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

mod matematicas {
    pub fn doble(n: i64) -> i64 {
        2 * n
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", matematicas::doble(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* En C la modularidad se hace por archivos .h/.c; aquí una función local. */
long doble(long n) {
    return 2 * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL organiza en esquemas (schemas); la operación va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (-4))
SELECT printf('resultado=%d', 2 * n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
// PHP usa namespaces; aquí una función que actúa como utilidad del módulo.
function matematicas_doble($n) {
    return 2 * $n;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . matematicas_doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `import`/`from` (Python), `require`/`import` (JS), `use` (Rust), `package` (Go/Java). |
| Semántica | El módulo define un espacio de nombres; se accede con prefijo o importando nombres. |
| Paradigmática | SQL organiza en esquemas (schemas), análogos a espacios de nombres. |

## 🧬 El concepto en la familia

En Ruby, módulos con `module M; def self.doble`. En C, la 'modularidad' es por archivos .h/.c y enlace.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 086
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Meter todo en un archivo** → causa: proyecto inmantenible → solución: separar por módulos con responsabilidad clara
- **Importar de más (namespace pollution)** → causa: colisiones y confusión → solución: importar solo lo necesario o usar el prefijo del módulo

## ❓ Preguntas frecuentes

- **¿Módulo, paquete o namespace?** Términos cercanos: agrupar y nombrar código. Cada lenguaje usa su palabra.
- **¿Por qué prefijos?** Para que dos módulos puedan tener funciones con el mismo nombre sin chocar.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. C. Martin — *Clean Code* (Prentice Hall).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).

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

> [⏮️ Clase 085](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 087 ⏭️](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md)
