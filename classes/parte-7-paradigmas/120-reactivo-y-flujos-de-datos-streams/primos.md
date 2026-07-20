# 🧬 El mismo programa en las familias de lenguajes — Clase 120

> [⬅️ Volver a la clase 120](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —tratar una lista como un flujo: filtrar los pares y
duplicarlos— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de JavaScript, la de Ruby te resultará familiar aunque no la hayas visto
nunca. Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio (hay al menos un par)
- **Salida** (stdout): `stream=<pares duplicados, unidos por ->`
- **Regla:** flujo `filtrar pares` → `map x → 2x`

| stdin | esperado |
|---|---|
| `1 2 3 4` | `stream=4-8` |
| `2 4` | `stream=4-8` |
| `6 7 8` | `stream=12-16` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La tubería `filtrar → transformar` existe en todos, pero solo algunos la hacen **perezosa**: es
decir, capaz de correr sobre un flujo infinito sin materializar la lista entera.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
stream = nums.lazy.select(&:even?).map { |x| x * 2 }
puts "stream=#{stream.to_a.join('-')}"
```

### Perl

```perl
my @nums = split ' ', do { local $/; <STDIN> };
my @stream = map { $_ * 2 } grep { $_ % 2 == 0 } @nums;
print "stream=", join('-', @stream), "\n";
```

### Lua

```lua
-- Lua no trae flujos ni map/filter: la corrutina hace de productor perezoso.
local function flujo(t)
  return coroutine.wrap(function()
    for _, x in ipairs(t) do
      if x % 2 == 0 then coroutine.yield(x * 2) end
    end
  end)
end

local nums = {}
for s in io.read("l"):gmatch("%S+") do
  nums[#nums + 1] = tonumber(s)
end

local salida = {}
for v in flujo(nums) do
  salida[#salida + 1] = v
end
print("stream=" .. table.concat(salida, "-"))
```

### Tcl

```tcl
gets stdin linea

set stream {}
foreach x [split $linea] {
    if {$x % 2 == 0} {
        lappend stream [expr {$x * 2}]
    }
}
puts "stream=[join $stream -]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " +")[[1]])
stream <- v[v %% 2 == 0] * 2
cat(paste0("stream=", paste(stream, collapse = "-"), "\n"))
```

**Qué reconocer:** Perl escribe la tubería **al revés** —`map` a la izquierda, `grep` a la derecha—
porque se lee de dentro hacia fuera, no de izquierda a derecha como el `.filter().map()` que ya
conoces. Ruby es el único de los cinco con pereza declarada: sin `.lazy`, `select` construye una
lista intermedia; con `.lazy`, cada elemento atraviesa toda la cadena antes de que empiece el
siguiente. Tcl no tiene ninguna de las dos cosas y vuelve al bucle explícito. R no necesita el flujo
porque **la operación ya es vectorial**: `v %% 2 == 0` produce un vector de verdaderos y falsos que
indexa el original, y multiplicar por 2 se aplica a todos los elementos a la vez.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Aquí es donde el reactivo dejó de ser una biblioteca y se volvió parte del lenguaje.

### Dart

```dart
import 'dart:io';

void main() async {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);

  final flujo = Stream.fromIterable(nums)
      .where((x) => x % 2 == 0)
      .map((x) => x * 2);

  final salida = await flujo.toList();
  print('stream=${salida.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene flujos ni stdin: lo más cercano son filter/map sobre Array,
// que son ansiosos y trabajan sobre datos ya completos en memoria.
package {
    public class Flujo {
        public static function procesar(nums:Array):String {
            var stream:Array = nums
                .filter(function (x:int, i:int, a:Array):Boolean { return x % 2 == 0; })
                .map(function (x:int, i:int, a:Array):int { return x * 2; });
            return "stream=" + stream.join("-");
        }
    }
}
```

**Qué reconocer:** Dart es el caso más limpio de toda esta página: `Stream` es un tipo **del núcleo
del lenguaje**, con `where` y `map` propios y con `await` integrado, de modo que una secuencia de
valores en el tiempo se trata igual que una lista. ActionScript enseña el punto de partida: sus
`filter` y `map` son los mismos de `Array` en JavaScript —ansiosos, sobre datos ya presentes— y para
lo asíncrono había que bajar a eventos. La distancia entre esos dos bloques es exactamente la que
recorrió la programación reactiva.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El `Stream` de Java 8 puso la tubería perezosa
en la biblioteca estándar; sus primos fueron más lejos, hasta el flujo asíncrono.

### Kotlin

```kotlin
import kotlinx.coroutines.flow.asFlow
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }

    val salida = nums.asFlow()
        .filter { it % 2 == 0 }
        .map { it * 2 }
        .toList()

    println("stream=" + salida.joinToString("-"))
}
```

### Scala

```scala
object Flujo extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val stream = LazyList.from(nums).filter(_ % 2 == 0).map(_ * 2)
  println(s"stream=${stream.mkString("-")}")
}
```

### Groovy

```groovy
def nums = System.in.text.trim().split(/\s+/)*.toInteger()
def stream = nums.findAll { it % 2 == 0 }.collect { it * 2 }
println "stream=${stream.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums   (map parse-long (str/split (str/trim (read-line)) #"\s+"))
      stream (sequence (comp (filter even?) (map #(* 2 %))) nums)]
  (println (str "stream=" (str/join "-" stream))))
```

**Qué reconocer:** los cuatro dicen lo mismo con cuatro vocabularios distintos, y ahí está el truco
de la familia. Groovy usa los nombres de Smalltalk (`findAll`, `collect`) y es **ansioso**: cada
paso construye una lista nueva. Scala usa `LazyList`, una secuencia perezosa que solo calcula lo que
alguien pide. Kotlin es el único con un flujo **asíncrono** —`Flow` vive en la biblioteca
`kotlinx.coroutines`, no en el núcleo, y por eso hace falta `runBlocking`—: sus operadores pueden
suspenderse esperando datos. Clojure separa la operación de la colección: `(comp (filter even?)
(map ...))` es un **transductor**, una tubería que no menciona sobre qué va a correr y sirve igual
para una secuencia, un canal o un flujo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). LINQ es la tubería perezosa del CLR, y todos los
lenguajes de la plataforma la comparten.

### F\#

```fsharp
open System

let nums =
    Console.ReadLine().Split(' ', StringSplitOptions.RemoveEmptyEntries)
    |> Seq.map int

let stream =
    nums
    |> Seq.filter (fun x -> x % 2 = 0)
    |> Seq.map (fun x -> x * 2)

printfn "stream=%s" (String.Join("-", stream))
```

### VB.NET

```vbnet
Imports System.Linq

Module Flujo
    Sub Main()
        Dim nums = Console.ReadLine().Trim() _
            .Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries) _
            .Select(Function(s) Integer.Parse(s))

        Dim stream = nums.Where(Function(x) x Mod 2 = 0).Select(Function(x) x * 2)

        Console.WriteLine("stream=" & String.Join("-", stream))
    End Sub
End Module
```

**Qué reconocer:** `Where`/`Select` de VB.NET y `Seq.filter`/`Seq.map` de F# son **la misma
`IEnumerable` perezosa** vista desde dos culturas: la de los métodos de extensión encadenados y la
de las funciones con `|>`. Ninguna de las dos calcula nada hasta que `String.Join` recorre el
resultado. .NET es también donde nació Rx (`IObservable`), el modelo reactivo que después copiaron
RxJava, RxJS y compañía: la idea de que un `IEnumerable` que empuja valores en vez de esperar a que
se los pidan es su dual exacto.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin tuberías en el lenguaje, el flujo es un bucle
con un `if` dentro… hasta C++20.

### C++

```cpp
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x;) nums.push_back(x);

    auto stream = nums
        | std::views::filter([](int x) { return x % 2 == 0; })
        | std::views::transform([](int x) { return x * 2; });

    std::cout << "stream=";
    bool primero = true;
    for (int v : stream) {
        if (!primero) std::cout << '-';
        std::cout << v;
        primero = false;
    }
    std::cout << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *entrada = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:entrada encoding:NSUTF8StringEncoding];

        NSMutableArray<NSNumber *> *stream = [NSMutableArray array];
        NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        for (NSString *s in [linea componentsSeparatedByCharactersInSet:espacios]) {
            if (s.length == 0) continue;
            NSInteger x = [s integerValue];
            if (x % 2 == 0) [stream addObject:@(x * 2)];
        }

        printf("stream=%s\n", [[stream componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** el `|` de C++20 no es el `or` a nivel de bits: los *ranges* redefinieron ese
operador para encadenar **vistas**, que no copian nada y solo calculan cuando el `for` avanza. Es
LINQ compilado a coste cero. Objective-C se quedó en la era anterior —`NSArray` no tiene `filter`
ni `map`, solo `filteredArrayUsingPredicate:` con `NSPredicate`— y por eso lo idiomático sigue
siendo el bucle con acumulador, que es literalmente la versión de C con objetos encima.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los iteradores de Rust
demostraron que la tubería perezosa puede compilar al mismo bucle que escribirías a mano.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const leido = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, leido, " \r"), ' ');

    // Zig no tiene filter/map en la biblioteca estándar: la tubería es el propio bucle.
    const out = std.io.getStdOut().writer();
    try out.writeAll("stream=");
    var primero = true;
    while (it.next()) |tok| {
        const x = try std.fmt.parseInt(i64, tok, 10);
        if (@rem(x, 2) != 0) continue;
        if (!primero) try out.writeAll("-");
        try out.print("{d}", .{x * 2});
        primero = false;
    }
    try out.writeAll("\n");
}
```

### Nim

```nim
import std/[strutils, sequtils]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
let stream = nums.filterIt(it mod 2 == 0).mapIt($(it * 2))
echo "stream=" & stream.join("-")
```

### D

```d
import std.algorithm, std.array, std.conv, std.stdio, std.string;

