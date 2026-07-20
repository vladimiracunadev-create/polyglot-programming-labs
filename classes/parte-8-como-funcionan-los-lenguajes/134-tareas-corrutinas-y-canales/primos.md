# 🧬 El mismo programa en las familias de lenguajes — Clase 134

> [⬅️ Volver a la clase 134](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —un productor que envía los valores por un canal y
un consumidor que se queda con el máximo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si la clase 133 preguntaba *quién ejecuta*, esta pregunta *quién cede el control y por dónde viajan
los datos*. Algunos lenguajes tienen la respuesta en el núcleo, otros en una biblioteca, y unos
cuantos no la tienen en absoluto.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** el productor envía los valores por un canal; el consumidor guarda el máximo

| stdin | esperado |
|---|---|
| `3 1 4` | `max=4` |
| `5` | `max=5` |
| `10 20 5` | `max=20` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tiene generadores (`yield`) y corrutinas (`async`/`await`); PHP tiene generadores desde 5.5.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)

productor = Fiber.new do          # las Fiber son corrutinas cooperativas de Ruby
  nums.each { |x| Fiber.yield(x) }
  nil                             # el nil final cierra la conversación
end

maximo = nil
while (x = productor.resume)
  maximo = x if maximo.nil? || x > maximo
end
puts "max=#{maximo}"
```

### Perl

```perl
# Perl no trae corrutinas ni canales en el núcleo (Coro y AnyEvent son de CPAN):
# lo más cercano es un CIERRE que se comporta como generador.
my @nums = split ' ', <STDIN>;
my $i = 0;
my $siguiente = sub { return $i < @nums ? $nums[$i++] : undef; };

my $maximo;
while (defined(my $x = $siguiente->())) {
    $maximo = $x if !defined($maximo) || $x > $maximo;
}
printf "max=%d\n", $maximo;
```

### Lua

```lua
local linea = io.read("l")

local productor = coroutine.wrap(function()   -- corrutina de primera clase
  for tok in linea:gmatch("%S+") do
    coroutine.yield(tonumber(tok))            -- cede un valor y se suspende
  end
end)

local maximo
for x in productor do                          -- el consumidor tira del productor
  if maximo == nil or x > maximo then maximo = x end
end
print(string.format("max=%d", maximo))
```

### Tcl

```tcl
gets stdin linea

proc productor {valores} {
    yield                          ;# Tcl 8.6 trae corrutinas de verdad
    foreach v $valores { yield $v }
    return ""                      ;# cadena vacía = fin
}

coroutine gen productor $linea
set maximo ""
while {[set x [gen]] ne ""} {
    if {$maximo eq "" || $x > $maximo} { set maximo $x }
}
puts "max=$maximo"
```

### R

```r
# R no tiene corrutinas, generadores ni canales: su idioma es vectorizar el problema
# o encadenarlo con Reduce. La "tubería" existe, pero no es concurrente.
v <- as.integer(strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]])
maximo <- Reduce(function(a, b) if (b > a) b else a, v)
cat(sprintf("max=%d\n", maximo))
```

**Qué reconocer:** Lua es aquí el **representante**, no el primo. Sus corrutinas son de primera
clase, simétricas y del núcleo del lenguaje: `coroutine.wrap` convierte una en un iterador y `for x
in productor` la consume como si fuera una lista. Tcl 8.6 llegó al mismo punto con `coroutine` y
`yield`, y Ruby con `Fiber` —que además es el motor de los `Enumerator` perezosos—. Perl y R marcan
el otro extremo: sin soporte en el lenguaje, lo más honesto es un **cierre con estado**, que es un
generador sin azúcar sintáctico. Fíjate en que ninguno de los cinco necesita un cerrojo: en una
corrutina el cambio de contexto ocurre **solo donde tú escribes `yield`**, así que entre dos `yield`
tienes exclusión mutua gratis. Esa es la ventaja que los hilos no dan.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
`async`/`await` sobre el bucle de eventos, y `async function*` para generadores asíncronos.

### Dart

```dart
import 'dart:io';

