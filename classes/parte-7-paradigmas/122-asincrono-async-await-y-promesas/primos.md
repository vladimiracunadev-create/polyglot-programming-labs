# 🧬 El mismo programa en las familias de lenguajes — Clase 122

> [⬅️ Volver a la clase 122](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —obtener el doble de un número a través de una tarea
asíncrona y esperarla— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

`async`/`await` es la palabra clave más copiada de la década, pero no todos la tienen. Donde falta,
lo que hay debajo sigue siendo lo mismo: **un valor que aún no está y una forma de esperarlo**.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** `await doble(n)`, donde `doble(n) = 2n`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `6` | `resultado=12` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tardó hasta la 3.5 en tener `async`/`await`; en esta familia, casi ninguno lo consiguió.

### Ruby

```ruby
# Ruby no tiene async/await en el lenguaje. Se espera con Thread#value, o con Fibers
# y un scheduler (Ruby 3) para que la E/S no bloquee el hilo.
n = STDIN.gets.to_i
tarea = Thread.new { n * 2 }
puts "resultado=#{tarea.value}"
```

### Perl

```perl
# Perl tampoco lo trae: las promesas vienen del ecosistema (Future, IO::Async,
# Mojo::Promise), donde `then` registra la continuación y `wait` corre el bucle:
#     my $promesa = Mojo::Promise->new;
#     $promesa->then(sub { print "resultado=$_[0]\n" });
#     $promesa->resolve($n * 2);
#     $promesa->wait;
# Sin CPAN el núcleo solo da la forma, no el motor: un trabajo diferido y una
# cola de continuaciones que hay que vaciar a mano. No hay bucle de eventos.
chomp(my $n = <STDIN>);

my $tarea = sub { $n * 2 };                        # lanzar: trabajo diferido
my @continuaciones = (sub { print "resultado=$_[0]\n" });   # then

$_->($tarea->()) for @continuaciones;              # wait: el planificador eres tú
```

### Lua

```lua
-- Lua no tiene async/await ni promesas: la corrutina es la primitiva y quien la
-- reanuda hace de planificador. No hay bucle de eventos en la biblioteca estándar.
local n = tonumber(io.read("l"))

local tarea = coroutine.create(function(x)
  coroutine.yield(x * 2)
end)

local _, resultado = coroutine.resume(tarea, n)
print("resultado=" .. resultado)
```

### Tcl

```tcl
# Tcl sí tiene bucle de eventos en el núcleo: `after` encola el trabajo y `vwait`
# bloquea hasta que la variable cambie. Es await escrito a mano.
gets stdin n

after 0 [list apply {{x} {
    set ::resultado [expr {$x * 2}]
}} $n]

vwait ::resultado
puts "resultado=$::resultado"
```

### R

```r
# R es secuencial y no tiene async/await. El paquete future da un objeto diferido
# que se resuelve con value(), pero por defecto el plan es sequential: no hay espera real.
library(future)

n <- as.integer(readLines("stdin", n = 1))
tarea <- future(n * 2)
cat(paste0("resultado=", value(tarea), "\n"))
```

**Qué reconocer:** de los cinco, ninguno tiene la palabra `await`, y sin embargo los cinco expresan
la misma forma: *lanzar* y luego *esperar*. Ruby usa un hilo y `value` bloquea hasta que termina.
Tcl es el más interesante porque ya tenía la pieza que le falta a los demás —un bucle de eventos en
el núcleo—, así que `vwait` es literalmente lo que un `await` hace por dentro: ceder el control al
bucle hasta que alguien deje el valor. Lua no llega ni ahí: sin planificador, `resume` es una
llamada a función con otro nombre. Perl deja la carencia a la vista: el núcleo da el trabajo
diferido y la cola de continuaciones, pero nadie la vacía salvo tú, y ese bucle que falta es
justo lo que `Mojo::Promise` trae del CPAN. R lo declara sin rodeos: el objeto `future` existe,
pero por defecto se evalúa en el momento.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia donde nació la promesa como concepto de masas, y donde el bucle de eventos es obligatorio.

### Dart

```dart
import 'dart:io';

Future<int> doble(int x) async => x * 2;

void main() async {
  final n = int.parse(stdin.readLineSync()!.trim());
  final resultado = await doble(n);
  print('resultado=$resultado');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 no tiene Promise ni async/await: lo asíncrono se expresa con
// eventos y callbacks sobre un bucle de eventos de un solo hilo. La continuación
// se registra antes, y el evento la invoca después.
package {
    import flash.events.Event;
    import flash.events.EventDispatcher;

    public class Doble extends EventDispatcher {
        private var valor:int;

        public function pedir(n:int):void {
            addEventListener(Event.COMPLETE, function (e:Event):void {
                trace("resultado=" + valor);
            });
            valor = n * 2;
            dispatchEvent(new Event(Event.COMPLETE));
        }
    }
}
```

**Qué reconocer:** Dart es JavaScript con los deberes hechos: `Future` es su `Promise`, `async` y
`await` se escriben igual, y el tipo `Future<int>` deja constancia en la firma de que el valor llega
más tarde —algo que en JS solo sabes leyendo el cuerpo—. ActionScript es el pasado del que se huyó:
lo que en Dart es una línea con `await`, aquí es registrar un manejador antes y confiar en que el
evento se dispare después. Encadenar tres pasos así es el famoso *callback hell*, y `async`/`await`
existe precisamente para que este segundo bloque no haga falta.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). `CompletableFuture` fue la respuesta de Java; y
sus primos, cada uno, decidieron que no bastaba.

