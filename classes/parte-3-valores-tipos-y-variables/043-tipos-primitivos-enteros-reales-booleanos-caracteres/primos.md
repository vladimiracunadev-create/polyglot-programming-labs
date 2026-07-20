# 🧬 El mismo programa en las familias de lenguajes — Clase 043

> [⬅️ Volver a la clase 043](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —mostrar un número como entero, como real y como
propiedad booleana— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `n` (un entero)
- **Salida** (stdout): `entero=<n> real=<n con 1 decimal> par=<true|false>`
- **Regla:** `real = (double) n` y `par = (n módulo 2 == 0)`

| stdin | esperado |
|---|---|
| `4` | `entero=4 real=4.0 par=true` |
| `7` | `entero=7 real=7.0 par=false` |
| `0` | `entero=0 real=0.0 par=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El tipo vive en el **valor**, no en la variable. La pregunta interesante es cuántos tipos primitivos
distingue realmente cada lenguaje.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "entero=#{n} real=#{format('%.1f', n)} par=#{n.even?}"
```

### Perl

```perl
# Perl no tiene tipo booleano: la verdad es un escalar, se traduce a mano.
my $n = <STDIN>;
chomp $n;
printf "entero=%d real=%.1f par=%s\n", $n, $n, ($n % 2 == 0 ? "true" : "false");
```

### Lua

```lua
local n = io.read("n")
local par = n % 2 == 0
print(string.format("entero=%d real=%.1f par=%s", n, n, tostring(par)))
```

### Tcl

```tcl
# En Tcl todo es cadena: el tipo lo decide el comando que consume el valor.
gets stdin n
set par [expr {$n % 2 == 0 ? "true" : "false"}]
puts "entero=$n real=[format %.1f $n] par=$par"
```

### R

```r
n <- scan("stdin", what = integer(), n = 1, quiet = TRUE)
# R escribe los lógicos como TRUE/FALSE: hay que pasarlos a minúscula.
par <- tolower(as.character(n %% 2 == 0))
cat(sprintf("entero=%d real=%.1f par=%s\n", n, n, par))
```

**Qué reconocer:** en los cinco el mismo dato pasa de entero a real sin decirlo en ninguna
declaración: basta con pedir `%.1f` al formatear. Y en los cinco el booleano es el tipo más frágil.
Perl no lo tiene —usa el 0, la cadena vacía y `undef` como falsos—, Tcl representa la verdad con las
cadenas `0` y `1`, y R sí tiene `TRUE`/`FALSE` pero **en mayúsculas**, así que el contrato obliga a
traducir. Ruby y Lua son los únicos con un `true`/`false` que ya sale escrito como el resto del
mundo lo escribe.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final real = n.toDouble();
  print('entero=$n real=${real.toStringAsFixed(1)} par=${n.isEven}');
}
```

### ActionScript 3

```actionscript
package {
    // Sin stdin en el reproductor Flash: se ilustra el tríptico de tipos primitivos.
    public class Primitivos {
        public static function describir(n:int):String {
            var real:Number = n;
            var par:Boolean = (n % 2 == 0);
            return "entero=" + n + " real=" + real.toFixed(1) + " par=" + par;
        }
    }
}
```

**Qué reconocer:** aquí está la diferencia más grande con JavaScript, y conviene verla bien.
JavaScript tiene **un solo tipo numérico** (`number`, un doble de 64 bits); Dart y ActionScript
recuperan la distinción `int` / `double`-`Number` que la clase da por sentada, y por eso `toDouble()`
y la conversión implícita `var real:Number = n` significan algo real. `toFixed(1)` es literalmente el
mismo método de JavaScript, y el `Boolean` de AS3 se concatena como `"true"`/`"false"` sin ayuda.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM define ocho tipos primitivos y todos
los lenguajes de la familia acaban usándolos, aunque los envuelvan en otra sintaxis.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val real = n.toDouble()
    val par = n % 2 == 0
    println("entero=$n real=%.1f par=$par".format(real))
}
```

### Scala

```scala
object Primitivos extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val real = n.toDouble
  println(f"entero=$n real=$real%.1f par=${n % 2 == 0}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
printf("entero=%d real=%.1f par=%b%n", n, n as double, n % 2 == 0)
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (parse-long (str/trim (read-line)))]
  (println (format "entero=%d real=%.1f par=%b" n (double n) (even? n))))
```

**Qué reconocer:** los cuatro terminan llamando a `String.format` de Java, por eso `%.1f` y `%b`
aparecen intactos. La conversión de entero a real es **explícita** en todos —`toDouble`, `as double`,
`double`— porque la JVM no la hace sola al pasar un argumento. En Kotlin y Scala los primitivos no
existen como tipo aparte en el código fuente: escribes `Int` y `Double` con mayúscula, y el
compilador decide si emite un primitivo o su envoltorio. Clojure ni siquiera nombra el tipo: `even?`
es una pregunta sobre el valor.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let real = float n
printfn "entero=%d real=%.1f par=%b" n real (n % 2 = 0)
```

### VB.NET

```vbnet
Imports System.Globalization