Stream<int> productor(List<int> nums) async* {   // generador asíncrono
  for (final x in nums) yield x;
}

Future<void> main() async {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  var maximo = nums.first;
  await for (final x in productor(nums)) {       // el consumidor espera cada valor
    if (x > maximo) maximo = x;
  }
  print('max=$maximo');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene corrutinas, generadores, async/await ni canales: el modelo es un solo
// hilo con eventos y callbacks sobre el bucle de fotogramas. Sin stdin, además.
package {
    public class Maximo {
        public static function calcular(nums:Array):String {
            var maximo:int = nums[0];
            for each (var x:int in nums) {
                if (x > maximo) { maximo = x; }
            }
            return "max=" + maximo;
        }
    }
}
```

**Qué reconocer:** Dart y JavaScript comparten la misma pareja de conceptos —`Future`/`Promise` para
un valor futuro, `Stream`/`AsyncIterable` para muchos— y la misma sintaxis para consumirlos:
`await` y `await for`. El `Stream` **es** el canal de esta familia, pero con una diferencia de fondo
frente al de Go: no hay ningún hilo esperando al otro lado, porque todo ocurre en el mismo bucle de
eventos y `await` solo devuelve el control al bucle. ActionScript enseña cómo era la vida antes de
esa sintaxis: los mismos programas, escritos con `addEventListener` y funciones de retorno anidadas,
que es exactamente el "infierno de callbacks" que `async`/`await` vino a resolver.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Sin corrutinas en el lenguaje hasta los hilos
virtuales del Proyecto Loom; cada primo eligió su propia salida.

### Kotlin

```kotlin
// kotlinx.coroutines: biblioteca, pero `suspend` sí es palabra clave del lenguaje.
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val canal = Channel<Int>()
    launch {                              // productor: una corrutina, no un hilo
        for (x in nums) canal.send(x)     // send suspende si nadie recibe
        canal.close()
    }
    var maximo = nums.first()
    for (x in canal) if (x > maximo) maximo = x
    println("max=$maximo")
}
```

### Scala

```scala
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.Duration

object Maximo {
  def main(args: Array[String]): Unit = {
    val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    val productor: Future[Array[Int]] = Future(nums)   // tarea asíncrona
    val maximo = Await.result(productor.map(_.max), Duration.Inf)
    println(s"max=$maximo")
  }
}
```

### Groovy

```groovy
// GPars ofrece DataflowQueue; con solo la biblioteca estándar de la JVM, el canal
// es una BlockingQueue y el cierre se marca con un centinela.
import java.util.concurrent.LinkedBlockingQueue

def nums = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def canal = new LinkedBlockingQueue<Integer>()
Thread.start {
    nums.each { canal.put(it) }
    canal.put(Integer.MIN_VALUE)
}
def maximo = Integer.MIN_VALUE
while (true) {
    def x = canal.take()
    if (x == Integer.MIN_VALUE) break
    if (x > maximo) maximo = x
}
println "max=$maximo"
```

### Clojure

```clojure
;; core.async es una biblioteca que reescribe el código con macros: `go` convierte
;; un bloque en una máquina de estados que no bloquea el hilo al esperar.
(require '[clojure.core.async :as a] '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))
      canal (a/chan)]
  (a/go
    (doseq [x nums] (a/>! canal x))
    (a/close! canal))
  (println (str "max=" (a/<!! (a/reduce max Integer/MIN_VALUE canal)))))