void main() {
    auto stream = readln().strip().split()
        .map!(to!int)
        .filter!(x => x % 2 == 0)
        .map!(x => to!string(x * 2));

    writefln("stream=%s", stream.join("-"));
}
```

**Qué reconocer:** D es el más cercano a Rust: sus `map!` y `filter!` son *ranges* perezosos, nada
se calcula hasta que `join` los recorre, y el compilador funde toda la cadena en un solo bucle. Nim
llega al mismo aspecto por otra vía —`filterIt`/`mapIt` son **macros** que reescriben la expresión
en tiempo de compilación, con `it` como variable implícita— pero son ansiosos: construyen un `seq`
intermedio. Zig es la excepción deliberada: su biblioteca estándar no ofrece `filter` ni `map`
porque el lenguaje evita las abstracciones que esconden asignaciones de memoria, así que el flujo se
escribe como lo que realmente es en la máquina, un bucle con `continue`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `WHERE` seguido de `SELECT` ya es una tubería
declarativa: se dice qué se quiere, no cómo recorrerlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    include([X]>>(0 is X mod 2), Nums, Pares),
    maplist([X, Y]>>(Y is X * 2), Pares, Dobles),
    maplist(number_string, Dobles, Textos),
    atomic_list_concat(Textos, '-', Salida),
    format("stream=~w~n", [Salida]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni flujos: no hay "primero filtra, luego transforma", porque
% no hay orden. Solo se declara qué relación deriva de cuál; el motor decide el resto.
num(1).
num(2).
num(3).
num(4).

par(X)   :- num(X), X mod 2 = 0.
doble(Y) :- par(X), Y = X * 2.
```

**Qué reconocer:** `include/3` y `maplist/3` son el `filter` y el `map` de Prolog, con una diferencia
de fondo: en vez de una función que devuelve un valor, reciben un **objetivo** que debe tener éxito
—`include` conserva los elementos para los que el objetivo es demostrable—. Datalog quita hasta eso:
`par` y `doble` son dos relaciones y la tubería es solo el hecho de que la segunda menciona a la
primera. No hay tiempo, no hay pereza, no hay orden de llegada. Es la misma renuncia de SQL, y por
eso la palabra *stream* no significa nada aquí: un flujo necesita un antes y un después.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una misma pregunta detrás: **cuándo se calcula cada elemento**.
Ansioso (Groovy, Nim), perezoso (Scala, D, ranges de C++), asíncrono (Dart, Flow de Kotlin) o sin
tiempo en absoluto (Datalog). El código se parece; las garantías no. Eso es lo transferible.

⏮️ [Volver a la clase 120](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
