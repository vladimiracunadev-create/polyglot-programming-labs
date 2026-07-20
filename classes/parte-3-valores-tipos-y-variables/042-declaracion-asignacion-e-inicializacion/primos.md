# 🧬 El mismo programa en las familias de lenguajes — Clase 042

> [⬅️ Volver a la clase 042](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —intercambiar dos variables— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros)
- **Salida** (stdout): `a=<nuevo a> b=<nuevo b>` tras intercambiar
- **Regla:** el valor que estaba en `a` pasa a `b` y viceversa

| stdin | esperado |
|---|---|
| `3 7` | `a=7 b=3` |
| `0 5` | `a=5 b=0` |
| `-2 9` | `a=9 b=-2` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La variable se declara al asignarla por primera vez, sin tipo y sin ceremonia. La pregunta de la
clase —¿hace falta una variable temporal?— se responde distinto en cada primo.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
a, b = b, a
puts "a=#{a} b=#{b}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
($a, $b) = ($b, $a);
print "a=$a b=$b\n";
```

### Lua

```lua
local a, b = io.read("n", "n")
a, b = b, a
print(string.format("a=%d b=%d", a, b))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
lassign [list $b $a] a b
puts "a=$a b=$b"
```

### R

```r
v <- scan("stdin", what = integer(), n = 2, quiet = TRUE)
v <- rev(v)
cat(sprintf("a=%d b=%d\n", v[1], v[2]))
```

**Qué reconocer:** los cinco declaran e inicializan en el mismo gesto —no hay una línea que diga
"esto es un entero"— y cuatro de ellos ofrecen **asignación múltiple**, que hace innecesaria la
variable temporal: el lado derecho se evalúa entero antes de asignar nada. Lua exige `local` para no
crear una global por accidente, un recordatorio de que "declarar" sí existe cuando importa el
ámbito. R vuelve a delatar su origen estadístico: no intercambia dos variables, **invierte un
vector**.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(' ').map(int.parse).toList();
  var a = v[0];
  var b = v[1];
  final tmp = a;
  a = b;
  b = tmp;
  print('a=$a b=$b');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el intercambio.
    public class Intercambio {
        public static function intercambiar(a:int, b:int):String {
            var tmp:int = a;
            a = b;
            b = tmp;
            return "a=" + a + " b=" + b;
        }
    }
}
```

**Qué reconocer:** ambos distinguen la variable que se reasigna (`var`) de la que se inicializa una
sola vez (`final`, `const`), la misma pareja `let`/`const` de JavaScript. Y ambos **carecen de
desestructuración con intercambio en una línea** al estilo de Python: aquí sí aparece la variable
temporal, que es lo que hacen por dentro los lenguajes que la esconden. ActionScript declara el tipo
después del nombre (`a:int`), exactamente la notación que TypeScript heredaría más tarde.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode; lo que
cambia es si el lenguaje te deja reasignar una variable o te empuja a no hacerlo.

### Kotlin

```kotlin
fun main() {
    var (a, b) = readLine()!!.trim().split(" ").map { it.toInt() }
    a = b.also { b = a }
    println("a=$a b=$b")
}
```

### Scala

```scala
object Intercambio extends App {
  // Los `val` son inmutables: el "intercambio" es nombrar al revés, no reasignar.
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"a=$b b=$a")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
(a, b) = [b, a]
println "a=$a b=$b"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; No hay variables reasignables: `let` liga nombres nuevos, no cambia los viejos.
(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "a=" b " b=" a)))
```

**Qué reconocer:** Kotlin marca la diferencia entre `val` (inicializar una vez) y `var` (poder
reasignar) en la propia palabra clave, y su `a = b.also { b = a }` es el truco idiomático para
intercambiar sin temporal. Scala y Clojure muestran el otro extremo dentro de la misma máquina
virtual: si nada se reasigna, **el intercambio deja de ser una operación** y se convierte en un
cambio de nombres. Groovy conserva la asignación múltiple con corchetes, hermana de la de Python.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// En F# los enlaces son inmutables por defecto: intercambiar es reordenar al imprimir.
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "a=%d b=%d" b a
```

### VB.NET

```vbnet
Module Intercambio
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))

        Dim tmp = a
        a = b
        b = tmp

        Console.WriteLine($"a={a} b={b}")
    End Sub
