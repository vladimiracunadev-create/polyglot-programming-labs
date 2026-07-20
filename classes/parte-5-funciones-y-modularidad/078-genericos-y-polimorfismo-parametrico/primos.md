# 🧬 El mismo programa en las familias de lenguajes — Clase 078

> [⬅️ Volver a la clase 078](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una función que devuelve el mayor de dos valores y
sirve para cualquier tipo comparable— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

La pregunta de fondo no es "¿tiene genéricos?" sino **cuándo existe el tipo**: en los dinámicos no
existe nunca, en la JVM y el CLR se borra o se conserva, y en C++, D o Zig el compilador **genera
una función nueva** por cada tipo que uses.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** `max<T>(a, b) = a` si `a > b`, si no `b`

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En esta familia la función ya es genérica sin decirlo: no hay tipo que parametrizar. El precio es
que el error de tipo, si lo hay, aparece **en tiempo de ejecución**.

### Ruby

```ruby
def mayor(a, b)
  a > b ? a : b   # sirve para cualquier objeto que responda a <=> (mixin Comparable)
end

a, b = STDIN.gets.split.map(&:to_i)
puts "max=#{mayor(a, b)}"
```

### Perl

```perl
# Perl no es genérico en la comparación: el operador elige el tipo.
# `>` compara numéricamente; para cadenas habría que escribir `gt`.
sub mayor {
    my ($x, $y) = @_;
    return $x > $y ? $x : $y;
}

my ($x, $y) = split ' ', <STDIN>;
printf "max=%d\n", mayor($x, $y);
```

### Lua

```lua
local function mayor(a, b)
  if a > b then return a end   -- `>` se puede redefinir por tipo con el metamétodo __lt
  return b
end

local a, b = io.read("n", "n")
print(string.format("max=%d", mayor(a, b)))
```

### Tcl

```tcl
proc mayor {a b} {
    return [expr {$a > $b ? $a : $b}]
}

gets stdin linea
lassign [split $linea] a b
puts "max=[mayor $a $b]"
```

### R

```r
mayor <- function(a, b) if (a > b) a else b

v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("max=%d\n", mayor(v[1], v[2])))
```

**Qué reconocer:** el polimorfismo aquí no es *paramétrico* sino **de duck typing**: la función
acepta lo que sea y falla solo si el objeto no sabe compararse. Ruby lo formaliza con el mixin
`Comparable`, que deriva `>`, `<` y `between?` de un único `<=>` — es lo más cerca que llega la
familia a una restricción de tipo. Lua permite redefinir la comparación por tipo con el metamétodo
`__lt`. Y Perl es el contraejemplo honesto: **no puede** ser genérico en esta función, porque el
operador —`>` o `gt`— es quien decide si los operandos son números o cadenas; ahí el tipo lo pone la
sintaxis, no el valor.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

T mayor<T extends Comparable<dynamic>>(T a, T b) => a.compareTo(b) > 0 ? a : b;

void main() {
  final v = stdin.readLineSync()!.trim().split(' ').map(int.parse).toList();
  print('max=${mayor(v[0], v[1])}');
}
```

### ActionScript 3

```actionscript
package {
    public class Comparador {
        // AS3 no tiene genéricos de usuario: el único tipo parametrizado del
        // lenguaje es Vector.<T>, tratado como caso especial por el compilador.
        // Para una función genérica solo queda el tipo comodín `*`.
        public static function mayor(a:*, b:*):* {
            return a > b ? a : b;
        }
    }
}
```

**Qué reconocer:** Dart y TypeScript comparten el patrón `<T extends ...>` y la **restricción**
como forma de justificar la operación: sin `Comparable`, el compilador no dejaría llamar a
`compareTo`. La diferencia está en el destino: los tipos de TypeScript se borran al compilar a
JavaScript y no queda rastro, mientras que Dart **conserva** el argumento de tipo en ejecución. AS3
enseña el escalón anterior de la familia: sin genéricos, la única salida es `*`, el tipo que apaga
toda comprobación — el `any` de TypeScript, pero sin alternativa.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Los genéricos de la JVM se **borran** (*type
erasure*): existen para el compilador y desaparecen en el bytecode.

### Kotlin

```kotlin
fun <T : Comparable<T>> mayor(a: T, b: T): T = if (a > b) a else b

fun main() {
    val (a, b) = readLine()!!.trim().split(" ").map { it.toInt() }
    println("max=${mayor(a, b)}")
}
```

### Scala

```scala
object Comparador {
  // La restricción no viaja en el tipo: llega como parámetro implícito.
  def mayor[T](a: T, b: T)(implicit ord: Ordering[T]): T =
    if (ord.gt(a, b)) a else b

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(s"max=${mayor(a, b)}")
  }
}
```

### Groovy

```groovy
// Groovy acepta la sintaxis genérica de Java, pero al despachar dinámicamente
// no necesita declararla: basta con que el objeto implemente Comparable.
def mayor(a, b) { a > b ? a : b }

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "max=${mayor(a, b)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn mayor [a b] (if (pos? (compare a b)) a b))   ; compare es polimórfico, sin tipos

