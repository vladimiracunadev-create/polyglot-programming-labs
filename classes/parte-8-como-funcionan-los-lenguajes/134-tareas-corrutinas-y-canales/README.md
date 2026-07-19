# Clase 134 — Tareas, corrutinas y canales

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir **tareas, corrutinas y canales**: en vez de compartir memoria, las tareas se comunican enviando datos por canales. Un productor envía los valores y un consumidor calcula el máximo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comunicar datos por un canal (concepto).
2. Separar productor de consumidor.
3. Contrastar canales con memoria compartida.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Canal | Tubería entre tareas |
| 2 | Productor/consumidor | Uno envía, otro recibe |
| 3 | Corrutina/goroutine | Tarea ligera |

## 📖 Definiciones y características

- **Canal** — conducto para enviar datos entre tareas concurrentes. Clave: comunicar sin compartir memoria.
- **Corrutina/goroutine** — tarea ligera que el runtime planifica. Clave: miles a bajo coste (Go).
- **Productor/consumidor** — un patrón: una tarea produce datos, otra los consume. Clave: se coordinan por el canal.

## 🧩 Situación

En Go, un productor manda los números por un canal y un consumidor los procesa; no comparten variables, se comunican. Calcular el máximo así modela ese flujo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** enviar los valores por un canal; el consumidor guarda el máximo

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `max=4` |
| `5` | `max=5` |
| `10 20 5` | `max=20` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
productor envía cada valor ; consumidor actualiza el máximo
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
maximo = nums[0]
for x in nums:  # consumidor
    if x > maximo:
        maximo = x
print(f"max={maximo}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
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
        int maximo = Integer.parseInt(p[0]);
        for (String s : p) maximo = Math.max(maximo, Integer.parseInt(s));
        System.out.println("max=" + maximo);
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
Console.WriteLine($"max={nums.Max()}");
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
	ch := make(chan int, len(f))
	go func() { // productor
		for _, s := range f {
			n, _ := strconv.Atoi(s)
			ch <- n
		}
		close(ch)
	}()
	primero := true
	maximo := 0
	for x := range ch { // consumidor
		if primero || x > maximo {
			maximo = x
			primero = false
		}
	}
	fmt.Printf("max=%d\n", maximo)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let maximo = *nums.iter().max().unwrap();
    println!("max={maximo}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x, maximo;
    if (scanf("%ld", &maximo) != 1) return 1;
    while (scanf("%ld", &x) == 1) {
        if (x > maximo) maximo = x;
    }
    printf("max=%ld\n", maximo);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: MAX agrega sobre las filas.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('max=%d', max(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "max=" . max($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | canales (Go), colas/streams (otros), simple recorrido aquí. |
| Semántica | Comunicar por canal evita compartir estado mutable. |
| Paradigmática | SQL usa MAX; el motor decide el cómo. |

## 🧬 El concepto en la familia

Go (canales) y Kotlin (corrutinas + channels) son referentes; también las colas concurrentes en Java.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 134
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquearse esperando un canal** → causa: deadlock → solución: cerrar el canal o usar tamaño/estructura adecuada
- **Compartir estado además del canal** → causa: condiciones de carrera → solución: comunicar solo por el canal

## ❓ Preguntas frecuentes

- **¿Canal o memoria compartida?** El canal evita muchos errores de concurrencia al no compartir estado.
- **¿Corrutina es un hilo?** Es más ligera: muchas corrutinas se multiplexan sobre pocos hilos.

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

> [⏮️ Clase 133](../../parte-8-como-funcionan-los-lenguajes/133-concurrencia-procesos-hilos-y-memoria-compartida/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 135 ⏭️](../../parte-8-como-funcionan-los-lenguajes/135-actores-y-paso-de-mensajes-modelo-beam/README.md)
