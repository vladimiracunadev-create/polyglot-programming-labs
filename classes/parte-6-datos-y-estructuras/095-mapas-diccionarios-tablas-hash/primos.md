# 🧬 El mismo programa en las familias de lenguajes — Clase 095

> [⬅️ Volver a la clase 095](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar cuántas veces aparece el primer elemento de
la lista— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `cuenta=<veces que aparece el primer elemento>`
- **Regla:** `cuenta = frecuencia[lista[0]]`

| stdin | esperado |
|---|---|
| `3 1 3 3` | `cuenta=3` |
| `5 5` | `cuenta=2` |
| `7 1 2` | `cuenta=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Es la familia donde el mapa es el tipo estrella: `dict` en Python, y en PHP el *array* asociativo, que
además hace de lista.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
freq = Hash.new(0)
nums.each { |x| freq[x] += 1 }
puts "cuenta=#{freq[nums.first]}"
```

### Perl

```perl
my @nums = split ' ', do { local $/; <STDIN> };
my %freq;
$freq{$_}++ for @nums;
print "cuenta=$freq{$nums[0]}\n";
```

### Lua

```lua
local nums, freq = {}, {}
for tok in io.read("a"):gmatch("%S+") do
  local x = tonumber(tok)
  nums[#nums + 1] = x
  freq[x] = (freq[x] or 0) + 1
end
print("cuenta=" .. freq[nums[1]])
```

### Tcl

```tcl
set nums [regexp -all -inline {\S+} [read stdin]]
set freq [dict create]
foreach x $nums {
    dict incr freq $x
}
puts "cuenta=[dict get $freq [lindex $nums 0]]"
```

### R

```r
nums <- scan("stdin", quiet = TRUE)
freq <- table(nums)
cat(sprintf("cuenta=%d\n", freq[[as.character(nums[1])]]))
```

**Qué reconocer:** el problema recurrente del mapa de frecuencias es **qué pasa con la clave ausente**,
y cada lenguaje lo resuelve a su manera: Ruby con `Hash.new(0)`, que fija un valor por defecto; Perl con
la *autovivificación*, que hace que `$freq{$x}++` cree la clave con 0 sin avisar; Lua con el `or 0`
explícito, porque una tabla devuelve `nil`. Perl vuelve a mostrar el sigilo trabajando: `%freq` declara
el hash, pero se accede a un elemento con `$freq{...}` porque **lo que sacas es un escalar**. Lua no
tiene diccionario separado: `nums` y `freq` son **la misma clase de tabla**, una indexada por enteros y
la otra por valores. Tcl tuvo arreglos asociativos primero y añadió `dict` como valor de primera clase
en 8.5, que es por lo que aquí `dict incr` puede pasarse por variable como cualquier cadena. R devuelve
`table`, un objeto estadístico con nombres, y por eso hay que indexar por `as.character`. Un último
detalle que solo importa cuando imprimes: el `Hash` de Ruby **conserva el orden de inserción** —está
garantizado desde 1.9, igual que en el `dict` de Python desde 3.7—, mientras que la tabla de Lua no
promete ningún orden al recorrerla con `pairs`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final freq = <int, int>{};
  for (final x in nums) {
    freq[x] = (freq[x] ?? 0) + 1;
  }
  print('cuenta=${freq[nums.first]}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin: Object y Dictionary son sus dos mapas.
package {
    import flash.utils.Dictionary;

    public class Frecuencia {
        public static function contar(nums:Array):String {
            var freq:Dictionary = new Dictionary();
            for each (var x:int in nums) {
                freq[x] = (freq[x] == undefined ? 0 : freq[x]) + 1;
            }
            return "cuenta=" + freq[nums[0]];
        }
    }
}
```

**Qué reconocer:** el `Map<int, int>` de Dart admite **cualquier tipo como clave** y respeta el orden
de inserción, igual que el `Map` de JavaScript moderno. ActionScript enseña por qué ese `Map` tuvo que
inventarse: su `Object` convierte toda clave a cadena, y `Dictionary` se añadió precisamente para
permitir claves por referencia. El `?? 0` de Dart es el mismo `|| 0` que verías en JavaScript, pero
más estricto: solo salta cuando el valor es nulo, no cuando es `0`, que es una fuente clásica de
errores al contar.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos usan `java.util.Map` por debajo, pero cada
uno tiene su atajo para contar.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val freq = nums.groupingBy { it }.eachCount()
    println("cuenta=${freq[nums.first()]}")
}
```

### Scala

```scala
object Frecuencia extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val freq = nums.groupBy(identity).view.mapValues(_.length).toMap
  println(s"cuenta=${freq(nums.head)}")
}
```

### Groovy

```groovy
def nums = System.in.text.split(/\s+/).findAll { it }*.toInteger()
def freq = nums.countBy { it }
println "cuenta=${freq[nums[0]]}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))
      freq (frequencies nums)]
  (println (str "cuenta=" (freq (first nums)))))
```

**Qué reconocer:** Java necesita el bucle con `merge` o `getOrDefault`; los cuatro primos traen la
operación ya empaquetada (`eachCount`, `groupBy`, `countBy`, `frequencies`), y esa es la marca de la
familia: mismo `HashMap` debajo, distinta altura de la biblioteca encima. Clojure vuelve a separarse:
sus mapas son **literales del lenguaje** (`{:a 1}`), persistentes, y además **invocables** —`(freq 3)`
es la forma normal de consultar, sin `get`—. Cuidado con el orden: `HashMap` no lo garantiza, así que
si imprimieras las claves de `freq` verías un orden que no es ni el de inserción ni el numérico.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
let freq = nums |> Array.countBy id |> Map.ofArray
printfn "cuenta=%d" freq.[nums.[0]]
```

### VB.NET

```vbnet
Imports System.Collections.Generic

Module Frecuencia
    Sub Main()
        Dim partes = Console.ReadLine().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
        Dim nums = Array.ConvertAll(partes, AddressOf Integer.Parse)
        Dim freq As New Dictionary(Of Integer, Integer)
        For Each x In nums
            Dim actual = 0
            freq.TryGetValue(x, actual)
            freq(x) = actual + 1
        Next
        Console.WriteLine("cuenta=" & freq(nums(0)))
    End Sub
End Module
```

**Qué reconocer:** VB.NET usa el mismo `Dictionary(Of K, V)` que C#, con la firma característica de
.NET para la clave ausente: `TryGetValue` devuelve un booleano y **escribe el valor en un parámetro de
salida**, en vez de devolver nulo. F# no usa ese tipo: su `Map` es inmutable, ordenado por clave y con
igualdad estructural, y `Array.countBy` hace el conteo sin escribir un solo bucle. Es la misma máquina
virtual sirviendo dos modelos de datos incompatibles en cuanto a mutación.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene mapas: o escribes la tabla hash o recorres
el arreglo contando.

### C++

```cpp
#include <iostream>
#include <unordered_map>
#include <vector>

int main() {
    std::vector<int> nums;
    int x;
    while (std::cin >> x) nums.push_back(x);

    std::unordered_map<int, int> freq;
    for (int v : nums) ++freq[v];
    std::cout << "cuenta=" << freq[nums.front()] << '\n';
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
        NSMutableArray<NSNumber *> *nums = [NSMutableArray array];
        NSCountedSet<NSNumber *> *freq = [NSCountedSet set];
        for (NSString *t in [linea componentsSeparatedByCharactersInSet:
                             [NSCharacterSet whitespaceAndNewlineCharacterSet]]) {
            if (t.length == 0) continue;
            NSNumber *n = @(t.intValue);
            [nums addObject:n];
            [freq addObject:n];
        }
        printf("cuenta=%lu\n", (unsigned long)[freq countForObject:nums.firstObject]);
    }
    return 0;
}
```

**Qué reconocer:** `++freq[v]` funciona porque `operator[]` de C++ **inserta la clave con el valor por
defecto** (`0` para `int`) si no existe; es cómodo y a la vez la trampa clásica, porque una simple
consulta con `[]` sobre un mapa constante no compila y sobre uno mutable crea la entrada. Igual que en
la clase de conjuntos, C++ te obliga a elegir entre `std::map` (árbol ordenado) y `std::unordered_map`
(tabla hash) en el nombre del tipo. Objective-C tiene `NSDictionary`, pero aquí lo idiomático es
`NSCountedSet`: un conjunto que **guarda la multiplicidad de cada objeto**, es decir, exactamente un
mapa de frecuencias con nombre propio.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). El mapa existe, pero el
lenguaje te recuerda que cuesta memoria.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    var freq = std.AutoHashMap(i64, u32).init(gpa.allocator());
    defer freq.deinit();

    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var primero: ?i64 = null;
    while (it.next()) |tok| {
        const x = try std.fmt.parseInt(i64, tok, 10);
        if (primero == null) primero = x;
        const e = try freq.getOrPut(x);
        if (!e.found_existing) e.value_ptr.* = 0;
        e.value_ptr.* += 1;
    }
    try std.io.getStdOut().writer().print("cuenta={d}\n", .{freq.get(primero.?).?});
}
```

### Nim

```nim
import std/[strutils, sequtils, tables]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
let freq = nums.toCountTable()
echo "cuenta=", freq[nums[0]]
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

void main() {
    auto nums = readln().strip().split().map!(to!int).array;
    int[int] freq;
    foreach (x; nums) freq[x]++;
    writeln("cuenta=", freq[nums[0]]);
}
```

**Qué reconocer:** D es el único de la familia con el mapa **en la sintaxis del lenguaje**: `int[int]`
se lee "enteros indexados por enteros", el mismo patrón que `int[]` para un arreglo, y no hace falta
importar nada. Nim trae `CountTable`, una tabla de frecuencias ya hecha, y devuelve `0` para claves
ausentes en vez de lanzar excepción. Zig es el más honesto sobre el coste: `getOrPut` hace **una sola
búsqueda** y te devuelve un puntero al hueco —en vez de las dos búsquedas de "¿existe? entonces
incrementa"—, y el mapa necesita asignador y `deinit`, así que aquí la tabla hash no es gratis ni
invisible.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `GROUP BY` es el mapa de frecuencias del mundo
relacional.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Nums),
    Nums = [Primero|_],
    include(==(Primero), Nums, Iguales),
    length(Iguales, C),
    format("cuenta=~d~n", [C]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni agregación: no puede contar.
% Lo más cercano es declarar el dato con su posición y derivar qué hechos coinciden
% con el primero; el conteo queda fuera del lenguaje.
num(1, 3).
num(2, 1).
num(3, 3).
num(4, 3).

primero(V) :- num(1, V).
coincide(I) :- num(I, V), primero(V).
```

**Qué reconocer:** ni Prolog ni Datalog construyen un mapa, y la razón es la misma: **la base de hechos
ya es la tabla indexada**. El motor de Prolog indexa `num/2` por su primer argumento igual que una tabla
hash indexa por clave, así que consultar es la operación primitiva y el diccionario sobra. Prolog aún
puede contar porque tiene `length/2` y agregados como `aggregate_all/3`; Datalog puro no —sin
agregación ni efectos, solo puede decir **qué** hechos coinciden, no cuántos—, que es la misma renuncia
que hace SQL al describir el `GROUP BY` sin decirte cómo agrupa.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma pregunta en todos: qué pasa cuando pides una clave que
no está. Valor por defecto, nulo, excepción, autovivificación o parámetro de salida. Ese detalle, y no
la sintaxis del acceso, es lo que distingue de verdad a un mapa de otro.

⏮️ [Volver a la clase 095](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