(let [[a b] (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "max=" (mayor a b))))
```

**Qué reconocer:** los cuatro corren sobre una máquina virtual que **no sabe nada de `T`**. Kotlin
copia el modelo de Java y añade azúcar: `a > b` se traduce a `a.compareTo(b) > 0` gracias a la
restricción. Scala rompe con el modelo y expresa la restricción como un **valor**, el `Ordering[T]`
implícito: en vez de exigir que el tipo implemente una interfaz, se pasa por separado la prueba de
que sabe compararse —así funciona incluso con tipos ajenos que no puedes modificar—. Groovy y
Clojure ni se molestan: resuelven la comparación en ejecución. Como el borrado es real, en los cuatro
`mayor` compila a **una sola** función que trabaja con `Object`; en la clase 081 verás que Rust hace
lo contrario.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR es la excepción entre las máquinas
virtuales: los genéricos están **reificados**, el tipo sobrevive en ejecución.

### F\#

```fsharp
// El tipo se infiere: 'a when 'a : comparison. No hace falta escribirlo.
let mayor a b = if a > b then a else b

let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "max=%d" (mayor a b)
```

### VB.NET

```vbnet
Module Comparador
    Function Maximo(Of T As IComparable(Of T))(a As T, b As T) As T
        Return If(a.CompareTo(b) > 0, a, b)
    End Function

    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Console.WriteLine($"max={Maximo(Integer.Parse(v(0)), Integer.Parse(v(1)))}")
    End Sub
End Module
```

**Qué reconocer:** la diferencia con la JVM es de fondo, no de sintaxis. El CLR **conserva** el
argumento de tipo, así que `typeof(T)` funciona y el JIT compila una versión especializada para cada
tipo por valor —`Maximo(Of Integer)` no mete el entero en una caja—. VB.NET escribe la restricción
con palabras (`Of T As IComparable(Of T)`) donde C# usa `where`, pero genera el mismo IL. F# va por
otro lado: **no declara nada**. La inferencia deduce la restricción `comparison` a partir de haber
usado `>`, y esa es la marca de la familia ML — el tipo genérico es lo que el compilador descubre,
no lo que tú anuncias.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene genéricos: se escribe una función por
tipo, o una macro que copie el cuerpo.

### C++

```cpp
#include <iostream>

template <typename T>
T mayor(const T& a, const T& b) {   // el compilador genera una función por cada T usado
    return a > b ? a : b;
}

int main() {
    long a, b;
    std::cin >> a >> b;
    std::cout << "max=" << mayor(a, b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Objective-C no tiene genéricos de función. Los "lightweight generics"
// (NSArray<NSNumber *> *) solo anotan colecciones y se borran al compilar:
// aquí solo queda `id` más el protocolo de comparación.
static id mayor(id a, id b) {
    return [a compare:b] == NSOrderedDescending ? a : b;
}

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        NSNumber *m = mayor(@(a), @(b));
        printf("max=%ld\n", [m longValue]);
    }
    return 0;
}
```

**Qué reconocer:** aquí está la división más profunda de toda la página. La plantilla de C++ **no es
un genérico borrado: es un generador de código**. `mayor<long>` y `mayor<std::string>` son dos
funciones distintas en el binario, cada una compilada y optimizada por separado —de ahí que las
plantillas no cuesten nada en ejecución y que el binario crezca—. La restricción, además, es
implícita: si `T` no soporta `>`, el error sale al instanciar, no al declarar (los *concepts* de
C++20 arreglan justo eso). Objective-C está en el extremo opuesto: todo pasa por `id`, el puntero a
objeto sin tipo, y la comparación se resuelve por **envío dinámico de mensajes** — si el objeto no
entiende `compare:`, revienta en ejecución.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Genéricos monomorfizados,
con restricción explícita y comprobada antes de instanciar.

### Zig

```zig
const std = @import("std");

