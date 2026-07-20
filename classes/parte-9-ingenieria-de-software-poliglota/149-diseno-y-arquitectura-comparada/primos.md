# 🧬 El mismo programa en las familias de lenguajes — Clase 149

> [⬅️ Volver a la clase 149](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar las capas de una arquitectura— resuelto por
los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes
del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): los nombres de las capas, separados por espacios
- **Salida** (stdout): `capas=<cantidad>`
- **Regla:** contar los nombres de capa

| stdin | esperado |
|---|---|
| `web api datos` | `capas=3` |
| `cli` | `capas=1` |
| `web api datos cache` | `capas=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno impone una estructura: un programa válido puede ser una sola línea suelta, y la arquitectura
es una convención del equipo, no una regla del lenguaje.

### Ruby

```ruby
capas = STDIN.read.split
puts "capas=#{capas.size}"
```

### Perl

```perl
use strict;
use warnings;

my @capas = split ' ', do { local $/; <STDIN> };
printf "capas=%d\n", scalar @capas;
```

### Lua

```lua
local n = 0
for _ in io.read("a"):gmatch("%S+") do
  n = n + 1
end
print("capas=" .. n)
```

### Tcl

```tcl
set capas [regexp -all -inline {\S+} [read stdin]]
puts "capas=[llength $capas]"
```

### R

```r
capas <- scan("stdin", what = character(), quiet = TRUE)
cat(sprintf("capas=%d\n", length(capas)))
```

**Qué reconocer:** los cinco resuelven el problema con código de nivel superior, sin declarar una
clase ni un módulo: el archivo **es** el programa. Eso explica su arquitectura típica —módulos por
convención de directorio, dependencias resueltas en tiempo de carga— y su riesgo característico: como
nada obliga a declarar la frontera entre capas, la separación se sostiene solo por disciplina y por
revisión de código. Lua es el caso extremo, con un lenguaje tan pequeño que ni siquiera trae un
concepto de paquete propio; Ruby es el opuesto dentro de la familia, con módulos y *mixins* que sí
permiten modelar capas explícitas. R vuelve a delatar su origen: trata las capas como un **vector**
de datos, que es la unidad de arquitectura de su comunidad.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final capas = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('capas=${capas.length}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin; además exige que todo viva dentro de una clase
// dentro de un paquete, así que la estructura mínima ya es esta.
package arquitectura {
    public class Capas {
        public static function contar(descripcion:String):String {
            return "capas=" + descripcion.split(" ").length;
        }
    }
}
```

**Qué reconocer:** `split` y `.length` son los mismos de JavaScript, pero el envoltorio cambia por
completo. Dart obliga a una función `main` y a importar explícitamente lo que usa; ActionScript va
más lejos y exige `package` + `class` + método, incluso para tres líneas de lógica. Esa es la
diferencia arquitectónica de fondo entre módulos y paquetes: JavaScript y Dart dejan que la unidad de
diseño sea el **archivo**, mientras que ActionScript —heredero de Java— impone que sea la **clase**,
y que la ruta de directorios coincida con el nombre del paquete. Cuando el lenguaje impone la
estructura, la arquitectura es verificable; cuando no, es un acuerdo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Comparten máquina virtual, pero no la unidad de
diseño: la familia va del objeto obligatorio de Java al espacio de nombres de funciones de Clojure.

### Kotlin

```kotlin
fun main() {
    val capas = readLine()!!.trim().split(Regex("\\s+"))
    println("capas=${capas.size}")
}
```

### Scala

```scala
object Arquitectura extends App {
  val capas = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"capas=${capas.length}")
}
```

### Groovy

```groovy
def capas = System.in.newReader().readLine().trim().split(/\s+/)
println "capas=${capas.size()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(println (str "capas=" (count (str/split (str/trim (read-line)) #"\s+"))))
```

**Qué reconocer:** `size`, `length`, `size()`, `count` son cuatro nombres para lo mismo sobre la misma
JVM, pero la unidad de arquitectura cambia radicalmente dentro de la familia. Java obliga a una clase
por archivo público; Kotlin permite funciones de nivel superior y hace de la clase una opción, no un
requisito; Scala añade `object` como módulo singleton; Clojure abandona los objetos y organiza por
**espacios de nombres de funciones puras**. La lección de diseño es que "correr sobre la JVM" no
determina la arquitectura: cuatro lenguajes con el mismo bytecode producen cuatro formas distintas de
trazar la frontera entre capas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let capas = stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "capas=%d" capas.Length
```

### VB.NET

```vbnet
Imports System

