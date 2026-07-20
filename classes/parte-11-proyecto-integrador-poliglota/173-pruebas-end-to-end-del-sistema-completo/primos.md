# 🧬 El mismo programa en las familias de lenguajes — Clase 173

> [⬅️ Volver a la clase 173](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —la prueba end-to-end que confirma que el sistema
completo responde lo que se esperaba— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b esperado`
- **Salida** (stdout): `e2e=<pasa|falla>`
- **Regla:** la prueba **pasa** si el sistema, que suma sus dos entradas, produce el valor esperado

| stdin | esperado |
|---|---|
| `3 4 7` | `e2e=pasa` |
| `2 2 5` | `e2e=falla` |
| `10 5 15` | `e2e=pasa` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia donde la prueba end-to-end suele escribirse como un script más: se invoca el sistema, se
compara la salida con la esperada y se informa. Sin ceremonia de framework.

### Ruby

```ruby
a, b, esperado = STDIN.gets.split.map(&:to_i)
puts "e2e=#{a + b == esperado ? 'pasa' : 'falla'}"
```

### Perl

```perl
my ($a, $b, $esperado) = split ' ', <STDIN>;
printf "e2e=%s\n", $a + $b == $esperado ? "pasa" : "falla";
```

### Lua

```lua
local a, b, esperado = io.read("n", "n", "n")
print("e2e=" .. (a + b == esperado and "pasa" or "falla"))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b esperado
set res [expr {$a + $b == $esperado ? "pasa" : "falla"}]
puts "e2e=$res"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("e2e=%s\n", if (v[1] + v[2] == v[3]) "pasa" else "falla"))
```

**Qué reconocer:** los cinco expresan la aserción como una comparación corriente dentro del flujo
normal del programa, no como una construcción especial del lenguaje. Lua usa el modismo
`cond and x or y` porque no tiene operador ternario. Y hay un dato histórico que conviene guardar:
el formato **TAP** (*Test Anything Protocol*), que hoy consumen arneses de pruebas de media docena
de familias, nació en el arnés de pruebas de Perl. Tcl trae `tcltest` en su distribución base y R
integra `stopifnot` en el propio lenguaje: en esta familia la prueba tiende a ser parte del paquete,
no una dependencia añadida.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.split(' ').map(int.parse).toList();
  print('e2e=${v[0] + v[1] == v[2] ? 'pasa' : 'falla'}');
}
```

### ActionScript 3

```actionscript
// ActionScript vive dentro del reproductor Flash: no hay stdin ni codigo de salida
// de proceso, asi que una prueba end-to-end de linea de comandos es inexpresable.
// Lo mas cercano es exponer la asercion como funcion pura y llamarla desde el arnes.
package {
    public class PruebaE2E {
        public static function verificar(a:int, b:int, esperado:int):String {
            return "e2e=" + (a + b == esperado ? "pasa" : "falla");
        }
    }
}
```

**Qué reconocer:** Dart interpola con `${...}` igual que JavaScript y ejecuta pruebas con
`dart test`, un corredor oficial del SDK; TypeScript y JavaScript dependen de un corredor externo
(Jest, Vitest, `node --test`). ActionScript marca el límite duro de esta familia: **un lenguaje
atado a un anfitrión gráfico no puede tener una prueba end-to-end de proceso**, porque no hay
proceso que devuelva un código de salida. La aserción existe; la frontera del sistema, no.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Los cuatro comparten el mismo ecosistema de
pruebas —JUnit— y el mismo formato de informe, aunque escriban la aserción de forma muy distinta.

### Kotlin

```kotlin
fun main() {
    val (a, b, esperado) = readLine()!!.split(" ").map { it.toInt() }
    println("e2e=" + if (a + b == esperado) "pasa" else "falla")
}
```

### Scala

```scala
object PruebaE2E extends App {
  val Array(a, b, esperado) = scala.io.StdIn.readLine().split(" ").map(_.toInt)
  val res = if (a + b == esperado) "pasa" else "falla"
  println(s"e2e=$res")
}
```

### Groovy

```groovy
def (a, b, esperado) = System.in.newReader().readLine().split(' ')*.toInteger()
println "e2e=${a + b == esperado ? 'pasa' : 'falla'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b esperado] (map parse-long (str/split (read-line) #"\s+"))]
  (println (str "e2e=" (if (= (+ a b) esperado) "pasa" "falla"))))
```

**Qué reconocer:** en Kotlin y Scala el `if` **devuelve un valor** y se puede asignar; en Java hay
que usar el ternario o una variable mutable. Esa diferencia sintáctica tiene consecuencia práctica
en pruebas: la aserción se compone en una expresión en vez de en un bloque. Los cuatro corren sobre
JUnit para el arnés real —Groovy añade Spock, con su gramática *given/when/then*, y Clojure trae
`clojure.test` en la biblioteca estándar—, así que un informe de pruebas de un proyecto Scala y uno
de un proyecto Java son el mismo XML.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Un único corredor, `dotnet test`, para todos los
lenguajes del CLR.

### F\#

