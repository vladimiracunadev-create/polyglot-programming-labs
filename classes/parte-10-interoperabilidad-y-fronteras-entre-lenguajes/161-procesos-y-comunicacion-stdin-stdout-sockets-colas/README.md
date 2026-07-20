# Clase 161 — Procesos y comunicación: stdin/stdout, sockets, colas

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ya sabemos serializar (159) y acordar un contrato (160). Falta el canal: por dónde salen esos bytes de un proceso y entran en otro. Y aquí aparece la distinción que más determina la arquitectura de un sistema políglota: comunicarse **de forma síncrona** —te llamo y espero tu respuesta— o **de forma asíncrona** —dejo el mensaje y sigo con lo mío—. No es un detalle de implementación: cambia quién falla cuando algo se rompe, quién absorbe los picos de carga y qué garantías de orden y entrega puedes prometer.

Kleppmann organiza el capítulo 4 de *Designing Data-Intensive Applications* justo por ahí: los datos fluyen entre procesos por bases de datos, por servicios (llamada síncrona) o por **mensajes asíncronos**. El objetivo de esta clase es entender los tres canales concretos que implementan ese flujo —tubería, socket y cola—, qué garantiza y qué no garantiza cada uno, y por qué una cola no es "un socket más lento" sino una decisión de diseño que desacopla al productor del consumidor en el tiempo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Recibir** y procesar datos que llegan por una cola.
2. **Explicar** los mecanismos de comunicación entre procesos y sus garantías.
3. **Reconocer** stdin/stdout como la tubería universal entre lenguajes.
4. **Distinguir** comunicación síncrona de asíncrona y sus consecuencias ante fallos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tubería (pipe) | stdout de uno a stdin de otro |
| 2 | Cola/socket | Comunicación asíncrona o en red |
| 3 | Productor/consumidor | Uno envía, otro recibe |

## 📖 Definiciones y características

La **comunicación entre procesos** (IPC) es el conjunto de mecanismos que permiten que dos programas con espacios de memoria separados intercambien datos. Que la memoria esté separada es el punto entero: sin punteros compartidos, todo lo que cruza son **bytes en un flujo**, y por eso el IPC es la frontera políglota por excelencia — el sistema operativo no sabe ni le importa en qué lenguaje está escrito cada extremo.

Una **tubería** (*pipe*) conecta el `stdout` de un proceso con el `stdin` de otro. Es un búfer en el núcleo, de tamaño limitado (típicamente 64 KB en Linux), con dos propiedades que se aprovechan sin pensar en ellas. La primera es el **contrapresión** (*backpressure*): si el búfer se llena porque el consumidor va lento, la escritura del productor se bloquea. Nadie se queda sin memoria; el rápido simplemente espera al lento. La segunda es el **EOF**: cuando el productor cierra su extremo, el consumidor recibe fin de fichero y sabe que no hay más datos. Sin ese cierre, el consumidor espera para siempre. Kernighan y Pike construyen todo *The Unix Programming Environment* sobre esta idea: programas pequeños que leen texto y escriben texto, componibles porque comparten un solo formato de frontera.

Un **socket** generaliza la tubería a través de la red. TCP añade lo que la red no da: entrega ordenada, sin duplicados y con reintentos. Pero no elimina el problema fundamental —añade uno nuevo, el **fallo parcial**—. En una tubería local, si el otro proceso muere lo sabes de inmediato. En un socket TCP, un extremo que deja de responder es indistinguible de uno que va lento, y solo un *timeout* que tú eliges rompe el empate. Tanenbaum lo llama la diferencia esencial entre lo local y lo distribuido: en la red, "no ha respondido todavía" y "no responderá nunca" son el mismo estado observable. Además, TCP es un flujo de bytes sin fronteras de mensaje: si envías dos mensajes seguidos, pueden llegar pegados o partidos. Hay que enmarcarlos —con longitud al principio o con un delimitador— y olvidarlo es de los errores más frecuentes al programar sockets a mano.