Module Arquitectura
    Sub Main()
        Dim capas = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("capas=" & capas.Length)
    End Sub
End Module
```

**Qué reconocer:** los tres comparten el mismo `String.Split` del CLR, y las tres unidades de
organización —`class`, `module`, `Module`— acaban siendo el mismo tipo estático en IL. Lo que sí es
una diferencia de diseño real es el **orden de los archivos en F#**: la compilación es secuencial y
un archivo solo puede usar lo definido antes, lo que impide dependencias circulares **por
construcción**. Es una restricción que en C# o VB.NET hay que imponer con herramientas de análisis, y
que en F# el compilador garantiza gratis: una arquitectura en capas que el lenguaje verifica en vez
de solo documentar.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La frontera entre capas es física: cabecera pública y
archivo de implementación.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string capa;
    int n = 0;
    while (std::cin >> capa) ++n;
    std::cout << "capas=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSUInteger n = 0;
        for (NSString *capa in [linea componentsSeparatedByCharactersInSet:espacios]) {
            if (capa.length > 0) n++;
        }
        printf("capas=%lu\n", (unsigned long)n);
    }
    return 0;
}
```

**Qué reconocer:** el bucle que cuenta es idéntico al de la versión en C. Donde la familia se separa
es en cómo declara una capa: C usa `.h` + `.c`, C++ añade `namespace` y clases, y Objective-C
introduce los **protocolos**, que son interfaces sin implementación y el mecanismo con el que Cocoa
desacopla vista y modelo (el patrón *delegate*). Los tres comparten un problema arquitectónico que no
existe en las familias anteriores: el `#include` es una copia textual, así que la dependencia entre
capas no es una relación declarada sino una inserción de código, y por eso la disciplina de cabeceras
—qué se expone y qué no— **es** el diseño en esta familia.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Modernizan el
`#include`: el módulo es una entidad del lenguaje, no un truco del preprocesador.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var n: usize = 0;
    while (it.next()) |_| n += 1;
    try std.io.getStdOut().writer().print("capas={d}\n", .{n});
}
```

### Nim

```nim
import std/strutils

echo "capas=" & $stdin.readLine().splitWhitespace().len
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto capas = readln().strip().split();
    writeln("capas=", capas.length);
}
```

**Qué reconocer:** en los tres el módulo se **importa como un valor**, no se pega como texto:
`@import` de Zig devuelve una estructura, `import` de Nim y D resuelve un archivo real. Eso elimina
el problema de las cabeceras de C y hace que la arquitectura sea comprobable por el compilador, igual
que en Go y Rust. Zig lleva la idea más lejos que nadie al no tener declaraciones separadas de la
implementación: no hay `.h`, no hay macros, y lo público se marca con `pub` —una sola fuente de
verdad para la frontera de la capa—. Es la misma decisión que toma Go con la mayúscula inicial y Rust
con `pub`: hacer de la visibilidad una propiedad del símbolo, no de un archivo aparte.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la arquitectura no se organiza en capas de
llamadas sino en **relaciones y reglas** que se derivan unas de otras.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Bruto),
    exclude(==(""), Bruto, Capas),
    length(Capas, N),
    format("capas=~w~n", [N]).
```

### Datalog

```datalog
% Datalog puro no imprime ni agrega; los dialectos con agregación (Soufflé) sí cuentan.
capa("web").
capa("api").
capa("datos").

capas(N) :- N = count : { capa(_) }.
```

**Qué reconocer:** `length/2` de Prolog y el `count(*)` de la versión SQL son la misma idea —una
propiedad del conjunto, no un contador que se incrementa—, y ninguno necesita un bucle. Para el
diseño, la familia propone una arquitectura distinta: no hay capas que se llamen entre sí, hay
**relaciones base** (los hechos) y **relaciones derivadas** (las reglas), que es exactamente la
diferencia entre una tabla y una vista en SQL. La estratificación de Datalog —una regla solo puede
depender de reglas de un nivel anterior— es, literalmente, una arquitectura en capas impuesta por el
motor: no puedes escribir una dependencia circular porque el programa deja de ser válido.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: partir la línea y contar. Lo que
cambia es **cuánta estructura exige el lenguaje** para alojar esas tres líneas: ninguna, una función,
una clase dentro de un paquete o un conjunto de reglas estratificadas. Eso es lo transferible.

⏮️ [Volver a la clase 149](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
