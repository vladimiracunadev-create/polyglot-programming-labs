# 🧬 El mismo programa en las familias de lenguajes — Clase 048

> [⬅️ Volver a la clase 048](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —saludar e informar la longitud de una palabra—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin): una palabra ASCII, sin espacios
- **Salida** (stdout): `hola=<palabra> longitud=<número de caracteres>`
- **Regla:** `longitud = |palabra|`

| stdin | esperado |
|---|---|
| `Ada` | `hola=Ada longitud=3` |
| `Bo` | `hola=Bo longitud=2` |
| `polyglot` | `hola=polyglot longitud=8` |

Las tres preguntas que separan a estos veinte lenguajes son siempre las mismas: **¿la cadena se puede
modificar?**, **¿se puede interpolar una variable dentro del literal?** y **¿qué cuenta exactamente
`longitud`: bytes o caracteres?**

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La cadena es el tipo estrella de esta familia, y casi todos ofrecen interpolación directa en el
literal. La sorpresa está en la mutabilidad, donde no coinciden entre sí.

### Ruby

```ruby
w = STDIN.gets.strip
# Las cadenas de Ruby SÍ son mutables (w << "!" las modifica en sitio),
# al contrario que las de Python. `freeze` es lo que las congela.
puts "hola=#{w} longitud=#{w.length}"
```

### Perl

```perl
use strict;
use warnings;

chomp(my $w = <STDIN>);
# La interpolación de Perl es la abuela de todas: la variable va tal cual
# dentro de las comillas dobles, sin llaves ni marcadores.
print "hola=$w longitud=", length($w), "\n";
```

### Lua

```lua
local w = io.read("l")
-- Lua no interpola: hay que concatenar con `..` o usar string.format.
-- Sus cadenas son inmutables e internadas, así que comparar es comparar punteros.
print(string.format("hola=%s longitud=%d", w, #w))
```

### Tcl

```tcl
set w [string trim [gets stdin]]
# En Tcl todo valor es una cadena, así que no hay conversión que hacer.
puts "hola=$w longitud=[string length $w]"
```

### R

```r
w <- trimws(readLines("stdin", n = 1))
# nchar() cuenta caracteres; nchar(w, type = "bytes") contaría bytes.
cat(sprintf("hola=%s longitud=%d\n", w, nchar(w)))
```

**Qué reconocer:** Perl, Ruby y Tcl interpolan la variable dentro de las comillas igual que hace la
f-string de Python; Lua y R no tienen interpolación y recurren al formateo posicional. En
mutabilidad la familia se parte: las cadenas de Ruby **sí** se pueden modificar en sitio, las de Lua
son inmutables e internadas, y en Tcl la pregunta casi pierde sentido porque el lenguaje lo trata
todo como cadena. Fíjate en el `#w` de Lua: el mismo operador de longitud que usa para las tablas.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final w = stdin.readLineSync()!.trim();
  // La interpolación de Dart usa $nombre o ${expresión}, como las plantillas de JS.
  print('hola=$w longitud=${w.length}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
// No hay interpolación ni plantillas: solo concatenación con +.
package {
    public class Saludo {
        public static function saludar(w:String):String {
            return "hola=" + w + " longitud=" + w.length;
        }
    }
}
```

**Qué reconocer:** los dos comparten con JavaScript el `String` inmutable y la propiedad `length`
—sin paréntesis, porque no es un método—. La diferencia es de época: ActionScript se congeló antes de
que existieran las plantillas literales, así que solo concatena; Dart nació después y adoptó el
`$variable` directo, sin necesidad de comillas especiales. Y en los dos, `length` cuenta **unidades
UTF-16**, no caracteres.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El `String` de la JVM es inmutable, está
internado en un *pool* y tiene una clase hermana mutable, `StringBuilder`, para cuando concatenar en
bucle sale caro.

### Kotlin

```kotlin
fun main() {
    val w = readLine()!!.trim()
    println("hola=$w longitud=${w.length}")
}
```

### Scala

```scala
object Saludo extends App {
  val w = scala.io.StdIn.readLine().trim
  // El prefijo s"" habilita la interpolación; f"" añade formateo tipo printf.
  println(s"hola=$w longitud=${w.length}")
}
```

### Groovy

```groovy
def w = System.in.newReader().readLine().trim()
// Las comillas dobles crean un GString interpolable; las simples, un String normal.
println "hola=$w longitud=${w.length()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure no tiene interpolación: se compone con str o con format.
(let [w (str/trim (read-line))]
  (println (str "hola=" w " longitud=" (count w))))
```

**Qué reconocer:** los cuatro usan por debajo el mismo `java.lang.String` inmutable, así que la
longitud sale del mismo sitio. Lo que añaden es azúcar sintáctico que Java tardó veinte años en
tener: Kotlin, Scala y Groovy interpolan con `$`, cada uno con su matiz —Scala exige el prefijo `s`,
Groovy distingue comillas simples de dobles—. Clojure renuncia a todo eso y compone con `str`, fiel a
su principio de que la sintaxis debe ser una sola: la llamada a función.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let w = stdin.ReadLine().Trim()
// printfn está comprobado en tiempo de compilación: %s solo acepta cadenas.
printfn "hola=%s longitud=%d" w w.Length
```

### VB.NET

```vbnet
Module Saludo
    Sub Main()
        Dim w = Console.ReadLine().Trim()
        ' VB.NET adoptó la interpolación $"" de C# en 2015; antes se usaba & para concatenar.
        Console.WriteLine($"hola={w} longitud={w.Length}")
    End Sub
End Module
```

**Qué reconocer:** el `System.String` del CLR es inmutable e internado, igual que el de la JVM, y los
tres lenguajes comparten `Length` como propiedad. La curiosidad es F#: su `printfn` no es una función
que recibe una cadena cualquiera, sino que el **compilador lee el literal de formato** y verifica que
los argumentos casen con `%s` y `%d`. Es el mismo control de tipos que en C queda en manos del
programador con `printf`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C no hay tipo cadena: hay un puntero a bytes
terminados en `\0`, y la longitud se calcula recorriéndolos uno a uno.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string w;
    std::cin >> w;
    // std::string SÍ es mutable y guarda su tamaño: size() es O(1),
    // frente al strlen de C que recorre hasta el terminador.
    std::cout << "hola=" << w << " longitud=" << w.size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[256];
        scanf("%255s", buf);
        NSString *w = [NSString stringWithUTF8String:buf];
        // NSString es inmutable; la variante que se modifica es NSMutableString.
        printf("hola=%s longitud=%lu\n", buf, (unsigned long)[w length]);
    }
    return 0;
}
```

**Qué reconocer:** los dos siguen pudiendo usar el `char*` de C —ahí sigue el búfer de 256 bytes—,
pero cada uno construyó encima una abstracción distinta. C++ hizo su `std::string` **mutable** y con
la longitud guardada, así que crece y se modifica sin drama. Objective-C copió el modelo de Smalltalk
y separó las clases: `NSString` inmutable y `NSMutableString` mutable, una pareja que se repite en
todo Foundation (`NSArray`/`NSMutableArray`) y que reapareció después en Swift.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Cadenas inmutables en
UTF-8, con la longitud medida en **bytes** y no en caracteres —una decisión honesta que obliga a
elegir explícitamente cuando quieres contar otra cosa—.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    // No existe un tipo cadena: w es un slice []const u8 y .len cuenta bytes.
    const w = std.mem.trim(u8, linea, " \r\n");
    try std.io.getStdOut().writer().print("hola={s} longitud={d}\n", .{ w, w.len });
}
```

