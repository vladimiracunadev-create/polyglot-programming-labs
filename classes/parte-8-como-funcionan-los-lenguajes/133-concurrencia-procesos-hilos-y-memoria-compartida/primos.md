# 🧬 El mismo programa en las familias de lenguajes — Clase 133

> [⬅️ Volver a la clase 133](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar los elementos de una lista con un acumulador
compartido— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Contar tres números no necesita concurrencia. El ejercicio consiste precisamente en **pedirle a cada
lenguaje que la use**, porque ahí es donde enseña qué unidad de ejecución tiene de verdad: hilos que
comparten memoria, procesos que no comparten nada, o ninguna de las dos.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `cuenta=<número de elementos>`
- **Regla:** un acumulador compartido que se incrementa una vez por elemento

| stdin | esperado |
|---|---|
| `1 2 3` | `cuenta=3` |
| `5` | `cuenta=1` |
| `10 20 30 40` | `cuenta=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tiene hilos reales pero un GIL que impide ejecutar bytecode en paralelo; PHP, en su modelo
clásico, ni siquiera tiene hilos en el proceso web.

### Ruby

```ruby
nums = STDIN.read.split
cuenta = 0
mutex = Mutex.new
hilos = nums.map do
  Thread.new { mutex.synchronize { cuenta += 1 } }
end
hilos.each(&:join)
# Los hilos son del sistema, pero el GVL de CRuby impide que dos corran Ruby a la vez.
puts "cuenta=#{cuenta}"
```

### Perl

```perl
# perlthrtut desaconseja los hilos de Perl: cada `threads->create` CLONA el intérprete
# entero, así que NO hay memoria compartida salvo lo marcado con threads::shared, y el
# coste suele superar la ganancia. La versión secuencial es la idiomática.
my @nums = split ' ', <STDIN>;
my $cuenta = 0;
$cuenta++ for @nums;
printf "cuenta=%d\n", $cuenta;
```

### Lua

```lua
-- Lua no tiene hilos del sistema: solo corrutinas cooperativas dentro de un único
-- estado. No hay paralelismo, y por eso tampoco hace falta ningún cerrojo.
local linea = io.read("l")
local cuenta = 0
local co = coroutine.create(function()
  for _ in linea:gmatch("%S+") do
    cuenta = cuenta + 1
    coroutine.yield()   -- cede el control; nadie corre a la vez que nosotros
  end
end)
while coroutine.resume(co) and coroutine.status(co) ~= "dead" do end
print(string.format("cuenta=%d", cuenta))
```

### Tcl

```tcl
# Los hilos de Tcl (paquete Thread) NO comparten variables: cada uno lleva su propio
# intérprete y se comunican con variables `tsv::` o pasando mensajes.
gets stdin linea
set cuenta 0
foreach _ $linea { incr cuenta }
puts "cuenta=$cuenta"
```

### R

```r
# R es de un solo hilo. El paquete `parallel` reparte el trabajo en PROCESOS
# (mclapply hace fork), así que no hay acumulador compartido: hay que reducir.
v <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]
cuenta <- sum(vapply(v, function(x) 1L, integer(1)))
cat(sprintf("cuenta=%d\n", cuenta))
```

**Qué reconocer:** esta familia es la que menos concurrencia real ofrece, y cada uno falla por un
motivo distinto. Ruby tiene hilos del sistema operativo pero un **GVL** que serializa la ejecución
de código Ruby: sirven para solapar E/S, no para usar varios núcleos —para eso están los `Ractor`
desde 3.0—. Perl los tiene y **su propia documentación los desaconseja**, porque cada hilo copia el
intérprete completo y lo compartido hay que declararlo pieza a pieza con `threads::shared`. Lua es
el caso más limpio: **solo corrutinas**, cooperativas y de un único núcleo, así que el problema de
la memoria compartida ni se plantea. Tcl sí tiene hilos de verdad, pero decidió que **no compartan
nada**: un intérprete por hilo. R directamente sustituye hilos por procesos. Si el acumulador
compartido te parece incómodo aquí, es porque en esta familia lo es.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Un solo hilo con bucle de eventos; el paralelismo llega con `Worker`, que no comparten heap.

### Dart

```dart
import 'dart:io';
import 'dart:isolate';

