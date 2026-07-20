# 🧬 El mismo programa en las familias de lenguajes — Clase 088

> [⬅️ Volver a la clase 088](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —traer el valor absoluto desde donde el lenguaje lo
guarde y usarlo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `abs=<|n|>`
- **Regla:** usar la función de valor absoluto de la biblioteca estándar, no reimplementarla

| stdin | esperado |
|---|---|
| `-5` | `abs=5` |
| `3` | `abs=3` |
| `0` | `abs=0` |

El programa es de una línea a propósito: lo que se compara aquí no es el cálculo, sino **de dónde
sale el nombre** `abs` y qué hubo que escribir para tenerlo a mano.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python importa por módulo (`import math`), PHP no importa nada porque su biblioteca es global. Sus
primos se reparten entre esos dos extremos.

### Ruby

```ruby
# Ruby no importa nada aquí: Integer#abs es parte del núcleo, siempre cargado.
# 'require' trae bibliotecas al proceso; 'include' mezcla un módulo en el
# espacio actual. Son dos gestos distintos que en Python se confunden en uno.
n = STDIN.gets.to_i
puts "abs=#{n.abs}"
```

### Perl

```perl
use strict;
use warnings;

# 'use Modulo qw(nombres)' trae a este paquete SOLO los nombres pedidos,
# elegidos entre los que el módulo publicó en @EXPORT_OK.
use List::Util qw(max);

my $n = <STDIN>;
chomp $n;
printf "abs=%d\n", max($n, -$n);
```

### Lua

```lua
-- require() devuelve la tabla que el módulo entrega; se guarda en una variable
-- local y el nombre con el que la llamas es cosa tuya.
local math = require("math")

local n = io.read("n")
print(string.format("abs=%d", math.abs(n)))
```

### Tcl

```tcl
# 'package require' pide una versión mínima al gestor de paquetes;
# abs() es una función del evaluador de expresiones, no un comando.
package require Tcl 8.6

set n [string trim [gets stdin]]
puts "abs=[expr {abs($n)}]"
```

### R

```r
# library(pkg) *adjunta* el paquete al camino de búsqueda, así que sus nombres
# quedan visibles sin prefijo; abs viene en 'base', siempre adjunto.
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("abs=%d\n", abs(n)))
```

**Qué reconocer:** los cinco resuelven lo mismo con políticas de importación radicalmente distintas.
Perl es el único que importa **por símbolo**: `qw(max)` trae ese nombre y ninguno más, y el módulo
tuvo que publicarlo antes en `@EXPORT_OK` —un contrato en dos direcciones—. Lua importa **por valor**:
`require` devuelve una tabla y el nombre local lo eliges tú, así que no hay contaminación posible del
espacio global. R hace lo contrario, `library()` vuelca todos los nombres del paquete al camino de
búsqueda y por eso dos paquetes pueden taparse mutuamente. Ruby y Tcl separan un eje que las demás
mezclan: *cargar* código (`require`) y *hacer visibles* sus nombres (`include`, el prefijo de
`namespace`) son dos decisiones independientes.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia que popularizó `import { x } from 'y'` y el árbol de dependencias en un archivo aparte.

### Dart

```dart
// Dart importa BIBLIOTECAS enteras, no símbolos sueltos: se puede filtrar con
// 'show'/'hide' o poner prefijo con 'as'. Las dependencias van en pubspec.yaml.
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('abs=${n.abs()}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash. Math es una clase global del reproductor,
// no se importa; el gesto de importar se ve con cualquier clase de paquete.
package {
    import flash.display.Sprite;

    public class Absoluto extends Sprite {
        public static function describir(n:int):String {
            return "abs=" + Math.abs(n);
        }
    }
}
```

**Qué reconocer:** ActionScript importa **clases**, una por línea, con su ruta completa de paquete
—el mismo modelo que Java—, y solo sirve para no repetir el nombre largo. Dart importa **archivos o
bibliotecas** y trae todos sus nombres, filtrando después con `show` y `hide`. La diferencia real con
JavaScript está fuera del código: en Dart, qué paquetes existen se declara en `pubspec.yaml` y quién
los usa en cada `import`, dos capas que conviene no confundir cuando organizas un proyecto —es lo
mismo que `package.json` frente a la sentencia `import`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En Java `import` no carga nada: es solo un
alias para no escribir el nombre completo, y la carga real la decide el *classpath*.

### Kotlin

```kotlin
// abs no está en la clase Math sino como función suelta de kotlin.math:
// por eso hay que importarla, aunque kotlin.* se importe solo.
import kotlin.math.abs

fun main() {
    val n = readLine()!!.trim().toInt()
    println("abs=${abs(n)}")
}
```

### Scala

```scala
import scala.math.abs

object Main {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"abs=${abs(n)}")
  }
}
```

### Groovy

```groovy
// Groovy importa por defecto java.lang, java.util, java.io, java.net,
// groovy.lang y groovy.util: Math ya está ahí sin escribir nada.
def n = System.in.newReader().readLine().trim() as int
println "abs=${Math.abs(n)}"
```

### Clojure

```clojure
;; 'require' carga un espacio de nombres y le da alias; 'import' se reserva para
;; clases Java. Son dos verbos distintos porque son dos mundos distintos.
(require '[clojure.string :as str])

(let [n (Integer/parseInt (str/trim (read-line)))]
  (println (str "abs=" (abs n))))
```

**Qué reconocer:** los cuatro comparten el classpath, pero cada uno decide un juego de importaciones
implícitas distinto: Groovy trae seis paquetes ya importados, Kotlin y Scala traen los suyos y aun
así piden `import kotlin.math.abs` porque su `abs` es una función libre y no un método estático de
`Math`. Clojure es el que marca la distinción más útil de esta página: `require` es para código
Clojure y **carga** el espacio de nombres si hace falta, mientras que `import` es solo para clases
Java y no carga nada, igual que el `import` de Java. Cuando un lenguaje tiene dos palabras para
importar, casi siempre es porque una carga y la otra solo abrevia.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Aquí conviven dos niveles que no hay que mezclar:
la **referencia al ensamblado** (en el `.csproj`) y el `using` (que solo abrevia nombres).

### F\#

```fsharp
// 'open' abre un espacio de nombres o un módulo; no carga ensamblados.
// El orden importa: lo abierto después puede tapar lo anterior.
open System

[<EntryPoint>]
let main _ =
    let n = Int32.Parse(stdin.ReadLine().Trim())
    printfn "abs=%d" (abs n)
    0
```

### VB.NET

```vbnet
' Imports equivale al 'using' de C#. Además, VB tiene importaciones a nivel de
' proyecto: System y System.Math suelen estar ya activas sin escribirlas.
Imports System

Module Programa
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("abs={0}", Math.Abs(n))
    End Sub
End Module
```

**Qué reconocer:** en los tres lenguajes del CLR la palabra que importa —`using`, `Imports`, `open`—
**no carga código**: solo acorta nombres dentro del archivo. Lo que decide qué existe es la
referencia declarada en el archivo de proyecto, y esa separación entre "qué está disponible" y "cómo
lo nombro" es la misma que en Java. F# añade dos rarezas: el orden de los `open` es significativo, y
su `abs` es una función genérica del propio lenguaje —no `Math.Abs`—, así que funciona sin abrir nada.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). `#include` no importa: **pega el texto** de la
cabecera antes de compilar, y por eso todo el mundo lleva décadas evitando incluir dos veces.

