# Clase 134 — Tareas, corrutinas y canales

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Los hilos de la clase anterior tienen dos problemas prácticos que ninguna dosis de disciplina resuelve. Son **caros**: cada hilo del sistema operativo reserva del orden de un megabyte de pila y cada cambio de contexto pasa por el núcleo, así que diez mil conexiones simultáneas no se atienden con diez mil hilos. Y son **peligrosos**: comunicar por memoria compartida exige candados que nadie garantiza que se tomen. Esta clase presenta la respuesta que la industria ha convergido en adoptar: tareas **ligeras**, planificadas en espacio de usuario, que se comunican por **canales** en lugar de por variables. El ejercicio —un productor que envía números y un consumidor que calcula el máximo— es el patrón productor/consumidor, el esqueleto de casi todo sistema concurrente real. El *porqué* de estudiarlo es que aquí se explica de golpe por qué Go puede lanzar un millón de goroutines, qué hace realmente `async`/`await` en Python o JavaScript, y por qué «comparte comunicando» no es un eslogan sino una consecuencia técnica: si el dato se transfiere por un canal, hay a lo sumo un dueño en cada instante y la carrera de datos desaparece.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar por qué una corrutina es órdenes de magnitud más barata que un hilo del sistema operativo.
2. Distinguir multitarea **cooperativa** de **apropiativa** y decir cuál usa cada runtime.
3. Describir qué hace un canal: transferir un valor y, además, **sincronizar** a las dos partes.
4. Diferenciar un canal sin búfer de uno con búfer y predecir cuándo bloquea cada envío.
5. Reconocer el patrón productor/consumidor y las dos formas clásicas de bloquearlo por accidente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tarea ligera (goroutine, corrutina) | Pila diminuta y planificación en espacio de usuario: cambia el orden de magnitud |
| 2 | Cooperativo frente a apropiativo | Quién decide cuándo se cede el control, y qué pasa si nadie cede |
| 3 | Canal | Transfiere el dato y coordina el ritmo en la misma operación |
| 4 | Con búfer o sin búfer | La capacidad determina si el envío es un encuentro o un depósito |
| 5 | Productor/consumidor | El patrón base, y sus interbloqueos característicos |

## 📖 Definiciones y características

Una **corrutina** —goroutine en Go, *task* en Python o Rust, corrutina en Kotlin, hilo virtual en Java 21— es una unidad de ejecución que **el runtime del lenguaje**, y no el sistema operativo, planifica. La diferencia de coste es estructural. Un hilo del SO necesita una pila de tamaño fijo reservada por adelantado (típicamente 1–8 MB de espacio virtual) y su cambio de contexto implica una transición al núcleo y el volcado de todo el estado de registros. Una goroutine arranca con una pila de unos pocos kilobytes que **crece y se encoge** dinámicamente —el compilador inserta comprobaciones al entrar en cada función—, y cambiar de una a otra es guardar unos pocos registros en espacio de usuario. Por eso un programa Go puede tener cientos de miles de goroutines vivas y un programa Java clásico se ahoga con unos miles de hilos.

El runtime que las orquesta multiplexa **M** corrutinas sobre **N** hilos del sistema. El planificador de Go se conoce como modelo G-M-P: goroutines (G) asignadas a procesadores lógicos (P), cada uno servido por un hilo del SO (M). Cuando una goroutine se bloquea en E/S, el runtime la aparta y coloca otra en el mismo hilo, de modo que el hilo nunca queda ocioso; además implementa *work stealing*, permitiendo que un procesador sin trabajo robe goroutines de la cola de otro.

Aquí entra la distinción clave entre multitarea **apropiativa** y **cooperativa**. En la apropiativa, un temporizador interrumpe la tarea sin su permiso: así funcionan los hilos del SO, y así funciona Go desde la versión 1.14, que puede desalojar una goroutine en un bucle sin llamadas. En la **cooperativa**, la tarea solo cede el control en puntos explícitos —cada `await` en Python, JavaScript o Rust—. Esto tiene una consecuencia enorme y frecuentemente mal entendida: en un runtime cooperativo, una tarea que hace un cálculo largo sin `await` **bloquea a todas las demás**. El famoso «no bloquees el bucle de eventos» es exactamente esto.

