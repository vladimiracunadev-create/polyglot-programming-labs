# Clase 143 — Dependencias, versiones y lockfiles

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender **dependencias, versiones y lockfiles**: el versionado semántico (SemVer) 'mayor.menor.parche' comunica compatibilidad. Descomponerlo es el primer paso para gestionar dependencias con criterio.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Parsear una versión semántica.
2. Explicar qué significa cada componente.
3. Reconocer el papel del lockfile.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | SemVer | mayor.menor.parche |
| 2 | Compatibilidad | Qué implica cada número |
| 3 | Lockfile | Versiones exactas fijadas |

## 📖 Definiciones y características

- **Versionado semántico** — esquema mayor.menor.parche donde cada número señala el tipo de cambio. Clave: comunica compatibilidad.
- **Mayor/menor/parche** — cambios incompatibles / nuevas features / correcciones. Clave: guían las actualizaciones.
- **Lockfile** — archivo con las versiones exactas resueltas. Clave: builds reproducibles.

## 🧩 Situación

Al depender de una librería '^1.4.2', importa si sube a 1.5.0 (compatible) o a 2.0.0 (posible ruptura). El lockfile fija la versión exacta para que todos obtengan lo mismo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `mayor=<M> menor=<m> parche=<p>`
- **Regla:** separar la versión por puntos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `mayor=1 menor=2 parche=3` |
| `0.5.10` | `mayor=0 menor=5 parche=10` |
| `2.0.0` | `mayor=2 menor=0 parche=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; separar por '.' ; ESCRIBIR componentes
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

mayor, menor, parche = sys.stdin.readline().strip().split(".")
print(f"mayor={int(mayor)} menor={int(menor)} parche={int(parche)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] v = br.readLine().trim().split("\\.");
        System.out.println("mayor=" + Integer.parseInt(v[0]) + " menor=" + Integer.parseInt(v[1]) + " parche=" + Integer.parseInt(v[2]));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] v = Console.In.ReadToEnd().Trim().Split('.');
Console.WriteLine($"mayor={int.Parse(v[0])} menor={int.Parse(v[1])} parche={int.Parse(v[2])}");
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
	v := strings.Split(strings.TrimSpace(line), ".")
	ma, _ := strconv.Atoi(v[0])
	me, _ := strconv.Atoi(v[1])
	pa, _ := strconv.Atoi(v[2])
	fmt.Printf("mayor=%d menor=%d parche=%d\n", ma, me, pa)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.trim().split('.').map(|x| x.parse().unwrap()).collect();
    println!("mayor={} menor={} parche={}", v[0], v[1], v[2]);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long ma, me, pa;
    if (scanf("%ld.%ld.%ld", &ma, &me, &pa) != 3) return 1;
    printf("mayor=%ld menor=%ld parche=%ld\n", ma, me, pa);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: separa la versión con funciones de texto (ilustrativo).
WITH v(s) AS (VALUES ('1.2.3'))
SELECT printf('mayor=%d menor=%d parche=%d',
       CAST(substr(s, 1, instr(s, '.') - 1) AS INTEGER),
       CAST(substr(s, instr(s, '.') + 1, instr(substr(s, instr(s, '.') + 1), '.') - 1) AS INTEGER),
       CAST(substr(s, length(s) - instr(reverse(s), '.') + 2) AS INTEGER)) AS resultado
FROM v;
```

### PHP · `php main.php`

```php
<?php
[$ma, $me, $pa] = explode(".", trim(fgets(STDIN)));
echo "mayor=" . (int) $ma . " menor=" . (int) $me . " parche=" . (int) $pa . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | split por '.' en cada lenguaje. |
| Semántica | Cada número tiene un significado de compatibilidad. |
| Paradigmática | SQL separa con funciones de texto. |

## 🧬 El concepto en la familia

npm, cargo, pip, composer usan SemVer y lockfiles (package-lock.json, Cargo.lock).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 143
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No commitear el lockfile** → causa: builds distintos por máquina → solución: versionar el lockfile
- **Fijar a 'latest'** → causa: roturas por actualizaciones → solución: acotar rangos y confiar en el lock

## ❓ Preguntas frecuentes

- **¿Qué sube en un parche?** Solo correcciones compatibles; no rompe nada.
- **¿Por qué el lockfile?** Garantiza que todos instalen exactamente las mismas versiones.

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

> [⏮️ Clase 142](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 144 ⏭️](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md)
