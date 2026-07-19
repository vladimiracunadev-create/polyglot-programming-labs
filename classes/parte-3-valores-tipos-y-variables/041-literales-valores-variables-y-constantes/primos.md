# 🧬 El mismo programa en las familias de lenguajes — Clase 041

> [⬅️ Volver a la clase 041](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el total de una venta— resuelto por los **primos**
de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `precio_unitario cantidad descuento`
- **Salida** (stdout): `Total: <total con 2 decimales>`
- **Regla:** `total = precio_unitario * cantidad * (1 - descuento)`

| stdin | esperado |
|---|---|
| `15000 2 0.10` | `Total: 27000.00` |
| `999.9 3 0` | `Total: 2999.70` |
| `5000 0 0.20` | `Total: 0.00` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico, poca ceremonia, la variable no declara tipo. La familia entera comparte el gesto:
leer la línea, partirla, convertir y formatear.

### Ruby

```ruby
precio, cantidad, descuento = STDIN.gets.split.map(&:to_f)
total = precio * cantidad * (1 - descuento)
puts format("Total: %.2f", total)
```

### Perl

```perl
my ($precio, $cantidad, $descuento) = split ' ', <STDIN>;
my $total = $precio * $cantidad * (1 - $descuento);
printf "Total: %.2f\n", $total;
```

### Lua

```lua
local precio, cantidad, descuento = io.read("n", "n", "n")
local total = precio * cantidad * (1 - descuento)
print(string.format("Total: %.2f", total))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] precio cantidad descuento
set total [expr {$precio * $cantidad * (1 - $descuento)}]
puts [format "Total: %.2f" $total]
```

### R

```r
v <- as.numeric(strsplit(readLines("stdin", n = 1), " ")[[1]])
total <- v[1] * v[2] * (1 - v[3])
cat(sprintf("Total: %.2f\n", total))
```

**Qué reconocer:** en los cinco la variable aparece sin tipo y la conversión de texto a número es
explícita (`to_f`, `parseFloat`, `as.numeric`). Tcl es el extremo del *todo es cadena*: incluso la
aritmética se pide con `expr`. R delata su origen estadístico tratando la línea como un **vector**
numérico en vez de tres variables sueltas.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.split(' ').map(double.parse).toList();
  final total = v[0] * v[1] * (1 - v[2]);
  print('Total: ${total.toStringAsFixed(2)}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
package {
    public class Venta {
        public static function total(precio:Number, cantidad:Number, descuento:Number):String {
            var t:Number = precio * cantidad * (1 - descuento);
            return "Total: " + t.toFixed(2);
        }
    }
}
```

**Qué reconocer:** `toStringAsFixed` / `toFixed` es el mismo `toFixed` de JavaScript, y `Number` es
el mismo tipo de coma flotante único. Dart añade tipos estáticos opcionales —igual que TypeScript
sobre JS— y el `!` que afirma que la lectura no fue nula.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val (precio, cantidad, descuento) = readLine()!!.split(" ").map { it.toDouble() }
    val total = precio * cantidad * (1 - descuento)
    println("Total: %.2f".format(total))
}
```

### Scala

```scala
object Venta extends App {
  val Array(precio, cantidad, descuento) =
    scala.io.StdIn.readLine().split(" ").map(_.toDouble)
  val total = precio * cantidad * (1 - descuento)
  println(f"Total: $total%.2f")
}
```

### Groovy

```groovy
def (precio, cantidad, descuento) = System.in.newReader().readLine().split(' ')*.toDouble()
def total = precio * cantidad * (1 - descuento)
printf("Total: %.2f%n", total)
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[precio cantidad descuento] (map read-string (str/split (read-line) #" "))
      total (* precio cantidad (- 1 descuento))]
  (println (format "Total: %.2f" (double total))))
```

**Qué reconocer:** los cuatro acaban llamando a `String.format` de Java, por eso `%.2f` aparece en
todos. Kotlin y Scala **desestructuran** la lista en tres nombres, algo que Java no permite. Clojure
cambia de paradigma dentro de la misma máquina virtual: prefijo, inmutable y sin variables que se
reasignen.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| precio; cantidad; descuento |] =
    stdin.ReadLine().Split(' ') |> Array.map float
let total = precio * cantidad * (1.0 - descuento)
printfn "Total: %.2f" total
```

### VB.NET

```vbnet
Imports System.Globalization

Module Venta
    Sub Main()
        Dim v = Console.ReadLine().Split(" "c)
        Dim precio = Double.Parse(v(0), CultureInfo.InvariantCulture)
        Dim cantidad = Double.Parse(v(1), CultureInfo.InvariantCulture)
        Dim descuento = Double.Parse(v(2), CultureInfo.InvariantCulture)
        Console.WriteLine("Total: " & (precio * cantidad * (1 - descuento)).ToString("F2", CultureInfo.InvariantCulture))
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR y comparten `Double` y `CultureInfo` —ese detalle de
la cultura invariante es la trampa clásica de .NET, porque en configuración regional española el
separador decimal es la coma—. F# muestra el otro extremo: funcional, con `|>` encadenando en vez
de anidar llamadas.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double precio, cantidad, descuento;
    std::cin >> precio >> cantidad >> descuento;
    const double total = precio * cantidad * (1 - descuento);
    std::cout << "Total: " << std::fixed << std::setprecision(2) << total << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        double precio, cantidad, descuento;
        scanf("%lf %lf %lf", &precio, &cantidad, &descuento);
        double total = precio * cantidad * (1 - descuento);
        printf("Total: %.2f\n", total);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C** — el código C de la clase compila casi tal cual
en los dos. C++ sustituye `printf` por flujos (`<<`) y controla los decimales con manipuladores;
Objective-C conserva `printf` intacto y solo añade su capa de objetos y el bloque de gestión de
memoria.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const precio = try std.fmt.parseFloat(f64, it.next().?);
    const cantidad = try std.fmt.parseFloat(f64, it.next().?);
    const descuento = try std.fmt.parseFloat(f64, it.next().?);
    const total = precio * cantidad * (1 - descuento);
    try std.io.getStdOut().writer().print("Total: {d:.2}\n", .{total});
}
```

### Nim

```nim
import std/[strutils, sequtils, strformat]