Un **canal** es una cola tipada con una propiedad que lo distingue de una cola cualquiera: además de transferir el dato, **sincroniza**. Un canal **sin búfer** (`make(chan int)`) implementa un encuentro: el emisor se bloquea hasta que hay un receptor listo y viceversa; la transferencia es un punto de cita en el que ambos coinciden. Un canal **con búfer** (`make(chan int, 10)`) permite depositar hasta su capacidad sin esperar; el emisor solo se bloquea cuando está lleno, y el receptor cuando está vacío. Esa capacidad no es un detalle de rendimiento: es el mecanismo de **contrapresión** (*backpressure*) que impide que un productor rápido agote la memoria alimentando a un consumidor lento. Cerrar un canal (`close`) es la señal de fin de datos que permite al receptor terminar su bucle en lugar de esperar para siempre.

La idea viene de lejos: los canales de Go descienden directamente del CSP (*Communicating Sequential Processes*) que Hoare formuló en 1978, y el mismo linaje pasa por Occam y por el operador `|` de las tuberías de Unix. Donovan y Kernighan articulan en *The Go Programming Language* la razón por la que este modelo reduce errores: si el valor se envía por el canal y el emisor deja de usarlo, hay **un solo dueño en cada instante** y no queda nada que proteger con candados.

## 🧩 Situación

Un servicio tiene que procesar un fichero de diez millones de líneas aplicando a cada una una llamada de red. Con un hilo por línea, el sistema muere. Con un solo hilo, tarda días. La solución canónica es un *pipeline*: una tarea lee el fichero y envía líneas a un canal; un grupo acotado de trabajadores —digamos cien corrutinas— consume de ese canal, hace la llamada y envía el resultado a un segundo canal; una tarea final agrega. La capacidad del primer canal regula la contrapresión: si los trabajadores se retrasan, el lector se bloquea solo y la memoria no crece. Este diseño no lleva un solo mutex, y el paralelismo se ajusta cambiando un número. El ejercicio de esta clase —productor que envía, consumidor que reduce a un máximo— es ese mismo esqueleto con una etapa.

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
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
maximo = nums[0]
for x in nums:  # consumidor
    if x > maximo:
        maximo = x
