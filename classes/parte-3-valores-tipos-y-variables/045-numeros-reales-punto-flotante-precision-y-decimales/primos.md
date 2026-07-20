# 🧬 El mismo programa en las familias de lenguajes — Clase 045

> [⬅️ Volver a la clase 045](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar y multiplicar dos reales y mostrarlos con dos
decimales— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos reales)
- **Salida** (stdout): `suma=<a+b con 2 decimales> producto=<a*b con 2 decimales>`
- **Regla:** `suma = a + b` y `producto = a * b`, ambos redondeados a dos decimales

| stdin | esperado |
|---|---|
| `1.5 2.5` | `suma=4.00 producto=3.75` |
| `0.1 0.2` | `suma=0.30 producto=0.02` |
| `10 3` | `suma=13.00 producto=30.00` |

El segundo caso es el famoso `0.1 + 0.2`, que en binario **no** da exactamente `0.3`. Que los veinte
programas impriman `0.30` no significa que el cálculo sea exacto: significa que el redondeo a dos
decimales tapa el error. Ese es el tema de la clase.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Un solo tipo real, doble precisión IEEE 754, y el formateo hecho con la misma familia de `%.2f` que
heredaron de C.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_f)
puts format("suma=%.2f producto=%.2f", a + b, a * b)
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
printf "suma=%.2f producto=%.2f\n", $a + $b, $a * $b;
```

### Lua

```lua
local a, b = io.read("n", "n")
print(string.format("suma=%.2f producto=%.2f", a + b, a * b))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
puts [format "suma=%.2f producto=%.2f" [expr {$a + $b}] [expr {$a * $b}]]
```

### R

```r
v <- scan("stdin", what = numeric(), n = 2, quiet = TRUE)
cat(sprintf("suma=%.2f producto=%.2f\n", v[1] + v[2], v[1] * v[2]))
```

**Qué reconocer:** los cinco usan `double` de 64 bits sin decirlo y arrastran por tanto la misma
imprecisión: en los cinco, `0.1 + 0.2 == 0.3` es **falso**. Perl y Lua ni siquiera distinguen entero
de real al leer —el escalar de Perl es el ejemplo extremo—, mientras que Tcl vuelve a mostrar su
naturaleza de cadenas: el texto solo se convierte en número dentro de `expr`. R, fiel a su origen,
opera sobre un vector de dos posiciones en vez de dos variables.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(double.parse).toList();
  final suma = v[0] + v[1];
  final producto = v[0] * v[1];
  print('suma=${suma.toStringAsFixed(2)} producto=${producto.toStringAsFixed(2)}');
}
```

### ActionScript 3

```actionscript
package {
    // Sin stdin en el reproductor Flash: se ilustra el cálculo y el redondeo.
    public class Reales {
        public static function operar(a:Number, b:Number):String {
            return "suma=" + (a + b).toFixed(2)
                + " producto=" + (a * b).toFixed(2);
        }
    }
}
```

**Qué reconocer:** `toStringAsFixed` y `toFixed` son el mismo método que usa la versión de
JavaScript, y `Number` de ActionScript es exactamente el `number` de JavaScript: un doble IEEE 754,
sin tipo entero separado. Dart es la excepción de la familia —tiene `int` y `double` como tipos
distintos—, y por eso aquí hay que pedir `double.parse` de forma explícita en vez de dejar que el
lenguaje decida. Todos redondean a dos decimales **solo al imprimir**: el valor guardado sigue
siendo el binario imperfecto.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Mismo `double`, misma `String.format`… y la
misma trampa regional.

### Kotlin

```kotlin
import java.util.Locale

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toDouble() }
    println("suma=%.2f producto=%.2f".format(Locale.ROOT, a + b, a * b))
}
```

### Scala

```scala
object Reales extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toDouble)
  println(f"suma=${a + b}%.2f producto=${a * b}%.2f")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toDouble()
println String.format(Locale.ROOT, "suma=%.2f producto=%.2f", a + b, a * b)
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map parse-double (str/split (str/trim (read-line)) #"\s+"))]
  (println (format "suma=%.2f producto=%.2f" (+ a b) (* a b))))
```

**Qué reconocer:** los cuatro acaban en `java.lang.String.format`, y ahí aparece la trampa que la
clase menciona: **`%.2f` usa la configuración regional por defecto de la JVM**, así que en una
máquina con locale español imprimiría `4,00` con coma y rompería el contrato. Kotlin y Groovy lo
evitan pasando `Locale.ROOT` de forma explícita; Scala con su interpolador `f` y Clojure con
`format` heredan el locale del sistema, y en producción convendría fijarlo igual. Es el mismo
problema que .NET resuelve con `InvariantCulture`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// printf de F# es invariante a la cultura: siempre imprime el punto decimal.
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map float
printfn "suma=%.2f producto=%.2f" (a + b) (a * b)
```

### VB.NET

```vbnet
Imports System.Globalization