```fsharp
let [| a; b; esperado |] = stdin.ReadLine().Split(' ') |> Array.map int
printfn "e2e=%s" (if a + b = esperado then "pasa" else "falla")
```

### VB.NET

```vbnet
Module PruebaE2E
    Sub Main()
        Dim v = Console.ReadLine().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Dim esperado = Integer.Parse(v(2))
        Console.WriteLine("e2e=" & If(a + b = esperado, "pasa", "falla"))
    End Sub
End Module
```

**Qué reconocer:** F# usa `=` para comparar, no `==`, porque reserva `<-` para la asignación: es la
convención de la rama ML, y confunde a quien llega de C#. VB.NET necesita la forma de tres
argumentos de `If(...)` para obtener un ternario, porque `If` normalmente es una sentencia. Lo que
no cambia es el arnés: xUnit y NUnit se consumen igual desde los tres lenguajes, y un ensamblado de
pruebas escrito en F# lo ejecuta el mismo `dotnet test` que uno de C#.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el protocolo de pruebas end-to-end es, casi
siempre, el código de salida del proceso más lo que se imprimió por stdout.

### C++

```cpp
#include <iostream>

int main() {
    long a, b, esperado;
    std::cin >> a >> b >> esperado;
    std::cout << "e2e=" << (a + b == esperado ? "pasa" : "falla") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a, b, esperado;
        if (scanf("%ld %ld %ld", &a, &b, &esperado) != 3) return 1;
        NSString *res = (a + b == esperado) ? @"pasa" : @"falla";
        printf("e2e=%s\n", [res UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ninguno de los dos —ni C— trae corredor de pruebas en el lenguaje ni en la
biblioteca estándar. Todo lo que existe es `assert.h`, que **aborta el proceso** en vez de informar,
y por eso la familia acumula frameworks de terceros (Google Test, Catch2, Unity, XCTest). Objective-C
es la excepción parcial: XCTest viene con las herramientas de Apple y es el estándar de facto de su
plataforma, pero sigue siendo del entorno, no del lenguaje. Fíjate en que el `scanf` de la clase
compila tal cual en ambos: son superconjuntos de C.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia que decidió
que las pruebas no debían ser una dependencia externa.

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
    const res = if (a + b == esperado) "pasa" else "falla";
    try std.io.getStdOut().writer().print("e2e={s}\n", .{res});
}

test "el sistema suma sus entradas" {
    try std.testing.expectEqual(@as(i64, 7), 3 + 4);
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
echo "e2e=", (if v[0] + v[1] == v[2]: "pasa" else: "falla")
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!long).array;
    writeln("e2e=", v[0] + v[1] == v[2] ? "pasa" : "falla");
}

unittest {
    assert(3 + 4 == 7);
}
```

**Qué reconocer:** aquí está la diferencia más fuerte de toda la página. **Zig y D tienen las
pruebas en la gramática**: `test "..."` y `unittest { ... }` son palabras del lenguaje, viven junto
al código que prueban y solo se compilan cuando se pide (`zig test`, `dmd -unittest`). Es la misma
decisión que Rust con `#[test]` y Go con `_test.go`: el representante que estudiaste ya te enseñó el
patrón. Nim lo resuelve un escalón más abajo, con `std/unittest` en la biblioteca estándar. En
ninguno de los tres hace falta añadir una dependencia para tener un arnés.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** debe ser cierto, no cómo
comprobarlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B, Esperado]),
    (   A + B =:= Esperado
    ->  Res = "pasa"
    ;   Res = "falla"
    ),
    format("e2e=~w~n", [Res]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni orden de ejecucion: no puede leer stdin ni "correr" una
% prueba. Los casos se declaran como hechos y la regla deriva solo los que pasan;
% que un caso falle se observa por su AUSENCIA en la relacion, no por un mensaje.
caso("3 4 7", 3, 4, 7).
caso("2 2 5", 2, 2, 5).
caso("10 5 15", 10, 5, 15).

pasa(Id) :- caso(Id, A, B, Esperado), Esperado = A + B.
```

**Qué reconocer:** en Prolog `=:=` compara evaluando aritmética, mientras `=` unifica y `is` liga:
tres operadores donde los lenguajes imperativos tienen uno, y confundirlos es el error clásico del
recién llegado. Datalog muestra el modelo de pruebas más ajeno de todos: bajo **mundo cerrado**, lo
que no se deriva simplemente no es cierto, así que "la prueba falla" equivale a "la tupla no
aparece". Es exactamente la lógica de un `SELECT` que devuelve cero filas —el mismo gesto que usaste
en la versión SQL de la clase para comprobar el sistema—.

---

## Y de vuelta a la clase

Veinte lenguajes, una sola prueba: alimentar al sistema, comparar con lo esperado, informar. Lo que
cambia no es la aserción —es idéntica en todos— sino **dónde vive el arnés**: en la gramática (Zig,
D, Rust, Go), en la biblioteca estándar (Clojure, Nim, Tcl), en un framework de terceros (C, C++) o
directamente en ningún sitio (ActionScript, Datalog). Elegir lenguaje es también elegir cuánta
infraestructura de pruebas te viene regalada.

⏮️ [Volver a la clase 173](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
