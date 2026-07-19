# Clase 108 — Imperativo y estructurado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **paradigma imperativo y estructurado**: describir la solución como una secuencia de pasos que modifican el estado (un acumulador), usando bucles y condiciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Resolver con estado mutable y bucles.
2. Reconocer la secuencia de pasos.
3. Contrastar con el estilo funcional.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Imperativo | Pasos que cambian el estado |
| 2 | Estructurado | Secuencia, selección, iteración |
| 3 | Estado mutable | Variables que cambian |

## 📖 Definiciones y características

- **Imperativo** — paradigma que describe cómo cambiar el estado paso a paso. Clave: bucles y asignaciones.
- **Estructurado** — usa solo secuencia, selección e iteración (sin goto). Clave: código claro.
- **Estado mutable** — variables que cambian durante la ejecución. Clave: el acumulador.

## 🧩 Situación

El estilo imperativo es el más cercano a cómo funciona la máquina: 'haz esto, luego esto'. Sumar con un acumulador y un bucle es su ejemplo puro.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** acumular la suma recorriendo la lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20` | `suma=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma <- 0 ; PARA CADA x: suma <- suma + x
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
suma = 0
for x in nums:
    suma += x
print(f"suma={suma}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) suma += x;
console.log(`suma=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) suma += x;
console.log(`suma=${suma}`);
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
        long suma = 0;
        for (String s : p) suma += Integer.parseInt(s);
        System.out.println("suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = 0;
foreach (string s in p) suma += int.Parse(s);
Console.WriteLine($"suma={suma}");
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
	suma := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		suma += n
	}
	fmt.Printf("suma=%d\n", suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut suma: i64 = 0;
    for x in s.split_whitespace() {
        suma += x.parse::<i64>().unwrap();
    }
    println!("suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) suma += x;
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega sobre filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$suma = 0;
foreach ($nums as $x) {
    $suma += (int) $x;
}
echo "suma=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle explícito en todos los imperativos. |
| Semántica | Modifica un acumulador; el estado evoluciona. |
| Paradigmática | El funcional evitaría el acumulador mutable con reduce. |

## 🧬 El concepto en la familia

Casi todos los lenguajes del núcleo soportan el estilo imperativo de forma nativa.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 108
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No inicializar el acumulador** → causa: resultado incorrecto → solución: empezar en 0
- **Efectos secundarios ocultos** → causa: estado difícil de seguir → solución: mantener el estado local y claro

## ❓ Preguntas frecuentes

- **¿Imperativo o funcional?** Imperativo es directo y eficiente; funcional es más declarativo. Depende.
- **¿Estructurado significa sin goto?** Sí: solo secuencia, selección e iteración.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 107](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 109 ⏭️](../../parte-7-paradigmas/109-procedimental-y-modular/README.md)
