# Clase 109 — Procedimental y modular

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **paradigma procedimental y modular**: descomponer el programa en procedimientos con nombre que se llaman entre sí. Es el imperativo organizado en unidades reutilizables.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encapsular un cálculo en un procedimiento.
2. Llamarlo desde el programa principal.
3. Reconocer la modularidad procedimental.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Procedimiento | Bloque con nombre reutilizable |
| 2 | Modularidad | Dividir en unidades |
| 3 | Reutilización | Llamar en vez de repetir |

## 📖 Definiciones y características

- **Procedimental** — paradigma que organiza el código en procedimientos/funciones. Clave: imperativo modular.
- **Procedimiento** — unidad con nombre que realiza una tarea. Clave: se invoca cuando se necesita.
- **Modularidad** — dividir el problema en piezas manejables. Clave: cada una con una responsabilidad.

## 🧩 Situación

En vez de un `main` gigante, se define `promedio(lista)` y se llama. El estilo procedimental (C, Pascal) organiza el imperativo en procedimientos.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `promedio=<suma dividida entre la cantidad, entera>`
- **Regla:** promedio = suma / cantidad (división entera)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 4 6` | `promedio=4` |
| `10` | `promedio=10` |
| `3 5` | `promedio=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PROCEDIMIENTO promedio(lista): DEVOLVER suma(lista)/|lista|
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def promedio(lista):
    return sum(lista) // len(lista)


nums = [int(x) for x in sys.stdin.read().split()]
print(f"promedio={promedio(nums)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function promedio(lista) {
  const suma = lista.reduce((a, b) => a + b, 0);
  return Math.trunc(suma / lista.length);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`promedio=${promedio(nums)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function promedio(lista: number[]): number {
  const suma = lista.reduce((a, b) => a + b, 0);
  return Math.trunc(suma / lista.length);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`promedio=${promedio(nums)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long promedio(int[] a) {
        long suma = 0;
        for (int x : a) suma += x;
        return suma / a.length;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        System.out.println("promedio=" + promedio(nums));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

long Promedio(int[] a) => a.Sum(x => (long) x) / a.Length;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
Console.WriteLine($"promedio={Promedio(nums)}");
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

func promedio(a []int) int {
	suma := 0
	for _, x := range a {
		suma += x
	}
	return suma / len(a)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("promedio=%d\n", promedio(nums))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn promedio(a: &[i64]) -> i64 {
    let suma: i64 = a.iter().sum();
    suma / a.len() as i64
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("promedio={}", promedio(&nums));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long suma = 0;
    for (int i = 0; i < n; i++) suma += v[i];
    printf("promedio=%ld\n", suma / n);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: AVG con división entera.
WITH nums(x) AS (VALUES (2), (4), (6))
SELECT printf('promedio=%d', sum(x) / count(*)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function promedio($a) {
    return intdiv(array_sum($a), count($a));
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "promedio=" . promedio($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Cada lenguaje define el procedimiento a su manera. |
| Semántica | El procedimiento agrupa pasos imperativos bajo un nombre. |
| Paradigmática | SQL usa AVG (declarativo). |

## 🧬 El concepto en la familia

C y Pascal son los ejemplos clásicos del estilo procedimental; casi todos lo soportan.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 109
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dividir sin controlar cantidad 0** → causa: división por cero → solución: aquí siempre hay elementos
- **Todo en el main** → causa: sin modularidad → solución: extraer procedimientos con responsabilidad clara

## ❓ Preguntas frecuentes

- **¿Procedimiento o función?** Un procedimiento actúa; una función devuelve valor. Aquí devolvemos el promedio.
- **¿Procedimental es viejo?** Es la base; sigue vigente y presente en todos los lenguajes.

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

> [⏮️ Clase 108](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 110 ⏭️](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md)
