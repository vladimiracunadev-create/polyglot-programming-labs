# 🧬 El mismo programa en las familias de lenguajes — Clase 090

> [⬅️ Volver a la clase 090](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —invertir una lista dinámica de enteros— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio, cantidad desconocida de antemano
- **Salida** (stdout): `invertido=<elementos en orden inverso unidos por ->`
- **Regla:** `invertido = reverse(lista)`

| stdin | esperado |
|---|---|
| `1 2 3` | `invertido=3-2-1` |
| `5` | `invertido=5` |
| `10 20 30 40` | `invertido=40-30-20-10` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí la lista dinámica **es** la estructura por defecto: no hay que elegirla ni pedir memoria, y por
eso todos resuelven el problema en dos o tres líneas.

### Ruby

```ruby
# Array es dinámico y punto: Ruby no tiene un tipo de arreglo fijo con el que contrastarlo.
nums = STDIN.read.split
puts "invertido=#{nums.reverse.join('-')}"
```

### Perl

```perl
# @nums crece sola: basta asignar a $nums[99] para que el arreglo llegue hasta ahí.
my @nums = split ' ', do { local $/; <STDIN> };
print "invertido=", join('-', reverse @nums), "\n";
```

### Lua

```lua
local nums = {}
for palabra in io.read("a"):gmatch("%S+") do
  nums[#nums + 1] = palabra  -- se crece por el final; el primer índice es 1, no 0
end
local invertido = {}
for i = #nums, 1, -1 do      -- se baja hasta 1, nunca hasta 0
  invertido[#invertido + 1] = nums[i]
end
print("invertido=" .. table.concat(invertido, "-"))
```

### Tcl

```tcl
set nums [regexp -all -inline {\S+} [read stdin]]
puts "invertido=[join [lreverse $nums] -]"
```

### R

```r
# Un vector es la unidad natural de R: rev() invierte el vector entero de una vez.
v <- scan("stdin", what = integer(), quiet = TRUE)
cat("invertido=", paste(rev(v), collapse = "-"), "\n", sep = "")
```

**Qué reconocer:** los cinco tienen una única estructura secuencial que crece sola, así que la
pregunta "¿fijo o dinámico?" ni se plantea: en Ruby y Perl el arreglo es siempre dinámico y no
existe una contraparte de tamaño fijo. Lua obliga a escribir el crecimiento a mano
(`nums[#nums + 1] = x`) porque su tabla no es una lista sino un diccionario que finge serlo, y ahí
aparece la trampa de la clase: **Lua numera desde 1**, así que el bucle inverso termina en `1` y no
en `0`, exactamente como en R —`v[1]` es el primer elemento— y al revés que en Tcl, cuyo `lindex`
cuenta desde 0. R vuelve a delatar su origen estadístico: no recorre nada, aplica `rev` al vector
completo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  // Por defecto las List de Dart son growable: crecen con add() sin declarar capacidad.
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('invertido=${nums.reversed.join("-")}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el Array dinámico.
package {
    public class Invertir {
        public static function invertir(entrada:String):String {
            var nums:Array = entrada.split(" ");  // Array crece y encoge en caliente
            nums.reverse();                        // muta el propio arreglo, no devuelve copia
            return "invertido=" + nums.join("-");
        }
    }
}
```

**Qué reconocer:** los dos heredan el `Array` elástico de JavaScript, donde `push` y `length` son la
única API que hace falta. La diferencia entre ellos está en si la inversión **muta o copia**:
`reverse()` de AS3 —igual que el de JavaScript— da la vuelta al arreglo original y devuelve esa
misma referencia, mientras que `reversed` de Dart entrega una vista perezosa (`Iterable`) que no
toca la lista. Es la misma división que separa `list.reverse()` de `reversed(list)` en Python, y
saber de qué lado está cada uno evita el bug de encontrarte la lista dada la vuelta sin haberlo
pedido.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En la JVM el array (`int[]`) es fijo, así que
lo dinámico siempre es una **clase de colección** construida encima.

### Kotlin

```kotlin
fun main() {
    // split devuelve List (solo lectura); hay que pedir MutableList para poder invertir en sitio.
    val nums = readLine()!!.trim().split(Regex("\\s+")).toMutableList()
    nums.reverse()
    println("invertido=${nums.joinToString("-")}")
}
```

### Scala

```scala
object Invertir extends App {
  // List de Scala es inmutable y enlazada: reverse devuelve otra lista, no modifica esta.
  val nums: List[String] = scala.io.StdIn.readLine().trim.split("\\s+").toList
  println(s"invertido=${nums.reverse.mkString("-")}")
}
```

### Groovy

```groovy
def nums = System.in.newReader().readLine().trim().split(/\s+/) as List
println "invertido=${nums.reverse().join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; rseq recorre un vector persistente al revés en tiempo constante, sin copiarlo.
(let [nums (vec (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "invertido=" (str/join "-" (rseq nums)))))
```

**Qué reconocer:** los cuatro acaban en `java.util.List` o en algo que la implementa, pero cada uno
dibuja la frontera mutable/inmutable en un sitio distinto. Kotlin separa el **tipo** `List` (solo
lectura) de `MutableList`, y por eso hay que llamar a `toMutableList()` antes de invertir en sitio.
Scala mantiene la misma distinción entre `Array` mutable y `List` inmutable, pero aquí la `List`
enlazada gana porque invertir una lista enlazada es lo natural: `reverse` construye una nueva y deja
la original intacta. Groovy vuelve al `ArrayList` mutable de Java sin ceremonia. Clojure usa
**vectores persistentes**: no hay mutación en ningún momento, `rseq` devuelve una vista invertida en
O(1) y el vector original sigue disponible para quien lo tuviera.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System

// F# distingue el Array mutable de la List inmutable y enlazada; aquí usamos la segunda.
let nums =
    stdin.ReadLine().Trim().Split([| ' ' |], StringSplitOptions.RemoveEmptyEntries)
    |> List.ofArray

printfn "invertido=%s" (nums |> List.rev |> String.concat "-")
```

### VB.NET

```vbnet
Imports System
Imports System.Collections.Generic

Module Invertir
    Sub Main()
        ' List(Of T) es la colección que crece; Dim arr(2) sería el arreglo fijo.
        Dim nums As New List(Of String)(Console.ReadLine().Trim().Split(" "c))
        nums.Reverse()  ' invierte en sitio y devuelve Nothing
        Console.WriteLine("invertido=" & String.Join("-", nums))
    End Sub
End Module
```

**Qué reconocer:** en el CLR la pareja es siempre la misma: `T[]` de longitud fija frente a
`List(Of T)` que redimensiona su búfer interno cuando se llena. VB.NET usa la clase mutable y su
`Reverse()` **no devuelve nada** —invierte en sitio—, error habitual de quien escribe
`nums = nums.Reverse()` y se queda con `Nothing`. F# elige la otra rama: su `list` es inmutable y
enlazada, con módulos separados (`List.rev` frente a `Array.rev`) que el compilador no deja
confundir, así que la pregunta "¿me modificó el original?" desaparece por construcción.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C crecer significa `malloc`, `realloc` y llevar
la cuenta de la capacidad a mano.

### C++

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    // std::vector reserva en el heap y duplica su capacidad al llenarse.
    std::vector<std::string> nums;
    for (std::string palabra; std::cin >> palabra; ) nums.push_back(palabra);
    std::reverse(nums.begin(), nums.end());

    std::cout << "invertido=";
    for (std::size_t i = 0; i < nums.size(); ++i) {
        if (i) std::cout << '-';
        std::cout << nums[i];
    }
    std::cout << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        // NSArray es dinámico pero inmutable; NSMutableArray es el que crece con addObject:.
        NSArray<NSString *> *campos =
            [[linea stringByTrimmingCharactersInSet:blancos] componentsSeparatedByString:@" "];
        NSArray *invertido = [[campos reverseObjectEnumerator] allObjects];
        printf("invertido=%s\n", [[invertido componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** los dos evitan el `realloc` manual de C, pero por caminos opuestos.
`std::vector` es la contraparte exacta de `std::array` que veíamos en la clase anterior: mismo
acceso `[i]`, misma contigüidad en memoria, pero reserva en el **heap** y crece amortizado, y por eso
el tamaño no aparece en el tipo. Objective-C parte en dos la idea de colección: `NSArray` es
dinámico en longitud pero **inmutable** una vez creado, y para añadir hace falta `NSMutableArray`
—dos clases distintas, no un modificador—. Además solo guarda objetos, así que los enteros viajarían
envueltos en `NSNumber`; aquí se manipulan como cadenas porque la salida es texto.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Crecer implica un
**asignador**, y estos lenguajes hacen visible quién lo provee y quién libera.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();  // en Zig el asignador es un argumento explícito

    var buf: [4096]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;

    var lista = std.ArrayList([]const u8).init(alloc);
    defer lista.deinit();
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, linea, " \r"), " ");
    while (it.next()) |palabra| try lista.append(palabra);

    std.mem.reverse([]const u8, lista.items);
    const salida = try std.mem.join(alloc, "-", lista.items);
    defer alloc.free(salida);
    try std.io.getStdOut().writer().print("invertido={s}\n", .{salida});
}
```

### Nim

```nim
import std/[strutils, algorithm]

var nums = stdin.readLine().splitWhitespace()  # seq[string]: el dinámico, frente a array[N, T]
nums.reverse()
echo "invertido=", nums.join("-")
```

### D

```d
import std.stdio, std.array, std.range, std.algorithm;

void main() {
    auto nums = readln().split();  // string[]: arreglo dinámico, puntero + longitud en el heap
    // retro es un rango perezoso: no copia nada, solo recorre al revés.
    writeln("invertido=", nums.retro.join("-"));
}
```

**Qué reconocer:** la contraparte dinámica del arreglo fijo aparece con nombre propio en los tres:
`ArrayList` en Zig, `seq[T]` frente a `array[N, T]` en Nim, `T[]` frente a `T[N]` en D. Zig es el
único que **no esconde el asignador**: hay que pasárselo a `init` y liberar con `deinit`, la misma
honestidad que exige `try` en cada operación falible. D enseña la pieza que explica toda la familia
—su arreglo dinámico es literalmente un *slice*, un puntero más una longitud— y por eso `retro`
invierte sin copiar, igual que `.rev()` sobre un iterador de Rust o un `[]int` reordenado en Go.
Nim se queda en el punto medio: sintaxis de scripting, pero `seq` y `array` siguen siendo tipos
distintos que el compilador vigila.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El orden no es una propiedad de la estructura:
hay que declararlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Nums),
    reverse(Nums, Invertido),  % la lista enlazada es EL tipo de datos de Prolog
    atomic_list_concat(Invertido, '-', Salida),
    format("invertido=~w~n", [Salida]).
```

### Datalog

```datalog
% Datalog no tiene listas, ni E/S, ni orden en el resultado: una secuencia solo se
% puede modelar como hechos (posición, valor), y la inversión es aritmética de índices.
elem(1, 1).
elem(2, 2).
elem(3, 3).
largo(3).

invertido(J, V) :- elem(I, V), largo(N), J = N - I + 1.
```

**Qué reconocer:** Prolog sí tiene una estructura secuencial de primera clase, pero es una **lista
enlazada inmutable**: `reverse/2` no modifica nada, relaciona una lista con otra, y por eso el
resultado necesita un nombre nuevo (`Invertido`) en vez de reasignar. Datalog no llega ni a eso —sin
listas ni términos compuestos, la secuencia se representa como una relación `elem(posición, valor)`
y "invertir" es una regla que calcula `N - I + 1`—. Es exactamente lo que hace SQL: la tabla no tiene
orden intrínseco, existe una columna de posición, y darle la vuelta es un `ORDER BY` descendente. La
lección es que fuera de las familias imperativas el índice deja de ser una dirección de memoria y
pasa a ser un dato como cualquier otro.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres decisiones que los separan: si existe siquiera una
contraparte de tamaño fijo, si invertir **muta** o **copia**, y quién paga la memoria cuando la
estructura crece. Reconocer esas tres respuestas en un lenguaje que nunca has visto es lo
transferible.

⏮️ [Volver a la clase 090](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
