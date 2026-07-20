# 🧬 El mismo programa en las familias de lenguajes — Clase 093

> [⬅️ Volver a la clase 093](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —invertir una cadena— resuelto por los **primos**
de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra ASCII sin espacios
- **Salida** (stdout): `invertido=<la palabra al revés>`
- **Regla:** invertir la secuencia de caracteres

| stdin | esperado |
|---|---|
| `hola` | `invertido=aloh` |
| `Ada` | `invertido=adA` |
| `abc` | `invertido=cba` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En esta familia la cadena es un objeto con métodos propios, y casi siempre existe uno que hace el
trabajo entero.

### Ruby

```ruby
w = STDIN.gets.strip
puts "invertido=#{w.reverse}"
```

### Perl

```perl
chomp(my $w = <STDIN>);
print "invertido=", scalar reverse($w), "\n";
```

### Lua

```lua
local w = io.read("l")
print("invertido=" .. w:reverse())
```

### Tcl

```tcl
gets stdin w
puts "invertido=[string reverse [string trim $w]]"
```

### R

```r
w <- readLines("stdin", n = 1)
cat(sprintf("invertido=%s\n", paste(rev(strsplit(w, "")[[1]]), collapse = "")))
```

**Qué reconocer:** aquí se ve de golpe si la cadena es un **tipo con identidad propia** o solo una
secuencia disfrazada. Ruby y Lua la tratan como objeto y le piden `reverse` directamente. Perl la
trata como escalar: `reverse` es una función de lista, y hace falta `scalar` para forzarla al modo
cadena —el sigilo `$` manda sobre la operación—. Tcl es el extremo del *todo es cadena*: `string
reverse` no es un método sino un subcomando del comando `string`. R rompe el patrón porque no tiene
tipo carácter: hay que **descomponer** la cadena en un vector de un carácter cada uno, invertir el
vector y volver a pegarlo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final w = stdin.readLineSync()!.trim();
  print('invertido=${w.split('').reversed.join()}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la inversión.
package {
    public class Cadena {
        public static function invertir(w:String):String {
            return "invertido=" + w.split("").reverse().join("");
        }
    }
}
```

**Qué reconocer:** ninguno de los dos tiene un método `reverse` sobre `String`, igual que JavaScript.
El rodeo es siempre el mismo —`split` para convertir la cadena en **lista**, invertir la lista, `join`
para volver a cadena—, y delata que en esta familia la cadena es **inmutable** y solo el arreglo
admite reordenarse en sitio. Dart marca la diferencia con `reversed`, que devuelve una vista perezosa
en vez de mutar, mientras que el `reverse()` de ActionScript modifica el arreglo original.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos comparten la misma `java.lang.String`
inmutable; lo que cambia es qué añade cada lenguaje encima.

### Kotlin

```kotlin
fun main() {
    val w = readLine()!!.trim()
    println("invertido=${w.reversed()}")
}
```

### Scala

```scala
object Cadena extends App {
  val w = scala.io.StdIn.readLine().trim
  println(s"invertido=${w.reverse}")
}
```

### Groovy

```groovy
def w = System.in.newReader().readLine().trim()
println "invertido=${w.reverse()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(println (str "invertido=" (str/reverse (str/trim (read-line)))))
```

**Qué reconocer:** Java necesita `new StringBuilder(w).reverse().toString()` porque `String` no tiene
el método; los cuatro primos lo **añaden por fuera** sin tocar la clase original —extensión en Kotlin,
conversión implícita a `StringOps` en Scala, metaclase en Groovy, función libre en Clojure—. Es el
mismo objeto de la JVM visto con cuatro estrategias distintas para ampliarlo. Scala además revela que
para él la cadena **es una colección**: `reverse` es el mismo método que usarías sobre una lista.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let w = stdin.ReadLine().Trim()
let invertido = w.ToCharArray() |> Array.rev |> System.String
printfn "invertido=%s" invertido
```

### VB.NET

```vbnet
Module Cadena
    Sub Main()
        Dim w = Console.ReadLine().Trim()
        Dim c = w.ToCharArray()
        Array.Reverse(c)
        Console.WriteLine("invertido=" & New String(c))
    End Sub
End Module
```

**Qué reconocer:** los tres pasan por el mismo puente, `ToCharArray`, porque en el CLR `String` es
inmutable y `Char[]` no: la cadena hay que **abrirla** a arreglo para poder reordenarla. La diferencia
está en el estilo: `Array.Reverse` de VB.NET muta el arreglo en sitio y no devuelve nada, mientras
`Array.rev` de F# devuelve uno nuevo y deja intacto el original. Misma biblioteca base, dos contratos
opuestos sobre quién puede modificar qué.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí la cadena no es un tipo: es memoria contigua.

### C++

```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string w;
    std::cin >> w;
    std::reverse(w.begin(), w.end());
    std::cout << "invertido=" << w << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *entrada = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] availableData]
                encoding:NSUTF8StringEncoding];
        NSString *w = [entrada stringByTrimmingCharactersInSet:
            [NSCharacterSet whitespaceAndNewlineCharacterSet]];
        NSMutableString *r = [NSMutableString stringWithCapacity:w.length];
        for (NSInteger i = (NSInteger)w.length - 1; i >= 0; i--) {
            [r appendFormat:@"%C", [w characterAtIndex:i]];
        }
        printf("invertido=%s\n", r.UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** en C la cadena es un `char*` terminado en `\0` y se invierte intercambiando bytes
con dos índices. C++ conserva ese modelo pero lo envuelve en `std::string`, que **sabe su longitud**
—por eso `w.begin()` y `w.end()` bastan y `std::reverse` es el mismo algoritmo genérico que usarías
sobre un `vector`—. Objective-C se va al otro extremo: `NSString` es un objeto con codificación
explícita, y la distinción entre `NSString` y `NSMutableString` está en el **tipo**, no en la
disciplina del programador.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y muy conscientes de que una cadena son bytes.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const w = std.mem.trim(u8, linea, " \r\t");
    const out = std.io.getStdOut().writer();
    try out.writeAll("invertido=");
    var i: usize = w.len;
    while (i > 0) : (i -= 1) try out.writeByte(w[i - 1]);
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/strutils

let w = stdin.readLine().strip()
var r = newStringOfCap(w.len)
for i in countdown(w.high, 0):
  r.add(w[i])
echo "invertido=", r
```

### D

```d
import std.stdio, std.string, std.algorithm;

void main() {
    auto w = readln().strip().dup;
    w.reverse();
    writeln("invertido=", w);
}
```

**Qué reconocer:** los tres dicen en voz alta lo que Python esconde: una cadena es un **arreglo de
bytes** y `w[i]` devuelve un byte, no un carácter. Zig ni siquiera construye la cadena invertida —la
escribe byte a byte al flujo de salida, sin reservar memoria—; Nim pide la capacidad por adelantado
con `newStringOfCap` para no reasignar; D necesita `.dup` porque `readln` devuelve una cadena
inmutable y `reverse` exige un `char[]` mutable. Esa es la razón por la que en esta familia invertir
texto **no ASCII** rompe: hay que decidir si se invierten bytes, puntos de código o grafemas, y ningún
lenguaje lo decide por ti.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
recorrerlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    string_chars(Linea, Cs),
    reverse(Cs, Rs),
    string_chars(Invertido, Rs),
    format("invertido=~w~n", [Invertido]).
```

### Datalog

```datalog
% Datalog puro no tiene cadenas ni recursión sobre caracteres: se declara la posición
% de cada carácter como un hecho y la regla invierte el índice.
letra(1, "h").
letra(2, "o").
letra(3, "l").
letra(4, "a").
largo(4).

invertida(J, C) :- letra(I, C), largo(N), J = N - I + 1.
```

**Qué reconocer:** `string_chars` es reversible —el mismo predicado descompone la cadena en lista y la
reconstruye según qué argumento venga sin ligar—, algo que ninguna función de las familias anteriores
puede hacer. Datalog muestra el límite del enfoque declarativo aplicado a texto: sin recursión sobre
la estructura de la cadena, la única forma de hablar de "orden" es **declararlo como dato**, exactamente
igual que SQL, que necesita una columna de posición o un CTE recursivo porque una tabla no tiene orden
propio.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que cada uno responde distinto: **¿qué es una
cadena?** Un objeto con métodos, una colección de caracteres, un arreglo de bytes, una lista de
símbolos o una relación de posiciones. La sintaxis se olvida; esa decisión de diseño no.

⏮️ [Volver a la clase 093](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
