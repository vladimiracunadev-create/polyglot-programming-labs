# 🧬 El mismo programa en las familias de lenguajes — Clase 052

> [⬅️ Volver a la clase 052](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el producto de dos enteros— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, dos enteros
- **Salida** (stdout): `producto=<a*b>`
- **Regla:** `producto = a * b`

| stdin | esperado |
|---|---|
| `3 4` | `producto=12` |
| `0 9` | `producto=0` |
| `-2 5` | `producto=-10` |

El programa es trivial a propósito. Lo que hay que mirar en cada bloque no es el cálculo, sino
**cuántas veces aparece escrita la palabra `int`** y quién la pone cuando no aparece.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En esta familia no hay inferencia porque no hay nada que inferir: no existe la anotación de tipo en
la variable.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
puts "producto=#{a * b}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
printf "producto=%d\n", $a * $b;
```

### Lua

```lua
local a, b = io.read("n", "n")
print(string.format("producto=%d", a * b))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
puts "producto=[expr {$a * $b}]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("producto=%d\n", v[1] * v[2]))
```

**Qué reconocer:** ningún bloque nombra un tipo, pero eso **no es inferencia**: es ausencia de
declaración. La diferencia importa. En un lenguaje con inferencia el tipo existe, está fijado y el
compilador lo conoce aunque tú no lo escribas; aquí el tipo viaja con el valor y puede cambiar en la
línea siguiente. Es la confusión más común de esta clase y estos cinco bloques son la prueba visual.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
TypeScript es probablemente el motor de inferencia más usado del mundo, y esta familia enseña cómo se
llega a él.

### Dart

```dart
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.split(' '); // p: List<String>, inferido
  final a = int.parse(p[0]);                  // a: int, inferido del retorno
  final b = int.parse(p[1]);
  print('producto=${a * b}');                 // a * b: int, inferido del operador
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
    // AS3 NO infiere: una `var` sin anotación no es "int deducido", es el
    // tipo comodín `*`, que desactiva la comprobación estática de esa variable.
    public class Producto {
        public static function calcular(a:int, b:int):String {
            var p:int = a * b;
            return "producto=" + p;
        }
    }
}
```

**Qué reconocer:** Dart infiere de derecha a izquierda —el tipo sale de la expresión que inicializa,
igual que en TypeScript— y por eso `final` y `var` bastan casi siempre. ActionScript 3 es el
contraejemplo perfecto dentro de la misma familia: omitir el tipo allí no significa "dedúcelo",
significa "no lo compruebes". Escribir menos no siempre es inferir.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó veinte años en aceptar `var` (Java
10); sus primos nacieron con inferencia desde el primer día.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.split(" ").map { it.toInt() }
    println("producto=${a * b}")
}
```

### Scala

```scala
object Producto extends App {
  val Array(a, b) = scala.io.StdIn.readLine().split(" ").map(_.toInt)
  println(s"producto=${a * b}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().split(' ')*.toInteger()
println "producto=${a * b}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "producto=" (* a b))))
```

**Qué reconocer:** en Kotlin y Scala no aparece ni un tipo, pero `a` y `b` son `Int` fijos y
comprobados: la inferencia atraviesa el `split`, el `map` y la desestructuración. Clojure y Groovy
llegan a un código casi idéntico por el camino opuesto —no infieren nada, resuelven en ejecución—.
La lección es que **el aspecto del código no te dice si hay inferencia**; hay que saber qué lenguaje
estás leyendo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). C# introdujo `var` en 2007 y desde entonces la
inferencia local es la norma en la plataforma.

### F\#

```fsharp
// Ni una sola anotación en todo el programa: F# usa inferencia Hindley-Milner,
// que deduce los tipos de la función entera, no solo de las variables locales.
let partes = stdin.ReadLine().Split(' ')
let a = int partes.[0]
let b = int partes.[1]
printfn "producto=%d" (a * b)
```

### VB.NET

```vbnet
Module Producto
    ' Option Infer On (por defecto en proyectos nuevos) permite `Dim` sin `As`.
    ' Con Option Infer Off, ese mismo `Dim` daría un Object: la misma línea
    ' significa dos cosas distintas según un ajuste del proyecto.
    Sub Main()
        Dim p = Console.ReadLine().Split(" "c)
        Dim a = Integer.Parse(p(0))
        Dim b = Integer.Parse(p(1))
        Console.WriteLine("producto=" & a * b)
    End Sub
End Module
```

