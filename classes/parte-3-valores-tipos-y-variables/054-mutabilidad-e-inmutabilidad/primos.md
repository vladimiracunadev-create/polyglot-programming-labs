# 🧬 El mismo programa en las familias de lenguajes — Clase 054

> [⬅️ Volver a la clase 054](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —construir la secuencia `1-2-...-n`— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir. Y aquí hay un premio extra:
construir una cadena por partes es el ejercicio que **delata** la postura de cada lenguaje frente a la
mutabilidad. Unos acumulan en un buffer que se modifica; otros no permiten modificar nada y producen
un valor nuevo en cada paso.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (con `n >= 1`)
- **Salida** (stdout): `sec=1-2-...-n`
- **Regla:** unir los números de `1` a `n` con el separador `-`

| stdin | esperado |
|---|---|
| `3` | `sec=1-2-3` |
| `1` | `sec=1` |
| `5` | `sec=1-2-3-4-5` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y estructuras mutables por defecto: la lista se llena a empujones y solo al final se
convierte en texto. La familia entera comparte ese gesto.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "sec=#{(1..n).to_a.join('-')}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
print "sec=", join('-', 1 .. $n), "\n";
```

### Lua

```lua
local n = tonumber(io.read("l"))
local partes = {}
for i = 1, n do
    partes[#partes + 1] = tostring(i)
end
print("sec=" .. table.concat(partes, "-"))
```

### Tcl

```tcl
gets stdin n
set partes {}
for {set i 1} {$i <= $n} {incr i} {
    lappend partes $i
}
puts "sec=[join $partes -]"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("sec=%s\n", paste(seq_len(n), collapse = "-")))
```

**Qué reconocer:** los cinco ofrecen un `join` / `concat` que evita concatenar la cadena una y otra
vez, porque en todos ellos las cadenas son **inmutables** y cada `+` crearía una copia nueva. Lo
mutable es el **contenedor**: la tabla de Lua y la lista de Tcl crecen en su sitio con `lappend` y
`#partes + 1`. Tcl es el caso más peculiar de la familia: al ser *todo cadena*, su "lista" es en
realidad texto con una representación interna de lista, y `join` funciona sobre esa doble naturaleza.
R vuelve a delatar su origen estadístico: no hay bucle ni acumulador, `seq_len(n)` **ya es** el vector
completo y `paste` lo colapsa de una vez.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final partes = List<int>.generate(n, (i) => i + 1);
  print('sec=${partes.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la construcción.
package {
    public class Secuencia {
        public static function construir(n:int):String {
            var partes:Array = [];
            for (var i:int = 1; i <= n; i++) {
                partes.push(i);
            }
            return "sec=" + partes.join("-");
        }
    }
}
```

**Qué reconocer:** `push` y `join` sobre un array son literalmente los mismos métodos de JavaScript;
`Array` en ActionScript es la clase de la que desciende el array de JS moderno. Dart marca la
diferencia con `final`: la **referencia** `partes` no se puede reasignar, pero la lista que hay detrás
sigue siendo mutable. Esa distinción —*el nombre está fijo, el contenido no*— es la misma que separa
`const` de un objeto congelado en JavaScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val n = readln().trim().toInt()
    println("sec=" + (1..n).joinToString("-"))
}
```

### Scala

```scala
object Secuencia extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  println("sec=" + (1 to n).mkString("-"))
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
println "sec=" + (1..n).join('-')
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Integer/parseInt (str/trim (read-line)))]
  (println (str "sec=" (str/join "-" (range 1 (inc n))))))
```

**Qué reconocer:** los cuatro heredan de Java la regla de que `String` es inmutable, y por eso los
cuatro tienen un rango (`1..n`, `1 to n`, `range`) que se colapsa de golpe en vez de un
`StringBuilder`. Kotlin y Scala hacen explícita la postura con `val`: un nombre que se liga una vez,
frente a `var`, que sí se reasigna. Clojure va mucho más lejos y no es solo una cuestión de estilo:
**no tiene variables reasignables en absoluto**. `let` liga un nombre a un valor dentro de su ámbito y
ahí se acaba; sus colecciones son persistentes, así que "añadir" siempre devuelve una estructura nueva
que comparte memoria con la anterior. Aquí no se nota el esfuerzo porque el problema no necesita
mutar nada, y ese es precisamente el argumento de Clojure.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let sec = [ 1 .. n ] |> List.map string |> String.concat "-"
printfn "sec=%s" sec
```

### VB.NET

```vbnet
Imports System
Imports System.Text

Module Secuencia
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim sb As New StringBuilder()
        For i = 1 To n
            If i > 1 Then sb.Append("-"c)
            sb.Append(i)
        Next
        Console.WriteLine("sec=" & sb.ToString())
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR, donde `System.String` es inmutable y `StringBuilder`
existe justamente para ofrecer el buffer mutable que falta. VB.NET usa esa herramienta de forma
canónica. F# elige el extremo opuesto: sus `let` son inmutables por defecto —para tener una variable
reasignable hay que pedirlo con `let mutable`— y su lista `[ 1 .. n ]` es una lista enlazada
inmutable, no un array que se rellena. Dos lenguajes, la misma biblioteca base, posturas contrarias
sobre quién debería poder cambiar qué.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    int n = 0;
    std::cin >> n;
    std::string sec;
    for (int i = 1; i <= n; ++i) {
        if (i > 1) sec += '-';
        sec += std::to_string(i);
    }
    std::cout << "sec=" << sec << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);
        NSMutableArray<NSString *> *partes = [NSMutableArray array];
        for (int i = 1; i <= n; i++) {
            [partes addObject:[NSString stringWithFormat:@"%d", i]];
        }
        NSString *sec = [partes componentsJoinedByString:@"-"];
        printf("sec=%s\n", [sec UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C**, pero aquí cada uno resuelve la mutabilidad con
la herramienta de su propia biblioteca. `std::string` de C++ es un buffer **mutable** que crece solo:
por eso `sec += ...` es idiomático y no el desastre de rendimiento que sería en Java o Python.
Objective-C hace explícita la distinción en el propio nombre del tipo: `NSArray` es inmutable y
`NSMutableArray` es su hermano modificable; la línea que declaras dice, sin comentarios, si el objeto
va a cambiar. Fíjate además en que el resultado final vuelve a ser un `NSString` inmutable.

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
    const n = try std.fmt.parseInt(u32, std.mem.trim(u8, linea, " \r"), 10);

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    var sec = std.ArrayList(u8).init(gpa.allocator());
    defer sec.deinit();

    var i: u32 = 1;
    while (i <= n) : (i += 1) {
        if (i > 1) try sec.append('-');
        try sec.writer().print("{d}", .{i});
    }
    try std.io.getStdOut().writer().print("sec={s}\n", .{sec.items});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let n = stdin.readLine().strip().parseInt()
echo "sec=" & toSeq(1 .. n).mapIt($it).join("-")
```

### D

```d
import std.stdio, std.array, std.conv, std.range, std.algorithm, std.string;

void main() {
    const n = readln().strip().to!int;
    const sec = iota(1, n + 1).map!(to!string).array.join("-");
    writeln("sec=", sec);
}
```

**Qué reconocer:** Zig es el más explícito de todos y aquí se ve por qué. La mutabilidad se declara en
la palabra clave —`const` frente a `var`, y el compilador rechaza un `var` que nunca cambia— y como no
hay recolector de basura, el buffer que crece exige un **asignador** que tú entregas y liberas con
`defer`. Nim y D esconden esa maquinaria: `let` en Nim es inmutable (para reasignar hace falta `var`)
y `const` en D marca la referencia y todo lo alcanzable a través de ella, una garantía **transitiva**
más fuerte que la de casi cualquier otro lenguaje de esta página.

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
    number_string(N, Linea),
    numlist(1, N, Numeros),
    maplist(number_string, Numeros, Textos),
    atomic_list_concat(Textos, '-', Sec),
    format("sec=~w~n", [Sec]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S, ni aritmética, ni construcción de cadenas: solo hechos y
% reglas. Lo más cercano es enumerar los números como hechos y declarar la relación de
% sucesión; unir el resultado en una cadena queda fuera del lenguaje.
numero(1).
numero(2).
numero(3).

sigue(I, J) :- numero(I), numero(J), J = I + 1.
```

**Qué reconocer:** en Prolog **no existe la mutabilidad en absoluto**, y no como decisión de estilo
sino como consecuencia del modelo. Un nombre como `N` o `Sec` no es una variable que guarde un valor:
es una **incógnita que se unifica una sola vez**. No hay forma de escribir `N = N + 1`, porque eso
pediría que `N` sea igual a algo distinto de sí mismo, y fallaría. Por eso el programa avanza creando
nombres nuevos (`Numeros`, `Textos`, `Sec`) en vez de reescribir uno. Datalog lleva la renuncia al
extremo: sin efectos, sin E/S y sin funciones, solo hechos que son ciertos y reglas que derivan más
hechos ciertos. Es la misma renuncia que hace SQL al no decirte cómo recorrer las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer `n`, generar los números,
unirlos con guiones. Lo que cambia es **quién tiene permiso para cambiar qué**: un buffer mutable en
C++ y Zig, una lista mutable con nombre fijo en Dart, una estructura persistente en Clojure, y en
Prolog ni siquiera eso. Eso es lo transferible.

⏮️ [Volver a la clase 054](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
