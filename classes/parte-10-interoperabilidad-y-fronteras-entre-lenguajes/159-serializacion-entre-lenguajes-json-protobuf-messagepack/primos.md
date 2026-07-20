# 🧬 El mismo programa en las familias de lenguajes — Clase 159

> [⬅️ Volver a la clase 159](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —serializar un par clave/valor— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `clave valor`
- **Salida** (stdout): `serializado=<clave>:<valor>`
- **Regla:** unir clave y valor con `:`

| stdin | esperado |
|---|---|
| `x 5` | `serializado=x:5` |
| `edad 30` | `serializado=edad:30` |
| `n 100` | `serializado=n:100` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y conversión implícita entre texto y número: justo el punto donde la serialización
se vuelve interesante, porque el formato de salida no recuerda de qué tipo venía el dato.

### Ruby

```ruby
require 'json' # la biblioteca estándar ya trae JSON, aquí basta el formato simple

clave, valor = STDIN.gets.split
puts "serializado=#{clave}:#{valor}"
```

### Perl

```perl
my ($clave, $valor) = split ' ', <STDIN>;
print "serializado=$clave:$valor\n";
```

### Lua

```lua
-- Lua no trae ningún serializador en su biblioteca estándar: para JSON
-- haría falta dkjson o lua-cjson. El formato `clave:valor` sí es nativo.
local clave, valor = io.read("l"):match("(%S+)%s+(%S+)")
print(string.format("serializado=%s:%s", clave, valor))
```

### Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] clave valor
puts "serializado=$clave:$valor"
```

### R

```r
p <- scan("stdin", what = "", nmax = 2, quiet = TRUE)
cat(sprintf("serializado=%s:%s\n", p[1], p[2]))
```

**Qué reconocer:** los cinco parten la línea y pegan las piezas, pero se separan en qué saben del
dato una vez serializado. Ruby y Perl traen serializador en la biblioteca estándar —`json` en Ruby,
`JSON::PP` en el núcleo de Perl desde 5.14—, mientras que **Lua no trae ninguno**: hay que instalar
dkjson o lua-cjson. Y hay una diferencia que muerde en producción: Lua anterior a 5.3 y R usan
**coma flotante doble para todo número**, así que un entero de 64 bits que cruce por JSON pierde
precisión silenciosamente por encima de 2^53. Tcl esquiva el problema por el lado contrario: para él
todo es cadena y nunca convierte a menos que se lo pidas.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
JSON nació aquí —es un subconjunto de los literales de objeto de JavaScript— y sus límites son los
límites del tipo `Number`.

### Dart

```dart
import 'dart:convert'; // jsonEncode viene en la biblioteca estándar
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('serializado=${p[0]}:${p[1]}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la serialización.
// Su formato binario propio es AMF (flash.net.registerClassAlias), no JSON.
package {
    public class Serializador {
        public static function serializar(clave:String, valor:String):String {
            return "serializado=" + clave + ":" + valor;
        }
    }
}
```

**Qué reconocer:** ambos comparten con JavaScript la idea de que serializar es "convertir a texto lo
que ya es un objeto", pero no comparten los tipos. ActionScript usa `Number` —doble— para todo
número no declarado, con lo que hereda la misma pérdida de precisión que JavaScript en enteros
grandes. Dart, en cambio, tiene un `int` de 64 bits real cuando compila a nativo, y aun así al
compilar a JavaScript ese `int` se vuelve doble: el mismo programa cambia de garantías según el
destino. Ninguno de los dos tiene fecha nativa en JSON —**JSON no tiene tipo fecha en absoluto**—,
por eso la convención universal es escribirla como cadena ISO 8601.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Tipos declarados de antemano: el
deserializador sabe a qué clase debe mapear cada campo antes de leer el primer byte.

### Kotlin

```kotlin
fun main() {
    val (clave, valor) = readLine()!!.trim().split(Regex("\\s+"))
    println("serializado=$clave:$valor")
}
```

### Scala

```scala
object Serializador extends App {
  val Array(clave, valor) = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"serializado=$clave:$valor")
}
```

### Groovy

```groovy
def (clave, valor) = System.in.newReader().readLine().trim().split(/\s+/)
println "serializado=$clave:$valor"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[clave valor] (str/split (str/trim (read-line)) #"\s+")]
  (println (str "serializado=" clave ":" valor)))
```

**Qué reconocer:** ninguno de los cuatro trae JSON en la biblioteca estándar de la plataforma —se usa
Jackson, `kotlinx.serialization` o `data.json`—, pero todos heredan de Java un `long` de 64 bits
exacto, así que el problema no es representar el entero sino que **el otro extremo del cable sepa
leerlo**. Kotlin declara el contrato con `@Serializable` y genera el codificador en compilación, lo
más cercano a Protobuf sin salir del lenguaje. Clojure aporta el contraste más instructivo: su
formato nativo **EDN** sí distingue entero de real (`1` frente a `1.0`), sí tiene enteros de
precisión arbitraria (`1N`) y sí tiene literal de instante (`#inst "2026-07-19T00:00:00Z"`) —
exactamente las tres cosas que JSON no puede expresar.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let partes = stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "serializado=%s:%s" partes.[0] partes.[1]
```

### VB.NET

```vbnet
Imports System

Module Serializador
    Sub Main()
        Dim p = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine($"serializado={p(0)}:{p(1)}")
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `System.Text.Json` en la biblioteca estándar y el mismo modelo
de contrato: una clase o `record` cuyas propiedades definen el esquema. Ese serializador tiene una
decisión famosa —escribe `long` como número JSON, con lo que un identificador de 64 bits llega roto
a un consumidor JavaScript, y por eso muchas APIs .NET lo emiten como cadena. F# añade un problema
propio: sus tipos unión discriminada y sus opciones no tienen representación natural en JSON y
requieren convertidores a medida, el recordatorio de que **el formato de intercambio es siempre el
mínimo común denominador**, no la riqueza del lenguaje.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el tipo lo pones tú, byte a byte.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string clave, valor;
    std::cin >> clave >> valor;
    std::cout << "serializado=" << clave << ':' << valor << '\n';
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
        printf("serializado=%s:%s\n", [p[0] UTF8String], [p[1] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ni C ni C++ traen JSON en la biblioteca estándar —se recurre a nlohmann/json o
RapidJSON—, lo que explica por qué en este mundo se prefieren formatos binarios con esquema
compilado: Protobuf y MessagePack generan estructuras C con los tipos exactos, sin pasar por texto.
Objective-C es la excepción de la familia: Foundation sí trae `NSJSONSerialization`, y al
deserializar devuelve `NSNumber` para todo número, un envoltorio que **borra la distinción entre
entero y real** hasta que consultas su `objCType`. Es el mismo problema de Lua o R, solo que envuelto
en un objeto.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y con tipos
exactos, pero con biblioteca estándar moderna: el serializador viene incluido.

### Zig

```zig
const std = @import("std"); // std.json forma parte de la biblioteca estándar

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    const clave = it.next().?;
    const valor = it.next().?;
    try std.io.getStdOut().writer().print("serializado={s}:{s}\n", .{ clave, valor });
}
```

### Nim

```nim
import std/[strutils, json] # json está en la biblioteca estándar

let p = stdin.readLine().splitWhitespace()
echo "serializado=", p[0], ":", p[1]
```

### D

```d
import std.stdio, std.array, std.string, std.json; // std.json viene incluido

void main() {
    auto p = readln().strip().split();
    writefln("serializado=%s:%s", p[0], p[1]);
}
```

**Qué reconocer:** los tres **sí traen JSON en la biblioteca estándar** (`std.json` en Zig y en D,
`std/json` en Nim), a diferencia de C, C++ o Lua. Y los tres deserializan hacia un tipo conocido:
`std.json.parseFromSlice(Config, ...)` en Zig exige la estructura destino en tiempo de compilación,
de modo que el entero de 64 bits llega como `i64` y no como doble. Esa es la diferencia central de la
clase: **quien declara el tipo destino conserva la precisión; quien deserializa a un tipo genérico la
pierde**. El precio es que un campo inesperado en el JSON es un error, no un dato que se ignora.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí el dato ya vive en una forma estructurada;
serializar es solo elegir cómo escribirla.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", [Clave, Valor]),
    format("serializado=~w:~w~n", [Clave, Valor]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni concatenación de cadenas: el par se declara como
% hecho, y la "serialización" es la propia forma canónica de la tupla.
par("x", "5").

serializado(K, V) :- par(K, V).
```

**Qué reconocer:** Prolog es el único de los veinte cuyo **formato de intercambio es su propia
sintaxis**: `write_canonical/1` emite un término que `read_term/2` vuelve a leer sin pérdida, con la
distinción entre entero y real intacta y con enteros de precisión arbitraria. No necesita JSON porque
el lenguaje ya es un formato de datos —aunque la biblioteca de SWI-Prolog trae `library(http/json)`
para hablar con el resto del mundo. Datalog lleva la idea al límite: sin E/S y sin efectos, los
hechos **son** el documento serializado. Es la misma renuncia de SQL, que no te dice cómo se
codifican las filas en disco porque el formato no es asunto de la consulta.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer, partir, unir con un
separador. Lo que cambia es qué recuerda el formato sobre el dato que transporta —y ahí se decide
si un entero de 64 bits, un decimal exacto o una fecha sobreviven al cruce. Eso es lo transferible.

⏮️ [Volver a la clase 159](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
