# 🧬 El mismo programa en las familias de lenguajes — Clase 073

> [⬅️ Volver a la clase 073](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —definir `suma(a, b)` y devolver su resultado—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b>`
- **Regla:** `suma(a, b) = a + b`

| stdin | esperado |
|---|---|
| `3 4` | `suma=7` |
| `10 20` | `suma=30` |
| `-5 5` | `suma=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La firma nombra los parámetros pero no su tipo: lo que la función promete se descubre al usarla, no
al leerla.

### Ruby

```ruby
def suma(a, b)
  a + b
end

a, b = STDIN.gets.split.map(&:to_i)
puts "suma=#{suma(a, b)}"
```

### Perl

```perl
sub suma {
    my ($x, $y) = @_;   # la firma no se declara: los argumentos llegan en @_
    return $x + $y;
}

my ($a, $b) = split ' ', <STDIN>;
printf "suma=%d\n", suma($a, $b);
```

### Lua

```lua
local function suma(a, b)
  return a + b
end

local a, b = io.read("n", "n")
print("suma=" .. suma(a, b))
```

### Tcl

```tcl
proc suma {a b} {
    return [expr {$a + $b}]
}

gets stdin linea
lassign [regexp -all -inline {\S+} $linea] a b
puts "suma=[suma $a $b]"
```

### R

```r
suma <- function(a, b) a + b

v <- scan("stdin", what = integer(), n = 2, quiet = TRUE)
cat(sprintf("suma=%d\n", suma(v[1], v[2])))
```

**Qué reconocer:** los cinco escriben la misma firma de dos parámetros, pero solo tres la
**declaran**. Perl no tiene lista de parámetros: toda función recibe un único array `@_` y la
primera línea del cuerpo es la que inventa los nombres; cambiar la firma en Perl es cambiar un
`my (...) = @_`, no la cabecera. Ruby y R **devuelven la última expresión evaluada** sin escribir
`return`, mientras Perl y Tcl lo escriben por costumbre. Tcl lleva su radicalidad al retorno: `suma`
devuelve una cadena, porque en Tcl todo valor lo es, y `expr` es quien hace la aritmética.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int suma(int a, int b) => a + b;

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('suma=${suma(v[0], v[1])}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la firma y el retorno.
package {
    public class Calculo {
        public static function suma(a:int, b:int):int {
            return a + b;
        }

        public static function linea(a:int, b:int):String {
            return "suma=" + suma(a, b);
        }
    }
}
```

**Qué reconocer:** ambos anotan el tipo de retorno **después** de la lista de parámetros —`:int` en
ActionScript, `int` delante en Dart— y ambos lo exigen en la firma, cosa que JavaScript no hace y
TypeScript sí permite. La flecha `=>` de Dart es la misma idea que la función flecha de JS: cuerpo de
una sola expresión, retorno implícito. ActionScript conserva el `return` explícito porque su bloque
siempre es un bloque, nunca una expresión.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode; lo que cambia
es cuánta firma hay que escribir para decir "dos enteros entran, uno sale".

### Kotlin

```kotlin
fun suma(a: Int, b: Int): Int = a + b

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("suma=${suma(a, b)}")
}
```

### Scala

```scala
object Calculo {
  def suma(a: Int, b: Int): Int = a + b

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(s"suma=${suma(a, b)}")
  }
}
```

### Groovy

```groovy
int suma(int a, int b) { a + b }

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "suma=${suma(a, b)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn suma [a b] (+ a b))

(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "suma=" (suma a b))))
```

**Qué reconocer:** Kotlin y Scala ponen el tipo **detrás** del nombre (`a: Int`) y el de retorno al
final, invirtiendo el orden de Java; es la notación que usan casi todos los lenguajes con inferencia,
porque el tipo puede omitirse sin dejar un hueco en la línea. En los cuatro el cuerpo de una sola
expresión **es** el valor devuelto: Kotlin y Scala con `=`, Groovy dejando caer el `return`, Clojure
porque una función es literalmente una expresión. Clojure además no declara tipos en la firma:
`[a b]` es un vector de nombres y nada más.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System

let suma a b = a + b

[<EntryPoint>]
let main _ =
    let v = Console.ReadLine().Trim().Split(' ') |> Array.map int
    printfn "suma=%d" (suma v.[0] v.[1])
    0
```

