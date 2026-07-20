# 🧬 El mismo programa en las familias de lenguajes — Clase 089

> [⬅️ Volver a la clase 089](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —tres enteros metidos en un arreglo de tamaño fijo,
su suma y su máximo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b c` — tres enteros separados por espacio
- **Salida** (stdout): `suma=<a+b+c> max=<el mayor>`
- **Regla:** los tres valores viven en un arreglo de **exactamente tres huecos**; se recorren para
  acumular la suma y quedarse con el máximo

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8 max=4` |
| `10 5 2` | `suma=17 max=10` |
| `1 1 1` | `suma=3 max=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de esta familia tiene un arreglo de tamaño fijo de verdad: la lista crece y encoge siempre.
El "tamaño fijo" es aquí una **disciplina del programador**, no una garantía del lenguaje.

### Ruby

```ruby
# Ruby no tiene arreglos de tamaño fijo: Array siempre puede crecer.
arr = STDIN.gets.split.map(&:to_i)
puts "suma=#{arr.sum} max=#{arr.max}"
```

### Perl

```perl
use List::Util qw(sum max);

# @arr es dinámico: Perl no distingue arreglo fijo de arreglo variable.
my @arr = split ' ', <STDIN>;
printf "suma=%d max=%d\n", sum(@arr), max(@arr);
```

### Lua

```lua
local a, b, c = io.read("n", "n", "n")
local arr = {a, b, c}          -- arr[1], arr[2], arr[3]: Lua numera desde 1
local suma, maximo = 0, arr[1]
for i = 1, #arr do             -- el bucle idiomático va de 1 a #arr, no de 0 a n-1
  suma = suma + arr[i]
  if arr[i] > maximo then maximo = arr[i] end
end
print(string.format("suma=%d max=%d", suma, maximo))
```

### Tcl

```tcl
gets stdin linea
set arr [split $linea]
set suma 0
set maximo [lindex $arr 0]     ;# lindex sí es base 0
foreach x $arr {
    incr suma $x
    if {$x > $maximo} {set maximo $x}
}
puts "suma=$suma max=$maximo"
```

### R

```r
# En R el "arreglo" es la unidad natural: sum() y max() operan sobre el vector entero.
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("suma=%d max=%d\n", sum(v), max(v)))
```

**Qué reconocer:** los cinco leen la línea y la parten igual, pero solo uno de ellos podría fallar
al portar el código. **Lua indexa desde 1**: `arr[1]` es el primer elemento y `arr[0]` simplemente
no existe (vale `nil`), la trampa clásica cuando se traduce un bucle `for i = 0` venido de C. R
comparte esa base 1 —`v[1]` es el primero— pero Tcl **no**: su `lindex` cuenta desde 0 pese a
parecerse en todo lo demás. Ruby y Perl ni siquiera plantean la pregunta del tamaño: sus arreglos
son dinámicos y punto, así que la aridad tres es una convención que nadie verifica. R lleva el eje
al otro extremo: no recorre nada, porque `sum` y `max` están **vectorizados** y consumen el vector
completo de una vez.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final campos = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  // growable: false congela la longitud; añadir un elemento lanza en tiempo de ejecución.
  final arr = List<int>.generate(3, (i) => int.parse(campos[i]), growable: false);
  final suma = arr.reduce((x, y) => x + y);
  final maximo = arr.reduce((x, y) => x > y ? x : y);
  print('suma=$suma max=$maximo');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el arreglo fijo.
package {
    public class Arreglo {
        public static function resumen(a:int, b:int, c:int):String {
            var arr:Vector.<int> = new <int>[a, b, c];
            arr.fixed = true;  // lo más cercano a un arreglo fijo: la longitud queda bloqueada
            var suma:int = 0;
            var maximo:int = arr[0];
            for (var i:int = 0; i < arr.length; i++) {
                suma += arr[i];
                if (arr[i] > maximo) maximo = arr[i];
            }
            return "suma=" + suma + " max=" + maximo;
        }
    }
}
```

**Qué reconocer:** los dos parten del `Array` elástico de JavaScript y le añaden un candado
**en tiempo de ejecución**, no en el tipo: `growable: false` en Dart y `fixed = true` en el
`Vector.<int>` de AS3. La diferencia con C o Zig es exactamente esa — aquí el tamaño fijo es una
propiedad del objeto que se comprueba al añadir, no una parte del tipo que impida compilar. AS3
además tipa el contenido (`Vector.<int>` solo acepta enteros), un paso intermedio entre el array
heterogéneo de JS y el arreglo homogéneo de los lenguajes de sistemas.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En la JVM el array nativo (`int[]`) **sí**
tiene longitud fija, fijada al construirlo; lo que cambia entre lenguajes es cuánto lo esconden.

