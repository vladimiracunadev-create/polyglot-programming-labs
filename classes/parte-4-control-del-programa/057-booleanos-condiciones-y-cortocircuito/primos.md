# 🧬 El mismo programa en las familias de lenguajes — Clase 057

> [⬅️ Volver a la clase 057](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —dos condiciones y su conjunción con cortocircuito—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `positivo=<true|false> par=<true|false> ambos=<true|false>`
- **Regla:** `positivo = n > 0`; `par = n % 2 == 0`; `ambos = positivo && par` (con cortocircuito)

| stdin | esperado |
|---|---|
| `4` | `positivo=true par=true ambos=true` |
| `-3` | `positivo=false par=false ambos=false` |
| `7` | `positivo=true par=false ambos=false` |

Ojo con un detalle que esta clase saca a la luz: la palabra `true` de la salida es **texto**, no el
booleano del lenguaje. Cada familia tiene su propia idea de qué es verdad y de cómo se imprime.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico, poca ceremonia. Aquí es donde más divergen las **nociones de verdad**: cada
lenguaje decidió por su cuenta qué valores cuentan como falsos.

### Ruby

```ruby
n = STDIN.gets.to_i
pos = n > 0
par = n.even?
puts "positivo=#{pos} par=#{par} ambos=#{pos && par}"
```

### Perl

```perl
chomp(my $n = <STDIN>);
my $pos = $n > 0;
my $par = $n % 2 == 0;
# Perl no tiene tipo booleano: la verdad es 1 y la falsedad la cadena vacía,
# así que hay que traducirla a "true"/"false" a mano.
my $tf = sub { $_[0] ? "true" : "false" };
printf "positivo=%s par=%s ambos=%s\n",
    $tf->($pos), $tf->($par), $tf->($pos && $par);
```

### Lua

```lua
local n = tonumber(io.read("l"))
local pos = n > 0
local par = n % 2 == 0
-- En Lua solo `nil` y `false` son falsos: el 0 y la cadena vacía son VERDADEROS.
print(("positivo=%s par=%s ambos=%s"):format(
  tostring(pos), tostring(par), tostring(pos and par)))
```

### Tcl

```tcl
proc tf {b} { expr {$b ? "true" : "false"} }

gets stdin n
set pos [expr {$n > 0}]
set par [expr {$n % 2 == 0}]
set ambos [expr {$pos && $par}]
puts "positivo=[tf $pos] par=[tf $par] ambos=[tf $ambos]"
```

### R

```r
tf <- function(b) if (b) "true" else "false"

n <- as.integer(readLines("stdin", n = 1))
pos <- n > 0
par <- n %% 2 == 0
cat(sprintf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par)))
```

**Qué reconocer:** los cinco escriben la comparación igual, pero **no comparten la noción de
verdad**. Ruby solo considera falsos `nil` y `false` —el `0` es verdadero, al contrario que en
Python—. Perl ni siquiera tiene tipo booleano: devuelve `1` o la cadena vacía, por eso hay que
traducir a texto a mano. Lua coincide con Ruby (`nil`/`false` y nada más). Tcl vive en el otro
extremo: sus booleanos son las cadenas `"1"` y `"0"`, y toda la lógica pasa por `expr`. R distingue
`&&` (escalar, con cortocircuito) de `&` (vectorizado, **sin** cortocircuito) —confundirlos es el
error clásico de la comunidad estadística—.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final pos = n > 0;
  final par = n % 2 == 0;
  print('positivo=$pos par=$par ambos=${pos && par}');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
    public class Booleanos {
        public static function describir(n:int):String {
            var pos:Boolean = n > 0;
            var par:Boolean = n % 2 == 0;
            return "positivo=" + pos + " par=" + par + " ambos=" + (pos && par);
        }
    }
}
```

**Qué reconocer:** el `&&` con cortocircuito es idéntico al de JavaScript, y la interpolación
convierte el booleano a `"true"`/`"false"` sin pedirlo. La diferencia relevante es el **rigor**:
Dart exige que la condición de un `if` sea un `bool` de verdad —no acepta `if (n)`—, mientras que
JavaScript y ActionScript aplican coerción. Es la misma disciplina que TypeScript intenta imponer
con `strict`, pero aquí la impone el propio lenguaje. Ojo también con `%`: Dart devuelve siempre un
resto no negativo (`-3 % 2` es `1`), mientras ActionScript conserva el signo (`-1`); con el test de
paridad `== 0` da igual, pero no siempre lo dará.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Mismo bytecode, misma biblioteca; lo que
cambia es cuánta ceremonia exige cada uno.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val pos = n > 0
    val par = n % 2 == 0
    println("positivo=$pos par=$par ambos=${pos && par}")
}
```

### Scala

```scala
object Booleanos extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  val pos = n > 0
  val par = n % 2 == 0
  println(s"positivo=$pos par=$par ambos=${pos && par}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def pos = n > 0
def par = n % 2 == 0
println "positivo=$pos par=$par ambos=${pos && par}"
```

### Clojure

```clojure
(let [n   (Integer/parseInt (.trim (read-line)))
      pos (pos? n)
      par (even? n)]
  ;; `and` no devuelve un booleano: devuelve el primer valor falso
  ;; o el último verdadero. Aquí ambos son booleanos, así que coincide.
  (println (format "positivo=%s par=%s ambos=%s" pos par (and pos par))))
```