### VB.NET

```vbnet
Module Programa
    Function Suma(a As Integer, b As Integer) As Integer
        Return a + b
    End Function

    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Console.WriteLine("suma=" & Suma(Integer.Parse(p(0)), Integer.Parse(p(1))))
    End Sub
End Module
```

**Qué reconocer:** VB.NET separa en la propia palabra clave lo que C# distingue con el tipo de
retorno: `Function` devuelve un valor, `Sub` no devuelve nada. F# muestra el otro extremo: `suma a b`
no tiene paréntesis ni comas porque la función está **currificada** —recibe `a` y devuelve otra
función que espera `b`—, de modo que `suma 3` es un valor perfectamente válido. Los tres acaban
siendo el mismo método sobre el CLR.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Tipo de retorno delante, parámetros declarados uno a
uno.

### C++

```cpp
#include <iostream>

int suma(int a, int b) {
    return a + b;
}

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << "suma=" << suma(a, b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Calculadora : NSObject
+ (NSInteger)sumaDe:(NSInteger)a con:(NSInteger)b;
@end

@implementation Calculadora
+ (NSInteger)sumaDe:(NSInteger)a con:(NSInteger)b {
    return a + b;
}
@end

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        printf("suma=%ld\n", (long)[Calculadora sumaDe:a con:b]);
    }
    return 0;
}
```

**Qué reconocer:** la función libre de C++ es la de C sin un solo cambio. Objective-C hace lo que
ningún otro lenguaje de esta página: **parte el nombre del método entre los argumentos**. La firma no
se llama `suma`, se llama `sumaDe:con:`, y en la llamada cada valor va precedido por su trozo de
nombre. Es el ancestro directo de las etiquetas de argumento de Swift, y explica por qué las API de
Apple se leen como frases.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Firmas explícitas, sin
conversiones ocultas entre tipos.

### Zig

```zig
const std = @import("std");

fn suma(a: i64, b: i64) i64 {
    return a + b;
}

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try std.io.getStdOut().writer().print("suma={d}\n", .{suma(a, b)});
}
```

### Nim

```nim
import std/strutils

proc suma(a, b: int): int = a + b

let v = stdin.readLine().splitWhitespace()
echo "suma=", suma(parseInt(v[0]), parseInt(v[1]))
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

int suma(int a, int b) {
    return a + b;
}

void main() {
    auto v = readln().split().map!(to!int).array;
    writefln("suma=%d", suma(v[0], v[1]));
}
```

**Qué reconocer:** el tipo de retorno va detrás de los parámetros en los tres, como en Rust
(`-> i64`) y Go. Zig lo escribe sin flecha y añade algo que no existe en el resto: el `!void` de
`main` es un tipo de retorno que dice "esto puede fallar", y el error forma parte de la firma. Nim
comprime `a, b: int` en una sola anotación para parámetros consecutivos del mismo tipo, un atajo que
Go también permite (`func suma(a, b int)`).

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay funciones que "devuelvan": hay relaciones
que se cumplen.

### Prolog

```prolog
:- initialization(main, main).

% suma/3: no hay valor de retorno, el resultado es el tercer argumento.
suma(A, B, Total) :- Total is A + B.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    suma(A, B, Total),
    format("suma=~d~n", [Total]).
```

### Datalog

```datalog
% Datalog no tiene funciones ni E/S: la "firma" es el nombre más la aridad,
% y el resultado es una columna más de la relación.
entrada(3, 4).

suma(A, B, S) :- entrada(A, B), S = A + B.
```

**Qué reconocer:** aquí desaparece el retorno. `suma/3` no devuelve nada: **relaciona** tres valores,
y por eso el resultado ocupa un argumento más. Esa barra con el número es literal: en Prolog la
aridad forma parte de la identidad del predicado, así que `suma/2` y `suma/3` son predicados
distintos que no se estorban. SQL hace la misma renuncia cuando una consulta produce filas en vez de
un valor de retorno.

---

## Y de vuelta a la clase

Veinte lenguajes, una sola función de dos parámetros, y tres decisiones que se repiten con distinto
reparto: si el tipo se declara o se infiere, si el retorno se escribe o es la última expresión, y si
el resultado sale por el nombre de la función o por un argumento más. Eso es lo transferible.

⏮️ [Volver a la clase 073](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
