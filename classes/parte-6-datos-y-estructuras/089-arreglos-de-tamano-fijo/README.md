# Clase 089 — Arreglos de tamaño fijo

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **arreglo de tamaño fijo**: una secuencia contigua con un número de elementos conocido. Es la estructura más básica y la más cercana a la memoria.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Declarar y recorrer un arreglo fijo.
2. Acumular suma y máximo.
3. Reconocer el acceso por índice.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arreglo fijo | Tamaño conocido, memoria contigua |
| 2 | Índice | Acceso por posición (base 0) |
| 3 | Recorrido | Visitar cada posición |

## 📖 Definiciones y características

- **Arreglo** — colección de elementos contiguos indexados. Clave: acceso O(1) por índice.
- **Tamaño fijo** — número de elementos definido al crear. Clave: no crece.
- **Índice** — posición de un elemento, empezando en 0. Clave: `arr[0]` es el primero.

## 🧩 Situación

Un arreglo fijo de 3 sensores, 12 meses, 7 días: cuando el tamaño se conoce, el arreglo fijo es la estructura más eficiente.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b c` (tres enteros)
- **Salida** (stdout): `suma=<a+b+c> max=<el mayor>`
- **Regla:** suma y máximo de los tres elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8 max=4` |
| `10 5 2` | `suma=17 max=10` |
| `1 1 1` | `suma=3 max=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER arr[3]
suma <- Σ arr ; max <- MAX(arr)
ESCRIBIR suma, max
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b, c = map(int, sys.stdin.readline().split())
arr = [a, b, c]
print(f"suma={sum(arr)} max={max(arr)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const arr = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const arr: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
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
        int[] arr = new int[3];
        for (int i = 0; i < 3; i++) arr[i] = Integer.parseInt(p[i]);
        int suma = 0, max = arr[0];
        for (int x : arr) {
            suma += x;
            if (x > max) max = x;
        }
        System.out.println("suma=" + suma + " max=" + max);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] arr = p.Take(3).Select(int.Parse).ToArray();
Console.WriteLine($"suma={arr.Sum()} max={arr.Max()}");
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
	f := strings.Fields(line)
	var arr [3]int
	for i := 0; i < 3; i++ {
		arr[i], _ = strconv.Atoi(f[i])
	}
	suma, max := 0, arr[0]
	for _, x := range arr {
		suma += x
		if x > max {
			max = x
		}
	}
	fmt.Printf("suma=%d max=%d\n", suma, max)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let arr: [i64; 3] = [v[0], v[1], v[2]];
    let suma: i64 = arr.iter().sum();
    let max = *arr.iter().max().unwrap();
    println!("suma={suma} max={max}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long arr[3];
    if (scanf("%ld %ld %ld", &arr[0], &arr[1], &arr[2]) != 3) return 1;
    long suma = 0, max = arr[0];
    for (int i = 0; i < 3; i++) {
        suma += arr[i];
        if (arr[i] > max) max = arr[i];
    }
    printf("suma=%ld max=%ld\n", suma, max);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: agrega sobre filas, no índices.
WITH arr(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d max=%d', sum(x), max(x)) AS resultado FROM arr;
```

### PHP · `php main.php`

```php
<?php
[$a, $b, $c] = preg_split('/\s+/', trim(fgets(STDIN)));
$arr = [(int) $a, (int) $b, (int) $c];
echo "suma=" . array_sum($arr) . " max=" . max($arr) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[a, b, c]` (Python/JS), `int[]` (Java/C#), `[i64; 3]` (Rust), `long[3]` (C). |
| Semántica | En C el tamaño es parte del tipo; en Python/JS el arreglo es dinámico. |
| Paradigmática | SQL agrega sobre filas, no índices. |

## 🧬 El concepto en la familia

En Go `[3]int` es fijo y `[]int` es slice dinámico. En C++ `std::array<int,3>`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 089
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Salirse del índice** → causa: acceso fuera de rango → solución: recorrer solo dentro del tamaño
- **Confundir fijo con dinámico** → causa: esperar que crezca → solución: usar lista/vector si el tamaño cambia

## ❓ Preguntas frecuentes

- **¿Por qué base 0?** El índice es un desplazamiento desde el inicio; el primero está a distancia 0.
- **¿Arreglo o lista?** Arreglo fijo si el tamaño es constante; lista si varía (siguiente clase).

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 088](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 090 ⏭️](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md)
