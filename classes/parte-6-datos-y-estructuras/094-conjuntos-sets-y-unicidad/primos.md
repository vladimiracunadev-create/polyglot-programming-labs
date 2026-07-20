# 🧬 El mismo programa en las familias de lenguajes — Clase 094

> [⬅️ Volver a la clase 094](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar cuántos valores distintos hay en una lista—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `unicos=<cantidad de valores distintos>`
- **Regla:** `unicos = |conjunto(lista)|`

| stdin | esperado |
|---|---|
| `1 2 2 3 3 3` | `unicos=3` |
| `5 5 5` | `unicos=1` |
| `1 2 3 4` | `unicos=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tiene `set` como tipo del lenguaje; PHP no, y usa las claves de un arreglo asociativo. Esa
grieta atraviesa a toda la familia.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
puts "unicos=#{nums.uniq.size}"
```

### Perl

```perl
my @nums = split ' ', do { local $/; <STDIN> };
my %visto;
$visto{$_} = 1 for @nums;
printf "unicos=%d\n", scalar keys %visto;
```

### Lua

```lua
local visto, n = {}, 0
for tok in io.read("a"):gmatch("%S+") do
  local x = tonumber(tok)
  if not visto[x] then
    visto[x] = true
    n = n + 1
  end
end
print("unicos=" .. n)
```

### Tcl

```tcl
set nums [regexp -all -inline {\S+} [read stdin]]
puts "unicos=[llength [lsort -unique -integer $nums]]"
```

### R

```r
nums <- scan("stdin", quiet = TRUE)
cat(sprintf("unicos=%d\n", length(unique(nums))))
```

**Qué reconocer:** solo Ruby tiene un `Set` de verdad (`require "set"`), y aun así es una clase de
biblioteca construida **sobre un Hash** con valores ignorados; por eso `uniq` sobre el arreglo es lo
que escribe un rubista. Perl no tiene conjuntos: los emula con `%visto`, y el sigilo lo delata —`%`
anuncia hash, `@` anuncia arreglo, la sintaxis misma dice qué estructura estás usando—. Lua es el caso
más radical: **no tiene ni conjuntos ni listas**, solo la tabla, que aquí hace de conjunto poniendo el
valor en las claves y `true` de relleno; la misma tabla haría de arreglo con claves 1..n. Tcl ni
siquiera crea una estructura: ordena y elimina adyacentes duplicados, que es la otra vía clásica para
la unicidad. R llega por el camino vectorial, con `unique` como operación sobre el vector entero.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  print('unicos=${nums.toSet().length}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin ni tipo Set: un Object hace de conjunto de claves.
package {
    public class Unicos {
        public static function contar(nums:Array):String {
            var visto:Object = {};
            var n:int = 0;
            for each (var x:int in nums) {
                if (visto[x] == undefined) {
                    visto[x] = true;
                    n++;
                }
            }
            return "unicos=" + n;
        }
    }
}
```

**Qué reconocer:** Dart trae `Set` desde el principio y `toSet()` cuelga de cualquier iterable, igual
que el `new Set(...)` de JavaScript moderno. ActionScript 3 es JavaScript **congelado en 2006**: se ve
el mismo lenguaje antes de que ES6 le diera `Set` y `Map`, obligado al truco de usar un objeto como
diccionario de claves. Ese truco tiene un coste real que Dart no paga: las claves de un `Object` se
convierten a **cadena**, así que `1` y `"1"` colisionan.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos acaban en `java.util.Set`, pero no todos
lo escriben igual ni con las mismas garantías.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("unicos=${nums.toSet().size}")
}
```

### Scala

```scala
object Unicos extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"unicos=${nums.toSet.size}")
}
```

### Groovy

```groovy
def nums = System.in.text.split(/\s+/).findAll { it }*.toInteger()
println "unicos=${nums.toSet().size()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))]
  (println (str "unicos=" (count (set nums)))))
```

**Qué reconocer:** el `toSet()` de Kotlin y Groovy devuelve un `LinkedHashSet`, que **conserva el orden
de inserción**; el de Scala y el `HashSet` pelado de Java no lo garantizan. Da igual para contar, pero
si imprimieras los elementos verías salidas distintas del mismo programa. Clojure va más lejos: sus
conjuntos son **literales del lenguaje** (`#{1 2 3}`) y son persistentes —añadir devuelve un conjunto
nuevo compartiendo estructura con el viejo, en vez de mutar el existente—. Además un conjunto de
Clojure es **invocable**: `(#{1 2 3} 2)` devuelve `2`, y esa es la forma idiomática de preguntar por
pertenencia.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
printfn "unicos=%d" (nums |> Set.ofArray |> Set.count)
```

### VB.NET

```vbnet
Imports System.Collections.Generic

Module Unicos
    Sub Main()
        Dim partes = Console.ReadLine().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
        Dim conjunto As New HashSet(Of Integer)
        For Each p In partes
            conjunto.Add(Integer.Parse(p))
        Next
        Console.WriteLine("unicos=" & conjunto.Count)
    End Sub
End Module
```

**Qué reconocer:** VB.NET usa el mismo `HashSet(Of T)` que C#, mutable y sin orden garantizado, y su
`Add` devuelve `False` si el elemento ya estaba —el propio método es la prueba de pertenencia—. F#
**no** usa ese tipo: `Set` de F# es un árbol binario balanceado, **inmutable y ordenado**, con
comparación estructural. La consecuencia práctica es que en F# dos conjuntos con los mismos elementos
son iguales con `=`, mientras que en C# y VB.NET `Equals` compara referencias y hay que llamar a
`SetEquals`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene conjuntos: hay que ordenar el arreglo o
escribirse la tabla hash.

### C++

```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> unicos;
    int x;
    while (std::cin >> x) unicos.insert(x);
    std::cout << "unicos=" << unicos.size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *linea = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile]
                encoding:NSUTF8StringEncoding];
        NSMutableSet<NSNumber *> *unicos = [NSMutableSet set];
        for (NSString *t in [linea componentsSeparatedByCharactersInSet:
                             [NSCharacterSet whitespaceAndNewlineCharacterSet]]) {
            if (t.length > 0) [unicos addObject:@(t.intValue)];
        }
        printf("unicos=%lu\n", (unsigned long)unicos.count);
    }
    return 0;
}
```

**Qué reconocer:** C++ es de los pocos lenguajes que te obliga a **elegir la implementación** en el
nombre del tipo: `std::set` es un árbol ordenado con inserción en O(log n), `std::unordered_set` es la
tabla hash en O(1) amortizado. En casi todas las familias anteriores esa decisión venía tomada de
fábrica. Objective-C sí trae `NSSet`, pero solo admite **objetos**: por eso `@(t.intValue)` envuelve
el entero en un `NSNumber`, el mismo peaje de empaquetado que paga Java con `Integer`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go tampoco tiene conjuntos
—usa `map[T]struct{}`—; Rust sí, con `HashSet`.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    var visto = std.AutoHashMap(i64, void).init(gpa.allocator());
    defer visto.deinit();

    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    while (it.next()) |tok| {
        try visto.put(try std.fmt.parseInt(i64, tok, 10), {});
    }
    try std.io.getStdOut().writer().print("unicos={d}\n", .{visto.count()});
}
```