End Module
```

**Qué reconocer:** `Dim a = ...` de VB.NET es exactamente el `var a = ...` de C#: declara e infiere
el tipo en la misma línea, sin escribirlo. F# invierte el valor por defecto —un `let` no se
reasigna salvo que pidas `let mutable`—, así que el problema desaparece en lugar de resolverse. Es
la misma lección que Scala y Clojure enseñan en la JVM: la inmutabilidad no es una limitación, es
una garantía.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Tipos declarados, memoria explícita y una variable
temporal cuando hace falta.

### C++

```cpp
#include <iostream>
#include <utility>

int main() {
    long a, b;
    std::cin >> a >> b;
    std::swap(a, b);
    std::cout << "a=" << a << " b=" << b << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;

        long tmp = a;
        a = b;
        b = tmp;

        printf("a=%ld b=%ld\n", a, b);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C** y la declaración `long a, b;` sin valor
inicial es idéntica a la de la clase: la variable existe pero su contenido es basura hasta que
alguien la asigna. Esa separación entre *declarar* e *inicializar* es lo que distingue a esta
familia de las anteriores. C++ esconde el temporal dentro de `std::swap`, pero el temporal sigue
ahí; Objective-C ni siquiera lo intenta y lo escribe a mano.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con una postura muy firme sobre qué variable puede cambiar.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    var a = try std.fmt.parseInt(i64, it.next().?, 10);
    var b = try std.fmt.parseInt(i64, it.next().?, 10);
    std.mem.swap(i64, &a, &b);
    try std.io.getStdOut().writer().print("a={d} b={d}\n", .{ a, b });
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
var (a, b) = (v[0], v[1])
swap(a, b)
echo "a=", a, " b=", b
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!long).array;
    long a = v[0], b = v[1];
    swap(a, b);
    writefln("a=%d b=%d", a, b);
}
```

**Qué reconocer:** los tres separan explícitamente el enlace inmutable del mutable —`const`/`var` en
Zig, `let`/`var` en Nim, `immutable`/normal en D— igual que Rust exige `mut` para poder reasignar. Y
los tres ofrecen `swap` recibiendo **direcciones** de las variables (`&a`, `&b` en Zig), no copias:
la operación modifica el original, que es justo lo que la clase llama asignación. Zig obliga además
a inicializar el búfer con `undefined` de forma explícita, para que "no inicializado" nunca sea un
descuido.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no cómo llegar
paso a paso.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene asignación: una variable se unifica una sola vez y nunca cambia.
main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    format("a=~d b=~d~n", [B, A]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni variables mutables: se declara el hecho y la regla que lo invierte.
par(3, 7).

intercambiado(B, A) :- par(A, B).
```

**Qué reconocer:** aquí el problema de la clase **no existe**. En Prolog `A` y `B` no son cajas con
un valor dentro sino nombres ligados a un término: una vez unificados no admiten reasignación, así
que "intercambiar" solo puede significar mencionarlos en otro orden. Datalog lleva la idea al
extremo —hechos y reglas, sin efectos ni entrada/salida— y expresa el intercambio como lo que
realmente es en este paradigma: **una relación nueva** derivada de la original, no una modificación
de la vieja. Es la misma renuncia que hace SQL cuando produce un resultado en vez de mutar filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los divide en dos mitades: ¿puede una
variable cambiar de valor? Donde la respuesta es sí, aparece el temporal o el `swap`. Donde es no,
el intercambio se disuelve en un cambio de nombres. Eso es lo transferible.

⏮️ [Volver a la clase 042](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