```

**Qué reconocer:** cuatro lenguajes sobre una máquina virtual que **no tenía** corrutinas, y cuatro
soluciones distintas al mismo hueco. Kotlin es el único que pidió ayuda al lenguaje: `suspend` es
palabra clave, y el compilador transforma la función en una máquina de estados con continuaciones,
de modo que sus `Channel` se parecen enormemente a los de Go y una corrutina cuesta unos pocos
cientos de bytes en vez de un hilo entero. Scala se queda en `Future`, que es una tarea sin
suspensión —o salta a los actores de Akka, que es el modelo de la clase 135—. Groovy y Clojure
delatan la carencia de la plataforma: Groovy termina usando una `BlockingQueue`, es decir, un canal
que **sí bloquea un hilo del sistema**, y Clojure evita ese coste reescribiendo el bloque `go` con
macros. Desde Java 21 los **hilos virtuales** vuelven barata la opción de Groovy y cambian el
cálculo para toda la familia.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). `async`/`await` nació aquí, y de aquí lo copiaron
JavaScript, Python, Rust y Kotlin.

### F\#

```fsharp
// MailboxProcessor: un agente con su propia cola de mensajes. Es el canal de F#.
let nums = stdin.ReadLine().Trim().Split(' ') |> Array.map int

let agente =
    MailboxProcessor<int * AsyncReplyChannel<int> option>.Start(fun buzon ->
        let rec bucle maximo =
            async {
                let! (x, respuesta) = buzon.Receive()
                let nuevo = max maximo x
                match respuesta with
                | Some canal -> canal.Reply(nuevo)
                | None -> ()
                return! bucle nuevo
            }
        bucle System.Int32.MinValue)

for x in nums do agente.Post(x, None)
let maximo = agente.PostAndReply(fun canal -> (System.Int32.MinValue, Some canal))
printfn "max=%d" maximo
```

### VB.NET

```vbnet
Imports System
Imports System.Threading.Channels
Imports System.Threading.Tasks

Module Maximo
    Async Function Ejecutar() As Task
        Dim sep = New Char() {" "c, ControlChars.Tab, ControlChars.Lf, ControlChars.Cr}
        Dim nums = Console.In.ReadToEnd().Split(sep, StringSplitOptions.RemoveEmptyEntries)
        Dim canal = Channel.CreateUnbounded(Of Integer)()

        Dim productor = Task.Run(Async Function()
                                     For Each s In nums
                                         Await canal.Writer.WriteAsync(Integer.Parse(s))
                                     Next
                                     canal.Writer.Complete()
                                 End Function)

        Dim maximo As Integer = Integer.MinValue
        Dim x As Integer
        While Await canal.Reader.WaitToReadAsync()
            While canal.Reader.TryRead(x)
                If x > maximo Then maximo = x
            End While
        End While
        Await productor
        Console.WriteLine("max=" & maximo)
    End Function

    Sub Main()
        Ejecutar().GetAwaiter().GetResult()
    End Sub
End Module
```

**Qué reconocer:** VB.NET y C# usan `System.Threading.Channels`, que es un canal con productor y
consumidor prácticamente calcado del de Go, incluida la contrapresión cuando se crea acotado. F#
llegó antes y por otro camino: el **`MailboxProcessor`** existe desde 2007, es un actor con su cola
privada, y su bucle recursivo `bucle nuevo` sustituye a la variable mutable —el estado del agente es
el **argumento** de la siguiente vuelta—. Ese `AsyncReplyChannel` es la pieza que convierte el
mensaje en pregunta y respuesta. Es la misma idea que verás en la clase 135 con Erlang, adelantada
una década dentro del CLR.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Ni corrutinas ni canales: hilos, cerrojos y
variables de condición.

### C++

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <sstream>
#include <string>
#include <thread>

// C++20 tiene corrutinas, pero son de bajísimo nivel; std::generator llega en C++23.
// Un canal como el de Go se construye a mano: cola + mutex + variable de condición.
int main() {
    std::string linea;
    std::getline(std::cin, linea);

    std::queue<long long> canal;
    std::mutex m;
    std::condition_variable cv;
    bool cerrado = false;

    std::thread productor([&] {
        std::istringstream ss(linea);
        for (long long x; ss >> x;) {
            std::lock_guard<std::mutex> lk(m);
            canal.push(x);
            cv.notify_one();
        }
        std::lock_guard<std::mutex> lk(m);
        cerrado = true;
        cv.notify_one();
    });

    long long maximo = 0;
    bool primero = true;
    for (;;) {
        std::unique_lock<std::mutex> lk(m);
        cv.wait(lk, [&] { return !canal.empty() || cerrado; });
        if (canal.empty()) break;
        const long long x = canal.front();
        canal.pop();
        lk.unlock();
        if (primero || x > maximo) { maximo = x; primero = false; }
    }
    productor.join();

    std::cout << "max=" << maximo << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>
#include <limits.h>

int main(void) {
    @autoreleasepool {
        // Objective-C nunca tuvo corrutinas: async/await llegó a la plataforma con
        // Swift. Aquí el canal es una cola serie de Grand Central Dispatch.
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *nums =
            [[linea stringByTrimmingCharactersInSet:blancos]
             componentsSeparatedByCharactersInSet:blancos];

        __block long long maximo = LLONG_MIN;
        dispatch_queue_t consumidor = dispatch_queue_create("max", DISPATCH_QUEUE_SERIAL);
        for (NSString *s in nums) {
            long long x = [s longLongValue];
            dispatch_async(consumidor, ^{ if (x > maximo) { maximo = x; } });
        }
        dispatch_sync(consumidor, ^{});   // barrera: espera a que se consuma todo
        printf("max=%lld\n", maximo);
    }
    return 0;
}
```

