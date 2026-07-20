# 🧬 El mismo programa en las familias de lenguajes — Clase 046

> [⬅️ Volver a la clase 046](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —las tres operaciones lógicas básicas— resuelto por
los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes
del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, cada uno `0` o `1`
- **Salida** (stdout): `and=<true|false> or=<true|false> not_a=<true|false>`
- **Regla:** interpretando `a` y `b` como booleanos, `and = a ∧ b`, `or = a ∨ b`, `not_a = ¬a`

| stdin | esperado |
|---|---|
| `1 0` | `and=false or=true not_a=false` |
| `1 1` | `and=true or=true not_a=false` |
| `0 0` | `and=false or=false not_a=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí la pregunta interesante no es cómo se escribe el `and`, sino **qué considera falso cada
lenguaje**. La familia comparte la sintaxis; discrepa en la tabla de verdad implícita.

### Ruby

```ruby
a, b = STDIN.gets.split.map { |s| s.to_i != 0 }
puts "and=#{a && b} or=#{a || b} not_a=#{!a}"
```

### Perl

```perl
use strict;
use warnings;

# Perl no tiene tipo booleano: lo verdadero es 1 y lo falso la cadena vacía.
my ($x, $y) = map { $_ != 0 } split ' ', <STDIN>;
sub tf { $_[0] ? "true" : "false" }
printf "and=%s or=%s not_a=%s\n", tf($x && $y), tf($x || $y), tf(!$x);
```

### Lua

```lua
local a, b = io.read("n", "n")
-- Cuidado: en Lua el 0 es VERDADERO. Solo false y nil son falsos,
-- así que la conversión de número a booleano tiene que ser explícita.
local ba, bb = a ~= 0, b ~= 0
print(string.format("and=%s or=%s not_a=%s",
    tostring(ba and bb), tostring(ba or bb), tostring(not ba)))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
# Los operadores lógicos de Tcl devuelven 0 o 1, no true/false.
proc tf {v} { return [expr {$v ? "true" : "false"}] }
puts "and=[tf [expr {$a && $b}]] or=[tf [expr {$a || $b}]] not_a=[tf [expr {!$a}]]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
a <- v[1] != 0
b <- v[2] != 0
# R sí tiene tipo logical, pero lo imprime en mayúsculas (TRUE/FALSE).
tf <- function(x) if (x) "true" else "false"
cat(sprintf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a)))
```

**Qué reconocer:** los cinco escriben la lógica igual que Python, pero solo R tiene un tipo booleano
de primera clase —y lo imprime como `TRUE`—. Perl representa la verdad con `1` y la falsedad con la
cadena vacía; Tcl, con `1` y `0`; Lua tiene `true`/`false` de verdad pero considera **verdadero el
cero**, justo al revés que Python. Por eso el `!= 0` explícito no es adorno: es la línea que fija la
semántica.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.split(' ').map(int.parse).toList();
  final a = v[0] != 0;
  final b = v[1] != 0;
  print('and=${a && b} or=${a || b} not_a=${!a}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
package {
    public class Verdad {
        public static function evaluar(a:Boolean, b:Boolean):String {
            return "and=" + (a && b) + " or=" + (a || b) + " not_a=" + !a;
        }
    }
}
```

