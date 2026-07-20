# 🧬 El mismo programa en las familias de lenguajes — Clase 114

> [⬅️ Volver a la clase 114](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —doblar cada elemento de una lista sin mutar la
original— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

El código de casi todos se parecerá: leer, `map`, unir con guiones. Lo que cambia es **quién
garantiza que la lista original no se tocó**. En la mayoría es una disciplina del programador; en
Clojure y F# es el estado natural del lenguaje; y en Prolog ni siquiera existe la operación de
modificar algo, así que la pureza no se impone, se hereda.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por guiones>`
- **Regla:** `doblados = map(x → 2x, lista)`, sin modificar la lista de entrada

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6` |
| `5` | `doblados=10` |
| `2 4` | `doblados=4-8` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos tienen `map` y todos permiten mutar la lista original: la pureza es una elección de estilo, no
una propiedad del lenguaje.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i).freeze
doblados = nums.map { |x| x * 2 }
puts "doblados=#{doblados.join('-')}"
```

### Perl

```perl
use strict;
use warnings;

my @nums = split ' ', do { local $/; <STDIN> };
my @doblados = map { $_ * 2 } @nums;   # map devuelve una lista nueva
print "doblados=", join('-', @doblados), "\n";
```

### Lua

```lua
-- Lua no trae `map` en la biblioteca estándar: la función pura se escribe a
-- mano y devuelve una tabla nueva en vez de recorrer la original mutándola.
local function map(t, f)
  local r = {}
  for i, v in ipairs(t) do
    r[i] = f(v)
  end
  return r
end

local nums = {}
for p in io.read("a"):gmatch("%-?%d+") do
  nums[#nums + 1] = tonumber(p)
end

local doblados = map(nums, function(x)
  return x * 2
end)
print("doblados=" .. table.concat(doblados, "-"))
```

### Tcl

```tcl
# Tcl pasa los valores por copia: `doblar` no puede modificar la lista del
# llamante aunque lo intente.
proc doblar {lista} {
    set r {}
    foreach x $lista { lappend r [expr {$x * 2}] }
    return $r
}

set nums [string trim [read stdin]]
puts "doblados=[join [doblar $nums] -]"
```

### R

```r
nums <- scan("stdin", quiet = TRUE)
doblados <- nums * 2   # copia al modificar: `nums` queda intacto
cat("doblados=", paste(as.integer(doblados), collapse = "-"), "\n", sep = "")
```

**Qué reconocer:** los cinco producen una colección nueva, pero solo dos lo **garantizan**. Ruby
ofrece `freeze` —una decisión opcional y superficial: congela la lista, no los objetos de dentro—.
Perl es el caso peligroso de la tanda: dentro de `map { ... }`, la variable `$_` es un **alias** al
elemento original, así que escribir `$_ *= 2` mutaría `@nums` sin avisar; la pureza depende por
completo de que el cuerpo se limite a devolver un valor. Tcl y R sí garantizan: Tcl copia al pasar
valores entre procedimientos y R copia al modificar, de modo que la mutación accidental a distancia
es imposible por construcción. R además muestra otra cosa: `nums * 2` no necesita `map` porque el
lenguaje es **vectorizado**, y la operación sobre el vector entero es su forma natural de escribir la
función pura.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = List<int>.unmodifiable(
      stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse));
  final doblados = nums.map((x) => x * 2);
  print('doblados=${doblados.join('-')}');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene stdin ni colecciones inmutables. `Array.map` sí devuelve un
// array nuevo, exactamente el mismo método que JavaScript.
package {
    public class Doblar {
        public static function doblados(nums:Array):String {
            var r:Array = nums.map(function(x:int, i:int, a:Array):int {
                return x * 2;
            });
            return "doblados=" + r.join("-");
        }
    }
}
```

**Qué reconocer:** el `map` de los dos es el mismo `Array.prototype.map` que ya conoces —devuelve una
colección nueva y deja la de entrada quieta— pero solo Dart puede impedir la mutación. `List` en Dart
es mutable por defecto; `List.unmodifiable` construye una que **lanza en ejecución** si intentas
escribirla, que es el mismo nivel de garantía que `Object.freeze` en JavaScript: real, pero tardío.
ActionScript 3 no tiene ni eso. Compáralo con `readonly` de TypeScript, que es lo contrario: impide
la escritura al **compilar** y desaparece al ejecutar.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java partió de colecciones mutables y añadió
las inmutables después; en esta familia conviven las dos herencias.

### Kotlin

```kotlin
fun main() {
    val nums: List<Int> = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val doblados = nums.map { it * 2 }
    println("doblados=${doblados.joinToString("-")}")
}
```

### Scala

```scala
object Doblar extends App {
  val nums: List[Int] = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).toList
  val doblados = nums.map(_ * 2)
  println(s"doblados=${doblados.mkString("-")}")
}
```

### Groovy

```groovy
def nums = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger().asImmutable()
def doblados = nums.collect { it * 2 }
println "doblados=${doblados.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))
      doblados (map #(* 2 %) nums)]
  (println (str "doblados=" (str/join "-" doblados))))
```

**Qué reconocer:** la misma máquina virtual, cuatro grados de compromiso distintos. Kotlin distingue
`val` de `var` —el enlace no se reasigna— y usa `List`, pero cuidado: `List` de Kotlin es una
interfaz de **solo lectura**, no inmutable; la colección de debajo puede seguir mutando por otra
referencia. Scala sí es serio: `scala.List` es inmutable de verdad y es el tipo por defecto, hay que
pedir `mutable.ListBuffer` a propósito. Groovy pide `asImmutable()` explícitamente. **Clojure es el
que cambia el punto de partida**: todas sus estructuras son inmutables y persistentes, `assoc`
devuelve una versión nueva compartiendo la mayor parte de la memoria, y no existe la operación de
mutar el vector —así que la función pura no es disciplina, es lo único disponible—.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let nums =
    stdin.ReadLine().Trim().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
    |> List.ofArray

let doblados = nums |> List.map (fun x -> x * 2)

printfn "doblados=%s" (doblados |> List.map string |> String.concat "-")
```

### VB.NET

```vbnet
Imports System.Linq

Module Programa
    Sub Main()
        Dim nums = Console.ReadLine().Trim().
            Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries).
            Select(Function(s) Integer.Parse(s))
        Dim doblados = nums.Select(Function(x) x * 2)
        Console.WriteLine("doblados=" & String.Join("-", doblados))
    End Sub
