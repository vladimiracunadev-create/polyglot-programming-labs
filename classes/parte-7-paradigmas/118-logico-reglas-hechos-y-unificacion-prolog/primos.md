# 🧬 El mismo programa en las familias de lenguajes — Clase 118

> [⬅️ Volver a la clase 118](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si un número divide a otro, expresado como
una **regla**— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Esta vez la comparación se invierte, y conviene decirlo desde el principio. En todas las clases
anteriores el núcleo era el representante y los primos eran variaciones; aquí el tema **es** Prolog.
Reglas, hechos y unificación no son un rasgo suyo: son su modelo entero de ejecución. Así que el
lenguaje del núcleo que aparece en la clase, [SQL](README.md#sql), pasa a ser el pariente que se le
parece —también declara condiciones y deja que un motor busque las respuestas—, y los otros
dieciocho lenguajes se leen como intentos de escribir una regla con herramientas que no fueron
hechas para eso. Datalog tampoco es aquí una nota al pie: es la versión de Prolog que renuncia a la
recursión no acotada y a los términos compuestos para ganar una garantía que Prolog no tiene.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, dos enteros con `a != 0`
- **Salida** (stdout): `divisor=true` o `divisor=false`
- **Regla:** `a` divide a `b` si y solo si `b mod a = 0`

| stdin | esperado |
|---|---|
| `3 12` | `divisor=true` |
| `5 12` | `divisor=false` |
| `4 12` | `divisor=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La regla se convierte en una expresión booleana, y el valor de verdad hay que traducirlo a la palabra
que pide el contrato.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
# true y false son objetos de verdad, y su to_s ya da la palabra exacta.
puts "divisor=#{(b % a).zero?}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
# Perl no tiene tipo booleano: la verdad es 1 y la falsedad la cadena vacía.
printf "divisor=%s\n", $b % $a == 0 ? 'true' : 'false';
```

### Lua

```lua
local a, b = io.read("n", "n")
print("divisor=" .. tostring(b % a == 0))
```

### Tcl

```tcl
gets stdin linea
lassign [regexp -all -inline {\S+} $linea] a b
# expr devuelve 1 o 0: la palabra hay que ponerla a mano.
puts "divisor=[expr {$b % $a == 0 ? {true} : {false}}]"
```

### R

```r
v <- scan("stdin", quiet = TRUE, n = 2)
# R imprime TRUE/FALSE en mayúsculas: hay que bajarlas para cumplir el contrato.
cat(sprintf("divisor=%s\n", tolower(as.character(v[2] %% v[1] == 0))))
```

**Qué reconocer:** ninguno de los cinco **declara una regla**: evalúan una expresión y luego
traducen su resultado a un texto. Y esa traducción, que parece un detalle de formato, es un rayo X de
lo que cada lenguaje entiende por verdad. Ruby tiene objetos `true` y `false` que ya se imprimen
como el contrato pide. Perl no tiene booleano en absoluto —la verdad es el número 1 y la falsedad la
cadena vacía—, así que el ternario es obligatorio. `expr` de Tcl produce 1 y 0. R produce `TRUE` en
mayúsculas porque viene de la notación estadística. Cinco nociones distintas de "verdadero" para un
mismo `b mod a = 0`. En Prolog esta traducción no hará falta de la misma forma, porque allí la
respuesta **es** que la demostración salga adelante.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

// La regla como función pura de dos enteros a Boolean.
bool esDivisor(int a, int b) => b % a == 0;

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('divisor=${esDivisor(v[0], v[1])}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la regla se expresa como método y el
// reproductor la invoca con datos ya cargados.
package {
    public class Divisor {
        public static function esDivisor(a:int, b:int):Boolean {
            return b % a == 0;
        }

        public static function resultado(a:int, b:int):String {
            return "divisor=" + esDivisor(a, b);
        }
    }
}
```

**Qué reconocer:** los dos tienen un tipo `Boolean` propio que se imprime como `true`/`false`, de
modo que la concatenación da el contrato gratis, sin ternario ni conversión. También comparten el
`%` heredado de C, que en ambos —como en Java— conserva el signo del dividendo: por eso lo correcto
es escribir `b % a == 0` y no confiar en el valor del resto, que con negativos deja de ser el
matemático. El `mod` de Prolog, en cambio, sigue el signo del divisor. Es la clase de diferencia que
nunca aparece en los casos de prueba y luego aparece en producción.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java).

### Kotlin

```kotlin
fun esDivisor(a: Int, b: Int): Boolean = b % a == 0

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("divisor=${esDivisor(a, b)}")
}
```

### Scala

```scala
object Divisor {
  def esDivisor(a: Int, b: Int): Boolean = b % a == 0

  def main(args: Array[String]): Unit = {
    // `val Array(a, b) = ...` no asigna: comprueba la forma y liga los nombres si encaja.
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(s"divisor=${esDivisor(a, b)}")
  }
}
```

### Groovy

```groovy
def esDivisor = { int a, int b -> b % a == 0 }

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "divisor=${esDivisor(a, b)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; La versión directa. Clojure tiene además core.logic (miniKanren), un motor de
;; unificación completo donde esto se escribiría como una relación, no como función.
(defn divisor? [a b] (zero? (mod b a)))

(let [[a b] (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "divisor=" (divisor? a b))))
```

**Qué reconocer:** el gesto más cercano a la unificación en toda la JVM es el `val Array(a, b)` de
Scala: no asigna nada, **compara una estructura contra un patrón** y liga los nombres solo si encaja
—si la línea trajera tres números, la comparación falla y el programa se rompe ahí—. Eso es media
unificación. La otra media, la que Prolog sí tiene y Scala no, es que el patrón funcione **en las dos
direcciones**: en Prolog el mismo `divisor(A, B)` sirve para comprobar y para generar. Kotlin y
Groovy desestructuran por posición, que se parece pero es otra cosa: son llamadas a `component1()` y
`component2()`, sin comprobación de forma. Y Clojure tiene la excepción real de esta familia:
`core.logic` mete un motor miniKanren completo dentro del lenguaje, con variables lógicas y
unificación de verdad.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let esDivisor a b = b % a = 0

// El match contra [| a; b |] es deconstrucción y comprobación en un solo paso:
// la forma del dato decide qué rama se toma, igual que la cabeza de una cláusula
// decide qué regla de Prolog se intenta.
let resultado =
    match stdin.ReadLine().Trim().Split(' ') |> Array.map int with
    | [| a; b |] -> esDivisor a b
    | _ -> failwith "se esperaban dos enteros"

printfn "divisor=%b" resultado
```

### VB.NET

```vbnet
Module Divisor
    Function EsDivisor(a As Integer, b As Integer) As Boolean
        Return b Mod a = 0
    End Function

    Sub Main()
        Dim p = Console.In.ReadToEnd().Split(
            New Char() {" "c, vbTab, vbCr, vbLf}, StringSplitOptions.RemoveEmptyEntries)
        ' VB imprime True/False con mayúscula inicial: hay que bajarla.
        Console.WriteLine(
            "divisor=" & EsDivisor(CInt(p(0)), CInt(p(1))).ToString().ToLowerInvariant())
    End Sub
End Module
```

**Qué reconocer:** el `match` de F\# elige la rama **por la forma del dato**, que es exactamente el
mecanismo por el que Prolog elige qué cláusula intentar: la cabeza de la regla es un patrón, y si no
unifica se prueba la siguiente. Fíjate además en un detalle que pasa desapercibido: en F\# el `=` de
`b % a = 0` es **comparación**, no asignación. Un lenguaje que no reasigna no necesita dos símbolos
distintos, y por la misma razón Prolog usa `=` para unificar y tiene que inventarse `is` cuando de
verdad quiere evaluar aritmética. VB.NET está en el otro extremo: escribe `Mod` como palabra, su
booleano se imprime `True` con mayúscula y hay que convertirlo, y la regla es un `Function` que
devuelve un valor, sin ninguna posibilidad de preguntarle al revés.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c), donde no hay ni siquiera un tipo booleano nativo
antes de C99.

### C++

```cpp
#include <iostream>

// constexpr: si los argumentos se conocen al compilar, la regla se evalúa entonces.
constexpr bool es_divisor(int a, int b) { return b % a == 0; }

int main() {
    int a, b;
    std::cin >> a >> b;
    // boolalpha es un manipulador dedicado a imprimir bool como palabra en vez de 1/0.
    std::cout << "divisor=" << std::boolalpha << es_divisor(a, b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

static BOOL esDivisor(int a, int b) {
    return b % a == 0;
}

int main(void) {
    @autoreleasepool {
        int a, b;
        scanf("%d %d", &a, &b);
        // BOOL es un typedef de char disfrazado: YES vale 1, y no hay palabra que imprimir.
        printf("divisor=%s\n", esDivisor(a, b) ? "true" : "false");
    }
    return 0;
}
```

**Qué reconocer:** C++ tiene `bool` de verdad y hasta un manipulador de flujo dedicado a imprimirlo
como palabra, `std::boolalpha` —un lujo que delata cuánto le importa a C++ el formato de salida—.
Objective-C conserva el `BOOL` de C, que es un `char` con otro nombre: `YES` es el número 1, no hay
nada legible que imprimir y el ternario es inevitable. El detalle interesante está en `constexpr`:
cuando los argumentos se conocen al compilar, C++ evalúa la regla entonces y la deja convertida en
una constante. Eso es, en el fondo, lo mismo que hace Datalog al derivar todos los hechos que se
siguen de las reglas antes de responder ninguna consulta.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust).

