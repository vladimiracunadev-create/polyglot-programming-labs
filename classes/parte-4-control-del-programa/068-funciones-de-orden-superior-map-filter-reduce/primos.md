# 🧬 El mismo programa en las familias de lenguajes — Clase 068

> [⬅️ Volver a la clase 068](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —duplicar cada número (`map`) y sumar los resultados
(`reduce`)— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

`map` y `reduce` son de los pocos nombres que viajan casi intactos entre familias. Casi: verás
`collect`, `inject`, `Select`, `Aggregate`, `lmap`, `maplist` y `foldl` diciendo exactamente lo
mismo, y algún lenguaje al que le falta la mitad del par.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por -> total=<suma de los doblados>`
- **Regla:** `doblados = map(x→2x)` ; `total = reduce(+, doblados)`

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6 total=12` |
| `5` | `doblados=10 total=10` |
| `2 4` | `doblados=4-8 total=12` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos tratan las funciones como valores, así que se pueden pasar como argumento. Lo que cambia es
si el lenguaje trae `reduce` de serie o hay que ir a buscarlo.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
doblados = nums.map { |x| x * 2 }
total = doblados.reduce(0, :+)
puts "doblados=#{doblados.join('-')} total=#{total}"
```

### Perl

```perl
use List::Util qw(reduce);

my @nums = split ' ', <STDIN>;
my @doblados = map { $_ * 2 } @nums;
my $total = reduce { $a + $b } 0, @doblados;

print "doblados=", join('-', @doblados), " total=$total\n";
```

### Lua

```lua
-- Lua no trae map ni reduce: el bucle que hace ambas cosas es lo idiomático.
local doblados, total = {}, 0
for palabra in io.read("l"):gmatch("%S+") do
  local d = tonumber(palabra) * 2
  doblados[#doblados + 1] = d
  total = total + d
end
print(string.format("doblados=%s total=%d", table.concat(doblados, "-"), total))
```

### Tcl

```tcl
gets stdin linea
set doblados [lmap n [split $linea] {expr {$n * 2}}]
set total [::tcl::mathop::+ {*}$doblados]
puts "doblados=[join $doblados -] total=$total"
```

### R

```r
nums <- scan("stdin", what = integer(), quiet = TRUE)
doblados <- nums * 2L
total <- Reduce(`+`, doblados)
cat(sprintf("doblados=%s total=%d\n", paste(doblados, collapse = "-"), total))
```

**Qué reconocer:** Ruby escribe `reduce(0, :+)` pasando el **símbolo** del operador, porque en Ruby
`+` es un método y su nombre es un valor. Perl tiene `map` en el núcleo del lenguaje pero `reduce`
en un módulo, y usa las variables mágicas `$a` y `$b` en vez de parámetros con nombre. Tcl consigue
el `reduce` con `{*}`, que **expande la lista en argumentos** del comando `+`: no es un pliegue, es
una llamada variádica —y por eso funciona igual con uno o con veinte elementos—. R no necesita
`map` en absoluto: `nums * 2L` multiplica el vector entero, y aunque `Reduce` existe, un usuario de
R escribiría `sum(doblados)`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  final doblados = nums.map((x) => x * 2).toList();
  final total = doblados.fold<int>(0, (a, b) => a + b);
  print('doblados=${doblados.join('-')} total=$total');
}
```

### ActionScript 3

```actionscript
// AS3 tiene map y filter en Array, pero NO reduce, y no tiene stdin.
package {
    public class Doblar {
        public static function procesar(nums:Array):String {
            var doblados:Array = nums.map(function (x:int, i:int, a:Array):int {
                return x * 2;
            });
            var total:int = 0;
            for each (var d:int in doblados) {
                total += d;
            }
            return "doblados=" + doblados.join("-") + " total=" + total;
        }
    }
}
```

**Qué reconocer:** Dart llama `fold` a lo que JavaScript llama `reduce`, y exige el valor inicial —
por eso nunca falla con la lista vacía, mientras que el `reduce` de JavaScript sin valor inicial sí
lanza excepción—. ActionScript 3 es el ejemplo de familia incompleta: heredó `map`, `filter`,
`forEach`, `every` y `some` de ECMAScript 4, pero **`reduce` llegó después** y nunca lo tuvo. El
pliegue hay que escribirlo con un bucle, que es la prueba de que `reduce` no es magia: es un
acumulador con otro nombre.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Las tres operaciones existen en la JVM desde
que llegaron los streams; los primos las tienen sobre las colecciones directamente.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val doblados = nums.map { it * 2 }
    val total = doblados.reduce { a, b -> a + b }
    println("doblados=${doblados.joinToString("-")} total=$total")
}
```

### Scala

```scala
object Doblar extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val doblados = nums.map(_ * 2)
  val total = doblados.foldLeft(0)(_ + _)
  println(s"doblados=${doblados.mkString("-")} total=$total")
}
```

### Groovy

```groovy
def nums = System.in.text.trim().split(/\s+/)*.toInteger()
def doblados = nums.collect { it * 2 }
def total = doblados.inject(0) { a, b -> a + b }
println "doblados=${doblados.join('-')} total=$total"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums     (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))
      doblados (map #(* 2 %) nums)
      total    (reduce + doblados)]
  (println (str "doblados=" (str/join "-" doblados) " total=" total)))
