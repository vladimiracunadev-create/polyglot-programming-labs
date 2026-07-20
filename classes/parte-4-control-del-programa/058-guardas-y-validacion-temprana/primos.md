# 🧬 El mismo programa en las familias de lenguajes — Clase 058

> [⬅️ Volver a la clase 058](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —clasificar una edad rechazando primero lo
inválido— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `edad`
- **Salida** (stdout): `invalido`, `menor` o `adulto`
- **Regla (guardas, en orden):** `edad < 0` → `invalido`; `edad < 18` → `menor`; si no → `adulto`

| stdin | esperado |
|---|---|
| `-5` | `invalido` |
| `10` | `menor` |
| `20` | `adulto` |

El patrón que se transfiere no es el `if`: es **salir pronto**. Cada guarda descarta un caso y deja
el resto del cuerpo con una condición menos de la que preocuparse.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Funciones ligeras y `return` temprano sin ceremonia: el terreno natural de la cláusula de guarda.

### Ruby

```ruby
def clasificar(edad)
  return "invalido" if edad.negative?
  return "menor"    if edad < 18
  "adulto"
end

puts clasificar(STDIN.gets.to_i)
```

### Perl

```perl
sub clasificar {
    my ($edad) = @_;
    return "invalido" if $edad < 0;
    return "menor"    if $edad < 18;
    return "adulto";
}

chomp(my $edad = <STDIN>);
print clasificar($edad), "\n";
```

### Lua

```lua
local function clasificar(edad)
  if edad < 0 then return "invalido" end
  if edad < 18 then return "menor" end
  return "adulto"
end

print(clasificar(tonumber(io.read("l"))))
```

### Tcl

```tcl
proc clasificar {edad} {
    if {$edad < 0}  { return "invalido" }
    if {$edad < 18} { return "menor" }
    return "adulto"
}

gets stdin edad
puts [clasificar $edad]
```

### R

```r
clasificar <- function(edad) {
  if (edad < 0) return("invalido")
  if (edad < 18) return("menor")
  "adulto"
}

edad <- as.integer(readLines("stdin", n = 1))
cat(clasificar(edad), "\n", sep = "")
```

**Qué reconocer:** los cinco escriben la misma escalera de salidas tempranas, pero dos se separan del
grupo por la forma. Ruby y Perl tienen **modificadores de sentencia** (`return X if cond`), que ponen
la acción antes que la condición y hacen que la guarda se lea como una frase; Python no los tiene, y
ese es todo el motivo de que su versión ocupe una línea más. R delata su naturaleza funcional: el
`return()` es una **función**, no una palabra clave, y la última expresión del cuerpo ya es el valor
devuelto —por eso `"adulto"` va suelto—. Tcl mantiene la costumbre de la familia con llaves aunque
sus llaves no sean bloques sino texto sin evaluar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

String clasificar(int edad) {
  if (edad < 0) return 'invalido';
  if (edad < 18) return 'menor';
  return 'adulto';
}

void main() {
  print(clasificar(int.parse(stdin.readLineSync()!.trim())));
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra la función.
    public class Edad {
        public static function clasificar(edad:int):String {
            if (edad < 0) return "invalido";
            if (edad < 18) return "menor";
            return "adulto";
        }
    }
}
```

**Qué reconocer:** la forma es exactamente la de JavaScript, con el tipo de retorno declarado delante
como en TypeScript. La diferencia que importa para las guardas es que Dart y ActionScript **exigen
que todos los caminos devuelvan** un valor del tipo declarado: si borras el `return "adulto"` final,
el compilador te lo señala. En JavaScript esa misma omisión pasa desapercibida y la función devuelve
`undefined` en silencio; el analizador de TypeScript es el que reconstruye la garantía.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Misma máquina virtual; lo que cambia es si el
lenguaje piensa en sentencias o en expresiones.

### Kotlin

```kotlin
fun clasificar(edad: Int): String = when {
    edad < 0 -> "invalido"
    edad < 18 -> "menor"
    else -> "adulto"
}

fun main() = println(clasificar(readLine()!!.trim().toInt()))
```

### Scala

```scala
object Edad extends App {
  def clasificar(edad: Int): String =
    if (edad < 0) "invalido"
    else if (edad < 18) "menor"
    else "adulto"

  println(clasificar(scala.io.StdIn.readLine().trim.toInt))
}
```

### Groovy

```groovy
def clasificar(int edad) {
    if (edad < 0) return 'invalido'
    if (edad < 18) return 'menor'
    'adulto'
}

println clasificar(System.in.newReader().readLine().trim() as int)
```

### Clojure

```clojure
(defn clasificar [edad]
  (cond
    (neg? edad) "invalido"
    (< edad 18) "menor"
    :else       "adulto"))

(println (clasificar (Integer/parseInt (.trim (read-line)))))
```

**Qué reconocer:** los cuatro corren sobre la JVM, pero solo Groovy conserva el `return` temprano de
Java. Los otros tres **no lo necesitan**, y ahí está la lección: cuando la construcción condicional
es una expresión que ya devuelve un valor, la guarda deja de ser un salto y pasa a ser una rama.
Kotlin usa `when` sin sujeto —la forma idiomática de una cadena de condiciones—, Scala encadena
`if`/`else` como expresión, y Clojure escribe `cond`, donde `:else` no es palabra clave sino
simplemente una palabra clave que siempre es verdadera. Groovy, además, permite omitir el `return`
final y devolver la última expresión, como Ruby.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let clasificar edad =
    if edad < 0 then "invalido"
    elif edad < 18 then "menor"
    else "adulto"

stdin.ReadLine().Trim() |> int |> clasificar |> printfn "%s"
```

### VB.NET

```vbnet
Module Edad
    Function Clasificar(edad As Integer) As String
        If edad < 0 Then Return "invalido"
        If edad < 18 Then Return "menor"
        Return "adulto"
    End Function

    Sub Main()
        Console.WriteLine(Clasificar(Integer.Parse(Console.ReadLine().Trim())))
    End Sub
End Module
```

**Qué reconocer:** VB.NET es C# con otra piel: `Return` temprano, tipo de retorno declarado, misma
escalera. F# rompe con la familia en algo esencial: **no tiene `return`**. Una función es una
expresión y su valor es el de la última expresión evaluada, de modo que la guarda no puede
implementarse como una salida anticipada —tiene que escribirse como el primer brazo de un
condicional—. Y como todo condicional debe tener el mismo tipo en ambas ramas, el `else` final no es
opcional: omitirlo es un error de compilación, no un descuido silencioso.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La guarda nació aquí, y no por elegancia: por
supervivencia frente a los punteros nulos y los códigos de error.

### C++

```cpp
#include <iostream>
#include <string>

std::string clasificar(long edad) {
    if (edad < 0) return "invalido";
    if (edad < 18) return "menor";
    return "adulto";
}

int main() {
    long edad;
    std::cin >> edad;
    std::cout << clasificar(edad) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

static NSString *clasificar(long edad) {
    if (edad < 0) return @"invalido";
    if (edad < 18) return @"menor";
    return @"adulto";
}

int main(void) {
    @autoreleasepool {
        long edad;
        if (scanf("%ld", &edad) != 1) return 1;
        printf("%s\n", clasificar(edad).UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** el `if (cond) return X;` de C aparece intacto en los dos. El detalle que separa a
las familias es qué ocurre **después** del `return`: en C++ el objeto local se destruye solo al salir
por cualquier camino (RAII), lo que hace seguro tener varias salidas; en C puro, cada `return`
temprano es un punto donde alguien puede olvidarse de liberar memoria, y por eso el `goto cleanup`
del núcleo Linux sigue siendo la guarda idiomática de C. Objective-C está en medio: el
`@autoreleasepool` recoge lo que se creó dentro, salgas por donde salgas.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go convirtió la guarda
en su estilo de casa (`if err != nil { return }`) y Rust la escondió dentro del operador `?`.

### Zig

```zig
const std = @import("std");

fn clasificar(edad: i64) []const u8 {
    if (edad < 0) return "invalido";
    if (edad < 18) return "menor";
    return "adulto";
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const edad = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("{s}\n", .{clasificar(edad)});
}
```

### Nim

```nim
import std/strutils

proc clasificar(edad: int): string =
  if edad < 0: return "invalido"
  if edad < 18: return "menor"
  "adulto"

echo clasificar(stdin.readLine().strip().parseInt())
```

### D

```d
import std.stdio, std.conv, std.string;

string clasificar(long edad) {
    if (edad < 0) return "invalido";
    if (edad < 18) return "menor";
    return "adulto";
}

void main() {
    writeln(clasificar(readln().strip().to!long));
}
```

**Qué reconocer:** los tres escriben la guarda igual que C, y los tres han añadido herramientas para
que salir pronto **no deje basura detrás**: Zig y D tienen `defer` / `scope(exit)` —código que se
ejecuta al abandonar el ámbito por el camino que sea—, y Nim tiene `defer` y destructores. Es la
misma preocupación que resuelve `try` en Zig y `?` en Rust: una guarda sobre un error que además
libera lo que había. Nim se separa en la superficie con su bloque por indentación y con la última
expresión como valor de retorno, al estilo de Ruby.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí no hay "salir pronto" porque no hay un
recorrido del que salir: hay reglas que se prueban.

### Prolog

```prolog
:- initialization(main, main).

% El corte (!) es la guarda: fija esta cláusula y prohíbe probar las siguientes.
clasificar(Edad, invalido) :- Edad < 0, !.
clasificar(Edad, menor)    :- Edad < 18, !.
clasificar(_,    adulto).

main :-
    read_line_to_string(user_input, Linea),
    number_string(Edad, Linea),
    clasificar(Edad, Etiqueta),
    format("~w~n", [Etiqueta]).
```

### Datalog

```datalog
% Datalog no tiene E/S, ni corte, ni orden entre cláusulas: no existe el "si no".
% Cada regla debe llevar su condición completa y ser mutuamente excluyente.
edad(10).

clasificacion(E, "invalido") :- edad(E), E < 0.
clasificacion(E, "menor")    :- edad(E), E >= 0, E < 18.
clasificacion(E, "adulto")   :- edad(E), E >= 18.
```

**Qué reconocer:** Prolog es el pariente más cercano de la guarda que se puede encontrar fuera de la
familia imperativa: las cláusulas se prueban **en orden** y el corte `!` dice "hasta aquí, no
retrocedas", que es literalmente el `return` temprano de esta clase. Datalog demuestra el precio de
renunciar a ese orden: sin corte y sin secuencia, la exclusión mutua hay que **escribirla** —fíjate
en el `E >= 0` de la segunda regla, redundante en todos los demás lenguajes de esta página y
obligatorio aquí—. SQL vive en el mismo mundo, y por eso su `CASE WHEN` sí evalúa las condiciones en
orden: fue la concesión que tuvo que hacer.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una misma idea: **descarta lo imposible primero y el resto del
código respira**. Lo que cambia es si el lenguaje te deja salir de en medio (`return`), te obliga a
convertirlo en ramas de una expresión (F#, Clojure, Kotlin) o te quita hasta el orden entre reglas
(Datalog). Eso es lo transferible.

⏮️ [Volver a la clase 058](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