Una **cola** (*message queue*) añade una pieza intermedia que persiste los mensajes: RabbitMQ, Kafka, SQS, Redis Streams. El cambio no es de velocidad sino de **acoplamiento temporal**. Con una llamada síncrona, si el receptor está caído tu operación falla; con una cola, el mensaje espera y el receptor lo procesa cuando vuelve. Eso permite absorber picos (el productor encola a mil por segundo aunque el consumidor procese cien), escalar añadiendo consumidores y aislar fallos. A cambio se pagan tres cosas: el propio *broker* es un sistema que hay que operar; la entrega suele ser **al menos una vez**, así que un mensaje puede llegar duplicado y el consumidor debe ser idempotente; y el **orden** solo se garantiza dentro de una partición o cola, nunca globalmente cuando hay varios consumidores en paralelo.

- **Comunicación entre procesos (IPC)** — mecanismos para que procesos con memoria separada intercambien datos. Clave: solo cruzan bytes, nunca punteros.
- **Tubería** — conecta la salida de un proceso con la entrada de otro. Clave: contrapresión automática y EOF como señal de fin.
- **Cola** — búfer persistente que desacopla productor y consumidor. Clave: tolera que el receptor esté caído, a cambio de duplicados y orden solo parcial.

## 🧩 Situación

En Unix, `productor | consumidor` conecta dos programas por una tubería, y ninguno sabe en qué lenguaje está escrito el otro. Este curso usa exactamente ese mecanismo: el verificador ejecuta las diez implementaciones, les escribe los casos por `stdin` y compara lo que sale por `stdout`. Es lo que permite que Python, Rust y SQL se comparen con la misma vara sin puentes ni FFI. Aquí el escenario es un consumidor que recibe una tanda de mensajes de una cola y los agrega: llegan en orden, se suman uno a uno, y el total se emite cuando la entrada se cierra — el fin de la cola es el EOF.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (mensajes en la cola)
- **Salida** (stdout): `recibido=<suma de los mensajes>`
- **Regla:** sumar los mensajes recibidos en orden

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `recibido=6` |
| `5` | `recibido=5` |
| `10 20 30 40` | `recibido=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA CADA mensaje de la cola: acumular ; ESCRIBIR suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
recibido = 0
for m in nums:  # consumidor de la cola
    recibido += m
print(f"recibido={recibido}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let recibido = 0;
for (const m of nums) recibido += m;
console.log(`recibido=${recibido}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let recibido = 0;
for (const m of nums) recibido += m;
console.log(`recibido=${recibido}`);
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
        long recibido = 0;
        for (String s : p) recibido += Integer.parseInt(s);
        System.out.println("recibido=" + recibido);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

