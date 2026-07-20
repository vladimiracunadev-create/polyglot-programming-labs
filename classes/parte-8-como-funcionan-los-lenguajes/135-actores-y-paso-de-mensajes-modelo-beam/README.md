# Clase 135 — Actores y paso de mensajes (modelo BEAM)

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Las dos clases anteriores fueron reduciendo lo que se comparte: primero candados sobre memoria común, luego canales que transfieren el dato. El modelo de actores da el paso final y elimina la memoria compartida **por completo**. Un actor es una unidad concurrente con estado privado que solo se comunica enviando mensajes; nadie puede leer ni escribir su estado desde fuera. La consecuencia es fuerte: la carrera de datos deja de existir, no porque el programador tenga cuidado ni porque el compilador vigile, sino porque no hay nada que compartir. Esta clase construye un acumulador que recibe un mensaje por número, y usa como referencia la implementación más madura del modelo: la máquina virtual **BEAM** de Erlang y Elixir. El *porqué* de estudiarla, aunque no programes en Erlang, es que BEAM resuelve un problema que los demás modelos ni siquiera se plantean —qué pasa cuando **una parte del sistema falla**— y que su respuesta, «deja que muera y reinícialo desde un estado bueno conocido», ha reaparecido en Kubernetes, en los microservicios y en la ingeniería de fiabilidad moderna. Los actores no son solo un modelo de concurrencia: son un modelo de tolerancia a fallos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Enunciar las tres cosas que un actor puede hacer al recibir un mensaje, según la formulación de Hewitt.
2. Explicar por qué el aislamiento total elimina la carrera de datos y qué se paga a cambio.
3. Describir qué es un proceso BEAM: su heap privado, su buzón, su GC individual y su coste real.
4. Explicar la filosofía *let it crash* y cómo los supervisores la convierten en fiabilidad.
5. Distinguir el modelo de actores del de canales (CSP) y saber cuándo se prefiere cada uno.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Actor: estado privado | Sin acceso externo no hay carrera posible |
| 2 | Buzón y `receive` | La cola de mensajes serializa el acceso al estado por construcción |
| 3 | Procesos BEAM | Cientos de miles de actores con GC y planificación propios |
| 4 | *Let it crash* y supervisores | El fallo aislado como estrategia de diseño, no como accidente |
| 5 | Actores frente a canales | Buzón nombrado por destinatario frente a conducto anónimo |

## 📖 Definiciones y características

El modelo de actores lo formuló Carl Hewitt en 1973, y su definición es sorprendentemente breve. Un **actor** es una entidad que, al recibir un mensaje, puede hacer exactamente tres cosas: enviar un número finito de mensajes a otros actores, crear un número finito de actores nuevos, y designar el comportamiento con el que tratará el **siguiente** mensaje. Nada más. En particular, no puede leer el estado de otro actor ni pedirle que lo modifique: solo puede pedírselo por mensaje y esperar, si acaso, una respuesta. El estado del actor es privado de forma absoluta.

De ahí sale la propiedad que hace valioso el modelo. Cada actor procesa **un mensaje a la vez**, de manera secuencial, tomándolos de su **buzón** (*mailbox*), una cola donde se acumulan en orden de llegada. Dentro del actor no hay concurrencia: su código es secuencial, su estado solo lo toca él, y por tanto no necesita candados ni atómicos ni razonamiento sobre entrelazados. La concurrencia vive **entre** actores, no dentro de ninguno. El sistema entero se vuelve concurrente sin que ninguna pieza individual tenga que serlo.

Un **proceso BEAM** es la encarnación práctica de esa idea, y sus números explican por qué Erlang tuvo éxito donde otras implementaciones de actores fracasaron. No es un proceso del sistema operativo ni un hilo: es una estructura del runtime que arranca ocupando unos cientos de bytes, de modo que un sistema con **cientos de miles o millones** de procesos vivos es rutina en BEAM. Cada proceso tiene su **propio heap** —los mensajes se **copian** al enviarse, con la excepción de los binarios grandes que se comparten por referencia y conteo— y, crucialmente, **su propio recolector de basura**. Ese detalle es una de las decisiones de diseño más elegantes del modelo: recolectar la memoria de un proceso no detiene a los demás, así que BEAM no tiene pausas globales de GC. Un sistema con un millón de procesos hace un millón de recolecciones diminutas e independientes en lugar de una gigante y bloqueante.

