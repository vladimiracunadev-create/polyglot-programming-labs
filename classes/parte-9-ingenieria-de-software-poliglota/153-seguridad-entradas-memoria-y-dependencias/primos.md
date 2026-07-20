# 🧬 El mismo programa en las familias de lenguajes — Clase 153

> [⬅️ Volver a la clase 153](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si una entrada es alfanumérica, la primera
línea de defensa de cualquier sistema— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra a validar
- **Salida** (stdout): `seguro=true` si todos los caracteres son letras o dígitos, `seguro=false` si no
- **Regla:** validar por **lista blanca**, no por lista negra de caracteres prohibidos

| stdin | esperado |
|---|---|
| `abc` | `seguro=true` |
| `a;b` | `seguro=false` |
| `hola123` | `seguro=true` |

Fíjate en el caso del medio: el carácter peligroso es `;`, que separa comandos en un intérprete de
órdenes y sentencias en SQL. Validar por lista blanca —"solo esto pasa"— en lugar de por lista negra
—"esto no pasa"— es la única defensa que no se rompe cuando aparece un carácter que nadie previó.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia donde el peligro no es la memoria sino la **evaluación**: `eval`, `system`, la
interpolación de una cadena dentro de una consulta. Y también la familia que inventó la mejor
defensa histórica contra ello.

### Ruby

```ruby
entrada = STDIN.gets.strip
# \A y \z, no ^ y $: en Ruby ^ y $ casan en cada salto de línea, y "abc\n; rm -rf /"
# pasaría una validación escrita con ^[[:alnum:]]+$.
puts "seguro=#{entrada.match?(/\A[[:alnum:]]+\z/)}"
```

### Perl

```perl
use strict;
use warnings;

# Con el modo taint (perl -T) esta línea llegaría "contaminada" desde stdin y el
# intérprete se negaría a usarla en system() o en un open(); el único modo de limpiarla
# es hacerla pasar por una captura de expresión regular como esta.
chomp(my $entrada = <STDIN>);
my $seguro = $entrada =~ /\A([A-Za-z0-9]+)\z/ ? 'true' : 'false';
print "seguro=$seguro\n";
```

### Lua

```lua
local entrada = io.read("l")
local seguro = entrada:match("^%w+$") ~= nil
print("seguro=" .. tostring(seguro))
```

### Tcl

```tcl
gets stdin entrada
puts "seguro=[expr {[string is alnum -strict $entrada] ? {true} : {false}}]"
```

### R

```r
entrada <- readLines("stdin", n = 1)
seguro <- grepl("^[[:alnum:]]+$", entrada)
cat(sprintf("seguro=%s\n", tolower(seguro)))
```

**Qué reconocer:** los cinco validan con una lista blanca de caracteres, pero cada uno enseña un
peligro distinto de su comunidad. Perl y Ruby tienen el **modo taint** —`perl -T`, y el equivalente
`$SAFE` que Ruby ya ha retirado—: el intérprete marca como contaminado todo lo que viene de fuera y
se niega a pasarlo a `system` o a `open` hasta que lo has limpiado con una captura de expresión
regular. Es la mejor idea histórica sobre validación de entradas y sigue sin tener equivalente
directo en la mayoría de lenguajes modernos. Ruby además obliga a `\A` y `\z` en vez de `^` y `$`,
porque sus anclas casan en cada salto de línea y esa diferencia ha causado vulnerabilidades reales.
Tcl es el caso más delicado de la familia: como todo es cadena y `expr` evalúa, interpolar entrada
sin comprobar es inyección directa —de ahí las llaves `{}` alrededor de la expresión, que impiden la
sustitución prematura—. Y `%w` de Lua depende de la configuración regional, así que "alfanumérico"
no significa exactamente lo mismo en todas las máquinas.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

final _alfanumerico = RegExp(r'^[A-Za-z0-9]+$');

void main() {
  final entrada = stdin.readLineSync()!.trim();
  print('seguro=${_alfanumerico.hasMatch(entrada)}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: la entrada llega como parámetro.
package {
    public class Validador {
        private static const ALFANUMERICO:RegExp = /^[A-Za-z0-9]+$/;

        public static function validar(entrada:String):String {
            return "seguro=" + ALFANUMERICO.test(entrada);
        }
    }
}
```

**Qué reconocer:** la sintaxis de expresión regular es la de JavaScript en los dos, y `hasMatch` /
`test` devuelven el booleano que se imprime tal cual. El riesgo característico de esta familia no es
el desbordamiento sino el **XSS**: una entrada no validada que acaba dentro del DOM. ActionScript lo
sufrió en su momento con `ExternalInterface.call`, que inyectaba en el JavaScript de la página, y
Flash acabó siendo retirado en 2020 en buena medida por su historial de vulnerabilidades — un
recordatorio de que la seguridad de un lenguaje incluye la de su tiempo de ejecución. Ojo también con
el `$` de esta familia y de .NET: en JavaScript sin la bandera `m` sí ancla al final real, pero es un
detalle que cambia entre motores y conviene no dar por supuesto.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Memoria gestionada y comprobación de límites en
cada acceso a un array: el desbordamiento de búfer simplemente no existe aquí.

### Kotlin

```kotlin
fun main() {
    val entrada = readLine()!!.trim()
    println("seguro=${entrada.isNotEmpty() && entrada.all { it.isLetterOrDigit() }}")
}
```

### Scala

```scala
object Validador {
  def main(args: Array[String]): Unit = {
    val entrada = scala.io.StdIn.readLine().trim
    val seguro = entrada.nonEmpty && entrada.forall(_.isLetterOrDigit)
    println(s"seguro=$seguro")
  }
}
```

### Groovy

```groovy
def entrada = System.in.newReader().readLine().trim()
// ==~ exige que la expresión case con la cadena entera; =~ solo busca dentro.
println "seguro=${entrada ==~ /[A-Za-z0-9]+/}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [entrada (str/trim (read-line))]
  ;; re-matches exige coincidencia completa; re-find solo buscaría una subcadena.
  (println (str "seguro=" (boolean (re-matches #"[A-Za-z0-9]+" entrada)))))
```

**Qué reconocer:** los cuatro evitan la expresión regular anclada usando `all` / `forall` sobre los
caracteres, o bien una función que **exige coincidencia total por diseño**. Esa es la diferencia que
importa: `==~` de Groovy y `re-matches` de Clojure fallan si sobra un solo carácter, mientras que
`=~` y `re-find` solo buscan dentro y son el origen clásico del bug "mi validación aceptaba
`abc; DROP TABLE`". El riesgo real de esta familia no es la memoria —la JVM comprueba todos los
límites— sino la **cadena de dependencias**: Log4Shell fue una vulnerabilidad de una biblioteca de
registro, no del lenguaje, y por eso aquí se firman artefactos y se auditan los `pom.xml`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System.Text.RegularExpressions

// En .NET, $ también casa justo antes de un \n final: para anclar de verdad hay que usar \z.
let esSeguro (s: string) = Regex.IsMatch(s, @"\A[A-Za-z0-9]+\z")

let entrada = stdin.ReadLine().Trim()
printfn "seguro=%b" (esSeguro entrada)
```

### VB.NET

```vbnet
Imports System.Linq

Module Validador
    Sub Main()
        Dim entrada = Console.ReadLine().Trim()
        Dim seguro = entrada.Length > 0 AndAlso entrada.All(Function(c) Char.IsLetterOrDigit(c))
        Console.WriteLine("seguro=" & If(seguro, "true", "false"))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `System.Text.RegularExpressions` y `Char.IsLetterOrDigit`, y
comparten también la trampa que el comentario de F# señala: en .NET el ancla `$` casa **antes de un
salto de línea final**, así que `"abc\n"` pasa una validación escrita con `$` y hay que usar `\z`
para cerrar de verdad. Es el mismo error que en Ruby, en otra plataforma. Fíjate además en que
VB.NET evita del todo la expresión regular: recorrer caracteres con `All` no tiene anclas que
equivocar, y tampoco puede sufrir un **ReDoS**, esa denegación de servicio por retroceso exponencial
que afecta a los motores de expresiones regulares con retroceso — el de .NET incluido, hasta que
llegó el motor no retroactivo opcional.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La única familia de esta página donde una entrada
demasiado larga puede sobrescribir la pila y ejecutar código ajeno.

### C++

```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>

int main() {
    std::string entrada;
    // std::string crece sola: aquí no hay búfer fijo que desbordar, a diferencia de
    // un scanf("%s", buf) sobre un char[].
    std::cin >> entrada;
    const bool seguro = !entrada.empty() &&
        std::all_of(entrada.begin(), entrada.end(),
                    [](unsigned char c) { return std::isalnum(c) != 0; });
    std::cout << "seguro=" << (seguro ? "true" : "false") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[256];
        // El ancho %255s es obligatorio: sin él, scanf escribe más allá de buf.
        if (scanf("%255s", buf) != 1) { buf[0] = '\0'; }
        NSString *entrada = [NSString stringWithUTF8String:buf];
        NSCharacterSet *noAlfa = [[NSCharacterSet alphanumericCharacterSet] invertedSet];
        BOOL seguro = entrada.length > 0 &&
            [entrada rangeOfCharacterFromSet:noAlfa].location == NSNotFound;
        printf("seguro=%s\n", seguro ? "true" : "false");
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C y **heredan sus desbordamientos**: son, junto con C,
los únicos lenguajes de esta página donde leer una palabra puede corromper la memoria del proceso.
C++ ofrece la salida —`std::string` gestiona su propio tamaño, así que el búfer fijo desaparece— pero
no la impone: el `char buf[256]` de C sigue compilando. Objective-C muestra el otro camino, que es
subir a `NSString` y `NSCharacterSet` en cuanto se puede, dejando el `char[]` reducido al mínimo
tramo posible. Ojo también con `std::isalnum`: hay que convertir a `unsigned char` antes de pasarlo,
porque con un carácter de signo negativo el comportamiento es indefinido — un detalle diminuto que
solo existe en esta familia.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Nacieron, entre otras
cosas, para tener el rendimiento de C sin sus vulnerabilidades de memoria.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    // El búfer es fijo, pero Zig comprueba los límites en Debug y ReleaseSafe:
    // un desbordamiento aborta el programa en vez de corromper la pila.
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const entrada = std.mem.trim(u8, linea, " \r\n");

    var seguro = entrada.len > 0;
    for (entrada) |c| {
        if (!std.ascii.isAlphanumeric(c)) seguro = false;
    }
    try std.io.getStdOut().writer().print("seguro={s}\n", .{if (seguro) "true" else "false"});
}
```

### Nim

```nim
import std/strutils

let entrada = stdin.readLine().strip()
let seguro = entrada.len > 0 and entrada.allCharsInSet(Letters + Digits)
echo "seguro=", (if seguro: "true" else: "false")
```

### D

```d
import std.stdio, std.string, std.algorithm, std.ascii;

void main() {
    const entrada = readln().strip();
    const seguro = entrada.length > 0 && entrada.all!isAlphaNum;
    writefln("seguro=%s", seguro ? "true" : "false");
}
```

**Qué reconocer:** los tres compilan a nativo como C, pero ninguno hereda su agujero. Zig lo dice
explícitamente en los modos `Debug` y `ReleaseSafe`: cada acceso a un array se comprueba y un
desbordamiento **aborta** el programa; en `ReleaseFast` esas comprobaciones se apagan, y esa decisión
es tuya y consciente, no un descuido. D comprueba también los límites por defecto y solo los quita
con `-boundscheck=off`, y Nim hace lo mismo salvo con `-d:danger`. Fíjate en `Letters + Digits` de
Nim: son conjuntos de caracteres del lenguaje, y `allCharsInSet` es una lista blanca escrita como
teoría de conjuntos. El otro frente de esta familia es la dependencia: `cargo audit` en Rust y
`govulncheck` en Go existen porque un binario nativo también arrastra código de terceros.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia donde nació la inyección más famosa de
todas, y donde la defensa correcta no es validar sino **parametrizar**.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    string_chars(Linea, Chars),
    (   Chars \= [],
        forall(member(C, Chars), char_type(C, alnum))
    ->  Seguro = true
    ;   Seguro = false
    ),
    format("seguro=~w~n", [Seguro]).
```

### Datalog

```datalog
% Datalog no lee de stdin ni recorre cadenas: la entrada se declara carácter a carácter,
% y "todos cumplen" se expresa con negación estratificada sobre "existe uno que no cumple".
caracter(1, a).
caracter(2, b).
caracter(3, c).

alfanumerico(a).
alfanumerico(b).
alfanumerico(c).

inseguro :- caracter(_, C), not alfanumerico(C).
seguro :- not inseguro.
```

**Qué reconocer:** `forall(member(C, Chars), char_type(C, alnum))` de Prolog no es un bucle: es la
afirmación lógica "para todo carácter se cumple", y el motor la comprueba por retroceso. Datalog no
puede ni recorrer la cadena, así que declara los caracteres como hechos y define `seguro` como la
negación de "existe un carácter no alfanumérico" — la doble negación es el modo de decir "todos" en
un lenguaje que solo sabe buscar ejemplos. Lo importante es que esta familia tiene su propia lección
de seguridad, y es la más repetida del oficio: **en SQL la validación de la entrada no sustituye a la
consulta parametrizada**. Los `?` de una sentencia preparada separan código de datos en el protocolo,
y esa separación es la única que ninguna entrada creativa puede saltarse. Prolog conoce el mismo
peligro por otro nombre: llamar a `read_term/2` o a `assert/1` sobre texto no validado equivale
exactamente al `eval` de los lenguajes dinámicos.

---

## Y de vuelta a la clase

Veinte lenguajes, una sola validación, y tres peligros que se reparten de forma muy desigual. El
**desbordamiento de memoria** solo existe en C, C++ y Objective-C; Zig, Nim y D lo neutralizan
comprobando límites y te dejan apagar la red a sabiendas; la JVM, el CLR y los dinámicos ni lo
plantean. La **inyección por evaluación** es el problema de los dinámicos y de SQL, y su antídoto
—separar código de datos, o marcar lo que viene de fuera como en el modo taint de Perl— vale en todos
ellos. Y la **dependencia** es la única amenaza que comparten los veinte. Saber cuál de las tres te
toca según la familia en la que estás: eso es lo transferible.

⏮️ [Volver a la clase 153](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
