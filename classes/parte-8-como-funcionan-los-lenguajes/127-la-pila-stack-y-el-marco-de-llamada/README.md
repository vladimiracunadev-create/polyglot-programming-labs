# Clase 127 — La pila (stack) y el marco de llamada

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Toda función que llamas necesita recordar dos cosas: sus datos locales y a dónde volver cuando termine. El mecanismo que lo hace posible es la **pila de llamadas (call stack)** y su unidad, el **marco de llamada (stack frame)**. Esta clase lo hace visible con una suma recursiva `1+…+n` que reporta además su profundidad, porque la recursión es la forma más limpia de *apilar* marcos: cada `sumar(n)` deja su marco activo mientras espera el resultado de `sumar(n-1)`, y con `n` invocaciones anidadas hay `n` marcos vivos a la vez. El *porqué* es que esta estructura, descrita al detalle por Bryant & O'Hallaron en su capítulo sobre el *procedimiento* y la organización del *stack frame* en x86-64, explica fenómenos que verás toda tu carrera: el *stack overflow* de una recursión sin caso base, por qué las variables locales «desaparecen» al volver de una función, cómo un depurador reconstruye el *backtrace*, y por qué la pila es rapidísima comparada con el heap. Es una región LIFO (*last-in, first-out*) que crece y decrece con puro movimiento de un puntero.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Describir qué guarda un marco de llamada: parámetros, variables locales y dirección de retorno.
2. Relacionar la recursión con marcos apilados y la profundidad con el número de marcos vivos.
3. Explicar el desbordamiento de pila y sus causas.
4. Contrastar la pila (automática, LIFO, acotada) con el heap (flexible, gestionado).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila de llamadas | Registra las funciones activas y su orden de retorno |
| 2 | Marco de llamada | Aísla los locales y el punto de retorno de cada invocación |
| 3 | Profundidad | Cuántos marcos coexisten; su límite provoca el desbordamiento |

## 📖 Definiciones y características

La **pila (stack)** es la región de memoria donde el runtime coloca los marcos de las funciones activas. Su disciplina es LIFO: el último marco que entra es el primero que sale, exactamente el orden en que las llamadas se anidan y retornan. Su gran virtud, como subrayan Bryant & O'Hallaron, es la velocidad: reservar espacio para un marco es restar al puntero de pila (*stack pointer*), y liberarlo es sumarlo de vuelta —una sola instrucción, sin buscar hueco ni contabilizar nada.

El **marco de llamada (stack frame)** es el bloque que una invocación reserva para sí: sus parámetros, sus variables locales y —crucial— la *dirección de retorno*, el punto del código al que la CPU debe saltar cuando la función acabe. Cuando `sumar(3)` llama a `sumar(2)`, el marco de `sumar(3)` permanece en la pila, congelado, guardando su `n=3` y su promesa de sumar `3` al resultado que espera. Por eso al volver de una función sus locales dejan de existir: su marco se desapiló.

El **desbordamiento de pila (stack overflow)** ocurre cuando se apilan más marcos de los que caben en el espacio reservado (típicamente unos pocos MB). Una recursión sin caso base apila marcos indefinidamente y lo provoca; también una recursión correcta pero demasiado profunda. Es un límite físico, no un error lógico: por eso Python lo anticipa con `sys.setrecursionlimit` y por eso los lenguajes funcionales optimizan la *recursión de cola* para no crecer la pila.

## 🧩 Situación

Un programa recursivo funciona perfecto con `n=100` y revienta con `n=1_000_000` lanzando un *stack overflow*. Sin el modelo de la pila, parece magia negra. Con él, es aritmética: un millón de marcos vivos a la vez no caben en los megabytes de pila que el sistema operativo asignó al hilo. Sumar `1..n` con recursión, reportando `profundidad=n`, hace tangible esa correspondencia uno-a-uno entre llamadas anidadas y marcos apilados, y prepara el terreno para entender por qué a veces conviene convertir recursión en iteración.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (1 <= n <= 1000)
- **Salida** (stdout): `suma=<1+...+n> profundidad=<n>`
- **Regla:** suma recursiva; profundidad = número de marcos = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15 profundidad=5` |
| `3` | `suma=6 profundidad=3` |
| `1` | `suma=1 profundidad=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
sumar(n) = n + sumar(n-1) ; sumar(0) = 0 ; profundidad = n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

sys.setrecursionlimit(5000)


def sumar(n):
    return 0 if n == 0 else n + sumar(n - 1)