Module Primitivos
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim real As Double = n
        Dim par As Boolean = (n Mod 2 = 0)

        ' Boolean.ToString() devuelve "True": el contrato pide minúscula.
        Dim texto = real.ToString("F1", CultureInfo.InvariantCulture)
        Console.WriteLine($"entero={n} real={texto} par={par.ToString().ToLowerInvariant()}")
    End Sub
End Module
```

**Qué reconocer:** `Integer`, `Double` y `Boolean` de VB.NET son alias de `System.Int32`,
`System.Double` y `System.Boolean`, los mismos que C# llama `int`, `double` y `bool`: tres nombres,
un solo tipo del CLR. De ahí la trampa que se ve en el código —`True` con mayúscula al convertir a
texto, y `CultureInfo.InvariantCulture` para que el separador decimal no se vuelva coma—. F# usa `=`
tanto para comparar como para ligar, y su `%b` imprime el booleano ya en minúscula.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Los tipos se declaran, ocupan un tamaño conocido y
el booleano es un recién llegado.

### C++

```cpp
#include <iostream>
#include <iomanip>

int main() {
    long n;
    std::cin >> n;
    std::cout << "entero=" << n
              << " real=" << std::fixed << std::setprecision(1) << static_cast<double>(n)
              << " par=" << std::boolalpha << (n % 2 == 0) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;

        /* BOOL de Objective-C es un entero de 8 bits, no un tipo aparte. */
        BOOL par = (n % 2 == 0);
        printf("entero=%ld real=%.1f par=%s\n", n, (double) n, par ? "true" : "false");
    }
    return 0;
}
```

**Qué reconocer:** en los dos la conversión de entero a real es un **cast** visible
(`static_cast<double>`, `(double)`), que es exactamente el gesto que la clase enseña en C. La
diferencia está en el booleano: C++ tiene un tipo `bool` de verdad y `std::boolalpha` lo escribe
`true`/`false` sin traducción; Objective-C conserva la costumbre de C —`BOOL` es un `signed char`
con `YES` y `NO`— y por eso hay que elegir la cadena a mano.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Tipos con tamaño en el
nombre y ninguna conversión gratuita.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    const real: f64 = @floatFromInt(n);
    const par = @rem(n, 2) == 0;
    try std.io.getStdOut().writer().print("entero={d} real={d:.1} par={}\n", .{ n, real, par });
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
echo "entero=", n, " real=", formatFloat(n.float, ffDecimal, 1), " par=", n mod 2 == 0
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    writefln("entero=%d real=%.1f par=%s", n, cast(double) n, n % 2 == 0);
}
```

**Qué reconocer:** los tres nombran el tamaño en el tipo —`i64`/`f64`, `int`/`float`, `long`/`double`—
igual que Rust escribe `i32` y `f64`. Zig es el más severo de toda esta página: convertir entero a
real no se hace con un cast sino con una función explícita, `@floatFromInt`, porque el lenguaje se
niega a que una conversión con pérdida pase desapercibida. Los tres, en cambio, imprimen el booleano
como `true`/`false` sin pedir nada especial: `bool` es un tipo primitivo de pleno derecho.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no cómo
calcularlo.

### Prolog

```prolog
:- initialization(main, main).

% En Prolog la verdad no es un valor sino el éxito o el fracaso de una consulta:
% para imprimir "true"/"false" hay que fabricar el átomo a mano.
main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    Real is float(N),
    ( 0 is N mod 2 -> Par = true ; Par = false ),
    format("entero=~d real=~1f par=~w~n", [N, Real, Par]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni reales: la "verdad" es que el hecho se pueda derivar o no.
numero(4).

par(N) :- numero(N), N % 2 = 0.
```

**Qué reconocer:** esta familia pone el dedo en la llaga del tipo booleano. En Prolog no hay
`true`/`false` como valores que se calculan: hay objetivos que **tienen éxito o fallan**, y el
`->` del código convierte esa distinción del motor en un átomo imprimible. Datalog es aún más
radical —no existe la salida, ni el tipo real, ni siquiera la negación en su forma pura—: la única
respuesta posible es qué hechos pertenecen a la relación `par`. Es la misma renuncia de SQL, donde
`WHERE` filtra filas en vez de devolverte un booleano suelto.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas a la pregunta "¿cuántos tipos
primitivos hay aquí?". El entero y el real se distinguen casi en todas partes; el booleano es el que
delata la edad y el paradigma del lenguaje. Eso es lo transferible.

⏮️ [Volver a la clase 043](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