### Zig

```zig
const std = @import("std");

fn esDivisor(a: i64, b: i64) bool {
    return @rem(b, a) == 0;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    // {} sobre un bool imprime true/false directamente.
    try std.io.getStdOut().writer().print("divisor={}\n", .{esDivisor(a, b)});
}
```

### Nim

```nim
import std/[strutils, sequtils]

# `func` es un `proc` sin efectos secundarios, y el compilador lo comprueba.
func esDivisor(a, b: int): bool = b mod a == 0

let v = stdin.readLine().splitWhitespace().map(parseInt)
echo "divisor=", esDivisor(v[0], v[1])
```

### D

```d
import std.stdio, std.string, std.conv, std.array, std.algorithm;

// `pure` es una anotación verificada: la función solo depende de sus argumentos.
pure bool esDivisor(int a, int b) { return b % a == 0; }

void main() {
    auto v = readln().strip().split().map!(to!int).array;
    writefln("divisor=%s", esDivisor(v[0], v[1]));
}
```

**Qué reconocer:** los tres imprimen el booleano como palabra sin ayuda, porque su `bool` es un tipo
de primera clase para el formateador. Pero lo que de verdad los acerca al tema de la clase es otra
cosa: los tres permiten **marcar la regla como pura** —`func` en Nim, `pure` en D, y en Zig la
ausencia declarada de efectos— y el compilador lo comprueba. Un predicado puro sobre datos inmutables
es, funcionalmente, una regla lógica: mismas entradas, misma verdad, sin que importe el orden en que
se evalúe. Es lo más cerca que llega un lenguaje de sistemas. Lo que sigue faltando es la
reversibilidad: `esDivisor(4, 12)` responde, pero no hay forma de preguntar `esDivisor(?, 12)` y
obtener todos los divisores. Y `@rem` de Zig, frente al `mod` de Nim, vuelve a poner sobre la mesa la
diferencia de signo entre resto y módulo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql), que en esta clase deja de ser el modelo y pasa a
ser el pariente: describe condiciones y deja buscar al motor, pero solo sobre las filas que ya tiene.

