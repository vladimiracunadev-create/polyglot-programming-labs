# Clase 141 — Depuradores: gdb, lldb, pdb y los de IDE

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar la idea de un **depurador**: avanzar paso a paso viendo cómo evoluciona el estado. La traza de sumas acumuladas (1, 3, 6, …) muestra el valor del acumulador en cada paso, como haría un depurador.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Producir una traza de estados.
2. Explicar el avance paso a paso.
3. Nombrar los depuradores por runtime.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Traza | Estado en cada paso |
| 2 | Paso a paso | Avanzar controladamente |
| 3 | Punto de ruptura | Pausar para inspeccionar |

## 📖 Definiciones y características

- **Depurador** — herramienta para pausar y avanzar viendo el estado (gdb, pdb). Clave: diagnóstico.
- **Traza** — secuencia de estados por los que pasa el programa. Clave: revela dónde se desvía.
- **Paso a paso (step)** — avanzar una instrucción a la vez. Clave: inspeccionar cada cambio.

## 🧩 Situación

Cuando un resultado sorprende, se avanza paso a paso viendo el acumulador. La traza 1-3-6 muestra la suma acumulada tras cada elemento, como el panel de variables de un depurador.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `traza=<sumas acumuladas 1..n unidas por ->`
- **Regla:** traza[i] = 1 + 2 + ... + i

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `traza=1-3-6` |
| `1` | `traza=1` |
| `4` | `traza=1-3-6-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
acc <- 0 ; PARA i de 1 a n: acc <- acc+i ; emitir acc
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
acc = 0
pasos = []
for i in range(1, n + 1):
    acc += i
    pasos.append(acc)
print("traza=" + "-".join(str(x) for x in pasos))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos: number[] = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
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
        long acc = 0;
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            acc += i;
            if (i > 1) sb.append("-");
            sb.append(acc);
        }
        System.out.println("traza=" + sb);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long acc = 0;
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    acc += i;
    if (i > 1) sb.Append("-");
    sb.Append(acc);
}
Console.WriteLine($"traza={sb}");
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
	acc := 0
	var pasos []string
	for i := 1; i <= n; i++ {
		acc += i
		pasos = append(pasos, strconv.Itoa(acc))
	}
	fmt.Printf("traza=%s\n", strings.Join(pasos, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut acc = 0i64;
    let mut pasos: Vec<String> = Vec::new();
    for i in 1..=n {
        acc += i;
        pasos.push(acc.to_string());
    }
    println!("traza={}", pasos.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long acc = 0;
    printf("traza=");
    for (long i = 1; i <= n; i++) {
        acc += i;
        if (i > 1) printf("-");
        printf("%ld", acc);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sumas acumuladas con función de ventana (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 3)
SELECT 'traza=' || group_concat(s, '-') AS resultado
FROM (SELECT sum(i) OVER (ORDER BY i) AS s FROM r);
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$acc = 0;
$pasos = [];
for ($i = 1; $i <= $n; $i++) {
    $acc += $i;
    $pasos[] = $acc;
}
echo "traza=" . implode("-", $pasos) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle con acumulador en cada lenguaje. |
| Semántica | La traza expone el estado intermedio. |
| Paradigmática | SQL usa sumas acumuladas con funciones de ventana. |

## 🧬 El concepto en la familia

gdb/lldb, pdb, y los depuradores de la JVM/.NET y los IDE ofrecen este avance paso a paso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 141
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depurar sin observar el estado** → causa: cambios al azar → solución: trazar el acumulador en cada paso
- **Olvidar reiniciar el acumulador** → causa: traza incorrecta → solución: empezar el acumulador en 0

## ❓ Preguntas frecuentes

- **¿print o depurador?** El depurador evita recompilar y permite avanzar paso a paso.
- **¿Qué es un watch?** Una expresión que el depurador reevalúa en cada pausa.

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

> [⏮️ Clase 140](../../parte-9-ingenieria-de-software-poliglota/140-pruebas-de-integracion-y-el-verificador-de-equivalencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 142 ⏭️](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md)
