# Clase 133 — Concurrencia: procesos, hilos y memoria compartida

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

`cuenta += 1` parece la operación más inocua del curso. No lo es: es una operación de **tres pasos** —leer el valor de memoria a un registro, sumarle uno, escribirlo de vuelta— y en cuanto dos hilos la ejecutan sobre la misma variable sin coordinarse, el resultado deja de ser predecible. Esta clase construye el modelo mental que explica por qué. Empieza por la unidad de aislamiento —el **proceso**, con su espacio de direcciones propio— y desciende hasta la unidad de ejecución que rompe ese aislamiento por dentro —el **hilo**, que comparte todo el heap con sus hermanos—. El *porqué* es que la concurrencia con memoria compartida es el modelo por defecto de la mayoría de los lenguajes del núcleo y, al mismo tiempo, la fuente de los bugs más caros que existen: no deterministas, dependientes de la carga, imposibles de reproducir en el portátil del desarrollador y perfectamente capaces de sobrevivir años en producción. Bryant & O'Hallaron dedican los capítulos finales de *CS:APP* a este terreno precisamente porque exige entender qué hay debajo: registros, cachés y un planificador que puede interrumpirte entre dos instrucciones cualesquiera.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir proceso de hilo en términos de espacio de direcciones, coste de creación y coste de cambio de contexto.
2. Explicar por qué `cuenta += 1` no es atómica y descomponerla en las operaciones máquina que la forman.
3. Definir sección crítica, exclusión mutua e invariante, y razonar sobre qué protege un mutex.
4. Diferenciar concurrencia de paralelismo, y explicar qué cambia el GIL de CPython en esa distinción.
5. Contrastar el modelo de memoria compartida con el de paso de mensajes y justificar cuándo conviene cada uno.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Proceso: aislamiento por hardware | La MMU garantiza que un fallo no contamine a los vecinos |
| 2 | Hilo: concurrencia dentro del proceso | Barato de crear y comunicar, sin ninguna barrera entre ellos |
| 3 | Atomicidad y sección crítica | Por qué una sola línea de código puede corromper el estado |
| 4 | Exclusión mutua | Qué garantiza un mutex y qué cuesta |
| 5 | Concurrencia frente a paralelismo | Estructurar tareas independientes no es ejecutarlas a la vez |

## 📖 Definiciones y características

Un **proceso** es un programa en ejecución con su propio espacio de direcciones virtual. El aislamiento no es una convención: lo impone el hardware. La unidad de gestión de memoria (MMU) traduce las direcciones virtuales de cada proceso a marcos físicos distintos mediante su tabla de páginas, de modo que la dirección `0x1000` de un proceso y la de otro son memoria físicamente distinta. Un puntero desbocado en un proceso no puede tocar a otro: provoca un fallo de segmentación y muere solo. Ese aislamiento se paga en dos monedas: crear un proceso es caro (hay que construir tablas de páginas, aunque `fork` lo mitigue con copia-al-escribir) y comunicar entre procesos exige un mecanismo explícito del sistema operativo —tuberías, sockets, memoria compartida mapeada—, con copias y llamadas al núcleo de por medio.

Un **hilo** es una línea de ejecución dentro de un proceso. Tiene lo mínimo imprescindible propio —su pila, su contador de programa, sus registros— y **comparte todo lo demás** con los hilos hermanos: el código, las variables globales y, sobre todo, el heap entero. Comunicar entre hilos es tan barato como escribir en una variable, porque literalmente es escribir en una variable. Esa es su virtud y su condena: no hay ninguna barrera que impida que dos hilos toquen el mismo dato al mismo tiempo, y nada en el código fuente lo señala.

Aquí aparece la **atomicidad**. `cuenta += 1` se compila típicamente a tres instrucciones: cargar de memoria, incrementar en registro, almacenar. El planificador del sistema operativo puede interrumpir un hilo entre cualesquiera dos de ellas. Si dos hilos leen `cuenta = 41` antes de que ninguno haya escrito, ambos calculan `42` y ambos lo escriben: dos incrementos, un solo resultado. La pérdida es real y silenciosa. Y el problema es peor de lo que sugiere ese ejemplo, porque además de la interrupción está el hardware: cada núcleo tiene su propia caché, las escrituras no se propagan instantáneamente al resto, y tanto el compilador como la CPU **reordenan** instrucciones cuando eso no cambia el resultado observable *en un solo hilo*. Un hilo puede ver las escrituras de otro en un orden distinto al del código fuente. Ese es el tema de la clase 136.

