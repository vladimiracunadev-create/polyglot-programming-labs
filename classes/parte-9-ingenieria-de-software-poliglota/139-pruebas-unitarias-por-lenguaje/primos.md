# 🧬 El mismo programa en las familias de lenguajes — Clase 139

> [⬅️ Volver a la clase 139](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una prueba unitaria que comprueba si `a + b` da el
valor esperado— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b esperado`, tres enteros
- **Salida** (stdout): `test=pasa` o `test=falla`
- **Regla:** pasa si `a + b == esperado`

| stdin | esperado |
|---|---|
| `3 4 7` | `test=pasa` |
| `2 2 5` | `test=falla` |
| `10 5 15` | `test=pasa` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí la prueba unitaria es un guion más: se lee, se compara y se informa. Lo que separa a la familia
no es la sintaxis de la aserción, sino **quién trae el marco de pruebas**: unos lo llevan en la
biblioteca estándar y otros lo instalan.

### Ruby

```ruby
a, b, esperado = STDIN.gets.split.map(&:to_i)
puts "test=#{a + b == esperado ? 'pasa' : 'falla'}"
```

### Perl

```perl
my ($x, $y, $esperado) = split ' ', <STDIN>;
print "test=", ($x + $y == $esperado ? "pasa" : "falla"), "\n";
```

### Lua

```lua
local a, b, esperado = io.read("n", "n", "n")
print("test=" .. (a + b == esperado and "pasa" or "falla"))
```

### Tcl

```tcl
lassign [split [gets stdin]] a b esperado
set r [expr {$a + $b == $esperado ? "pasa" : "falla"}]
puts "test=$r"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("test=%s\n", if (v[1] + v[2] == v[3]) "pasa" else "falla"))
```

**Qué reconocer:** los cinco expresan la comprobación como una condición corriente, pero su
ecosistema de pruebas difiere mucho. Ruby es el único que trae **Minitest en la biblioteca
estándar**, con **RSpec** como alternativa externa de estilo declarativo. Perl aporta la pieza más
influyente de todas: **`Test::More`** y el protocolo **TAP** (*Test Anything Protocol*), que nació en
Perl y hoy lo hablan corredores de pruebas de muchos otros lenguajes. Lua no lleva nada dentro y la
comunidad usa **busted**; R usa **testthat**; Tcl trae **tcltest** con la distribución. La aserción
se parece; el andamiaje que la rodea es lo que cambia.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('test=${v[0] + v[1] == v[2] ? "pasa" : "falla"}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la aserción.
package {
    public class PruebaSuma {
        public static function test(a:int, b:int, esperado:int):String {
            return "test=" + (a + b == esperado ? "pasa" : "falla");
        }
    }
}
```

**Qué reconocer:** Dart ordena su ecosistema desde arriba: `package:test` es el paquete oficial y
`dart test` el corredor único, sin la fragmentación de marcos que caracteriza a JavaScript. Los
tipos de la firma `(a:int, b:int, esperado:int)` de ActionScript son el mismo gesto que TypeScript
hace sobre JavaScript, y en los dos casos la comprobación queda **fuera** del lenguaje: ActionScript
no tiene entrada estándar, así que su prueba solo puede vivir como función pura invocada por otro
código.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Comparten bytecode, biblioteca estándar y, casi
siempre, el mismo corredor de pruebas.

### Kotlin

```kotlin
fun main() {
    val (a, b, esperado) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("test=" + if (a + b == esperado) "pasa" else "falla")
}
```

### Scala

```scala
object PruebaSuma {
  def main(args: Array[String]): Unit = {
    val Array(a, b, esperado) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    val r = if (a + b == esperado) "pasa" else "falla"
    println(s"test=$r")
  }
}
```

### Groovy

```groovy
def (a, b, esperado) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "test=${a + b == esperado ? 'pasa' : 'falla'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b esperado] (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "test=" (if (= (+ a b) esperado) "pasa" "falla"))))
```

**Qué reconocer:** la JVM es el caso más claro de que **el marco de pruebas es un lenguaje aparte**.
**JUnit** sirve tanto a Java como a Kotlin sin ninguna adaptación, porque Kotlin compila a las mismas
clases. Scala prefiere **ScalaTest** o **MUnit**, que aprovechan su sintaxis para escribir la
expectativa casi en inglés. Groovy tiene **Spock**, cuyos bloques `given/when/then` solo son posibles
porque Groovy permite reescribir la sintaxis en tiempo de compilación. Clojure lleva **`clojure.test`
en su propia biblioteca estándar**, con `deftest` y `is`, coherente con su idea de que la prueba es
un dato más del programa. Cuatro estilos de aserción, una sola máquina virtual debajo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| a; b; esperado |] =
    stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "test=%s" (if a + b = esperado then "pasa" else "falla")
```

### VB.NET

```vbnet
Module PruebaSuma
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Dim esperado = Integer.Parse(v(2))
        Console.WriteLine("test=" & If(a + b = esperado, "pasa", "falla"))
    End Sub
