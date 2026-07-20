# 🧬 El mismo programa en las familias de lenguajes — Clase 176

> [⬅️ Volver a la clase 176](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta es la última página del programa, y por una vez no viene a enseñarte nada nuevo. Viene a
**cobrar la apuesta**.

Durante 176 clases sostuvimos una tesis: que no hacía falta estudiar cuarenta lenguajes, que bastaba
con aprender bien un **representante** de cada familia para reconocer a todos sus **primos**. Aquí
abajo hay veinte programas en veinte lenguajes que este curso nunca te enseñó. Ni uno solo tuvo su
clase. Recorre la página sin prisa y comprueba una cosa: **los entiendes todos**.

No los entiendes porque sean fáciles. Los entiendes porque en cada uno reconoces a alguien —el
`STDIN.gets` que es el `input()` de Python, el `readLine()!!` que es el `readLine()` de Java con la
promesa de que no viene vacío, el `!void` de Zig que es el `Result` de Rust con otro nombre—. Eso
que estás a punto de hacer al leerlos es exactamente la habilidad para la que servía el programa.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, las lecciones que te llevas
- **Salida** (stdout): `lecciones=<n> transferible=si`
- **Regla:** informar las lecciones y confirmar que el conocimiento es transferible

| stdin | esperado |
|---|---|
| `5` | `lecciones=5 transferible=si` |
| `12` | `lecciones=12 transferible=si` |
| `1` | `lecciones=1 transferible=si` |

Es el programa más simple de las 176 clases, a propósito. Cuando el problema no distrae, lo único
que queda a la vista es **la forma de cada familia** — y esa forma ya la conoces.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).

### Ruby

```ruby
n = STDIN.gets.strip
puts "lecciones=#{n} transferible=si"
```

### Perl

```perl
chomp(my $n = <STDIN>);
print "lecciones=$n transferible=si\n";
```

### Lua

```lua
local n = io.read("l")
print("lecciones=" .. n .. " transferible=si")
```

### Tcl

```tcl
gets stdin n
puts "lecciones=[string trim $n] transferible=si"
```

### R

```r
n <- readLines("stdin", n = 1)
cat(sprintf("lecciones=%s transferible=si\n", n))
```

**Qué reconocer:** ninguna declaración de tipo, ninguna función `main`, ninguna ceremonia: el
programa es el archivo. Si sabes leer las tres líneas de Python de esta clase, acabas de leer cinco
lenguajes más sin ayuda. Lo que te queda por aprender de cada uno cabe en una tarde: la **sintaxis de
interpolación** (`#{}` en Ruby, `$var` dentro de comillas en Perl y Tcl, `..` de concatenación en
Lua, `sprintf` en R) y poco más. Fíjate en que Tcl te obliga a `string trim` porque para él todo es
cadena, y en que R devuelve un **vector** donde los demás devuelven un valor: son las dos únicas
sorpresas de todo el apartado, y las dos las anticipaste porque conoces la familia.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = stdin.readLineSync()!.trim();
  print('lecciones=$n transferible=si');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash y no tiene stdin: se ilustra la
// composicion de la linea. Es el unico lenguaje de esta pagina que ya no puede
// ejecutarse en un navegador actual.
package {
    public class Cierre {
        public static function informe(n:int):String {
            return "lecciones=" + n + " transferible=si";
        }
    }
}
```

**Qué reconocer:** el `!` de Dart y el `${}` de la plantilla te resultan obvios porque son los mismos
gestos de TypeScript. Pero el aprendizaje que te llevas de esta familia no es sintáctico: es que un
lenguaje puede tener toda la sintaxis del mundo y ninguna plataforma donde correr. **ActionScript
está aquí para eso.** Fue durante quince años una elección profesional impecable y hoy no arranca en
ningún navegador. Cuando dentro de cinco años tengas que decidir sobre un lenguaje nuevo y brillante,
esta será una de las lecciones que te llevas.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java).

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim()
    println("lecciones=$n transferible=si")
}
```

### Scala

```scala
object Cierre extends App {
  val n = scala.io.StdIn.readLine().trim
  println(s"lecciones=$n transferible=si")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim()
println "lecciones=$n transferible=si"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (str/trim (read-line))]
  (println (str "lecciones=" n " transferible=si")))
```

**Qué reconocer:** aprendiste Java y con él te llevaste, sin pagarlas aparte, cuatro sintaxis más y
una plataforma entera —el mismo `.jar`, el mismo `String.trim`, las mismas herramientas—. Kotlin,
Scala y Groovy los lees ya sin esfuerzo. Clojure es el único que exige un giro de cabeza real, y
merece que te fijes: el paréntesis va **antes** del nombre de la función, la lista es la estructura
del código, y no hay ninguna variable que se reasigne. Aun así lo sigues: `let` liga nombres,
`println` imprime, `str` concatena. Si puedes leer eso —y puedes— has cruzado la frontera entre
paradigmas, que es la más ancha de todo el Atlas.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim()
printfn "lecciones=%s transferible=si" n
```

### VB.NET

```vbnet
Module Cierre
    Sub Main()
        Dim n = Console.ReadLine().Trim()
        Console.WriteLine("lecciones=" & n & " transferible=si")
    End Sub