long recibido = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"recibido={recibido}");
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
	recibido := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		recibido += n
	}
	fmt.Printf("recibido=%d\n", recibido)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let recibido: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("recibido={recibido}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long recibido = 0, m;
    while (scanf("%ld", &m) == 1) recibido += m;
    printf("recibido=%ld\n", recibido);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL agrega los mensajes con SUM.
WITH cola(x) AS (VALUES (1), (2), (3))
SELECT printf('recibido=%d', sum(x)) AS resultado FROM cola;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "recibido=" . array_sum($nums) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `1 2 3` debe producir `recibido=6`. El consumidor lee los mensajes que le llegan por el canal, los acumula en orden y emite el total. Fíjate en que la salida solo puede escribirse **cuando la entrada termina**: hasta que no llega EOF, el consumidor no sabe si viene otro mensaje. Ese es el ritmo real de un consumidor de cola.

En **Python**, `sys.stdin.read()` es la decisión clave: lee hasta EOF, es decir, se bloquea hasta que el productor cierra su extremo. Solo entonces `.split()` trocea y el bucle acumula. Si el productor abriera la tubería y no la cerrara, este programa esperaría indefinidamente — el fallo más común al encadenar procesos a mano.

En **C**, `while (scanf("%ld", &m) == 1) recibido += m;` expresa el mecanismo en su forma más desnuda: se consume mientras haya un dato válido, y el bucle termina cuando `scanf` devuelve algo distinto de 1 (EOF o basura). El acumulador es `long`, no `int`, porque una cola larga desborda un entero de 32 bits sin avisar. Esa elección de anchura es la misma que en la clase 156 sobre FFI: en la frontera, el tipo importa.

En **Go**, `bufio.NewReader(os.Stdin)` envuelve la entrada en un búfer antes de leer, y no es un adorno. Leer del sistema operativo byte a byte implica una llamada al núcleo por byte; el búfer las agrupa. Es la misma lógica que hace que un consumidor real de Kafka pida lotes de mensajes en vez de uno a uno: **cruzar una frontera cuesta, así que se cruza pocas veces con mucha carga**.

En **SQL**, `SUM(x)` sobre una tabla de valores hace la agregación de golpe, sin bucle ni concepto de proceso. Es la vista declarativa del mismo problema, y no es casual: los sistemas de streaming modernos (Kafka Streams, Flink SQL, ksqlDB) permiten justamente escribir el consumidor como una consulta SQL sobre un flujo infinito, con ventanas temporales en lugar de tablas finitas.

## 🔬 Comparación

| Lenguaje | Canales de IPC idiomáticos |
|---|---|
| Python | `sys.stdin`/`stdout`, `subprocess`, `socket`, `multiprocessing.Queue`; `pika` (RabbitMQ), `confluent-kafka`. |
| JavaScript | Streams de Node (`process.stdin`), `child_process`, `net` para sockets, `worker_threads` con paso de mensajes. |
| TypeScript | Igual que JS, con los tipos de `@types/node` describiendo el contenido del canal. |
| Java | `java.io` y NIO (`SocketChannel`, `Selector`); `BlockingQueue` en proceso; clientes JMS y Kafka. |
| C# | `Stream` y `Pipe` (`System.IO.Pipelines`), `Channel<T>` para productor/consumidor en proceso. |
| Go | `os.Stdin`, `net.Conn`, `os/exec`; y los **canales** del lenguaje, que llevan la idea de cola al propio modelo de concurrencia. |
| Rust | `std::io` y `std::net`; `std::sync::mpsc` para colas entre hilos; `tokio` para E/S asíncrona. |
| C | La capa base: `pipe()`, `fork()`, `dup2()`, `socket()`, `read()`/`write()`. Todo lo demás la envuelve. |
| SQL | No hace IPC: el cliente le habla por un socket con el protocolo del motor; `LISTEN`/`NOTIFY` en PostgreSQL es la excepción. |
| PHP | `STDIN`/`STDOUT`, `proc_open`, extensión `sockets`; colas vía Redis o RabbitMQ en el framework. |

La diferencia sintáctica es notable, pero la que decide arquitecturas es semántica: **si el canal bloquea o no, y qué garantiza**. Un `read()` bloqueante convierte al consumidor en rehén del productor; un canal asíncrono le permite atender otras cosas mientras espera. Go lleva esto al extremo interesante: sus canales (`chan`) son colas dentro del proceso con la misma semántica de contrapresión que una tubería del núcleo, lo que hace que pasar de comunicación intra-proceso a inter-proceso sea un cambio de canal y no de estructura del programa. C, en el otro extremo, expone las primitivas crudas: `pipe()` y `read()` son literalmente lo que las bibliotecas de todos los demás lenguajes acaban llamando. Y en todos los casos aparece el mismo problema que Kleppmann subraya: como la entrega puede reintentarse, **el consumidor debe tolerar mensajes repetidos**; sumar dos veces el mismo mensaje da un total mal, y ninguna cola te protege de eso — solo tu diseño idempotente.

## 🧬 El concepto en la familia

La escala del canal cambia, el patrón productor/consumidor no. Dentro de un proceso son los canales de Go, los `Channel<T>` de C#, `mpsc` de Rust o las `BlockingQueue` de Java. Entre procesos de una máquina, tuberías y sockets Unix. Entre máquinas, TCP y HTTP. Y entre servicios que no quieren esperarse, los *brokers*: **RabbitMQ** (colas con enrutamiento, el mensaje se borra al consumirse), **Kafka** (un registro particionado y persistente donde cada consumidor lleva su propia posición y puede releer el histórico) y las variantes gestionadas en la nube. La diferencia entre RabbitMQ y Kafka no es de rendimiento sino de modelo —cola frente a *log*—, y es la distinción que Kleppmann considera central para decidir cómo fluyen los datos en un sistema. Por debajo de todo sigue habiendo lo mismo: bytes que salen de un proceso y entran en otro, sin importar el lenguaje de ninguno de los dos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 161
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden global con varios productores o consumidores** → causa: el orden solo se garantiza dentro de una cola o partición, no entre ellas → solución: particionar por clave (todos los eventos de un pedido a la misma partición) o incluir un número de secuencia y ordenar al consumir.
- **No cerrar la tubería** → causa: el consumidor espera EOF que nunca llega y el sistema se queda colgado sin error → solución: cerrar el descriptor al terminar de enviar, y poner *timeout* en toda lectura bloqueante.
- **Tratar los mensajes como si llegaran exactamente una vez** → causa: casi todo *broker* entrega *al menos una vez*, y un reintento duplica el mensaje → solución: hacer idempotente el consumidor con un identificador de mensaje deduplicado.
- **Olvidar enmarcar los mensajes en un socket TCP** → causa: TCP es un flujo de bytes sin fronteras; dos mensajes llegan pegados o partidos → solución: prefijar la longitud o usar un delimitador, y leer hasta completar el marco.
- **Escribir sin leer y llenar el búfer** → causa: un proceso escribe en la tubería mientras el otro no consume; la escritura se bloquea y ambos se quedan esperando → solución: consumir siempre lo que se produce, o usar E/S asíncrona en ambos extremos.
- **Confundir cola con "socket lento"** → causa: se despliega un *broker* creyendo que solo añade latencia → solución: entender que aporta desacoplamiento temporal y persistencia, y que a cambio es un sistema más que hay que operar y vigilar.

## ❓ Preguntas frecuentes

- **¿Tubería o socket?** Tubería cuando los procesos comparten máquina y ciclo de vida: es más rápida y el fin se detecta solo. Socket cuando cruzan máquinas, o cuando el ciclo de vida es independiente y hace falta reconectar.
- **¿Por qué stdin/stdout?** Porque es la tubería universal: todo lenguaje la implementa igual y el sistema operativo la provee. Por eso el verificador del curso compara diez lenguajes sin escribir un solo puente específico.
- **¿Cuándo pasar de llamada síncrona a cola?** Cuando el emisor no necesita la respuesta para continuar, cuando la carga llega en picos, o cuando quieres que un fallo del receptor no tumbe al emisor. Si el usuario espera el resultado en pantalla, síncrono suele ser lo correcto.
- **¿La cola garantiza que no se pierda nada?** Solo si está configurada para persistir y replicar, y si el consumidor confirma (*ack*) después de procesar, no antes. Confirmar al recibir y fallar luego pierde el mensaje silenciosamente.
- **¿Qué pasa si el consumidor va más lento que el productor?** La cola crece. Es su virtud a corto plazo y su peligro a largo: hay que vigilar el retraso acumulado (*lag*) y escalar consumidores o descartar con una política explícita antes de agotar el almacenamiento.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: flujo de datos por mensajes; cap. 11: colas frente a *logs* particionados.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Comunicación síncrona frente a asíncrona y sus efectos sobre el acoplamiento.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 4: comunicación orientada a flujo y a mensajes; fallo parcial y *timeouts*.

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

> [⏮️ Clase 160](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/160-contratos-de-api-rest-grpc-y-esquemas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 162 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/162-webassembly-como-objetivo-comun/README.md)
