# 🧬 El mismo programa en las familias de lenguajes — Clase 075

> [⬅️ Volver a la clase 075](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —construir un punto pasando `x` e `y` **por
nombre**— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros: `x` e `y`)
- **Salida** (stdout): `punto(x=<a>, y=<b>)`
- **Regla:** la función se llama pasando los argumentos por nombre, `punto(x = a, y = b)`

| stdin | esperado |
|---|---|
| `3 4` | `punto(x=3, y=4)` |
| `0 -2` | `punto(x=0, y=-2)` |
| `5 5` | `punto(x=5, y=5)` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí la familia se rompe por dentro: solo algunos tienen argumentos con nombre de verdad, el resto
los fabrica con una estructura de datos.

### Ruby

```ruby
def punto(x:, y:)
  "punto(x=#{x}, y=#{y})"
end

a, b = STDIN.gets.split.map(&:to_i)
puts punto(y: b, x: a)
```

### Perl

```perl
sub punto {
    my %arg = @_;   # sin parámetros declarados: los nombres se emulan con un hash
    return "punto(x=$arg{x}, y=$arg{y})";
}

my ($a, $b) = split ' ', <STDIN>;
print punto(y => $b, x => $a), "\n";
```

### Lua

```lua
-- Lua no tiene argumentos con nombre: se pasa una tabla, y la llamada
-- puede omitir los paréntesis cuando el único argumento es un constructor.
local function punto(t)
  return string.format("punto(x=%d, y=%d)", t.x, t.y)
end

local a, b = io.read("n", "n")
print(punto{ y = b, x = a })
```

### Tcl

```tcl
proc punto {args} {
    array set opt $args      ;# convención Tcl: pares nombre-valor recogidos en args
    return "punto(x=$opt(-x), y=$opt(-y))"
}

gets stdin linea
lassign [regexp -all -inline {\S+} $linea] a b
puts [punto -y $b -x $a]
```

### R

```r
punto <- function(x, y) sprintf("punto(x=%d, y=%d)", x, y)

v <- scan("stdin", what = integer(), n = 2, quiet = TRUE)
cat(punto(y = v[2], x = v[1]), "\n", sep = "")
```

**Qué reconocer:** los cinco imprimen lo mismo llamando con `y` **antes** que `x`, pero solo tres lo
hacen de verdad. Ruby tiene argumentos de palabra clave reales, y los dos puntos sin valor (`x:`,
`y:`) los declaran además como **obligatorios**: llamar sin uno de ellos es un error, no un `nil`. R
va incluso más lejos que Python y empareja el nombre **abreviado** mientras no sea ambiguo: con estos
dos parámetros, `punto(y = 4, x = 3)` y `punto(y = 4, 3)` dan lo mismo, porque R asigna primero los
argumentos con nombre y reparte los sueltos por los huecos que quedan. Perl y Tcl solo simulan: en
Perl la lista plana
`@_` se lee como un hash, así que `x => 3` es literalmente la cadena `"x"` seguida del 3, y en Tcl la
convención de guiones (`-x`) es cultura de la comunidad, no sintaxis del lenguaje.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