**Qué reconocer:** compara el tamaño de estos dos programas con el de Kotlin o el de Go. Esa
diferencia **es** el valor de tener canales en la biblioteca: aquí hay que construir la cola, el
cerrojo, la variable de condición y la señal de cierre a mano, y cada una de esas piezas es un sitio
donde equivocarse —olvidar el `notify_one` deja al consumidor dormido para siempre—. C++20 sí añadió
corrutinas al lenguaje, pero como **infraestructura para autores de bibliotecas**: `co_await` y
`co_yield` no sirven de nada sin un tipo `promise_type` que tú escribas, y hasta `std::generator` de
C++23 no hubo nada listo para usar. Objective-C nunca las tuvo: la respuesta de la plataforma fueron
las colas de GCD, y luego Swift.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go puso el canal en el
centro del lenguaje —"comparte memoria comunicando"—; Rust tiene `async`/`await` y `mpsc`.

### Zig

```zig
const std = @import("std");

// `async`/`await` están DESHABILITADOS desde Zig 0.11 a la espera del nuevo backend:
// hoy el canal se monta con hilo, mutex y variable de condición.
const Canal = struct {
    datos: [64]i64 = undefined,
    n: usize = 0,
    listo: bool = false,
    m: std.Thread.Mutex = .{},
    cond: std.Thread.Condition = .{},
};

fn productor(canal: *Canal, linea: []const u8) void {
    var it = std.mem.tokenizeAny(u8, linea, " \t");
    while (it.next()) |tok| {
        const x = std.fmt.parseInt(i64, tok, 10) catch continue;
        canal.m.lock();
        canal.datos[canal.n] = x;
        canal.n += 1;
        canal.m.unlock();
    }
    canal.m.lock();
    canal.listo = true;
    canal.cond.signal();
    canal.m.unlock();
}

pub fn main() !void {
    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;

    var canal = Canal{};
    const recortada = std.mem.trim(u8, linea, " \r\t");
    const h = try std.Thread.spawn(.{}, productor, .{ &canal, recortada });

    canal.m.lock();
    while (!canal.listo) canal.cond.wait(&canal.m);
    var maximo = canal.datos[0];
    for (canal.datos[0..canal.n]) |x| {
        if (x > maximo) maximo = x;
    }
    canal.m.unlock();
    h.join();

    try std.io.getStdOut().writer().print("max={d}\n", .{maximo});
}
```

### Nim

```nim
import std/strutils

# Nim tiene iteradores de CIERRE, que son corrutinas de un solo sentido, y `Channel[T]`
# para comunicar hilos de verdad. Aquí el productor es un iterador perezoso.
iterator productor(linea: string): int {.closure.} =
  for tok in linea.splitWhitespace():
    yield tok.parseInt()

var maximo = low(int)
for x in productor(stdin.readLine().strip()):
  if x > maximo: maximo = x
echo "max=", maximo
```

