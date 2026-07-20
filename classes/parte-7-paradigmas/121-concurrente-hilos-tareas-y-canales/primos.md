# 🧬 El mismo programa en las familias de lenguajes — Clase 121

> [⬅️ Volver a la clase 121](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —repartir una lista en dos partes, sumar cada una
por separado y combinar— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Esta es la tanda donde los primos **más se separan**. En las clases anteriores casi todos decían lo
mismo con otra sintaxis; aquí hay lenguajes con hilos de sistema, lenguajes con corrutinas de un
solo hilo, lenguajes que prefieren procesos y lenguajes que sencillamente no tienen concurrencia.
Cuando eso pasa, lo decimos.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `suma=<suma total>`
- **Regla:** repartir la lista, sumar por partes, combinar los parciales

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma=10` |
| `5` | `suma=5` |
| `10 20 30` | `suma=60` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia de los intérpretes es donde más duele la concurrencia: casi todos nacieron con un
intérprete de un solo hilo y arrastran esa decisión.

### Ruby

```ruby
# En MRI los hilos existen pero no dan paralelismo: el GVL solo deja correr uno a la vez
# (sirven para E/S, no para CPU). Para paralelismo real están los Ractor, desde Ruby 3.0.
nums = STDIN.read.split.map(&:to_i)
medio = nums.size / 2

partes = [nums[0...medio], nums[medio..]]
tareas = partes.map { |p| Thread.new { p.sum } }

puts "suma=#{tareas.sum(&:value)}"
```

### Perl

```perl
# Los hilos de Perl (ithreads) están desaconsejados desde hace años: copian el
# intérprete entero por hilo. Lo idiomático es repartir en procesos con fork.
my @nums = split ' ', do { local $/; <STDIN> };
my $medio = int(@nums / 2);
my @partes = ([ @nums[0 .. $medio - 1] ], [ @nums[$medio .. $#nums] ]);

my $total = 0;
for my $parte (@partes) {
    pipe(my $lector, my $escritor);
    if (fork() == 0) {
        close $lector;
        my $s = 0;
        $s += $_ for @$parte;
        print $escritor "$s\n";
        exit 0;
    }
    close $escritor;
    $total += <$lector>;
    wait;
}
print "suma=$total\n";
```

### Lua

```lua
-- Lua no tiene hilos: sus corrutinas son cooperativas y viven en un solo hilo del
-- sistema. No hay paralelismo, solo intercalado — y solo cuando alguien hace resume.
local nums = {}
for s in io.read("l"):gmatch("%S+") do
  nums[#nums + 1] = tonumber(s)
end

local function sumador(desde, hasta)
  return coroutine.create(function()
    local s = 0
    for i = desde, hasta do s = s + nums[i] end
    coroutine.yield(s)
  end)
end

local medio = math.floor(#nums / 2)
local _, p1 = coroutine.resume(sumador(1, medio))
local _, p2 = coroutine.resume(sumador(medio + 1, #nums))

print("suma=" .. (p1 + p2))
```

### Tcl

```tcl
# Tcl sí tiene hilos reales (paquete Thread), pero cada uno lleva su propio
# intérprete y no comparten variables: comunicarse es enviar un script.
package require Thread

gets stdin linea
set nums [split $linea]
set medio [expr {[llength $nums] / 2}]
set partes [list [lrange $nums 0 [expr {$medio - 1}]] [lrange $nums $medio end]]

set total 0
foreach parte $partes {
    set t [thread::create]
    incr total [thread::send $t [list apply {{p} {
        set acc 0
        foreach x $p { incr acc $x }
        return $acc
    }} $parte]]
    thread::release $t
}
puts "suma=$total"
```

### R

```r
# R es esencialmente secuencial: no hay hilos en el lenguaje. Lo más cercano es
# parallel::mclapply, que lanza *procesos* con fork — y en Windows ni eso: cae a lapply.
library(parallel)

v <- as.integer(strsplit(readLines("stdin", n = 1), " +")[[1]])
medio <- length(v) %/% 2
partes <- list(head(v, medio), tail(v, length(v) - medio))

parciales <- mclapply(partes, sum)
cat(paste0("suma=", sum(unlist(parciales)), "\n"))
```

**Qué reconocer:** aquí los cinco cuentan historias distintas y ninguna es la de Python. Ruby es el
más parecido —hilos que se ven reales pero que el GVL serializa, igual que el GIL de CPython—, con
la salida de emergencia de los `Ractor`, que aíslan memoria para poder correr de verdad en paralelo.
Perl tiró la toalla con los hilos y su respuesta es `fork`: dos **procesos**, memoria separada, y
una tubería para devolver el parcial. Tcl elige el mismo aislamiento pero dentro del proceso: un
intérprete por hilo, comunicación por mensajes. Lua es el caso más honesto de todos: sus corrutinas
no son concurrencia, son **multitarea cooperativa** —el control solo cambia de manos cuando alguien
llama a `yield` o `resume`—, así que el programa de arriba es estrictamente secuencial. R ni
siquiera lo intenta desde el lenguaje.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia del bucle de eventos: un solo hilo por diseño, y todo lo demás es aislamiento.

### Dart

```dart
import 'dart:io';
import 'dart:isolate';

void main() async {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final medio = nums.length ~/ 2;

  // Los isolates no comparten memoria: se envía una copia y se recibe el parcial.
  final izq = nums.sublist(0, medio);
  final der = nums.sublist(medio);
  final p1 = await Isolate.run(() => izq.fold<int>(0, (a, b) => a + b));
  final p2 = await Isolate.run(() => der.fold<int>(0, (a, b) => a + b));

  print('suma=${p1 + p2}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 tiene un único hilo con bucle de eventos: no hay concurrencia real.
// Los Worker de AIR/Flash 11.4 son intérpretes aislados que hablan por mensajes,
// no hilos con memoria compartida. Sin ellos, esto es un cálculo secuencial.
package {
    public class Suma {
        public static function total(nums:Array):String {
            var medio:int = nums.length / 2;
            return "suma=" + (parcial(nums.slice(0, medio)) + parcial(nums.slice(medio)));
        }

        private static function parcial(parte:Array):int {
            var s:int = 0;
            for each (var x:int in parte) s += x;
            return s;
        }
    }
}
```

**Qué reconocer:** ninguno de los dos comparte memoria entre unidades de ejecución, y esa es la
marca de la familia. Dart lo convierte en su modelo central: un `Isolate` es un hilo **con su propio
montón**, así que `Isolate.run` copia los datos de entrada y devuelve el resultado copiado. No hay
carreras de datos porque no hay datos compartidos —el mismo trato que hace Rust por otro camino—.
ActionScript se quedó un escalón antes: el reproductor tiene un solo hilo, el bucle de eventos, y
por eso el bloque de arriba **no es concurrente**, solo está escrito como si repartiera el trabajo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM sí tiene hilos de sistema de verdad y
memoria compartida; lo que cambia entre sus lenguajes es qué te dan para no pegarte un tiro.

### Kotlin

```kotlin
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val medio = nums.size / 2

    val p1 = async(Dispatchers.Default) { nums.subList(0, medio).sum() }
    val p2 = async(Dispatchers.Default) { nums.subList(medio, nums.size).sum() }

    println("suma=${p1.await() + p2.await()}")
}
```

### Scala

```scala
import scala.concurrent.{Await, Future}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.Duration

object Suma extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val (izq, der) = nums.splitAt(nums.length / 2)

  // Los Future se lanzan aquí: si se crearan dentro del for, correrían en serie.
  val f1 = Future(izq.sum)
  val f2 = Future(der.sum)
  val total = for { p1 <- f1; p2 <- f2 } yield p1 + p2

  println(s"suma=${Await.result(total, Duration.Inf)}")
}
```

### Groovy

```groovy
import java.util.concurrent.Callable
import java.util.concurrent.Executors

def nums = System.in.text.trim().split(/\s+/)*.toInteger()
def medio = (nums.size() / 2) as int
def pool = Executors.newFixedThreadPool(2)

def tareas = [nums[0..<medio], nums[medio..<nums.size()]].collect { parte ->
    pool.submit({ parte.sum(0) } as Callable)
}
println "suma=${tareas.sum { it.get() }}"
pool.shutdown()
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums  (mapv parse-long (str/split (str/trim (read-line)) #"\s+"))
      medio (quot (count nums) 2)
      total (ref 0)
      tareas [(future (dosync (alter total + (reduce + (subvec nums 0 medio)))))
              (future (dosync (alter total + (reduce + (subvec nums medio)))))]]
  (run! deref tareas)
  (println (str "suma=" @total)))
```

**Qué reconocer:** los cuatro corren sobre el mismo `ForkJoinPool` de Java por debajo, pero cada uno
te vende una idea distinta de qué es una tarea. Groovy es Java sin disfraz: pool, `Callable`,
`Future.get()`. Scala envuelve eso en un `Future` **componible**, un valor que se transforma con
`map` y `for` antes de existir —y por eso hay que fijarse en dónde se construye: dentro del `for`
irían en serie—. Kotlin cambia de mecanismo: una corrutina `suspend` no ocupa un hilo mientras
espera, así que puedes tener cientos de miles. Clojure es el que ataca el problema de raíz: no
sincroniza el acceso a una variable compartida, sino que usa **STM** —`ref` más `dosync`—, una
transacción con la misma semántica que una de base de datos, que reintenta sola si hubo conflicto.
Con `atom` bastaría aquí; con `ref` se ve la maquinaria.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR comparte `Task` y el pool de hilos entre
todos sus lenguajes, pero F# trae encima un modelo que no existe en el resto.

### F\#

```fsharp
open System

// MailboxProcessor es un actor: una cola de mensajes con estado privado que se
// procesa de uno en uno. Nadie toca el acumulador desde fuera, así que no hay
// nada que sincronizar.
type Mensaje =
    | Sumar of int list
    | Total of AsyncReplyChannel<int>

let acumulador =
    MailboxProcessor.Start(fun buzon ->
        let rec bucle total =
            async {
                match! buzon.Receive() with
                | Sumar parte -> return! bucle (total + List.sum parte)
                | Total canal ->
                    canal.Reply total
                    return! bucle total
            }
        bucle 0)

let nums =
    Console.ReadLine().Split(' ', StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
    |> Array.toList

let medio = nums.Length / 2
acumulador.Post(Sumar(List.truncate medio nums))
acumulador.Post(Sumar(List.skip medio nums))

printfn "suma=%d" (acumulador.PostAndReply Total)
```

### VB.NET

```vbnet
Imports System.Linq
Imports System.Threading.Tasks

Module Suma
    Sub Main()
        Dim nums = Console.ReadLine().Trim() _
            .Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries) _
            .Select(Function(s) Integer.Parse(s)).ToArray()
        Dim medio = nums.Length \ 2

        Dim t1 = Task.Run(Function() nums.Take(medio).Sum())
        Dim t2 = Task.Run(Function() nums.Skip(medio).Sum())
        Task.WaitAll(t1, t2)

        Console.WriteLine("suma=" & (t1.Result + t2.Result))
    End Sub
End Module
```

**Qué reconocer:** VB.NET es C# palabra por palabra —`Task.Run`, `WaitAll`, `.Result`— porque la
concurrencia de .NET vive en la biblioteca, no en la sintaxis. F# es la sorpresa de toda esta
página: su `MailboxProcessor` es **un actor de manual**, el mismo modelo que hizo famoso a Erlang y
que en la JVM requiere Akka. Un actor no comparte estado: recibe mensajes de una cola, los procesa
de uno en uno y guarda su estado como el argumento de una función recursiva (`bucle total`). Fíjate
en que aquí **no hay ni un candado ni una operación atómica**, y aun así no hay carrera posible: el
orden de `Post` garantiza que los dos parciales llegan antes que la petición de `Total`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Los hilos POSIX son la capa sobre la que están
construidos casi todos los demás de esta página.

### C++

```cpp
#include <future>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x;) nums.push_back(x);

    const auto medio = nums.begin() + static_cast<std::ptrdiff_t>(nums.size() / 2);
    auto t1 = std::async(std::launch::async, [&] { return std::accumulate(nums.begin(), medio, 0LL); });
    auto t2 = std::async(std::launch::async, [&] { return std::accumulate(medio, nums.end(), 0LL); });

    std::cout << "suma=" << t1.get() + t2.get() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSMutableArray<NSNumber *> *nums = [NSMutableArray array];
        for (int x; scanf("%d", &x) == 1;) [nums addObject:@(x)];

        NSUInteger medio = nums.count / 2;
        __block long long p1 = 0, p2 = 0;

        dispatch_group_t grupo = dispatch_group_create();
        dispatch_queue_t cola = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
        dispatch_group_async(grupo, cola, ^{
            for (NSUInteger i = 0; i < medio; i++) p1 += nums[i].longLongValue;
        });
        dispatch_group_async(grupo, cola, ^{
            for (NSUInteger i = medio; i < nums.count; i++) p2 += nums[i].longLongValue;
        });
        dispatch_group_wait(grupo, DISPATCH_TIME_FOREVER);

        printf("suma=%lld\n", p1 + p2);
    }
    return 0;
}
```

**Qué reconocer:** los dos comparten memoria de verdad y ninguno te protege de las carreras: aquí
funcionan porque cada tarea escribe en **su propia** variable. C++ envuelve el hilo en un
`std::future`, un valor que todavía no está: `get()` bloquea hasta que llegue. Objective-C no
gestiona hilos, sino **colas**: con Grand Central Dispatch tú encolas bloques y el sistema decide
cuántos hilos usar. `dispatch_group_wait` es el `join` de toda la vida, y ese `__block` no es
decorativo —sin él, el bloque capturaría una copia de solo lectura y los parciales se perderían—.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Goroutines y canales por
un lado; hilos con propiedad verificada por el compilador por el otro.

### Zig

```zig
const std = @import("std");

fn sumar(parte: []const i64, resultado: *i64) void {
    var s: i64 = 0;
    for (parte) |x| s += x;
    resultado.* = s;
}

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const leido = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, leido, " \r"), ' ');

    var nums: [64]i64 = undefined;
    var n: usize = 0;
    while (it.next()) |tok| : (n += 1) nums[n] = try std.fmt.parseInt(i64, tok, 10);

    const medio = n / 2;
    var p1: i64 = 0;
    var p2: i64 = 0;
    const h1 = try std.Thread.spawn(.{}, sumar, .{ nums[0..medio], &p1 });
    const h2 = try std.Thread.spawn(.{}, sumar, .{ nums[medio..n], &p2 });
    h1.join();
    h2.join();

    try std.io.getStdOut().writer().print("suma={d}\n", .{p1 + p2});
}
```

### Nim

```nim
# Compilar con --threads:on. spawn devuelve un FlowVar; el operador ^ espera su valor.
import std/[strutils, sequtils, threadpool]

proc sumar(parte: seq[int]): int =
  for x in parte: result += x

let nums = stdin.readLine().splitWhitespace().map(parseInt)
let medio = nums.len div 2

let p1 = spawn sumar(nums[0 ..< medio])
let p2 = spawn sumar(nums[medio ..< nums.len])

echo "suma=" & $(^p1 + ^p2)
```

### D

```d
import std.algorithm, std.array, std.conv, std.parallelism, std.stdio, std.string;

void main() {
    auto nums = readln().strip().split().map!(to!long).array;
    const medio = nums.length / 2;

    auto t1 = task!(a => a.sum)(nums[0 .. medio]);
    auto t2 = task!(a => a.sum)(nums[medio .. $]);
    t1.executeInNewThread();
    t2.executeInNewThread();

    writefln("suma=%d", t1.yieldForce + t2.yieldForce);
}
```

**Qué reconocer:** los tres lanzan hilos de sistema de verdad, y los tres eligen algo distinto de lo
que hace Go. Zig es el más crudo: `std.Thread.spawn` recibe la función y sus argumentos, y el
resultado sale por un puntero que tú preparas —ni canales, ni futuros, ni comprobación de que dos
hilos no escriban la misma dirección—. Nim se parece más a Rust en las garantías: por defecto cada
hilo tiene su propio montón, y `spawn` devuelve un `FlowVar` que hay que esperar con `^`; a cambio
te obliga a compilar con `--threads:on` y a que lo que cruce el límite sea seguro de mover. D ocupa
el punto medio con `std.parallelism`: `task` crea la unidad de trabajo y `yieldForce` la fuerza,
pero las variables globales son compartidas solo si las declaras `__gshared` —por defecto en D cada
hilo tiene **su copia**, al revés que en C++—.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se declara el resultado y el motor decide si lo
calcula en un hilo o en veinte: el paralelismo no está en el lenguaje.

### Prolog

```prolog
:- initialization(main, main).

sumar(Parte, Cola) :-
    sum_list(Parte, S),
    thread_send_message(Cola, S).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    length(Nums, Total),
    Medio is Total // 2,
    length(Izq, Medio),
    append(Izq, Der, Nums),
    message_queue_create(Cola),
    thread_create(sumar(Izq, Cola), H1, []),
    thread_create(sumar(Der, Cola), H2, []),
    thread_get_message(Cola, S1),
    thread_get_message(Cola, S2),
    thread_join(H1),
    thread_join(H2),
    Suma is S1 + S2,
    format("suma=~d~n", [Suma]).
```

### Datalog

```datalog
% Datalog no tiene hilos, ni orden de evaluación, ni forma de decir "reparte esto en
% dos". El motor puede evaluar las reglas en paralelo, pero eso es cosa suya. Tampoco
% hay agregación en el Datalog puro: la línea de abajo usa la extensión de los
% dialectos que sí la traen (Souffle y similares).
num(1).
num(2).
num(3).
num(4).

suma(S) :- S = sum X : { num(X) }.
```

**Qué reconocer:** Prolog rompe el molde de esta familia. SWI-Prolog tiene hilos POSIX de verdad y
**colas de mensajes**, y el código de arriba es casi el mismo esqueleto que el de Go: lanzar dos
trabajadores y leer dos resultados de un canal. Fíjate en que cada hilo lleva su propia base de datos
de variables, así que nada se comparte por accidente. Datalog es el extremo contrario y no hay que
disimularlo: sin efectos, sin estado y sin tiempo, "concurrente" no significa nada dentro del
lenguaje. Lo único que se declara es el total; que el motor lo calcule con un hilo o con dieciséis
es invisible desde el programa. Esa es exactamente la promesa —y la renuncia— de SQL.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la mayor dispersión de todo el curso: hilos con memoria
compartida (C++, Zig, JVM), hilos aislados (Tcl, Dart, Nim), procesos (Perl, R), actores (F#),
transacciones (Clojure), corrutinas de un solo hilo (Lua, Kotlin) y sencillamente nada
(ActionScript, Datalog). El programa se parece; **lo que garantiza no se parece en absoluto**. Eso
es lo transferible.

⏮️ [Volver a la clase 121](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
