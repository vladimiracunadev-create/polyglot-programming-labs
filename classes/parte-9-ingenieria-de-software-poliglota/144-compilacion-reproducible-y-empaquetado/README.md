# Clase 144 — Compilación reproducible y empaquetado

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **compilación reproducible y el empaquetado**: una build reproducible produce siempre el mismo artefacto para la misma entrada, comprobable con una suma de verificación (checksum). Aquí el checksum es la suma de los valores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular una suma de comprobación.
2. Explicar la reproducibilidad.
3. Relacionar el checksum con la verificación de artefactos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Reproducibilidad | Misma entrada, mismo artefacto |
| 2 | Checksum | Huella de los datos |
| 3 | Verificación | Detectar cambios |

## 📖 Definiciones y características

- **Compilación reproducible** — produce un artefacto idéntico byte a byte para la misma entrada. Clave: confianza y auditoría.
- **Checksum** — valor derivado de los datos que cambia si estos cambian. Clave: detecta alteraciones.
- **Artefacto** — salida de la build (binario, paquete). Clave: se verifica con su checksum.

## 🧩 Situación

Al descargar un binario, su checksum publicado permite verificar que no fue alterado. Una build reproducible da siempre el mismo checksum, lo que hace auditable la cadena de suministro.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `checksum=<suma de los valores>`
- **Regla:** checksum = suma de los valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `checksum=6` |
| `5` | `checksum=5` |
| `10 20 30` | `checksum=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; checksum <- suma ; ESCRIBIR checksum
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"checksum={sum(nums)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long c = 0;
        for (String s : p) c += Integer.parseInt(s);
        System.out.println("checksum=" + c);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

long c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"checksum={c}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	c := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		c += n
	}
	fmt.Printf("checksum=%d\n", c)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("checksum={c}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long c = 0, x;
    while (scanf("%ld", &x) == 1) c += x;
    printf("checksum=%ld\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM como checksum simple.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('checksum=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "checksum=" . array_sum($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Suma en cada lenguaje (un checksum real usaría un hash). |
| Semántica | La misma entrada da el mismo checksum: reproducibilidad. |
| Paradigmática | SQL suma con SUM. |

## 🧬 El concepto en la familia

Los gestores de paquetes verifican con SHA-256; aquí una suma simple ilustra el concepto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 144
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en un checksum débil** → causa: colisiones → solución: usar hashes criptográficos para seguridad real
- **Builds no reproducibles** → causa: checksums que cambian sin motivo → solución: eliminar fuentes de no-determinismo (fechas, orden)

## ❓ Preguntas frecuentes

- **¿Suma o hash?** Para integridad real se usa un hash (SHA-256); la suma solo ilustra.
- **¿Por qué builds reproducibles?** Auditar que el binario proviene del código y no fue manipulado.

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

> [⏮️ Clase 143](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 145 ⏭️](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md)