**Qué reconocer:** los cuatro heredan de Java el `boolean` primitivo y su impresión en minúsculas,
por eso ninguno necesita traducir a texto. Kotlin y Scala son estrictos como Java: la condición ha de
ser booleana. Groovy rompe la familia introduciendo *Groovy truth* —cadenas vacías, colecciones
vacías, `0` y `null` son falsos—, un dinamismo que Java jamás aceptó. Clojure cambia dos cosas a la
vez: su `and` **no es un operador sino una macro** que devuelve un valor (por eso puede cortocircuitar
y por eso `(and 1 2)` vale `2`), y en su noción de verdad solo `nil` y `false` son falsos.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let pos = n > 0
let par = n % 2 = 0
printfn "positivo=%b par=%b ambos=%b" pos par (pos && par)
```

### VB.NET

```vbnet
Module Booleanos
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim pos = n > 0
        Dim par = (n Mod 2 = 0)
        ' AndAlso cortocircuita; And evalúa siempre los dos lados.
        ' Boolean.ToString() devuelve "True", así que hay que bajarlo a minúsculas.
        Console.WriteLine("positivo={0} par={1} ambos={2}",
            pos.ToString().ToLowerInvariant(),
            par.ToString().ToLowerInvariant(),
            (pos AndAlso par).ToString().ToLowerInvariant())
    End Sub
End Module
```

**Qué reconocer:** los tres comparten el `System.Boolean` del CLR, y ahí aparece la trampa: su
`ToString()` devuelve `"True"` con mayúscula, no `"true"`. C# la esquiva porque la interpolación de
`bool` también da `"True"` y hay que corregirla igual; F# la esquiva con `%b`, que imprime en
minúsculas. VB.NET además distingue explícitamente **dos parejas de operadores**: `And`/`Or` evalúan
siempre los dos lados y `AndAlso`/`OrElse` cortocircuitan —una separación que la mayoría de lenguajes
esconde en un solo símbolo—. F# marca la otra frontera: usa `=` para comparar (no `==`) porque `=`
ya no significa asignar.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin tipo booleano real hasta C99, y arrastrando la
costumbre de tratar cualquier entero como condición.

### C++

```cpp
#include <iostream>

int main() {
    long n;
    std::cin >> n;
    const bool pos = n > 0;
    const bool par = n % 2 == 0;
    std::cout << std::boolalpha
              << "positivo=" << pos
              << " par=" << par
              << " ambos=" << (pos && par) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

static const char *tf(BOOL x) { return x ? "true" : "false"; }

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        BOOL pos = n > 0;
        BOOL par = n % 2 == 0;
        printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par));
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C y heredan su regla: **cero es falso, cualquier otro
valor es verdadero**. C++ añade un `bool` de primera clase y el manipulador `std::boolalpha`, que
imprime `true`/`false` sin escribir el ternario. Objective-C se queda más cerca de C: su `BOOL` es
históricamente un `signed char`, así que sigue haciendo falta traducirlo a texto a mano. En los dos,
`&&` cortocircuita exactamente igual que en C, y ese es el punto que transfiere.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y estrictos:
aquí la condición **tiene** que ser un booleano.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    const pos = n > 0;
    const par = @rem(n, 2) == 0;
    try std.io.getStdOut().writer().print(
        "positivo={} par={} ambos={}\n",
        .{ pos, par, pos and par },
    );
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
let pos = n > 0
let par = n mod 2 == 0
echo "positivo=", pos, " par=", par, " ambos=", pos and par
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    const pos = n > 0;
    const par = n % 2 == 0;
    writefln("positivo=%s par=%s ambos=%s", pos, par, pos && par);
}
```

**Qué reconocer:** los tres imprimen `bool` como `true`/`false` sin ayuda, igual que Go y Rust. Zig
escribe los operadores lógicos con **palabras** (`and`, `or`, `!`) en vez de símbolos, y obliga a
elegir entre `@rem` (resto con el signo del dividendo, como C) y `@mod` (siempre no negativo): esa
decisión que otros lenguajes toman por ti, Zig te la pone en la mano. Nim también usa `and`, pero
—atención— ese `and` es lógico entre booleanos y **bit a bit** entre enteros; el compilador lo
resuelve por el tipo. D conserva `&&` de C con el mismo cortocircuito.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la verdad no es un valor que se guarda:
es que algo **se pueda demostrar**.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    ( N > 0        -> Pos = true ; Pos = false ),
    ( 0 =:= N mod 2 -> Par = true ; Par = false ),
    ( Pos == true, Par == true -> Ambos = true ; Ambos = false ),
    format("positivo=~w par=~w ambos=~w~n", [Pos, Par, Ambos]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni valores booleanos: un hecho o se deriva o no existe.
% (Aritmética en el estilo de Soufflé; el Datalog puro ni siquiera la tiene.)
n(4).

positivo(N) :- n(N), N > 0.
par(N)      :- n(N), N % 2 = 0.
ambos(N)    :- positivo(N), par(N).
```

**Qué reconocer:** en Prolog el `,` de una regla **es** la conjunción, y cortocircuita de forma
natural: si el primer objetivo falla, el segundo ni se intenta. Lo que Prolog no tiene es un `if`
imperativo; el `( Cond -> Entonces ; Si_no )` es una construcción de control sobre la resolución, y
el `->` descarta los puntos de elección de la condición. Datalog va más lejos todavía: no hay
booleanos, no hay negación libre y no hay salida —`ambos(4)` existe o no existe en el modelo, y
"falso" significa simplemente *no derivable* (hipótesis de mundo cerrado)—. Es la misma renuncia que
hace SQL cuando le describes el resultado en vez del recorrido, con el agravante de que SQL sí tiene
una tercera verdad: `NULL`.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: comparar, negar, conjuntar,
imprimir. Lo que cambia aquí no es la forma sino algo más profundo —**qué considera verdad cada
lenguaje**— y por eso esta clase es la que más sorpresas guarda al saltar de familia. Eso es lo
transferible.

⏮️ [Volver a la clase 057](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