End Module
```

**Qué reconocer:** en .NET el marco de pruebas es de la **plataforma**, no del lenguaje: **NUnit** y
**xUnit** sirven igual a C#, F# y VB.NET porque todos producen ensamblados del CLR y el corredor solo
ve atributos sobre métodos. F# añade algo que los otros dos no tienen a mano: **FsCheck**, pruebas
**basadas en propiedades**, donde en vez de fijar `3 + 4 = 7` se declara la ley `a + b = b + a` y la
herramienta genera cientos de casos buscando el contraejemplo. Fíjate también en el `=` de F#: es
comparación, no asignación, exactamente al revés que en VB.NET, donde `=` hace las dos cosas según el
contexto.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Tipos declarados, `printf` y ninguna red de
seguridad puesta por el lenguaje.

### C++

```cpp
#include <iostream>

int main() {
    int a, b, esperado;
    std::cin >> a >> b >> esperado;
    std::cout << "test=" << (a + b == esperado ? "pasa" : "falla") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int a, b, esperado;
        scanf("%d %d %d", &a, &b, &esperado);
        NSString *r = (a + b == esperado) ? @"pasa" : @"falla";
        printf("test=%s\n", [r UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C** y el código de la clase compila casi tal cual
en ambos. La diferencia de fondo está en las pruebas: la biblioteca estándar de C++ **no incluye
ninguna**, así que la comunidad se reparte entre **Catch2** —una sola cabecera, aserciones con
`REQUIRE`— y **GoogleTest**, con su jerarquía de *fixtures*. Objective-C es la excepción del grupo:
**XCTest** viene con las herramientas de Apple y está integrado en Xcode, así que ahí la prueba sí
llega en la caja, pero de la mano de la plataforma y no del lenguaje.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con las pruebas metidas dentro del propio lenguaje.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    const esperado = try std.fmt.parseInt(i64, it.next().?, 10);
    const r = if (a + b == esperado) "pasa" else "falla";
    try std.io.getStdOut().writer().print("test={s}\n", .{r});
}

// `test` es una palabra clave del lenguaje: `zig test` ejecuta este bloque.
test "la suma cuadra" {
    try std.testing.expectEqual(@as(i64, 7), 3 + 4);
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
echo "test=", (if v[0] + v[1] == v[2]: "pasa" else: "falla")
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!int).array;
    writeln("test=", v[0] + v[1] == v[2] ? "pasa" : "falla");
}

// `unittest` es sintaxis del lenguaje: se compila solo con -unittest.
unittest {
    assert(3 + 4 == 7);
}
```

**Qué reconocer:** esta es la diferencia de fondo de la familia y no un detalle de comodidad: **Zig,
Nim y D traen las pruebas integradas en el lenguaje**. En Zig `test` es una palabra clave y
`zig test` compila y ejecuta esos bloques; en D `unittest` es un bloque sintáctico que el compilador
incluye solo con `-unittest`; en Nim `unittest` llega en la biblioteca estándar con `suite`, `test` y
`check`, y además `doAssert` funciona sin importar nada. La consecuencia práctica es que la prueba
**vive junto a la función que prueba**, en el mismo archivo, igual que hace Rust con `#[test]` y en
la misma línea de lo que Go consigue con `go test`. Ninguno de los tres necesita elegir marco antes
de escribir la primera aserción.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** debe cumplirse, no cómo
comprobarlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B, Esperado]),
    (   A + B =:= Esperado
    ->  R = "pasa"
    ;   R = "falla"
    ),
    format("test=~w~n", [R]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: el caso de prueba entra como hecho y la
% comprobación es una regla que solo se deriva si los valores concuerdan.
caso(3, 4, 7).
suma(3, 4, 7).

pasa(A, B, E) :- caso(A, B, E), suma(A, B, E).
falla(A, B, E) :- caso(A, B, E), not suma(A, B, E).
```

**Qué reconocer:** en Prolog la prueba es literalmente una **consulta**: preguntar si `A + B =:= E`
tiene éxito es lo mismo que ejecutar una aserción, y por eso SWI-Prolog incluye **plunit** en la
distribución, donde un caso de prueba se escribe como una cláusula más. Datalog lleva la idea al
extremo: sin efectos ni entrada/salida, no puede *ejecutar* una prueba, solo **derivarla** —si la
tupla aparece en la relación `pasa`, el caso pasó—. Es la misma renuncia que hace SQL, y también la
razón por la que en esas dos familias no existe un "marco de pruebas": la consulta ya era la prueba.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma comprobación de tres tokens en todos. Lo que de
verdad los separa no es cómo se escribe la aserción, sino **de dónde viene el marco**: integrado en
el lenguaje (Zig, D, Nim, Rust, Go), en la biblioteca estándar (Ruby, Clojure, Perl), en la
plataforma (JUnit, NUnit, XCTest) o completamente fuera (C++, Lua). Eso es lo transferible.

⏮️ [Volver a la clase 139](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