### C++

```cpp
// <cstdlib> es la versión C++ de <stdlib.h>: pone abs también en std::.
// Desde C++20 existe 'import <iostream>;', que sí es un módulo de verdad.
#include <iostream>
#include <cstdlib>

int main() {
    int n;
    std::cin >> n;
    std::cout << "abs=" << std::abs(n) << '\n';
}
```

### Objective-C

```objc
// #import es #include con memoria: no vuelve a pegar la misma cabecera dos veces,
// así que no hacen falta los guardas de inclusión clásicos de C.
#import <Foundation/Foundation.h>
#include <stdlib.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        printf("abs=%d\n", abs(n));
    }
    return 0;
}
```

**Qué reconocer:** esta familia es la única de las siete donde importar es una operación **textual**,
no semántica: el compilador ve un único archivo gigante después del preprocesador, y de ahí vienen
los tiempos de compilación y los conflictos de macros. Objective-C aportó `#import`, un `#include`
que recuerda lo ya incluido —una mejora tan obvia que C++ tardó hasta la versión 20 en tener su
equivalente con módulos reales—. El detalle práctico: en C++ `<cstdlib>` mete los nombres en `std::`
además de en el espacio global, mientras que en C y Objective-C `abs` está sencillamente suelto.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos llegaron con un
gestor de paquetes y un archivo de manifiesto desde el primer día: `go.mod`, `Cargo.toml`.