// Los isolates de Dart NO comparten memoria: cada uno tiene su heap y su recolector.
void contar(List<Object> args) {
  final salida = args[0] as SendPort;
  final nums = (args[1] as List).cast<String>();
  salida.send(nums.length);
}

Future<void> main() async {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final puerto = ReceivePort();
  await Isolate.spawn(contar, [puerto.sendPort, nums]);
  final cuenta = await puerto.first;
  print('cuenta=$cuenta');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene stdin. Su concurrencia son los Worker (Flash Player 11.4+), que tampoco
// comparten memoria: se comunican por MessageChannel, o por un ByteArray marcado como
// shareable, que es la única memoria compartida real de la plataforma.
package {
    public class Contador {
        public static function contar(nums:Array):String {
            var cuenta:int = 0;
            for each (var x:* in nums) {
                cuenta++;
            }
            return "cuenta=" + cuenta;
        }
    }
}
```

**Qué reconocer:** la familia web tomó una decisión de diseño y la sostuvo: **aislamiento por
defecto**. Los `Worker` de JavaScript, los `Isolate` de Dart y los `Worker` de Flash tienen cada uno
su montón, y lo que cruza la frontera se **copia** o se transfiere, no se comparte. Ese es el motivo
de que en esta familia casi nunca veas un mutex: sin memoria compartida no hay condición de carrera
que proteger. La excepción confirma la regla —`SharedArrayBuffer` en JavaScript y el `ByteArray`
`shareable` de AS3 sí comparten bytes, y en cuanto los usas necesitas `Atomics` y vuelves al mundo
de los cerrojos—.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Hilos del sistema operativo, memoria
compartida de verdad y un modelo de memoria especificado.

### Kotlin

```kotlin
import java.util.concurrent.atomic.AtomicInteger
import kotlin.concurrent.thread

fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+"))
    val cuenta = AtomicInteger(0)   // acumulador compartido entre hilos de verdad
    nums.map { thread { cuenta.incrementAndGet() } }.forEach { it.join() }
    println("cuenta=${cuenta.get()}")
}
```

### Scala

```scala
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.Duration

object Contar {
  def main(args: Array[String]): Unit = {
    val nums = scala.io.StdIn.readLine().trim.split("\\s+")
    // Scala prefiere componer Futures a compartir estado mutable: no hay cerrojo.
    val tareas = Future.sequence(nums.toList.map(_ => Future(1)))
    val cuenta = Await.result(tareas, Duration.Inf).sum
    println(s"cuenta=$cuenta")
  }
}
```

### Groovy

```groovy
import java.util.concurrent.atomic.AtomicInteger

def nums = System.in.newReader().readLine().trim().split(/\s+/)
def cuenta = new AtomicInteger(0)
def hilos = nums.collect { Thread.start { cuenta.incrementAndGet() } }
hilos*.join()
println "cuenta=${cuenta.get()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (str/split (str/trim (read-line)) #"\s+")
      cuenta (ref 0)]                     ; referencia coordinada por la STM
  (doall (pmap (fn [_] (dosync (alter cuenta inc))) nums))
  (println (str "cuenta=" @cuenta)))
```

**Qué reconocer:** aquí sí hay hilos del sistema operativo con **un solo montón compartido**, y por
eso reaparece el problema clásico: `cuenta += 1` desde dos hilos pierde incrementos. Kotlin y Groovy
lo resuelven con la herramienta canónica de la JVM, `AtomicInteger`, que es una instrucción atómica
del procesador y no un cerrojo. Scala se desvía: en vez de proteger un estado compartido, **compone
`Future`s** y suma al final, y su ecosistema (Akka, Cats Effect, ZIO) empuja aún más en esa
dirección. Clojure hace la propuesta más radical de las cuatro: su **STM** —memoria transaccional
por software— deja mutar `ref`s solo dentro de `dosync`, y si dos transacciones chocan, una se
**reintenta** sola. Para un contador basta un `atom` con `swap!`, que es la variante sin
coordinación; `ref` se gana el sueldo cuando hay que cambiar **dos** cosas a la vez sin que nadie
vea el estado intermedio. Cuatro lenguajes, un mismo hardware, cuatro filosofías.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Hilos reales, `lock`, `Interlocked` y una
biblioteca de paralelismo de datos encima.

### F\#

```fsharp
open System.Threading

