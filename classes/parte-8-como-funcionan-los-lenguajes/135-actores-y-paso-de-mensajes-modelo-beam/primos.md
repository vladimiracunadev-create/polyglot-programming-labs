# 🧬 El mismo programa en las familias de lenguajes — Clase 135

> [⬅️ Volver a la clase 135](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar una lista enviando cada número como mensaje a
un actor acumulador— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí hay una honestidad que conviene decir antes de empezar: los lenguajes que **definieron** el
modelo de actores —Erlang y Elixir— viven en la familia *concurrente / actor* del Atlas y **no están
en el núcleo** de este curso. El núcleo se acerca por dos lados: Go con canales (CSP) y Java o C#
con hilos y colas. Entre los primos, en cambio, sí aparecen los tres parecidos más honestos al BEAM:
el `MailboxProcessor` de F#, los actores de Akka en Scala y el `agent` de Clojure. Léelos con eso en
mente.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `total=<suma de todos>`
- **Regla:** cada número es un mensaje enviado al actor; el actor acumula en su estado privado

| stdin | esperado |
|---|---|
| `1 2 3` | `total=6` |
| `5` | `total=5` |
| `10 20` | `total=30` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los dos nació concurrente: Python tiene el GIL y PHP el modelo de petición aislada. La
familia entera resuelve el problema con lo que tenga a mano —una cola, un proceso hijo, una
corrutina— y por eso es el mejor sitio para ver qué **no** es un actor.

### Ruby

```ruby
buzon = Thread::Queue.new

actor = Thread.new do        # el actor solo toca su propio `total`
  total = 0
  while (m = buzon.pop) != :fin
    total += m
  end
  total
end

STDIN.read.split.each { |s| buzon << s.to_i }
buzon << :fin
puts "total=#{actor.value}"
```

### Perl

```perl
use strict;
use warnings;

# Perl no tiene actores: el primo más cercano es un proceso hijo con dos tuberías,
# que sí garantiza aislamiento total de memoria.
my @nums = split ' ', do { local $/; <STDIN> };

pipe(my $buzon_r, my $buzon_w) or die $!;
pipe(my $resp_r,  my $resp_w)  or die $!;

if (fork()) {                       # emisor: cada número, un mensaje
    close $buzon_r; close $resp_w;
    print $buzon_w "$_\n" for @nums;
    close $buzon_w;
    chomp(my $total = <$resp_r>);
    wait;
    print "total=$total\n";
} else {                            # actor: acumula lo que le llega por su buzón
    close $buzon_w; close $resp_r;
    my $total = 0;
    while (my $m = <$buzon_r>) { $total += $m }
    print $resp_w "$total\n";
    exit 0;
}
```

### Lua

```lua
-- Lua no tiene hilos preemptivos: el actor más cercano es una corrutina, que
-- tiene estado privado pero cede el control de forma explícita, no concurrente.
local actor = coroutine.wrap(function(m)
  local total = 0
  while m do
    total = total + m
    m = coroutine.yield(total)
  end
end)

local total = 0
for s in io.read("a"):gmatch("%S+") do
  total = actor(tonumber(s))
end
print(string.format("total=%d", total))
```

### Tcl

```tcl
package require Thread

# Cada hilo de Tcl es un intérprete aislado: no comparten variables, solo mensajes.
set actor [thread::create {
    set total 0
    proc recibir {m} { global total; incr total $m }
    thread::wait
}]

foreach m [read stdin] {
    thread::send -async $actor [list recibir $m]
}
thread::send $actor {set total} total
puts "total=$total"
```

### R

```r
# R ejecuta en un solo hilo y no tiene buzones: el "buzón" es un vector y el
# "actor", un pliegue que lleva el estado de mensaje en mensaje.
buzon <- scan("stdin", what = integer(), quiet = TRUE)
total <- Reduce(function(estado, mensaje) estado + mensaje, buzon, 0L)
cat(sprintf("total=%d\n", total))
```

**Qué reconocer:** los cinco tienen que **fabricar** el buzón, porque ninguno lo trae en el lenguaje.
Ruby usa `Thread::Queue`, pero su intérprete de referencia tiene GVL: hay concurrencia, no
paralelismo. Perl paga procesos enteros a cambio del aislamiento real que un actor exige. Lua es el
caso más instructivo del contraste: la corrutina **sí** tiene el estado privado del actor, pero le
falta lo otro —ejecución independiente— y por eso el `resume` es una llamada, no un envío. Tcl es la
sorpresa: sus hilos son intérpretes separados sin memoria común, que es exactamente la premisa del
BEAM. R admite abiertamente que aquí no compite.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia web ya usa paso de mensajes a diario sin llamarlo así: `postMessage` entre el hilo
principal y un *worker* es un envío asíncrono a un contexto que no comparte memoria.

### Dart

```dart
import 'dart:io';
import 'dart:isolate';

void actor(SendPort respuesta) {
  final buzon = ReceivePort();
  respuesta.send(buzon.sendPort);
  var total = 0;                       // estado privado del isolate
  buzon.listen((mensaje) {
    if (mensaje is int) {
      total += mensaje;
    } else {
      respuesta.send(total);
      buzon.close();
    }
  });
}

Future<void> main() async {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final mias = ReceivePort();
  await Isolate.spawn(actor, mias.sendPort);
  await for (final evento in mias) {
    if (evento is SendPort) {
      for (final m in nums) {
        evento.send(m);                // cada número, un mensaje
      }
      evento.send('fin');
    } else {
      print('total=$evento');
      mias.close();
    }
  }
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin. Sus Worker (Flash Player 11.4+) sí pasan mensajes
// por MessageChannel, pero aquí se ilustra solo el estado privado del actor.
package {
    public class Acumulador {
        private var total:int = 0;

        public function recibir(mensaje:int):void {
            total += mensaje;
        }

        public function resultado():String {
            return "total=" + total;
        }
    }
}
```

**Qué reconocer:** el `Isolate` de Dart es, de todos los primos de esta página, el más cercano al
proceso del BEAM: memoria separada, buzón propio (`ReceivePort`) y envío asíncrono por `SendPort`. La
consecuencia se ve en el código: no hay ninguna variable compartida que proteger, y por eso tampoco
hay candados. ActionScript enseña el otro extremo de la familia: un solo hilo de reproductor, donde
"actor" se queda en lo que un objeto con estado privado puede ofrecer.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM no tiene actores en el lenguaje, pero es
la plataforma donde más se han construido encima: Akka nació aquí precisamente imitando a Erlang.

### Kotlin

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.channels.Channel

fun main() = runBlocking {
    val buzon = Channel<Int>(Channel.UNLIMITED)
    val actor = async {                  // el actor solo toca su propio `total`
        var total = 0L
        for (m in buzon) total += m
        total
    }
    readLine()!!.trim().split(Regex("\\s+")).forEach { buzon.send(it.toInt()) }
    buzon.close()
    println("total=${actor.await()}")
}
```

### Scala

```scala
import akka.actor.typed.ActorSystem
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

object Acumulador {
  sealed trait Mensaje
  final case class Numero(n: Long) extends Mensaje
  case object Fin extends Mensaje

  def apply(total: Long = 0L): Behavior[Mensaje] = Behaviors.receiveMessage {
    case Numero(n) => apply(total + n)     // el estado viaja en el comportamiento
    case Fin       => println(s"total=$total"); Behaviors.stopped
  }
}

object Main extends App {
  val sistema = ActorSystem(Acumulador(), "suma")
  scala.io.StdIn.readLine().trim.split("\\s+").foreach(s => sistema ! Acumulador.Numero(s.toLong))
  sistema ! Acumulador.Fin
}
```

### Groovy

```groovy
import groovyx.gpars.actor.DefaultActor

class Acumulador extends DefaultActor {
    long total = 0

    void act() {
        loop {
            react { mensaje ->
                if (mensaje == 'fin') {
                    println "total=$total"
                    terminate()
                } else {
                    total += mensaje
                }
            }
        }
    }
}

def actor = new Acumulador().start()
System.in.newReader().readLine().trim().split(/\s+/).each { actor << (it as long) }
actor << 'fin'
actor.join()
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Un `agent` es el primo directo del proceso del BEAM: su estado solo cambia
;; enviándole funciones, y esos envíos se serializan uno detrás de otro.
(def acumulador (agent 0))

(doseq [s (str/split (str/trim (read-line)) #"\s+")]
  (send acumulador + (Long/parseLong s)))

(await acumulador)
(println (str "total=" @acumulador))
(shutdown-agents)
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina virtual y cuatro grados distintos de
cercanía al modelo. Kotlin ofrece un canal, que es CSP como Go: el buzón existe pero no pertenece a
nadie. Akka en Scala es la imitación deliberada de Erlang —`!` para enviar, un `Behavior` que
**devuelve el siguiente comportamiento** en vez de mutar un campo, y un sistema de supervisión que
aquí ni se ve—. Groovy con GPars trae `react`/`loop`, el mismo gesto de "espera un mensaje y
reacciona". Clojure es el más limpio conceptualmente: el `agent` garantiza que las actualizaciones no
se pisan sin que aparezca un solo candado en el código, porque el envío, y no el candado, es el
mecanismo de exclusión.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
type Mensaje =
    | Numero of int64
    | Total of AsyncReplyChannel<int64>

// MailboxProcessor es literalmente un buzón con un bucle asíncrono detrás:
// el equivalente idiomático más cercano a un proceso de Erlang en .NET.
let actor =
    MailboxProcessor.Start(fun buzon ->
        let rec bucle total =
            async {
                let! m = buzon.Receive()
                match m with
                | Numero n -> return! bucle (total + n)
                | Total canal -> canal.Reply total
            }
        bucle 0L)

stdin.ReadLine().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
|> Array.iter (fun s -> actor.Post(Numero(int64 s)))

printfn "total=%d" (actor.PostAndReply Total)
```

### VB.NET

```vbnet
Imports System.Collections.Concurrent
Imports System.Threading.Tasks

Module Suma
    Sub Main()
        ' VB.NET no trae actores: el buzón más cercano es una BlockingCollection
        ' consumida por una única tarea.
        Dim buzon As New BlockingCollection(Of Long)()
        Dim actor = Task.Run(Function()
                                 Dim total As Long = 0
                                 For Each m In buzon.GetConsumingEnumerable()
                                     total += m
                                 Next
                                 Return total
                             End Function)

        For Each s In Console.ReadLine().Trim().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
            buzon.Add(Long.Parse(s))
        Next
        buzon.CompleteAdding()
        Console.WriteLine("total=" & actor.Result)
    End Sub
End Module
```

**Qué reconocer:** el `MailboxProcessor` de F# se lee casi como Erlang traducido: el estado no es un
campo mutable sino el **argumento de la función recursiva** `bucle`, y cada mensaje procesado produce
la siguiente vuelta con el estado nuevo. `PostAndReply` añade la otra mitad del modelo, la pregunta
con respuesta, que en el BEAM se escribe como un envío que incluye el remitente. VB.NET muestra lo
que queda cuando el lenguaje no ayuda: la cola concurrente sigue siendo memoria compartida y hay que
recordar cerrar la entrada (`CompleteAdding`) o el consumidor no termina nunca.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). No hay buzón, ni hilo, ni actor: hay memoria y hay
que construirlo todo, incluida la sincronización.

### C++

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <optional>
#include <queue>
#include <sstream>
#include <string>
#include <thread>

int main() {
    std::string linea;
    std::getline(std::cin, linea);

    std::queue<std::optional<long long>> buzon;   // el buzón es memoria compartida
    std::mutex m;
    std::condition_variable cv;
    long long total = 0;

    std::thread actor([&] {
        for (;;) {
            std::unique_lock<std::mutex> lk(m);
            cv.wait(lk, [&] { return !buzon.empty(); });
            auto mensaje = buzon.front();
            buzon.pop();
            lk.unlock();
            if (!mensaje) break;                  // nullopt = mensaje de cierre
            total += *mensaje;
        }
    });

    std::istringstream in(linea);
    long long n;
    while (in >> n) {
        {
            std::lock_guard<std::mutex> lk(m);
            buzon.push(n);
        }
        cv.notify_one();
    }
    {
        std::lock_guard<std::mutex> lk(m);
        buzon.push(std::nullopt);
    }
    cv.notify_one();

    actor.join();
    std::cout << "total=" << total << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *linea = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] availableData]
                encoding:NSUTF8StringEncoding];

        long long *total = calloc(1, sizeof(long long));
        // Una cola serie de GCD es el buzón: los bloques se atienden de uno en uno,
        // así que el estado queda protegido sin ningún candado explícito.
        dispatch_queue_t buzon = dispatch_queue_create("actor.acumulador", DISPATCH_QUEUE_SERIAL);

        NSCharacterSet *sep = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        for (NSString *s in [linea componentsSeparatedByCharactersInSet:sep]) {
            if (s.length == 0) continue;
            long long n = s.longLongValue;
            dispatch_async(buzon, ^{ *total += n; });
        }
        dispatch_sync(buzon, ^{});     // barrera: espera a vaciar el buzón

        printf("total=%lld\n", *total);
        free(total);
    }
    return 0;
}
```

**Qué reconocer:** C++ deja a la vista todo lo que un actor de verdad te ahorra —cola, mutex,
variable de condición y un mensaje centinela para decir "no envío más"—, y además obliga a razonar
sobre el *happens-before*: `total` se escribe en un hilo y se lee en otro, y lo único que hace esa
lectura legal es el `join()`. Objective-C sube un peldaño con GCD: una cola **serie** ya es exclusión
mutua, así que el candado desaparece del código aunque siga habiendo memoria compartida por debajo.
Ni uno ni otro tienen lo que define al BEAM: aislamiento, y un fallo que no arrastra al vecino.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go es el pariente cercano
en el núcleo: gorrutina más canal es paso de mensajes, aunque de estilo CSP y no de actor.

### Zig

```zig
const std = @import("std");

// Zig no tiene canales en su biblioteca estándar: el buzón se construye a mano.
const Buzon = struct {
    mutex: std.Thread.Mutex = .{},
    cond: std.Thread.Condition = .{},
    cola: std.ArrayList(i64),
    cerrado: bool = false,
    total: i64 = 0,

    fn enviar(self: *Buzon, m: i64) !void {
        self.mutex.lock();
        defer self.mutex.unlock();
        try self.cola.append(m);
        self.cond.signal();
    }

    fn cerrar(self: *Buzon) void {
        self.mutex.lock();
        defer self.mutex.unlock();
        self.cerrado = true;
        self.cond.signal();
    }

    fn actor(self: *Buzon) void {
        self.mutex.lock();
        defer self.mutex.unlock();
        while (true) {
            while (self.cola.items.len > 0) {
                self.total += self.cola.orderedRemove(0);
            }
            if (self.cerrado) return;
            self.cond.wait(&self.mutex);
        }
    }
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    var buf: [4096]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;

    var buzon = Buzon{ .cola = std.ArrayList(i64).init(gpa.allocator()) };
    defer buzon.cola.deinit();

    const hilo = try std.Thread.spawn(.{}, Buzon.actor, .{&buzon});
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    while (it.next()) |t| try buzon.enviar(try std.fmt.parseInt(i64, t, 10));
    buzon.cerrar();
    hilo.join();

    try std.io.getStdOut().writer().print("total={d}\n", .{buzon.total});
}
```

### Nim

```nim
import std/strutils

# Nim aísla la memoria por hilo salvo lo que se comparte a propósito, y trae
# `Channel` en la biblioteca estándar. Compilar con `--threads:on` (por defecto en Nim 2).
var buzon: Channel[int]
var respuesta: Channel[int]

proc actor() {.thread.} =
  var total = 0
  while true:
    let m = buzon.recv()
    if m == low(int): break      # centinela de cierre
    total += m
  respuesta.send(total)

buzon.open()
respuesta.open()

var hilo: Thread[void]
createThread(hilo, actor)

for s in stdin.readLine().splitWhitespace():
  buzon.send(parseInt(s))
buzon.send(low(int))

echo "total=", respuesta.recv()
joinThread(hilo)
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv, std.concurrency;

// `std.concurrency` de D es paso de mensajes de manual: hilos aislados, `send`,
// `receive` con despacho por tipo de mensaje, y solo `shared`/`immutable` cruza.
void actor(Tid emisor) {
    long total = 0;
    bool seguir = true;
    while (seguir) {
        receive(
            (long m) { total += m; },
            (bool _) { seguir = false; }
        );
    }
    send(emisor, total);
}

void main() {
    auto nums = readln().split().map!(to!long).array;
    auto tid = spawn(&actor, thisTid);
    foreach (n; nums) send(tid, n);
    send(tid, true);
    writefln("total=%d", receiveOnly!long());
}
```

**Qué reconocer:** los tres compilan a nativo y aun así llegan a sitios muy distintos. Zig no te
regala nada: el buzón entero es tuyo, incluido el `signal`/`wait`. Nim y D sí traen la primitiva, y D
es el que más se parece al BEAM entre los lenguajes de sistemas: `receive` **despacha por el tipo del
mensaje**, igual que una cláusula `receive` de Erlang despacha por el patrón, y el sistema de tipos
impide que un hilo toque la memoria de otro si no está marcada `shared`. Esa es la diferencia real
frente a Go: en Go el canal transporta punteros y nada te impide compartir lo apuntado.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no cómo se
coordina el cálculo.

### Prolog

```prolog
:- initialization(main, main).

% SWI-Prolog sí tiene colas de mensajes de verdad (`message_queue_create/1`),
% y el estado del actor viaja como argumento porque nada se reasigna.
actor(Cola, Acumulado, Total) :-
    thread_get_message(Cola, M),
    (   M == fin
    ->  Total = Acumulado
    ;   Siguiente is Acumulado + M,
        actor(Cola, Siguiente, Total)
    ).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Utiles),
    maplist([S, N]>>number_string(N, S), Utiles, Nums),
    message_queue_create(Cola),
    forall(member(N, Nums), thread_send_message(Cola, N)),
    thread_send_message(Cola, fin),
    actor(Cola, 0, Total),
    format("total=~d~n", [Total]).
```

### Datalog

```datalog
% Datalog no tiene procesos, ni buzones, ni orden de ejecución observable:
% los "mensajes" son hechos y el "actor" es la agregación sobre ellos.
mensaje(1, 1).
mensaje(2, 2).
mensaje(3, 3).

total(T) :- T = sum N : mensaje(_, N).
```

**Qué reconocer:** Prolog sorprende dos veces. La primera, porque SWI trae colas de mensajes
auténticas. La segunda, y más importante: como en Prolog una variable se liga **una sola vez**, el
estado del actor no puede ser un campo que se muta —tiene que ser un argumento que se pasa a la
siguiente llamada—, y esa es exactamente la forma que toman los procesos de Erlang y el `Behavior` de
Akka. Datalog renuncia a todo: sin efectos, sin orden, sin identidad, solo el conjunto de hechos que
se deriva. Es la misma renuncia de SQL cuando no te deja decir en qué orden se recorren las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los ordena: ¿el estado que acumula la suma
está **aislado** o solo **protegido**? Dart, Tcl, D y Perl aíslan; C++, Kotlin, Ruby y VB.NET
protegen. El BEAM eligió aislar, y de ahí sale todo lo demás —fallos que no se propagan, supervisión,
distribución transparente—. Reconocer esa bifurcación en un lenguaje nuevo es lo transferible.

⏮️ [Volver a la clase 135](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