End Module
```

**Qué reconocer:** los dos usan la misma maquinaria —LINQ y `IEnumerable` sobre el CLR— con
posiciones de partida opuestas. En VB.NET, `Dim` crea una variable reasignable y las colecciones son
mutables: `Select` respeta el original por convenio de LINQ, no porque el lenguaje lo impida.
**F# invierte todos los valores por defecto**: `let` liga y no reasigna (para reasignar hace falta
`mutable` explícito), `List` es una lista enlazada inmutable, y una función sin efectos es lo que
sale si no haces nada especial. Es el mismo runtime, la misma biblioteca, y sin embargo escribir un
programa impuro en F# cuesta más trabajo que escribirlo puro —exactamente al revés que en VB.NET—.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C todo es memoria escribible y el compilador solo
puede avisar con `const`; la inmutabilidad es una promesa, no un muro.

### C++

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

int main() {
    const std::vector<int> nums{std::istream_iterator<int>(std::cin),
                                std::istream_iterator<int>()};
    std::vector<int> doblados(nums.size());
    std::transform(nums.begin(), nums.end(), doblados.begin(),
                   [](int x) { return x * 2; });

    std::ostringstream out;
    for (std::size_t i = 0; i < doblados.size(); ++i) {
        if (i) out << '-';
        out << doblados[i];
    }
    std::cout << "doblados=" << out.str() << '\n';
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
        // NSArray es inmutable por tipo; NSMutableArray es la variante que muta.
        NSArray<NSString *> *partes = [[entrada stringByTrimmingCharactersInSet:
            [NSCharacterSet whitespaceAndNewlineCharacterSet]]
            componentsSeparatedByString:@" "];
        NSMutableArray<NSString *> *doblados = [NSMutableArray array];
        for (NSString *p in partes) {
            [doblados addObject:[NSString stringWithFormat:@"%d", [p intValue] * 2]];
        }
        printf("doblados=%s\n", [[doblados componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** los dos declaran la inmutabilidad **en el tipo**, y en los dos es una garantía a
medias. El `const std::vector<int>` de C++ impide escribir a través de ese nombre, pero es una
propiedad de la referencia, no del objeto: otro puntero no `const` al mismo dato lo modificaría sin
que el compilador dijera nada, y un `const_cast` derriba el muro en una línea. Objective-C lo hace
con **dos clases distintas**: `NSArray` no tiene métodos de escritura y `NSMutableArray` sí, de modo
que la inmutabilidad viaja en la interfaz del objeto y no en cómo lo mires. Compáralo con Rust, donde
`&` y `&mut` hacen esa distinción a nivel de tipo *y* el compilador impide que coexistan.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí la inmutabilidad no
es estética: determina si el compilador puede razonar sobre concurrencia y sobre alias.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const entrada = try std.io.getStdIn().reader().readAllAlloc(alloc, 4096);
    defer alloc.free(entrada);

    var salida = std.ArrayList(u8).init(alloc);
    defer salida.deinit();

    var it = std.mem.tokenizeAny(u8, entrada, " \r\n\t");
    var primero = true;
    while (it.next()) |tok| {
        const n = try std.fmt.parseInt(i64, tok, 10);
        if (!primero) try salida.append('-');
        primero = false;
        try salida.writer().print("{d}", .{n * 2});
    }
    try std.io.getStdOut().writer().print("doblados={s}\n", .{salida.items});
}
```

