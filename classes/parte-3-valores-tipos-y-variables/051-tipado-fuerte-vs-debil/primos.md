# 🧬 El mismo programa en las familias de lenguajes — Clase 051

> [⬅️ Volver a la clase 051](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar un número consigo mismo y concatenarlo
consigo mismo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `suma=<n+n> texto=<n concatenado consigo mismo>`
- **Regla:** `suma = n + n`; `texto` es la representación textual de `n` repetida dos veces

| stdin | esperado |
|---|---|
| `5` | `suma=10 texto=55` |
| `3` | `suma=6 texto=33` |
| `12` | `suma=24 texto=1212` |

Este es el problema que mejor separa **fuerte** de **débil**: el mismo valor tiene que comportarse
como número en un sitio y como texto en el otro. Lo interesante no es el resultado, sino **cuánto
trabajo pide cada lenguaje** para conseguir las dos cosas.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí viven los dos extremos: Python es dinámico pero **fuerte** (`1 + "1"` es un error), y PHP es
dinámico y **débil** (`1 + "1"` vale `2`).

### Ruby

```ruby
n = STDIN.gets.to_i
# Ruby es fuerte: `n + n.to_s` lanzaría TypeError. La conversión se escribe.
puts "suma=#{n + n} texto=#{n.to_s + n.to_s}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
# El caso extremo de tipado débil: el escalar no tiene tipo, lo elige el OPERADOR.
# `+` lo lee como número; `.` lo lee como texto. Nunca hay que convertir nada.
printf "suma=%d texto=%s\n", $n + $n, $n . $n;
```

### Lua

```lua
local n = io.read("n")
-- Lua coacciona en las dos direcciones: número en `..` y cadena en aritmética.
print(string.format("suma=%d texto=%s", n + n, n .. n))
```

### Tcl

```tcl
gets stdin n
# En Tcl *todo* es cadena: concatenar es simple yuxtaposición y para sumar
# hay que pedir explícitamente una evaluación aritmética con `expr`.
puts "suma=[expr {$n + $n}] texto=$n$n"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("suma=%d texto=%s\n", n + n, paste0(n, n)))
```

**Qué reconocer:** los cinco son dinámicos, pero se reparten en toda la escala de fuerza. Ruby y R
son fuertes: exigen `to_s` / `paste0` para tratar el número como texto. Perl, Lua y Tcl son débiles y
lo son de tres maneras distintas —Perl deja que el operador decida, Lua coacciona en ambos sentidos,
Tcl parte de que todo es cadena y sube a número solo bajo `expr`—. **Dinámico y débil no son
sinónimos**, y esta familia lo demuestra ella sola.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia del `+` sobrecargado: suma si los dos lados son números, concatena si alguno es texto.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  // Dart corrigió el `+` de JavaScript: `n + '$n'` no compila.
  print('suma=${n + n} texto=$n$n');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
    // Conserva el `+` ambiguo de ECMAScript: con un operando String, concatena.
    public class Fuerza {
        public static function linea(n:int):String {
            return "suma=" + (n + n) + " texto=" + (String(n) + String(n));
        }
    }
}
```

**Qué reconocer:** ActionScript 3 hereda el `+` ambiguo de ECMAScript, con los mismos paréntesis
defensivos alrededor de `n + n` que hacen falta en JavaScript. Dart rompió con esa herencia: aunque
la sintaxis se parece, su `+` es **fuerte** y solo suma números. TypeScript se queda en medio —marca
el error al compilar, pero el JavaScript generado sigue concatenando en tiempo de ejecución—.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Una familia fuerte, con una única grieta
famosa: el `+` de `String`.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    // `n + "$n"` no compila: Int no tiene un `plus(String)`.
    println("suma=${n + n} texto=$n$n")
}
```

### Scala

```scala
object Fuerza extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"suma=${n + n} texto=$n$n")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
// Groovy relaja la regla: `'a' + 1` concatena y `1 + '1'` falla. La asimetría es suya.
println "suma=${n + n} texto=${n.toString() + n}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Long/parseLong (str/trim (read-line)))]
  ;; `(+ 1 "1")` lanza ClassCastException: fuerte, pero comprobado en ejecución.
  (println (str "suma=" (+ n n) " texto=" n n)))
```