String punto({required int x, required int y}) => 'punto(x=$x, y=$y)';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print(punto(y: v[1], x: v[0]));
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene argumentos con nombre ni stdin: se emulan con un objeto.
package {
    public class Geometria {
        public static function punto(args:Object):String {
            return "punto(x=" + args.x + ", y=" + args.y + ")";
        }
        // Llamada: Geometria.punto({ y: 4, x: 3 });
    }
}
```

**Qué reconocer:** JavaScript resuelve esto desestructurando un objeto en la firma —lo que hace la
implementación de la clase—, y ActionScript se queda un paso antes: recibe el objeto entero y lee sus
campos, porque no tiene desestructuración. Dart es el único de la familia con argumentos nombrados
**de verdad**, con llaves en la declaración y dos puntos en la llamada; `required` es la parte que
los hace comparables a los de Ruby, porque sin él un parámetro nombrado es opcional y puede llegar
nulo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java **no tiene** argumentos nombrados: se pasan
por posición y el nombre del parámetro es puro comentario.

### Kotlin

```kotlin
fun punto(x: Int, y: Int): String = "punto(x=$x, y=$y)"

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println(punto(y = b, x = a))
}
```

### Scala

```scala
object Geometria {
  def punto(x: Int, y: Int): String = s"punto(x=$x, y=$y)"

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(punto(y = b, x = a))
  }
}
```

### Groovy

```groovy
// El primer parámetro Map recoge todos los pares nombre:valor de la llamada.
def punto(Map args) { "punto(x=${args.x}, y=${args.y})" }

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println punto(y: b, x: a)
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn punto [& {:keys [x y]}]
  (str "punto(x=" x ", y=" y ")"))

(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (punto :y b :x a)))
```

**Qué reconocer:** Kotlin y Scala llaman con `y = b, x = a` sin declarar nada especial —cualquier
parámetro puede usarse por nombre—, y por eso en ambos **renombrar un parámetro rompe a quien te
llama**: el nombre pasa a ser parte del contrato público, no un detalle interno como en Java. Groovy
y Clojure vuelven al truco de la estructura: Groovy declara un `Map` como primer parámetro y el
compilador empaqueta ahí los pares de la llamada; Clojure desestructura una lista de claves con
`{:keys [x y]}`. Los cuatro compilan al mismo bytecode posicional de la JVM.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System

// En F# los argumentos por nombre existen en miembros de tipo, no en funciones `let`.
type Geometria =
    static member Punto(x: int, y: int) = sprintf "punto(x=%d, y=%d)" x y

[<EntryPoint>]
let main _ =
    let v = Console.ReadLine().Trim().Split(' ') |> Array.map int
    printfn "%s" (Geometria.Punto(y = v.[1], x = v.[0]))
    0
```

### VB.NET

```vbnet
Module Programa
    Function Punto(x As Integer, y As Integer) As String
        Return String.Format("punto(x={0}, y={1})", x, y)
    End Function

    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Console.WriteLine(Punto(y:=Integer.Parse(p(1)), x:=Integer.Parse(p(0))))
    End Sub
End Module
```

**Qué reconocer:** VB.NET tuvo argumentos nombrados desde el principio con su propio operador `:=`,
y C# los copió en la versión 4.0 usando `:` a secas — el mismo mecanismo, distinta puntuación. F#
marca la frontera más clara de esta página: una función `let` **no** admite llamada por nombre, solo
los miembros de un tipo, porque una función currificada no tiene una lista de argumentos que nombrar,
tiene una cadena de funciones de un argumento.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C solo hay posiciones.

### C++

```cpp
#include <iostream>

struct Coords {
    int x;
    int y;
};

// C++ no tiene argumentos nombrados: lo más cercano son los
// inicializadores designados de C++20, que sí nombran cada campo.
void punto(Coords c) {
    std::cout << "punto(x=" << c.x << ", y=" << c.y << ")\n";
}

int main() {
    int a, b;
    std::cin >> a >> b;
    punto({.x = a, .y = b});
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Geometria : NSObject
+ (NSString *)puntoConX:(NSInteger)x y:(NSInteger)y;
@end

@implementation Geometria
+ (NSString *)puntoConX:(NSInteger)x y:(NSInteger)y {
    return [NSString stringWithFormat:@"punto(x=%ld, y=%ld)", (long)x, (long)y];
}
@end

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        printf("%s\n", [[Geometria puntoConX:a y:b] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** esta es la clase donde Objective-C brilla. El nombre del método está **partido
entre los argumentos** —`puntoConX:y:`—, así que cada valor de la llamada va precedido por su
etiqueta y leer la llamada es leer una frase. No son argumentos nombrados opcionales como los de
Kotlin: son **obligatorios y en orden fijo**, porque las etiquetas forman el nombre del método y
reordenarlas nombraría otro método. C++ no tiene nada de eso; su inicializador designado nombra los
campos de una estructura, que además deben ir en el orden de declaración.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno tiene argumentos
nombrados; ambos usan structs con campos nombrados, que es lo que hace la implementación Go de la
clase.

### Zig

```zig
const std = @import("std");

