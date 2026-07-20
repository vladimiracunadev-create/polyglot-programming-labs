# 🧬 El mismo programa en las familias de lenguajes — Clase 150

> [⬅️ Volver a la clase 150](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —comprobar que `n*2` y `n+n` siguen dando lo
mismo— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por
los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `equivalente=<true|false> resultado=<2n>`
- **Regla:** `viejo = n * 2`, `nuevo = n + n`; equivalente si coinciden

| stdin | esperado |
|---|---|
| `5` | `equivalente=true resultado=10` |
| `0` | `equivalente=true resultado=0` |
| `7` | `equivalente=true resultado=14` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Sin tipos declarados, ninguna herramienta puede demostrar que un cambio es seguro: la red que sostiene
la refactorización son las pruebas.

### Ruby

```ruby
n = STDIN.gets.to_i
viejo = n * 2
nuevo = n + n
puts "equivalente=#{viejo == nuevo} resultado=#{nuevo}"
```

### Perl

```perl
use strict;
use warnings;

my $n = <STDIN> + 0;
my $viejo = $n * 2;
my $nuevo = $n + $n;
printf "equivalente=%s resultado=%d\n", ($viejo == $nuevo ? 'true' : 'false'), $nuevo;
```

### Lua

```lua
local n = math.tointeger(io.read("n"))
local viejo, nuevo = n * 2, n + n
print(string.format("equivalente=%s resultado=%d", tostring(viejo == nuevo), nuevo))
```

### Tcl

```tcl
gets stdin linea
set n [expr {int([string trim $linea])}]
set viejo [expr {$n * 2}]
set nuevo [expr {$n + $n}]
puts "equivalente=[expr {$viejo == $nuevo ? {true} : {false}}] resultado=$nuevo"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
viejo <- n * 2
nuevo <- n + n
cat(sprintf("equivalente=%s resultado=%d\n", tolower(viejo == nuevo), nuevo))
```

**Qué reconocer:** fíjate primero en el detalle pequeño: solo Ruby imprime `true` tal cual; Perl no
tiene tipo booleano (cierto es `1`, falso es la cadena vacía), Tcl usa `0`/`1`, R escribe `TRUE` en
mayúsculas y hay que bajarlo. Ese desajuste ya es un aviso de lo que viene. Lo grande es esto: en los
cinco, **renombrar `nuevo` es buscar y reemplazar**, con todo el riesgo que eso implica —el editor no
sabe si `nuevo` en otro archivo es la misma variable, un método de otra clase o una cadena—. No hay
renombrado seguro porque no hay información de tipos que permita resolver a qué se refiere cada
nombre. Por eso estas comunidades son las que más insisten en la cobertura de pruebas: en un lenguaje
dinámico **la suite de pruebas ocupa el lugar que en otros ocupa el compilador**, y refactorizar sin
ella no es refactorizar, es reescribir a ciegas.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final viejo = n * 2;
  final nuevo = n + n;
  print('equivalente=${viejo == nuevo} resultado=$nuevo');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin: se ilustra la comparación de las dos versiones.
package refactor {
    public class Doble {
        public static function comprobar(n:int):String {
            var viejo:int = n * 2;
            var nuevo:int = n + n;
            return "equivalente=" + (viejo == nuevo) + " resultado=" + nuevo;
        }
    }
}
```

**Qué reconocer:** esta familia contiene el experimento natural más claro del asunto. JavaScript y
TypeScript son el **mismo lenguaje** con y sin tipos, y la diferencia en refactorización es enorme:
sobre `.ts` el editor renombra un símbolo en todo el proyecto con garantías, y sobre `.js` el mismo
editor solo puede ofrecer una heurística que falla en cuanto hay acceso dinámico por cadena
(`obj["nuevo"]`). Dart y ActionScript anotan tipos —`int`, `Number`— y por eso el renombrado vuelve a
ser una transformación verificable. Es el argumento de ingeniería que empuja a los proyectos grandes
hacia el tipado estático: no es la elegancia, es poder cambiar el código sin miedo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Es la familia donde nació la refactorización
automática: el IDE conoce el árbol de tipos completo y puede reescribirlo.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val viejo = n * 2
    val nuevo = n + n
    println("equivalente=${viejo == nuevo} resultado=$nuevo")
}
```

### Scala

```scala
object Refactor extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val viejo = n * 2
  val nuevo = n + n
  println(s"equivalente=${viejo == nuevo} resultado=$nuevo")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def viejo = n * 2
def nuevo = n + n
println "equivalente=${viejo == nuevo} resultado=$nuevo"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (parse-long (str/trim (read-line)))
      viejo (* n 2)
      nuevo (+ n n)]
  (println (str "equivalente=" (= viejo nuevo) " resultado=" nuevo)))
```

**Qué reconocer:** los cuatro imprimen `true` sin adaptación porque comparten el `Boolean.toString`
de Java. La diferencia real está en las garantías de cambio: **Kotlin y Scala tienen renombrado
seguro** —el compilador resuelve cada referencia, así que el IDE puede extraer un método o cambiar
una firma y avisar de cada uso roto—, mientras que Groovy, aun corriendo sobre la misma JVM, resuelve
métodos en tiempo de ejecución y cae en la misma trampa que Ruby: el editor adivina. Clojure ocupa un
lugar propio: es dinámico, pero al ser inmutable y sin efectos ocultos, la refactorización más común
—extraer una función— es trivialmente segura, porque una expresión pura se puede mover sin cambiar el
significado del programa. Dos ejes distintos, entonces: **tipos** para renombrar, **pureza** para
mover.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let viejo = n * 2
let nuevo = n + n
printfn "equivalente=%b resultado=%d" (viejo = nuevo) nuevo
```

### VB.NET

```vbnet
Imports System

Module Refactor
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim viejo = n * 2
        Dim nuevo = n + n
        Console.WriteLine("equivalente=" & (viejo = nuevo).ToString().ToLowerInvariant() & " resultado=" & nuevo)
    End Sub
End Module
```

**Qué reconocer:** VB.NET obliga a bajar `True` a minúsculas, un recordatorio de que el formato de un
booleano es una convención de cada lenguaje y no una verdad universal. En cuanto a refactorización,
los tres son estáticos y el compilador de Roslyn expone el árbol semántico a las herramientas: de ahí
que **C# y VB.NET tengan renombrado seguro, extracción de método y cambio de firma** aplicables a
toda la solución, y que los analizadores puedan proponer y aplicar arreglos automáticos. F# añade una
garantía extra que conviene ver: con **tipos algebraicos y coincidencia de patrones**, añadir un caso
nuevo hace que el compilador señale cada punto del código que dejó de ser exhaustivo. Eso convierte
un cambio de modelo en una lista de tareas verificada por la máquina, que es lo más cerca que llega
un lenguaje a garantizar una refactorización completa.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Estáticos, pero con un preprocesador que las
herramientas no pueden atravesar del todo.

### C++

```cpp
#include <iostream>

int main() {
    long long n;
    std::cin >> n;
    const long long viejo = n * 2;
    const long long nuevo = n + n;
    std::cout << "equivalente=" << std::boolalpha << (viejo == nuevo)
              << " resultado=" << nuevo << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n = 0;
        scanf("%ld", &n);
        long viejo = n * 2;
        long nuevo = n + n;
        printf("equivalente=%s resultado=%ld\n", viejo == nuevo ? "true" : "false", nuevo);
    }
    return 0;
}
```

**Qué reconocer:** `std::boolalpha` de C++ es exactamente el interruptor que convierte `1` en `true`;
Objective-C conserva el `printf` de C y con él la necesidad de escribir el ternario a mano. En
refactorización, la familia es un caso intermedio incómodo: hay tipos, así que en principio el
renombrado es analizable, pero el **preprocesador** rompe la garantía —una macro puede generar el
identificador que estás renombrando, y la compilación condicional esconde ramas enteras del código
que la herramienta nunca ve porque no están activas en tu configuración—. Por eso las herramientas
serias de esta familia (clang-tidy, clangd) trabajan sobre la base de datos de compilación real:
necesitan saber con qué banderas se compiló cada archivo antes de atreverse a tocar un nombre.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Estáticos y sin
preprocesador textual, que es justo lo que devuelve la refactorización automática a la familia C.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\n"), 10);
    const viejo = n * 2;
    const nuevo = n + n;
    try std.io.getStdOut().writer().print("equivalente={} resultado={d}\n", .{ viejo == nuevo, nuevo });
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
let viejo = n * 2
let nuevo = n + n
echo "equivalente=" & $(viejo == nuevo) & " resultado=" & $nuevo
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    const viejo = n * 2;
    const nuevo = n + n;
    writefln("equivalente=%s resultado=%s", viejo == nuevo, nuevo);
}
```

