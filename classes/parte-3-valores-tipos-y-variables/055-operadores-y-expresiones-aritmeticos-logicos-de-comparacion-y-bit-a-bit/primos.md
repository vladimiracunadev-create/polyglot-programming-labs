# 🧬 El mismo programa en las familias de lenguajes — Clase 055

> [⬅️ Volver a la clase 055](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —las cinco operaciones aritméticas sobre dos
enteros— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir. Y este problema esconde una
trampa magnífica: `+`, `-` y `*` se escriben igual en los veinte lenguajes, pero la **división
entera** no. Ahí es donde cada familia enseña su modelo numérico.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (enteros positivos, con `b != 0`)
- **Salida** (stdout): `suma=<a+b> resta=<a-b> mult=<a*b> div=<a/b entera> mod=<a%b>`
- **Regla:** las cinco operaciones aritméticas sobre `a` y `b`, con división **entera**

| stdin | esperado |
|---|---|
| `10 3` | `suma=13 resta=7 mult=30 div=3 mod=1` |
| `20 4` | `suma=24 resta=16 mult=80 div=5 mod=0` |
| `7 2` | `suma=9 resta=5 mult=14 div=3 mod=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico, poca ceremonia, la variable no declara tipo. Y justo por eso, cada uno tiene que
decidir qué significa dividir dos enteros.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
puts "suma=#{a + b} resta=#{a - b} mult=#{a * b} div=#{a / b} mod=#{a % b}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
printf "suma=%d resta=%d mult=%d div=%d mod=%d\n",
    $a + $b, $a - $b, $a * $b, int($a / $b), $a % $b;
```

### Lua

```lua
local a, b = io.read("n", "n")
print(string.format("suma=%d resta=%d mult=%d div=%d mod=%d",
    a + b, a - b, a * b, a // b, a % b))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
puts [format "suma=%d resta=%d mult=%d div=%d mod=%d" \
    [expr {$a + $b}] [expr {$a - $b}] [expr {$a * $b}] \
    [expr {$a / $b}] [expr {$a % $b}]]
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
a <- v[1]
b <- v[2]
cat(sprintf("suma=%d resta=%d mult=%d div=%d mod=%d\n",
            a + b, a - b, a * b, a %/% b, a %% b))
```

**Qué reconocer:** los cinco escriben `+`, `-` y `*` exactamente igual, y a partir de ahí se separan.
Ruby, como Python, hace que `/` entre enteros ya sea entero. Perl **no tiene enteros**: todo número es
un escalar de coma flotante, así que `10 / 3` da `3.333...` y hay que truncarlo a mano con `int(...)`.
Lua tuvo el mismo problema hasta la versión 5.3, que introdujo el operador `//` precisamente para
distinguir la división entera de la real. R marca sus dos operadores con símbolos rodeados de
porcentajes —`%/%` para dividir y `%%` para el resto—, una notación heredada de su sintaxis de
operadores definibles por el usuario. Tcl, fiel a su naturaleza de *todo es cadena*, ni siquiera puede
sumar sin envolver la expresión en `expr`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final a = v[0];
  final b = v[1];
  print('suma=${a + b} resta=${a - b} mult=${a * b} div=${a ~/ b} mod=${a % b}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustran los operadores.
// Aunque los parámetros sean `int`, `a / b` produce un `Number` de coma flotante:
// la división entera hay que forzarla con una conversión explícita.
package {
    public class Operaciones {
        public static function calcular(a:int, b:int):String {
            return "suma=" + (a + b) +
                   " resta=" + (a - b) +
                   " mult=" + (a * b) +
                   " div=" + int(a / b) +
                   " mod=" + (a % b);
        }
    }
}
```

**Qué reconocer:** ActionScript enseña sin filtro la herencia de JavaScript, donde el único número era
un `double` de 64 bits: aunque declares `int`, la división te devuelve coma flotante y el truncado es
cosa tuya. Dart rompió con esa tradición —tiene `int` y `double` como tipos distintos— y por eso
necesitó un operador nuevo: `~/` es "divide y trunca", el equivalente exacto del `//` de Python. Ver
un símbolo que no existe en ningún otro lenguaje de la familia es la pista de que el modelo numérico
cambió por debajo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readln().trim().split(Regex("\\s+")).map { it.toInt() }
    println("suma=${a + b} resta=${a - b} mult=${a * b} div=${a / b} mod=${a % b}")
}
```

### Scala

```scala
object Operaciones extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"suma=${a + b} resta=${a - b} mult=${a * b} div=${a / b} mod=${a % b}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "suma=${a + b} resta=${a - b} mult=${a * b} div=${a.intdiv(b)} mod=${a % b}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))]
  (println (format "suma=%d resta=%d mult=%d div=%d mod=%d"
                   (+ a b) (- a b) (* a b) (quot a b) (rem a b))))
```

**Qué reconocer:** Kotlin y Scala se comportan igual que Java —`/` entre `Int` es división entera— y
además **desestructuran** el resultado en dos nombres, algo que Java no permite. Groovy es la
excepción reveladora: para evitar la sorpresa clásica de que `10 / 3` valga `3`, cambió el operador
para que devuelva un `BigDecimal` exacto, y quien quiera la división entera debe pedirla por su nombre
con `intdiv`. Clojure cambia de paradigma dentro de la misma máquina virtual: **los operadores no son
operadores**, son funciones normales invocadas en prefijo, y por eso `(+ a b)` acepta cualquier número
de argumentos. También distingue `quot`/`rem` (truncan hacia cero, como Java) de `mod` (redondea hacia
abajo, como Python), una diferencia invisible con enteros positivos y decisiva con negativos.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "suma=%d resta=%d mult=%d div=%d mod=%d" (a + b) (a - b) (a * b) (a / b) (a % b)
```