```

**Qué reconocer:** Groovy conserva los nombres viejos de Smalltalk —`collect` para map, `inject`
para reduce— que Ruby también heredó; son la misma operación con la genealogía a la vista. Kotlin
distingue `reduce` (empieza con el primer elemento, falla si la lista está vacía) de `fold` (empieza
con un valor inicial), y Scala añade la dirección: `foldLeft` frente a `foldRight`. Clojure es el
más limpio de los cuatro porque `+` ya es una función de verdad y se pasa tal cual, sin envolverla
en una lambda; además su `map` es perezoso, así que `doblados` no existe como lista hasta que se
imprime.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). LINQ trae las tres, con nombres de base de datos:
`Select` es map, `Where` es filter, `Aggregate` es reduce.

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int

let doblados = nums |> Array.map (fun x -> x * 2)
let total = doblados |> Array.fold (+) 0

printfn "doblados=%s total=%d" (doblados |> Array.map string |> String.concat "-") total
```

### VB.NET

```vbnet
Imports System
Imports System.Linq

Module Doblar
    Sub Main()
        Dim nums = Console.ReadLine().
            Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries).
            Select(Function(s) Integer.Parse(s))

        Dim doblados = nums.Select(Function(x) x * 2).ToList()
        Dim total = doblados.Aggregate(0, Function(a, b) a + b)

        Console.WriteLine("doblados=" & String.Join("-", doblados) & " total=" & total)
    End Sub
End Module
```

**Qué reconocer:** `Select` y `Aggregate` son `map` y `reduce` con el vocabulario de SQL, porque LINQ
se diseñó para que la misma expresión pudiera ejecutarse en memoria o traducirse a una consulta
contra una base de datos. F# enseña el fondo del asunto: `Array.fold (+) 0` pasa el operador `+` sin
envolverlo en ninguna lambda, algo que ni C# ni VB.NET pueden hacer porque allí los operadores no
son valores de primera clase. Los tres corren sobre el mismo CLR; la diferencia es cuánta ceremonia
cuesta nombrar una función.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Se puede pasar un puntero a función, pero no hay
lambdas ni capturas: el bucle explícito gana casi siempre.