### Zig

```zig
// @import es una función del compilador que devuelve un valor: se asigna a una
// constante. "std" es el módulo estándar; "otro.zig" sería un archivo del proyecto.
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    // @abs es una función incorporada del compilador: no se importa de ningún sitio.
    try std.io.getStdOut().writer().print("abs={d}\n", .{@abs(n)});
}
```

### Nim

```nim
# std/strutils: el prefijo 'std/' distingue la biblioteca estándar de los
# paquetes de terceros, que se declaran en un archivo .nimble.
import std/strutils

let n = parseInt(stdin.readLine().strip())
echo "abs=", abs(n)   # abs vive en 'system', importado siempre y sin escribirlo
```

### D

```d
// D permite importación selectiva: 'import modulo : simbolo' trae solo ese nombre,
// y el import puede ir incluso dentro de una función, con alcance local.
import std.stdio;
import std.conv : to;
import std.string : strip;
import std.math : abs;

void main() {
    auto n = readln().strip().to!int;
    writefln("abs=%d", abs(n));
}
```

**Qué reconocer:** los tres separan con claridad la biblioteca estándar de las dependencias externas
—`std/` en Nim, `"std"` en Zig, `std.` en D— y todos tienen un manifiesto fuera del código para lo
demás, como `go.mod` y `Cargo.toml`. Donde se apartan es en la granularidad: D es el más fino de las
veinte implementaciones, porque `import std.math : abs` trae un único símbolo y un `import` puede
declararse dentro de una función, limitando su alcance a ese bloque. Zig va al otro extremo y ni
siquiera tiene sentencia de importación: `@import("std")` es una expresión que devuelve un valor y se
guarda en una constante, así que importar y declarar una variable son literalmente lo mismo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL no importa nada: las funciones incorporadas
existen sin más, y lo externo entra como extensión instalada en el motor.

### Prolog

```prolog
% use_module carga una biblioteca y trae sus predicados exportados.
% abs/1 es una función aritmética de is/2, no un predicado: no se importa.
:- use_module(library(readutil)).
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    A is abs(N),
    format("abs=~d~n", [A]).
```

### Datalog

```datalog
% Datalog puro no tiene módulos, ni biblioteca estándar, ni E/S: el valor absoluto
% se expresa con dos reglas, una por rama del signo. Los motores concretos
% (Souffle, por ejemplo) sí añaden funciones incorporadas, pero como extensión.
entrada(-5).

resultado(A) :- entrada(N), N < 0, A = -N.
resultado(A) :- entrada(N), N >= 0, A = N.
```

**Qué reconocer:** Prolog distingue dos vocabularios que se escriben en el mismo programa: los
**predicados**, que sí viven en bibliotecas y se traen con `use_module`, y las **funciones
aritméticas** como `abs`, que solo existen dentro de `is/2` y forman parte del evaluador. Es la misma
frontera que en Tcl separa `expr` del resto del lenguaje. Datalog no tiene ninguna de las dos cosas:
sin biblioteca que importar, el valor absoluto se expresa **declarando las dos ramas** y dejando que
el motor elija cuál aplica. Cuando no hay nada que importar, el lenguaje suele estar diciéndote que
tampoco espera que escribas programas grandes con él.

---

## Y de vuelta a la clase

Veinte lenguajes y una operación trivial que, sin embargo, los ordena por completo: los que no
importan nada porque su biblioteca es global, los que importan un **archivo o módulo** entero, los
que importan **símbolos sueltos** y los que solo **abrevian nombres** sin cargar nada. Y por encima
de todos, la separación entre el código que dice `import` y el manifiesto que dice qué existe —
`package.json`, `pubspec.yaml`, `go.mod`, `Cargo.toml`, `.nimble`, `.csproj`—. Reconocer esos dos
niveles en un proyecto ajeno es la mitad del trabajo de orientarse en él.

⏮️ [Volver a la clase 088](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