El planificador de BEAM es **apropiativo y justo**: asigna a cada proceso un presupuesto de *reducciones* (aproximadamente, operaciones ejecutadas) y lo desaloja al agotarlo. La consecuencia práctica es que un proceso que entra en un bucle infinito no puede monopolizar el sistema —a diferencia de lo que ocurre en un runtime cooperativo como asyncio o el bucle de eventos de JavaScript—. BEAM ejecuta un planificador por núcleo, con robo de trabajo entre ellos, de modo que el paralelismo real es automático.

La última pieza es la que hace del modelo algo más que concurrencia: la **tolerancia a fallos**. Como los procesos están aislados, uno puede morir sin corromper a nadie, y su muerte es un evento observable: otro proceso enlazado (`link`) o monitor (`monitor`) recibe la notificación. Sobre esa base se construyen los **supervisores**, procesos cuya única función es vigilar hijos y reiniciarlos según una estrategia declarada. De ahí la filosofía **let it crash**: en lugar de llenar el código de manejo defensivo para estados imprevistos, se deja que el proceso falle rápido y se reinicie desde un estado inicial correcto. Es un cambio de mentalidad importante —no se intenta que nada falle, se asume que fallará y se diseña la recuperación—, y es la razón por la que se citan disponibilidades de nueve nueves en centrales telefónicas construidas con Erlang.

## 🧩 Situación

Un servidor de chat mantiene cien mil conexiones simultáneas. Con hilos y memoria compartida, harían falta cien mil hilos —imposible— o un pool de hilos con una estructura compartida de sesiones protegida por candados que se convierten en el cuello de botella y en la fuente de todos los bugs. Con actores, cada conexión **es** un proceso: tiene su estado, su buzón, y si uno de ellos falla por un mensaje malformado, muere solo, su supervisor lo reinicia, y las otras 99.999 conexiones ni se enteran. No hay ni un candado en el sistema. Ese perfil —muchísimas entidades independientes, con estado, que deben aislar fallos— es exactamente donde el modelo de actores gana. Un actor acumulador que suma cada número recibido es su versión mínima: estado propio, un mensaje cada vez, ninguna sincronización.

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
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

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

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m) { this.total += m; } };
const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m: number) { this.total += m; } };
const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

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

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

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

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

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

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

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

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL agrega sin actores; SUM sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('total=%d', sum(x)) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

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

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Ninguno de los diez lenguajes del núcleo tiene actores nativos, así que las implementaciones **modelan la forma** del actor con lo que cada uno ofrece. Leerlas comparándolas con lo que haría BEAM es el ejercicio.

En **Go** está la aproximación más fiel, y merece la pena mirarla con detalle. `buzon := make(chan int, 64)` es literalmente un buzón con capacidad para 64 mensajes pendientes. La goroutine lanzada con `go func()` es el actor: su `total` es una variable **local a la clausura**, invisible desde fuera —estado privado real, no por convención—, y el bucle `for m := range buzon` es el `receive`: consume mensajes de uno en uno, secuencialmente, así que `total += int64(m)` no necesita candado alguno. El `main` es el emisor: manda cada número al buzón y luego `close(buzon)` señala el fin. El segundo canal, `done`, implementa el patrón petición-respuesta: el actor publica su resultado final y `<-done` lo espera. Fíjate en la diferencia con BEAM: aquí el buzón está **acotado a 64**, así que un emisor demasiado rápido se bloquea —contrapresión—, mientras que los buzones de BEAM son ilimitados y un actor lento acaba consumiendo memoria hasta tumbar el nodo. Ambas decisiones tienen defensores.

