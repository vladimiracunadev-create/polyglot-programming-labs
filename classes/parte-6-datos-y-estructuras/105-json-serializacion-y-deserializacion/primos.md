# 🧬 El mismo programa en las familias de lenguajes — Clase 105

> [⬅️ Volver a la clase 105](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —emitir un objeto JSON con un nombre y una edad—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

JSON es un formato universal, pero el soporte no lo es: aquí lo que decide es **la biblioteca
estándar**. Unos lenguajes traen el codificador de serie, otros lo dejan fuera y otros directamente no
tienen ninguno. Y entre los que sí lo traen, dos detalles se separan enseguida: cuánto espacio en
blanco emiten y si respetan el orden en que escribiste las claves.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `{"nombre": "<nombre>", "edad": <edad>}`
- **Regla:** un objeto JSON con las claves `nombre` (cadena) y `edad` (número), en ese orden

| stdin | esperado |
|---|---|
| `Ada 36` | `{"nombre": "Ada", "edad": 36}` |
| `Bo 5` | `{"nombre": "Bo", "edad": 5}` |
| `Cy 99` | `{"nombre": "Cy", "edad": 99}` |

El espaciado del contrato —un espacio tras cada `:` y cada `,`— es el que emite por defecto
`json.dumps` de Python. Casi todos los demás codificadores emiten **compacto**
(`{"nombre":"Ada","edad":36}`), que es JSON igual de válido pero otra cadena. Por eso varios primos
usan su biblioteca para **escapar el valor** y componen la forma exacta a mano: es la manera honesta
de cumplir el contrato sin fingir que el codificador produce algo que no produce.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Los lenguajes de esta familia tienen diccionarios nativos, que son casi el mismo objeto que JSON
describe. La diferencia está en si el codificador viene incluido o hay que instalarlo.

### Ruby

```ruby
require "json"

nombre, edad = STDIN.gets.split
# JSON es biblioteca estándar en Ruby, y su salida es compacta:
# {"nombre":"Ada","edad":36}. Aquí to_json escapa el valor y fijamos la forma.
puts format('{"nombre": %s, "edad": %d}', nombre.to_json, edad.to_i)
```

### Perl

```perl
use strict;
use warnings;
use JSON::PP;   # JSON::PP sí forma parte del core de Perl desde 5.14.

my ($nombre, $edad) = split ' ', <STDIN>;
# Un hash de Perl no tiene orden, y ->canonical ordenaría alfabéticamente
# (edad antes que nombre), así que fijamos la forma y encode escapa la cadena.
my $json = JSON::PP->new->allow_nonref;
printf "{\"nombre\": %s, \"edad\": %d}\n", $json->encode($nombre), $edad;
```

### Lua

```lua
-- Lua NO trae JSON en la biblioteca estándar: no hay nada que require. En un
-- proyecto real se instala dkjson o lua-cjson con LuaRocks:
--   local json = require("dkjson")
--   print(json.encode({nombre = nombre, edad = edad}))
-- Sin dependencias, se compone la cadena.
local nombre, edad = io.read("l"):match("(%S+)%s+(%d+)")
print(string.format('{"nombre": "%s", "edad": %d}', nombre, tonumber(edad)))
```

### Tcl

```tcl
package require json::write   ;# viene con tcllib, no con el núcleo de Tcl

gets stdin linea
lassign $linea nombre edad
# json::write string escapa y entrecomilla el valor.
puts [format {{"nombre": %s, "edad": %d}} [json::write string $nombre] $edad]
```

### R

```r
# jsonlite no es parte de R base: install.packages("jsonlite").
library(jsonlite)

campos <- strsplit(readLines("stdin", n = 1), " ")[[1]]
# Todo en R es vector, así que toJSON daría ["Ada"]; auto_unbox lo evita.
cat(sprintf('{"nombre": %s, "edad": %d}\n',
            toJSON(campos[1], auto_unbox = TRUE), as.integer(campos[2])))
```

**Qué reconocer:** aquí la biblioteca estándar decide, y las cinco respuestas son distintas. Ruby trae
JSON de serie, como Python. Perl trae **JSON::PP en el core**, así que `use JSON::PP` funciona en una
instalación limpia, aunque el hash sin orden obliga a pensar en las claves. **Lua no trae JSON en
absoluto**: hace falta dkjson o cjson desde LuaRocks, y conviene decirlo sin rodeos —su estándar cabe
en unas pocas páginas y esa pequeñez es una decisión de diseño, no un olvido—. Tcl lo tiene en
tcllib, la biblioteca de paquetes que se distribuye aparte del intérprete. Y R invierte la
proporción: `jsonlite` es externo, pero `read.csv` y los data frames sí son nativos, porque su formato
de datos de casa nunca fue JSON sino la tabla.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:convert';
import 'dart:io';

void main() {
  final t = stdin.readLineSync()!.split(' ');
  // jsonEncode (dart:convert, estándar) emite compacto: {"nombre":"Ada",...}.
  print('{"nombre": ${jsonEncode(t[0])}, "edad": ${int.parse(t[1])}}');
}
```

### ActionScript 3

```actionscript
// Flash Player 11 incorporó la clase JSON nativa, calcada de la de JavaScript,
// pero no hay stdin: se ilustra la serialización.
package {
    public class Persona {
        public static function aJson(nombre:String, edad:int):String {
            // JSON.stringify emite compacto; el contrato pide el formato ancho.
            return '{"nombre": ' + JSON.stringify(nombre) + ', "edad": ' + edad + '}';
        }
    }
}
```

**Qué reconocer:** esta es la única familia donde JSON no es una biblioteca sino **parte del idioma
materno**: el formato salió literalmente de la sintaxis de objetos de JavaScript, y por eso
`JSON.stringify` está en el lenguaje y no en un paquete. Dart lo saca a `dart:convert` pero lo
mantiene en la estándar. ActionScript llegó tarde —el `JSON` nativo apareció en Flash Player 11, antes
había que usar la biblioteca as3corelib— y conserva la misma API que JavaScript, incluido el orden de
inserción de las claves.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Aquí está la ausencia más llamativa de todo el
mapa: la biblioteca estándar de Java **no tiene JSON**, y los lenguajes que la heredan tampoco.

### Kotlin

```kotlin
// Ni la estándar de Kotlin ni la de Java traen JSON: en producción se usa
// kotlinx.serialization (@Serializable + Json.encodeToString) o Jackson.
fun main() {
    val (nombre, edad) = readLine()!!.split(" ")
    println("""{"nombre": "$nombre", "edad": ${edad.toInt()}}""")
}
```

### Scala

```scala
// Scala tampoco lleva JSON en su estándar: existió scala.util.parsing.json,
// hoy retirado. Se usan circe, play-json o uPickle.
object Persona extends App {
  val Array(nombre, edad) = scala.io.StdIn.readLine().split(" ")
  println(s"""{"nombre": "$nombre", "edad": ${edad.toInt}}""")
}
```

### Groovy

```groovy
import groovy.json.JsonOutput   // Groovy sí trae JSON de serie, a diferencia de Java

def (nombre, edad) = System.in.newReader().readLine().split(' ')
// toJson emite compacto; prettyPrint mete saltos de línea e indentación.
println "{\"nombre\": ${JsonOutput.toJson(nombre)}, \"edad\": ${edad.toInteger()}}"
```

### Clojure

```clojure
;; Clojure necesita org.clojure/data.json como dependencia externa. Lo que sí es
;; nativo es EDN: (pr-str {:nombre "Ada" :edad 36}) ya es un formato de datos.
(require '[clojure.string :as str]
         '[clojure.data.json :as json])

(let [[nombre edad] (str/split (read-line) #" ")]
  (println (str "{\"nombre\": " (json/write-str nombre)
                ", \"edad\": " (Integer/parseInt edad) "}")))
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina virtual y cuatro respuestas distintas a la
misma pregunta. Kotlin y Scala heredan el hueco de Java y lo llenan con bibliotecas externas —
kotlinx.serialization, circe— que además hacen el trabajo en **tiempo de compilación**, generando el
codificador a partir del tipo. Groovy sí trae `groovy.json` en su distribución, uno de esos añadidos
que justifican usarlo sobre Java. Clojure necesita `clojure.data.json` de fuera, pero tiene una
respuesta propia: **EDN**, su formato nativo, que no es JSON pero sí es el mismo gesto —los datos son
literales del lenguaje— y encima admite conjuntos, símbolos y valores exactos que JSON no sabe
representar.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System.Text.Json   // parte de la biblioteca base desde .NET Core 3.0

let t = stdin.ReadLine().Split(' ')
// JsonSerializer.Serialize emite compacto: {"nombre":"Ada","edad":36}.
printfn "{\"nombre\": %s, \"edad\": %d}" (JsonSerializer.Serialize t.[0]) (int t.[1])
```

### VB.NET

```vbnet
Imports System.Text.Json

Module Persona
    Sub Main()
        Dim t = Console.ReadLine().Split(" "c)
        ' WriteIndented = True es la única opción de formato: o compacto, o con
        ' saltos de línea. No hay término medio.
        Console.WriteLine($"{{""nombre"": {JsonSerializer.Serialize(t(0))}, ""edad"": {CInt(t(1))}}}")
    End Sub
End Module
```

**Qué reconocer:** .NET llegó tarde y con dos capas: durante años lo estándar de facto fue
**Newtonsoft.Json**, un paquete externo tan universal que parecía parte de la plataforma, hasta que
.NET Core 3.0 incorporó `System.Text.Json` a la biblioteca base. Los dos lenguajes usan exactamente el
mismo tipo, porque comparten CLR. Y ojo con la cultura: `JsonSerializer` escribe los números en
formato invariante, pero si compones la cadena a mano con `ToString()` y la máquina está en
configuración española, saldría `36,5` en vez de `36.5` — y eso ya no es JSON válido.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde la biblioteca estándar es más
pequeña, y donde JSON es siempre una decisión de dependencias.

### C++

```cpp
// La biblioteca estándar de C++ no tiene JSON, ni siquiera en C++23: lo habitual
// es nlohmann/json (nlohmann::json j; j["nombre"] = nombre;) o RapidJSON.
#include <iostream>
#include <string>

int main() {
    std::string nombre;
    int edad;
    std::cin >> nombre >> edad;
    std::cout << "{\"nombre\": \"" << nombre << "\", \"edad\": " << edad << "}\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char n[64];
        int edad;
        scanf("%63s %d", n, &edad);
        NSString *nombre = [NSString stringWithUTF8String:n];
        // NSJSONSerialization está en Foundation, pero devuelve NSData (bytes),
        // no NSString, y un NSDictionary no conserva el orden de las claves.
        NSDictionary *obj = @{@"nombre": nombre, @"edad": @(edad)};
        NSData *bytes = [NSJSONSerialization dataWithJSONObject:obj options:0 error:nil];
        NSString *compacto = [[NSString alloc] initWithData:bytes
                                                   encoding:NSUTF8StringEncoding];
        NSLog(@"%@", compacto);   // sale por stderr: no interfiere con stdout
        printf("{\"nombre\": \"%s\", \"edad\": %d}\n", [nombre UTF8String], edad);
    }
    return 0;
}
```

**Qué reconocer:** el contraste dentro de la misma familia es total. C++ no tiene JSON en la estándar
y probablemente nunca lo tenga: su filosofía es que los formatos son cosa de bibliotecas. Objective-C
sí lo tiene, pero no porque sea C — lo trae **Foundation**, el framework de Apple, y por eso la API
piensa en objetos: `NSJSONSerialization` produce `NSData`, es decir bytes, y hay que decodificarlos
para verlos como texto. Esa insistencia de Foundation en separar `NSData` de `NSString` es la misma
que verás al leer archivos, y es lo que hace de Objective-C el primo más *tipado* de la familia de las
llaves.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go trae
`encoding/json` en la estándar; Rust deja `serde_json` fuera, y esa división parte también a los
primos.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const cruda = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, cruda, "\r"), " ");
    const nombre = it.next().?;
    const edad = try std.fmt.parseInt(u32, it.next().?, 10);
    const out = std.io.getStdOut().writer();
    // std.json está en la estándar. stringify de la estructura entera daría
    // {"nombre":"Ada","edad":36}; aquí se usa para escapar solo la cadena.
    try out.writeAll("{\"nombre\": ");
    try std.json.stringify(nombre, .{}, out);
    try out.print(", \"edad\": {d}}}\n", .{edad});
}
```

### Nim

```nim
import std/[json, strutils]   # std/json viene en la biblioteca estándar

let t = stdin.readLine().splitWhitespace()
let obj = %*{"nombre": t[0], "edad": parseInt(t[1])}
# $obj emite compacto y pretty(obj) emite indentado; se compone el término medio.
echo "{\"nombre\": ", obj["nombre"], ", \"edad\": ", obj["edad"].getInt, "}"
```

### D

```d
import std.stdio, std.array, std.conv, std.json;   // std.json viene en Phobos

void main() {
    auto t = readln().split();
    // JSONValue.toString() emite compacto, y un objeto JSONValue se guarda en un
    // JSONValue[string]: las claves salen en orden de hash, no de inserción.
    writefln("{\"nombre\": %s, \"edad\": %d}",
             JSONValue(t[0]).toString(), t[1].to!int);
}
```

**Qué reconocer:** los tres traen JSON en la estándar —`std.json` de Zig, `std/json` de Nim,
`std.json` de Phobos en D—, lo que los acerca a Go y los separa de Rust, donde `serde` es la
dependencia más descargada del ecosistema precisamente porque no está incluida. La diferencia de
diseño se ve en el tipo: Nim y D usan un **árbol dinámico** (`JsonNode`, `JSONValue`) que se consulta
en tiempo de ejecución, como haría Python; Zig y Rust prefieren serializar directamente desde el tipo
estático, sin construir nada intermedio. Y Zig deja a la vista lo que los demás esconden: no hay
asignador implícito, así que si quieres el resultado en memoria en vez de escrito al flujo, tienes que
decir de dónde sale esa memoria.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Serializar es convertir una estructura en texto,
y aquí el problema es que la estructura no es un objeto sino una relación.

### Prolog

```prolog
:- initialization(main, main).
:- use_module(library(http/json)).   % SWI-Prolog sí trae JSON en su distribución

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [Nombre, EdadS]),
    number_string(Edad, EdadS),
    % json_write_dict(current_output, _{nombre: Nombre, edad: Edad}) produciría
    % JSON válido, pero con el espaciado propio de SWI. Fijamos la forma.
    format("{\"nombre\": \"~w\", \"edad\": ~d}~n", [Nombre, Edad]).
```

### Datalog

```datalog
% Datalog no serializa: no tiene cadenas compuestas, ni E/S, ni la noción de
% "documento". La relación ES el dato, y volcarla a un formato ocurre fuera del
% motor (Soufflé escribe sus relaciones a TSV/CSV, nunca a JSON).
.decl persona(nombre: symbol, edad: number)
persona("Ada", 36).
.output persona
```

**Qué reconocer:** Prolog tiene JSON porque SWI-Prolog decidió incluirlo, y la traducción le sale
natural: un objeto JSON es un **dict** y un array es una lista, dos estructuras que el lenguaje ya
tenía. Datalog no puede ni acercarse, y por una razón de fondo que merece la pena entender: la
serialización supone un orden —primero `nombre`, luego `edad`— y en un lenguaje declarativo puro no
hay orden, solo hechos. Es la misma renuncia de SQL, donde una fila no tiene "forma serializada"
hasta que un cliente decide cómo escribirla.

---

## Y de vuelta a la clase

Veinte lenguajes ante el mismo objeto de dos claves, y la respuesta no depende del paradigma sino de
**qué metió cada comunidad en su biblioteca estándar**: JavaScript lo lleva en la sintaxis, Ruby, Go,
Groovy, Zig, Nim y D lo traen incluido, Perl lo tiene en el core, Java y Scala no lo tienen, y Lua no
tiene nada en absoluto. Aprender a preguntar "¿esto viene de serie o es una dependencia?" antes de
escribir la primera línea es lo transferible.

⏮️ [Volver a la clase 105](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