**Qué reconocer:** los tres marcan las ligaduras como inmutables por defecto o casi —`const`, `let`,
`const`—, igual que `let` en Rust y a diferencia de C. Eso importa más de lo que parece al
refactorizar: si una variable no se reasigna, moverla, renombrarla o extraer la expresión que la
calcula no puede cambiar el comportamiento, porque no hay estado que dependa del orden. Es la misma
propiedad que hace segura la extracción de funciones en Clojure, aquí conseguida sin renunciar al
control de bajo nivel. Zig añade un detalle que encaja con esta clase: al no tener macros ni
sobrecarga de operadores, **el código dice lo que hace**, y una herramienta que analiza el fuente ve
lo mismo que el compilador — que es la condición previa para que cualquier refactorización automática
sea de fiar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La equivalencia entre dos formas de escribir lo
mismo no se prueba ejecutando: se razona sobre la declaración.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    Viejo is N * 2,
    Nuevo is N + N,
    (   Viejo =:= Nuevo
    ->  Eq = true
    ;   Eq = false
    ),
    format("equivalente=~w resultado=~w~n", [Eq, Nuevo]).
```

### Datalog

```datalog
% Datalog no tiene E/S: las dos versiones se declaran como reglas y la equivalencia
% se comprueba por ausencia de contraejemplo (la relación queda vacía).
num(5).

viejo(N, D) :- num(N), D = N * 2.
nuevo(N, D) :- num(N), D = N + N.

contraejemplo(N) :- viejo(N, A), nuevo(N, B), A != B.
```

**Qué reconocer:** en Prolog `Viejo is N * 2` no es una asignación sino una ligadura única, así que la
refactorización clásica de "cambiar el valor de una variable" ni siquiera existe: solo puedes
reescribir la regla. Y ahí está la idea que esta familia aporta al tema de la clase — el bloque de
Datalog **es la definición formal de refactorización segura**: dos implementaciones son equivalentes
si no existe ninguna entrada para la que difieran, y `contraejemplo` es exactamente la consulta que
lo pregunta. Un motor Datalog puede evaluarla sobre todos los hechos declarados; una suite de pruebas
solo la comprueba en los casos que alguien escribió. Esa es la distancia real entre *probar* y
*demostrar*, y es la razón de que el optimizador de una base de datos pueda reescribir tu consulta
sin pedirte permiso.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: calcular de dos formas y comparar.
Lo que cambia es **quién te garantiza que el cambio fue seguro**: el compilador y el IDE en los
estáticos, la suite de pruebas en los dinámicos, y un razonamiento formal en los declarativos. Eso es
lo transferible.

⏮️ [Volver a la clase 150](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
