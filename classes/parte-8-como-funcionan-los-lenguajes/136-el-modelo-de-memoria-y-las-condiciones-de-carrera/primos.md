# 🧬 El mismo programa en las familias de lenguajes — Clase 136

> [⬅️ Volver a la clase 136](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —incrementar un contador `n` veces sin perder ni un
incremento— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

El contrato es minúsculo a propósito, porque lo interesante no es el resultado sino la pregunta que
cada lenguaje contesta antes de llegar a él: **¿puede este lenguaje siquiera tener una carrera de
datos?** Algunos no pueden —Lua no tiene hilos preemptivos, R corre en un único hilo, ActionScript
vive en un solo hilo del reproductor— y en ellos `cuenta = cuenta + 1` es seguro sin más. Otros sí
pueden, y entonces lo que importa es qué **garantías** ofrece el modelo de memoria.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** incrementar un contador `n` veces con exclusión, de modo que no se pierda ninguno

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Es la familia donde más se confunde "no he visto la carrera" con "no puede haberla". Aquí conviven
los dos casos, y distinguirlos es todo el ejercicio.

### Ruby

```ruby
n = STDIN.gets.to_i
cuenta = 0
lock = Mutex.new

# En el MRI el GVL impide el paralelismo real de bytecode Ruby, pero NO hace
# atómico el `+=`: el intérprete puede cambiar de hilo entre leer y escribir.
hilos = Array.new(n) { Thread.new { lock.synchronize { cuenta += 1 } } }
hilos.each(&:join)

puts "cuenta=#{cuenta}"
```

### Perl

```perl
use strict;
use warnings;
use threads;
use threads::shared;

# En Perl los hilos NO comparten nada por defecto: cada uno recibe una copia.
# Solo lo marcado `:shared` es memoria común, y por eso puede haber carrera.
chomp(my $n = <STDIN>);
my $cuenta :shared = 0;

my @hilos = map { threads->create(sub { lock($cuenta); $cuenta++; }) } 1 .. $n;
$_->join for @hilos;

print "cuenta=$cuenta\n";
```

### Lua

```lua
-- Lua no tiene hilos preemptivos: una corrutina solo cede el control donde el
-- programador lo pide, así que aquí NO puede existir una carrera de datos.
local n = tonumber(io.read("l"))
local cuenta = 0

local tareas = {}
for _ = 1, n do
  tareas[#tareas + 1] = coroutine.create(function() cuenta = cuenta + 1 end)
end
for _, t in ipairs(tareas) do
  coroutine.resume(t)
end

print(string.format("cuenta=%d", cuenta))
```

### Tcl

```tcl
package require Thread

# Los hilos de Tcl son intérpretes aislados: no comparten variables en absoluto.
# El estado común vive en `tsv`, cuyas operaciones ya son atómicas.
set n [string trim [gets stdin]]
tsv::set contador cuenta 0

set hilos {}
for {set i 0} {$i < $n} {incr i} {
    lappend hilos [thread::create -joinable {
        tsv::incr contador cuenta
        thread::release
    }]
}
foreach h $hilos { thread::join $h }

puts "cuenta=[tsv::get contador cuenta]"
```

### R

```r
# R evalúa en un único hilo y no expone memoria compartida mutable: no hay
# forma de escribir una condición de carrera sobre `cuenta`.
n <- as.integer(readLines("stdin", n = 1))
cuenta <- 0L
for (i in seq_len(n)) cuenta <- cuenta + 1L
cat(sprintf("cuenta=%d\n", cuenta))
```

**Qué reconocer:** tres de los cinco **no pueden** tener una carrera de datos y conviene decirlo sin
rodeos. Lua no la puede tener porque sus corrutinas no se interrumpen: el cambio de contexto ocurre
donde tú escribes `yield`, y entre leer `cuenta` y escribirla no hay ninguno. R no la puede tener
porque no hay un segundo hilo que mire esa memoria. Tcl tampoco, pero por la razón contraria —sí hay
hilos, solo que sin nada compartido, y por eso hace falta `tsv` para tener siquiera un contador
común—. Ruby y Perl sí pueden, y cada uno lo delata a su manera: Ruby porque su GVL protege el
intérprete pero no tu operación de tres pasos, y Perl porque te obliga a declarar `:shared` la
variable, es decir, a **pedir explícitamente** el riesgo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
El bucle de eventos de un solo hilo es lo que hace que la familia web casi nunca vea carreras; el
`SharedArrayBuffer` con `Atomics` es la excepción que confirma la regla.

### Dart

```dart
import 'dart:io';

// Dart no comparte memoria mutable entre isolates: cada uno tiene su propio
// montón. Una carrera de datos sobre `cuenta` es imposible por construcción.
void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var cuenta = 0;
  for (var i = 0; i < n; i++) {
    cuenta++;
  }
  print('cuenta=$cuenta');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en un único hilo del reproductor y no tiene stdin.
// Sin paralelismo de memoria compartida no puede haber condición de carrera.
package {
    public class Contador {
        public static function contar(n:int):String {
            var cuenta:int = 0;
            for (var i:int = 0; i < n; i++) {
                cuenta++;
            }
            return "cuenta=" + cuenta;
        }
    }
}
```

**Qué reconocer:** ninguno de los dos puede tener una carrera de datos, y las razones no son la
misma. ActionScript es sencillamente monohilo: no hay concurrencia que sincronizar. Dart **sí** tiene
paralelismo real —varios isolates corriendo a la vez en varios núcleos— pero prohibió la memoria
compartida mutable, así que el paralelismo existe y la carrera no. Esa distinción es la que hay que
llevarse: "un solo hilo" y "sin memoria compartida" dan el mismo resultado por caminos opuestos, y
solo el segundo escala.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM es la plataforma que popularizó la idea
misma de *modelo de memoria*: desde la **JSR-133** (Java 5), el lenguaje especifica formalmente qué
escrituras de un hilo está obligado a ver otro.

### Kotlin

```kotlin
import java.util.concurrent.atomic.AtomicInteger
import kotlin.concurrent.thread

fun main() {
    val n = readLine()!!.trim().toInt()
    // `AtomicInteger` da atomicidad Y visibilidad; `@Volatile` daría solo la
    // segunda, y `cuenta++` sobre un volátil seguiría perdiendo incrementos.
    val cuenta = AtomicInteger(0)
    val hilos = List(n) { thread { cuenta.incrementAndGet() } }
    hilos.forEach { it.join() }
    println("cuenta=${cuenta.get()}")
}
```

### Scala

```scala
import java.util.concurrent.atomic.AtomicInteger

object Contador extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val cuenta = new AtomicInteger(0)
  val hilos = (1 to n).map(_ => new Thread(() => cuenta.incrementAndGet()))
  hilos.foreach(_.start())
  hilos.foreach(_.join())
  println(s"cuenta=${cuenta.get()}")
}
```

### Groovy

```groovy
import java.util.concurrent.atomic.AtomicInteger

def n = System.in.newReader().readLine().trim() as int
def cuenta = new AtomicInteger(0)
def hilos = (0..<n).collect { Thread.start { cuenta.incrementAndGet() } }
hilos*.join()
println "cuenta=${cuenta.get()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure hace inmutables los valores por defecto: la mutación solo ocurre a
;; través de una referencia (`atom`), y `swap!` es un compare-and-set en bucle.
(def cuenta (atom 0))

(let [n (Long/parseLong (str/trim (read-line)))]
  (->> (repeatedly n #(future (swap! cuenta inc)))
       doall
       (run! deref))
  (println (str "cuenta=" @cuenta)))

(shutdown-agents)
```

**Qué reconocer:** los cuatro comparten el **modelo de memoria de Java desde JSR-133**, que es lo que
da sentido a las garantías que usan. La trampa clásica vive aquí: `volatile` asegura que la escritura
de un hilo se **vea** en otro, pero no hace atómico el `++`, que son tres operaciones —leer, sumar,
escribir— y puede intercalarse. Por eso Kotlin, Scala y Groovy recurren a `AtomicInteger`, que
implementa el incremento con una instrucción de comparación-e-intercambio del procesador. Clojure
cambia el planteamiento entero: como los valores son inmutables, no hay nada que dos hilos puedan
corromper; lo que se coordina es la **identidad**, y `swap!` reintenta hasta que su vista del estado
sigue siendo la vigente.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR tiene su propio modelo de memoria,
emparentado con el de Java y endurecido en .NET Core respecto a la especificación original de ECMA.

### F\#

```fsharp
open System.Threading
open System.Threading.Tasks

// F# empuja a la inmutabilidad: hay que escribir `mutable` a propósito, y para
// tocarlo desde varias tareas hace falta `Interlocked`.
let mutable cuenta = 0

[<EntryPoint>]
let main _ =
    let n = int (stdin.ReadLine().Trim())
    let tareas = [| for _ in 1 .. n -> Task.Run(fun () -> Interlocked.Increment(&cuenta) |> ignore) |]
    Task.WaitAll(tareas)
    printfn "cuenta=%d" cuenta
    0
```

### VB.NET

```vbnet
Imports System.Threading
Imports System.Threading.Tasks

Module Contador
    Private cuenta As Integer = 0

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim tareas(n - 1) As Task
        For i = 0 To n - 1
            ' `SyncLock` daría exclusión mutua; `Interlocked` hace lo mismo sin
            ' bloquear, con una instrucción atómica del procesador.
            tareas(i) = Task.Run(Sub() Interlocked.Increment(cuenta))
        Next
        Task.WaitAll(tareas)
        Console.WriteLine("cuenta=" & cuenta)
    End Sub
End Module
```

**Qué reconocer:** los dos llaman a `Interlocked.Increment`, que es el `AtomicInteger` de la JVM
escrito de otra forma: una sola operación indivisible sobre la posición de memoria, sin candado. El
detalle interesante del CLR es que el `volatile` de .NET tiene semántica de barrera *adquirir/liberar*
—más débil que el `volatile` de Java, que es secuencialmente consistente—, así que traducir código
concurrente entre las dos plataformas token a token es precisamente el error que esta clase quiere
evitar. F# añade su propia pista cultural: para llegar a tener una carrera hay que escribir la
palabra `mutable`, es decir, salir del camino por defecto.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí la carrera de datos no es solo un resultado
incorrecto: es **comportamiento indefinido**, y el compilador tiene permiso para optimizar asumiendo
que no ocurre.

### C++

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    long long n = 0;
    std::cin >> n;

    // Desde C++11 el lenguaje TIENE modelo de memoria: sin `std::atomic` esto
    // sería una carrera de datos, o sea comportamiento indefinido, no "un número raro".
    std::atomic<long long> cuenta{0};

    std::vector<std::thread> hilos;
    hilos.reserve(static_cast<size_t>(n));
    for (long long i = 0; i < n; ++i) {
        hilos.emplace_back([&cuenta] { cuenta.fetch_add(1, std::memory_order_relaxed); });
    }
    for (auto& h : hilos) h.join();

    std::cout << "cuenta=" << cuenta.load() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>
#import <stdatomic.h>

int main(void) {
    @autoreleasepool {
        long long n = 0;
        scanf("%lld", &n);

        // `volatile` de C NO sirve para sincronizar entre hilos: impide que el
        // compilador cachee el valor, pero no ordena ni hace atómica la operación.
        _Atomic long long *cuenta = calloc(1, sizeof(_Atomic long long));

        dispatch_group_t grupo = dispatch_group_create();
        dispatch_queue_t cola = dispatch_get_global_queue(QOS_CLASS_DEFAULT, 0);
        for (long long i = 0; i < n; i++) {
            dispatch_group_async(grupo, cola, ^{ atomic_fetch_add(cuenta, 1); });
        }
        dispatch_group_wait(grupo, DISPATCH_TIME_FOREVER);

        printf("cuenta=%lld\n", atomic_load(cuenta));
        free(cuenta);
    }
    return 0;
}
```

**Qué reconocer:** hasta C++11 y C11 el lenguaje ni siquiera sabía que existían los hilos —la
concurrencia era cosa de la biblioteca, POSIX, y las garantías las ponía el sistema operativo—. Lo
que cambió `std::atomic` no fue dar una suma indivisible, sino **definir el orden**: cada operación
declara su `memory_order` y con eso el compilador y el procesador saben qué reordenaciones les están
prohibidas. Aquí basta `relaxed` porque solo importa que no se pierda ningún incremento, no en qué
orden se vean respecto a otras escrituras. Y la advertencia que más repite esta familia: `volatile`
**no** es una herramienta de concurrencia en C ni en C++; sirve para memoria mapeada a hardware, no
para sincronizar hilos.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go documenta su modelo de
memoria y trae detector de carreras (`go run -race`); Rust va más lejos y hace que el compilador
rechace el programa.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(usize, std.mem.trim(u8, linea, " \t\r"), 10);

    // Zig no impide las carreras en el sistema de tipos: te da `atomic` y la
    // responsabilidad de usarlo. El orden de memoria es explícito en cada llamada.
    var cuenta = std.atomic.Value(i64).init(0);

    const alloc = std.heap.page_allocator;
    const hilos = try alloc.alloc(std.Thread, n);
    defer alloc.free(hilos);

    const Trabajo = struct {
        fn sumar(c: *std.atomic.Value(i64)) void {
            _ = c.fetchAdd(1, .monotonic);
        }
    };
    for (hilos) |*h| h.* = try std.Thread.spawn(.{}, Trabajo.sumar, .{&cuenta});
    for (hilos) |h| h.join();

    try std.io.getStdOut().writer().print("cuenta={d}\n", .{cuenta.load(.monotonic)});
}
```

### Nim

```nim
import std/[strutils, atomics]

# En Nim cada hilo tiene su propio montón salvo lo que se comparta a propósito.
# Las variables globales son la memoria común, y por eso llevan `Atomic`.
var cuenta: Atomic[int]

proc incrementar() {.thread.} =
  discard cuenta.fetchAdd(1)

let n = parseInt(stdin.readLine().strip())
var hilos = newSeq[Thread[void]](n)
for h in hilos.mitems:
  createThread(h, incrementar)
joinThreads(hilos)

echo "cuenta=", cuenta.load()
```

### D

```d
import std.stdio, std.string, std.conv, core.atomic, core.thread;

// En D lo que NO está marcado `shared` es local al hilo (thread-local por
// defecto): el sistema de tipos te obliga a declarar qué es memoria común.
shared long cuenta = 0;

void main() {
    immutable n = readln().strip().to!long;
    auto grupo = new ThreadGroup();
    foreach (i; 0 .. n) {
        grupo.create({ cuenta.atomicOp!"+="(1); });
    }
    grupo.joinAll();
    writefln("cuenta=%d", cuenta.atomicLoad());
}
```

**Qué reconocer:** aquí se ve el abanico completo de "cuánto te ayuda el lenguaje". Zig es el más
crudo: te da atómicos con orden explícito y ninguna comprobación; si compartes memoria mal, compila.
Nim y D mueven la decisión al **sistema de tipos**, con una idea que Rust llevó al extremo: lo normal
es que la memoria sea local al hilo, y compartirla exige escribirlo (`shared` en D, una global en
Nim). Ese es el mismo movimiento que hace `Send`/`Sync` en Rust —convertir un error de ejecución
imposible de reproducir en un error de compilación—, y reconocerlo en un lenguaje nuevo te dice de
inmediato cuánto vas a tener que razonar tú.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL no habla de hilos: habla de
**transacciones** y niveles de aislamiento, que son la versión declarativa del mismo problema.

### Prolog

```prolog
:- initialization(main, main).

% En Prolog una variable se liga una sola vez: no existe la operación
% "leer, sumar, escribir" y por tanto no existe la carrera. El estado es un
% argumento que se acumula llamada a llamada.
contar(0, C, C) :- !.
contar(N, C0, C) :-
    N > 0,
    C1 is C0 + 1,
    N1 is N - 1,
    contar(N1, C1, C).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    contar(N, 0, Cuenta),
    format("cuenta=~d~n", [Cuenta]).
```

### Datalog

```datalog
% Datalog no tiene hilos, ni asignación, ni orden de ejecución observable:
% una condición de carrera es literalmente inexpresable. El contador es el
% tamaño de una relación derivada.
incremento(1).
incremento(2).
incremento(3).

cuenta(C) :- C = count : incremento(_).
```

**Qué reconocer:** los dos ilustran la salida más radical del problema —eliminar el estado mutable— y
por eso ninguno **puede** tener una carrera de datos. En Prolog `C1 is C0 + 1` no reasigna nada:
liga un nombre nuevo, igual que el `swap!` de Clojure produce un valor nuevo en vez de modificar el
viejo. Datalog va aún más lejos y ni siquiera tiene orden de evaluación observable, lo que permite
que un motor evalúe las reglas en paralelo sin que el programador se entere: exactamente la promesa
que hace el planificador de SQL cuando paraleliza una consulta sin pedirte permiso.

---

## Y de vuelta a la clase

Veinte lenguajes y una sola pregunta que los divide en tres grupos: los que **no pueden** tener una
carrera (Lua, R, ActionScript, Dart, Prolog, Datalog), los que **pueden y te avisan** con el sistema
de tipos (Rust, D, Nim, Perl con `:shared`) y los que **pueden y confían en ti** (C, C++, Zig, la
JVM, el CLR). Cuando abras un lenguaje que no conoces, esa clasificación es la primera que conviene
hacer, porque decide cuánto trabajo de razonamiento te queda a ti.

⏮️ [Volver a la clase 136](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