Module Reales
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Double.Parse(v(0), CultureInfo.InvariantCulture)
        Dim b = Double.Parse(v(1), CultureInfo.InvariantCulture)

        Dim suma = (a + b).ToString("F2", CultureInfo.InvariantCulture)
        Dim producto = (a * b).ToString("F2", CultureInfo.InvariantCulture)

        Console.WriteLine($"suma={suma} producto={producto}")
    End Sub
End Module
```

**Qué reconocer:** `float` en F# **no** es un real de 32 bits sino el alias de `System.Double`, el
mismo `double` de C#: un nombre engañoso que conviene tener fichado. VB.NET muestra la cultura
invariante en los dos extremos del programa —al **leer** y al **escribir**—, porque en configuración
regional española el separador decimal es la coma y `Double.Parse("1.5")` fallaría. F# se libra del
problema porque su `printfn` no consulta la cultura; es la misma diferencia que separa a `%.2f` de
`String.format` en la JVM.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Donde nació `%.2f` y donde el `double` no oculta
nada.

### C++

```cpp
#include <iomanip>
#include <iostream>

int main() {
    double a, b;
    std::cin >> a >> b;
    std::cout << std::fixed << std::setprecision(2)
              << "suma=" << a + b
              << " producto=" << a * b << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        double a, b;
        if (scanf("%lf %lf", &a, &b) != 2) return 1;
        printf("suma=%.2f producto=%.2f\n", a + b, a * b);
    }
    return 0;
}
```

**Qué reconocer:** Objective-C es indistinguible de la versión de C de la clase —`scanf("%lf")`,
`printf("%.2f")`— porque es un superconjunto estricto. C++ sustituye el formato por manipuladores de
flujo, y conviene fijarse en que `std::fixed` y `std::setprecision(2)` son **pegajosos**: se aplican
a todo lo que se imprima después, no solo al siguiente número. Los dos exponen sin adornos lo que la
clase quiere enseñar: el `double` es un binario de 64 bits y `%.2f` no lo corrige, solo lo redondea
al escribirlo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). El tamaño del real está
en el nombre del tipo y la conversión nunca es automática.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseFloat(f64, it.next().?);
    const b = try std.fmt.parseFloat(f64, it.next().?);
    try std.io.getStdOut().writer().print("suma={d:.2} producto={d:.2}\n", .{ a + b, a * b });
}
```

### Nim

```nim
import std/[strutils, sequtils, strformat]

let v = stdin.readLine().splitWhitespace().map(parseFloat)
let suma = v[0] + v[1]
let producto = v[0] * v[1]
echo &"suma={suma:.2f} producto={producto:.2f}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!double).array;
    writefln("suma=%.2f producto=%.2f", v[0] + v[1], v[0] * v[1]);
}
```

**Qué reconocer:** `f64` en Zig, `float` en Nim y `double` en D son el mismo IEEE 754 de doble
precisión que usa Rust: la aritmética es idéntica y el error de `0.1 + 0.2` también. Lo que cambia
es el rigor al convertir texto en número —`parseFloat` puede fallar, y Zig obliga a escribir `try`
delante— y el hecho de que estos lenguajes no promocionan enteros a reales por su cuenta. D es el
único de los tres que ofrece además un `real` de precisión extendida (80 bits en x86), un recordatorio
de que "coma flotante" no significa siempre 64 bits.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se declara el resultado, no el procedimiento.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    Suma is float(A + B),
    Producto is float(A * B),
    format("suma=~2f producto=~2f~n", [Suma, Producto]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni redondeo; solo los dialectos con aritmética (p. ej. Soufflé)
% admiten expresiones como estas. Se declaran los operandos y se derivan los resultados.
operandos(1.5, 2.5).

suma(S) :- operandos(A, B), S = A + B.
producto(P) :- operandos(A, B), P = A * B.
```

**Qué reconocer:** en Prolog `Suma is A + B` **no** es una asignación sino la unificación de `Suma`
con el resultado de evaluar la expresión, y ahí aparece un detalle propio del lenguaje: si los dos
operandos son enteros el resultado también lo es, por eso el código pide `float(...)` de forma
explícita antes de formatear con `~2f`. Datalog llega al límite del paradigma: sin salida y sin
redondeo, lo único que puede declarar es **qué relación** existe entre los operandos y los
resultados. Es la misma renuncia de SQL, donde el redondeo es una función aplicada a una columna, no
un paso de un programa.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo IEEE 754 debajo de todos: la suma de `0.1` y `0.2`
falla igual en los veinte, y en los veinte el `%.2f` la disimula. Lo que de verdad los separa no es
la aritmética sino **quién decide el separador decimal**: el programa o la configuración regional de
la máquina. Eso es lo transferible.

⏮️ [Volver a la clase 045](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