End Module
```

**Qué reconocer:** `Console.ReadLine`, `Trim`, `Console.WriteLine` — es la biblioteca de C# palabra
por palabra, y por eso VB.NET se lee de corrido aunque su sintaxis venga de otro siglo. F# cambia el
aspecto pero no la plataforma: el mismo CLR, los mismos tipos. Esta familia enseña una lección
específica y muy rentable: **cuando dos lenguajes comparten runtime y biblioteca estándar, lo único
que te separa de leer el segundo es un rato de sintaxis**. Vale para .NET, vale para la JVM y valdrá
para la próxima plataforma que aparezca.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c).

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string n;
    std::cin >> n;
    std::cout << "lecciones=" << n << " transferible=si\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[64];
        scanf("%63s", buf);
        printf("lecciones=%s transferible=si\n", buf);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C**, así que el programa en C de esta clase
compila casi tal cual en ambos. Lo único nuevo es la capa que cada uno añade encima: flujos y
`std::string` en C++, corchetes de mensaje y bloque de autorelease en Objective-C. Este es el caso
más literal de la tesis del curso: no aprendiste dos lenguajes más, aprendiste **el mismo lenguaje
con dos capas**, y por eso te bastó con uno.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust).

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = std.mem.trim(u8, linea, " \r");
    try std.io.getStdOut().writer().print("lecciones={s} transferible=si\n", .{n});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip()
echo "lecciones=" & n & " transferible=si"
```

### D

```d
import std.stdio, std.string;

void main() {
    const n = readln().strip();
    writefln("lecciones=%s transferible=si", n);
}
```

**Qué reconocer:** Zig es el programa más largo de la página y aun así lo entiendes entero, porque
cada pieza tiene su equivalente en Rust: el búfer que se reserva antes de usarlo, el `try` que
propaga el error de cada operación que puede fallar, el `!void` que declara "esta función puede
fallar" igual que un `Result`. Nim y D, en cambio, se leen como Python y compilan como C — la prueba
de que "sintaxis ligera" y "binario nativo" nunca fueron incompatibles, solo dos decisiones
independientes que estás ya entrenado para separar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql).

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(N), Linea),
    format("lecciones=~w transferible=si~n", [N]).
```

### Datalog

```datalog
% Datalog no lee entrada ni escribe salida: no tiene efectos. Las lecciones son
% un hecho declarado y el cierre una relacion derivada. Es el ultimo recordatorio
% del curso de que hay lenguajes que no "hacen" nada: solo dicen que es cierto.
lecciones(12).

cierre(N, "si") :- lecciones(N).
```

**Qué reconocer:** llegas al final capaz de leer el paradigma más ajeno de los cuatro. Reconoces que
en Prolog las mayúsculas son variables y las minúsculas átomos, que `:-` se lee "si", que las comas
son conjunciones y que nada de eso se ejecuta paso a paso sino que **se resuelve**. Y reconoces por
qué Datalog no puede imprimir: porque renunció a los efectos a cambio de que sus consultas siempre
terminen. Ese intercambio —poder a cambio de garantías— es la idea que más veces ha aparecido en el
programa, en tipos, en memoria, en concurrencia y ahora aquí.

---

## Y de vuelta a la clase

Veinte lenguajes. Ninguno tuvo clase propia. Los has leído todos.

Cuenta lo que hizo falta para eso: diez representantes, siete familias y un puñado de preguntas que
ahora haces automáticamente ante cualquier código —¿quién gestiona la memoria?, ¿los tipos se
comprueban antes o durante?, ¿esto se ejecuta o se resuelve?, ¿qué garantías compra a cambio de qué
poder?—. Esas preguntas son el verdadero contenido de las 176 clases. La sintaxis siempre fue lo
barato.

Y por eso el programa no termina con un examen, sino con una invitación concreta:

**Abre el [Atlas](../../../atlas/README.md), elige un primo que no hayas escrito nunca** —Kotlin,
Nim, Elixir, el que te llame— **y vuelve a cualquier clase del núcleo a resolverla con él.** Una
sola. Coge su `casos.json`, escribe la implementación y compruébala contra los casos esperados como
llevas 176 clases haciendo. No busques un tutorial del lenguaje: busca su documentación oficial, mira
dos ejemplos y confía en lo que ya sabes de su familia.

Vas a tardar menos de lo que crees. Ese es, exactamente, el resultado del curso.

⏮️ [Volver a la clase 176](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