### Kotlin

```kotlin
import kotlinx.coroutines.runBlocking

suspend fun doble(x: Int): Int = x * 2

fun main() = runBlocking {
    val n = readLine()!!.trim().toInt()
    println("resultado=${doble(n)}")
}
```

### Scala

```scala
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.Duration

object Asincrono extends App {
  def doble(x: Int): Future[Int] = Future(x * 2)

  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"resultado=${Await.result(doble(n), Duration.Inf)}")
}
```

### Groovy

```groovy
import java.util.concurrent.CompletableFuture

def n = System.in.newReader().readLine().trim() as int
def tarea = CompletableFuture.supplyAsync { n * 2 }
println "resultado=${tarea.get()}"
```

### Clojure

```clojure
;; Clojure no tiene async/await: `future` devuelve algo que se espera con deref (@).
;; core.async añade canales y `go`, que es otro modelo (el de Go), no el de promesas.
(require '[clojure.string :as str])

(let [n     (parse-long (str/trim (read-line)))
      tarea (future (* 2 n))]
  (println (str "resultado=" @tarea)))
```

**Qué reconocer:** Groovy es Java literal: `supplyAsync` y `get()`. Scala envuelve lo mismo en un
`Future` que es un **valor componible** —`map` y `flatMap` encadenan sin bloquear, y `Await.result`
solo aparece al final porque hay que imprimir—. Kotlin es el único con `await` de verdad, aunque no
se vea: `suspend` marca la función como suspendible y la llamada `doble(n)` **es** el punto de
espera; el compilador la convierte en una máquina de estados y por eso una corrutina bloqueada no
ocupa un hilo. Clojure declina el modelo entero: `@tarea` bloquea el hilo actual, sin más, y quien
quiera asincronía de verdad usa `core.async`, que copia los canales de Go en vez de las promesas de
JavaScript.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Aquí nació `async`/`await` tal como lo copió
después medio mundo, JavaScript incluido.

### F\#

```fsharp
open System

// F# tuvo workflows asíncronos años antes que C#: `async { }` es una computation
// expression, y `let!` es el await. Async es perezoso: no arranca hasta que se corre.
let doble x = async { return x * 2 }

[<EntryPoint>]
let main _ =
    let n = Console.ReadLine().Trim() |> int
    let resultado = doble n |> Async.RunSynchronously
    printfn "resultado=%d" resultado
    0
```

### VB.NET

```vbnet
Imports System.Threading.Tasks

Module Asincrono
    Async Function Doble(x As Integer) As Task(Of Integer)
        Return Await Task.FromResult(x * 2)
    End Function

    ' VB.NET no admite un Main asíncrono (C# sí desde la 7.1), así que la raíz
    ' bloquea con .Result en vez de con Await.
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("resultado=" & Doble(n).Result)
    End Sub
End Module
```

**Qué reconocer:** VB.NET tiene el mismo `Async`/`Await` que C# —misma `Task`, mismo compilador
generando la máquina de estados— y solo se separa en un detalle revelador: sin `Main` asíncrono, la
cadena de `await` tiene que romperse en algún sitio con un `.Result` bloqueante. F# llegó primero y
por otro camino: su `Async` es **perezoso**, un plan que describe qué hacer y que no empieza hasta
que alguien lo lanza con `RunSynchronously` o `Async.Start`. Una `Task` de .NET, en cambio, ya está
corriendo en el momento en que la tienes en la mano. Esa diferencia —descripción contra ejecución en
curso— es la misma que separa `IO` de Haskell de una promesa de JavaScript.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene nada de esto: lo asíncrono es un
descriptor de fichero y un `select`.

### C++

```cpp
#include <future>
#include <iostream>

int main() {
    int n = 0;
    std::cin >> n;

    // std::future es la promesa; C++20 añadió co_await, pero sin tipo de tarea
    // en la biblioteca estándar todavía hay que traérselo de fuera.
    std::future<int> tarea = std::async(std::launch::async, [n] { return n * 2; });

    std::cout << "resultado=" << tarea.get() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);

        // Objective-C nunca tuvo async/await: eso llegó con Swift. Aquí, GCD y
        // un semáforo para esperar el bloque.
        __block int resultado = 0;
        dispatch_semaphore_t hecho = dispatch_semaphore_create(0);
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
            resultado = n * 2;
            dispatch_semaphore_signal(hecho);
        });
        dispatch_semaphore_wait(hecho, DISPATCH_TIME_FOREVER);

        printf("resultado=%d\n", resultado);
    }
    return 0;
}
```