let nums = stdin.ReadLine().Trim().Split(' ')
let cuenta = ref 0   // celda en el montón: todos los hilos ven la misma
nums
|> Array.Parallel.iter (fun _ -> Interlocked.Increment(&cuenta.contents) |> ignore)
printfn "cuenta=%d" cuenta.Value
```

### VB.NET

```vbnet
Imports System
Imports System.Threading
Imports System.Threading.Tasks

Module Contar
    Sub Main()
        Dim sep = New Char() {" "c, ControlChars.Tab, ControlChars.Lf, ControlChars.Cr}
        Dim nums = Console.In.ReadToEnd().Split(sep, StringSplitOptions.RemoveEmptyEntries)
        Dim cuenta As Integer = 0
        ' Interlocked.Increment recibe la variable ByRef: incremento atómico sin cerrojo.
        Parallel.ForEach(nums, Sub(x) Interlocked.Increment(cuenta))
        Console.WriteLine("cuenta=" & cuenta)
    End Sub
End Module
```

**Qué reconocer:** F#, VB.NET y C# comparten el `ThreadPool` del CLR y las mismas primitivas:
`Interlocked` para operaciones atómicas, `Monitor` bajo el `lock` de C# y el `SyncLock` de VB, y la
**Task Parallel Library** por encima, que reparte el trabajo sola en función de los núcleos
disponibles. La sorpresa del código es F#: aunque es funcional, **no puede capturar una variable
`mutable` local en una lambda**, así que hay que usar una celda `ref` —el compilador te obliga a
hacer explícito que el estado vive en el montón y se comparte—. Es una restricción de tipos que
señala exactamente el punto peligroso, y no la tiene ninguno de los otros dos.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). `pthread_create`, `pthread_mutex_lock`: aquí no hay
capas intermedias.

### C++

```cpp
#include <atomic>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

int main() {
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream ss(linea);
    std::vector<std::string> nums;
    for (std::string tok; ss >> tok;) nums.push_back(tok);

    std::atomic<int> cuenta{0};   // memoria compartida de verdad, sin cerrojo
    std::vector<std::thread> hilos;
    for (std::size_t i = 0; i < nums.size(); ++i) {
        hilos.emplace_back([&cuenta] {
            cuenta.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& h : hilos) h.join();

    std::cout << "cuenta=" << cuenta.load() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *nums =
            [[linea stringByTrimmingCharactersInSet:blancos]
             componentsSeparatedByCharactersInSet:blancos];

        __block NSInteger cuenta = 0;   // __block: la variable se comparte con los bloques
        dispatch_queue_t serie = dispatch_queue_create("cuenta", DISPATCH_QUEUE_SERIAL);
        dispatch_apply(nums.count, DISPATCH_APPLY_AUTO, ^(size_t i) {
            dispatch_sync(serie, ^{ cuenta++; });   // la cola serie hace de cerrojo
        });
        printf("cuenta=%ld\n", (long)cuenta);
    }
    return 0;
}
```

**Qué reconocer:** los dos comparten memoria sin ninguna red de seguridad —nada impide escribir
`cuenta++` sin protección y obtener un resultado distinto en cada ejecución—, pero el vocabulario ya
no es el de C. C++11 trajo `std::thread`, `std::mutex` y, sobre todo, un **modelo de memoria** con
órdenes explícitos: ese `memory_order_relaxed` dice "solo me importa que el incremento sea atómico,
no en qué orden lo vean los demás", y es más barato que el `seq_cst` por defecto. Objective-C
cambia de nivel: en vez de hilos, **colas** de Grand Central Dispatch, y el cerrojo se sustituye por
una **cola serie** —solo una tarea a la vez, luego no hay carrera—. Es la misma idea que un mutex,
expresada como estructura de datos en vez de como candado.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go da goroutines
baratas; Rust da hilos del sistema y un compilador que rechaza las carreras.

### Zig

```zig
const std = @import("std");

fn incrementar(cuenta: *std.atomic.Value(u32)) void {
    _ = cuenta.fetchAdd(1, .monotonic);
}

pub fn main() !void {
    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, linea, " \r\t"), " \t");

    var cuenta = std.atomic.Value(u32).init(0);
    var hilos: [64]std.Thread = undefined;
    var n: usize = 0;
    while (it.next()) |_| : (n += 1) {
        hilos[n] = try std.Thread.spawn(.{}, incrementar, .{&cuenta});
    }
    for (hilos[0..n]) |h| h.join();

    try std.io.getStdOut().writer().print("cuenta={d}\n", .{cuenta.load(.monotonic)});
}
```

### Nim

```nim
import std/[strutils, atomics]