n = int(sys.stdin.readline())
print(f"suma={sumar(n)} profundidad={n}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function sumar(n) {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function sumar(n: number): number {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long sumar(int n) {
        return n == 0 ? 0 : n + sumar(n - 1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("suma=" + sumar(n) + " profundidad=" + n);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long Sumar(int n) => n == 0 ? 0 : n + Sumar(n - 1);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={Sumar(n)} profundidad={n}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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

func sumar(n int) int64 {
	if n == 0 {
		return 0
	}
	return int64(n) + sumar(n-1)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("suma=%d profundidad=%d\n", sumar(n), n)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn sumar(n: i64) -> i64 {
    if n == 0 {
        0
    } else {
        n + sumar(n - 1)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} profundidad={}", sumar(n), n);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long sumar(long n) {
    return n == 0 ? 0 : n + sumar(n - 1);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld profundidad=%ld\n", sumar(n), n);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: recursión con CTE (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d profundidad=%d', sum(i), max(i)) AS resultado FROM r;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function sumar($n) {
    return $n === 0 ? 0 : $n + sumar($n - 1);
}

$n = (int) trim(fgets(STDIN));
echo "suma=" . sumar($n) . " profundidad=$n\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Todas las implementaciones comparten la misma recurrencia `sumar(n) = n + sumar(n-1)` con caso base `sumar(0) = 0`, y todas apilan `n` marcos para `sumar(n)`. Las diferencias revelan cómo cada lenguaje trata el límite de la pila.

En **Python**, la primera línea significativa es `sys.setrecursionlimit(5000)`. Es una confesión honesta del modelo: CPython impone un tope artificial a la profundidad de recursión —por defecto ~1000— para transformar un *stack overflow* nativo (que colgaría el proceso) en una excepción `RecursionError` manejable. Sin ese ajuste, `sumar(2000)` fallaría no por lógica sino por chocar contra el límite. La función `sumar` apila un marco de intérprete por llamada, y `profundidad={n}` reporta cuántos hubo vivos en el punto más hondo.

En **C**, `long sumar(long n)` apila marcos *nativos* reales sobre la pila del hilo. Cada marco de C es minúsculo —unos pocos bytes para `n` y la dirección de retorno—, y no hay red de seguridad: si `n` fuera lo bastante grande, el programa no lanzaría una excepción sino que escribiría más allá del final de la pila y moriría con un *segmentation fault*. Este es el modelo que Bryant & O'Hallaron describen en el metal: la pila crece hacia direcciones bajas y el `stack pointer` se mueve con cada `call` y `ret`.

En **Go**, `func sumar(n int) int64` corre sobre una *goroutine* con una pila que empieza pequeña (unos KB) pero *crece dinámicamente*: el runtime detecta cuando falta espacio y realoja la pila en una región mayor, copiando los marcos. Por eso Go tolera recursiones que tumbarían a C con la misma pila fija, a cambio de un coste de gestión. Tres lenguajes, tres políticas de pila —tope artificial, pila fija nativa, pila que crece— para exactamente la misma recurrencia.

## 🔬 Comparación

| Rasgo | Cómo se comporta entre los 10 lenguajes |
|---|---|
| Tipo de marco | Nativo real en C, Rust, Go; marco de intérprete/VM en Python, PHP; de la JVM/CLR en Java, C#. |
| Límite de profundidad | Artificial y ajustable en Python (`setrecursionlimit`); pila fija del hilo en C/Rust/Java; pila que crece en Go. |
| Fallo al exceder | `RecursionError` (Python), `StackOverflowError` (Java/C#), *segfault* (C), *panic* (Rust). |
| Recursión de cola | Optimizada en algunos (funcionales, a veces C/Rust con `-O`); no garantizada en Python ni Java. |
| SQL | Sin pila visible: el CTE recursivo (`WITH RECURSIVE`) expresa la iteración de forma declarativa. |

## 🧬 El concepto en la familia

La pila de llamadas es universal, pero su relación con la recursión cambia según el paradigma. En Haskell y otros funcionales, la recursión *es* el bucle natural, y el compilador optimiza la *recursión de cola* (cuando la llamada recursiva es lo último que se hace) reutilizando el marco en vez de apilar uno nuevo —convirtiendo una recursión en un bucle de pila constante. Scheme lo garantiza por norma del lenguaje. Python y Java, en cambio, deliberadamente *no* la optimizan, priorizando *backtraces* legibles sobre la eficiencia de pila. Entender el marco de llamada te permite predecir cuáles de estos lenguajes sobreviven a una recursión profunda y cuáles exigen reescribirla como iteración.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 127
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Recursión sin caso base** → causa: nada detiene el anidamiento, la pila se llena → solución: definir y verificar el caso base (`sumar(0) = 0`) antes de la llamada recursiva.
- **Recursión correcta pero demasiado profunda** → causa: incluso con caso base, `n` enorme excede la pila del hilo → solución: convertir a iteración, o a recursión de cola si el lenguaje la optimiza.
- **Confiar en la optimización de cola donde no existe** → causa: asumir que Python o Java reciclan el marco → solución: comprobar que el lenguaje la garantiza; si no, reescribir el bucle a mano.

## ❓ Preguntas frecuentes

- **¿Por qué existe la pila?** Para que cada función activa recuerde sus datos locales y su dirección de retorno sin pisar a las demás, con reserva y liberación en una sola instrucción.
- **¿Pila o heap?** La pila guarda marcos de vida ligada a la llamada (rápida, automática, LIFO, acotada); el heap guarda datos de vida flexible que sobreviven al retorno (clase 128).
- **¿Qué es un *backtrace*?** La lista de marcos vivos en el momento de un error: es literalmente la pila de llamadas leída de arriba abajo, y por eso un depurador puede mostrártela.

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

> [⏮️ Clase 126](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 128 ⏭️](../../parte-8-como-funcionan-los-lenguajes/128-el-heap-y-la-asignacion-dinamica/README.md)