// Zig no tiene sintaxis de genéricos: el tipo es un parámetro normal,
// evaluado en tiempo de compilación con `comptime`.
fn mayor(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try std.io.getStdOut().writer().print("max={d}\n", .{mayor(i64, a, b)});
}
```

### Nim

```nim
import std/[strutils, strformat]

proc mayor[T: SomeNumber](a, b: T): T =
  if a > b: a else: b   # `T: SomeNumber` restringe el genérico a tipos numéricos

let v = stdin.readLine().splitWhitespace()
echo &"max={mayor(parseInt(v[0]), parseInt(v[1]))}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

// La restricción es una condición booleana evaluada en compilación.
T mayor(T)(T a, T b) if (__traits(compiles, T.init > T.init)) {
    return a > b ? a : b;
}

void main() {
    auto v = readln().split().map!(to!long).array;
    writefln("max=%d", mayor(v[0], v[1]));
}
```

**Qué reconocer:** los tres **generan código**, como C++ y a diferencia de la JVM: hay una `mayor`
distinta por tipo instanciado. Zig es el más radical porque **no inventa sintaxis**: `comptime T:
type` dice que el tipo es un argumento más, solo que resuelto antes de ejecutar — la misma idea que
permite escribir estructuras de datos genéricas sin un sistema de plantillas aparte. Nim declara la
restricción en el propio parámetro (`T: SomeNumber`), al estilo de los *trait bounds* de Rust. D usa
el mecanismo más flexible y más peligroso: `if (__traits(compiles, ...))`, una condición arbitraria
evaluada en compilación, que acepta cualquier tipo que simplemente *compile* con esa operación —
polimorfismo estructural, no nominal.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). `max()` es polimórfico de fábrica y el tipo lo
pone la columna.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene tipos que parametrizar: el mismo predicado sirve para todo.
% Con `@>` (orden estándar de términos) compararía incluso átomos y estructuras.
mayor(A, B, A) :- A >= B, !.
mayor(_, B, B).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    mayor(A, B, Max),
    format("max=~d~n", [Max]).
```

### Datalog

```datalog
% Datalog no tiene funciones ni E/S: el máximo es una relación con dos reglas,
% una por cada caso, y los "genéricos" no existen porque no hay tipos declarados.
par(3, 7).

maximo(A, B, A) :- par(A, B), A >= B.
maximo(A, B, B) :- par(A, B), B > A.
```

**Qué reconocer:** aquí no hay genéricos porque **no hay tipos que parametrizar**: un término es un
término. Y sin embargo Prolog tiene el polimorfismo más amplio de la página — el orden estándar
`@>` compara *cualquier* par de términos, números, átomos o estructuras, con un criterio total
definido por el lenguaje. Fíjate también en que `mayor/3` necesita el corte (`!`) para no ofrecer la
segunda solución cuando `A >= B`: en Prolog una función genérica es una relación, y hay que decirle
explícitamente que ya terminó. Datalog, sin corte y sin negación, resuelve lo mismo con dos reglas
mutuamente excluyentes.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas a la misma pregunta. Los dinámicos
no tienen tipo que parametrizar; la JVM lo **borra** y compila una única función sobre `Object`; C++,
D, Zig, Nim, Rust y el CLR **generan una versión por tipo**. Reconocer a cuál de los tres grupos
pertenece un lenguaje te dice de antemano qué te va a costar su código genérico: rendimiento, tamaño
del binario o errores en ejecución. Eso es lo transferible.

⏮️ [Volver a la clase 078](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
