# Clase 121 — Concurrente: hilos, tareas y canales

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Asomarse al paradigma **concurrente**: hacer varias cosas a la vez con hilos, tareas o canales. Sumar una lista puede repartirse entre trabajadores; el resultado combinado es la suma total.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la idea de dividir el trabajo.
2. Reconocer hilos, tareas y canales.
3. Combinar resultados parciales.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Concurrencia | Varias cosas a la vez |
| 2 | Dividir y combinar | Repartir el trabajo |
| 3 | Hilos, tareas, canales | Primitivas por lenguaje |

## 📖 Definiciones y características

- **Concurrencia** — estructurar el programa como tareas que progresan a la vez. Clave: aprovecha varios núcleos.
- **Hilo/goroutine** — unidad de ejecución concurrente. Clave: comparte o no memoria según el modelo.
- **Combinar** — reunir los resultados parciales en el final. Clave: la suma total.

## 🧩 Situación

Sumar millones de números, procesar imágenes o atender miles de conexiones: repartir el trabajo entre hilos o tareas aprovecha varios núcleos. El resultado combinado es el mismo, más rápido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma total>`
- **Regla:** repartir la lista, sumar por partes, combinar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma=10` |
| `5` | `suma=5` |
| `10 20 30` | `suma=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
dividir lista ; sumar cada parte (concurrente) ; combinar sumas
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
# Visión concurrente: dividir en dos mitades y combinar.
medio = len(nums) // 2
parcial1 = sum(nums[:medio])
parcial2 = sum(nums[medio:])
print(f"suma={parcial1 + parcial2}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const medio = Math.floor(nums.length / 2);
const p1 = nums.slice(0, medio).reduce((a, b) => a + b, 0);
const p2 = nums.slice(medio).reduce((a, b) => a + b, 0);
console.log(`suma=${p1 + p2}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const medio = Math.floor(nums.length / 2);
const p1 = nums.slice(0, medio).reduce((a, b) => a + b, 0);
const p2 = nums.slice(medio).reduce((a, b) => a + b, 0);
console.log(`suma=${p1 + p2}`);
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
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int medio = nums.length / 2;
        long p1 = 0, p2 = 0;
        for (int i = 0; i < medio; i++) p1 += nums[i];
        for (int i = medio; i < nums.length; i++) p2 += nums[i];
        System.out.println("suma=" + (p1 + p2));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int medio = nums.Length / 2;
long p1 = nums.Take(medio).Sum(x => (long) x);
long p2 = nums.Skip(medio).Sum(x => (long) x);
Console.WriteLine($"suma={p1 + p2}");
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
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	medio := len(nums) / 2
	ch := make(chan int, 2)
	sumar := func(parte []int) {
		s := 0
		for _, x := range parte {
			s += x
		}
		ch <- s
	}
	go sumar(nums[:medio])
	go sumar(nums[medio:])
	s1 := <-ch
	s2 := <-ch
	fmt.Printf("suma=%d\n", s1+s2)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let medio = nums.len() / 2;
    let p1: i64 = nums[..medio].iter().sum();
    let p2: i64 = nums[medio..].iter().sum();
    println!("suma={}", p1 + p2);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int medio = n / 2;
    long p1 = 0, p2 = 0;
    for (int i = 0; i < medio; i++) p1 += v[i];
    for (int i = medio; i < n; i++) p2 += v[i];
    printf("suma=%ld\n", p1 + p2);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el motor decide el paralelismo; aquí, SUM.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$medio = intdiv(count($nums), 2);
$p1 = array_sum(array_slice($nums, 0, $medio));
$p2 = array_sum(array_slice($nums, $medio));
echo "suma=" . ($p1 + $p2) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | hilos (Java/C#), goroutines+canales (Go), async (Rust), workers (JS). |
| Semántica | El resultado es determinista; el orden de ejecución no. |
| Paradigmática | SQL delega el paralelismo al motor. |

## 🧬 El concepto en la familia

Go (CSP con goroutines/canales) y Erlang/Elixir (actores) son los referentes de la concurrencia segura.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 121
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin sincronizar** → causa: condiciones de carrera → solución: preferir mensajes o sumas parciales independientes
- **Sobre-paralelizar tareas pequeñas** → causa: el coste de coordinar supera la ganancia → solución: paralelizar solo cuando compensa

## ❓ Preguntas frecuentes

- **¿Concurrencia = paralelismo?** No exactamente: concurrencia es estructurar tareas; paralelismo es ejecutarlas a la vez.
- **¿El resultado cambia?** El valor no; el orden de ejecución sí puede variar.

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

> [⏮️ Clase 120](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 122 ⏭️](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md)
