# 🧬 El mismo programa en las familias de lenguajes — Clase 117

> [⬅️ Volver a la clase 117](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar solo los números pares de una lista, diciendo
**qué** queremos y no **cómo** recorrerla— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El estilo declarativo de esta clase se reduce a tres verbos: **seleccionar** (`WHERE`, `filter`),
**transformar** (`SELECT`, `map`) y **plegar** (`SUM`, `reduce`). La página es interesante porque no
todos los primos los tienen: unos los traen completos y perezosos, otros a medias, y un par se
niegan a ofrecerlos por principio. Ver dónde falta el vocabulario es lo que demuestra que
"declarativo" no es magia del lenguaje, sino biblioteca que alguien se molestó en escribir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacios
- **Salida** (stdout): `suma_pares=<suma de los pares>`
- **Regla:** suma de los `x` de la lista tales que `x` es par; si no hay ninguno, `0`

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma_pares=6` |
| `2 4 6` | `suma_pares=12` |
| `1 3 5` | `suma_pares=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python lo resuelve con una comprensión y PHP con `array_filter` + `array_sum`: la misma pareja
filtrar-plegar que verás repetirse toda la página.

### Ruby

```ruby
nums = STDIN.read.split.map(&:to_i)
puts "suma_pares=#{nums.select(&:even?).sum}"
```

### Perl

```perl
use List::Util qw(sum0);

my @nums = split ' ', do { local $/; <STDIN> };
# sum0 devuelve 0 con la lista vacía; sum devolvería undef.
printf "suma_pares=%d\n", sum0(grep { $_ % 2 == 0 } @nums);
```

### Lua

```lua
-- La biblioteca estándar de Lua no trae filter ni reduce: se recorre a mano.
local suma = 0
for palabra in io.read("a"):gmatch("%S+") do
  local x = tonumber(palabra)
  if x % 2 == 0 then suma = suma + x end
end
print("suma_pares=" .. suma)
```

### Tcl

```tcl
# Tcl tampoco tiene filter/reduce sobre listas: el bucle es el idioma.
set suma 0
foreach x [regexp -all -inline {\S+} [read stdin]] {
    if {$x % 2 == 0} { incr suma $x }
}
puts "suma_pares=$suma"
```

### R

```r
nums <- scan("stdin", quiet = TRUE)
# R es vectorial: la condición produce un vector lógico que indexa al propio vector.
cat(sprintf("suma_pares=%d\n", as.integer(sum(nums[nums %% 2 == 0]))))
```

**Qué reconocer:** Ruby y Perl tienen los tres verbos en la biblioteca (`select`/`sum`,
`grep`/`sum0`) y por eso el programa entra en una línea con la misma forma que `WHERE ... SUM` de
SQL. Lua y Tcl no los tienen, y el resultado es revelador: vuelven al bucle explícito con el
acumulador a la vista. No es que sean menos capaces —el resultado es idéntico—, es que el estilo
declarativo **es una biblioteca**, no una propiedad mística del lenguaje. R es el más declarativo de
los veinte y ni siquiera nombra la iteración: `nums %% 2 == 0` produce un vector de verdaderos y
falsos, y `nums[...]` lo usa para seleccionar. Eso es exactamente una cláusula `WHERE` aplicada a una
columna entera, y explica por qué R se parece tanto a una base de datos con sintaxis de programa.
Fíjate además en `sum0` de Perl: existe precisamente por el caso `1 3 5`, donde la lista filtrada
queda vacía.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  // where y fold son perezosos sobre Iterable: nada se materializa hasta el fold.
  final suma = nums.where((x) => x % 2 == 0).fold<int>(0, (a, b) => a + b);
  print('suma_pares=$suma');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: los datos llegan ya como Array.
// AS3 se quedó en ECMAScript 4: tiene filter y map, pero NO tiene reduce.
package {
    public class Pares {
        public static function suma(nums:Array):String {
            var pares:Array = nums.filter(function(x:int, i:int, a:Array):Boolean {
                return x % 2 == 0;
            });
            var total:int = 0;
            for each (var x:int in pares) {
                total += x;
            }
            return "suma_pares=" + total;
        }
    }
}
```

**Qué reconocer:** Dart encadena `where` y `fold` sobre `Iterable`, y lo hace **perezosamente**: el
`where` no construye una lista intermedia, solo describe la condición, y nada se recorre hasta que
el `fold` lo pide. Es el mismo trato que hace un motor SQL cuando no materializa la tabla
intermedia. ActionScript enseña el otro lado: se congeló en la propuesta de ECMAScript 4, cuando ya
existían `filter` y `map` pero `reduce` todavía no había entrado en el estándar. Por eso la mitad del
programa es declarativa y la otra mitad vuelve al bucle. Ver una biblioteca a medio construir es la
mejor prueba de la tesis: cada verbo declarativo llegó por separado y alguien tuvo que escribirlo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java), cuyos *streams* (Java 8) son literalmente un
motor de consultas: `stream().filter(...).sum()`.

### Kotlin

```kotlin
fun main() {
    val suma = readLine()!!.trim().split(Regex("\\s+"))
        .map { it.toInt() }
        .filter { it % 2 == 0 }
        .sum()
    println("suma_pares=$suma")
}
```

### Scala

```scala
object Pares {
  def main(args: Array[String]): Unit = {
    val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    // for-comprehension con guarda: azúcar de withFilter + map, ahora sobre una colección.
    val suma = (for (x <- nums if x % 2 == 0) yield x).sum
    println(s"suma_pares=$suma")
  }
}
```

### Groovy

```groovy
def nums = System.in.text.trim().split(/\s+/)*.toInteger()
// sum() sobre lista vacía devuelve null; sum(0) da el elemento neutro.
println "suma_pares=${nums.findAll { it % 2 == 0 }.sum(0)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))]
  ;; filter es perezoso; reduce con valor inicial 0 cubre la lista vacía.
  (println (str "suma_pares=" (reduce + 0 (filter even? nums)))))
