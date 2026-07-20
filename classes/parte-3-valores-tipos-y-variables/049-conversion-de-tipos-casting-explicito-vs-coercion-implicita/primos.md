# 🧬 El mismo programa en las familias de lenguajes — Clase 049

> [⬅️ Volver a la clase 049](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —pasar de texto a real, y de real a entero— resuelto
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

- **Entrada** (stdin): un número real escrito como texto
- **Salida** (stdout): `entero=<parte entera truncada> real=<valor con 2 decimales>`
- **Regla:** `entero = truncar(real)`, y el real se formatea con dos decimales

| stdin | esperado |
|---|---|
| `3.7` | `entero=3 real=3.70` |
| `5.0` | `entero=5 real=5.00` |
| `8.9` | `entero=8 real=8.90` |

Dos conversiones en tres líneas: una de **texto a número** y otra de **real a entero**. La segunda
esconde la trampa: truncar no es redondear, y no todos los lenguajes eligen lo mismo por defecto.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí conviven los dos extremos del curso: lenguajes que convierten texto en número **sin que se lo
pidas** (Perl, Tcl) y lenguajes que exigen decirlo (Python).

### Ruby

```ruby
f = STDIN.gets.to_f
# to_i trunca hacia cero; round() redondearía. Ruby NO coacciona sola:
# "3" + 1 es un error de tipo, al contrario que en Perl.
puts "entero=#{f.to_i} real=#{format('%.2f', f)}"
```

### Perl

```perl
use strict;
use warnings;

my $f = <STDIN>;
# Perl es el rey de la coerción implícita: el mismo escalar es texto o número
# según el operador que lo toque. int() trunca hacia cero, no redondea.
printf "entero=%d real=%.2f\n", int($f), $f;
```

### Lua

```lua
local f = io.read("n")
-- Ojo: math.floor redondea hacia ABAJO, no hacia cero. Para los casos
-- positivos de la clase coincide con truncar; para -3.7 daría -4, no -3.
-- Desde Lua 5.3 existen enteros reales y math.tointeger.
print(string.format("entero=%d real=%.2f", math.floor(f), f))
```

### Tcl

```tcl
gets stdin linea
# En Tcl todo es cadena: double() e int() son funciones de expr, no casts.
set f [expr {double($linea)}]
puts "entero=[expr {int($f)}] real=[format %.2f $f]"
```

### R

```r
f <- as.numeric(readLines("stdin", n = 1))
# as.integer() trunca hacia cero; round() usa redondeo al par más cercano.
cat(sprintf("entero=%d real=%.2f\n", as.integer(f), f))
```

**Qué reconocer:** los cinco escriben la conversión con una llamada explícita, igual que el `int()`
de Python, pero la diferencia real está en lo que pasa **sin llamarla**. En Perl `"3.7" * 2` vale
`7.4` sin protestar; en Ruby, `"3.7" * 2` devuelve `"3.73.7"` porque el `*` de cadena repite. Y
atención a la trampa de Lua: `math.floor` no es truncar, y solo coincide con el `int()` de Python
mientras el número sea positivo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final f = double.parse(stdin.readLineSync()!.trim());
  // int y double no se convierten solos en Dart: truncate() es obligatorio.
  print('entero=${f.truncate()} real=${f.toStringAsFixed(2)}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
package {
    public class Conversion {
        public static function convertir(s:String):String {
            var f:Number = parseFloat(s);
            // int() trunca hacia cero, igual que el Math.trunc de JavaScript.
            return "entero=" + int(f) + " real=" + f.toFixed(2);
        }
    }
}
```

**Qué reconocer:** ActionScript es JavaScript con tipos declarados, y arrastra su coerción: el `+`
concatena si un operando es cadena, y por eso `"entero=" + int(f)` funciona sin conversión explícita.
Dart cortó justamente con eso. Su `int` y su `double` son tipos distintos que **no se mezclan**, no
existe la conversión implícita en el `+`, y por tanto la interpolación es la única forma limpia de
pegar un número a un texto. Es la misma corrección que hizo TypeScript sobre JavaScript, pero
llevada al tiempo de ejecución.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM sí tiene coerción implícita, pero solo
en la dirección segura: `int` sube a `double` solo; bajar de `double` a `int` exige un `cast`.

### Kotlin

```kotlin
fun main() {
    val f = readLine()!!.trim().toDouble()
    // Kotlin eliminó incluso las conversiones ampliadoras implícitas de Java:
    // un Int NO se asigna a un Double sin toDouble(). toInt() trunca hacia cero.
    println("entero=${f.toInt()} real=${"%.2f".format(f)}")
}
```

### Scala

```scala
object Conversion extends App {
  val f = scala.io.StdIn.readLine().trim.toDouble
  println(f"entero=${f.toInt}%d real=$f%.2f")
}
```

### Groovy

```groovy
def f = System.in.newReader().readLine().trim() as double
// Groovy resucita la coerción dinámica sobre la JVM: `as` convierte casi cualquier cosa.
printf("entero=%d real=%.2f%n", (int) f, f)
```

### Clojure

```clojure
;; (long f) trunca hacia cero; (Math/round f) redondearía.
(let [f (Double/parseDouble (clojure.string/trim (read-line)))]
  (println (format "entero=%d real=%.2f" (long f) f)))
```

**Qué reconocer:** los cuatro truncan hacia cero porque abajo hay una única instrucción de bytecode,
`d2i`, y esa instrucción trunca. Lo que cambia es cuánto te obligan a escribirlo. Kotlin es el más
estricto de todos —más incluso que Java, porque prohíbe también las conversiones ampliadoras
automáticas—, mientras que Groovy va al extremo contrario y recupera con `as` una coerción de
lenguaje dinámico. Misma máquina virtual, filosofías opuestas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// F# no admite NINGUNA conversión implícita, ni siquiera int → float:
// `int` y `float` son funciones que hay que escribir. `int` trunca hacia cero.
let f = float (stdin.ReadLine().Trim())
printfn "entero=%d real=%.2f" (int f) f
```

### VB.NET

```vbnet
Imports System.Globalization

Module Conversion
    Sub Main()
        Dim f = Double.Parse(Console.ReadLine().Trim(), CultureInfo.InvariantCulture)
        ' Trampa clásica de VB: CInt() REDONDEA al par más cercano (CInt(3.5) = 4,
        ' CInt(2.5) = 2). El que trunca hacia cero es Fix().
        Dim entero As Long = CLng(Fix(f))
        Console.WriteLine("entero=" & entero & " real=" & f.ToString("F2", CultureInfo.InvariantCulture))
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR y comparten `Double` y `CultureInfo` —esa cultura
invariante es imprescindible aquí, porque en configuración regional española el separador decimal es
la coma y `Parse` fallaría—. Pero cada uno resuelve la conversión a entero de forma distinta: C# usa
un cast que trunca, F# una función que trunca, y VB.NET arrastra del BASIC clásico una pareja
peligrosa donde `CInt` **redondea** y solo `Fix` trunca. Es exactamente el tipo de detalle que hace
que un programa traducido «token a token» dé otro resultado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La conversión de `double` a `int` está definida por
el estándar: descarta la parte fraccionaria, es decir, trunca hacia cero.

### C++

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double f;
    std::cin >> f;
    // La conversión sería implícita, pero static_cast la deja a la vista
    // y avisa al compilador de que la pérdida de precisión es intencionada.
    std::cout << "entero=" << static_cast<int>(f)
              << " real=" << std::fixed << std::setprecision(2) << f << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        double f;
        scanf("%lf", &f);
        // El cast al estilo C, idéntico al de la implementación de la clase.
        printf("entero=%d real=%.2f\n", (int)f, f);
    }
    return 0;
}
```

**Qué reconocer:** los dos aceptan el cast `(int)f` de C sin cambios, así que la implementación de la
clase compila tal cual en ambos. C++ añade `static_cast`, que hace lo mismo pero es **buscable** y
no puede confundirse con las conversiones peligrosas (`reinterpret_cast`, `const_cast`); es una
mejora de legibilidad, no de semántica. Objective-C no tocó nada de esto: su capa de objetos se monta
encima, sin alterar la aritmética heredada.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno de los dos
convierte nada solo: cada cambio de tipo se escribe, y por eso las conversiones son fáciles de
auditar.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const f = try std.fmt.parseFloat(f64, std.mem.trim(u8, linea, " \r\n"));
    // Zig prohíbe toda conversión con pérdida silenciosa: @intFromFloat es
    // obligatorio y trunca hacia cero. El tipo destino lo fija la declaración.
    const entero: i64 = @intFromFloat(f);
    try std.io.getStdOut().writer().print("entero={d} real={d:.2}\n", .{ entero, f });
}
```

### Nim

```nim
import std/[strutils, strformat]

# Nim sí convierte int → float solo, pero NUNCA float → int: int() es explícito y trunca.
let f = parseFloat(stdin.readLine().strip())
echo &"entero={int(f)} real={f:.2f}"
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const f = readln().strip().to!double;
    // Cuidado con el par de D: to!int REDONDEA y lanza si no cabe;
    // cast(int) es el que trunca hacia cero, como en C.
    writefln("entero=%d real=%.2f", cast(int) f, f);
}
```

**Qué reconocer:** los tres exigen escribir la conversión que pierde información, igual que el
`as i64` de Rust y el `int(f)` de Go. Zig es el más radical: no hay cast genérico, hay funciones
integradas con nombre (`@intFromFloat`, `@floatFromInt`) que dicen exactamente qué se está haciendo.
Y D repite aquí la trampa que ya vimos en VB.NET: dos formas de convertir que **no dan el mismo
resultado**, `to!int` redondeando y `cast(int)` truncando.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La conversión se pide como una operación sobre
un valor de la relación (`CAST`), no como un cambio de la variable.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    % number_string convierte texto a número y funciona en ambas direcciones.
    number_string(F, Linea),
    % `is` fuerza la evaluación aritmética; truncate/1 corta hacia cero.
    Entero is truncate(F),
    format("entero=~d real=~2f~n", [Entero, F]).
```

### Datalog

```datalog
% Datalog puro no tiene aritmética de conversión, funciones ni formateo de salida:
% no existe un truncate. El par (real, parte entera) tiene que declararse como hecho.
medida(3.7, 3).
medida(5.0, 5).
medida(8.9, 8).

entrada(3.7).

resultado(R, E) :- entrada(R), medida(R, E).
```

**Qué reconocer:** Prolog separa dos cosas que en los lenguajes imperativos van juntas. `F = 3+4`
**no** vale 7: unifica `F` con el término literal `3+4`; hace falta `is` para pedir que se evalúe. Esa
distinción entre *término* y *valor calculado* es la razón de que la conversión de tipos en Prolog se
vea siempre alrededor de un `is`. Datalog no llega ni a tener aritmética —cualquier función
convertiría el lenguaje en algo que ya no garantiza terminar—, y esa renuncia es la misma que hace
SQL al no dejarte escribir bucles.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer texto, volverlo número,
recortarlo a entero y formatearlo con dos decimales. Lo que cambia es la **forma** y, en algunos
casos, las **garantías**. Eso es lo transferible.

⏮️ [Volver a la clase 049](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