### Prolog

```prolog
:- initialization(main, main).

% La regla, tal cual se lee: A divide a B si el resto de B entre A es cero.
% No hay `return` ni `if`: esto es una relación entre A y B, no una función.
divisor(A, B) :- 0 is B mod A.

main :-
    read_line_to_string(user_input, Linea),
    % Unificación: la lista de partes se compara contra el patrón [SA, SB] y solo
    % encaja si hay exactamente dos. El patrón ES la comprobación.
    split_string(Linea, " ", " ", [SA, SB]),
    number_string(A, SA),
    number_string(B, SB),
    (   divisor(A, B)
    ->  writeln('divisor=true')
    ;   writeln('divisor=false')
    ).

% Y como es una relación, la MISMA regla sirve para generar en vez de comprobar:
%   ?- between(1, 12, A), divisor(A, 12).
%   A = 1 ; A = 2 ; A = 3 ; A = 4 ; A = 6 ; A = 12.
```

### Datalog

```datalog
% Datalog no lee stdin ni tiene efectos: los pares a comprobar entran como hechos.
par(3, 12).
par(5, 12).
par(4, 12).

% La misma regla que en Prolog, pero sin recursión no acotada ni términos
% compuestos: la evaluación de esta consulta SIEMPRE termina.
divisor(A, B) :- par(A, B), B % A = 0.
```

**Qué reconocer:** aquí es donde la página deja de comparar y empieza a explicar. En Prolog
`divisor(A, B)` **no es una función que devuelva verdadero o falso**: es una relación, y la respuesta
del programa es si el motor consiguió demostrarla. Por eso la regla no tiene `return` ni `if`; el
`->` que ves en `main` está solo para traducir "el objetivo tuvo éxito" a la palabra que exige el
contrato, y es la única parte del programa que no es lógica pura. La unificación aparece dos veces y
con dos papeles distintos: en `split_string(..., [SA, SB])` el patrón hace de comprobación —si no hay
exactamente dos partes, el objetivo falla y no hace falta ningún `assert`—, y en `0 is B mod A` no
liga nada, porque los dos lados ya están instanciados, así que degenera en una comparación. Y luego
está lo que ningún otro de los veinte lenguajes puede hacer: la misma regla, sin tocar una línea,
responde `divisor(3, 12)` y también enumera todos los `A` que dividen a 12. Una función va en una
dirección; una relación va en todas.

SQL, el pariente del núcleo, hace la mitad: `WHERE b % a = 0` describe la condición igual de bien y
deja que el planificador decida el recorrido, pero solo puede preguntar por las filas que ya están en
la tabla. No puede inventarse los candidatos. Datalog se sitúa en medio y es el mejor resumen de todo
el asunto: es Prolog al que se le han quitado la recursión no acotada y los términos compuestos, con
lo que pierde la capacidad de construir estructuras arbitrarias y de escribir bucles que no acaben,
y a cambio gana algo que Prolog no puede prometer —**toda consulta termina**—. Esa es exactamente la
razón por la que Datalog, y no Prolog, es el lenguaje que se ha colado en los motores de análisis
estático, en los sistemas de permisos y en las bases de datos deductivas.

---

## Y de vuelta a la clase

Veinte lenguajes preguntando "¿divide 3 a 12?", y dieciocho de ellos respondiendo con una expresión
booleana que hay que traducir a una palabra. Solo Prolog y Datalog contestan preguntando: declaran la
relación y dejan que el motor busque. La transferencia que queda es esta: cada vez que escribas una
función pura que devuelve un booleano, estás escribiendo una regla lógica a la que le han quitado la
capacidad de correr hacia atrás.

⏮️ [Volver a la clase 118](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