### Nim

```nim
import std/[strutils, strformat]

let w = stdin.readLine().strip()
# Las cadenas de Nim son mutables y de tamaño variable, como un seq[char].
# &"" es interpolación en tiempo de COMPILACIÓN: la plantilla se expande al compilar.
echo &"hola={w} longitud={w.len}"
```

### D

```d
import std.stdio, std.string;

void main() {
    // string en D es un alias de immutable(char)[]: la inmutabilidad
    // está en el sistema de tipos, no en una convención de la biblioteca.
    const w = readln().strip();
    writefln("hola=%s longitud=%d", w, w.length);
}
```

**Qué reconocer:** los tres miden la longitud en bytes, como Go y Rust, y en ASCII eso coincide con
el número de caracteres —fuera de ASCII, no—. Se separan en la mutabilidad: Zig trabaja con
*slices* crudos, Nim hace sus cadenas mutables como cualquier secuencia, y D codifica la
inmutabilidad **en el propio tipo** (`immutable(char)[]`), de modo que el compilador la garantiza en
vez de confiar en la disciplina. Fíjate también en el `&""` de Nim: la interpolación se resuelve al
compilar, sin coste en ejecución.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Nada se modifica en sitio: se declara una
relación entre la palabra y su longitud, y el motor la resuelve.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(W), Linea),
    string_length(W, N),
    format("hola=~w longitud=~d~n", [W, N]).
```

### Datalog

```datalog
% Datalog no manipula cadenas ni tiene E/S: no existe una función de longitud.
% Lo más cercano es declarar el par palabra/longitud como hecho y relacionarlo.
palabra("Ada", 3).
palabra("Bo", 2).
palabra("polyglot", 8).

entrada("Ada").

saludo(W, N) :- entrada(W), palabra(W, N).
```

**Qué reconocer:** en Prolog una cadena ligada a una variable **no se reasigna nunca**: la
inmutabilidad no es una propiedad del tipo sino del modelo de cómputo entero, porque `W` es un
nombre para un valor, no una casilla de memoria. Datalog es aún más restrictivo —sin funciones de
cadena, la longitud tiene que venir dada como hecho—, y esa limitación es deliberada: es lo que
garantiza que toda consulta termine. Es el mismo intercambio que hace SQL cuando te obliga a
declarar qué quieres en vez de cómo obtenerlo.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer una palabra, contar sus
caracteres y componer una línea de salida. Lo que cambia es la **forma** y, en algunos casos, las
**garantías**. Eso es lo transferible.

⏮️ [Volver a la clase 048](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
