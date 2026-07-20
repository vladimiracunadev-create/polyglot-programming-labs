# 🧬 El mismo programa en las familias de lenguajes — Clase 172

> [⬅️ Volver a la clase 172](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —guardar un par clave/valor y confirmar lo
almacenado— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `clave valor`
- **Salida** (stdout): `guardado=<clave>=<valor>`
- **Regla:** almacenar el par y confirmar leyéndolo del almacén, no de la variable de entrada

| stdin | esperado |
|---|---|
| `x 5` | `guardado=x=5` |
| `nombre ada` | `guardado=nombre=ada` |
| `n 100` | `guardado=n=100` |

El almacén de estos programas es un diccionario en memoria: es el modelo mínimo de una
persistencia —escribir por clave, leer por clave— y basta para ver la forma. Lo que decide de verdad
el lenguaje de este componente es **el conector a la base real**, así que cada apartado nombra los
drivers que existen de verdad y dice quién tiene un ORM maduro y quién escribe SQL a mano.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El diccionario es un tipo del lenguaje, no una clase de biblioteca: la sintaxis de guardar y leer es
casi la misma en los cinco.

### Ruby

```ruby
clave, valor = STDIN.gets.split
almacen = {}
almacen[clave] = valor
puts "guardado=#{clave}=#{almacen[clave]}"
```

### Perl

```perl
my ($clave, $valor) = split ' ', <STDIN>;
chomp $valor;
my %almacen = ($clave => $valor);
print "guardado=$clave=$almacen{$clave}\n";
```

### Lua

```lua
local clave, valor = io.read("l"):match("^%s*(%S+)%s+(%S+)")
local almacen = {}
almacen[clave] = valor
print("guardado=" .. clave .. "=" .. almacen[clave])
```

### Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] clave valor
array set almacen [list $clave $valor]
puts "guardado=$clave=$almacen($clave)"
```

### R

```r
p <- strsplit(readLines("stdin", n = 1), " ")[[1]]
almacen <- new.env()
assign(p[1], p[2], envir = almacen)
cat(sprintf("guardado=%s=%s\n", p[1], get(p[1], envir = almacen)))
```

**Qué reconocer:** los cinco tienen conectores reales y maduros a bases relacionales, pero solo uno
tiene ORM de primera línea. **Ruby** es el mejor equipado de la familia después de Python: las gemas
`pg`, `mysql2` y `sqlite3` son los drivers de referencia, y encima está **ActiveRecord** —el ORM de
Rails, con migraciones versionadas— o **Sequel** si prefieres algo más cercano al SQL. **Perl** tiene
**DBI**, que además de ser sólido es históricamente importante: es el diseño del que copiaron media
docena de lenguajes la idea de una interfaz común con drivers `DBD::Pg`, `DBD::mysql`, `DBD::SQLite`
detrás; su capa ORM, **DBIx::Class**, existe y funciona, aunque con poca actividad. **Lua** tiene
**LuaSQL** —driver fino sobre PostgreSQL, MySQL, SQLite y ODBC— y nada parecido a un ORM; en
OpenResty se usan clientes no bloqueantes como `pgmoon` o `lua-resty-redis`, y el SQL se escribe a
mano. **Tcl** tiene `tdbc` en su distribución (`tdbc::postgres`, `tdbc::sqlite3`), correcto y sin
ecosistema alrededor. **R** tiene **DBI** propio —mismo nombre y misma idea que el de Perl— con
`RPostgres` y `RSQLite`, y **dbplyr**, que no es un ORM sino algo distinto y muy suyo: traduce
verbos de `dplyr` a SQL para que consultes la base con la misma sintaxis con la que manipulas un
*data frame*. Nótese que en R el almacén natural no es un `dict`, sino un **entorno**; el objeto
mutable por referencia del lenguaje.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final p = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final almacen = <String, String>{};
  almacen[p[0]] = p[1];
  print('guardado=${p[0]}=${almacen[p[0]]}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin ni acceso a bases de datos de servidor. Su
// persistencia real es el SharedObject (Local Shared Object), el almacen local
// del reproductor Flash: exactamente un mapa clave/valor en disco del cliente.
package {
    import flash.net.SharedObject;

    public class Almacen {
        public static function guardar(clave:String, valor:String):String {
            var so:SharedObject = SharedObject.getLocal("proyecto");
            so.data[clave] = valor;
            so.flush();
            return "guardado=" + clave + "=" + so.data[clave];
        }
    }
}
```

**Qué reconocer:** **Dart** distingue en el tipo lo que JavaScript deja implícito —`Map<String,
String>` frente al objeto que acepta cualquier cosa— y sus conectores son reales pero jóvenes:
`postgres` y `mysql1` en pub.dev, y **Drift** como ORM sobre SQLite, que es donde el ecosistema
tiene su fuerza porque el caso dominante es la app Flutter guardando datos en el dispositivo. Ese
sesgo es la diferencia clave con Node: el ecosistema de persistencia de Dart está optimizado para el
**cliente**, no para el servidor. **ActionScript** lo lleva al extremo: su única persistencia es el
almacén local del reproductor, sin transacciones, sin consultas y borrable por el usuario. Un
componente de datos no se elige por la sintaxis del mapa; se elige por a qué se puede conectar.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La familia con la historia de persistencia más
profunda del Atlas, y toda ella pasa por una sola pieza: **JDBC**.

### Kotlin

```kotlin
fun main() {
    val (clave, valor) = readLine()!!.trim().split(Regex("\\s+"))
    val almacen = mutableMapOf<String, String>()
    almacen[clave] = valor
    println("guardado=$clave=${almacen[clave]}")
}
```

### Scala

```scala
object Persistencia extends App {
  val Array(clave, valor) = scala.io.StdIn.readLine().trim.split("\\s+")
  val almacen = Map(clave -> valor)
  println(s"guardado=$clave=${almacen(clave)}")
}
```

### Groovy

```groovy
def (clave, valor) = System.in.newReader().readLine().trim().split(/\s+/)
def almacen = [:]
almacen[clave] = valor
println "guardado=$clave=${almacen[clave]}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[clave valor] (str/split (str/trim (read-line)) #"\s+")
      almacen (assoc {} clave valor)]
  (println (str "guardado=" clave "=" (get almacen clave))))
```

**Qué reconocer:** los cuatro usan **el mismo driver** que Java —el `.jar` de JDBC de PostgreSQL o
de Oracle es literalmente el mismo archivo— y eso significa que la decisión de lenguaje dentro de la
JVM **no afecta** a la conectividad, al *pool* de conexiones ni al soporte del proveedor. Es el
argumento más limpio que verás en todo el sistema. Lo que cambia es la capa de arriba: **Kotlin**
tiene **Exposed** (DSL de JetBrains) y usa Hibernate sin fricción; **Scala** prefiere no tener ORM y
va con **Slick**, **Doobie** o **Quill**, que traducen consultas comprobadas por el compilador;
**Groovy** aporta el veterano **GORM** de Grails y `groovy.sql.Sql`, que es JDBC con una línea;
**Clojure** rechaza el ORM por principio y usa `next.jdbc` con HoneySQL para componer SQL como datos.
Fíjate además en Scala y Clojure: el `Map` que crean es **inmutable**, así que "guardar" devuelve un
mapa nuevo en vez de mutar el existente —el mismo cambio de mentalidad que hay entre `UPDATE` y una
tabla de hechos con versiones—.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System.Collections.Generic

let partes = stdin.ReadLine().Trim().Split(' ')
let almacen = Dictionary<string, string>()
almacen[partes[0]] <- partes[1]
printfn "guardado=%s=%s" partes[0] almacen[partes[0]]
```

### VB.NET

```vbnet
Module Persistencia
    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Dim almacen As New Dictionary(Of String, String)
        almacen(p(0)) = p(1)
        Console.WriteLine("guardado=" & p(0) & "=" & almacen(p(0)))
    End Sub
End Module
```

**Qué reconocer:** lo mismo que en la JVM, con otro nombre: la capa común es **ADO.NET**
(`IDbConnection`, `IDbCommand`, `DbDataReader`) y encima están **Entity Framework Core** como ORM
completo y **Dapper** como micro-ORM cuando quieres el SQL a la vista. Los tres lenguajes comparten
esas tres piezas exactamente igual, con los mismos proveedores `Npgsql` para PostgreSQL o
`Microsoft.Data.SqlClient`. **F#** añade algo que C# no tiene: los **type providers** de
`FSharp.Data.SqlClient`, que leen el esquema de la base **en tiempo de compilación** y hacen que una
consulta con una columna mal escrita no compile; es la integración lenguaje-base de datos más
estrecha del Atlas. **VB.NET** accede a todo el mismo ADO.NET sin ninguna limitación técnica, pero
las herramientas de *scaffolding* de EF Core generan C# y la documentación de proveedores rara vez
trae ejemplos en VB: el coste no está en las capacidades, está en el camino trillado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el almacén no viene de serie: se construye o se
enlaza con una biblioteca en C.

### C++

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::string clave, valor;
    std::cin >> clave >> valor;
    std::map<std::string, std::string> almacen;
    almacen[clave] = valor;
    std::cout << "guardado=" << clave << "=" << almacen[clave] << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char c[64], v[64];
        scanf("%63s %63s", c, v);
        NSMutableDictionary<NSString *, NSString *> *almacen = [NSMutableDictionary dictionary];
        NSString *clave = @(c);
        almacen[clave] = @(v);
        printf("guardado=%s=%s\n", clave.UTF8String, [almacen[clave] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** la biblioteca estándar de **C** no tiene diccionario, así que la clase tuvo que
construir el almacén; **C++** sí lo trae —`std::map` ordenado, `std::unordered_map` como tabla
hash— y **Objective-C** lo trae en Foundation con `NSMutableDictionary`. Para bases reales, ambos se
conectan con los clientes nativos en C —`libpq`, la API de SQLite, `libmysqlclient`— que son
precisamente los mismos que envuelven por debajo casi todos los drivers de las otras familias:
cuando en Python usas `psycopg`, hay `libpq` debajo. ORM maduro no hay: en C++ existen **SOCI** y
**ODB**, útiles pero de nicho. **Objective-C** es distinto: tiene **Core Data**, un mapeador de
objetos a almacén persistente de primer nivel, con migraciones y consultas —solo que atado al
ecosistema de Apple y pensado para datos del dispositivo, no para el servidor—.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con una relación con las bases de datos que aún se está construyendo.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const clave = it.next().?;
    const valor = it.next().?;

    var almacen = std.StringHashMap([]const u8).init(alloc);
    defer almacen.deinit();
    try almacen.put(clave, valor);

    try std.io.getStdOut().writer().print("guardado={s}={s}\n", .{ clave, almacen.get(clave).? });
}
```

### Nim

```nim
import std/[strutils, tables]

let p = stdin.readLine().splitWhitespace()
var almacen = initTable[string, string]()
almacen[p[0]] = p[1]
echo "guardado=" & p[0] & "=" & almacen[p[0]]
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto p = readln().strip().split();
    string[string] almacen;
    almacen[p[0]] = p[1];
    writefln("guardado=%s=%s", p[0], almacen[p[0]]);
}
```

**Qué reconocer:** los tres tienen tabla hash de serie —**D** hasta la tiene en la sintaxis del
lenguaje, `string[string]`, sin importar nada— pero el mapa en memoria no es lo que se juzga aquí.
**Zig** exige lo que Rust también exige y Go esconde: decir **quién reserva la memoria** del almacén
(`allocator`) y quién la libera (`defer`). Para bases de datos, Zig depende de enlazar `libpq` o
SQLite por su interfaz C —cosa que hace muy bien, es una de sus mejores bazas— pero no hay driver
puro ni ORM que merezca el nombre. **Nim** tiene `db_connector` (los antiguos módulos `db_postgres`,
`db_mysql` y `db_sqlite`, sacados de la estándar a un paquete propio a partir de la versión 2.0), y
**Norm** como ORM ligero; funciona, con comunidad pequeña. **D** conviene decirlo con claridad: **no
existe** un `std.database` en la biblioteca estándar —fue una propuesta que nunca se incorporó—, así
que se va por Vibe.d o por los bindings de la comunidad como `ddbc` y `mysql-native`. Ninguno de los
tres tiene algo comparable a `database/sql` de Go o a `sqlx`/Diesel de Rust: esta es, con diferencia,
la mayor distancia entre los representantes del núcleo y sus primos de sistemas.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí no hay conector que discutir: la familia
**es** el almacén.

### Prolog

```prolog
:- initialization(main, main).
:- dynamic almacenado/2.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [Clave, Valor|_]),
    assertz(almacenado(Clave, Valor)),
    almacenado(Clave, V),
    format("guardado=~w=~w~n", [Clave, V]).
```

### Datalog

```datalog
% Datalog no tiene estado mutable ni entrada: no se puede "guardar" nada en
% tiempo de ejecucion. El par entra como hecho declarado y la confirmacion es
% una relacion derivada de el.
almacenado("x", "5").

guardado(K, V) :- almacenado(K, V).
```

**Qué reconocer:** **Prolog** tiene aquí su momento más revelador. `assertz` **añade un hecho a la
base de conocimiento** durante la ejecución, y la línea siguiente lo **consulta** —no lee una
variable, resuelve `almacenado(Clave, V)` contra la base—. Eso es literalmente un `INSERT` seguido de
un `SELECT`, escrito sin salir del lenguaje, porque en Prolog el programa y el almacén son la misma
cosa; SWI-Prolog además persiste eso a disco con `library(persistency)`. La declaración `:- dynamic`
es la que autoriza que esa relación cambie: sin ella los hechos son inmutables. **Datalog** renuncia
incluso a eso y se queda solo con los hechos declarados, que es exactamente por qué se usa como motor
de consulta —en análisis de código o control de accesos— y nunca como sistema de escritura.

---

## Y de vuelta a la clase

Veinte lenguajes, un par clave/valor, y la lección de todo el componente: guardar en memoria se
parece en todos, **conectarse a una base de verdad no**. Dentro de la JVM y de .NET la elección de
lenguaje es casi gratis porque JDBC y ADO.NET son comunes; fuera de ahí decide todo, y en la familia
de sistemas la brecha entre el representante y sus primos —`database/sql` frente a un `std.database`
que no existe— es el argumento más concreto que llevarás a la defensa de la clase 175.

⏮️ [Volver a la clase 172](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