print(f"max={maximo}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

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

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
Console.WriteLine($"max={nums.Max()}");
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

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

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

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

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

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: MAX agrega sobre las filas.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('max=%d', max(x)) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "max=" . max($nums) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Solo **Go** implementa literalmente el modelo; el resto muestra la reducción secuencial equivalente, y conviene leerlos como el «después» de un pipeline que ya se resolvió.

En **Go**, `ch := make(chan int, len(f))` crea un canal **con búfer** de capacidad exactamente igual al número de elementos. Esa elección es deliberada y vale la pena entenderla: como el búfer nunca se llena, el productor puede depositar los `len(f)` valores sin bloquearse ni una vez, aunque el consumidor todavía no haya empezado. Si el canal fuera sin búfer (`make(chan int)`), cada envío esperaría a que el consumidor recibiera —un encuentro por valor— y el programa seguiría siendo correcto, solo que con el productor y el consumidor avanzando al mismo paso.

`go func() { ... }()` lanza la goroutine productora. Es la única palabra clave que Go dedica a la concurrencia, y su coste es una reserva de un par de kilobytes: la función arranca en paralelo y `main` continúa inmediatamente sin esperar. Dentro, el bucle envía con `ch <- n` y termina con `close(ch)`. Ese `close` es imprescindible: sin él, el `for x := range ch` del consumidor esperaría eternamente un valor más y el runtime de Go abortaría con `all goroutines are asleep - deadlock!`. Cerrar es la forma de decir «no habrá más datos», y solo el emisor puede hacerlo.

En el consumidor, `for x := range ch` itera hasta que el canal se cierra **y** se vacía. Fíjate en que ni `maximo` ni `primero` se protegen con candado alguno, y sin embargo no hay carrera: solo la goroutine principal los toca. Ese es exactamente el argumento del modelo —el estado deja de ser compartido porque el dato viaja—. La bandera `primero` existe porque `maximo` arranca en 0 y una entrada de números negativos daría un resultado incorrecto sin ella.

En **Python**, la traducción directa sería `asyncio.Queue` con un productor y un consumidor `async def`, o `queue.Queue` con hilos; en ambos casos el `await queue.get()` es el punto de cesión cooperativa. En **JavaScript**, un `async generator` recorrido con `for await ... of` cumple el mismo papel: el productor cede en cada `yield` y el consumidor en cada iteración. En **Java 21**, los hilos virtuales del Proyecto Loom trajeron por fin corrutinas al lenguaje —un hilo virtual se escribe con la misma API bloqueante de siempre, pero se desmonta del hilo portador al bloquearse—, con `BlockingQueue` como canal. En **C#**, `Channel<T>` de `System.Threading.Channels` es una traducción casi literal de los canales de Go, con soporte de contrapresión incluido. En **Rust**, `std::sync::mpsc` da canales entre hilos y `tokio::sync::mpsc` entre tareas asíncronas; y aquí el sistema de tipos vuelve a hacer su trabajo, porque enviar un valor por un canal es un **movimiento**: el emisor deja de poder usarlo, y el compilador lo garantiza. En **C** no hay nada de esto en el lenguaje: se construye a mano con una cola, un mutex y una variable de condición. En **SQL**, `MAX` delega toda la ejecución —incluido el posible paralelismo— al planificador del motor.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Unidad ligera | Goroutine (Go); `asyncio.Task` (Python); `Promise` sobre el bucle de eventos (JS/TS); hilo virtual desde Java 21; `Task` (C#); `Future` sobre Tokio (Rust); ninguna nativa (C, PHP, SQL). |
| Planificación | Apropiativa desde Go 1.14 (Go); cooperativa, cede solo en `await` (Python, JS, Rust, C#); apropiativa en los puntos de bloqueo (hilos virtuales de Java). |
| Canal | `chan T` con y sin búfer (Go); `asyncio.Queue` / `queue.Queue` (Python); `Channel<T>` (C#); `BlockingQueue` (Java); `mpsc` (Rust); `MessageChannel` entre workers (JS); construido a mano (C). |
| ¿El envío transfiere la propiedad? | Semánticamente sí, por convención (Go, Java, C#, Python); **verificado por el compilador** (Rust); nada que verificar (JS, PHP). |
| Contrapresión | Capacidad del canal (Go, C#, Rust, Java); `maxsize` de la cola (Python); a menudo ausente por descuido en JS con promesas. |
| Color de función | Las corrutinas no «tiñen» el código (Go, hilos virtuales de Java); `async`/`await` sí lo hace: una función async solo se llama desde otra async (Python, JS, Rust, C#). |

## 🧬 El concepto en la familia

El linaje de los canales arranca en el CSP de Hoare y en el operador `|` de Unix, y llega a Go casi sin cambios —no es casualidad: Rob Pike, uno de los diseñadores de Go, venía de Plan 9 y de los lenguajes Newsqueak y Limbo, construidos sobre la misma idea—. Kotlin ofrece la versión más elaborada del modelo con corrutinas estructuradas: cada corrutina pertenece a un ámbito que garantiza que ninguna quede huérfana al fallar el padre, un principio (*structured concurrency*) que Python adoptó en los `TaskGroup` y Java en su API de concurrencia estructurada. La familia de actores —Erlang, Elixir, Akka— usa el mismo paso de mensajes pero sin canal como entidad independiente: cada actor tiene su propio buzón y se le escribe por su identificador, tema de la clase 135. En el mundo asíncrono de un solo hilo, JavaScript popularizó `async`/`await`, que C# había introducido antes y que Python, Rust, Swift y Kotlin adoptaron después; su virtud es escribir código concurrente con forma secuencial, y su defecto conocido es el **color de función**: `async` se propaga hacia arriba por toda la pila de llamadas, algo que las goroutines y los hilos virtuales evitan por completo. Esa tensión —corrutinas transparentes frente a `async` explícito— es hoy una de las divisorias vivas del diseño de lenguajes.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 134
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No cerrar el canal** → causa: el consumidor con `for x := range ch` espera un valor más que nunca llega → solución: el **emisor** cierra cuando termina de producir. Nunca el receptor, y nunca dos veces: cerrar un canal ya cerrado provoca pánico.
- **Enviar a un canal sin búfer sin un receptor listo** → causa: el envío es un encuentro y bloquea indefinidamente; si es el único hilo, el runtime de Go lo detecta y aborta con `all goroutines are asleep - deadlock!` → solución: lanzar el productor en su propia goroutine, o dar capacidad al canal.
- **Compartir estado además de comunicar por el canal** → causa: enviar un puntero o un *slice* por el canal y seguir usándolo desde el emisor → solución: transferir la propiedad de verdad: enviar copias, o dejar de tocar el dato tras enviarlo. En Rust el compilador lo impone; en Go depende de tu disciplina, y `-race` es tu red.
- **Bloquear el bucle de eventos con trabajo de CPU** → causa: en un runtime cooperativo (Python asyncio, JavaScript), un cálculo largo sin `await` congela **todas** las demás tareas → solución: mover el cálculo a un ejecutor de hilos o procesos (`run_in_executor`, `worker_threads`), o insertar puntos de cesión.
- **Mezclar API bloqueante dentro de código asíncrono** → causa: llamar a `requests.get` o a `time.sleep` dentro de una corrutina `async` → solución: usar la variante asíncrona (`aiohttp`, `asyncio.sleep`); una llamada bloqueante secuestra el hilo portador y anula la concurrencia entera.
- **Crear corrutinas sin límite** → causa: lanzar una goroutine por elemento sobre un millón de elementos, sin canal acotado → solución: un grupo fijo de trabajadores consumiendo de un canal con capacidad; ahí está la contrapresión.
- **Olvidar esperar a las tareas lanzadas** → causa: `main` termina y se lleva por delante goroutines a medias, o una tarea de `asyncio` se recolecta sin ejecutarse → solución: `sync.WaitGroup` en Go, `TaskGroup` en Python, concurrencia estructurada en general.

## ❓ Preguntas frecuentes

- **¿Canal o memoria compartida?** Los canales como opción por defecto: hacen explícito quién tiene el dato y eliminan la carrera por construcción. Memoria compartida cuando la copia es cara (una estructura grande de solo lectura) o cuando la operación es un simple incremento, donde un atómico es mucho más eficiente que un mensaje. La regla práctica de Go es «usa canales para transferir propiedad y coordinar; usa un mutex para proteger un dato pequeño y local».
- **¿Una corrutina es un hilo?** No. Un hilo lo planifica el sistema operativo y cuesta megabytes; una corrutina la planifica el runtime del lenguaje y cuesta kilobytes. Muchas corrutinas se multiplexan sobre pocos hilos, y por eso puedes tener cien mil corrutinas y no cien mil hilos. Lo que **sí** son ambas cosas es concurrencia real: dos corrutinas pueden ejecutarse en paralelo en núcleos distintos si el runtime lo permite (Go sí; Python asyncio no).
- **¿Cuánta capacidad doy a un canal?** Sin búfer si quieres máxima sincronía y detectar antes los desajustes de ritmo. Con búfer pequeño (decenas) para absorber ráfagas sin perder contrapresión. Evita búferes enormes: solo esconden el problema y trasladan el desbordamiento a la memoria. Un canal ilimitado no es una optimización, es una fuga esperando su turno.
- **¿Qué es el «color de función» y por qué importa?** En los lenguajes con `async`/`await`, una función asíncrona solo puede llamarse desde otra asíncrona, así que el `async` se propaga hacia arriba y acaba tiñendo toda la base de código; además obliga a duplicar bibliotecas (`requests` frente a `aiohttp`). Las goroutines y los hilos virtuales de Java evitan esto: escribes código bloqueante normal y el runtime se encarga de desmontarlo del hilo cuando se bloquea.
- **¿Qué es la concurrencia estructurada?** El principio de que ninguna tarea sobreviva al ámbito que la creó: si el padre termina o falla, sus hijas se cancelan y se esperan. Elimina las tareas huérfanas y los errores que se pierden en silencio. Kotlin lo introdujo en su diseño de corrutinas, y Python (`asyncio.TaskGroup`) y Java lo han adoptado después; Go, notablemente, no lo tiene de serie —`errgroup` lo aproxima—.

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