### D

```d
import std.stdio, std.string, std.conv, std.array;
import std.concurrency;

// std.concurrency: paso de mensajes tipado entre hilos, con `receive` por patrón.
void productor(Tid consumidor, string linea) {
    foreach (tok; linea.split())
        send(consumidor, tok.to!long);
    send(consumidor, true);   // centinela de cierre
}

void main() {
    immutable linea = readln().strip().idup;
    spawn(&productor, thisTid, linea);

    long maximo = long.min;
    bool fin = false;
    while (!fin) {
        receive(
            (long x) { if (x > maximo) maximo = x; },
            (bool _) { fin = true; }
        );
    }
    writefln("max=%d", maximo);
}
```

**Qué reconocer:** los tres se separan en **dónde vive la abstracción**. Zig es hoy el caso más
honesto y más incómodo: tuvo `async`/`await` en el lenguaje, los **desactivó** en 0.11 mientras
rehace su backend, y por eso el código de arriba se parece más al de C++ que al de Go. Nim distingue
dos cosas que Go junta: sus **iteradores de cierre** son corrutinas para producir valores en el
mismo hilo —sin coste de sincronización, como las de Lua— y su `Channel[T]` es para comunicar hilos
distintos, con copia profunda de por medio. D acerca `std.concurrency` al modelo de actores: no hay
un canal nombrado sino un buzón por hilo, y `receive` despacha **por el tipo del mensaje**, algo que
ni Go ni Rust hacen. Rust está en medio: `async`/`await` en el lenguaje, pero sin ejecutor en la
biblioteca estándar, así que hay que traer Tokio.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Un cursor es un productor perezoso, pero el
orden de evaluación no es del programador.

### Prolog

```prolog
:- initialization(main, main).

% SWI llama "coroutining" a la ejecución suspendida: freeze/2 retiene un objetivo
% hasta que su variable se liga. Para productor/consumidor entre hilos hay colas de
% mensajes (message_queue_create/3). El backtracking ya es un generador perezoso.
main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Textos),
    maplist([S, N]>>number_string(N, S), Textos, Nums),
    max_list(Nums, Maximo),
    format("max=~d~n", [Maximo]).
```

### Datalog

```datalog
% Sin canales, sin orden de ejecución y sin productor: el motor decide la estrategia
% de evaluación y el máximo se expresa como una agregación sobre los hechos.
valor(3).
valor(1).
valor(4).

max_valor(M) :- M = max v : { valor(v) }.
```

**Qué reconocer:** Prolog ya trae de fábrica el mecanismo que las corrutinas imitan: al pedir la
siguiente solución con `;`, el motor **reanuda** la ejecución donde la dejó, que es exactamente lo
que hace `yield`. Encima añade el *coroutining* propiamente dicho —`freeze/2`, `when/2`, `dif/2`—,
donde un objetivo queda **suspendido** hasta que otra parte del programa ligue su variable: no es un
canal, es una espera declarativa sobre un dato. Datalog renuncia incluso a eso: no hay orden, no hay
productor y no hay consumidor, solo un `max` agregado sobre un conjunto de hechos, igual que el
`MAX()` de SQL no te deja decidir en qué orden se leen las filas.

---

## Y de vuelta a la clase

Veinte lenguajes y cuatro respuestas a "cómo cedo el control": **corrutinas en el lenguaje** (Lua,
Tcl, Ruby, Kotlin, Dart, Nim), **canales como biblioteca** (.NET, core.async, Go, Rust con Tokio),
**colas y cerrojos a mano** (C++, Zig, Objective-C, Groovy) y **nada, porque el modelo no lo pide**
(Prolog, Datalog, R). Reconocer en cuál de los cuatro grupos cae un lenguaje nuevo te dice de
antemano cuánto código vas a tener que escribir tú.

⏮️ [Volver a la clase 134](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