var cuenta: Atomic[int]   # las globales de Nim SÍ se comparten entre hilos

proc incrementar() {.thread.} =
  cuenta.atomicInc(1)

let nums = stdin.readLine().strip().splitWhitespace()
var hilos = newSeq[Thread[void]](nums.len)
for i in 0 ..< nums.len:
  createThread(hilos[i], incrementar)
joinThreads(hilos)
echo "cuenta=", cuenta.load()
```

### D

```d
import std.stdio, std.string, std.array;
import std.concurrency, core.atomic;
import core.thread : thread_joinAll;

// En D las variables de módulo son THREAD-LOCAL por defecto: para compartirlas de
// verdad hay que escribir `shared`, y entonces el compilador exige acceso atómico.
shared int cuenta = 0;

void incrementar() {
    atomicOp!"+="(cuenta, 1);
}

void main() {
    auto nums = readln().strip().split();
    foreach (_; nums)
        spawn(&incrementar);
    thread_joinAll();
    writefln("cuenta=%d", atomicLoad(cuenta));
}
```

**Qué reconocer:** los tres tienen hilos del sistema y memoria compartida, y los tres intentan que
el **compilador** te obligue a decirlo. Zig lo hace con tipos: `std.atomic.Value(u32)` no se lee ni
se escribe sin indicar un orden de memoria, así que el punto de sincronización es imposible de
pasar por alto. Nim añade una vuelta interesante: con ARC/ORC cada hilo tiene su propio montón, y
mover datos entre hilos exige `Isolated[T]` para garantizar que nadie más conserva una referencia
—el mismo razonamiento que `Send` en Rust—. D es el más singular de todo el documento: **las
variables globales son thread-local por defecto**, al revés que en C, Go o Java. Compartir es la
excepción, se escribe `shared`, y a partir de ahí el compilador rechaza cualquier lectura o
escritura que no sea atómica. Es la idea de Rust —hacer del compartir algo explícito y verificado—
llegando desde otro punto de partida.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El motor decide solo si paraleliza; el
programador describe el resultado.

### Prolog

```prolog
:- initialization(main, main).

% SWI-Prolog sí tiene hilos nativos (thread_create/3), pero NO comparten variables
% lógicas: cada hilo tiene sus propias pilas y se comunican con message_queue_create/3.
main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Nums),
    length(Nums, Cuenta),
    format("cuenta=~d~n", [Cuenta]).
```

### Datalog

```datalog
% Datalog no tiene hilos ni estado mutable. Paradójicamente por eso los motores
% (Soufflé, por ejemplo) sí paralelizan la evaluación solos: no hay nada que compartir.
elemento(1).
elemento(2).
elemento(3).

cuenta(N) :- N = count : { elemento(_) }.
```

**Qué reconocer:** aquí el acumulador compartido **desaparece del código**, y no por pobreza sino
por diseño. Prolog tiene hilos de verdad, pero decidió lo mismo que Tcl y que Erlang: **nada
compartido**, comunicación por colas de mensajes, así que un contador global no es expresable sin
salir del modelo. Datalog llega al extremo opuesto y por el mismo camino: como sus reglas son
monótonas y sin efectos, evaluar dos reglas a la vez **no puede** dar un resultado distinto que
evaluarlas en serie, y por eso motores como Soufflé reparten el trabajo entre núcleos sin que el
programador escriba una palabra sobre concurrencia. Es exactamente lo que hace el planificador de
SQL, y la lección de la familia: si no hay estado mutable compartido, la concurrencia deja de ser un
problema del programador.

---

## Y de vuelta a la clase

Veinte lenguajes y tres modelos de fondo: **hilos que comparten un montón** —JVM, CLR, C++,
Objective-C, Zig, Nim, D con `shared`—, **unidades aisladas que se pasan mensajes** —Dart, Tcl,
Prolog, los Worker de la web, R con procesos— y **ninguna concurrencia real**, como Lua con sus
corrutinas o Perl con sus hilos desaconsejados. Ante un lenguaje nuevo, la primera pregunta útil no
es cómo lanzar un hilo: es si dos de ellos pueden ver la misma variable.

⏮️ [Volver a la clase 133](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
