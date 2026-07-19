# Clase 131 — Recolección de basura (GC)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **recolección de basura (GC)**: el runtime libera automáticamente la memoria de los objetos que ya no son alcanzables. El programador no llama a free; el GC lo hace.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es la recolección de basura.
2. Reconocer objetos inalcanzables.
3. Contrastar GC con gestión manual.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Recolector de basura | Libera lo inalcanzable |
| 2 | Alcanzabilidad | Si algo aún se puede usar |
| 3 | Pausas del GC | Coste del automatismo |

## 📖 Definiciones y características

- **Recolección de basura** — liberación automática de objetos ya inalcanzables. Clave: sin free manual.
- **Alcanzable** — objeto accesible desde una variable viva. Clave: lo inalcanzable es basura.
- **Pausa del GC** — momento en que el recolector trabaja. Clave: puede introducir latencia.

## 🧩 Situación

En Java, Python o Go creas objetos y los olvidas: el GC recupera su memoria cuando ya nadie los referencia. Cómodo, pero introduce pausas impredecibles.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de objetos temporales)
- **Salida** (stdout): `creados=<n> estado=recolectado`
- **Regla:** crear n objetos temporales; al perder la referencia, se recolectan

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `creados=5 estado=recolectado` |
| `0` | `creados=0 estado=recolectado` |
| `3` | `creados=3 estado=recolectado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
crear n objetos ; descartar referencias ; el GC recolecta
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
for _ in range(n):
    _tmp = object()  # temporal; sin referencia persistente, se recolecta
print(f"creados={n} estado=recolectado")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp = {}; // sin referencia persistente, será recolectado
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp: Record<string, unknown> = {};
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        for (int i = 0; i < n; i++) {
            Object tmp = new Object(); // el GC lo recolectará
            if (tmp == null) return;
        }
        System.out.println("creados=" + n + " estado=recolectado");
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
for (int i = 0; i < n; i++) {
    var tmp = new object(); // el GC lo recolectará
    if (tmp == null) return;
}
Console.WriteLine($"creados={n} estado=recolectado");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	for i := 0; i < n; i++ {
		tmp := new(int) // sin referencia persistente, el GC lo recolecta
		_ = tmp
	}
	fmt.Printf("creados=%d estado=recolectado\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    for _ in 0..n {
        let _tmp = Box::new(0); // se libera al salir del ámbito (sin GC)
    }
    println!("creados={n} estado=recolectado");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    for (long i = 0; i < n; i++) {
        long *tmp = malloc(sizeof(long)); /* en C se libera a mano */
        free(tmp);
    }
    printf("creados=%ld estado=recolectado\n", n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone la memoria; se informa el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('creados=%d estado=recolectado', n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
for ($i = 0; $i < $n; $i++) {
    $tmp = new stdClass(); // recolectado por conteo de referencias
    unset($tmp);
}
echo "creados=$n estado=recolectado\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | No hay free: se crean objetos y se olvidan. |
| Semántica | GC (Java/Python/Go) vs. ownership (Rust) vs. manual (C). |
| Paradigmática | SQL no expone memoria. |

## 🧬 El concepto en la familia

Java, C#, Go, Python, JS usan GC. Rust evita el GC con ownership; C es manual.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 131
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en el GC para recursos no-memoria** → causa: archivos/sockets sin cerrar → solución: cerrar explícitamente esos recursos
- **Retener referencias sin querer** → causa: fuga lógica: el GC no libera lo aún referenciado → solución: soltar las referencias que ya no usas

## ❓ Preguntas frecuentes

- **¿El GC elimina toda fuga?** Las de memoria en su mayoría; no las lógicas (referencias retenidas) ni otros recursos.
- **¿GC o sin GC?** GC da comodidad; sin GC (Rust/C) da control y latencia predecible.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 130](../../parte-8-como-funcionan-los-lenguajes/130-gestion-manual-de-memoria-c-malloc-free/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 132 ⏭️](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md)
