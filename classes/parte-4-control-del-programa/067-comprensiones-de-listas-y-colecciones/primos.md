# 🧬 El mismo programa en las familias de lenguajes — Clase 067

> [⬅️ Volver a la clase 067](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —quedarse solo con los números pares de una lista—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Aquí se ve algo que la clase ya anticipa: la *comprensión* como sintaxis existe en pocos lenguajes,
pero la **idea** —describir la colección resultante en vez de construirla paso a paso— aparece en
todos, con nombres distintos: `filter`, `findAll`, `grep`, `where`, indexación lógica, `findall`.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio, con al menos un par
- **Salida** (stdout): `pares=<los pares unidos por -, en orden>`
- **Regla:** `pares = [x ∈ lista : x par]`

| stdin | esperado |
|---|---|
| `1 2 3 4` | `pares=2-4` |
| `10 15 20` | `pares=10-20` |
| `6 7 8` | `pares=6-8` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La comprensión de listas nació aquí —Python la tomó de Haskell y de la notación de conjuntos—, pero
ninguno de sus primos la copió con esa sintaxis: todos filtran con una función.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
pares = nums.select(&:even?)
puts "pares=#{pares.join('-')}"
```

### Perl

```perl
my @nums = split ' ', <STDIN>;
my @pares = grep { $_ % 2 == 0 } @nums;
print "pares=", join('-', @pares), "\n";
```

### Lua

```lua
-- Lua no tiene comprensiones ni filter: el bucle con `if` es lo idiomático.
local pares = {}
for palabra in io.read("l"):gmatch("%S+") do
  local n = tonumber(palabra)
  if n % 2 == 0 then
    pares[#pares + 1] = n
  end
end
print("pares=" .. table.concat(pares, "-"))
```

### Tcl

```tcl
gets stdin linea
# `continue` dentro de lmap descarta el elemento: así se filtra en Tcl.
set pares [lmap n [split $linea] {expr {$n % 2 == 0 ? $n : [continue]}}]
puts "pares=[join $pares -]"
```

### R

```r
nums <- scan("stdin", what = integer(), quiet = TRUE)
pares <- nums[nums %% 2 == 0]
cat(sprintf("pares=%s\n", paste(pares, collapse = "-")))
```

**Qué reconocer:** Ruby y Perl usan el mismo verbo con dos nombres —`select` y `grep`— y ambos
reciben un bloque que devuelve verdadero o falso; es exactamente la parte `if` de la comprensión de
Python, extraída a función. Lua no ofrece ni eso: su biblioteca estándar es deliberadamente mínima y
el `if` dentro del bucle es la respuesta idiomática, no una carencia disimulada. Tcl tiene `lmap`
(un `map`) y filtra con un truco: `continue` descarta el elemento actual. R es el más parecido a la
notación matemática de todos: `nums[nums %% 2 == 0]` construye un vector de verdaderos y falsos y lo
usa como máscara, sin nombrar la variable del elemento ni una sola vez.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  final pares = nums.where((n) => n.isEven);
  print('pares=${pares.join('-')}');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene comprensiones ni stdin: Array.filter es lo más cercano.
package {
    public class Pares {
        public static function filtrar(nums:Array):String {
            var pares:Array = nums.filter(function (n:int, i:int, a:Array):Boolean {
                return n % 2 == 0;
            });
            return "pares=" + pares.join("-");
        }
    }
}
```

**Qué reconocer:** JavaScript nunca tuvo comprensiones —hubo una propuesta y se retiró—, así que
toda la familia filtra con método. Dart lo llama `where` en vez de `filter`, un nombre heredado de
LINQ, y devuelve un `Iterable` **perezoso**: nada se filtra hasta que el `join` lo recorre.
ActionScript conserva la firma completa de la retrollamada `(elemento, índice, array)` que
JavaScript sigue usando hoy, con los tipos declarados encima.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java filtra con `Stream.filter`; sus primos
llegan a tener comprensiones de verdad.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val pares = nums.filter { it % 2 == 0 }
    println("pares=" + pares.joinToString("-"))
}
```

### Scala

```scala
object Pares extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val pares = for (n <- nums if n % 2 == 0) yield n
  println("pares=" + pares.mkString("-"))
}
```

### Groovy

```groovy
def nums = System.in.text.trim().split(/\s+/)*.toInteger()
def pares = nums.findAll { it % 2 == 0 }
println "pares=${pares.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums  (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))
      pares (for [n nums :when (even? n)] n)]
  (println (str "pares=" (str/join "-" pares))))
```

**Qué reconocer:** Kotlin y Groovy filtran con método (`filter`, `findAll`) sobre listas ya
construidas, sin el `.stream()` que Java obliga a escribir. Scala y Clojure sí tienen comprensión de
verdad, y las dos usan la palabra `for` para algo que **no es un bucle**: `for (n <- nums if ...)
yield n` produce una colección nueva, y el `for` de Clojure devuelve una secuencia perezosa. Ese es
el punto de la clase escrito en dos sintaxis distintas: la misma palabra clave significa "recorre" o
"construye" según lleve `yield` o no.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). LINQ es la comprensión de la plataforma: existe
como método (`Where`) y como sintaxis de consulta (`From ... Where ... Select`).

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int

// Comprensión de lista nativa de F#: el `for ... if ... yield` va entre corchetes.
let pares = [ for n in nums do if n % 2 = 0 then yield n ]

printfn "pares=%s" (pares |> List.map string |> String.concat "-")
```

### VB.NET

