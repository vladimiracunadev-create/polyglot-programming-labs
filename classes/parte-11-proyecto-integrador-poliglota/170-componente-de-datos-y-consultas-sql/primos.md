# 🧬 El mismo programa en las familias de lenguajes — Clase 170

> [⬅️ Volver a la clase 170](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —agregar los valores que devuelve una consulta—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de SQL, la de R te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio (los valores a agregar)
- **Salida** (stdout): `total=<suma de los valores>`
- **Regla:** `total = suma de los valores`

| stdin | esperado |
|---|---|
| `10 20 30` | `total=60` |
| `5` | `total=5` |
| `1 2 3 4` | `total=10` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Es la familia que más a menudo se sienta entre la base de datos y el resto del sistema: recibe filas,
las agrega y las entrega.

### Ruby

```ruby
total = STDIN.read.split.map(&:to_i).sum
puts "total=#{total}"
```

### Perl

```perl
use List::Util qw(sum0);

my @valores = split ' ', <STDIN>;
printf "total=%d\n", sum0(@valores);
```

### Lua

```lua
local total = 0
for palabra in io.read("l"):gmatch("%S+") do
  total = total + tonumber(palabra)
end
print("total=" .. total)
```

### Tcl

```tcl
gets stdin linea
set total 0
foreach v $linea { incr total $v }
puts "total=$total"
```

### R

```r
datos <- data.frame(valor = scan("stdin", what = integer(), quiet = TRUE))
cat(sprintf("total=%d\n", sum(datos$valor)))
```

**Qué reconocer:** cuatro de los cinco recorren la línea elemento a elemento; **R no**. R es el
especialista real de esta clase: su unidad natural no es el escalar sino el vector y el
`data.frame`, una tabla con columnas tipadas que es, literalmente, el mismo modelo mental que una
tabla SQL. Por eso `sum(datos$valor)` es una agregación de columna y no un bucle, y por eso `dplyr`
—con `group_by()` y `summarise()`— se lee casi como el `GROUP BY` de la clase. Perl delata su
propia especialidad en la primera línea: `split ' '` en modo *awk* parte por cualquier racha de
espacios sin que haya que pedirlo. Y Tcl sigue siendo el extremo del *todo es cadena*: la línea leída
**ya es** una lista válida, así que `foreach` la recorre sin partirla.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final total = stdin
      .readLineSync()!
      .trim()
      .split(RegExp(r'\s+'))
      .fold<int>(0, (acc, s) => acc + int.parse(s));
  print('total=$total');
}
```

### ActionScript 3

```actionscript
// Sin stdin y sin cliente de base de datos: en el reproductor Flash los datos
// llegan siempre de un servicio remoto. Se ilustra la agregación en memoria.
package {
    public class Consulta {
        public static function total(valores:Array):String {
            var suma:int = 0;
            for each (var v:int in valores) {
                suma += v;
            }
            return "total=" + suma;
        }
    }
}
```

**Qué reconocer:** la familia web es la que peor lleva esta clase, y por una razón de tipos: su
número es un flotante de doble precisión único, así que un `SUM()` sobre enteros grandes puede
perder precisión por encima de 2^53 —de ahí que las bibliotecas serias devuelvan los `BIGINT` de
PostgreSQL como cadena y no como número—. Dart es la excepción dentro de la familia: tiene `int`
separado de `double`, con enteros de 64 bits en la máquina virtual nativa, aunque al compilar a
JavaScript vuelve a la misma limitación. El gesto compartido es el `fold`/`reduce`, que es el
`reduce` de JavaScript con otro nombre.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val total = readLine()!!.trim().split(Regex("\\s+")).sumOf { it.toInt() }
    println("total=$total")
}
```

### Scala

```scala
object Consulta {
  def main(args: Array[String]): Unit = {
    val total = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).sum
    println(s"total=$total")
  }
}
```

### Groovy

```groovy
def total = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger().sum()
println "total=$total"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [total (->> (str/split (str/trim (read-line)) #"\s+")
                 (map #(Integer/parseInt %))
                 (reduce +))]
  (println (format "total=%d" total)))
```

**Qué reconocer:** los cuatro comparten **JDBC**, la interfaz que Java definió en 1997 y que sigue
siendo la puerta única de la JVM a cualquier base de datos relacional; cambiar de PostgreSQL a
Oracle es cambiar el *driver* en el classpath, no el código. Encima de esa base cada primo pone su
capa: Kotlin tiene Exposed, Scala tiene Slick y Doobie, Groovy tiene el `groovy.sql.Sql` de una
línea. Fíjate en que la agregación se escribe distinto en los cuatro —`sumOf`, `.sum`, `*.` de
Groovy, `reduce +` de Clojure— pero todas terminan en el mismo bucle sobre el mismo bytecode.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let total =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.sumBy int
printfn "total=%d" total
```

### VB.NET

```vbnet
Imports System

