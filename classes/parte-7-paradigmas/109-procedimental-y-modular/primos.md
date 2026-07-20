# 🧬 El mismo programa en las familias de lenguajes — Clase 109

> [⬅️ Volver a la clase 109](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el promedio entero de una lista, calculado por un
procedimiento reutilizable— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El salto de esta clase es doble: dar nombre a un trozo de cálculo (**procedimiento**) y agrupar esos
nombres en una unidad con frontera (**módulo**). Lo primero lo tienen todos; lo segundo lo resuelve
cada familia con una construcción distinta, y ahí es donde se les ve el paradigma de origen.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `promedio=<suma dividida entre la cantidad, entera>`
- **Regla:** `promedio = suma / cantidad`, con **división entera**

| stdin | esperado |
|---|---|
| `2 4 6` | `promedio=4` |
| `10` | `promedio=10` |
| `3 5` | `promedio=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Definir una función es trivial en los cinco; lo que cambia es qué llaman "módulo".

### Ruby

```ruby
module Estadistica
  def self.promedio(nums)
    nums.sum / nums.size
  end
end

nums = STDIN.gets.split.map(&:to_i)
puts "promedio=#{Estadistica.promedio(nums)}"
```

### Perl

```perl
use strict;
use warnings;

sub promedio {
    my @nums = @_;
    my $suma = 0;
    $suma += $_ for @nums;
    return int($suma / scalar @nums);
}

my @nums = split ' ', <STDIN>;
printf "promedio=%d\n", promedio(@nums);
```

### Lua

```lua
local estadistica = {}

function estadistica.promedio(nums)
  local suma = 0
  for _, x in ipairs(nums) do
    suma = suma + x
  end
  return suma // #nums
end

local nums = {}
for t in io.read("l"):gmatch("%S+") do
  nums[#nums + 1] = tonumber(t)
end
print("promedio=" .. estadistica.promedio(nums))
```

### Tcl

```tcl
namespace eval estadistica {
    proc promedio {nums} {
        set suma 0
        foreach x $nums { incr suma $x }
        return [expr {$suma / [llength $nums]}]
    }
}

gets stdin linea
puts "promedio=[estadistica::promedio [split [string trim $linea]]]"
```

### R

```r
promedio <- function(nums) sum(nums) %/% length(nums)

nums <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("promedio=%d\n", promedio(nums)))
```

**Qué reconocer:** las cinco funciones se parecen; los cinco **módulos** no. Ruby tiene una palabra
reservada, `module`, y el procedimiento hay que declararlo `self.` para que pertenezca al módulo y no
a quien lo incluya. Tcl usa `namespace eval` y separa con `::`, la misma marca que verás en C++.
Perl declara `sub` sin envoltorio: su unidad de módulo es el **paquete**, y en un archivo suelto no
hace falta. Lua es el caso revelador: **no tiene módulos como construcción del lenguaje**; un módulo
es una tabla a la que se le cuelgan funciones, exactamente el mismo truco con el que construirá las
clases dos clases más adelante. R ni siquiera lo intenta: su unidad de agrupación es el *package*
completo, no algo que quepa en un archivo. Y fíjate en la división entera, que cada uno escribe a su
manera: `/` entre enteros en Ruby, `int()` en Perl, `//` en Lua, `%/%` en R.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int promedio(List<int> nums) => nums.reduce((a, b) => a + b) ~/ nums.length;

void main() {
  final nums =
      stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('promedio=${promedio(nums)}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la lista llega como argumento.
// ActionScript 3 no tiene funciones sueltas: el procedimiento vive en una clase.
package estadistica {
    public class Promedio {
        public static function de(nums:Array):int {
            var suma:int = 0;
            for (var i:int = 0; i < nums.length; i++) {
                suma += int(nums[i]);
            }
            return int(suma / nums.length);
        }
    }
}
```

**Qué reconocer:** Dart declara `promedio` en el nivel superior del archivo, y el **archivo mismo** es
el módulo: quien quiera usarlo hace `import`. ActionScript 3 no permite eso; obliga a un `package` y
a una clase que actúa de contenedor, aunque el procedimiento no tenga estado ninguno. Ese patrón
—clases usadas como bolsas de funciones estáticas— es el precio de un lenguaje donde el módulo y la
clase son la misma cosa. Dart además tiene operador propio de división entera, `~/`, en vez de
truncar a mano.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En Java todo procedimiento es un método de una
clase; sus primos se separaron justo en ese punto.

### Kotlin

```kotlin
// Kotlin admite funciones de nivel superior: el archivo es el módulo.
fun promedio(nums: List<Int>): Int = nums.sum() / nums.size

fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("promedio=${promedio(nums)}")
}
```

### Scala

```scala
object Estadistica {
  def promedio(nums: Seq[Int]): Int = nums.sum / nums.size
}

object Main extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).toSeq
  println(s"promedio=${Estadistica.promedio(nums)}")
}
```

### Groovy

```groovy
def promedio(List<Integer> nums) {
    nums.sum().intdiv(nums.size())
}