// Zig no tiene argumentos nombrados: se pasa una estructura anónima con campos nombrados.
const Punto = struct { x: i64, y: i64 };

fn imprimir(p: Punto) !void {
    try std.io.getStdOut().writer().print("punto(x={d}, y={d})\n", .{ p.x, p.y });
}

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try imprimir(.{ .y = b, .x = a });
}
```

### Nim

```nim
import std/strutils

proc punto(x, y: int): string =
  "punto(x=" & $x & ", y=" & $y & ")"

let v = stdin.readLine().splitWhitespace()
echo punto(y = parseInt(v[1]), x = parseInt(v[0]))
```

### D

```d
import std.stdio, std.array, std.string, std.conv, std.format;

struct Punto {
    long x;
    long y;
}

string punto(Punto p) {
    return format("punto(x=%d, y=%d)", p.x, p.y);
}

void main() {
    auto v = readln().strip().split();
    // Inicializador de struct con campos nombrados: lo más portable en D.
    Punto p = {x: v[0].to!long, y: v[1].to!long};
    writeln(punto(p));
}
```

**Qué reconocer:** Nim es el único de los tres con llamada por nombre nativa, y la escribe con `=`
como Kotlin. Zig y D hacen lo mismo que Go: mueven los nombres del punto de llamada a los **campos de
un tipo**. El `.{ .y = b, .x = a }` de Zig es una estructura anónima cuyo tipo se deduce del
parámetro, y ahí el orden sí da igual — que es tan cerca de un argumento nombrado como llega un
lenguaje que se niega a tener sintaxis oculta en la llamada.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL las columnas tienen nombre, pero los
argumentos de una función siguen siendo posicionales.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene argumentos por nombre: manda la posición.
% Lo más cercano es envolver cada valor en un término etiquetado, x(3) e y(4).
punto(x(X), y(Y), S) :- format(atom(S), "punto(x=~d, y=~d)", [X, Y]).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [A, B]),
    number_string(X, A),
    number_string(Y, B),
    punto(x(X), y(Y), S),
    writeln(S).
```

### Datalog

```datalog
% Datalog no tiene funciones ni llamadas: los "nombres" de los argumentos
% viven en el esquema de la relación, no en el punto de uso.
punto(3, 4).

coordenada_x(X) :- punto(X, _).
coordenada_y(Y) :- punto(_, Y).
```

**Qué reconocer:** aquí el nombre se va del todo. Un predicado Prolog identifica sus argumentos solo
por la posición, y la comunidad compensa con **términos etiquetados**: `x(3)` no es una llamada, es
un dato compuesto cuyo functor hace de etiqueta. Es la misma solución que Go con sus structs y que
JavaScript con su objeto, llevada al mundo de los términos. Datalog ni eso: el significado de la
primera columna es una convención documentada, exactamente igual que en una tabla SQL sin
`SELECT x AS ...`.

---

## Y de vuelta a la clase

Veinte lenguajes y una pregunta que los ordena: ¿el nombre del parámetro es parte del **contrato
público** o un detalle interno? Donde hay argumentos nombrados reales (Python, Ruby, Kotlin, Scala,
Dart, Nim, VB.NET) renombrar un parámetro rompe a quien llama. Donde no los hay, el nombre se
recupera con una estructura —objeto, hash, tabla, struct, término— o se pierde por completo. Eso es
lo transferible.

⏮️ [Volver a la clase 075](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
