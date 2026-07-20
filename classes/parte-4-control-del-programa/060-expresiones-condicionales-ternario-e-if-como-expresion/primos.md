# 🧬 El mismo programa en las familias de lenguajes — Clase 060

> [⬅️ Volver a la clase 060](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el mayor de dos enteros escrito como una sola
expresión— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): dos enteros separados por espacio, `a b`
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** `max = (a > b) ? a : b` — una **expresión**, no una bifurcación con dos asignaciones

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

Esta es la clase donde el árbol genealógico se parte en dos ramas nítidas: los lenguajes que
heredaron el `?:` de C y los que hicieron del `if` una expresión y por eso nunca necesitaron un
operador aparte.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python se salió de la familia con su `a if cond else b`; el resto se repartió entre las dos ramas.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
puts "max=#{a > b ? a : b}"
```

### Perl

```perl
my ($x, $y) = split ' ', <STDIN>;
printf "max=%d\n", $x > $y ? $x : $y;
```

### Lua

```lua
-- Lua no tiene ternario: el modismo es `cond and v1 or v2`,
-- correcto solo mientras v1 no pueda ser nil ni false.
local a, b = io.read("l"):match("(-?%d+)%s+(-?%d+)")
a, b = tonumber(a), tonumber(b)
print("max=" .. (a > b and a or b))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
puts "max=[expr {$a > $b ? $a : $b}]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " +")[[1]])
# En R el `if` ya es una expresión; `ifelse()` existe pero es la versión vectorizada.
mx <- if (v[1] > v[2]) v[1] else v[2]
cat("max=", mx, "\n", sep = "")
```

**Qué reconocer:** Ruby, Perl y Tcl heredan el `?:` de C sin tocarlo. Lua **no lo tiene**, y su
comunidad usa `cond and v1 or v2`, un modismo que funciona por cortocircuito pero que se rompe en
silencio si `v1` vale `nil` o `false` —es el ejemplo canónico de un modismo que no es equivalente al
ternario, solo se le parece—. R está en el otro extremo: no necesita ternario porque su `if` ya
devuelve valor, y su `ifelse()` no es un ternario sino una función **vectorizada** que evalúa las dos
ramas enteras; confundirlas es un error clásico. Tcl recuerda su naturaleza: el `?:` no es del
lenguaje, es de `expr`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('max=${v[0] > v[1] ? v[0] : v[1]}');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra la expresión.
    public class Maximo {
        public static function mayor(a:int, b:int):String {
            return "max=" + (a > b ? a : b);
        }
    }
}
```

**Qué reconocer:** el ternario de C intacto, en el mismo sitio y con la misma precedencia baja que
obliga a los paréntesis al concatenar. Los tres de esta familia comparten además la escalera de
operadores derivados que nació aquí: `??` para el nulo y `?.` para el acceso seguro —Dart los tiene
desde el principio, JavaScript los adoptó tarde y ActionScript se quedó sin ellos—. Son ternarios
especializados: condicionales que caben en una expresión porque la condición está implícita.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java conservó el `?:`; sus primos lo tiraron.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    // Kotlin no tiene ternario: el `if` ya es una expresión y lo hace innecesario.
    println("max=${if (a > b) a else b}")
}
```

### Scala

```scala
object Maximo extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"max=${if (a > b) a else b}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "max=${a > b ? a : b}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))]
  ;; En Clojure TODO es expresión: `if` devuelve valor y no existe otra forma.
  (println (str "max=" (if (> a b) a b))))
```

**Qué reconocer:** aquí se ve la partición con toda claridad dentro de una misma máquina virtual.
Groovy conserva el `?:` de Java y añade el operador Elvis `?:` de dos posiciones (`a ?: b`, "a si es
verdadero, si no b"). Kotlin y Scala lo **eliminaron a propósito**: teniendo `if` como expresión, un
operador ternario sería una segunda forma de decir lo mismo. Clojure ni siquiera tuvo que decidirlo:
en un Lisp no existen las sentencias, todo formulario devuelve un valor, y `(if c a b)` es la única
construcción condicional que hay —el `cond` de la clase anterior está construido sobre ella—.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "max=%d" (if a > b then a else b)
```

### VB.NET

```vbnet
Module Maximo
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        ' If(cond, x, y) evalúa una sola rama; el viejo IIf() evaluaba las dos.
        Console.WriteLine("max=" & If(a > b, a, b))
    End Sub
End Module
```

