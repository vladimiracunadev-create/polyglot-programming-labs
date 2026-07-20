# 🧬 El mismo programa en las familias de lenguajes — Clase 160

> [⬅️ Volver a la clase 160](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —construir el contrato de un endpoint a partir del
método y el recurso— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `metodo recurso`
- **Salida** (stdout): `contrato=<METODO> /<recurso>`
- **Regla:** combinar método y recurso en un endpoint

| stdin | esperado |
|---|---|
| `GET users` | `contrato=GET /users` |
| `POST items` | `contrato=POST /items` |
| `PUT data` | `contrato=PUT /data` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Familia de los contratos verificados **en ejecución**: nada impide llamar a un endpoint que no
existe hasta que el servidor responde 404.

### Ruby

```ruby
metodo, recurso = STDIN.gets.split
puts "contrato=#{metodo} /#{recurso}"
```

### Perl

```perl
my ($metodo, $recurso) = split ' ', <STDIN>;
printf "contrato=%s /%s\n", $metodo, $recurso;
```

### Lua

```lua
local metodo, recurso = io.read("l"):match("(%S+)%s+(%S+)")
print(string.format("contrato=%s /%s", metodo, recurso))
```

### Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] metodo recurso
puts "contrato=$metodo /$recurso"
```

### R

```r
p <- scan("stdin", what = "", nmax = 2, quiet = TRUE)
cat(sprintf("contrato=%s /%s\n", p[1], p[2]))
```

**Qué reconocer:** los cinco construyen el endpoint como texto, y esa es exactamente la relación de
esta familia con los contratos: el esquema no existe en el lenguaje, existe en un documento aparte.
Ruby y Perl traen JSON en la biblioteca estándar (`json`, `JSON::PP`), de modo que pueden validar el
cuerpo de una respuesta sin instalar nada; **Lua no trae ninguno** y necesita dkjson o lua-cjson
antes siquiera de leer un contrato. La diferencia se agrava con los tipos: Lua anterior a 5.3 y R
tratan todo número como coma flotante doble, así que un `id` de 64 bits declarado como `int64` en el
esquema **llega redondeado** aunque el contrato dijera otra cosa. De los cinco solo Ruby tiene
implementación oficial de gRPC; los demás viven de REST y de la disciplina del programador.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia donde el contrato de API se escribe como tipo y se comprueba en el editor.

### Dart

```dart
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('contrato=${p[0]} /${p[1]}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la
// construcción del endpoint que luego consumiría un URLRequest.
package {
    public class Contrato {
        public static function endpoint(metodo:String, recurso:String):String {
            return "contrato=" + metodo + " /" + recurso;
        }
    }
}
```

**Qué reconocer:** Dart hereda de TypeScript la idea de describir la respuesta como tipo, pero lo
lleva más lejos: sus paquetes generan la clase a partir de un esquema OpenAPI o `.proto` y el
compilador rechaza el campo mal escrito. ActionScript representa la etapa anterior de la web —tipos
declarados (`String`, `int`, `Number`) pero un contrato de red que es solo una URL construida a
mano— y expone la trampa de la familia: su `Number` es doble, así que el `int64` del esquema no
sobrevive al viaje. Ninguno de los dos puede expresar una fecha en JSON, porque **JSON no tiene tipo
fecha**: el contrato se cierra acordando ISO 8601 como cadena, y ese acuerdo es parte del esquema,
no del lenguaje.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El mundo donde nació la generación de código a
partir de esquema —WSDL primero, `.proto` después.

### Kotlin

```kotlin
fun main() {
    val (metodo, recurso) = readLine()!!.trim().split(Regex("\\s+"))
    println("contrato=$metodo /$recurso")
}
```

### Scala

```scala
object Contrato extends App {
  val Array(metodo, recurso) = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"contrato=$metodo /$recurso")
}
```

### Groovy

```groovy
def (metodo, recurso) = System.in.newReader().readLine().trim().split(/\s+/)
println "contrato=$metodo /$recurso"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[metodo recurso] (str/split (str/trim (read-line)) #"\s+")]
  (println (str "contrato=" metodo " /" recurso)))
```

**Qué reconocer:** los cuatro comparten el mismo `protoc` y el mismo runtime de gRPC de Java, así que
un `.proto` compila para todos y el `int64` del esquema llega como `long` exacto —la familia que
menos pierde en el cruce. Lo que cambia es cómo se declara el contrato en el propio lenguaje: Kotlin
usa `data class` con `@Serializable`, Scala tipos algebraicos con `sealed trait`, y Clojure se sale
del molde con **spec** y **Malli**, que describen la forma del dato como valores en tiempo de
ejecución en vez de como tipos en compilación. Es la misma diferencia que separa OpenAPI —un
documento que se valida cuando llega la petición— de Protobuf, que se valida cuando compilas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let partes = stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "contrato=%s /%s" partes.[0] partes.[1]
```

### VB.NET

```vbnet
Imports System

Module Contrato
    Sub Main()
        Dim p = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine($"contrato={p(0)} /{p(1)}")
    End Sub
End Module
```

**Qué reconocer:** los tres comparten ASP.NET Core, donde el contrato REST se declara con atributos
sobre el método (`[HttpGet("/users")]`) y el propio framework genera el documento OpenAPI a partir
de las firmas: el código **es** el esquema. `Grpc.Tools` compila el `.proto` en el mismo proyecto,
sin paso aparte. F# aporta el matiz honesto: sus uniones discriminadas describen respuestas
"o esto o aquello" con una precisión que ni OpenAPI ni Protobuf pueden expresar sin rodeos, así que
el contrato publicado siempre es **más pobre que el tipo interno**. VB.NET consume el mismo
generador que C# porque el contrato vive en el CLR, no en la sintaxis.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin framework: el contrato son las cabeceras que
declaran las estructuras.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string metodo, recurso;
    std::cin >> metodo >> recurso;
    std::cout << "contrato=" << metodo << " /" << recurso << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSFileHandle *in = [NSFileHandle fileHandleWithStandardInput];
        NSString *linea = [[NSString alloc] initWithData:[in availableData]
                                                encoding:NSUTF8StringEncoding];
        NSArray<NSString *> *p = [[linea stringByTrimmingCharactersInSet:
            [NSCharacterSet whitespaceAndNewlineCharacterSet]]
            componentsSeparatedByString:@" "];
        printf("contrato=%s /%s\n", [p[0] UTF8String], [p[1] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ninguno de los dos trae JSON ni cliente HTTP en la biblioteca estándar del
lenguaje, y por eso esta familia es la que más se apoya en **esquemas compilados**: `protoc` genera
clases C++ con los campos tipados y gRPC nació precisamente aquí. Objective-C rompe la regla gracias
a Foundation, que sí trae `NSURLSession` y `NSJSONSerialization`; el precio es que la deserialización
devuelve `NSNumber` y `NSDictionary` genéricos, sin contrato verificable, justo lo contrario de lo
que ofrece el `.proto`. Ambos comparten con C el detalle que el contrato de red no menciona nunca:
en un `struct` el **orden y el relleno de los campos** importan, y por eso el formato del cable no
puede ser el volcado de memoria.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Lenguajes nacidos
cuando el contrato de API ya era un problema de primera clase.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    const metodo = it.next().?;
    const recurso = it.next().?;
    try std.io.getStdOut().writer().print("contrato={s} /{s}\n", .{ metodo, recurso });
}
```

### Nim

```nim
import std/strutils

let p = stdin.readLine().splitWhitespace()
echo "contrato=", p[0], " /", p[1]
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto p = readln().strip().split();
    writefln("contrato=%s /%s", p[0], p[1]);
}
```

**Qué reconocer:** los tres **traen JSON en la biblioteca estándar** —`std.json` en Zig y en D,
`std/json` en Nim—, así que pueden validar un contrato REST sin dependencias, algo que C, C++ y Lua
no pueden. Y los tres deserializan contra un tipo declarado: Zig lo resuelve con `comptime`, de modo
que el esquema es literalmente una `struct` conocida en compilación y el `int64` del contrato llega
como `i64` exacto. Para gRPC dependen de generadores de la comunidad, no oficiales, lo que ilustra
una verdad incómoda de esta clase: **el contrato lo define quien tiene el generador de código**, y
los lenguajes jóvenes lo consumen antes de poder definirlo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El esquema no acompaña al dato: **es** el dato.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", [Metodo, Recurso]),
    format("contrato=~w /~w~n", [Metodo, Recurso]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni concatenación: el contrato se declara como hecho
% y la regla deriva qué endpoints son válidos. La forma de la relación
% (aridad y tipos) es todo el esquema que existe.
metodo_recurso("GET", "users").

contrato(M, R) :- metodo_recurso(M, R).
```

**Qué reconocer:** en Prolog el contrato de un predicado se documenta con su **modo** —qué argumentos
entran ligados y cuáles salen—, y `library(http/json)` traduce entre términos y JSON cuando hace
falta hablar REST. Datalog es la versión más pura de la idea que sostiene esta clase: una relación
declarada con nombre, aridad y tipos **es** un esquema, y ninguna regla puede referirse a un predicado
que no exista. Lo mismo que hace una tabla de SQL o un `message` de Protobuf, solo que sin la capa de
serialización en medio, porque aquí no hay red que cruzar ni tipos que puedan perderse.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer el método, leer el recurso,
componer el endpoint. Lo que cambia es **cuándo** se comprueba que ese contrato es correcto —al
compilar, al arrancar o cuando el servidor devuelve 404— y cuánto del tipo original sobrevive al
documento que lo describe. Eso es lo transferible.

⏮️ [Volver a la clase 160](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