### Kotlin

```kotlin
fun main() {
    val arr = IntArray(3)  // longitud 3, inmutable como longitud; los huecos sí se escriben
    readLine()!!.trim().split(Regex("\\s+")).forEachIndexed { i, s -> arr[i] = s.toInt() }
    println("suma=${arr.sum()} max=${arr.max()}")
}
```

### Scala

```scala
object Arreglo extends App {
  // Array es el int[] de Java: mutable en contenido, fijo en longitud.
  val arr: Array[Int] = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"suma=${arr.sum} max=${arr.max}")
}
```

### Groovy

```groovy
int[] arr = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "suma=${arr.sum()} max=${arr.max()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [arr (int-array (map parse-long (str/split (str/trim (read-line)) #"\s+")))
      v   (vec arr)]  ; el vector persistente es la estructura por defecto de Clojure
  (println (format "suma=%d max=%d" (reduce + v) (apply max v))))
```

**Qué reconocer:** los cuatro acaban sobre el mismo `int[]` de la JVM, cuya longitud es inmutable
—`arr.length` es un campo, no un método—. Kotlin lo hace explícito con `IntArray(3)` y separa ese
tipo de `List`/`MutableList`; Scala mantiene la misma frontera entre `Array` **mutable** y `List`
**inmutable**, y aquí elige el primero justo porque el problema habla de arreglos. Groovy disuelve
la distinción tras `def` y la coerción automática. Clojure rompe con la familia: `int-array` existe
para interoperar con Java, pero lo idiomático es el **vector persistente** `[3 1 4]`, que no tiene
tamaño fijo ni mutación: cada cambio devuelve una estructura nueva compartiendo memoria con la
anterior.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// Array es la estructura mutable y de longitud fija; List sería inmutable y enlazada.
let arr : int[] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "suma=%d max=%d" (Array.sum arr) (Array.max arr)
```

### VB.NET

```vbnet
Imports System

Module Arreglo
    Sub Main()
        Dim campos = Console.ReadLine().Trim().Split(" "c)
        Dim arr(2) As Integer  ' Dim arr(2) declara el ÚLTIMO índice: son 3 huecos, 0..2
        For i = 0 To 2
            arr(i) = Integer.Parse(campos(i))
        Next
        Dim suma = 0
        Dim maximo = arr(0)
        For Each x In arr
            suma += x
            If x > maximo Then maximo = x
        Next
        Console.WriteLine($"suma={suma} max={maximo}")
    End Sub