**Qué reconocer:** ninguno de los dos tiene `await` usable en la biblioteca estándar, y los dos
resuelven la espera **bloqueando**. `std::future::get()` es exactamente eso: para el hilo hasta que
el valor exista. C++20 sí añadió `co_await` como palabra clave, pero la biblioteca no trae todavía
el tipo de tarea que lo acompañe, así que en la práctica se importa de fuera. Objective-C ni lo
intenta: el par `dispatch_async` + semáforo es el patrón clásico, y es justo lo que Swift vino a
sustituir con su `async`/`await`. Que aquí haya que crear un semáforo a mano deja ver la cantidad de
trabajo que una palabra clave puede ahorrarte.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Dos respuestas opuestas:
Go esconde el planificador; Rust te obliga a elegirlo.

### Zig

```zig
// El async/await del lenguaje salió de Zig en la 0.11, pendiente de rediseño: hoy
// lo concurrente se expresa con hilos, y la espera es un join.
const std = @import("std");

fn doble(n: i64, salida: *i64) void {
    salida.* = n * 2;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const leido = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, leido, " \r"), 10);

    var resultado: i64 = 0;
    const h = try std.Thread.spawn(.{}, doble, .{ n, &resultado });
    h.join();

    try std.io.getStdOut().writer().print("resultado={d}\n", .{resultado});
}
```

### Nim

```nim
# Nim sí trae async/await en la biblioteca estándar, con su propio bucle de eventos.
import std/[strutils, asyncdispatch]

proc doble(x: int): Future[int] {.async.} =
  return x * 2

let n = stdin.readLine().strip().parseInt()
echo "resultado=" & $(waitFor doble(n))
```

### D

```d
// D no tiene async/await: lo más cercano es un task perezoso que se fuerza al
// pedir su valor. Las fibers de core.thread permiten construirlo, pero a mano.
import std.conv, std.parallelism, std.stdio, std.string;

int doble(int x) { return x * 2; }

void main() {
    const n = readln().strip().to!int;
    auto tarea = task!doble(n);
    tarea.executeInNewThread();
    writefln("resultado=%d", tarea.yieldForce);
}
```

**Qué reconocer:** Nim es el único de los tres con el modelo completo —`{.async.}` reescribe la
función en una máquina de estados, `Future[int]` es el valor pendiente y `waitFor` corre el bucle
hasta que llegue—, y es notable que quepa en la biblioteca estándar, algo que Rust dejó
deliberadamente fuera para que eligieras tu runtime. Zig es el caso contrario y merece decirse
claro: **tuvo** `async`/`await` en el lenguaje y los **quitó** en la 0.11 al rediseñar la E/S, así
que hoy lo idiomático es un hilo y un `join`. D se queda en el terreno de la clase anterior: `task`
y `yieldForce` son concurrencia, no asincronía; la diferencia es que un `await` real libera el hilo
mientras espera, y un `yieldForce` no.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una consulta no "tarda" desde dentro del
lenguaje: la latencia la ve el cliente, nunca la expresión.

### Prolog

```prolog
% Prolog no tiene async/await; SWI lanza un hilo y recoge el valor de una cola,
% que es la misma forma "lanzar y esperar" sin sintaxis dedicada.
:- initialization(main, main).

doble(N, Cola) :-
    D is N * 2,
    thread_send_message(Cola, D).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    message_queue_create(Cola),
    thread_create(doble(N, Cola), Hilo, []),
    thread_get_message(Cola, Resultado),
    thread_join(Hilo),
    format("resultado=~d~n", [Resultado]).
```

### Datalog

```datalog
% Datalog no tiene tiempo, ni efectos, ni espera: una regla no "tarda" y no existe
% el concepto de valor pendiente. Lo único declarable es la relación entre n y su doble.
n(5).

resultado(Y) :- n(X), Y = X * 2.
```

**Qué reconocer:** Prolog vuelve a demostrar que la implementación pesa más que el paradigma:
`thread_get_message` bloquea hasta que el hilo deposite el valor, que es *lanzar y esperar* con otro
vocabulario. Datalog es el final natural de esta serie de cuatro clases: sin eventos, sin flujos,
sin hilos y sin espera, porque nada de eso existe cuando no hay tiempo en el modelo. `resultado(Y)`
no ocurre después de `n(X)`: simplemente es verdad al mismo tiempo. Un `await` solo tiene sentido
cuando el lenguaje admite que las cosas pasan en un orden.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una idea que sobrevive con o sin palabra clave: **un valor que
todavía no está**. Se llama `Future`, `Promise`, `Task`, `FlowVar`, `AsyncReplyChannel` o
simplemente una variable y un semáforo. Lo que cambia es si esperar **bloquea un hilo** (C++,
Objective-C, Clojure) o solo **suspende una función** (Kotlin, Dart, Nim, C#). Eso es lo
transferible.

⏮️ [Volver a la clase 122](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