La **sección crítica** es el fragmento de código que accede a estado compartido y durante el cual una **invariante** del programa está temporalmente rota. La **exclusión mutua** —un mutex, un `lock`, un `synchronized`— garantiza que a lo sumo un hilo la ejecute a la vez, de modo que nadie observe el estado intermedio. Lo que hay que retener es qué protege realmente un mutex: no protege *datos*, protege *invariantes*. Es una convención entre las partes del programa que acuerdan tomar el mismo candado antes de tocar los mismos datos; nada en el lenguaje —salvo en Rust, donde el dato vive *dentro* del `Mutex`— obliga a respetarla.

Conviene, por último, separar dos ideas que se confunden constantemente. La **concurrencia** es una propiedad de la estructura del programa: hay varias tareas cuyo progreso se intercala y cuyo orden relativo no está fijado. El **paralelismo** es una propiedad de la ejecución: varias cosas ocurren físicamente a la vez, en núcleos distintos. Un programa concurrente en una máquina de un solo núcleo no es paralelo, y sin embargo tiene todos los problemas de carrera. CPython es el ejemplo canónico: su GIL (*Global Interpreter Lock*) permite que solo un hilo ejecute bytecode a la vez, así que los hilos de Python dan concurrencia pero no paralelismo de CPU —siguen siendo útiles para E/S, donde el hilo bloqueado suelta el GIL— y por eso el paralelismo real en Python pasa históricamente por procesos (`multiprocessing`).

## 🧩 Situación

Un contador de peticiones en un servidor multihilo reporta 998.734 tras exactamente un millón de peticiones. Nadie perdió peticiones: se perdieron *incrementos*, unos pocos miles de veces en que dos hilos leyeron el mismo valor antes de escribir. El bug no aparece con dos hilos y poca carga, ni en el entorno de pruebas, ni al añadir un `print` para depurar —porque el `print` cambia el ritmo y hace la colisión improbable—. Solo aparece en producción, bajo carga, y de forma irreproducible. Ese es el perfil exacto de una condición de carrera, y la razón de que este modelo haya que entenderlo *antes* de escribir el primer hilo. Contar elementos con un acumulador es esa misma operación en su forma más simple, aquí de un solo hilo y por tanto correcta.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<número de elementos>`
- **Regla:** acumulador compartido que cuenta los elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `cuenta=3` |
| `5` | `cuenta=1` |
| `10 20 30 40` | `cuenta=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; PARA CADA elemento: cuenta <- cuenta + 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = sys.stdin.read().split()
cuenta = 0
for _ in nums:
    cuenta += 1  # acumulador compartido