let v = stdin.readLine().splitWhitespace().map(parseFloat)
let total = v[0] * v[1] * (1 - v[2])
echo &"Total: {total:.2f}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!double).array;
    const total = v[0] * v[1] * (1 - v[2]);
    writefln("Total: %.2f", total);
}
```

**Qué reconocer:** Zig es el más explícito de todos —reserva el búfer a mano y cada operación que
puede fallar lleva `try`, igual que Rust obliga a tratar el error—. Nim y D esconden esa maquinaria
tras una sintaxis de scripting, pero siguen compilando a binario nativo: demuestran que "parecerse a
Python" y "compilar como C" no son incompatibles.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [Precio, Cantidad, Descuento]),
    Total is Precio * Cantidad * (1 - Descuento),
    format("Total: ~2f~n", [Total]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: se declaran los hechos y la regla que deriva el total.
venta(15000, 2, 0.10).

total(T) :- venta(P, C, D), T = P * C * (1 - D).
```

**Qué reconocer:** en Prolog `Total is ...` **no** es una asignación sino una unificación con el
resultado de evaluar la expresión: el nombre se liga una sola vez y no se reasigna, igual que una
constante. Datalog lleva la idea al extremo —solo hechos y reglas, sin efectos ni entrada/salida—,
que es la misma renuncia que hace SQL al no decirte cómo recorrer las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer, convertir, multiplicar,
formatear con dos decimales. Lo que cambia es la **forma** y, en algunos casos, las **garantías**.
Eso es lo transferible.

⏮️ [Volver a la clase 041](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
