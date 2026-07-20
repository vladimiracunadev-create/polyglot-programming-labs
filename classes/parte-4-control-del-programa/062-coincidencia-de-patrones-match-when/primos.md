# 🧬 El mismo programa en las familias de lenguajes — Clase 062

> [⬅️ Volver a la clase 062](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —clasificar el signo de un entero— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Rust, la de Scala te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `signo=<positivo|negativo|cero>`
- **Regla:** `n > 0 → positivo`; `n < 0 → negativo`; `n == 0 → cero`

| stdin | esperado |
|---|---|
| `5` | `signo=positivo` |
| `-3` | `signo=negativo` |
| `0` | `signo=cero` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Es la familia donde más se nota la diferencia: la coincidencia de patrones llegó tarde (o no llegó),
y cada lenguaje improvisó su propia solución con las piezas que ya tenía.

### Ruby

```ruby
n = STDIN.gets.to_i
signo = case n
        when 1..    then "positivo"
        when ..-1   then "negativo"
        else "cero"
        end
puts "signo=#{signo}"
```

### Perl

```perl
# Perl no tiene coincidencia de patrones sobre valores.
# El idioma de la comunidad es el operador de comparación numérica <=>,
# que devuelve exactamente -1, 0 o 1: el signo, ya clasificado.
my $n = <STDIN>;
chomp $n;
my %signo = (1 => 'positivo', -1 => 'negativo', 0 => 'cero');
printf "signo=%s\n", $signo{$n <=> 0};
```

### Lua

```lua
-- En Lua "patrón" significa patrón de texto (string.match): no existe
-- coincidencia estructural sobre valores. La cadena de if es lo idiomático.
local n = tonumber(io.read("l"))
local signo
if n > 0 then
    signo = "positivo"
elseif n < 0 then
    signo = "negativo"
else
    signo = "cero"
end
print("signo=" .. signo)
```

### Tcl

```tcl
# El switch de Tcl compara CADENAS (exacto, glob o regexp): no sabe de rangos
# numéricos, así que la clasificación se hace con expr.
gets stdin n
set signo [expr {$n > 0 ? "positivo" : ($n < 0 ? "negativo" : "cero")}]
puts "signo=$signo"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
# sign() reduce el valor a -1, 0 o 1, y switch() sobre una cadena
# sí admite ramas con nombre.
signo <- switch(as.character(sign(n)),
                "1"  = "positivo",
                "-1" = "negativo",
                "0"  = "cero")
cat(sprintf("signo=%s\n", signo))
```

**Qué reconocer:** de los cinco, solo Ruby distingue por **forma** y no por comparación: sus `when`
son rangos (`1..`, `..-1`) y el `case` los prueba con el operador `===`, el mismo mecanismo que
permitiría poner ahí una clase o una expresión regular. Los otros cuatro no tienen coincidencia de
patrones y lo confiesan con distintos disfraces: Perl y R **normalizan primero** el valor a −1/0/1 y
luego consultan una tabla; Lua encadena `if`; Tcl usa el operador ternario porque su `switch` solo
sabe de cadenas. Cuando un lenguaje carece del concepto, el problema no desaparece: se desplaza.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final signo = switch (n) {
    > 0 => 'positivo',
    < 0 => 'negativo',
    _ => 'cero',
  };
  print('signo=$signo');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin ni coincidencia de patrones.
// El truco clásico de la familia es switch(true): cada case es una condición.
package {
    public class Signo {
        public static function de(n:int):String {
            switch (true) {
                case n > 0: return "signo=positivo";
                case n < 0: return "signo=negativo";
                default:    return "signo=cero";
            }
        }
    }
}
```

**Qué reconocer:** ActionScript enseña el estado en el que sigue JavaScript: sin patrones, y con el
apaño de `switch (true)` para meter condiciones donde el lenguaje solo espera valores. Dart 3 es la
otra mitad de la historia —añadió **patrones relacionales** (`> 0`, `< 0`) y comodín `_` dentro de
una expresión `switch`—, y es exactamente la propuesta que JavaScript lleva años discutiendo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java añadió patrones tarde; sus primos
llevaban una década con ellos.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val signo = when {
        n > 0 -> "positivo"
        n < 0 -> "negativo"
        else -> "cero"
    }
    println("signo=$signo")
}
```

### Scala

```scala
object Signo extends App {
  val signo = scala.io.StdIn.readInt() match {
    case n if n > 0 => "positivo"
    case n if n < 0 => "negativo"
    case _          => "cero"
  }
  println(s"signo=$signo")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def signo
switch (n) {
    case { it > 0 }: signo = 'positivo'; break
    case { it < 0 }: signo = 'negativo'; break
    default: signo = 'cero'
}
println "signo=$signo"
```

### Clojure

```clojure
(let [n (Integer/parseInt (.trim (read-line)))
      signo (cond
              (pos? n) "positivo"
              (neg? n) "negativo"
              :else    "cero")]
  (println (str "signo=" signo)))
```

**Qué reconocer:** Scala es el que tiene coincidencia de patrones **de verdad**: el `case n if n > 0`
liga el valor a un nombre y le aplica una guarda, y el mismo `match` sabría descomponer una tupla,
una lista o una `case class` por su estructura. Kotlin recorta: su `when` sin sujeto es una cadena de
condiciones bien vestida, no un desestructurador. Groovy aprovecha que su `case` usa `isCase`, así
que una **clausura** funciona como patrón. Clojure elige `cond` en vez de `case` porque `case`
compara constantes por igualdad y aquí hacen falta comparaciones; su coincidencia estructural vive
aparte, en `core.match` y en la desestructuración de `let`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let signo =
    match int (stdin.ReadLine().Trim()) with
    | n when n > 0 -> "positivo"
    | n when n < 0 -> "negativo"
    | _ -> "cero"
printfn "signo=%s" signo
```

### VB.NET

```vbnet
Module Signo
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim signo As String
        Select Case n
            Case Is > 0 : signo = "positivo"
            Case Is < 0 : signo = "negativo"
            Case Else : signo = "cero"
        End Select
        Console.WriteLine("signo=" & signo)
    End Sub
End Module
```

**Qué reconocer:** el `match` de F# es el original del que C# copió sus *pattern matching
expressions*: mismo `when` para las guardas, mismo `_` como comodín, y un compilador que avisa si el
conjunto de casos no es exhaustivo. VB.NET no tiene patrones, pero su `Select Case` sí acepta
**relaciones y rangos** —`Case Is > 0`, `Case 1 To 10`—, algo que el `switch` de C nunca permitió.
Es un punto intermedio interesante: más expresivo que un `switch` clásico, menos que un `match`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí no hay patrones, y el `switch` solo compara
enteros con constantes: para clasificar por rango hay que bajar a los condicionales.

### C++

```cpp
#include <iostream>

int main() {
    int n;
    std::cin >> n;
    const char* signo = (n > 0) ? "positivo"
                      : (n < 0) ? "negativo"
                                : "cero";
    std::cout << "signo=" << signo << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        NSString *signo = n > 0 ? @"positivo" : (n < 0 ? @"negativo" : @"cero");
        printf("signo=%s\n", signo.UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** ninguno de los dos puede escribir `case > 0`, porque el `switch` de C exige
constantes enteras conocidas en compilación. La respuesta idiomática de la familia es el **operador
ternario encadenado**, que al menos conserva lo importante: sigue siendo una *expresión* que produce
un valor. C++ está incorporando la idea por partes —`std::visit` sobre `std::variant`, `if` con
inicializador, propuestas de `inspect`—, pero a día de hoy la coincidencia de patrones no es parte
del lenguaje.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust hizo del `match`
exhaustivo su sello de identidad; sus vecinos toman decisiones distintas.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    // std.math.order devuelve un enum de tres valores: el switch queda
    // exhaustivo sin necesidad de else, y el compilador lo comprueba.
    const signo = switch (std.math.order(n, 0)) {
        .gt => "positivo",
        .lt => "negativo",
        .eq => "cero",
    };
    try std.io.getStdOut().writer().print("signo={s}\n", .{signo});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
let signo =
  case n
  of low(int) .. -1: "negativo"
  of 0: "cero"
  else: "positivo"
echo "signo=", signo
```

### D

```d
import std.stdio, std.conv, std.string, std.math;

void main() {
    const n = readln().strip().to!int;
    string signo;
    // sgn() reduce el valor a -1, 0 o 1 para poder usar case con constantes.
    switch (sgn(n)) {
        case  1: signo = "positivo"; break;
        case -1: signo = "negativo"; break;
        default: signo = "cero";     break;
    }
    writefln("signo=%s", signo);
}
```

**Qué reconocer:** Zig y Nim sí distinguen por forma, cada uno a su manera. Zig no usa guardas:
convierte la comparación en un **enum de tres valores** y deja que el `switch` sea exhaustivo por
construcción —muy en su estilo de hacer visible lo que otros ocultan—. Nim admite **rangos** como
patrón (`low(int) .. -1`), que es más de lo que puede C pero menos que el `match` de Rust. D vuelve
al truco de normalizar con `sgn()` porque su `switch`, heredado de C, quiere constantes.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la coincidencia de patrones no es una
construcción del lenguaje: **es el motor de ejecución entero**.

### Prolog

```prolog
:- initialization(main, main).

signo(N, "positivo") :- N > 0, !.
signo(N, "negativo") :- N < 0, !.
signo(_, "cero").

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    signo(N, S),
    format("signo=~w~n", [S]).
```

### Datalog

```datalog
% Datalog no tiene E/S: la entrada se declara como un hecho.
% Las comparaciones en el cuerpo son extensión de dialectos prácticos
% (Soufflé, LogiQL); el Datalog puro solo une variables entre relaciones.
entrada(5).

signo("positivo") :- entrada(N), N > 0.
signo("negativo") :- entrada(N), N < 0.
signo("cero")     :- entrada(N), N = 0.
```

**Qué reconocer:** Prolog es, junto con Scala y F#, el que hace coincidencia de patrones **real** —y
la hace en la cabeza de la cláusula, antes de entrar en el cuerpo—. Las tres cláusulas de `signo/2`
se prueban en orden y la unificación decide cuál encaja; los `>` y `<` del cuerpo son las guardas, y
el `!` evita que el backtracking siga probando las siguientes tras haber encontrado respuesta. Sin
esos cortes, un `5` daría dos soluciones: `"positivo"` y también `"cero"`. Datalog conserva las tres
reglas pero pierde el orden: las evalúa **todas a la vez** hasta el punto fijo, así que la
exclusividad tiene que estar en las condiciones, no en la secuencia.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una línea divisoria muy nítida: los que distinguen por
**forma** —Scala, F#, Prolog, Dart 3, Rust— y los que solo saben comparar valores y tienen que
normalizar antes (Perl, R, D) o encadenar condiciones (Lua, C++, Tcl). Saber de qué lado está el
lenguaje que tienes delante es lo transferible.

⏮️ [Volver a la clase 062](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