def nums = System.in.newReader().readLine().trim().split(/\s+/).collect { it as int }
println "promedio=${promedio(nums)}"
```

### Clojure

```clojure
(ns estadistica
  (:require [clojure.string :as str]))

(defn promedio [nums]
  (quot (reduce + nums) (count nums)))

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "promedio=" (promedio nums))))
```

**Qué reconocer:** los cuatro acaban generando una clase en el bytecode —la JVM no sabe hacer otra
cosa— pero ninguno se lo hace escribir al programador. Kotlin y Groovy declaran la función en el
archivo; Clojure declara un **namespace** con `ns`, que es un módulo de verdad, con su propio mapa de
símbolos y sus `require` explícitos. Scala usa `object`, que es a la vez módulo y singleton: la misma
palabra sirve para las dos cosas, y esa fusión es su manera deliberada de mezclar objetos y
funciones. La división entera también delata la tradición: `/` sobre `Int` en Kotlin y Scala,
`intdiv` en Groovy —donde `/` daría un `BigDecimal`— y `quot` en Clojure, que separa por nombre lo
que otros distinguen por tipo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
module Estadistica =
    let promedio (nums: int list) = List.sum nums / List.length nums

let nums = stdin.ReadLine().Trim().Split(' ') |> Array.map int |> List.ofArray
printfn "promedio=%d" (Estadistica.promedio nums)
```

### VB.NET

```vbnet
Module Estadistica
    Function Promedio(nums As Integer()) As Integer
        Dim suma = 0
        For Each x In nums
            suma += x
        Next
        Return suma \ nums.Length
    End Function

    Sub Main()
        Dim nums = Array.ConvertAll(Console.ReadLine().Trim().Split(" "c), AddressOf Integer.Parse)
        Console.WriteLine("promedio=" & Promedio(nums))
    End Sub
End Module
```

**Qué reconocer:** los dos tienen la palabra `module` y significan casi lo mismo: un contenedor de
procedimientos sin instancias, que el compilador convierte en una clase estática del CLR. La
diferencia está dentro. VB.NET escribe el procedimiento como una receta con acumulador y tiene un
operador dedicado a la división entera, `\`, distinto del `/` decimal. F# lo escribe como composición
de dos funciones de biblioteca sobre una lista inmutable. Es la misma frontera de siempre en esta
plataforma: describir los pasos o describir el resultado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La función es la unidad de reutilización desde 1972;
el módulo llegó mucho después.

### C++

```cpp
#include <iostream>
#include <numeric>
#include <vector>

namespace estadistica {

long long promedio(const std::vector<long long>& nums) {
    return std::accumulate(nums.begin(), nums.end(), 0LL) /
           static_cast<long long>(nums.size());
}

}  // namespace estadistica

