# Clase 063 — Iteración por condición: while y do-while

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el bucle `while`: repetir mientras una condición sea verdadera. Es el bucle más básico y el que subyace a todos los demás.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle while con una condición de parada.
2. Actualizar el estado en cada vuelta.
3. Evitar el bucle infinito.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | while | Repetir mientras se cumpla una condición |
| 2 | Condición de parada | Cuándo termina el bucle |
| 3 | Acumulador | Sumar en cada vuelta |
| 4 | Bucle infinito | El peligro de no avanzar |

## 📖 Definiciones y características

- **while** — bucle que repite mientras la condición sea verdadera. Clave: comprueba antes de cada vuelta.
- **do-while** — variante que ejecuta al menos una vez (comprueba al final). Clave: no en todos los lenguajes.
- **Condición de parada** — lo que hace terminar el bucle. Clave: algo debe acercarse a ella.
- **Acumulador** — variable que reúne el resultado. Clave: se actualiza cada vuelta.

## 🧩 Situación

Sumar 1..n con while obliga a manejar el contador y la condición a mano. Si el contador no avanza, el bucle no termina: el error más clásico de los bucles.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `1` | `suma=1` |
| `10` | `suma=55` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
suma <- 0 ; i <- 1
MIENTRAS i <= n: suma <- suma+i ; i <- i+1
ESCRIBIR "suma=" suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
suma = 0
i = 1
while i <= n:
    suma += i
    i += 1
print(f"suma={suma}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
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
        int n = Integer.parseInt(br.readLine().trim());
        long suma = 0;
        int i = 1;
        while (i <= n) {
            suma += i;
            i++;
        }
        System.out.println("suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
int i = 1;
while (i <= n) {
    suma += i;
    i++;
}
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	suma := 0
	i := 1
	for i <= n {
		suma += i
		i++
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
    let n: i64 = s.trim().parse().unwrap();
    let mut suma = 0i64;
    let mut i = 1i64;
    while i <= n {
        suma += i;
        i += 1;
    }
    println!("suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    long i = 1;
    while (i <= n) {
        suma += i;
        i++;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: suma 1..n con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 10
)
SELECT printf('suma=%d', sum(i)) AS resultado FROM seq;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
$i = 1;
while ($i <= $n) {
    $suma += $i;
    $i++;
}
echo "suma=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `while cond:` (Python) vs. `while (cond) {}` (C/Java/JS). |
| Semántica | El while comprueba antes; el do-while (C/Java/JS) al menos una vez. |
| Paradigmática | SQL evita el bucle: suma con un CTE recursivo o una fórmula. |

## 🧬 El concepto en la familia

En Ruby `while i <= n`. En Go solo hay `for` (que hace de while): `for i <= n`. Rust `while i <= n`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 063
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No avanzar el contador** → causa: bucle infinito → solución: asegurar que algo cambia hacia la condición de parada
- **Condición mal puesta** → causa: una vuelta de más o de menos (off-by-one) → solución: verificar los límites con un caso pequeño

## ❓ Preguntas frecuentes

- **¿while o for?** El for es más compacto cuando el número de vueltas se conoce; el while, cuando depende de una condición.
- **¿Go no tiene while?** No como palabra: usa `for cond {}`, que es lo mismo.

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

> [⏮️ Clase 062](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 064 ⏭️](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md)
