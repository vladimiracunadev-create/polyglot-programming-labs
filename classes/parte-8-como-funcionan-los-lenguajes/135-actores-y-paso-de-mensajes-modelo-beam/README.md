# Clase 135 — Actores y paso de mensajes (modelo BEAM)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **modelo de actores y el paso de mensajes** (la máquina BEAM de Erlang/Elixir): actores aislados sin memoria compartida que se comunican por mensajes. Un actor acumula la suma recibiendo un mensaje por número.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el modelo de actores.
2. Simular el paso de mensajes.
3. Contrastar actores con memoria compartida.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Actor | Proceso aislado con estado propio |
| 2 | Mensaje | Única forma de comunicarse |
| 3 | Sin memoria compartida | No hay condiciones de carrera |

## 📖 Definiciones y características

- **Actor** — unidad concurrente con estado propio que solo se comunica por mensajes. Clave: aislamiento.
- **Paso de mensajes** — enviar datos a un actor en vez de compartir memoria. Clave: sin carreras.
- **BEAM** — la máquina virtual de Erlang/Elixir, optimizada para millones de actores. Clave: tolerancia a fallos.

## 🧩 Situación

En Erlang/Elixir no hay memoria compartida: cada actor tiene su estado y recibe mensajes. Un actor 'acumulador' suma cada número que le llega, sin riesgo de condiciones de carrera.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `total=<suma de todos>`
- **Regla:** cada número es un mensaje al actor; el actor acumula

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `total=6` |
| `5` | `total=5` |
| `10 20` | `total=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA CADA número: enviar mensaje al actor ; el actor suma a su estado
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


class Acumulador:  # actor con estado propio
    def __init__(self):
        self.total = 0

    def recibir(self, mensaje):
        self.total += mensaje


nums = [int(x) for x in sys.stdin.read().split()]
actor = Acumulador()
for m in nums:
    actor.recibir(m)
print(f"total={actor.total}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m) { this.total += m; } };
const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m: number) { this.total += m; } };
const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Acumulador {
        long total = 0;
        void recibir(int m) { total += m; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Acumulador actor = new Acumulador();
        for (String s : p) actor.recibir(Integer.parseInt(s));
        System.out.println("total=" + actor.total);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

var actor = new Acumulador();
foreach (string s in Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries))
    actor.Recibir(int.Parse(s));
Console.WriteLine($"total={actor.Total}");

class Acumulador {
    public long Total { get; private set; }
    public void Recibir(int m) => Total += m;
}
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
	buzon := make(chan int, 64)
	done := make(chan int64)
	go func() { // actor: acumula los mensajes de su buzón
		var total int64
		for m := range buzon {
			total += int64(m)
		}
		done <- total
	}()
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		buzon <- n
	}
	close(buzon)
	fmt.Printf("total=%d\n", <-done)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

struct Acumulador {
    total: i64,
}

impl Acumulador {
    fn recibir(&mut self, mensaje: i64) {
        self.total += mensaje;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut actor = Acumulador { total: 0 };
    for x in s.split_whitespace() {
        actor.recibir(x.parse().unwrap());
    }
    println!("total={}", actor.total);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long total = 0, m;
    while (scanf("%ld", &m) == 1) {
        total += m; /* el 'actor' acumula cada mensaje */
    }
    printf("total=%ld\n", total);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL agrega sin actores; SUM sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('total=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
class Acumulador {
    public int $total = 0;
    public function recibir($m) { $this->total += $m; }
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$actor = new Acumulador();
foreach ($nums as $m) {
    $actor->recibir($m);
}
echo "total={$actor->total}\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | En el núcleo se simula con una función que acumula; en Elixir, un proceso real. |
| Semántica | El actor no comparte estado: recibe mensajes uno a uno. |
| Paradigmática | SQL agrega sin actores. |

## 🧬 El concepto en la familia

Erlang y Elixir (BEAM) son los referentes; también Akka (JVM) y el modelo de actores en muchos frameworks.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 135
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Compartir estado entre actores** → causa: rompe el aislamiento → solución: comunicar solo por mensajes
- **Buzón que crece sin control** → causa: actor saturado → solución: procesar los mensajes a ritmo suficiente

## ❓ Preguntas frecuentes

- **¿Actor o hilo?** El actor no comparte memoria: se comunica por mensajes, evitando muchos errores.
- **¿Qué es 'let it crash'?** Dejar morir un actor con error y reiniciarlo desde un supervisor.

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

> [⏮️ Clase 134](../../parte-8-como-funcionan-los-lenguajes/134-tareas-corrutinas-y-canales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 136 ⏭️](../../parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md)