Module Consulta
    Sub Main()
        Dim partes = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Dim total = 0
        For Each p In partes
            total += Integer.Parse(p)
        Next
        Console.WriteLine($"total={total}")
    End Sub
End Module
```

**Qué reconocer:** .NET es la plataforma que más lejos llevó la idea de esta clase, porque LINQ borra
la frontera entre agregar en memoria y agregar en la base de datos: la misma expresión
`.Where(...).Sum(...)` se ejecuta sobre una lista o se **traduce a SQL** y viaja al servidor, según
el proveedor que haya detrás. Por debajo está siempre ADO.NET —`IDbConnection`, `IDbCommand`,
`IDataReader`—, el equivalente exacto de JDBC en la JVM. F# añade además los proveedores de tipos,
que leen el esquema de la base en tiempo de compilación y hacen que una columna mal escrita sea un
error de compilación y no de ejecución.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>

int main() {
    long long total = 0, v = 0;
    while (std::cin >> v) {
        total += v;
    }
    std::cout << "total=" << total << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *entrada = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:entrada encoding:NSUTF8StringEncoding];
        NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        long total = 0;
        for (NSString *p in [linea componentsSeparatedByCharactersInSet:espacios]) {
            if (p.length > 0) {
                total += [p integerValue];
            }
        }
        printf("total=%ld\n", total);
    }
    return 0;
}
```

**Qué reconocer:** aquí está el suelo de toda la pila de datos: SQLite, PostgreSQL y MySQL están
escritos en C, y las bibliotecas cliente de casi todos los demás lenguajes —`psycopg` de Python, el
`sqlite3` de Ruby, el DBD de R— son envoltorios sobre esas mismas funciones en C. Objective-C aporta
la otra mitad de la historia en las plataformas de Apple: Core Data es su capa de persistencia, y
por debajo guarda en SQLite. Fíjate también en el detalle de tipos: aquí el ancho del entero se
elige a mano (`long long`), que es exactamente la decisión que la familia web no puede tomar.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var total: i64 = 0;
    while (it.next()) |t| {
        total += try std.fmt.parseInt(i64, t, 10);
    }
    try std.io.getStdOut().writer().print("total={d}\n", .{total});
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

let total = stdin.readLine().splitWhitespace().map(parseInt).sum()
echo "total=", total
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    const total = readln().split().map!(to!long).sum();
    writefln("total=%d", total);
}
```

**Qué reconocer:** en esta familia el acceso a datos casi siempre pasa por **enlazar con la
biblioteca en C** del motor, porque escribir un cliente de protocolo desde cero rara vez compensa:
Zig importa la cabecera de SQLite con `@cImport` sin generador intermedio, Nim y D tienen su propio
mecanismo de declaraciones externas. Rust y Go son la excepción del núcleo —`sqlx` y `database/sql`
implementan el protocolo de PostgreSQL en el propio lenguaje— y esa diferencia se paga en trabajo de
mantenimiento pero se cobra en compilación sin dependencias de C. La agregación en sí es idéntica a
la de cualquier otra familia: recorrer y acumular, con el ancho del entero declarado a la vista.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Numeros),
    sum_list(Numeros, Total),
    format("total=~d~n", [Total]).
```

### Datalog

```datalog
% Datalog no lee de stdin: los valores son hechos de la base extensional y la
% suma se declara con la agregación de Soufflé.
valor(1, 10).
valor(2, 20).
valor(3, 30).

total(T) :- T = sum X : { valor(_, X) }.
```

**Qué reconocer:** esta es la familia de la que **procede** el representante del núcleo. Datalog es
literalmente el ancestro teórico del SQL recursivo: la regla `total(T) :- T = sum X : {...}` es un
`SELECT SUM(x)` escrito como implicación lógica, sin bucle, sin acumulador y sin orden de
evaluación. Y muestra el límite honesto de la idea: al no tener efectos ni entrada, los datos tienen
que estar ya en la base como hechos. Prolog conserva la unificación pero recupera el mundo real
—lee, convierte, imprime— al precio de dejar de ser puramente declarativo.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una diferencia que solo esta clase deja ver: agregar es
trivial en todos, pero **hablar con la base de datos** no lo es. JDBC en la JVM, ADO.NET en .NET, la
biblioteca en C debajo de casi todo lo demás, y R con el modelo tabular metido dentro del propio
lenguaje. Reconocer esa capa es lo transferible.

⏮️ [Volver a la clase 170](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