En **Python**, **Java**, **C#**, **Rust**, **JavaScript**, **TypeScript** y **PHP**, el actor se reduce a un objeto con estado encapsulado (`Acumulador`) y un método `recibir`. Es la forma correcta del modelo —estado privado, una única puerta de entrada— pero **sin la parte concurrente**: al llamar a `recibir` directamente, el emisor ejecuta el código del actor en su propio hilo. Si dos hilos llamaran a `actor.recibir(m)` a la vez, la carrera reaparecería intacta. Lo que falta es exactamente lo que aporta el modelo: la cola que serializa. La versión real añadiría un buzón (`queue.Queue`, `BlockingQueue`, `Channel<T>`, `mpsc`) y un hilo o tarea propietaria que lo consuma. En **Rust**, además, la firma `fn recibir(&mut self, ...)` deja constancia en el sistema de tipos de que mutar el actor exige acceso exclusivo, que es la misma garantía que el buzón proporciona en BEAM, por otra vía.

En **C**, la acumulación en una variable local es la reducción secuencial pura: sin objeto, sin buzón, sin actor. Y en **SQL**, `SUM` expresa el resultado sin ninguna noción de proceso. Este contraste es útil: cuando el problema es una agregación pura sobre datos que ya tienes, todo el aparato concurrente es innecesario. Los actores pagan por lo que dan —copias de mensajes, latencia de buzón—, y solo compensan cuando hay estado vivo, muchas entidades independientes y necesidad de aislar fallos.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Unidad concurrente | Proceso BEAM con heap propio (Erlang/Elixir, referencia); goroutine + canal (Go); objeto con cola y tarea (Java, C#, Python, Rust); ninguna nativa (C, SQL, PHP). |
| Estado del actor | Privado por construcción (Go, por la clausura; Erlang, por el runtime); privado por convención de encapsulamiento (Java, C#, PHP, Python); exclusivo por tipos (`&mut self` en Rust). |
| Buzón | Canal con búfer, acotado (Go, C# `Channel<T>`, Rust `mpsc`); `BlockingQueue` (Java); `queue.Queue` / `asyncio.Queue` (Python); ilimitado (BEAM). |
| Semántica del envío | Copia del valor y aislamiento total (BEAM); copia del entero pero potencialmente puntero compartido si el mensaje fuera un puntero (Go, Java, C#); **movimiento verificado** (Rust). |
| Recolección de basura | Por proceso, sin pausa global (BEAM); global y compartida por todos (JVM, .NET, Go, Python). |
| Aislamiento de fallos | Un proceso muere sin afectar a nadie y un supervisor lo reinicia (BEAM); una excepción no capturada en un hilo puede dejar el estado compartido a medias (todos los demás). |

## 🧬 El concepto en la familia

Erlang es el referente y no por casualidad: se diseñó en Ericsson en los años 80 para centralitas telefónicas, donde la disponibilidad continua no era un objetivo comercial sino un requisito, y el modelo de actores con supervisión resultó ser la forma de conseguirla. Elixir revitalizó el ecosistema en los 2010 aportando una sintaxis moderna y macros sobre la misma BEAM, con OTP —el conjunto de comportamientos `GenServer`, `Supervisor`, `Application`— como la biblioteca que codifica décadas de práctica en fiabilidad. En la JVM, Akka trasladó el modelo a Scala y Java, con la diferencia crucial de que los actores de Akka comparten el heap de la JVM: los mensajes no se copian y, por tanto, el aislamiento depende de que se envíen mensajes inmutables —una convención que la máquina no impone—; además, un fallo de memoria afecta a toda la JVM. Microsoft construyó Orleans sobre el mismo modelo con *virtual actors*, que se activan y desactivan bajo demanda, para sistemas distribuidos a gran escala. Pony lleva la idea al extremo combinando actores con un sistema de tipos de capacidades que garantiza, en compilación, la ausencia de carreras sin copiar los mensajes. Y conviene distinguir bien el modelo del de la clase anterior: en el modelo de actores el destinatario tiene nombre y su buzón le pertenece; en CSP el canal es una entidad anónima e independiente por la que dos partes cualesquiera se encuentran. Actores para entidades con identidad y estado vivo; canales para tuberías y flujos de datos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 135
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Enviar una referencia mutable como mensaje** → causa: en runtimes que comparten heap (Akka, Go, Java), mandar un objeto mutable y seguir usándolo desde el emisor reintroduce exactamente la carrera que el modelo pretendía eliminar → solución: mensajes inmutables o copiados. BEAM lo impone copiando; en la JVM y en Go es disciplina tuya.
- **Buzón que crece sin control** → causa: el productor va más rápido que el actor durante suficiente tiempo; en BEAM los buzones son ilimitados y el nodo acaba muriendo por falta de memoria → solución: acotar la cola para introducir contrapresión, descartar mensajes con política explícita, o vigilar la longitud del buzón como métrica de salud del sistema. Es el modo de fallo característico de los sistemas de actores.
- **Actores que se piden respuesta mutuamente** → causa: A hace una llamada síncrona a B mientras B hace una llamada síncrona a A; ambos esperan en su `receive` y ninguno procesa → solución: interbloqueo clásico del modelo; romperlo con mensajes asíncronos, con tiempos de espera obligatorios, o rediseñando la dependencia.
- **Poner demasiado estado en un solo actor** → causa: un actor «registro global» al que todos escriben se convierte en el cuello de botella, porque procesa **un** mensaje a la vez → solución: repartir el estado entre muchos actores (uno por entidad, no uno por tipo de entidad). El paralelismo del modelo viene de tener muchos actores, no de que cada uno sea rápido.
- **Programar defensivamente contra todo error** → causa: llenar el actor de `try/catch` para estados imprevistos, contradiciendo el modelo → solución: capturar solo los errores esperados del dominio y dejar que los inesperados maten al proceso; el supervisor lo reinicia desde un estado correcto. Un `catch` que oculta un error deja el actor vivo pero con estado inconsistente, que es peor.
- **Suponer que los mensajes llegan en cualquier orden** o, al revés, **que llegan en orden global** → causa: BEAM garantiza el orden **entre dos procesos dados**, pero no un orden global entre tres o más → solución: no asumir causalidad entre mensajes de emisores distintos; si el orden importa, hacerlo explícito con números de secuencia.

## ❓ Preguntas frecuentes

- **¿Actor o hilo?** Un hilo comparte memoria con sus hermanos y necesita candados; un actor no comparte nada y no los necesita. La contrapartida es el coste de copiar mensajes y la latencia del buzón: para una operación que en memoria compartida sería un incremento atómico, el actor es órdenes de magnitud más caro. Elige actores cuando el sistema tenga muchas entidades con estado propio y necesites aislar fallos; elige memoria compartida para trabajo numérico intensivo sobre datos comunes.
- **¿Qué es exactamente *let it crash*?** No es «ignora los errores», sino separar el código de la lógica del código de la recuperación. El actor solo maneja el caso feliz y los errores esperados del dominio; cualquier otra cosa lo mata, y un supervisor —cuya única responsabilidad es esa— decide si reiniciarlo, reiniciar a sus hermanos o escalar el fallo hacia arriba. La apuesta de fondo es que la mayoría de los errores en producción son transitorios (una condición rara, un dato corrupto puntual) y que reiniciar desde un estado limpio los resuelve mejor que intentar reparar un estado que ya no se entiende.
- **¿Los actores sirven en sistemas distribuidos?** Es su punto fuerte: como la comunicación ya es por mensajes asíncronos y no hay memoria compartida, mover un actor a otra máquina no cambia el modelo de programación. En Erlang, enviar a un proceso local o a uno de otro nodo se escribe igual. Ojo con la falacia clásica de tratar la red como si fuera fiable: la latencia y las particiones siguen existiendo, y el envío deja de ser garantizado.
- **¿Por qué BEAM no tiene pausas de GC perceptibles?** Porque cada proceso tiene su propio heap y su propio recolector. Recolectar un proceso de unos kilobytes es instantáneo y no detiene a nadie más; no existe la «recolección completa del heap» que en la JVM puede llegar a cientos de milisegundos. Ese diseño es la razón de que BEAM sea la plataforma de referencia para sistemas de latencia predecible con muchísimas conexiones.
- **¿Puedo hacer actores en un lenguaje que no los tiene?** Sí, y es un patrón muy útil: un objeto con estado privado, una cola de entrada y un único hilo o tarea que la consume. Eso te da la propiedad esencial —serialización del acceso al estado sin candados—. Lo que no obtendrás sin un runtime como BEAM es lo barato de los procesos, el aislamiento de memoria real y la supervisión integrada.

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