print(f"cuenta={cuenta}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        int cuenta = 0;
        for (String s : nums) cuenta += 1;
        System.out.println("cuenta=" + cuenta);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int cuenta = 0;
foreach (var s in nums) cuenta += 1;
Console.WriteLine($"cuenta={cuenta}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	cuenta := 0
	for range strings.Fields(line) {
		cuenta++
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut cuenta = 0;
    for _ in s.split_whitespace() {
        cuenta += 1;
    }
    println!("cuenta={cuenta}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int cuenta = 0;
    while (scanf("%ld", &x) == 1) cuenta++;
    printf("cuenta=%d\n", cuenta);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COUNT sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$cuenta = 0;
foreach ($nums as $_) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Las diez implementaciones son secuenciales a propósito: un solo hilo toca el acumulador, así que el resultado es determinista. Lo interesante es imaginar cada una con dos hilos y ver qué haría falta.

En **Python**, `cuenta += 1` se compila a un `LOAD_FAST`, un `BINARY_OP` y un `STORE_FAST`. El GIL garantiza que solo un hilo ejecuta bytecode a la vez, pero **no** que estas tres instrucciones se ejecuten juntas: el intérprete puede ceder el GIL entre ellas. Es un malentendido muy extendido creer que el GIL hace seguros los contadores; no lo hace, y por eso existen `threading.Lock` y, para este caso concreto, `itertools.count` o los tipos atómicos. La versión correcta con hilos usaría un `Lock` o, mejor aún, delegaría el conteo a una `queue.Queue`.

En **Java** y **C#**, `cuenta += 1` sobre un campo compartido tiene el mismo problema, agravado por el modelo de memoria: sin `synchronized`, `volatile` o `lock`, un hilo puede no ver nunca las escrituras de otro, porque el JIT tiene permiso para mantener el valor en un registro indefinidamente. Las bibliotecas ofrecen la solución directa: `AtomicLong.incrementAndGet()` en Java, `Interlocked.Increment` en C#, ambos apoyados en una instrucción de comparación-e-intercambio del procesador que hace el ciclo leer-modificar-escribir indivisible en hardware, sin candado.

En **Go**, la variante concurrente sería el idioma más característico del lenguaje: en lugar de proteger `cuenta` con un `sync.Mutex`, se lanzarían goroutines que envían por un canal y una sola goroutine acumularía. Donovan y Kernighan insisten en *The Go Programming Language* en esta preferencia, resumida en el lema del lenguaje: no comuniques compartiendo memoria, comparte comunicando. Es el tema de la clase 134. Go, además, trae un detector de carreras integrado (`go run -race`), una herramienta que conviene conocer antes que cualquier teoría.

En **Rust**, el compilador simplemente **no deja** escribir la versión rota. Mover `cuenta` a dos hilos exigiría dos préstamos mutables simultáneos, que el *borrow checker* rechaza; la versión que compila es `Arc<Mutex<i64>>` o `AtomicI64`, y en el primer caso el dato vive *dentro* del mutex, de forma que acceder sin tomar el candado es sintácticamente imposible. Los rasgos `Send` y `Sync` codifican en el sistema de tipos qué se puede mover entre hilos y qué se puede compartir. Es el corolario de la clase 132.

En **C**, no hay red de seguridad de ninguna clase: con `pthreads`, `cuenta++` desde dos hilos es comportamiento indefinido, y la solución es `pthread_mutex_t` o los atómicos de C11 (`_Atomic int`). En **JavaScript** el problema desaparece por diseño: el modelo es de un solo hilo con bucle de eventos, y los *workers* no comparten memoria salvo que se use explícitamente un `SharedArrayBuffer`. **PHP**, en su modelo clásico por petición, tampoco lo plantea. Y **SQL** resuelve el asunto en otra capa entera: `COUNT(*)` se ejecuta bajo el control de transacciones y aislamiento del motor, que puede paralelizar internamente garantizándote una vista consistente.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Unidad de concurrencia | Hilos del SO (Java, C#, C, Rust); goroutines multiplexadas sobre hilos (Go); hilos con GIL (Python); bucle de eventos de un solo hilo (JS); proceso por petición (PHP). |
| ¿Paralelismo real de CPU? | Sí (Java, C#, Go, Rust, C); no con hilos, sí con procesos (Python por el GIL); no en el hilo principal (JS). |
| Protección del estado compartido | `synchronized` / `AtomicLong` (Java); `lock` / `Interlocked` (C#); `sync.Mutex` o canales (Go); `Mutex<T>` verificado por tipos (Rust); `pthread_mutex` / `_Atomic` (C); `threading.Lock` (Python). |
| ¿El compilador detecta la carrera? | Solo Rust, en compilación. Go la detecta en ejecución con `-race`. El resto, nunca. |
| Estilo preferido por la comunidad | Memoria compartida con candados (Java, C#, C); paso de mensajes (Go); asíncrono de un hilo (JS); procesos (Python, PHP). |
| Coste de crear la unidad | Hilo del SO: ~1 MB de pila y una llamada al núcleo. Goroutine: ~2 KB de pila que crece bajo demanda, gestionada en espacio de usuario. |

## 🧬 El concepto en la familia

La familia C —C, C++ y por herencia Java y C#— adoptó la memoria compartida con candados como modelo central, con `pthreads` y luego `std::thread` y `java.util.concurrent`. Es el modelo más eficiente y el más propenso a error: interbloqueos, carreras, inversión de prioridades. La familia concurrente/actor —Erlang, Elixir y en buena medida Akka en la JVM— tomó el camino opuesto: **nada** se comparte, todo se comunica por mensajes copiados entre procesos ligeros y aislados, con lo que la carrera de datos deja de existir por construcción (clase 135). Go se sitúa en medio: ofrece memoria compartida y candados, pero su cultura y sus primitivas empujan hacia los canales, herederos directos del CSP de Hoare (clase 134). La familia funcional —Haskell, Clojure— ataca el problema desde la inmutabilidad: si los datos no cambian, compartirlos es trivialmente seguro, y la mutación se canaliza por construcciones controladas como la memoria transaccional o los *atoms*. Rust hace algo distinto de todos: conserva la memoria compartida y los candados, pero mueve su corrección al sistema de tipos. Y JavaScript escapa por la tangente eliminando los hilos del modelo del programador. Cinco respuestas a la misma pregunta, y ninguna gratuita.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 133
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Suponer que una sola línea es atómica** → causa: `cuenta += 1`, `lista.append(x)` o `if (mapa.get(k) == null) mapa.put(k, v)` parecen indivisibles y no lo son → solución: usar tipos atómicos (`AtomicLong`, `Interlocked`, `_Atomic`) o proteger la secuencia entera con un candado; para el caso del mapa, `computeIfAbsent` o `putIfAbsent`.
- **Proteger la lectura pero no la escritura (o al revés)** → causa: creer que leer es inofensivo → solución: si un hilo escribe, *todos* los que acceden deben sincronizar. Sin sincronización, un lector puede ver un valor a medio escribir o no ver nunca la actualización, porque el compilador tiene permiso para cachearla en un registro.
- **Tomar candados en orden distinto en rutas distintas** → causa: un hilo toma A y luego B, otro toma B y luego A: interbloqueo clásico → solución: definir y documentar un orden global de adquisición de candados, o usar un único candado de grano más grueso.
- **Sobre-sincronizar** → causa: envolver funciones enteras en `synchronized` «por si acaso» → solución: la sección crítica debe ser lo más corta posible y no contener E/S ni llamadas a código ajeno; un candado retenido durante una llamada de red serializa todo el sistema.
- **Depurar una carrera añadiendo trazas** → causa: el `print` introduce E/S y sincronización, cambia el ritmo y hace desaparecer el síntoma → solución: usar herramientas diseñadas para esto: `go run -race`, ThreadSanitizer (`-fsanitize=thread`), o el detector de Java Flight Recorder.
- **Confiar en `sleep` para coordinar** → causa: «espero 100 ms y para entonces el otro hilo habrá terminado» → solución: sincronización explícita —`join`, condición, canal, barrera—. Un `sleep` no es una garantía, es una apuesta que se pierde bajo carga.

## ❓ Preguntas frecuentes

- **¿Compartir memoria o comunicar?** El lema de Go —«no comuniques compartiendo memoria; comparte comunicando»— resume una preferencia por defecto sensata: el paso de mensajes hace explícita la transferencia de datos y elimina categorías enteras de error. Pero no es dogma: para estructuras de datos grandes y de solo lectura, o para un contador de alta frecuencia, la memoria compartida con un atómico es órdenes de magnitud más eficiente que copiar mensajes.
- **¿Proceso o hilo?** Hilo cuando necesitas compartir estado y crear muchas unidades baratas. Proceso cuando necesitas **aislamiento de fallos**: si un hilo corrompe el heap, se lleva por delante todo el proceso; si un proceso lo hace, muere solo y el supervisor lo reinicia. Esa es la razón de que Chrome separe pestañas en procesos y de que muchos servidores usen un modelo multiproceso pese al coste.
- **¿El GIL de Python hace mis hilos seguros?** No. Garantiza que solo un hilo ejecuta bytecode a la vez, pero cede el control entre instrucciones, y una operación de alto nivel casi nunca es una sola instrucción. Lo que el GIL sí garantiza es que las estructuras internas del intérprete no se corrompan; tus invariantes son cosa tuya.
- **¿Cuántos hilos conviene crear?** Para trabajo de CPU, del orden del número de núcleos: más hilos solo añaden cambios de contexto. Para trabajo de E/S, muchos más, porque pasan la mayor parte del tiempo bloqueados; ese desajuste es precisamente lo que motivó las corrutinas y las goroutines de la clase siguiente, que permiten decenas de miles de tareas concurrentes sobre unos pocos hilos del sistema.
- **¿Un mutex protege un dato?** Protege una *invariante*, y solo si todo el código que la puede romper acuerda tomar el mismo candado. Es una convención, no una garantía del lenguaje —salvo en Rust, donde el dato vive dentro del `Mutex` y no hay forma de alcanzarlo sin bloquear—.

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

> [⏮️ Clase 132](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 134 ⏭️](../../parte-8-como-funcionan-los-lenguajes/134-tareas-corrutinas-y-canales/README.md)