```

**Qué reconocer:** los cuatro dicen lo mismo con los tres verbos de siempre, que SQL llama `SELECT`,
`WHERE` y `SUM`. La `for`-comprehension de Scala vuelve a aparecer, pero ahora sobre una colección en
vez de sobre un `Option`: mismo azúcar, distinto contenedor, que es justo el punto de la clase
anterior —lo que sabe hacer `flatMap` no depende de qué haya dentro—. El detalle honesto está en
Groovy: `sum()` sobre la lista vacía devuelve `null`, y el caso `1 3 5` produce exactamente esa lista
vacía, así que hay que escribir `sum(0)`. Es el mismo problema que obliga a poner
`COALESCE(sum(x), 0)` en la implementación SQL de la clase, y Clojure lo evita con el `0` inicial
de `reduce`. Toda
agregación necesita un elemento neutro; los lenguajes que lo olvidan te devuelven un nulo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1), donde LINQ nació precisamente para meter SQL
dentro del lenguaje.

### F\#

```fsharp
let separadores = [| ' '; '\t'; '\n'; '\r' |]

let suma =
    stdin.ReadToEnd().Split(separadores, System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
    |> Array.filter (fun x -> x % 2 = 0)
    |> Array.sum

printfn "suma_pares=%d" suma
```

### VB.NET

```vbnet
Imports System.Linq

Module Pares
    Sub Main()
        Dim p = Console.In.ReadToEnd().Split(
            New Char() {" "c, vbTab, vbCr, vbLf}, StringSplitOptions.RemoveEmptyEntries)

        ' VB.NET tiene sintaxis de consulta integrada: se lee casi como SQL.
        Dim suma = Aggregate s In p
                   Let x = CInt(s)
                   Where x Mod 2 = 0
                   Into Sum(x)

        Console.WriteLine("suma_pares=" & suma)
    End Sub
End Module
```

**Qué reconocer:** VB.NET es, de los veinte lenguajes, el que más se parece a SQL a simple vista:
`Aggregate ... Where ... Into Sum(...)` son palabras clave del lenguaje, no llamadas a métodos, y el
compilador las traduce a las mismas llamadas que escribe F\# con `|>`. Dos sintaxis, un solo plan de
ejecución. Y hay un detalle de diseño que conviene notar: LINQ pone el **origen primero**
(`From`/`Aggregate ... In`) y la proyección al final, al revés que SQL, que escribe `SELECT` antes
que `FROM` aunque el motor lo evalúe después. Ese cambio de orden no es cosmético: es lo que permite
al editor autocompletar los campos, porque cuando llegas a la proyección ya se sabe de dónde salen
los datos.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C no hay nada declarativo: hay un bucle, un
acumulador y un `if`.

### C++

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x;) nums.push_back(x);

    // accumulate con el filtro dentro del lambda: selección y pliegue en una pasada.
    // Desde C++20 se puede escribir con rangos: nums | std::views::filter(...)
    const int suma = std::accumulate(nums.begin(), nums.end(), 0,
                                     [](int a, int x) { return x % 2 == 0 ? a + x : a; });

    std::cout << "suma_pares=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSMutableArray<NSNumber *> *nums = [NSMutableArray array];
        for (int x; scanf("%d", &x) == 1;) [nums addObject:@(x)];

        // NSPredicate es un motor de consultas de verdad, evaluado en tiempo de ejecución.
        NSArray *pares = [nums filteredArrayUsingPredicate:
            [NSPredicate predicateWithBlock:^BOOL(NSNumber *x, NSDictionary *b) {
                return x.intValue % 2 == 0;
            }]];

        // @sum.self es un operador de colección de KVC: la agregación como texto.
        NSNumber *suma = [pares valueForKeyPath:@"@sum.self"];
        printf("suma_pares=%d\n", suma.intValue);
    }
    return 0;
}
```

**Qué reconocer:** C++ no tiene lenguaje de consulta, tiene **algoritmos sobre iteradores**:
`accumulate`, `copy_if`, y desde C++20 las vistas de rangos, que se encadenan con `|` como una
tubería de shell. Todo se resuelve en tiempo de compilación, así que la abstracción no cuesta nada.
Objective-C guarda la sorpresa de esta página: `NSPredicate` y el operador `@sum.self` de KVC son un
motor de consultas real, con predicados que se pueden construir desde una cadena de texto y evaluar
en tiempo de ejecución. No es casualidad que se parezca tanto a SQL —es el mismo mecanismo que Core
Data traduce a SQL cuando la colección resulta ser una tabla—. De los veinte lenguajes, este es el
único donde la consulta es un **dato** que se puede pasar, guardar y componer, igual que una cadena
`WHERE`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust encadena iteradores
perezosos (`filter().sum()`); Go, fiel a su estilo, escribe el bucle.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");

    // Zig no ofrece filter ni reduce: su estilo rechaza las abstracciones que
    // esconden reservas de memoria o flujo de control.
    var suma: i64 = 0;
    while (it.next()) |t| {
        const x = try std.fmt.parseInt(i64, t, 10);
        if (@rem(x, 2) == 0) suma += x;
    }

    try std.io.getStdOut().writer().print("suma_pares={d}\n", .{suma});
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
# filterIt es una plantilla: `it` es el elemento, y todo se expande en compilación.
echo "suma_pares=", nums.filterIt(it mod 2 == 0).sum()
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv, std.string;

void main() {
    // std.algorithm es perezoso: filter no construye ningún array intermedio.
    const suma = readln().strip().split()
        .map!(to!int)
        .filter!(x => x % 2 == 0)
        .sum();
    writefln("suma_pares=%d", suma);
}
```

**Qué reconocer:** D trae el vocabulario declarativo completo y **perezoso** sobre rangos, que es lo
mismo que hacen los iteradores de Rust: `filter` no recorre nada, devuelve un rango que recorrerá
cuando `sum` se lo pida, así que no hay array intermedio ni reserva de memoria. Nim lo consigue por
otra vía, con plantillas (`filterIt`) que se expanden en tiempo de compilación. Zig se niega, y la
negativa es deliberada: su regla de estilo es que ninguna llamada oculte una reserva de memoria ni un
salto, y `filter().sum()` oculta ambas cosas, así que el bucle explícito **es** el idioma de Zig, no
una carencia. Nota final para los tres: con `1 3 5` los tres devuelven `0` sin ningún caso especial,
porque plegar el conjunto vacío da el elemento neutro. Es lo que SQL hace mal al devolver `NULL`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql), que en esta clase es el protagonista: `WHERE` +
`SUM` es el enunciado del problema, casi palabra por palabra.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpias),
    maplist([S, N]>>number_string(N, S), Limpias, Nums),
    % aggregate_all es el SUM ... WHERE de Prolog: recorre TODAS las soluciones
    % del objetivo y las pliega. Con cero soluciones devuelve 0, no nulo.
    aggregate_all(sum(X), (member(X, Nums), 0 is X mod 2), Suma),
    format("suma_pares=~d~n", [Suma]).
```

### Datalog

```datalog
% Datalog no lee stdin: cada número entra como un hecho.
num(1). num(2). num(3). num(4).

par(X) :- num(X), X % 2 = 0.

% Datalog puro solo deriva hechos: no sabe agregar sobre un conjunto.
% La agregación es una extensión de dialecto (Soufflé, DDlog):
suma_pares(S) :- S = sum X : { par(X) }.
```

**Qué reconocer:** aquí la comparación es casi una identidad. `aggregate_all(sum(X), Objetivo, S)` de
Prolog **es** `SELECT SUM(x) ... WHERE objetivo`: describes la condición, el motor enumera todas las
soluciones y las pliega, y en ningún momento dices cómo recorrer nada. Prolog además acierta donde
SQL falla: con cero soluciones devuelve `0`, mientras que `SUM` en SQL devuelve `NULL` y obliga al
`COALESCE` que ves en la implementación de la clase. Datalog puro se queda corto y conviene decirlo
sin adornos: solo sabe **derivar hechos nuevos a partir de hechos**, no calcular sobre el conjunto de
resultados, así que la agregación es una extensión que añaden los dialectos prácticos. Lo que Datalog
compra a cambio de esa pobreza es enorme —sin recursión no acotada ni términos compuestos, toda
consulta **termina**—, y esa garantía es también la razón por la que un `SELECT` sin funciones de
ventana nunca se cuelga.

---

## Y de vuelta a la clase

Veinte lenguajes y una sola frase: *de estos números, quédate con los pares y súmalos*. Los que
tienen los tres verbos la escriben tal cual; los que no, la traducen a un bucle con acumulador. Lo
que cambia no es el resultado sino **quién decide el recorrido**: tú o el motor. Y donde lo decide el
motor —SQL, Prolog, los rangos perezosos de D— aparece el otro premio: puede reordenar el trabajo sin
pedirte permiso.

⏮️ [Volver a la clase 117](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
