# Clase 054 — Mutabilidad e inmutabilidad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la diferencia entre construir un resultado **mutando** un acumulador (StringBuilder, lista que crece) y hacerlo de forma **inmutable**. Construir una secuencia numérica muestra el patrón acumulador en cada lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un resultado acumulando en un bucle.
2. Reconocer estructuras mutables (builder, lista).
3. Explicar el coste de concatenar cadenas inmutables.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Acumulador | Una variable que crece en cada vuelta |
| 2 | Mutable vs. inmutable | Modificar en sitio o crear nuevo |
| 3 | StringBuilder | Construir texto eficientemente |
| 4 | Coste de la inmutabilidad | Concatenar cadenas puede recrear todo |

## 📖 Definiciones y características

- **Mutabilidad** — capacidad de cambiar un valor in situ. Clave: eficiente para construir por partes.
- **Inmutabilidad** — el valor no cambia; toda 'modificación' crea uno nuevo. Clave: más seguro, a veces más caro.
- **Acumulador** — variable que reúne el resultado a lo largo de un bucle. Clave: patrón universal.
- **Builder** — estructura mutable para construir cadenas/colecciones (StringBuilder). Clave: evita recrear en cada paso.

## 🧩 Situación

Concatenar 10.000 cadenas con `+` en un bucle puede ser lentísimo si cada `+` recrea toda la cadena. Por eso existen los builders mutables. Construir '1-2-...-n' ilustra el patrón.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `sec=1-2-...-n` (números de 1 a n separados por guiones)
- **Regla:** sec = unir([1..n], separador='-')

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `sec=1-2-3` |
| `1` | `sec=1` |
| `5` | `sec=1-2-3-4-5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
acc <- vacío
PARA i de 1 a n: añadir i a acc
ESCRIBIR "sec=" UNIR(acc, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print("sec=" + "-".join(str(i) for i in range(1, n + 1)))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const parts = [];
for (let i = 1; i <= n; i++) parts.push(i);
console.log(`sec=${parts.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const parts: number[] = [];
for (let i = 1; i <= n; i++) parts.push(i);
console.log(`sec=${parts.join("-")}`);
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
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append("-");
            sb.append(i);
        }
        System.out.println("sec=" + sb);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    if (i > 1) sb.Append("-");
    sb.Append(i);
}
Console.WriteLine($"sec={sb}");
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
	var sb strings.Builder
	for i := 1; i <= n; i++ {
		if i > 1 {
			sb.WriteString("-")
		}
		sb.WriteString(strconv.Itoa(i))
	}
	fmt.Printf("sec=%s\n", sb.String())
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let parts: Vec<String> = (1..=n).map(|i| i.to_string()).collect();
    println!("sec={}", parts.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("sec=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", i);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL construye la secuencia con un CTE recursivo y group_concat (ilustrativo, n=5).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 5
)
SELECT 'sec=' || group_concat(i, '-') AS resultado FROM seq;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$parts = [];
for ($i = 1; $i <= $n; $i++) {
    $parts[] = $i;
}
echo "sec=" . implode("-", $parts) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `'-'.join(...)` (Python), `StringBuilder` (Java/C#), `strings.Builder` (Go). |
| Semántica | Java/C#/Go usan builders mutables; Python/Rust juntan una lista al final. |
| Paradigmática | SQL usa `group_concat` sobre filas generadas, no un bucle. |

## 🧬 El concepto en la familia

En Ruby `(1..n).to_a.join('-')`. En Haskell `intercalate "-" (map show [1..n])`, puramente inmutable. En C++ un `std::ostringstream`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 054
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Concatenar con `+` en bucle grande** → causa: recrear la cadena cada vuelta (O(n²)) → solución: usar un builder mutable o juntar al final
- **Olvidar el caso n=1** → causa: poner un guion de más → solución: no añadir separador antes del primer elemento

## ❓ Preguntas frecuentes

- **¿Siempre es mejor mutar?** Para construir por partes, el builder es eficiente; para compartir datos, la inmutabilidad es más segura.
- **¿Por qué las cadenas suelen ser inmutables?** Seguridad y para poder compartirlas/hashearlas sin copiar.

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

> [⏮️ Clase 053](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 055 ⏭️](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md)
