# 🧬 El mismo programa en las familias de lenguajes — Clase 050

> [⬅️ Volver a la clase 050](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar un entero y un real— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, con `a` entero y `b` real
- **Salida** (stdout): `suma=<a+b con 2 decimales>`
- **Regla:** `suma = a + b`, con el entero promovido a real

| stdin | esperado |
|---|---|
| `2 3.5` | `suma=5.50` |
| `10 0.25` | `suma=10.25` |
| `0 0` | `suma=0.00` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El tipo vive en el **valor**, no en la variable: nadie declara `int` ni `float`, y la decisión de
cómo interpretar el texto de entrada se toma en tiempo de ejecución.

### Ruby

```ruby
entero, real = STDIN.gets.split
suma = entero.to_i + real.to_f
puts format("suma=%.2f", suma)
```

### Perl

```perl
my ($entero, $real) = split ' ', <STDIN>;
# Perl ni siquiera separa entero de real: un escalar guarda "un número" y ya.
printf "suma=%.2f\n", $entero + $real;
```

### Lua

```lua
-- Desde Lua 5.3 el número tiene dos subtipos, integer y float, pero se eligen
-- en tiempo de ejecución: la variable sigue sin declarar nada.
local entero, real = io.read("n", "n")
print(string.format("suma=%.2f", entero + real))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] entero real
puts [format "suma=%.2f" [expr {$entero + $real}]]
```

### R

```r
p <- strsplit(readLines("stdin", n = 1), " ")[[1]]
entero <- as.integer(p[1])
real <- as.numeric(p[2])
cat(sprintf("suma=%.2f\n", entero + real))
```

**Qué reconocer:** en los cinco la variable aparece **sin tipo** y el error de tipos, si lo hay,
aparece al ejecutar y no al escribir. Tcl es el extremo: todo es cadena hasta que `expr` decide
tratarlo como número. Perl va más lejos todavía y ni distingue entero de real; R sí distingue
(`integer` frente a `double`) pero lo comprueba en ejecución, como los demás.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia enseña justo la tensión de esta clase: un lenguaje dinámico y una capa estática encima.

### Dart

```dart
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.split(' ');
  final int entero = int.parse(p[0]);
  final double real = double.parse(p[1]);
  print('suma=${(entero + real).toStringAsFixed(2)}');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
    // Las anotaciones :int y :Number se comprueban al compilar; sin ellas el tipo
    // es `*` y la comprobación vuelve a ser dinámica.
    public class Suma {
        public static function calcular(entero:int, real:Number):String {
            var suma:Number = entero + real;
            return "suma=" + suma.toFixed(2);
        }
    }
}
```

**Qué reconocer:** ambos son estáticos por elección, no por obligación. Dart declara `int` y `double`
como dos tipos distintos —a diferencia del `Number` único de JavaScript— y el compilador comprueba
la suma antes de ejecutar. ActionScript 3 fue el primer intento de poner tipos estáticos sobre
ECMAScript, exactamente lo que TypeScript hace hoy.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La misma máquina virtual soporta lenguajes
estáticos y dinámicos: la comprobación de tipos es una decisión del compilador, no del bytecode.

### Kotlin

```kotlin
fun main() {
    val (x, y) = readLine()!!.split(" ")
    val entero: Int = x.toInt()
    val real: Double = y.toDouble()
    println("suma=%.2f".format(entero + real))
}
```

### Scala

```scala
object Suma extends App {
  val Array(x, y) = scala.io.StdIn.readLine().split(" ")
  val entero: Int = x.toInt
  val real: Double = y.toDouble
  println(f"suma=${entero + real}%.2f")
}
```

### Groovy

```groovy
// Groovy es dinámico con `def` y comprueba tipos si los declaras: aquí los declaramos.
def (x, y) = System.in.newReader().readLine().split(' ')
int entero = x as int
double real = y as double
printf("suma=%.2f%n", entero + real)
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[x y] (str/split (str/trim (read-line)) #"\s+")
      entero (Long/parseLong x)
      real (Double/parseDouble y)]
  (println (format "suma=%.2f" (+ entero real))))
```

**Qué reconocer:** Kotlin y Scala son tan estáticos como Java —`Int` y `Double` son tipos distintos y
la promoción la aplica el compilador—, mientras que Clojure resuelve `+` en ejecución mirando los
valores, igual que Python. Groovy es el caso más interesante: es **las dos cosas**, dinámico con
`def` y estático cuando escribes el tipo, sobre la misma JVM.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let partes = stdin.ReadLine().Split(' ')
let entero : int = int partes.[0]
let real : float = float partes.[1]
// F# no promueve int a float por su cuenta: la conversión es obligatoria y explícita.
printfn "suma=%.2f" (float entero + real)
```

### VB.NET

```vbnet
Imports System.Globalization

Module Suma
    Sub Main()
        ' Con Option Strict On el compilador exige tipos y conversiones explícitas;
        ' con Option Strict Off, VB acepta enlaces tardíos y se comporta casi como un
        ' lenguaje dinámico sobre el mismo CLR.
        Dim p = Console.ReadLine().Split(" "c)
        Dim entero As Integer = Integer.Parse(p(0), CultureInfo.InvariantCulture)
        Dim real As Double = Double.Parse(p(1), CultureInfo.InvariantCulture)
        Console.WriteLine("suma=" & (entero + real).ToString("F2", CultureInfo.InvariantCulture))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `Int32` y `Double` del CLR y la trampa de `CultureInfo`. Pero
F# es el más estricto de la familia: donde C# y VB.NET promueven el entero a `double` en silencio,
F# se niega y exige escribir `float entero`. Es tipado estático llevado al extremo de no confiar ni
en las conversiones seguras.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Tipos declarados en cada variable y comprobados al
compilar; el binario resultante ya no sabe nada de tipos.

### C++

```cpp
#include <iostream>
#include <iomanip>

int main() {
    int entero;
    double real;
    std::cin >> entero >> real;
    std::cout << "suma=" << std::fixed << std::setprecision(2) << entero + real << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int entero;
        double real;
        scanf("%d %lf", &entero, &real);
        printf("suma=%.2f\n", entero + real);
    }
    return 0;
}
```

**Qué reconocer:** en los dos la promoción de `int` a `double` la hace el compilador siguiendo las
*conversiones aritméticas usuales* de C, sin que aparezca nada en el código. Objective-C añade un
matiz que rompe el molde: su tipo `id` es un puntero a objeto **sin tipo comprobado**, así que dentro
de un lenguaje estático convive un envío de mensajes tan dinámico como el de Ruby.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Estáticos y compilados,
con la particularidad de que aquí ni siquiera las conversiones seguras son gratis.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const entero = try std.fmt.parseInt(i64, it.next().?, 10);
    const real = try std.fmt.parseFloat(f64, it.next().?);
    const suma = @as(f64, @floatFromInt(entero)) + real;
    try std.io.getStdOut().writer().print("suma={d:.2}\n", .{suma});
}
```

### Nim

```nim
import std/[strutils, strformat]

