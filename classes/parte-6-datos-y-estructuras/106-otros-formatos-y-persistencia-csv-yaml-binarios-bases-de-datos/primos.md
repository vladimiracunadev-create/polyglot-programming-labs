# 🧬 El mismo programa en las familias de lenguajes — Clase 106

> [⬅️ Volver a la clase 106](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —convertir una lista de valores en una línea CSV y
contar sus campos— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Unir con comas es trivial; lo interesante empieza en el caso que el contrato no cubre: un campo que
contiene una coma, o una comilla, o un salto de línea. Ahí es donde se ve **qué trajo cada lenguaje
en su biblioteca estándar** — un módulo CSV, un lector YAML, un serializador binario, un cliente de
base de datos — y qué dejó fuera para que lo resuelva el ecosistema.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `csv=<valores separados por coma> campos=<cantidad>`
- **Regla:** `csv` es la unión de los valores con coma; `campos` es cuántos hay

| stdin | esperado |
|---|---|
| `1 2 3` | `csv=1,2,3 campos=3` |
| `5` | `csv=5 campos=1` |
| `10 20` | `csv=10,20 campos=2` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Los lenguajes de administración de sistemas viven de leer y escribir formatos de texto, así que aquí
es donde más se nota qué llevaba puesto cada uno el día que se popularizó.

### Ruby

```ruby
require "csv"   # CSV es biblioteca estándar en Ruby, igual que JSON

campos = STDIN.gets.split
# generate_line entrecomilla los campos que lo necesiten y añade el salto.
puts "csv=#{CSV.generate_line(campos).chomp} campos=#{campos.size}"
```

### Perl

```perl
use strict;
use warnings;

# Perl trae JSON::PP en el core, pero NO un módulo CSV: Text::CSV y su versión
# rápida Text::CSV_XS se instalan desde CPAN. Para campos sin comas, join basta.
my @campos = split ' ', <STDIN>;
printf "csv=%s campos=%d\n", join(",", @campos), scalar(@campos);
```

### Lua

```lua
-- Lua no trae CSV, ni YAML, ni JSON, ni cliente de base de datos: su estándar
-- son cadenas, tablas, E/S básica y poco más. Todo lo demás llega por LuaRocks
-- (lua-csv, lyaml, luasql). Con gmatch y table.concat el caso simple se resuelve.
local campos = {}
for tok in io.read("l"):gmatch("%S+") do campos[#campos + 1] = tok end
print(string.format("csv=%s campos=%d", table.concat(campos, ","), #campos))
```

### Tcl

```tcl
package require csv   ;# el paquete csv llega con tcllib, no con el núcleo

gets stdin linea
set campos [split $linea " "]
# csv::join entrecomilla los campos que contengan comas, comillas o saltos.
puts "csv=[csv::join $campos] campos=[llength $campos]"
```

### R

```r
# read.csv y write.csv son parte de R base: el CSV es el formato de casa, y la
# unidad de trabajo del lenguaje es el data frame, no la lista de cadenas.
campos <- strsplit(readLines("stdin", n = 1), " ")[[1]]
cat(sprintf("csv=%s campos=%d\n", paste(campos, collapse = ","), length(campos)))
```

**Qué reconocer:** la biblioteca estándar reparte las cartas de otra manera que con JSON. Ruby vuelve
a ganar: trae `CSV` de serie, con analizador completo y comillas correctas, además de YAML mediante
Psych. Perl invierte la relación respecto a la clase anterior — tiene JSON::PP en el core pero **no
CSV**, y Text::CSV es una de las descargas más habituales de CPAN. Lua sigue sin traer nada, y aquí ya
es un patrón, no una casualidad. Tcl lo tiene en tcllib, el mismo sitio que `json`. Y R es el caso
más revelador: `jsonlite` era externo, pero `read.csv` es base y devuelve directamente un **data
frame** con tipos inferidos por columna, porque el lenguaje se diseñó alrededor de la tabla.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  // dart:convert trae JSON y utf8, pero CSV y YAML son paquetes de pub.dev.
  // Para persistir hay sqflite (SQLite) o Hive, ambos fuera de la estándar.
  final campos = stdin.readLineSync()!.split(' ').where((s) => s.isNotEmpty).toList();
  print('csv=${campos.join(',')} campos=${campos.length}');
}
```

### ActionScript 3

```actionscript
// En el reproductor Flash no hay disco ni base de datos: solo SharedObject para
// guardar en local. Adobe AIR sí añadió flash.filesystem y SQLite embebido.
package {
    public class Fila {
        public static function resumen(linea:String):String {
            var campos:Array = linea.split(" ");
            return "csv=" + campos.join(",") + " campos=" + campos.length;
        }
    }
}
```

**Qué reconocer:** la familia del navegador no tuvo persistencia durante años, y su vocabulario
todavía lo refleja: `localStorage`, `IndexedDB`, `SharedObject` — almacenes de clave-valor con cuota,
no archivos. JSON es la excepción porque nació dentro del lenguaje; CSV y YAML son siempre paquetes.
Adobe AIR y Node fueron los dos intentos de sacar la familia al sistema de archivos, y en ambos casos
el acceso a disco llegó como **API añadida**, no como parte del lenguaje.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM no trae CSV ni YAML, pero sí trae algo
que ninguna otra familia estandarizó tan pronto: **JDBC**, una interfaz única para hablar con
cualquier base de datos relacional.

### Kotlin

```kotlin
// Ni CSV ni YAML en la estándar: se usan Apache Commons CSV, OpenCSV o
// SnakeYAML. Lo que sí es estándar es java.sql (JDBC) para bases de datos.
fun main() {
    val campos = readLine()!!.split(" ").filter { it.isNotEmpty() }
    println("csv=${campos.joinToString(",")} campos=${campos.size}")
}
```

### Scala

```scala
object Fila extends App {
  // Igual que Kotlin: JDBC sí, CSV no. Las bibliotecas de datos de Scala
  // (Spark, Doobie) construyen sobre esa base.
  val campos = scala.io.StdIn.readLine().split("\\s+").filter(_.nonEmpty)
  println(s"csv=${campos.mkString(",")} campos=${campos.length}")
}
```

### Groovy

```groovy
// Groovy trae JSON y XML de serie (groovy.json, groovy.xml) y groovy.sql.Sql,
// que envuelve JDBC en una línea. CSV y YAML siguen siendo externos.
def campos = System.in.newReader().readLine().split(/\s+/).findAll { it }
println "csv=${campos.join(',')} campos=${campos.size()}"
```

### Clojure

```clojure
;; clojure.data.csv es una dependencia aparte, igual que clojure.data.json.
;; Nativo de Clojure es EDN: (spit "datos.edn" (pr-str datos)) persiste
;; cualquier estructura y (clojure.edn/read-string ...) la recupera.
(require '[clojure.string :as str])

(let [campos (str/split (read-line) #"\s+")]
  (println (str "csv=" (str/join "," campos) " campos=" (count campos))))
```

**Qué reconocer:** los cuatro comparten el mismo hueco (nada de CSV ni YAML) y la misma abundancia
(JDBC, `Serializable`, `ObjectOutputStream` para binario). La serialización binaria de Java es además
la lección negativa de la plataforma: venía en la estándar, deserializar datos ajenos resultó ser un
agujero de seguridad clásico, y hoy la recomendación oficial es no usarla. Groovy vuelve a ser el que
añade comodidad encima —`groovy.sql.Sql` convierte una consulta JDBC en una línea— y Clojure vuelve a
responder con **EDN**: no necesita un formato de persistencia porque sus propios literales ya lo son.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// La BCL de .NET no trae lector CSV; en F# lo idiomático es FSharp.Data y su
// CsvProvider, que genera los tipos de las columnas leyendo el archivo real.
let campos = stdin.ReadLine().Split(' ') |> Array.filter (fun s -> s <> "")
printfn "csv=%s campos=%d" (String.concat "," campos) campos.Length
```

### VB.NET

```vbnet
Module Fila
    Sub Main()
        ' Curiosidad de la plataforma: el único analizador CSV que .NET incluye
        ' vive en la biblioteca de Visual Basic (Microsoft.VisualBasic.FileIO.
        ' TextFieldParser), y los usuarios de C# la referencian desde allí.
        Dim campos = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine($"csv={String.Join(",", campos)} campos={campos.Length}")
    End Sub
End Module
```

**Qué reconocer:** .NET trajo pronto la parte cara —**ADO.NET**, el equivalente de JDBC, en la
plataforma desde el primer día— y se olvidó de la barata: no hay CSV en la biblioteca base, salvo el
`TextFieldParser` heredado de Visual Basic 6, que sigue ahí por compatibilidad y acaba siendo el
recurso de todo el mundo. YAML tampoco existe en la BCL (se usa YamlDotNet). Los dos lenguajes ven
exactamente las mismas clases, porque el reparto lo hace el CLR, no el compilador.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí la persistencia por defecto no es un formato de
texto sino volcar la estructura tal cual está en memoria: `fwrite` de un `struct`.

### C++

```cpp
// La estándar de C++ no tiene CSV, YAML ni base de datos: todo es externo
// (rapidcsv, yaml-cpp, SQLiteCpp). Lo que sí hay es escritura binaria cruda.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream ss(linea);
    std::vector<std::string> campos;
    for (std::string t; ss >> t;) campos.push_back(t);
    std::string csv;
    for (std::size_t i = 0; i < campos.size(); ++i) {
        if (i) csv += ',';
        csv += campos[i];
    }
    std::cout << "csv=" << csv << " campos=" << campos.size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        // Foundation no tiene CSV, pero sí tres formatos propios de persistencia:
        // property lists (XML o binario), NSKeyedArchiver y NSUserDefaults.
        // Los tres producen NSData, nunca NSString.
        NSString *linea = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] availableData]
                encoding:NSUTF8StringEncoding];
        NSArray *campos = [[linea stringByTrimmingCharactersInSet:
                            [NSCharacterSet whitespaceAndNewlineCharacterSet]]
                           componentsSeparatedByString:@" "];
        printf("csv=%s campos=%lu\n",
               [[campos componentsJoinedByString:@","] UTF8String],
               (unsigned long)[campos count]);
    }
    return 0;
}
```

**Qué reconocer:** en C y C++ persistir es escribir bytes, y el formato es "lo que había en memoria",
con todos los problemas que eso arrastra: relleno entre campos, orden de bytes y tamaño de los enteros
cambian con la máquina, así que el archivo no siempre se lee donde no se escribió. Objective-C rompe
con esa herencia porque Foundation le dio formatos de verdad —las *property lists* y `NSKeyedArchiver`
son serialización con esquema, no un volcado— y mantiene su distinción de siempre: el resultado es
`NSData`, bytes explícitos, no una cadena que se pueda imprimir sin decodificar.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go trae `encoding/csv`
en la estándar; Rust usa el crate `csv`. Los primos vuelven a repartirse entre esas dos posturas.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    // Zig trae std.json, pero ni CSV ni YAML ni cliente de base de datos: la
    // biblioteca estándar es deliberadamente pequeña y todavía inestable.
    var buf: [1024]u8 = undefined;
    const cruda = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const linea = std.mem.trim(u8, cruda, " \r");
    const out = std.io.getStdOut().writer();
    try out.writeAll("csv=");
    var it = std.mem.tokenizeScalar(u8, linea, ' ');
    var campos: usize = 0;
    while (it.next()) |campo| {
        if (campos > 0) try out.writeByte(',');
        try out.writeAll(campo);
        campos += 1;
    }
    try out.print(" campos={d}\n", .{campos});
}
```

### Nim

```nim
import std/strutils

# Nim sí trae std/parsecsv en la estándar, pero solo lee: para escribir una fila
# se usa join. También trae std/marshal para volcar objetos a texto.
let campos = stdin.readLine().splitWhitespace()
echo "csv=", campos.join(","), " campos=", campos.len
```

### D

```d
import std.stdio, std.array;

void main() {
    // Phobos incluye std.csv, que lee registros CSV directamente tipados en un
    // struct: csvReader!Registro(texto). Para escribir, join es suficiente.
    auto campos = readln().split();
    writefln("csv=%s campos=%d", campos.join(","), campos.length);
}
```

**Qué reconocer:** el reparto aquí es tan desigual como en JSON, pero no en el mismo sentido. **D es
el más equipado**: `std.csv` está en Phobos y además lee directamente hacia un `struct` tipado, algo
que ni Go hace en su estándar. Nim trae `std/parsecsv`, pero solo el analizador — escribir queda de tu
cuenta, una asimetría que se repite en muchos lenguajes. Zig no trae nada de esto y lo dice
abiertamente: su estándar es pequeña a propósito y aún se reorganiza entre versiones. Ninguno de los
tres incluye cliente de base de datos, igual que Rust y Go, porque en esta familia hablar con Postgres
significa enlazar con `libpq` o reimplementar el protocolo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia donde la persistencia no es una
biblioteca que se importa, sino el punto de partida del lenguaje.

### Prolog

```prolog
:- initialization(main, main).
:- use_module(library(csv)).   % SWI-Prolog trae CSV en su distribución

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Campos),
    atomic_list_concat(Campos, ',', Csv),
    length(Campos, N),
    % csv_read_file/2 carga un CSV como hechos fila/N directamente consultables,
    % y csv_write_stream/3 hace el camino inverso.
    format("csv=~w campos=~d~n", [Csv, N]).
```

### Datalog

```datalog
% En Soufflé el CSV no es un formato que se procese: es la entrada y la salida
% del motor. .input y .output leen y escriben relaciones sin una línea de código
% de serialización, porque una relación ya es una tabla.
.decl campo(pos: number, valor: symbol)
.input campo

.decl campos(n: number)
campos(n) :- n = count : { campo(_, _) }.
.output campos
```

**Qué reconocer:** los dos tratan un archivo tabular como lo que la familia entiende: **hechos**. En
Prolog, `csv_read_file` no devuelve una lista de listas para que la recorras, sino que puede afirmar
cada fila como una cláusula que ya se consulta con unificación. En Datalog la idea llega al extremo —
`.input` y `.output` sustituyen a toda la capa de serialización, y el CSV es el formato por defecto
justo porque es el más parecido a una relación—. Es la misma continuidad que hace que en SQL nadie
hable de "cargar un archivo": se hace `COPY` o `LOAD DATA` y a partir de ahí es una tabla más.

---

## Y de vuelta a la clase

Veinte lenguajes uniendo tres números con comas, y el mapa que aparece detrás es el de las bibliotecas
estándar: Ruby y R traen CSV de casa, D lo trae y encima tipado, Nim solo lo lee, Perl y la JVM lo
dejan fuera aunque sí trajeran otras cosas, y Lua no trae nada porque decidió no traer nada. Encima de
eso, cada familia tiene un formato propio que no necesita biblioteca —EDN en Clojure, property lists
en Objective-C, relaciones en Datalog—. Preguntarse qué formato es *nativo* de un lenguaje, y no solo
cuál sabe leer, es lo transferible.

⏮️ [Volver a la clase 106](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