End Module
```

**Qué reconocer:** los tres comparten el mismo `System.Array` del CLR, con `Length` fijo desde la
construcción y `System.Collections.Generic.List(Of T)` como la alternativa que sí crece. VB.NET
esconde la trampa de indexación más sutil de toda esta página: `Dim arr(2)` **no** declara dos
elementos sino tres, porque el número entre paréntesis es el índice superior, no la cantidad —un
resto histórico de BASIC, donde incluso existía `Option Base 1` para empezar a contar en 1. F#
enseña el otro eje: `int[]` es su estructura mutable de tamaño fijo y `int list` la inmutable, dos
tipos distintos con módulos distintos (`Array.sum` frente a `List.sum`), y el compilador no deja
confundirlos.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El arreglo fijo es aquí un bloque contiguo de
memoria cuyo tamaño se conoce al compilar.

### C++

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>

int main() {
    std::array<int, 3> arr{};  // el 3 va en el TIPO: vive en la pila, sin reservar heap
    std::cin >> arr[0] >> arr[1] >> arr[2];
    const int suma = std::accumulate(arr.begin(), arr.end(), 0);
    const int maximo = *std::max_element(arr.begin(), arr.end());
    std::cout << "suma=" << suma << " max=" << maximo << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int arr[3];  // arreglo C puro: NSArray existiría, pero es dinámico y de objetos
        scanf("%d %d %d", &arr[0], &arr[1], &arr[2]);
        int suma = 0, maximo = arr[0];
        for (int i = 0; i < 3; i++) {
            suma += arr[i];
            if (arr[i] > maximo) maximo = arr[i];
        }
        printf("suma=%d max=%d\n", suma, maximo);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C** y el `int arr[3]` de la clase compila tal cual
en los dos. C++ añade la distinción que da nombre a esta clase: `std::array<int, 3>` lleva el tamaño
en el tipo y se asigna en la **pila**, mientras que `std::vector<int>` reserva en el **heap** y
crece — dos tipos separados para dos decisiones distintas de memoria, algo que C deja al
programador. Objective-C se queda en el arreglo C para los enteros porque su `NSArray` solo guarda
objetos y siempre es dinámico: para meter tres `int` habría que envolverlos en `NSNumber`, pagando
una indirección que el problema no pide.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los tres primos
distinguen con precisión quirúrgica lo que ocupa un tamaño conocido de lo que se reserva en tiempo
de ejecución.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, linea, " \r"), " ");

    var arr: [3]i64 = undefined;  // el tamaño es parte del tipo: [3]i64 y [4]i64 no son el mismo
    for (&arr) |*hueco| {
        hueco.* = try std.fmt.parseInt(i64, it.next().?, 10);
    }

    var suma: i64 = 0;
    var maximo: i64 = arr[0];
    for (arr) |x| {
        suma += x;
        if (x > maximo) maximo = x;
    }
    try std.io.getStdOut().writer().print("suma={d} max={d}\n", .{ suma, maximo });
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

let campos = stdin.readLine().splitWhitespace().map(parseInt)
var arr: array[3, int]  # array[3, int] es fijo; seq[int] sería el dinámico
for i in 0 ..< 3:
  arr[i] = campos[i]
echo "suma=", arr.sum, " max=", arr.max
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto campos = readln().split();
    int[3] arr;  // arreglo estático: en la pila. int[] sería dinámico, en el heap
    foreach (i, ref x; arr) x = campos[i].to!int;
    // arr[] toma un slice del estático: vista sin copia sobre los mismos 3 enteros
    writefln("suma=%d max=%d", arr[].sum, arr[].maxElement);
}
```

**Qué reconocer:** aquí el eje de la clase está escrito en la sintaxis. **Zig exige el tamaño en el
tipo**: `[3]i64` es un tipo distinto de `[4]i64`, así que pasar un arreglo de la longitud
equivocada ni siquiera compila. Nim marca la misma frontera con dos nombres, `array[3, int]` fijo
frente a `seq[int]` dinámico. D distingue arreglo **estático** (`int[3]`, en la pila) de
**dinámico** (`int[]`, en el heap) y añade la pieza que los conecta: el *slice* `arr[]`, una vista
de puntero más longitud sobre esos mismos tres enteros, sin copiarlos — la misma idea que el
`&[i32]` de Rust y el `[]int` de Go.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay arreglos ni índices: hay relaciones, y
la posición se vuelve un dato más.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    Nums = [_, _, _],  % la aridad fija se comprueba unificando, no declarando un tamaño
    sum_list(Nums, Suma),
    max_list(Nums, Maximo),
    format("suma=~d max=~d~n", [Suma, Maximo]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni agregados: no puede sumar. Se declaran las celdas
% del arreglo como hechos (índice, valor) y se deriva el máximo por negación.
celda(0, 3).
celda(1, 1).
celda(2, 4).

superado(X) :- celda(_, X), celda(_, Y), Y > X.
maximo(X) :- celda(_, X), not superado(X).
```

**Qué reconocer:** ninguno de los dos tiene arreglo de tamaño fijo, y esa ausencia es informativa.
Prolog usa **listas** enlazadas, así que el tamaño no se declara: se **comprueba** unificando con
el patrón `[_, _, _]`, que falla si llegan dos o cuatro elementos — la aridad como consulta, no
como tipo. Datalog va más lejos: sin listas ni agregados estándar, un arreglo solo se puede modelar
como una relación `celda(índice, valor)`, exactamente lo que hace SQL cuando guardas una secuencia
en una tabla con columna de orden. El índice deja de ser una dirección de memoria y pasa a ser un
atributo, que es justo por qué en esas dos familias la pregunta "¿empieza en 0 o en 1?" pierde todo
su sentido.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres preguntas que cada familia responde distinto: ¿el tamaño
está en el tipo o en el objeto?, ¿el arreglo vive en la pila o en el heap?, ¿el primer elemento es
el 0 o el 1? Reconocer cuál de las tres te va a morder al portar código es lo transferible.

⏮️ [Volver a la clase 089](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
