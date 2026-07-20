# 🧬 El mismo programa en las familias de lenguajes — Clase 091

> [⬅️ Volver a la clase 091](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —recibir dos enteros como una tupla e intercambiar
sus componentes— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` — dos enteros separados por espacio
- **Salida** (stdout): `tupla=(<b>, <a>)`
- **Regla:** `(a, b) → (b, a)` — el par se accede **por posición**, nunca por nombre de campo

| stdin | esperado |
|---|---|
| `3 4` | `tupla=(4, 3)` |
| `0 -2` | `tupla=(-2, 0)` |
| `5 5` | `tupla=(5, 5)` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tiene tuplas de verdad; el resto de la familia, no. Aquí el "registro posicional" se simula
casi siempre con la lista de siempre.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
t = [a, b]              # Ruby no tiene tupla: un Array de dos posiciones hace el papel
t = [t[1], t[0]]
puts "tupla=(#{t[0]}, #{t[1]})"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
my @t = ($a, $b);   # Perl simula la tupla con una lista: no hay tipo de aridad fija
@t = @t[1, 0];      # slice por posición: reordena sin variable temporal
printf "tupla=(%d, %d)\n", @t;
```

### Lua

```lua
local a, b = io.read("n", "n")
local t = {a, b}                  -- t[1] y t[2]: Lua numera desde 1
t[1], t[2] = t[2], t[1]           -- asignación múltiple: el intercambio sin temporal
print(string.format("tupla=(%d, %d)", t[1], t[2]))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
set t [list $b $a]
puts "tupla=([lindex $t 0], [lindex $t 1])"  ;# lindex sí cuenta desde 0
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
t <- v[c(2, 1)]  # se reordena el vector con un vector de índices, base 1
cat(sprintf("tupla=(%d, %d)\n", t[1], t[2]))
```

**Qué reconocer:** ninguno de los cinco tiene un tipo tupla, así que todos lo **simulan** con su
única estructura secuencial, y eso tiene una consecuencia real: nada impide que ese "par" acabe con
tres elementos, porque la aridad no forma parte de ningún tipo. Lo que sí comparten con Python es la
**asignación múltiple**, el gesto que hace idiomático `a, b = b, a` sin variable temporal. Y vuelve
la trampa de la familia: en Lua el primer componente es `t[1]` y en R es `v[1]`, mientras que el
`lindex` de Tcl arranca en 0 — copiar el índice de un lenguaje al otro rompe el programa en silencio.
R además ni siquiera indexa dos veces: reordena el vector entero pasándole el vector de posiciones
`c(2, 1)`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final (int, int) t = (v[0], v[1]);   // registro posicional de Dart 3: tupla real
  final intercambiado = (t.$2, t.$1);  // los campos se llaman $1, $2: pura posición
  print('tupla=(${intercambiado.$1}, ${intercambiado.$2})');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene tuplas ni stdin: lo más cercano es un Array de dos posiciones.
package {
    public class Tupla {
        public static function intercambiar(a:int, b:int):String {
            var t:Array = [a, b];
            t = [t[1], t[0]];
            return "tupla=(" + t[0] + ", " + t[1] + ")";
        }
    }
}
```

**Qué reconocer:** los dos parten del mundo de JavaScript, donde durante veinte años la tupla fue un
array de dos elementos y el desempaquetado llegó tarde con `const [x, y] = par`. AS3 sigue en ese
punto: sin tipo de par, la aridad es una convención. Dart en cambio incorporó **registros** en su
versión 3 y son tuplas de verdad —`(int, int)` es un tipo, con aridad y tipos por componente
comprobados al compilar—, y los campos se llaman literalmente `$1` y `$2` para dejar claro que se
accede por **posición**, no por nombre. Es el mismo salto que dan las tuplas de TypeScript
(`[number, number]`) sobre el array suelto de JS.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM no tiene tuplas: cada lenguaje se
inventa las suyas, y se nota en la ergonomía.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val t = Pair(a, b)          // Kotlin solo llega hasta Pair y Triple
    val (x, y) = t.second to t.first
    println("tupla=($x, $y)")
}
```

### Scala

```scala
object Tupla extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val t: (Int, Int) = (a, b)  // tupla real, hasta 22 componentes, con tipo propio
  val (x, y) = t.swap
  println(s"tupla=($x, $y)")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def t = new Tuple2(a, b)  // Tuple2 implementa List: se accede por índice base 0
println "tupla=(${t[1]}, ${t[0]})"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; No hay tipo tupla: un vector de dos elementos hace de registro posicional,
;; y el propio vector es invocable como función de su índice.
(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))
      t     [a b]]
  (println (format "tupla=(%d, %d)" (t 1) (t 0))))
```

**Qué reconocer:** cuatro respuestas distintas a la misma carencia de Java. **Scala tiene tuplas
reales**: `(Int, Int)` es un tipo de primera clase con aridad hasta 22, desempaquetado en el `val` y
hasta un `swap` propio para pares. **Kotlin se queda corto a propósito**: solo ofrece `Pair` y
`Triple`, y su documentación recomienda una `data class` con nombres en cuanto haya más de dos o
tres campos —posición para lo trivial, nombres para lo demás—. Groovy tiene `Tuple2`, pero como
implementa `List` se acaba accediendo por índice, con la aridad garantizada solo por el nombre de la
clase. Clojure ni lo intenta: el vector persistente `[a b]` es el registro posicional, y `(t 1)`
funciona porque en Clojure el vector **es** una función de su índice.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR sí trae tuplas en la propia plataforma,
así que aquí los tres primos comparten tipo.

### F\#

```fsharp
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
let t = (a, b)          // tupla nativa: el tipo se escribe int * int (producto cartesiano)
let (x, y) = (snd t, fst t)
printfn "tupla=(%d, %d)" x y
```

### VB.NET

```vbnet
Imports System

Module Tupla
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        ' ValueTuple: los campos posicionales se llaman Item1, Item2 y empiezan en 1.
        Dim t = (Integer.Parse(v(0)), Integer.Parse(v(1)))
        Dim intercambiado = (t.Item2, t.Item1)
        Console.WriteLine($"tupla=({intercambiado.Item1}, {intercambiado.Item2})")
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `System.ValueTuple`, una estructura de valor sin reserva en el
heap, y por eso el `(a, b)` de C#, de F# y de VB.NET son literalmente el mismo tipo cruzando el
límite entre lenguajes. La diferencia está en cómo se nombran los componentes: VB.NET y C# usan
`Item1`/`Item2` —numerados desde **1**, no desde 0, a diferencia de cualquier arreglo del mismo
lenguaje—, mientras que F# prefiere `fst`/`snd` y el desempaquetado por patrón. F# además escribe el
tipo como `int * int`, notación de **producto cartesiano** que explica de dónde viene la idea:
una tupla es el producto de sus tipos, y su aridad es parte del tipo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene tuplas: tiene `struct`, que es un
registro con **nombres**, no con posiciones.

### C++

```cpp
#include <iostream>
#include <tuple>

int main() {
    int a = 0, b = 0;
    std::cin >> a >> b;
    std::tuple<int, int> t{a, b};  // acceso por std::get<N>: el índice va en el TIPO
    t = std::make_tuple(std::get<1>(t), std::get<0>(t));
    std::cout << "tupla=(" << std::get<0>(t) << ", " << std::get<1>(t) << ")\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Objective-C no tiene tuplas: se usa un struct de C, que nombra sus campos.
typedef struct { int primero; int segundo; } Par;

int main(void) {
    @autoreleasepool {
        Par t;
        scanf("%d %d", &t.primero, &t.segundo);
        Par intercambiado = { t.segundo, t.primero };  // el orden del literal sí es posicional
        printf("tupla=(%d, %d)\n", intercambiado.primero, intercambiado.segundo);
    }
    return 0;
}
```

**Qué reconocer:** aquí se ve la frontera exacta entre tupla y registro. C++ añadió `std::tuple`
sobre C, y su acceso `std::get<0>(t)` tiene una peculiaridad que delata el mecanismo: el índice es
un **parámetro de plantilla**, resuelto al compilar, así que no se puede escribir un bucle que
recorra los componentes como si fuera un arreglo. Objective-C se queda con el `struct` de C, donde
los campos tienen nombre; lo único posicional que sobrevive es el literal de inicialización
`{ t.segundo, t.primero }`, que sí depende del orden de declaración. Esa es la lección: una tupla
identifica sus componentes por **dónde están**, un registro por **cómo se llaman**, y C++ es de los
pocos que ofrece las dos cosas en el mismo lenguaje.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust tiene tuplas
nativas; Go solo múltiples valores de retorno, que no son un tipo.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, linea, " \r"), " ");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);

    // En Zig la tupla es un struct anónimo cuyos campos se llaman "0" y "1".
    const t = .{ a, b };
    const intercambiado = .{ t[1], t[0] };
    const out = std.io.getStdOut().writer();
    try out.print("tupla=({d}, {d})\n", .{ intercambiado[0], intercambiado[1] });
}
```

### Nim

```nim
import std/strutils

let campos = stdin.readLine().splitWhitespace()
# Nim unifica tupla y registro: los campos tienen nombre Y posición a la vez.
let t: tuple[a, b: int] = (parseInt(campos[0]), parseInt(campos[1]))
let intercambiado = (t.b, t.a)
echo "tupla=(", intercambiado[0], ", ", intercambiado[1], ")"
```

### D

```d
import std.stdio, std.array, std.conv, std.typecons;

void main() {
    auto campos = readln().split();
    auto t = tuple(campos[0].to!int, campos[1].to!int);  // std.typecons, no palabra clave
    auto intercambiado = tuple(t[1], t[0]);
    writefln("tupla=(%d, %d)", intercambiado[0], intercambiado[1]);
}
```

**Qué reconocer:** los tres desmontan la tupla y enseñan de qué está hecha. En Zig es un **struct
anónimo** cuyos campos se llaman literalmente `"0"` y `"1"`, por eso `t[0]` funciona pero el índice
tiene que ser conocido al compilar, igual que en `std::tuple`. Nim borra la frontera de la clase
anterior: su `tuple[a, b: int]` se puede leer por nombre (`t.a`) **y** por posición (`t[0]`), las
dos cosas sobre el mismo valor. D ni siquiera la trae en el lenguaje: `tuple` viene de la biblioteca
`std.typecons`, construida con plantillas — la prueba de que una tupla no necesita sintaxis
especial, solo un tipo genérico sobre una lista de tipos.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En el modelo relacional una fila **es** una
tupla: el nombre viene de ahí.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    T = par(A, B),  % término compuesto: el functor par/2 y su aridad son "el tipo"
    T = par(X, Y),  % unificación: extrae los componentes por posición, sin accesores
    format("tupla=(~d, ~d)~n", [Y, X]).
```

### Datalog

```datalog
% Datalog no tiene E/S: toda relación ES una tupla, así que la fila par(3, 4)
% es el registro posicional y el intercambio es una regla que reordena argumentos.
par(3, 4).

intercambiado(B, A) :- par(A, B).
```

**Qué reconocer:** estas dos familias son el origen del concepto y por eso lo expresan con menos
ceremonia que nadie. Prolog usa **términos compuestos**: `par(A, B)` no es una llamada sino un dato,
identificado por su functor y su aridad —`par/2` y `par/3` son cosas distintas—, y los componentes
se sacan **unificando** con el patrón, sin `.first`, sin `Item1` y sin índices. Datalog lo reduce a
lo mínimo: una fila de una relación es la tupla, e intercambiar es escribir la regla con los
argumentos al revés, exactamente el `SELECT b, a FROM par` de SQL. Aquí no hay pregunta de si el
índice empieza en 0 o en 1, porque no hay índices: hay posiciones en una cabecera, y quien las lee
es el motor.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una escala clara: de los que **no tienen tupla** y la simulan
con listas (Ruby, Perl, AS3), a los que la ofrecen a medias (`Pair` de Kotlin, `Tuple2` de Groovy),
a los que la tienen como tipo con aridad comprobada (Scala, F#, Dart 3, Rust), hasta los que la
convierten en el dato fundamental del lenguaje (Prolog, Datalog, SQL). Saber en qué escalón está el
lenguaje que tienes delante es lo transferible.

⏮️ [Volver a la clase 091](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
