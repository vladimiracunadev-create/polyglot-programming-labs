# 🧬 El mismo programa en las familias de lenguajes — Clase 104

> [⬅️ Volver a la clase 104](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar las palabras y los caracteres de una línea de
texto— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por
los diez lenguajes del núcleo.

La entrada llega por stdin, que no es más que un archivo ya abierto. Por eso el contrato es tan
pequeño: lo que de verdad separa a las familias no es contar, sino **qué considera cada lenguaje que
hay dentro de un archivo**. Unos ven caracteres, otros ven bytes, y unos pocos te obligan a decir
cuál de las dos cosas quieres antes de dejarte leer.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un texto que puede contener espacios
- **Salida** (stdout): `palabras=<número de palabras> caracteres=<longitud de la línea>`
- **Regla:** las palabras son las partes separadas por espacios; los caracteres incluyen los espacios

| stdin | esperado |
|---|---|
| `hola mundo` | `palabras=2 caracteres=10` |
| `abc` | `palabras=1 caracteres=3` |
| `a b c d` | `palabras=4 caracteres=7` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En esta familia abrir un archivo es una sola llamada y el contenido llega como cadena. El precio de
esa comodidad es que la frontera entre texto y bytes queda escondida en un modo o una opción.

### Ruby

```ruby
linea = STDIN.gets.chomp
# File.read devuelve texto con codificación; File.binread devuelve ASCII-8BIT.
puts "palabras=#{linea.split.size} caracteres=#{linea.length}"
```

### Perl

```perl
use strict;
use warnings;

my $linea = <STDIN>;
chomp $linea;
my @palabras = split ' ', $linea;
# Sin la capa ':encoding(UTF-8)' en el open, length() cuenta bytes, no caracteres.
printf "palabras=%d caracteres=%d\n", scalar(@palabras), length($linea);
```

### Lua

```lua
-- En Lua una cadena es una secuencia de bytes: #linea cuenta bytes, siempre.
local linea = io.read("l")
local palabras = 0
for _ in linea:gmatch("%S+") do palabras = palabras + 1 end
print(string.format("palabras=%d caracteres=%d", palabras, #linea))
```

### Tcl

```tcl
gets stdin linea
# llength trata la línea como lista: colapsa los espacios repetidos.
puts "palabras=[llength $linea] caracteres=[string length $linea]"
```

### R

```r
linea <- readLines("stdin", n = 1)
palabras <- length(strsplit(linea, "\\s+")[[1]])
# nchar() cuenta caracteres; nchar(linea, type = "bytes") cuenta bytes.
cat(sprintf("palabras=%d caracteres=%d\n", palabras, nchar(linea)))
```

**Qué reconocer:** los cinco leen una línea con una sola llamada, igual que Python, pero se separan en
qué cuentan. Ruby y R distinguen carácter de byte con una opción (`binread`, `type = "bytes"`); Perl
lo decide en el `open`, con capas de E/S (`:raw` frente a `:encoding(UTF-8)`), y si te olvidas, cuenta
bytes en silencio. **Lua no tiene tipo texto**: su cadena es un vector de bytes y `#s` nunca cuenta
otra cosa, lo que la vuelve perfecta para binario y torpe para Unicode. Tcl es el opuesto: sus canales
son de texto por defecto y hay que pedir `fconfigure -translation binary` para que dejen de traducir
saltos de línea.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  // File.readAsString() decodifica; File.readAsBytes() devuelve Uint8List.
  final linea = stdin.readLineSync()!;
  final palabras = linea.split(RegExp(r'\s+')).where((s) => s.isNotEmpty).length;
  print('palabras=$palabras caracteres=${linea.length}');
}
```

### ActionScript 3

```actionscript
// El reproductor Flash no tiene stdin ni acceso libre al disco: los archivos
// llegan por FileReference, siempre con un diálogo que el usuario aprueba.
package {
    public class Conteo {
        public static function resumen(linea:String):String {
            var partes:Array = linea.split(/\s+/).filter(
                function(s:String, i:int, a:Array):Boolean { return s.length > 0; });
            return "palabras=" + partes.length + " caracteres=" + linea.length;
        }
    }
}
```

**Qué reconocer:** la familia nació en el navegador, donde no había disco, y eso todavía se nota. Dart
solo tiene archivos porque `dart:io` existe fuera del navegador, y ahí sí separa las dos operaciones
en dos métodos distintos: `readAsString` frente a `readAsBytes`. ActionScript se quedó en el otro
lado de la frontera: el binario existe (`ByteArray`), pero abrir un archivo es una acción del usuario,
no del programa. Ojo con `length`: en ambos cuenta unidades UTF-16, así que un emoji suma dos.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM puso la distinción texto/binario en el
**sistema de tipos**: `Reader`/`Writer` mueven caracteres, `InputStream`/`OutputStream` mueven bytes,
y para pasar de unos a otros hay que nombrar la codificación.

### Kotlin

```kotlin
fun main() {
    // File.readText() usa Reader; File.readBytes() devuelve ByteArray.
    val linea = readLine()!!
    val palabras = linea.split(Regex("\\s+")).filter { it.isNotEmpty() }.size
    println("palabras=$palabras caracteres=${linea.length}")
}
```

### Scala

```scala
object Conteo extends App {
  // scala.io.Source envuelve un Reader de Java y pide Codec implícito.
  val linea = scala.io.StdIn.readLine()
  val palabras = linea.split("\\s+").count(_.nonEmpty)
  println(s"palabras=$palabras caracteres=${linea.length}")
}
```

### Groovy

```groovy
// Groovy añade File.text y File.bytes: la misma dualidad en dos propiedades.
def linea = System.in.newReader().readLine()
def palabras = linea.split(/\s+/).findAll { it }.size()
println "palabras=$palabras caracteres=${linea.length()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; slurp devuelve texto; para bytes hay que bajar a los flujos de Java.
(let [linea (read-line)
      palabras (count (remove str/blank? (str/split linea #"\s+")))]
  (println (str "palabras=" palabras " caracteres=" (count linea))))
```

**Qué reconocer:** los cuatro terminan en las mismas clases de `java.io` y `java.nio`, así que heredan
su regla: no puedes leer texto sin decidir una codificación, aunque el valor por defecto la esconda.
Kotlin y Groovy tapan la ceremonia con propiedades (`readText`/`readBytes`, `.text`/`.bytes`) que
siguen siendo dos caminos distintos. Clojure ofrece `slurp` para texto y nada para binario: cuando
necesitas bytes, se cae al Java de debajo sin disimulo. Y en los cuatro `length`/`count` sobre una
cadena cuenta unidades UTF-16, igual que en Java.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// File.ReadAllText frente a File.ReadAllBytes: la BCL repite el par texto/bytes.
let linea = stdin.ReadLine()
let palabras = linea.Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "palabras=%d caracteres=%d" palabras.Length linea.Length
```

### VB.NET

```vbnet
Module Conteo
    Sub Main()
        Dim linea = Console.ReadLine()
        Dim palabras = linea.Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        ' StreamReader lee caracteres; FileStream lee bytes. Nunca se mezclan.
        Console.WriteLine($"palabras={palabras.Length} caracteres={linea.Length}")
    End Sub
End Module
```

**Qué reconocer:** el CLR copia el reparto de la JVM —`StreamReader`/`StreamWriter` para caracteres,
`FileStream` para bytes— y le añade una trampa propia: desde .NET Core la codificación por defecto es
UTF-8 **sin BOM**, mientras que en el .NET Framework antiguo era UTF-8 con BOM, y ese preámbulo de
tres bytes aparecía en los archivos generados. `String.Length` cuenta unidades UTF-16 en los dos
lenguajes, porque la cadena de .NET es la misma.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí no hay tipo texto: un archivo es una tira de
bytes y la interpretación la pone quien lee.

### C++

```cpp
#include <iostream>
#include <sstream>
#include <string>

int main() {
    // std::ifstream f(ruta, std::ios::binary) es el único cambio para binario.
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream ss(linea);
    std::string palabra;
    int palabras = 0;
    while (ss >> palabra) ++palabras;
    std::cout << "palabras=" << palabras << " caracteres=" << linea.size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        // Foundation obliga a decirlo: los bytes llegan como NSData y hay que
        // decodificarlos a NSString nombrando la codificación.
        NSData *bytes = [[NSFileHandle fileHandleWithStandardInput] availableData];
        NSString *linea = [[[NSString alloc] initWithData:bytes encoding:NSUTF8StringEncoding]
                           stringByTrimmingCharactersInSet:[NSCharacterSet newlineCharacterSet]];
        NSArray *partes = [linea componentsSeparatedByCharactersInSet:
                           [NSCharacterSet whitespaceCharacterSet]];
        NSUInteger palabras = [[partes filteredArrayUsingPredicate:
                                [NSPredicate predicateWithFormat:@"length > 0"]] count];
        printf("palabras=%lu caracteres=%lu\n",
               (unsigned long)palabras, (unsigned long)[linea length]);
    }
    return 0;
}
```

**Qué reconocer:** `std::string` de C++ y `char *` de C son lo mismo que en Lua —bytes— y por eso
`size()` mide bytes; la `"b"` de `fopen` y `std::ios::binary` solo importan en Windows, donde el
sistema traduce `\n` a `\r\n`. Objective-C es el contraste más limpio de toda la página: `NSData` y
`NSString` son **tipos distintos**, no puedes pasar uno donde va el otro, y convertir exige nombrar la
codificación. Esa separación es exactamente la que Java, .NET y Python hicieron después.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con la lectura de archivos a la vista: buffers, tamaños y errores explícitos.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    // Todo es []u8: no hay tipo texto, y el búfer lo reservas tú.
    var buf: [4096]u8 = undefined;
    const cruda = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const linea = std.mem.trim(u8, cruda, "\r");
    var it = std.mem.tokenizeAny(u8, linea, " \t");
    var palabras: usize = 0;
    while (it.next()) |_| palabras += 1;
    try std.io.getStdOut().writer().print(
        "palabras={d} caracteres={d}\n", .{ palabras, linea.len });
}
```

### Nim

```nim
import std/strutils

# readFile devuelve string (bytes) y readAll lo mismo: Nim no separa los tipos.
let linea = stdin.readLine()
echo "palabras=", linea.splitWhitespace().len, " caracteres=", linea.len
```

### D

```d
import std.stdio, std.string, std.array;

void main() {
    // std.file.readText valida UTF-8 y devuelve string; std.file.read devuelve
    // void[], que se moldea a ubyte[] cuando lo que quieres son bytes.
    string linea = readln().chomp();
    auto palabras = linea.split().length;
    writefln("palabras=%d caracteres=%d", palabras, linea.length);
}
```

**Qué reconocer:** Zig no tiene tipo cadena en absoluto —un texto es un `[]u8` y punto—, así que la
pregunta "¿texto o binario?" ni siquiera se plantea: siempre es binario y la interpretación es tuya.
Nim está en el mismo sitio con azúcar de scripting. D es el único de los tres que sí separa: `string`
es UTF-8 **validado** e inmutable y `ubyte[]` es binario, con funciones distintas (`readText` frente a
`read`) que fallan de forma distinta ante bytes inválidos. Y como en Go, `linea.length` es bytes: es
la familia entera la que cuenta bytes, no caracteres.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El archivo, aquí, no es un objeto que se abre:
es una fuente de hechos que el motor carga.

### Prolog

```prolog
:- initialization(main, main).

main :-
    % read_line_to_string da texto; read_line_to_codes da la lista de códigos,
    % y set_stream(S, encoding(octet)) convierte el flujo en binario.
    read_line_to_string(user_input, Linea),
    split_string(Linea, " \t", " \t", Partes0),
    exclude(==(""), Partes0, Partes),
    length(Partes, N),
    string_length(Linea, L),
    format("palabras=~d caracteres=~d~n", [N, L]).
```

### Datalog

```datalog
% Datalog puro no abre archivos ni tiene efectos: la carga de datos ocurre fuera
% del programa. En Soufflé se declara la relación y el motor la lee del disco.
.decl palabra(linea: symbol, pos: number, texto: symbol)
.input palabra

.decl conteo(linea: symbol, n: number)
conteo(l, n) :- palabra(l, _, _), n = count : { palabra(l, _, _) }.
.output conteo
```

**Qué reconocer:** Prolog conserva la dualidad bajo otros nombres —`string` frente a `codes`, y un
flujo que se declara `octet` para trabajar con bytes— pero sigue siendo un lenguaje que abre y lee.
Datalog renuncia del todo: no hay `open`, no hay orden de lectura, no hay efectos. El archivo entra
por una **declaración** (`.input`) y el motor decide cuándo leerlo, que es la misma renuncia que hace
SQL cuando cargas una tabla y dejas de saber en qué orden se recorrió el disco.

---

## Y de vuelta a la clase

Veinte lenguajes y un solo archivo —stdin— demuestran que "leer un archivo" no significa lo mismo en
todas partes. Hay tres posturas: la que solo conoce bytes (C, Lua, Zig), la que solo te da texto y
esconde la codificación (Ruby, Tcl, Clojure), y la que te obliga a elegir con dos tipos distintos
(Objective-C con `NSData`, la JVM con `Reader`/`InputStream`, D con `string` frente a `ubyte[]`).
Saber en cuál de las tres cae un lenguaje que nunca has visto es lo transferible.

⏮️ [Volver a la clase 104](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