```vbnet
Imports System
Imports System.Linq

Module Pares
    Sub Main()
        Dim nums = Console.ReadLine().
            Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries).
            Select(Function(s) Integer.Parse(s))

        Dim pares = From n In nums Where n Mod 2 = 0 Select n

        Console.WriteLine("pares=" & String.Join("-", pares))
    End Sub
End Module
```

**Qué reconocer:** la consulta de VB.NET —`From n In nums Where ... Select n`— es la comprensión de
Python con las palabras cambiadas de orden y en mayúsculas; el compilador la traduce a la misma
llamada a `Where` que escribirías a mano. F# trae la comprensión en el propio lenguaje, con
corchetes para lista, llaves para secuencia perezosa y `[| |]` para array: el delimitador decide la
estructura de datos que sale, no el contenido. Y en los tres el filtrado es **diferido** hasta que
alguien recorre el resultado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C se filtra recorriendo y copiando a mano.

### C++

```cpp
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x; ) nums.push_back(x);

    std::string salida;
    for (int n : nums | std::views::filter([](int x) { return x % 2 == 0; })) {
        if (!salida.empty()) salida += '-';
        salida += std::to_string(n);
    }

    std::cout << "pares=" << salida << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *entrada = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile]
                encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *partes =
            [[entrada stringByTrimmingCharactersInSet:blancos] componentsSeparatedByString:@" "];

        NSPredicate *esPar = [NSPredicate predicateWithBlock:^BOOL(id obj, NSDictionary *bindings) {
            return [(NSString *)obj intValue] % 2 == 0;
        }];
        NSArray<NSString *> *pares = [partes filteredArrayUsingPredicate:esPar];

        printf("pares=%s\n", [[pares componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** C++20 acerca la familia al resto con `views::filter`, que además es perezoso: la
tubería `|` describe el filtrado y el `for` lo ejecuta elemento a elemento, sin crear un segundo
vector. Objective-C llega por otro camino, muy suyo: `NSPredicate` es un **objeto que representa una
condición** —se puede construir desde una cadena, guardar o enviar por la red— y `filteredArrayUsingPredicate:`
lo aplica. La condición deja de ser código y pasa a ser un dato.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Filtrar sin pagar de más:
o el compilador elimina la abstracción, o no la hay.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [512]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");

    const out = std.io.getStdOut().writer();
    try out.writeAll("pares=");

    // Zig no tiene comprensiones ni closures en la stdlib: el filtro es un `if`.
    var primero = true;
    while (it.next()) |tok| {
        const n = try std.fmt.parseInt(i64, tok, 10);
        if (@mod(n, 2) != 0) continue;
        if (!primero) try out.writeByte('-');
        primero = false;
        try out.print("{d}", .{n});
    }

    try out.writeByte('\n');
}
```

### Nim

```nim
import std/[strutils, sequtils, sugar]

let nums = stdin.readLine().splitWhitespace().map(parseInt)

# `collect` (std/sugar) es la comprensión de listas de Nim.
let pares = collect:
  for n in nums:
    if n mod 2 == 0:
      n

echo "pares=", pares.join("-")
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv;

void main() {
    auto nums = readln().split().map!(to!int);
    auto pares = nums.filter!(n => n % 2 == 0);
    writeln("pares=", pares.map!(to!string).join("-"));
}
```

**Qué reconocer:** Zig es el único de los veinte que no puede expresar el concepto de ninguna forma
abreviada, y eso es una decisión de diseño declarada: sin sobrecarga de operadores, sin clausuras en
la biblioteca, sin control de flujo escondido. Nim sí tiene comprensión —`collect` es una macro que
se expande a un bucle con `add`, así que no cuesta nada— y también `nums.filterIt(it mod 2 == 0)`
para el caso corto. D encadena *ranges* perezosos: `map!` y `filter!` no recorren nada hasta que
`join` lo pide.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El `WHERE` de SQL es, literalmente, la parte
condicional de una comprensión.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    % findall recoge todas las soluciones de la condición: la comprensión de Prolog.
    findall(N, (member(N, Nums), 0 is N mod 2), Pares),
    atomic_list_concat(Pares, '-', Salida),
    format("pares=~w~n", [Salida]).
```

### Datalog

```datalog
% Filtrar es la operación natural de Datalog: una regla con una condición.
% (La aritmética `%` es una extensión de motor, p. ej. Soufflé; Datalog puro no la tiene.)
num(1). num(2). num(3). num(4).

par(N) :- num(N), N % 2 = 0.
```

**Qué reconocer:** `findall(N, (member(N, Nums), Condición), Pares)` es la comprensión de listas
escrita con paréntesis: el primer argumento es el "qué quiero" —la parte de la izquierda en
Python—, y el segundo, la condición. En Datalog la regla `par(N) :- num(N), N % 2 = 0.` ni siquiera
tiene un contenedor de resultados: define la **relación** de los pares, y el motor te la da entera.
Es la misma renuncia de SQL —dices qué filas quieres, no cómo recorrerlas— llevada al extremo.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una separación clara: los que tienen sintaxis de comprensión
(Python, Scala, Clojure, F#, Nim, VB.NET con LINQ) y los que expresan lo mismo con una función de
filtrado (todo el resto). La forma cambia; la idea —describir el resultado en vez de construirlo
paso a paso— no. Y en varios de ellos hay un extra que conviene notar: el filtrado es perezoso, así
que la lista intermedia nunca llega a existir. Eso es lo transferible.

⏮️ [Volver a la clase 067](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