let p = stdin.readLine().splitWhitespace()
let entero: int = parseInt(p[0])
let real: float = parseFloat(p[1])
# Nim tampoco mezcla int y float en la misma expresión sin permiso: `entero.float`.
echo &"suma={entero.float + real:.2f}"
```

### D

```d
import std.stdio, std.array, std.conv;

void main() {
    auto p = readln().split();
    int entero = p[0].to!int;
    double real_ = p[1].to!double;
    writefln("suma=%.2f", entero + real_);
}
```

**Qué reconocer:** Zig es el más radical de todos —`@floatFromInt` obliga a escribir la conversión
que C y Go hacen solos— y Nim va por el mismo camino con `entero.float`. D, en cambio, hereda las
promociones implícitas de C. El detalle de `real_` en D no es capricho: `real` es una **palabra
reservada** (el tipo de coma flotante de 80 bits), y esa colisión es un recordatorio de que en un
lenguaje estático los nombres de tipo ocupan sitio en el vocabulario.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí el tipo lo lleva el **dato**, no la
variable, y en el caso de SQL lo declara el esquema de la tabla.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    % Prolog no declara tipos: `number_string` decide en ejecución si sale
    % un entero o un flotante, y `is` aplica la promoción al evaluar.
    number_string(Entero, SA),
    number_string(Real, SB),
    Suma is Entero + Real,
    format("suma=~2f~n", [Suma]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: se declara el hecho y la regla que deriva la suma.
% Tampoco hay declaración de tipos; el "tipo" de un predicado es su aridad.
entrada(2, 3.5).

suma(S) :- entrada(A, B), S = A + B.
```

**Qué reconocer:** Prolog no tiene declaraciones de tipo en absoluto: `Entero` y `Real` son solo
nombres de variables lógicas, y si la entrada no fuera un número el fallo llegaría al ejecutar. Es el
extremo dinámico del atlas. SQL está en el opuesto —cada columna declara su tipo en el `CREATE
TABLE`— y las dos posturas conviven bajo la misma etiqueta de "declarativo".

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los divide en dos mitades: **¿quién comprueba
que el entero y el real se pueden sumar, el compilador o la máquina en marcha?** La respuesta no
cambia el resultado, pero sí cambia cuándo te enteras del error. Eso es lo transferible.

⏮️ [Volver a la clase 050](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
