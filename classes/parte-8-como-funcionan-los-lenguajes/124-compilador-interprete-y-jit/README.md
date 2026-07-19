# Clase 124 — Compilador, intérprete y JIT

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Diferenciar **compilador, intérprete y JIT** por su forma de ejecutar. El programa (contar dígitos) es el mismo; lo que cambia entre modelos es cuándo y cómo se traduce a instrucciones de la máquina.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar dígitos recorriendo el número.
2. Explicar compilado, interpretado y JIT.
3. Relacionar el modelo con el rendimiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Compilador | Traduce antes de ejecutar |
| 2 | Intérprete | Ejecuta la fuente al vuelo |
| 3 | JIT | Compila durante la ejecución |

## 📖 Definiciones y características

- **Compilador** — traduce todo el programa a código máquina antes de ejecutar. Clave: rápido, errores antes.
- **Intérprete** — ejecuta la fuente instrucción a instrucción. Clave: flexible, más lento.
- **JIT** — compila a máquina las partes calientes durante la ejecución. Clave: combina ambos (V8, JVM).

## 🧩 Situación

Contar dígitos corre igual en C (compilado), Python (interpretado) y JavaScript (JIT); lo que cambia es el rendimiento y cuándo aparecen los errores, no el resultado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 0)
- **Salida** (stdout): `digitos=<cantidad de dígitos>`
- **Regla:** contar los dígitos de n (0 tiene 1)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `12345` | `digitos=5` |
| `7` | `digitos=1` |
| `100` | `digitos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
contar dígitos dividiendo por 10 hasta 0 (o longitud del texto)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"digitos={len(str(n))}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: string = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String n = br.readLine().trim();
        System.out.println("digitos=" + n.length());
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string n = Console.In.ReadToEnd().Trim();
Console.WriteLine($"digitos={n.Length}");
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
	n := strings.TrimSpace(line)
	fmt.Printf("digitos=%d\n", len(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.trim();
    println!("digitos={}", n.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char n[64];
    if (scanf("%63s", n) != 1) return 1;
    printf("digitos=%d\n", (int) strlen(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: length sobre el texto del número.
WITH nums(n) AS (VALUES ('12345'))
SELECT printf('digitos=%d', length(n)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = trim(fgets(STDIN));
echo "digitos=" . strlen($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Igual en todos: recorrer o medir el número. |
| Semántica | El modelo de ejecución no cambia el resultado. |
| Paradigmática | SQL usa length sobre el texto del número. |

## 🧬 El concepto en la familia

C compila; CPython interpreta bytecode; V8 y la JVM usan JIT. El programa es idéntico.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 124
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar 0 como 0 dígitos** → causa: el 0 tiene un dígito → solución: tratar el caso n=0
- **Dividir sin parar** → causa: bucle infinito → solución: parar cuando el número llega a 0

## ❓ Preguntas frecuentes

- **¿Cuál es más rápido?** Compilado suele ganar en ejecución; interpretado gana en iteración; JIT busca ambos.
- **¿Python compila?** A bytecode internamente; luego lo interpreta.

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

> [⏮️ Clase 123](../../parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 125 ⏭️](../../parte-8-como-funcionan-los-lenguajes/125-bytecode-y-maquinas-virtuales-jvm-clr-v8/README.md)