**Qué reconocer:** los tres llegan a `Int32` sin escribirlo, pero F# es de otra categoría. `var` de
C# y `Dim` de VB.NET solo miran la expresión de la derecha; el motor de F# resuelve un sistema de
ecuaciones sobre todo el programa y puede deducir el tipo de un parámetro por cómo se usa dentro del
cuerpo. Es la inferencia de la familia ML, la misma de Haskell y OCaml.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C todo tipo se escribe; sus descendientes fueron
añadiendo formas de callarlo.

### C++

```cpp
#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    // `auto` (C++11) deduce int del tipo de la expresión, igual que `var` en C#.
    const auto producto = a * b;
    std::cout << "producto=" << producto << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int a, b;
        scanf("%d %d", &a, &b);
        // `__auto_type` es una extensión de Clang: Objective-C no trae
        // inferencia en el estándar, así que lo normal es escribir `int`.
        __auto_type producto = a * b;
        printf("producto=%d\n", producto);
    }
    return 0;
}
```

**Qué reconocer:** `auto` en C++ no inventó nada nuevo, solo dejó de obligarte a repetir lo que el
compilador ya sabía —su valor real se ve con iteradores, donde el tipo escrito ocuparía tres
líneas—. Objective-C se quedó fuera de esa evolución y depende de una extensión del compilador;
Swift, su sucesor, nació con inferencia completa. Es la misma línea evolutiva de C a `auto` que
recorrió toda la familia de las llaves.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go infiere con `:=` y
Rust con `let`, pero los dos frenan en la frontera de la función.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    // `const a` deduce el tipo del resultado, pero fíjate en que `i64` hay que
    // dárselo a parseInt: Zig nunca infiere hacia atrás, desde el destino.
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try std.io.getStdOut().writer().print("producto={d}\n", .{a * b});
}
```

### Nim

```nim
import std/strutils

let p = stdin.readLine().splitWhitespace()
let a = parseInt(p[0])   # int, deducido del retorno de parseInt
let b = parseInt(p[1])
echo "producto=", a * b
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!int).array;
    auto producto = v[0] * v[1];
    writefln("producto=%d", producto);
}
```

**Qué reconocer:** los tres infieren la variable local a partir de la expresión, exactamente como el
`:=` de Go. Y los tres marcan el mismo límite que Rust: **la firma de una función siempre lleva los
tipos escritos**, porque es el contrato público del código. La inferencia de esta familia es una
comodidad dentro del cuerpo, no un sustituto de la declaración.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL sí infiere —el tipo de una columna calculada
lo deduce el motor del esquema y de la operación—, y sus primos lo llevan al extremo de no tener
tipos que inferir.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    % No hay tipos, luego no hay inferencia: `A` y `B` son variables lógicas
    % que se ligan a lo que llegue, y `is` falla en ejecución si no es número.
    number_string(A, SA),
    number_string(B, SB),
    Producto is A * B,
    format("producto=~w~n", [Producto]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: se declara el hecho y la regla que deriva el producto.
% El único "tipo" de un predicado es su aridad, y esa sí la deduce el motor.
entrada(3, 4).

producto(P) :- entrada(A, B), P = A * B.
```

**Qué reconocer:** Prolog es el límite inferior de esta clase: sin declaración y sin inferencia, solo
comprobación al ejecutar. Sin embargo, sus dialectos con tipos —Mercury, o los `:- pred` de algunos
sistemas— sí infieren modos y tipos, señal de que la idea es tan útil que acaba apareciendo en todas
partes. SQL es el recordatorio de que el motor infiere el tipo de `a * b` sin que nadie lo pida.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y un mismo malentendido a evitar: **no escribir el tipo no
significa no tener tipo**. En Kotlin, F# o Rust el tipo está fijado y comprobado aunque no aparezca;
en Ruby o Tcl no aparece porque no existe hasta que el valor llega. Distinguir esas dos ausencias es
lo transferible.

⏮️ [Volver a la clase 052](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
