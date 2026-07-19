# Clase 064 — Iteración por rango: for clásico y for-range

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el bucle `for` cuando el número de vueltas se conoce. El factorial multiplica de 1 a n y muestra el `for` clásico y el `for`-range de cada lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle for con contador.
2. Acumular un producto.
3. Reconocer el for-range frente al for clásico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for clásico | init; condición; incremento |
| 2 | for-range | Recorrer un rango directamente |
| 3 | Acumular un producto | Multiplicar en cada vuelta |
| 4 | Caso base 0! = 1 | El bucle no se ejecuta y queda 1 |

## 📖 Definiciones y características

- **for** — bucle con inicialización, condición e incremento. Clave: para un número conocido de vueltas.
- **for-range** — recorrer un rango o colección sin gestionar el índice (Python, Rust, Go). Clave: menos errores.
- **Factorial** — n! = 1·2·…·n. Clave: 0! = 1 por definición.
- **Acumulador de producto** — variable que empieza en 1 y se multiplica. Clave: 1 es el neutro del producto.

## 🧩 Situación

El factorial aparece en combinatoria y probabilidad. Con un for de 1 a n se calcula directo; el caso `0! = 1` sale gratis porque el bucle no se ejecuta y el acumulador queda en 1.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 20)
- **Salida** (stdout): `factorial=<n!>`
- **Regla:** n! = 1·2·…·n ; 0! = 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `factorial=120` |
| `1` | `factorial=1` |
| `0` | `factorial=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
f <- 1
PARA i de 1 a n: f <- f*i
ESCRIBIR "factorial=" f
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
f = 1
for i in range(1, n + 1):
    f *= i
print(f"factorial={f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
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
        long f = 1;
        for (int i = 1; i <= n; i++) {
            f *= i;
        }
        System.out.println("factorial=" + f);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long f = 1;
for (int i = 1; i <= n; i++) {
    f *= i;
}
Console.WriteLine($"factorial={f}");
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
	var f int64 = 1
	for i := 1; i <= n; i++ {
		f *= int64(i)
	}
	fmt.Printf("factorial=%d\n", f)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut f: i64 = 1;
    for i in 1..=n {
        f *= i;
    }
    println!("factorial={f}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long f = 1;
    for (long i = 1; i <= n; i++) {
        f *= i;
    }
    printf("factorial=%ld\n", f);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: factorial con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE fact(i, f) AS (
    VALUES (1, 1)
    UNION ALL SELECT i + 1, f * (i + 1) FROM fact WHERE i < 5
)
SELECT printf('factorial=%d', f) AS resultado FROM fact ORDER BY i DESC LIMIT 1;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$f = 1;
for ($i = 1; $i <= $n; $i++) {
    $f *= $i;
}
echo "factorial=$f\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `for i in range(1,n+1)` (Python) vs. `for(i=1;i<=n;i++)` (C/Java) vs. `for i in 1..=n` (Rust). |
| Semántica | El for-range evita el error de límites; el for clásico lo deja en tus manos. |
| Paradigmática | SQL usa un CTE recursivo o una agregación, no un for. |

## 🧬 El concepto en la familia

En Ruby `(1..n).reduce(1, :*)`. En Go `for i := 1; i <= n; i++`. Kotlin `for (i in 1..n)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 064
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Empezar el acumulador en 0** → causa: el producto siempre da 0 → solución: iniciar el acumulador de producto en 1
- **Límites del rango mal** → causa: un factor de más o de menos → solución: verificar con 0! y 1! que el rango es correcto

## ❓ Preguntas frecuentes

- **¿Por qué long y no int?** El factorial crece muy rápido; 21! ya desborda 64 bits. Aquí n<=20.
- **¿0! por qué es 1?** Es el producto vacío: el neutro de la multiplicación es 1.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 063](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 065 ⏭️](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md)
