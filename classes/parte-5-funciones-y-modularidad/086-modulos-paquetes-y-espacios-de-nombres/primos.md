# 🧬 El mismo programa en las familias de lenguajes — Clase 086

> [⬅️ Volver a la clase 086](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —llamar a una función `doble` que vive en un módulo
o espacio de nombres separado— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** `modulo.doble(n) = 2n`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `-4` | `resultado=-8` |

Como el verificador ejecuta **un solo archivo**, todos los primos declaran el módulo en línea. En un
proyecto real cada uno viviría en su propio archivo; el comentario de cada bloque dice cuál sería.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los dos nació con módulos: se los añadieron cuando los programas dejaron de caber en un
archivo. Sus primos resolvieron el mismo problema tarde y de formas muy distintas.

### Ruby

```ruby
# Un módulo Ruby sirve para dos cosas: espacio de nombres (Matematicas.doble)
# y mixin (include Matematicas dentro de una clase).
module Matematicas
  def self.doble(n)
    2 * n
  end
end

n = STDIN.gets.to_i
puts "resultado=#{Matematicas.doble(n)}"
```

### Perl

```perl
use strict;
use warnings;

# 'package' abre un espacio de nombres; el archivo Matematicas.pm se traería
# con 'use Matematicas' y exportaría nombres vía @EXPORT_OK.
package Matematicas;

sub doble { return 2 * $_[0]; }

package main;

my $n = <STDIN>;
chomp $n;
printf "resultado=%d\n", Matematicas::doble($n);
```

### Lua

```lua
-- Un módulo Lua es una tabla que el archivo *devuelve*; require() entrega esa tabla.
local matematicas = {}

function matematicas.doble(n)
  return 2 * n
end

local n = io.read("n")
print(string.format("resultado=%d", matematicas.doble(n)))
```

### Tcl

```tcl
namespace eval matematicas {
    proc doble {n} { expr {2 * $n} }
}

set n [string trim [gets stdin]]
puts "resultado=[matematicas::doble $n]"
```

### R

```r
# R agrupa código en paquetes; dentro de un script, un entorno hace de espacio de nombres.
matematicas <- new.env()
matematicas$doble <- function(n) 2 * n

n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("resultado=%d\n", matematicas$doble(n)))
```

**Qué reconocer:** los cinco separan igual, con un punto o dos puntos dobles, pero lo que hay al otro
lado del separador no es lo mismo. En Lua el módulo es literalmente una **tabla**: no hay sintaxis de
módulo, solo un valor que el archivo devuelve, y por eso `matematicas.doble` es un acceso a campo
corriente. En R pasa algo parecido con los **entornos**. Ruby y Perl sí tienen una construcción
dedicada —`module` y `package`—, pero Ruby la usa además para **mezclar** métodos dentro de clases,
un uso que Perl no contempla. Tcl es el único cuyo `namespace` es puramente léxico: agrupa nombres de
comando, sin objeto ni valor que puedas guardar en una variable.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia donde el archivo **es** el módulo.

### Dart

```dart
// En un proyecto real 'doble' viviría en lib/matematicas.dart y se traería con
// import 'matematicas.dart' as matematicas; el archivo es la unidad de módulo.
import 'dart:io';

int doble(int n) => 2 * n;

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('resultado=${doble(n)}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash. Aquí el paquete es el espacio de nombres y
// obliga a que la ruta de carpetas coincida: cl/curso/Matematicas.as.
package cl.curso {
    public class Matematicas {
        public static function doble(n:int):int {
            return 2 * n;
        }
    }
}
```

**Qué reconocer:** Dart sigue la línea de los módulos ES de JavaScript —el archivo es la unidad, se
importa entero y opcionalmente se le pone prefijo con `as`—, y no existe ninguna palabra clave
`module` en el código. ActionScript 3 va por el camino contrario, el de Java: declara `package` con
una ruta jerárquica que **debe** corresponder a la estructura de carpetas. Es la diferencia entre
"el módulo es dónde está el archivo" y "el módulo es lo que el archivo declara ser".

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En Java el paquete es obligatorio y la unidad
mínima de agrupación es la **clase**, no el archivo. Sus primos discrepan.

### Kotlin

```kotlin
// Kotlin permite funciones fuera de toda clase: el paquete basta como agrupador.
package matematicas

fun doble(n: Int) = 2 * n

fun main() {
    val n = readLine()!!.trim().toInt()
    println("resultado=${doble(n)}")
}
```

### Scala

```scala
package matematicas

// Un 'object' es un singleton: hace de espacio de nombres con estado propio.
object Numeros {
  def doble(n: Int): Int = 2 * n
}

object Main {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"resultado=${Numeros.doble(n)}")
  }
}
```

### Groovy

```groovy
class Matematicas {
    static int doble(int n) { 2 * n }
}

def n = System.in.newReader().readLine().trim() as int
println "resultado=${Matematicas.doble(n)}"
```

### Clojure

```clojure
;; Cada 'ns' vive en su propio archivo (matematicas.clj) y se trae con
;; (:require [matematicas :as m]) para llamar (m/doble n).
(ns matematicas)

(defn doble [n] (* 2 n))

(println (str "resultado=" (doble (Integer/parseInt (.trim (read-line))))))
```

**Qué reconocer:** los cuatro acaban generando una clase en el bytecode, porque la JVM no conoce
otra cosa; lo interesante es lo que dejan ver. Groovy es el más fiel a Java: hay que envolver `doble`
en una clase para poder llamarla como `Matematicas.doble`. Kotlin rompe con eso y permite funciones
de nivel superior (el compilador fabrica una clase `MatematicasKt` que no escribes). Scala añade el
`object`, un singleton que hace de espacio de nombres y que además puede tener estado y heredar,
cosa que un paquete Java no puede. Clojure es el único con un mecanismo de dos piezas: `ns` declara
el espacio y `require` decide con qué alias se ve desde fuera —el prefijo `m/` es elección de quien
importa, no de quien exporta.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR separa dos ejes que suelen confundirse:
el **espacio de nombres** (organiza nombres) y el **ensamblado** (unidad de despliegue).

### F\#

```fsharp
// 'module' en F# es a la vez espacio de nombres y contenedor de funciones sueltas.
module Matematicas =
    let doble n = 2 * n

[<EntryPoint>]
let main _ =
    let n = int (stdin.ReadLine().Trim())
    printfn "resultado=%d" (Matematicas.doble n)
    0
```

### VB.NET

```vbnet
Namespace Matematicas
    ' Un 'Module' de VB expone sus miembros sin instanciar nada.
    Public Module Operaciones
        Public Function Doble(n As Integer) As Integer
            Return 2 * n
        End Function
    End Module
End Namespace

Module Programa
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("resultado={0}", Matematicas.Operaciones.Doble(n))
    End Sub
End Module
```

**Qué reconocer:** VB.NET separa las dos piezas con dos palabras distintas —`Namespace` agrupa
nombres, `Module` contiene los miembros—, mientras que F# fusiona ambas en un solo `module`, que se
compila a una clase estática. En los dos, y también en C#, el espacio de nombres es **puramente
sintáctico**: no implica ningún archivo ni ninguna carpeta, y dos ensamblados distintos pueden
contribuir al mismo `System.Collections`. Es lo opuesto a Java o a los módulos ES, donde nombre y
ubicación van atados.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene módulos: tiene `#include`, que es un
pegado literal de texto, y por eso los nombres colisionan.

### C++

```cpp
// Hasta C++20 el "módulo" era un par cabecera/.cpp pegado con #include;
// desde C++20 existe 'import matematicas;' de verdad. El namespace es lo que
// siempre ha evitado las colisiones de nombres.
#include <iostream>

namespace matematicas {
    int doble(int n) { return 2 * n; }
}

int main() {
    int n;
    std::cin >> n;
    std::cout << "resultado=" << matematicas::doble(n) << '\n';
}
```

### Objective-C

```objc
// Objective-C no tiene espacios de nombres: la interfaz iría en Matematicas.h,
// la implementación en Matematicas.m, y las colisiones se evitan con un prefijo
// de dos o tres letras (NS..., UI..., aquí CRS...).
#import <Foundation/Foundation.h>

@interface CRSMatematicas : NSObject
+ (int)doble:(int)n;
@end

@implementation CRSMatematicas
+ (int)doble:(int)n { return 2 * n; }
@end

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        printf("resultado=%d\n", [CRSMatematicas doble:n]);
    }
    return 0;
}
```

**Qué reconocer:** los dos heredan de C la separación **interfaz/implementación** en dos archivos, un
reparto que Python o Ruby no necesitan porque el módulo se carga entero. La diferencia entre ellos es
brutal: C++ añadió `namespace` y así puede tener dos `doble` sin conflicto, mientras que Objective-C
nunca lo hizo y toda su biblioteca vive con nombres prefijados —`NSString`, `NSArray`— que son un
espacio de nombres implementado a mano, letra a letra. Cuando veas prefijos así en cualquier
lenguaje, estás viendo el hueco donde debería haber un módulo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos aprendieron del
desastre de `#include` y pusieron el sistema de módulos en el propio lenguaje.

### Zig

```zig
const std = @import("std");

// En Zig cada archivo *es* una struct: lo real sería
// const matematicas = @import("matematicas.zig");
const matematicas = struct {
    pub fn doble(n: i64) i64 {
        return 2 * n;
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("resultado={d}\n", .{matematicas.doble(n)});
}
```

### Nim

```nim
import std/strutils

# En un proyecto real esto sería matematicas.nim, traído con 'import matematicas'.
# El asterisco es lo que hace visible el nombre fuera del módulo.
proc doble*(n: int): int = 2 * n

let n = parseInt(stdin.readLine().strip())
echo "resultado=", doble(n)
```

### D

```d
module matematicas;

import std.stdio, std.conv, std.string;

int doble(int n) { return 2 * n; }

void main() {
    auto n = readln().strip().to!int;
    writefln("resultado=%d", doble(n));
}
```

**Qué reconocer:** los tres atan el módulo al archivo, como Go y Rust, pero cada uno lo declara desde
un extremo distinto. D escribe `module matematicas;` en la primera línea y exige que coincida con la
ruta del archivo —declaración explícita, como Java—. Nim no declara nada: el nombre del módulo **es**
el nombre del archivo, y lo único que se marca es qué sale, con el asterisco. Zig da el paso más
radical: no hay palabra clave `module` en absoluto porque un archivo ya es un valor de tipo `struct`,
y `@import` simplemente lo devuelve; es la misma idea que la tabla de Lua, pero resuelta en tiempo de
compilación.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL organiza en **esquemas**, que además de
agrupar nombres son la unidad sobre la que se conceden permisos.

### Prolog

```prolog
% La lista de exportación es explícita: solo doble/2 se ve desde fuera.
:- module(matematicas, [doble/2]).
:- initialization(main, main).

doble(N, R) :- R is 2 * N.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    doble(N, R),
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog puro no tiene módulos ni E/S: el único "espacio de nombres" es el propio
% nombre del predicado, y todos los predicados viven en un espacio plano y global.
entrada(5).

doble(N, R) :- entrada(N), R = 2 * N.
```

**Qué reconocer:** Prolog es, de los veinte, el que declara la frontera con más precisión: el módulo
enumera `doble/2` —nombre **y aridad**—, así que `doble/3` seguiría siendo privado. Es lo mismo que
hace Perl con `@EXPORT_OK`, pero llevado al detalle de la firma. Datalog no tiene nada de esto, y por
la misma razón que no tiene orden superior: su modelo es un conjunto plano de hechos y reglas sobre
el que se razona globalmente. Cuando un lenguaje renuncia a los módulos, casi siempre es porque
renunció antes a los programas grandes.

---

## Y de vuelta a la clase

Veinte lenguajes y tres respuestas a la misma pregunta —¿qué es un módulo?—: un **archivo** (Lua,
Nim, Zig, Dart), una **declaración** dentro del archivo (Java, D, Prolog, C++) o un **valor** que
puedes manipular como cualquier otro dato (la tabla de Lua, la struct de Zig). Detectar cuál de las
tres usa un lenguaje nuevo te dice de inmediato dónde buscar sus funciones.

⏮️ [Volver a la clase 086](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