### C++

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x; ) nums.push_back(x);

    std::vector<int> doblados(nums.size());
    std::transform(nums.begin(), nums.end(), doblados.begin(), [](int x) { return x * 2; });
    const int total = std::accumulate(doblados.begin(), doblados.end(), 0);

    std::string salida;
    for (int d : doblados) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(d);
    }

    std::cout << "doblados=" << salida << " total=" << total << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *entrada = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile]
                encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *partes =
            [[entrada stringByTrimmingCharactersInSet:blancos] componentsSeparatedByString:@" "];

        // Foundation no tiene map ni reduce sobre NSArray: se recorre y se acumula.
        NSMutableArray<NSString *> *doblados = [NSMutableArray array];
        NSInteger total = 0;
        for (NSString *p in partes) {
            NSInteger d = [p integerValue] * 2;
            total += d;
            [doblados addObject:[NSString stringWithFormat:@"%ld", (long)d]];
        }

        printf("doblados=%s total=%ld\n",
               [[doblados componentsJoinedByString:@"-"] UTF8String], (long)total);
    }
    return 0;
}
```

**Qué reconocer:** C++ tiene las tres operaciones desde 1998, pero con nombres que despistan:
`transform` es `map` y `accumulate` es `reduce`, y ambas se piden con **pares de iteradores** en
lugar de con la colección. La lambda `[](int x) { ... }` es lo que faltaba en C y lo que hace usable
toda la biblioteca de algoritmos. Objective-C no trae `map` ni `reduce` en `NSArray`; lo más cercano
son los operadores de KVC (`[array valueForKeyPath:@"@sum.self"]`), que resuelven la suma pero no el
caso general, así que el bucle con acumulador sigue siendo lo idiomático.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust encadena
`map`/`fold` y el compilador los funde en un solo bucle; Go, hasta hace poco, no tenía ni genéricos
para escribirlos.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [512]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");

    const out = std.io.getStdOut().writer();
    var total: i64 = 0;
    var primero = true;
    try out.writeAll("doblados=");

    // Sin closures en la stdlib: map y reduce ocurren en el mismo bucle.
    while (it.next()) |tok| {
        const d = (try std.fmt.parseInt(i64, tok, 10)) * 2;
        total += d;
        if (!primero) try out.writeByte('-');
        primero = false;
        try out.print("{d}", .{d});
    }

    try out.print(" total={d}\n", .{total});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
let doblados = nums.mapIt(it * 2)
let total = doblados.foldl(a + b, 0)

echo "doblados=", doblados.join("-"), " total=", total
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv, std.string;

void main() {
    auto nums = readln().split().map!(to!int);
    auto doblados = nums.map!(x => x * 2).array;
    const total = doblados.fold!((a, b) => a + b)(0);

    writeln("doblados=", doblados.map!(to!string).join("-"), " total=", total);
}
```

**Qué reconocer:** Nim y D tienen el trío completo con nombres reconocibles —`mapIt`/`foldl`,
`map!`/`fold!`— y ambos son **plantillas o macros**, no llamadas a función: el compilador las
expande en el bucle que escribirías a mano, así que la abstracción sale gratis. Zig es la excepción
declarada: sin clausuras en la biblioteca estándar, `map` y `reduce` no existen, y el resultado es
que ambas fases se funden en un único recorrido. Curiosamente, eso es lo mismo que hace el
compilador de Rust con `.map().sum()`; la diferencia es quién escribe la fusión.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `SELECT x*2` es el map y `SUM(...)` el reduce:
SQL lleva décadas haciendo esto sin llamarlo así.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    maplist([X, D]>>(D is X * 2), Nums, Doblados),
    foldl([X, A0, A]>>(A is A0 + X), Doblados, 0, Total),
    atomic_list_concat(Doblados, '-', Salida),
    format("doblados=~w total=~d~n", [Salida, Total]).
```

### Datalog

```datalog
% Datalog no tiene funciones de orden superior: el `map` es una regla y el `reduce`
% un agregado del motor (sintaxis de Soufflé; Datalog puro no tiene ninguno de los dos).
num(1, 1).
num(2, 2).
num(3, 3).

doblado(I, D) :- num(I, X), D = X * 2.
total(T) :- T = sum D : { doblado(_, D) }.
```

**Qué reconocer:** `maplist` y `foldl` de Prolog son `map` y `reduce` con otro nombre, pero con una
diferencia de fondo: al no haber valores de retorno, la función se escribe como una **relación** con
un argumento de entrada y otro de salida (`[X, D]>>(D is X * 2)`). Datalog no admite funciones como
argumento en absoluto: el map se convierte en una regla que define una nueva relación derivada, y el
reduce solo existe si el motor añade agregados. Es la misma jerarquía de renuncias que hace SQL: no
le pasas una función, le describes el resultado.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y un par de operaciones que resultan ser universales: transformar
cada elemento y plegar la colección en un valor. Los nombres cambian (`collect`, `inject`, `Select`,
`Aggregate`, `maplist`, `foldl`), algún lenguaje se deja media pareja fuera y otros los expanden en
tiempo de compilación para que no cuesten nada. Pero en cuanto reconoces la forma —una función que
recibe otra función— el resto es vocabulario. Eso es lo transferible.

⏮️ [Volver a la clase 068](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
