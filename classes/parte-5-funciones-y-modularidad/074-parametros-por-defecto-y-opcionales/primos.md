# 🧬 El mismo programa en las familias de lenguajes — Clase 074

> [⬅️ Volver a la clase 074](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una potencia cuyo exponente vale 2 si no lo
escribes— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `base` o bien `base exp`
- **Salida** (stdout): `resultado=<base^exp>`
- **Regla:** `potencia(base, exp = 2)`; si la línea trae un solo número, el exponente es 2

| stdin | esperado |
|---|---|
| `3` | `resultado=9` |
| `2 3` | `resultado=8` |
| `5` | `resultado=25` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El defecto vive en la **definición** de la función, no en cada llamada: quien llama puede olvidarse
de que el segundo parámetro existe.

### Ruby

```ruby
def potencia(base, exp = 2)
  base**exp
end

t = STDIN.gets.split.map(&:to_i)
puts "resultado=#{t.size > 1 ? potencia(t[0], t[1]) : potencia(t[0])}"
```

### Perl

```perl
sub potencia {
    my ($base, $exp) = @_;
    $exp //= 2;   # sin lista de parámetros no hay defectos: se rellena a mano sobre @_
    return $base ** $exp;
}

my @t = split ' ', <STDIN>;
printf "resultado=%d\n", potencia(@t);
```

### Lua

```lua
local function potencia(base, exp)
  exp = exp or 2  -- los argumentos que faltan llegan como nil; los que sobran se ignoran
  local r = 1
  for _ = 1, exp do r = r * base end
  return r
end

local nums = {}
for s in io.read("l"):gmatch("%S+") do nums[#nums + 1] = tonumber(s) end
print("resultado=" .. potencia(nums[1], nums[2]))
```

### Tcl

```tcl
proc potencia {base {exp 2}} {
    return [expr {$base ** $exp}]
}

gets stdin linea
puts "resultado=[potencia {*}[regexp -all -inline {\S+} $linea]]"
```

### R

```r
potencia <- function(base, exp = 2) base^exp

v <- scan("stdin", what = integer(), quiet = TRUE)
r <- if (length(v) > 1) potencia(v[1], v[2]) else potencia(v[1])
cat(sprintf("resultado=%d\n", as.integer(r)))
```

**Qué reconocer:** Ruby, Tcl y R escriben el defecto **en la firma**, igual que Python; Tcl lo hace
con su sintaxis de llaves (`{exp 2}`), que es la misma lista de parámetros de siempre con un elemento
de dos partes. Los otros dos revelan lo que hay debajo. Lua no tiene defectos porque no tiene control
de aridad: si faltan argumentos los rellena con `nil` y si sobran los tira, así que el defecto es un
`or` en la primera línea del cuerpo. Perl ni siquiera tiene parámetros —todo llega en `@_`—, por eso
`potencia(@t)` funciona igual con uno o con dos elementos: el array se aplana en la llamada y el
`//=` decide si faltó algo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

// Los corchetes marcan el parámetro posicional opcional.
int potencia(int base, [int exp = 2]) {
  var r = 1;
  for (var i = 0; i < exp; i++) r *= base;
  return r;
}

void main() {
  final t = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: se ilustra el parámetro por defecto.
package {
    public class Calculo {
        public static function potencia(base:int, exp:int = 2):int {
            var r:int = 1;
            for (var i:int = 0; i < exp; i++) r *= base;
            return r;
        }
    }
}
```

**Qué reconocer:** ActionScript escribe `exp:int = 2` exactamente igual que JavaScript moderno y
TypeScript, porque los tres descienden del mismo borrador de ECMAScript 4. Dart introduce una
distinción que el resto de la familia no tiene: un parámetro opcional es **posicional** si va entre
corchetes `[...]` y **nombrado** si va entre llaves `{...}`, y hay que elegir una de las dos formas al
declarar la función.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java **no tiene** parámetros por defecto: los
simula con sobrecarga, y el resto de la familia arregla justo eso.

### Kotlin

```kotlin
fun potencia(base: Long, exp: Int = 2): Long {
    var r = 1L
    repeat(exp) { r *= base }
    return r
}

fun main() {
    val t = readLine()!!.trim().split(Regex("\\s+"))
    val base = t[0].toLong()
    println("resultado=" + if (t.size > 1) potencia(base, t[1].toInt()) else potencia(base))
}
```

### Scala

```scala
object Calculo {
  def potencia(base: Long, exp: Int = 2): Long =
    (1 to exp).foldLeft(1L)((acc, _) => acc * base)

  def main(args: Array[String]): Unit = {
    val t = scala.io.StdIn.readLine().trim.split("\\s+")
    val base = t(0).toLong
    val r = if (t.length > 1) potencia(base, t(1).toInt) else potencia(base)
    println(s"resultado=$r")
  }
}
```

### Groovy

```groovy
def potencia(base, exp = 2) { base ** exp }

def t = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "resultado=${t.size() > 1 ? potencia(t[0], t[1]) : potencia(t[0])}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure no tiene defectos: tiene múltiples aridades, y la corta llama a la larga.
(defn potencia
  ([base] (potencia base 2))
  ([base exp] (reduce * 1 (repeat exp base))))

(let [t (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "resultado=" (apply potencia t))))
```

**Qué reconocer:** Kotlin, Scala y Groovy escriben `exp: Int = 2` y el compilador genera por dentro
las llamadas que Java tendría que escribir a mano. Clojure elige la otra salida y la hace explícita:
una `defn` con dos cuerpos, uno por aridad, donde el de un argumento delega en el de dos. Es
literalmente la sobrecarga de Java —el mismo truco que usa la implementación Java de la clase—, solo
que dentro de una sola definición y sin tipos que la distingan. Groovy, además, tiene `**` como
operador de potencia; en Java hay que llamar a `Math.pow`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System

// En F# los valores por defecto solo existen en miembros de tipo, no en funciones `let`.
type Calculo =
    static member Potencia(valor: int, ?exp: int) =
        let e = defaultArg exp 2
        pown valor e

[<EntryPoint>]
let main _ =
    let t = Console.ReadLine().Trim().Split(' ')
    let b = int t.[0]
    let r = if t.Length > 1 then Calculo.Potencia(b, int t.[1]) else Calculo.Potencia(b)
    printfn "resultado=%d" r
    0
```

### VB.NET

```vbnet
Module Programa
    Function Potencia(valor As Integer, Optional exp As Integer = 2) As Long
        Dim r As Long = 1
        For i = 1 To exp
            r *= valor
        Next
        Return r
    End Function

    Sub Main()
        Dim t = Console.ReadLine().Trim().Split(" "c)
        Dim b = Integer.Parse(t(0))
        Dim r = If(t.Length > 1, Potencia(b, Integer.Parse(t(1))), Potencia(b))
        Console.WriteLine("resultado=" & r)
    End Sub
End Module
```

**Qué reconocer:** VB.NET marca el parámetro con la palabra `Optional`, un requisito que C# eliminó
al copiar la idea en su versión 4.0. F# es el caso interesante: sus funciones `let` **no admiten**
valores por defecto, solo los miembros de un tipo, y el mecanismo es distinto —`?exp` convierte el
parámetro en un `int option` y `defaultArg` decide qué hacer si llegó `None`—. Es el defecto tratado
como lo que realmente es: un valor que puede faltar.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C **no tiene** parámetros por defecto y la clase lo
resuelve pasando siempre el exponente.

### C++

```cpp
#include <iostream>
#include <sstream>
#include <string>

long potencia(long base, int exp = 2) {
    long r = 1;
    for (int i = 0; i < exp; ++i) r *= base;
    return r;
}

int main() {
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream in(linea);
    long base;
    int exp;
    in >> base;
    std::cout << "resultado=" << ((in >> exp) ? potencia(base, exp) : potencia(base)) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Calculadora : NSObject
+ (long)potencia:(long)base;
+ (long)potencia:(long)base exponente:(int)exp;
@end

@implementation Calculadora
+ (long)potencia:(long)base {
    return [self potencia:base exponente:2];  // sin defectos: otro selector que delega
}

+ (long)potencia:(long)base exponente:(int)exp {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= base;
    return r;
}
@end

int main(void) {
    @autoreleasepool {
        long base;
        int exp;
        int leidos = scanf("%ld %d", &base, &exp);
        if (leidos < 1) return 1;
        long r = leidos == 2 ? [Calculadora potencia:base exponente:exp]
                             : [Calculadora potencia:base];
        printf("resultado=%ld\n", r);
    }
    return 0;
}
```

**Qué reconocer:** aquí los dos superconjuntos de C se separan. C++ **sí** añadió argumentos por
defecto —con la regla de que todos los que los tengan deben ir al final— y el valor se sustituye en
el punto de llamada, en compilación. Objective-C no los tiene y no puede tenerlos: como el nombre del
método se parte entre los argumentos, quitar un argumento cambia el nombre del método. Por eso
`potencia:` y `potencia:exponente:` son **dos selectores distintos**, y el corto delega en el largo,
que es el patrón de "inicializador designado" de todo Cocoa.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ninguno de los dos tiene
parámetros por defecto, y es una decisión deliberada.

### Zig

```zig
const std = @import("std");

// Zig no tiene parámetros por defecto: se declara una función que delega.
fn potencia(base: i64, exp: u32) i64 {
    var r: i64 = 1;
    var i: u32 = 0;
    while (i < exp) : (i += 1) r *= base;
    return r;
}

fn cuadrado(base: i64) i64 {
    return potencia(base, 2);
}

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r");
    const base = try std.fmt.parseInt(i64, it.next().?, 10);
    const r = if (it.next()) |t| potencia(base, try std.fmt.parseInt(u32, t, 10)) else cuadrado(base);
    try std.io.getStdOut().writer().print("resultado={d}\n", .{r});
}
```

### Nim

```nim
import std/strutils

proc potencia(base: int, exp: int = 2): int =
  result = 1
  for _ in 1 .. exp:
    result *= base

let t = stdin.readLine().splitWhitespace()
let b = parseInt(t[0])
echo "resultado=", (if t.len > 1: potencia(b, parseInt(t[1])) else: potencia(b))
```

### D

```d
import std.stdio, std.array, std.conv, std.string;

long potencia(long base, int exp = 2) {
    long r = 1;
    foreach (_; 0 .. exp) r *= base;
    return r;
}

void main() {
    auto t = readln().strip().split();
    const b = t[0].to!long;
    writefln("resultado=%d", t.length > 1 ? potencia(b, t[1].to!int) : potencia(b));
}
```

**Qué reconocer:** Nim y D heredan los argumentos por defecto de C++ y los escriben igual. Zig los
rechaza por el mismo motivo que Go y Rust: un defecto es información que **no** se ve en el punto de
llamada, y estos lenguajes prefieren que leer `cuadrado(base)` diga la verdad completa sin ir a
buscar la firma. Fíjate además en el `result` de Nim: es una variable implícita, ya inicializada, que
la función devuelve al terminar sin escribir `return`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql).

### Prolog

```prolog
:- initialization(main, main).

% potencia/2 y potencia/3 son predicados DISTINTOS: la aridad es parte de la identidad.
% El "defecto" es una cláusula de aridad menor que llama a la mayor.
potencia(Base, R) :- potencia(Base, 2, R).
potencia(Base, Exp, R) :- R is Base ^ Exp.

resultado([Base], R) :- potencia(Base, R).
resultado([Base, Exp], R) :- potencia(Base, Exp, R).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Limpios),
    maplist([S, N]>>number_string(N, S), Limpios, Nums),
    resultado(Nums, R),
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene funciones, ni parámetros, ni valores por defecto, ni potencias.
% Lo más cercano: un hecho que fija el exponente y una regla por cada forma de la entrada.
entrada(3).
entrada_con_exp(2, 3).
exp_por_defecto(2).

potencia_pedida(B, E) :- entrada(B), exp_por_defecto(E).
potencia_pedida(B, E) :- entrada_con_exp(B, E).
```

**Qué reconocer:** Prolog hace visible lo que el resto esconde. `potencia/2` y `potencia/3` no son
"la misma función con un argumento opcional": son **dos predicados sin ninguna relación** para el
motor, y el enlace entre ellos existe solo porque lo escribimos como una cláusula que llama a la
otra. Esa es exactamente la sobrecarga de Java y las aridades de Clojure, pero aquí la aridad no es
un detalle de resolución sino parte del nombre. Datalog, sin aritmética ni efectos, solo puede
declarar el defecto como un hecho más de la base de conocimiento.

---

## Y de vuelta a la clase

Veinte lenguajes y tres estrategias que se reparten entre ellos: el defecto **en la firma** (Python,
Ruby, Kotlin, C++, Nim…), el defecto **en el cuerpo** cuando el lenguaje no controla la aridad
(Perl, Lua), y el defecto **como otra función** cuando la aridad es sagrada (Java, Clojure,
Objective-C, Prolog). Reconocer cuál de las tres estás leyendo es lo transferible.

⏮️ [Volver a la clase 074](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