int main() {
    std::vector<long long> nums;
    for (long long x; std::cin >> x;) nums.push_back(x);
    std::cout << "promedio=" << estadistica::promedio(nums) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Objective-C hereda las funciones de C, pero su unidad de agrupación idiomática
// es una clase con métodos de clase.
@interface Estadistica : NSObject
+ (long)promedio:(NSArray<NSNumber *> *)nums;
@end

@implementation Estadistica
+ (long)promedio:(NSArray<NSNumber *> *)nums {
    long suma = 0;
    for (NSNumber *x in nums) suma += x.longValue;
    return suma / (long)nums.count;
}
@end

int main(void) {
    @autoreleasepool {
        NSMutableArray<NSNumber *> *nums = [NSMutableArray array];
        long x = 0;
        while (scanf("%ld", &x) == 1) [nums addObject:@(x)];
        printf("promedio=%ld\n", [Estadistica promedio:nums]);
    }
    return 0;
}
```

**Qué reconocer:** C resuelve la modularidad **fuera del lenguaje**, con archivos `.h` y `.c` y la
convención de prefijar los nombres. C++ añadió `namespace` justo para eso, y por eso su `::` se
parece tanto al de Tcl. Objective-C tomó el otro camino: como es Smalltalk montado sobre C, su
agrupación natural es una clase, y `+ (long)promedio:` es un **método de clase** invocado con
`[Estadistica promedio:nums]`. Los corchetes no son azúcar de llamada a función: son envío de un
mensaje a un objeto, y ese objeto aquí es la clase misma. Prefijos globales, espacios de nombres o
clases: tres respuestas a la misma pregunta de la clase.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Modularidad decidida en
el diseño del lenguaje, no por convención.

### Zig

```zig
const std = @import("std");

fn promedio(nums: []const i64) i64 {
    var suma: i64 = 0;
    for (nums) |x| suma += x;
    return @divTrunc(suma, @as(i64, @intCast(nums.len)));
}

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var nums: [64]i64 = undefined;
    var n: usize = 0;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    while (it.next()) |t| : (n += 1) {
        nums[n] = try std.fmt.parseInt(i64, t, 10);
    }
    try std.io.getStdOut().writer().print("promedio={d}\n", .{promedio(nums[0..n])});
}
```

### Nim

```nim
import std/[strutils, sequtils]

proc promedio(nums: seq[int]): int =
  var suma = 0
  for x in nums:
    suma += x
  suma div nums.len

let nums = stdin.readLine().splitWhitespace().mapIt(it.parseInt())
echo "promedio=", promedio(nums)
```

### D

```d
import std.stdio, std.string, std.conv, std.algorithm, std.array;

long promedio(long[] nums) {
    return nums.sum / cast(long) nums.length;
}

void main() {
    auto nums = readln().strip().split().map!(to!long).array;
    writefln("promedio=%d", promedio(nums));
}
```

**Qué reconocer:** en los tres el archivo **ya es** el módulo, y lo que se exporta se marca en la
declaración: `pub` en Zig, el asterisco de exportación en Nim, `private` en D. Zig hace visible algo
que los demás esconden: `@divTrunc` dice por escrito que la división entera trunca, porque el
lenguaje se niega a que un operador tenga comportamiento implícito según los tipos. Nim aprovecha su
regla de que la última expresión de un `proc` es el valor devuelto, y escribe `suma div nums.len` sin
`return`. Detalles pequeños, misma idea: un procedimiento con nombre, un archivo con frontera.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Donde no hay procedimientos, hay reglas.

### Prolog

```prolog
:- initialization(main, main).

% El "procedimiento" de Prolog es un predicado: no devuelve nada, unifica un
% argumento de salida. Por eso `promedio/2` tiene dos argumentos, no uno.
promedio(Nums, P) :-
    sum_list(Nums, S),
    length(Nums, N),
    P is S // N.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    maplist([T, X]>>number_string(X, T), Partes, Nums),
    promedio(Nums, P),
    format("promedio=~d~n", [P]).
```

### Datalog

```datalog
// Datalog no tiene procedimientos ni parámetros: solo relaciones. Tampoco tiene
// E/S, así que los datos entran como hechos.
.decl nota(x:number)
nota(2). nota(4). nota(6).

.decl promedio(p:number)
promedio(p) :- p = (sum x : { nota(x) }) / (count : { nota(_) }).
```

**Qué reconocer:** `promedio(Nums, P)` parece una función de dos parámetros y no lo es: `P` es el
hueco donde el motor deja la respuesta al unificar. La consecuencia práctica es que un predicado
puede consultarse en varias direcciones, algo que ningún procedimiento imperativo permite. Datalog da
el paso final y elimina el concepto: aquí `promedio` es el nombre de una **relación**, no de un
cálculo; no se llama, se consulta. La modularidad, en ambos, es la propia base de reglas. Si el resto
de la página trata de dónde meter las funciones, esta sección recuerda que hay paradigmas donde
sencillamente no hay funciones que meter en ningún sitio.

---

## Y de vuelta a la clase

Veinte lenguajes, un procedimiento de tres líneas, y siete respuestas distintas a "¿dónde vive?":
módulo, espacio de nombres, paquete, clase, objeto singleton, archivo, base de reglas. El
procedimiento con nombre es universal; la frontera que lo rodea es lo que cada familia se inventó, y
reconocer cuál estás mirando te dice casi siempre de qué tradición viene el lenguaje.

⏮️ [Volver a la clase 109](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