**Qué reconocer:** C# tiene el `?:` de C; VB.NET, que viene de otra estirpe, lo escribe como una
**función de tres argumentos**: `If(cond, x, y)`. Y ahí guarda la mejor lección de esta clase: su
antecesor `IIf()` era una función de verdad, así que evaluaba **los dos brazos** antes de elegir —sin
cortocircuito, con sus efectos secundarios y sus divisiones por cero—. El `If()` moderno es sintaxis
del compilador precisamente para arreglarlo. F# va por el camino de Kotlin y Scala: no hay ternario
porque `if ... then ... else` ya es una expresión, con la condición añadida de que ambas ramas
tengan el mismo tipo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La cuna del `?:`, el único operador ternario del
lenguaje y el motivo de que su nombre coloquial sea "el ternario".

### C++

```cpp
#include <iostream>

int main() {
    long a, b;
    std::cin >> a >> b;
    std::cout << "max=" << (a > b ? a : b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        printf("max=%ld\n", a > b ? a : b);
    }
    return 0;
}
```

**Qué reconocer:** el mismo operador, byte por byte, en los dos superconjuntos de C. Lo que añade
cada uno es revelador: C++ convierte el ternario en una expresión que puede devolver una
**referencia** —`(c ? x : y) = 5` es código válido y asigna a una de las dos variables—, algo
impensable en C. Objective-C aporta el ternario abreviado de GCC, `a ?: b`, que devuelve `a` si es
verdadero y evalúa `a` una sola vez: el mismo Elvis de Groovy, veinte años antes y como extensión del
compilador. En ambos, `?:` cortocircuita: la rama no elegida **no se evalúa**.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos extremos: Go se
negó a tener ternario, Rust lo hizo innecesario.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    // Zig no tiene `?:`: el `if` es una expresión, igual que en Rust.
    try std.io.getStdOut().writer().print("max={d}\n", .{if (a > b) a else b});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
echo "max=", (if v[0] > v[1]: v[0] else: v[1])
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

void main() {
    auto v = readln().strip().split().map!(to!long).array;
    writefln("max=%d", v[0] > v[1] ? v[0] : v[1]);
}
```

**Qué reconocer:** D mantiene el `?:` de C sin cambios. Zig y Nim se alinean con Rust: `if` es una
expresión y por eso no hace falta un operador aparte —Nim conserva incluso los dos puntos de su
sintaxis por indentación dentro de la expresión—. El caso interesante es Go, el otro representante
del núcleo: **rechazó el ternario a propósito**, argumentando que se anida mal y se vuelve ilegible,
y tampoco hizo su `if` una expresión; el resultado es que Go es el único de los veinte que obliga a
escribir cuatro líneas para esto. Que el mismo problema de diseño tenga dos soluciones opuestas en la
misma familia es justo lo que esta página quiere mostrar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El `CASE WHEN` de SQL **es** una expresión
condicional: se puede poner donde quepa un valor.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    % `Cond -> Entonces ; Si_no` es lo más cercano a un ternario,
    % pero liga una variable en vez de devolver un valor.
    ( A > B -> Max = A ; Max = B ),
    format("max=~w~n", [Max]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni expresiones condicionales: los dos casos se declaran
% como reglas disjuntas y la "elección" la hace la derivación.
par(3, 7).

max(M) :- par(A, B), A > B, M = A.
max(M) :- par(A, B), A <= B, M = B.
```

**Qué reconocer:** Prolog tiene el `->` , que se lee como un ternario y hasta cortocircuita (descarta
los puntos de elección de la condición), pero **no es una expresión**: no devuelve un valor que
puedas incrustar en otro cálculo, sino que unifica una variable dentro de un objetivo. Esa distinción
—elegir un valor frente a elegir un camino de prueba— es la frontera real entre esta familia y todas
las anteriores. Datalog la cruza del todo: sin condicional, los dos casos se escriben como dos reglas
disjuntas, y hay que cerrar el segundo con `A <= B` porque no existe el "si no". SQL se quedó a
medias, y de ahí que su `CASE WHEN` —que sí es expresión y sí evalúa en orden— sea la pieza más
imperativa del lenguaje.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta de diseño detrás de todos: **¿el condicional
produce un valor o solo dirige el flujo?** Quien contestó "un valor" (Kotlin, Scala, Rust, Zig, F#,
Clojure, Nim, R) no necesitó ternario; quien contestó "solo dirige" tuvo que inventar el `?:` para
recuperar la expresión, y Go decidió vivir sin ninguna de las dos cosas. Eso es lo transferible.

⏮️ [Volver a la clase 060](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