**Qué reconocer:** los cuatro son fuertes, y se nota en que ninguno suma un número con una cadena.
Pero cambia **cuándo** te lo dicen: Kotlin y Scala en el compilador, Clojure al ejecutar. Clojure
además evita el problema de raíz separando los operadores —`+` solo suma, `str` solo concatena—, la
misma solución que adoptaron los lenguajes de sistemas. Groovy es la oveja negra: reintroduce a
propósito parte de la debilidad para parecerse a un lenguaje de scripting.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
// F# es el más fuerte del atlas: ni siquiera `1 + 1.0` compila, y `+` con
// una cadena tampoco. Todo cruce de tipos pasa por una conversión escrita.
printfn "suma=%d texto=%s" (n + n) (string n + string n)
```

### VB.NET

```vbnet
Module Fuerza
    Sub Main()
        ' Con Option Strict Off, VB.NET convierte solo: "5" + 5 da 10.
        ' Por eso el operador de concatenación canónico es `&`, no `+`:
        ' `&` siempre significa texto y no deja lugar a la ambigüedad.
        Dim n As Integer = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("suma=" & (n + n) & " texto=" & n.ToString() & n.ToString())
    End Sub
End Module
```

**Qué reconocer:** el CLR es fuerte por debajo, pero cada lenguaje decide cuánta debilidad ofrece
encima. F# no ofrece ninguna. VB.NET arrastra la de sus antepasados BASIC y por eso inventó un
operador aparte, `&`, para que concatenar nunca se confunda con sumar. C# se queda en el medio, con
`+` sobrecargado para `string` igual que Java.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Estático y, en teoría, tipado; en la práctica, con
un agujero enorme llamado *cast*.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    int n;
    std::cin >> n;
    // `+` sobre std::string concatena, pero por SOBRECARGA de operador,
    // no por coerción: los tipos siguen comprobándose uno a uno.
    const std::string s = std::to_string(n);
    std::cout << "suma=" << n + n << " texto=" << s + s << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        NSString *s = [NSString stringWithFormat:@"%d", n];
        NSString *texto = [s stringByAppendingString:s];
        printf("suma=%d texto=%s\n", n + n, [texto UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** en C concatenar dos números sería copiar bytes a mano, y por eso los dos primos
resuelven la mitad textual con un tipo aparte —`std::string`, `NSString`—. C++ consigue escribir
`s + s` sin debilitar nada: es una **sobrecarga** resuelta al compilar, no una conversión implícita.
Objective-C ni siquiera intenta sobrecargar `+` y pide el mensaje `stringByAppendingString:`, mucho
más verboso pero imposible de confundir con una suma.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia que decidió
que la mejor forma de evitar la ambigüedad es **no reutilizar el mismo símbolo**.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    // Zig no tiene sobrecarga de operadores: `+` solo suma números.
    // El texto se construye siempre por formateo.
    try std.io.getStdOut().writer().print("suma={d} texto={d}{d}\n", .{ n + n, n, n });
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
# `+` suma, `&` concatena, `$` convierte a texto. Tres operadores, cero ambigüedad.
echo "suma=", n + n, " texto=", $n & $n
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    int n = readln().strip().to!int;
    string s = n.to!string;
    // D reservó `~` para concatenar precisamente para que `+` no tuviera que decidir.
    writefln("suma=%d texto=%s", n + n, s ~ s);
}
```

**Qué reconocer:** los tres separan los operadores —`&` en Nim, `~` en D, solo formateo en Zig— y
exigen una conversión escrita (`$`, `to!string`) para pasar de número a texto. Es la misma postura
que Rust con `to_string()` y que Go con `strconv`. Cuando un lenguaje quiere ser fuerte de verdad, lo
primero que hace es dejar de reutilizar el signo `+`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL es notoriamente débil —compara y suma entre
tipos distintos con reglas de conversión propias de cada motor—, y sus primos van en la dirección
contraria.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    % `is` evalúa aritmética; nunca concatena. Y el texto se construye
    % con predicados aparte: los dos mundos jamás se tocan.
    Suma is N + N,
    format(string(S), "~w", [N]),
    string_concat(S, S, Texto),
    format("suma=~w texto=~w~n", [Suma, Texto]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni concatenación de cadenas: solo hechos y reglas
% con aritmética sobre los términos. Se muestra la mitad numérica del contrato.
entrada(5).

suma(S) :- entrada(N), S = N + N.
```

**Qué reconocer:** en Prolog el término `5` y el término `"5"` son cosas distintas que nunca se
convierten solas: hay un predicado para cada travesía (`number_string`, `string_concat`). Eso lo hace
**fuerte** aunque no declare tipos, que es justo la combinación que Python también encarna. Y es el
contraste exacto con SQL, donde `'5' + 5` puede dar `10`, un error o `'55'` según el motor.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los ordena de punta a punta: **¿el lenguaje
convierte por ti o te obliga a escribir la conversión?** Perl y Tcl están en un extremo, F# y Zig en
el otro, y en medio cabe casi todo lo que usarás en tu vida profesional. Eso es lo transferible.

⏮️ [Volver a la clase 051](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