**Qué reconocer:** los dos heredan de JavaScript la conversión automática de `Boolean` a la cadena
`"true"` al concatenar o interpolar. Pero Dart rompe con el JavaScript clásico en un punto decisivo:
**no hay valores «truthy»**. Un `if (v[0])` sobre un entero es un error de compilación, mientras que
en JavaScript y en ActionScript sería válido y valdría `false` para el `0`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El `boolean` de la JVM es un tipo propio,
sin conversión a número ni desde número: la máquina virtual impone la disciplina a todos.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.split(" ").map { it.toInt() != 0 }
    println("and=${a && b} or=${a || b} not_a=${!a}")
}
```

### Scala

```scala
object Verdad extends App {
  val Array(a, b) = scala.io.StdIn.readLine().split(" ").map(_.toInt != 0)
  println(s"and=${a && b} or=${a || b} not_a=${!a}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().split(' ').collect { it.toInteger() != 0 }
println "and=${a && b} or=${a || b} not_a=${!a}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; En Clojure, igual que en Lua, el 0 es verdadero: solo false y nil son falsos.
(let [[a b] (map #(not= "0" %) (str/split (read-line) #" "))]
  (println (str "and=" (and a b) " or=" (or a b) " not_a=" (not a))))
```

**Qué reconocer:** los cuatro imprimen `true`/`false` en minúsculas porque acaban llamando al
`Boolean.toString` de Java. Kotlin, Scala y Groovy respetan el `boolean` estricto de la JVM. Clojure
es la excepción dentro de su propia máquina: reintroduce la noción de «valor falso» —solo `false` y
`nil`— y con ella la posibilidad de escribir `(if x ...)` sobre cualquier cosa, algo que Java
prohíbe.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| a; b |] = stdin.ReadLine().Split(' ') |> Array.map (fun s -> int s <> 0)
printfn "and=%b or=%b not_a=%b" (a && b) (a || b) (not a)
```

### VB.NET

```vbnet
Module Verdad
    Sub Main()
        Dim v = Console.ReadLine().Split(" "c)
        Dim a = Integer.Parse(v(0)) <> 0
        Dim b = Integer.Parse(v(1)) <> 0
        ' Boolean.ToString() del CLR devuelve "True"/"False": hay que bajarlo a minúsculas.
        Dim tfAnd = (a AndAlso b).ToString().ToLowerInvariant()
        Dim tfOr = (a OrElse b).ToString().ToLowerInvariant()
        Dim tfNot = (Not a).ToString().ToLowerInvariant()
        Console.WriteLine("and=" & tfAnd & " or=" & tfOr & " not_a=" & tfNot)
    End Sub
End Module
```

**Qué reconocer:** los tres comparten el mismo `System.Boolean` del CLR, y por eso comparten su
manía: `ToString()` devuelve `"True"` con mayúscula. F# lo esquiva porque su `printfn "%b"` es un
formateador propio del lenguaje que sí escribe en minúsculas. Fíjate además en `AndAlso`/`OrElse`:
VB.NET distingue por nombre el operador **cortocircuitado** del que evalúa siempre (`And`, `Or`),
una separación que en C# se hace con `&&` frente a `&`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C el booleano llegó tarde: hasta C99 la verdad
era simplemente «un entero distinto de cero».

### C++

```cpp
#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    const bool ba = a != 0, bb = b != 0;
    // std::boolalpha cambia la impresión de 1/0 a true/false.
    std::cout << std::boolalpha
              << "and=" << (ba && bb)
              << " or=" << (ba || bb)
              << " not_a=" << !ba << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// BOOL de Objective-C es un signed char con las macros YES/NO.
static const char *tf(BOOL v) { return v ? "true" : "false"; }

int main(void) {
    @autoreleasepool {
        int a, b;
        scanf("%d %d", &a, &b);
        BOOL ba = (a != 0), bb = (b != 0);
        printf("and=%s or=%s not_a=%s\n", tf(ba && bb), tf(ba || bb), tf(!ba));
    }
    return 0;
}
```

**Qué reconocer:** ambos parten del mismo hecho que C —cualquier entero no nulo es verdadero— y
cada uno lo viste a su manera. C++ añadió un `bool` real al lenguaje y un manipulador (`boolalpha`)
para imprimirlo con palabras; Objective-C se quedó en un `typedef` sobre `signed char` con `YES` y
`NO`, así que la traducción a `"true"`/`"false"` sigue siendo trabajo del programador.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Booleano estricto, sin
conversión implícita desde entero, y condicionales que exigen exactamente un `bool`.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = (try std.fmt.parseInt(i32, it.next().?, 10)) != 0;
    const b = (try std.fmt.parseInt(i32, it.next().?, 10)) != 0;
    try std.io.getStdOut().writer().print("and={} or={} not_a={}\n", .{ a and b, a or b, !a });
}
```

### Nim

```nim
import std/[strutils, strformat]

let v = stdin.readLine().splitWhitespace()
let a = parseInt(v[0]) != 0
let b = parseInt(v[1]) != 0
echo &"and={a and b} or={a or b} not_a={not a}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!int).array;
    const a = v[0] != 0;
    const b = v[1] != 0;
    writefln("and=%s or=%s not_a=%s", a && b, a || b, !a);
}
```

**Qué reconocer:** los tres tienen un `bool` que no es un número, igual que Go y Rust. Zig y Nim
llegan a usar las **palabras** `and`, `or`, `not` en vez de los símbolos, herencia de Pascal y de
Python respectivamente; D conserva los `&&` y `||` de C. Y los tres formatean el booleano como
`true`/`false` sin pedirlo, porque su tipo sabe imprimirse solo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la verdad no es un valor que se guarda en
una variable: es el hecho de que algo **se pueda demostrar**.

### Prolog

```prolog
:- initialization(main, main).

verdad(0, false).
verdad(1, true).

conj(true, true, true) :- !.
conj(_, _, false).

disy(false, false, false) :- !.
disy(_, _, true).

neg(true, false).
neg(false, true).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    number_string(NA, SA),
    number_string(NB, SB),
    verdad(NA, A),
    verdad(NB, B),
    conj(A, B, And),
    disy(A, B, Or),
    neg(A, NotA),
    format("and=~w or=~w not_a=~w~n", [And, Or, NotA]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni tipo booleano: la entrada se declara como hechos
% y "ser verdadero" se representa por la PRESENCIA del hecho, no por un valor.
a(1).
b(0).

cierto_a :- a(1).
cierto_b :- b(1).

resultado_and :- cierto_a, cierto_b.
resultado_or :- cierto_a.
resultado_or :- cierto_b.

% La negación no es lógica pura: exige la extensión de negación estratificada,
% que asume que lo no demostrable es falso (hipótesis de mundo cerrado).
resultado_not_a :- not cierto_a.
```

**Qué reconocer:** en Prolog `true` y `false` son **átomos corrientes**, no un tipo del lenguaje; la
tabla de verdad se escribe como hechos y reglas, exactamente igual que se escribiría cualquier otra
relación. Datalog lleva la idea al extremo: no hay valor booleano en absoluto, solo hechos que se
derivan o no se derivan. Fíjate en que el `resultado_or` necesita **dos reglas** —una por cada
disyunto— y que la negación tiene que pedirse como extensión, porque negar algo en lógica pura
significa demostrar que nunca podrá derivarse. Es el mismo territorio incómodo del `NULL` de SQL,
donde `NOT NULL` tampoco es `TRUE`.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer dos números, decidir qué
significa «verdadero», combinar y escribir la respuesta. Lo que cambia es la **forma** y, en algunos
casos, las **garantías**. Eso es lo transferible.

⏮️ [Volver a la clase 046](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
