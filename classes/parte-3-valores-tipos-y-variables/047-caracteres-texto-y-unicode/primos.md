# 🧬 El mismo programa en las familias de lenguajes — Clase 047

> [⬅️ Volver a la clase 047](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —un carácter y su punto de código— resuelto por los
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

- **Entrada** (stdin): un único carácter ASCII
- **Salida** (stdout): `char=<c> codigo=<punto de código>`
- **Regla:** `codigo = punto_de_codigo(c)`

| stdin | esperado |
|---|---|
| `A` | `char=A codigo=65` |
| `z` | `char=z codigo=122` |
| `0` | `char=0 codigo=48` |

El contrato se limita a ASCII **a propósito**: es el único rango donde los veinte lenguajes coinciden
sin discusión. En cuanto se sale de ahí, cada familia responde una cosa distinta, y los comentarios
del código señalan dónde.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de estos lenguajes tiene un tipo *carácter*: un carácter es una cadena de longitud uno. Lo
que cambia entre ellos es si esa cadena guarda **bytes** o **puntos de código**.

### Ruby

```ruby
c = STDIN.getc
# String#ord devuelve el punto de código según el encoding de la cadena.
puts "char=#{c} codigo=#{c.ord}"
```

### Perl

```perl
use strict;
use warnings;

my $c = substr(<STDIN>, 0, 1);
# Sin capas de E/S, ord() devuelve el BYTE. Para puntos de código Unicode
# haría falta `binmode(STDIN, ":encoding(UTF-8)")` antes de leer.
printf "char=%s codigo=%d\n", $c, ord($c);
```

### Lua

```lua
local c = io.read(1)
-- Lua no conoce Unicode: las cadenas son bytes y string.byte devuelve un byte.
-- Desde 5.3 existe utf8.codepoint(c) para el punto de código real.
print(string.format("char=%s codigo=%d", c, string.byte(c)))
```

### Tcl

```tcl
set c [string index [gets stdin] 0]
# Tcl es de los pocos que guarda las cadenas como puntos de código desde el diseño:
# scan %c los devuelve directamente, sin capas de codificación de por medio.
scan $c %c codigo
puts "char=$c codigo=$codigo"
```

### R

```r
c <- substr(readLines("stdin", n = 1), 1, 1)
cat(sprintf("char=%s codigo=%d\n", c, utf8ToInt(c)))
```

**Qué reconocer:** los cinco tratan el carácter como una cadena, igual que Python, pero se separan en
la pregunta de fondo: **¿qué unidad cuenta?** Tcl y R responden «puntos de código» sin condiciones.
Lua responde «bytes» siempre. Perl y Ruby responden lo uno o lo otro **según cómo se haya abierto el
flujo**: el mismo `ord` da 233 o 195 para una `é` dependiendo de si la entrada se decodificó. En
ASCII las cinco respuestas coinciden, y por eso el contrato de la clase se queda ahí.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final c = stdin.readLineSync()!.substring(0, 1);
  // runes recorre puntos de código; codeUnits recorrería unidades UTF-16.
  print('char=$c codigo=${c.runes.first}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
// charCodeAt devuelve una unidad UTF-16, no un punto de código, igual que en JavaScript.
package {
    public class Caracter {
        public static function describir(s:String):String {
            return "char=" + s.charAt(0) + " codigo=" + s.charCodeAt(0);
        }
    }
}
```

**Qué reconocer:** el `charCodeAt` de ActionScript es literalmente el de JavaScript, con su misma
limitación: cuenta **unidades UTF-16**, así que un emoji devuelve la mitad de un par suplente. Dart
nació después del problema y ofrece las dos vistas con nombres distintos —`codeUnits` frente a
`runes`— para que el programador declare cuál quiere. Es la misma corrección que JavaScript incorporó
más tarde con `codePointAt`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El `char` de la JVM son 16 bits fijos, una
decisión de 1995 que se tomó cuando parecía que Unicode cabría entero en ellos.

### Kotlin

```kotlin
fun main() {
    val c = readLine()!![0]
    println("char=$c codigo=${c.code}")
}
```

### Scala

```scala
object Caracter extends App {
  val c = scala.io.StdIn.readLine().charAt(0)
  println(s"char=$c codigo=${c.toInt}")
}
```

### Groovy

```groovy
def c = System.in.newReader().readLine().charAt(0)
println "char=$c codigo=${(int) c}"
```

### Clojure

```clojure
;; java.lang.Character envuelto: (int c) desempaqueta la unidad UTF-16.
(let [c (first (read-line))]
  (println (str "char=" c " codigo=" (int c))))
```

**Qué reconocer:** los cuatro heredan el mismo `char` de 16 bits, y por eso los cuatro tienen el
mismo techo: para cualquier carácter fuera del plano básico hace falta `codePointAt`, porque un
`char` solo no alcanza. Kotlin es el único que renombró la conversión: `c.code` en vez de `c.toInt()`,
precisamente para dejar de sugerir que un carácter «es» un número. Scala y Groovy conservan el
`(int)` clásico de Java.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let c = stdin.ReadLine().[0]
printfn "char=%c codigo=%d" c (int c)
```

### VB.NET

```vbnet
Module Caracter
    Sub Main()
        Dim c As Char = Console.ReadLine()(0)
        ' AscW conserva el nombre del BASIC clásico pero devuelve la unidad UTF-16;
        ' Asc(), su hermano antiguo, dependía de la página de códigos del sistema.
        Console.WriteLine($"char={c} codigo={AscW(c)}")
    End Sub
End Module
```

**Qué reconocer:** el `System.Char` del CLR es exactamente el mismo modelo que el de la JVM —16 bits,
UTF-16—, así que las trampas son idénticas. Lo curioso está en VB.NET: mantiene `Asc` y `AscW` como
funciones sueltas, restos del BASIC de los años ochenta, donde la `W` de *wide* marca la versión que
sí entiende Unicode. F#, en cambio, tiene un especificador `%c` propio en su `printfn`, algo que ni
C# ni VB.NET ofrecen.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C el carácter **es** un entero pequeño: no hay
diferencia real entre `'A'` y `65`.

### C++

```cpp
#include <iostream>

int main() {
    char c;
    std::cin >> c;
    // char es un entero de 8 bits: basta promoverlo para ver su código.
    std::cout << "char=" << c << " codigo=" << static_cast<int>(c) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int c = getchar();
        // getchar devuelve int para poder distinguir EOF (-1) de un byte válido.
        // NSString usaría unichar (UTF-16); para ASCII el byte de C basta.
        printf("char=%c codigo=%d\n", c, c);
    }
    return 0;
}
```

**Qué reconocer:** ambos conservan intacta la ecuación de C, *carácter igual a byte igual a entero*,
y por eso la conversión al código no cuesta nada: no hay nada que convertir, solo hay que pedirle a
la salida que lo imprima como número. C++ añadió después `char8_t`, `char16_t` y `char32_t` para
distinguir unidades de codificación; Objective-C resolvió lo mismo subiendo un piso, con `NSString` y
`unichar`, en lugar de tocar el tipo primitivo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos tomaron la misma
decisión moderna: las cadenas son **UTF-8** y el tipo carácter, cuando existe, es un punto de código
completo (`rune` en Go, `char` de 4 bytes en Rust).

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    const c = try std.io.getStdIn().reader().readByte();
    // Zig no tiene tipo carácter: u8 es un byte y las cadenas son []const u8 en UTF-8.
    // Para un punto de código real habría que decodificar con std.unicode.
    try std.io.getStdOut().writer().print("char={c} codigo={d}\n", .{ c, c });
}
```

### Nim

```nim
import std/strformat

let c = stdin.readLine()[0]
# `char` en Nim es un byte; el tipo Unicode se llama Rune y vive en std/unicode.
echo &"char={c} codigo={ord(c)}"
```

### D

```d
import std.stdio, std.string, std.range;

void main() {
    // D distingue char (UTF-8), wchar (UTF-16) y dchar (punto de código).
    // `front` sobre una cadena decodifica automáticamente y devuelve dchar.
    dchar c = readln().strip().front;
    writefln("char=%s codigo=%d", c, cast(uint) c);
}
```

**Qué reconocer:** los tres almacenan UTF-8 como Go y Rust, pero se reparten distinto la
responsabilidad de decodificar. Zig y Nim son deliberadamente crudos: `u8`/`char` es un byte, y si
quieres puntos de código los pides tú (`std.unicode`, `Rune`). D va al otro extremo y **decodifica
solo** al recorrer una cadena —de ahí que `front` devuelva un `dchar` de 32 bits—, una comodidad que
la propia comunidad de D discute porque cuesta rendimiento sin avisar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El carácter no es un tipo especial: es un dato
más de una tabla o un término más de una relación.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    string_chars(Linea, [C | _]),
    % char_code es una relación bidireccional: sirve para ir del carácter al
    % código y también al revés, según cuál de los dos argumentos esté ligado.
    char_code(C, Codigo),
    format("char=~w codigo=~d~n", [C, Codigo]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni funciones sobre caracteres: no existe un "ord".
% Lo más cercano es declarar la tabla de códigos como hechos y consultarla.
codigo('A', 65).
codigo('z', 122).
codigo('0', 48).

entrada('A').

respuesta(C, N) :- entrada(C), codigo(C, N).
```

**Qué reconocer:** `char_code(C, Codigo)` es la mejor demostración de qué significa «relación» en
lugar de «función»: el mismo predicado convierte en las dos direcciones porque no tiene entrada ni
salida fijas, solo argumentos que pueden estar ligados o libres. Datalog no llega ni ahí —sin
funciones aritméticas ni de cadena, la correspondencia carácter/código tiene que **enumerarse a
mano**—, y eso deja a la vista la misma frontera que encuentras en SQL: lo que no está en una tabla,
no se puede consultar.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer un carácter y mostrar el
número que lo representa. Lo que cambia es la **forma** y, en algunos casos, las **garantías**. Eso
es lo transferible.

⏮️ [Volver a la clase 047](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
