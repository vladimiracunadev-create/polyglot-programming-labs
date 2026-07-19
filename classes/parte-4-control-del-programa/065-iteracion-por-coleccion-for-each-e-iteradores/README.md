# Clase 065 — Iteración por colección: for-each e iteradores

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Recorrer una colección con `for-each` (para cada elemento), sin gestionar índices. Es la forma idiomática de procesar listas en casi todos los lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una colección con for-each.
2. Acumular un resultado sobre todos los elementos.
3. Leer una lista de longitud variable.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for-each | Para cada elemento, sin índice |
| 2 | Colección | Una secuencia de valores |
| 3 | Acumulación | Sumar recorriendo |
| 4 | Longitud variable | No se sabe cuántos hay de antemano |

## 📖 Definiciones y características

- **for-each** — bucle que recorre cada elemento de una colección. Clave: sin índice manual.
- **Colección** — estructura que agrupa varios valores (lista, arreglo). Clave: se recorre en orden.
- **Iterar** — visitar cada elemento una vez. Clave: base del procesamiento de datos.
- **Acumulación** — reunir un resultado (suma) recorriendo. Clave: patrón universal.

## 🧩 Situación

Sumar una lista de precios, contar elementos, buscar un máximo: todo empieza recorriendo la colección. El for-each expresa 'para cada elemento' sin el ruido del índice.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma = Σ elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8` |
| `10 20 30` | `suma=60` |
| `5` | `suma=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
suma <- 0
PARA CADA x EN lista: suma <- suma + x
ESCRIBIR "suma=" suma
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
for (const x of nums) {
  suma += x;
}
console.log(`suma=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
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
        String[] p = br.readLine().trim().split("\\s+");
        long suma = 0;
        for (String s : p) {
            suma += Integer.parseInt(s);
        }
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
foreach (string s in p) {
    suma += int.Parse(s);
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
	data, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	suma := 0
	for _, s := range strings.Fields(data) {
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
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut suma = 0i64;
    for x in &nums {
        suma += x;
    }
    println!("suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega sobre las filas, sin bucle.
WITH nums(x) AS (VALUES (3), (1), (4))
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
| Sintáctica | `for x in lista` (Python) vs. `for (int x : arr)` (Java) vs. `for x in &v` (Rust). |
| Semántica | Todos recorren sin índice; C aún usa índice o puntero. |
| Paradigmática | SQL suma con `SUM()` sobre filas, sin bucle explícito. |

## 🧬 El concepto en la familia

En Ruby `lista.each` o `lista.sum`. En Go `for _, x := range xs`. Kotlin `for (x in xs)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 065
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar índice cuando no hace falta** → causa: código más largo y con más errores → solución: usar for-each cuando solo necesitas el valor
- **Olvidar inicializar el acumulador** → causa: resultado incorrecto → solución: empezar la suma en 0

## ❓ Preguntas frecuentes

- **¿for-each o for con índice?** for-each si solo necesitas el valor; con índice si también necesitas la posición.
- **¿Cómo leo una lista de tamaño desconocido?** Leyendo toda la línea/entrada y separando por espacios.

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

> [⏮️ Clase 064](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 066 ⏭️](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md)