### Nim

```nim
import std/[strutils, sequtils]

# `let` liga una sola vez; para reasignar habría que escribir `var`.
let nums = stdin.readAll().splitWhitespace().map(parseInt)
let doblados = nums.mapIt(it * 2)   # mapIt devuelve una secuencia nueva
echo "doblados=", doblados.mapIt($it).join("-")
```

### D

```d
import std.stdio, std.string, std.array, std.conv, std.algorithm;

void main() {
    immutable nums = readln().strip().split().map!(to!int).array.idup;
    auto doblados = nums.map!(x => x * 2);
    writeln("doblados=", doblados.map!(to!string).join("-"));
}
```

**Qué reconocer:** tres niveles de garantía muy distintos. Zig es el más honesto sobre el coste: la
lista de salida se construye con un asignador explícito y `const` en Zig solo dice que **ese
nombre** no se reasigna. Nim distingue `let` de `var` igual que Kotlin, y `func` promete además que
la función no tiene efectos secundarios —el compilador lo comprueba—. D es el más fuerte de la
familia y quizá de toda la página: `immutable` es **transitivo y profundo**, se propaga a todo lo
alcanzable desde ese valor, y el compilador puede por ello compartir el dato entre hilos sin
sincronización. Esa es la razón real por la que estos lenguajes se preocupan por la inmutabilidad: no
es elegancia, es lo que hace seguro compartir memoria.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una consulta no modifica las filas que lee:
declara qué resultado quiere y produce una relación nueva.

### Prolog

```prolog
:- initialization(main, main).

% `maplist` es el `map` de Prolog. No hay asignación: cada variable se liga una
% sola vez, así que `Nums` no puede cambiar mientras se construye `Doblados`.
doblar(X, Y) :- Y is X * 2.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    maplist(doblar, Nums, Doblados),
    maplist([N, S]>>number_string(N, S), Doblados, Textos),
    atomic_list_concat(Textos, '-', Salida),
    format("doblados=~w~n", [Salida]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni listas: los elementos se declaran como hechos con su
% posición, y la "función pura" es una regla que deriva un predicado nuevo sin
% borrar ni modificar ninguno de los hechos de partida.
num(1, 1).
num(2, 2).
num(3, 3).

doblado(I, D) :- num(I, V), D = V * 2.
```

**Qué reconocer:** este es el cierre de la clase y su mejor argumento. En Prolog no existe la
asignación: `Y is X * 2` **liga** `Y` con el resultado, y una vez ligada no se puede volver a ligar a
otra cosa dentro de la misma solución —no hay disciplina que mantener, porque la operación de mutar
sencillamente no está en el lenguaje—. Datalog lleva la misma idea al conjunto entero de datos: una
regla **añade** hechos derivados, jamás retira ni cambia los que ya estaban, y por eso el resultado
no depende del orden en que se evalúen las reglas. Eso último es exactamente lo que se gana con las
funciones puras en cualquier lenguaje —poder razonar sobre el resultado sin seguir el orden de
ejecución—, solo que aquí viene de fábrica y no se puede renunciar a ello.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y casi el mismo código: leer, `map`, unir. Lo que no se ve en el
código es lo que importa — quién **impide** la mutación. En Ruby o Perl no la impide nadie; en Dart
falla al ejecutar; en TypeScript, al compilar; en D es transitiva y profunda; en Clojure y F# la
mutación es lo que hay que pedir a propósito; y en Prolog y Datalog ni siquiera existe la palabra
para pedirla. Reconocer en qué punto de esa escala está un lenguaje nuevo te dice cuánto puedes
confiar en su `map`.

⏮️ [Volver a la clase 114](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