### VB.NET

```vbnet
Imports System

Module Operaciones
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Console.WriteLine($"suma={a + b} resta={a - b} mult={a * b} div={a \ b} mod={a Mod b}")
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR y comparten el mismo `Int32`, pero VB.NET viene de otra
tradición sintáctica y lo dice en cada símbolo: usa `\` para la división **entera** (reservando `/`
para la real, que siempre devuelve coma flotante) y escribe el resto como la palabra `Mod` en vez de
`%`. Es el mismo bytecode con vocabulario de BASIC. F# muestra el otro extremo: funcional, con `|>`
encadenando en vez de anidar llamadas, y con una regla que sorprende a quien viene de C# —sus
operadores aritméticos **no convierten tipos automáticamente**, así que mezclar un `int` y un `float`
en la misma expresión es un error de compilación, no una promoción silenciosa.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>

int main() {
    long long a = 0, b = 0;
    std::cin >> a >> b;
    std::cout << "suma=" << a + b
              << " resta=" << a - b
              << " mult=" << a * b
              << " div=" << a / b
              << " mod=" << a % b << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a = 0, b = 0;
        scanf("%ld %ld", &a, &b);
        printf("suma=%ld resta=%ld mult=%ld div=%ld mod=%ld\n",
               a + b, a - b, a * b, a / b, a % b);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C** y heredan sus operadores intactos: `/` entre
enteros trunca hacia cero y `%` es el resto de esa división, con la misma regla que fija el estándar de
C desde C99. Los dos comparten además el peligro que el ejercicio no llega a tocar: `%` **no está
definido** para el divisor cero y el desbordamiento con enteros con signo es comportamiento
indefinido, no un error en tiempo de ejecución. C++ sustituye `printf` por flujos (`<<`), lo que le
permite formatear sin declarar el tipo en la cadena; Objective-C conserva `printf` tal cual, con sus
`%ld` que deben coincidir exactamente con el tipo o el programa lee basura.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try std.io.getStdOut().writer().print(
        "suma={d} resta={d} mult={d} div={d} mod={d}\n",
        .{ a + b, a - b, a * b, @divTrunc(a, b), @rem(a, b) },
    );
}
```

### Nim

```nim
import std/[strutils, strformat]

let v = stdin.readLine().splitWhitespace()
let a = v[0].parseInt
let b = v[1].parseInt
echo &"suma={a + b} resta={a - b} mult={a * b} div={a div b} mod={a mod b}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

void main() {
    auto v = readln().split().map!(to!long).array;
    const a = v[0], b = v[1];
    writefln("suma=%d resta=%d mult=%d div=%d mod=%d", a + b, a - b, a * b, a / b, a % b);
}
```

**Qué reconocer:** Zig es el más explícito de todos y aquí llega hasta el final: con enteros con signo
**se niega a aceptar `/` y `%`**, porque el redondeo con negativos es ambiguo, y te obliga a elegir
entre `@divTrunc` y `@divFloor`, entre `@rem` y `@mod`. Además, sus `+`, `-` y `*` comprueban el
desbordamiento y **abortan** el programa en compilación de depuración en vez de dar la vuelta en
silencio, la misma decisión que toma Rust. Nim escribe la división entera con palabras (`div`, `mod`)
en lugar de símbolos, herencia directa de Pascal y Modula, mientras que D conserva la sintaxis de C
intacta. Tres lenguajes con el mismo destino —un binario nativo— y tres respuestas distintas a la
pregunta de cuánto debe estorbarte el compilador.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    Suma is A + B,
    Resta is A - B,
    Mult is A * B,
    Div is A // B,
    Mod is A mod B,
    format("suma=~d resta=~d mult=~d div=~d mod=~d~n", [Suma, Resta, Mult, Div, Mod]).
```

### Datalog

```datalog
% Datalog puro no tiene funciones ni aritmética: solo relaciones entre hechos. Los
% dialectos extendidos (Soufflé, LogiQL) sí evalúan expresiones, y así se escribiría.
% La entrada tampoco viene de stdin: los operandos son un hecho declarado.
par(10, 3).

operaciones(S, R, M, D, Md) :-
    par(A, B),
    S = A + B, R = A - B, M = A * B, D = A / B, Md = A % B.
```

**Qué reconocer:** en Prolog `Suma is A + B` **no** es una asignación sino una unificación con el
resultado de evaluar la expresión, y el detalle importante es que la aritmética solo ocurre porque se
la pide explícitamente con `is`: escribir `Suma = A + B` ligaría `Suma` al **término** `10+3` sin
calcular nada. Sus operadores también se escriben con palabras (`//`, `mod`, `rem`), y `mod` redondea
hacia abajo mientras `rem` trunca, la misma distinción que hace Clojure. Datalog lleva la idea al
extremo: sin efectos, sin entrada/salida y —en su forma pura— sin ni siquiera aritmética, porque una
función convertiría el conjunto de hechos derivables en infinito. Es la misma renuncia que hace SQL al
no decirte cómo recorrer las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer dos enteros, aplicar cinco
operaciones, imprimir la línea. Lo que cambia es la **forma** —símbolos, palabras o funciones— y, sobre
todo, las **garantías**: quién trunca, quién redondea, quién avisa del desbordamiento y quién se calla.
Eso es lo transferible.

⏮️ [Volver a la clase 055](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