### Nim

```nim
import std/[strutils, sequtils, sets]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
echo "unicos=", toHashSet(nums).len
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

void main() {
    auto nums = readln().strip().split().map!(to!int);
    bool[int] visto;
    foreach (x; nums) visto[x] = true;
    writeln("unicos=", visto.length);
}
```

**Qué reconocer:** solo Nim trae un conjunto de biblioteca (`HashSet`, y además `set[T]` como conjunto
de bits para tipos ordinales pequeños). Zig y D repiten el gesto de Go: **el conjunto es un mapa con el
valor vacío** —`void` en Zig, `bool` en D— porque en sistemas nadie quiere pagar por una estructura que
puede derivarse de otra. Zig añade lo que ninguno de los anteriores exige: el conjunto necesita un
**asignador explícito** y un `deinit`, así que la pregunta "¿quién libera esta memoria?" está en el
propio código en vez de en el recolector de basura.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `COUNT(DISTINCT x)` responde en una línea porque
la unicidad ya es parte del modelo relacional.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Nums),
    sort(Nums, Unicos),
    length(Unicos, C),
    format("unicos=~d~n", [C]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni agregación estándar: aquí la unicidad no se calcula.
% Una relación *es* un conjunto, y declarar el mismo hecho dos veces no lo duplica.
num(1).
num(2).
num(2).
num(3).
num(3).
num(3).

distinto(X) :- num(X).
```

**Qué reconocer:** en Prolog `sort/2` **elimina duplicados** además de ordenar —si quieres conservarlos
tienes que pedir `msort/2`—, así que el conjunto sale como efecto de la ordenación, igual que en Tcl.
Datalog enseña el fondo del asunto: en el modelo relacional una relación es un conjunto **por
definición**, y por eso los seis hechos `num` de arriba son solo tres. Es exactamente la razón por la
que SQL necesita la palabra `DISTINCT` como excepción: las tablas de SQL, a diferencia de las
relaciones puras, sí admiten filas repetidas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una división limpia: los que tienen conjunto como tipo del
lenguaje, los que lo tienen como clase de biblioteca, y los que lo fabrican con un mapa de claves.
Saber en cuál de los tres grupos estás te dice de antemano qué código vas a escribir.

⏮️ [Volver a la clase 094](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
