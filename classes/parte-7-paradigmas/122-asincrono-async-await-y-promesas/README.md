# Clase 122 — Asíncrono: async/await y promesas

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase anterior repartía trabajo entre hilos que corrían de verdad a la vez. El paradigma **asíncrono** persigue un objetivo parecido —no quedarse parado esperando— pero con una filosofía opuesta: un solo hilo que, en vez de bloquearse mientras aguarda una operación lenta, la inicia, la deja en marcha y sigue haciendo otra cosa, para retomarla cuando el resultado esté listo. No hay paralelismo; hay *concurrencia sin paralelismo*. La palabra clave es *no bloquear*: cuando pides un dato a la red o al disco, no congelas el programa entero durante los milisegundos (o segundos) que tarda la respuesta.

La pieza que representa "un valor que todavía no está pero llegará" es la **promesa** (o *future*, o *task*). Es un objeto que devuelves de inmediato como un pagaré: "aquí tienes un recibo; cuando el cálculo termine, contendrá el valor". El operador `await` es lo que canjeas ese recibo: suspende tu función en ese punto, devuelve el control al **bucle de eventos** —el mismo motor que viste en la clase 119— y reanuda tu función justo donde la dejaste cuando la promesa se resuelve. Bajo el azúcar, `async/await` es una máquina de estados: el compilador trocea tu función en los puntos de `await` y guarda dónde iba para poder continuar después. Es, en el fondo, *azúcar sintáctico sobre continuaciones y callbacks*: lo que en la clase 119 escribías como pirámide de callbacks anidados, aquí se lee como código secuencial de arriba abajo.

Nuestro laboratorio reduce el paradigma a su gesto mínimo —una tarea asíncrona que calcula el doble de un número y se espera su valor— para que veas la *forma* `async/await` sin el ruido de la I/O real. El cálculo es instantáneo, pero la estructura (definir una operación asíncrona, iniciarla, esperar su resultado con `await`) es idéntica a la de leer un archivo o consultar una base de datos, que es donde este estilo despliega toda su ventaja.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir y esperar una tarea asíncrona.
2. Explicar por qué no bloquea.
3. Reconocer async/await por lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Asíncrono | No bloquear mientras se espera |
| 2 | async/await | Esperar sin bloquear el hilo |
| 3 | Tarea/promesa/future | El resultado que llegará |

## 📖 Definiciones y características

- **Asíncrono** — iniciar algo que tarda y seguir sin bloquear. Clave: eficiente para I/O.
- **async/await** — sintaxis para escribir código asíncrono como si fuera secuencial. Clave: legible.
- **Promesa/Future/Task** — objeto que representa un resultado futuro. Clave: se espera con await.

## 🧩 Situación

Leer de la red, de disco o de una base de datos tarda. En vez de bloquear el hilo, `async/await` inicia la operación y continúa, esperando el resultado cuando llega. Clave en servidores y UI.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** await doble(n) = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `6` | `resultado=12` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
async doble(x): DEVOLVER 2x ; resultado <- await doble(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys
import asyncio


async def doble(x):
    return x * 2


async def main():
    n = int(sys.stdin.readline())
    resultado = await doble(n)
    print(f"resultado={resultado}")


asyncio.run(main())
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

async function doble(x) {
  return x * 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
(async () => {
  const resultado = await doble(n);
  console.log(`resultado=${resultado}`);
})();
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

async function doble(x: number): Promise<number> {
  return x * 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
(async () => {
  const resultado: number = await doble(n);
  console.log(`resultado=${resultado}`);
})();
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException, ExecutionException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        CompletableFuture<Integer> tarea = CompletableFuture.supplyAsync(() -> n * 2);
        System.out.println("resultado=" + tarea.get());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Threading.Tasks;

async Task<int> Doble(int x) => await Task.FromResult(x * 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
int resultado = await Doble(n);
Console.WriteLine($"resultado={resultado}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

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
	// Go usa goroutines y canales en lugar de async/await.
	ch := make(chan int, 1)
	go func() { ch <- n * 2 }()
	fmt.Printf("resultado=%d\n", <-ch)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    // Sin runtime async externo, se muestra el resultado de la tarea.
    let resultado = n * 2;
    println!("resultado={resultado}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    /* C no tiene async a nivel de lenguaje; se calcula el resultado. */
    printf("resultado=%ld\n", n * 2);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene async a nivel de lenguaje.
WITH nums(n) AS (VALUES (5), (0), (6))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
// PHP es síncrono por defecto; se muestra el resultado de la tarea.
echo "resultado=" . ($n * 2) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `async/await` (JS/TS/Python/C#/Rust), goroutines+canales (Go). |
| Semántica | await no bloquea el hilo; libera para otras tareas. |
| Paradigmática | SQL no tiene async a nivel de lenguaje. |

## 🧬 El concepto en la familia

JavaScript popularizó async/await; hoy está en Python, C#, Rust y otros. Go usa goroutines en su lugar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 122
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquear en vez de esperar** → causa: desperdiciar la ventaja asíncrona → solución: usar await, no una espera activa
- **Olvidar await** → causa: obtener la promesa, no el valor → solución: esperar el resultado antes de usarlo

## ❓ Preguntas frecuentes

- **¿Async es paralelismo?** No: es no bloquear mientras se espera; puede usar un solo hilo.
- **¿Y Go?** Usa goroutines y canales en lugar de async/await, con un modelo distinto.

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

> [⏮️ Clase 121](../../parte-7-paradigmas/121-concurrente-hilos-tareas-y-canales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 123 ⏭️](../../parte-8-como-funcionan-los-lenguajes/123-del-codigo-a-la-ejecucion-fases-de-compilacion/README.md)
