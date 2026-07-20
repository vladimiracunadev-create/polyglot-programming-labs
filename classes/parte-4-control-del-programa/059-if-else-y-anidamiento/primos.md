# 🧬 El mismo programa en las familias de lenguajes — Clase 059

> [⬅️ Volver a la clase 059](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —convertir una calificación numérica en una letra
mediante una cadena de condiciones— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `score` entre 0 y 100
- **Salida** (stdout): `nota=<A|B|C|F>`
- **Regla:** `score >= 90` → `A`; `>= 80` → `B`; `>= 70` → `C`; si no → `F`

| stdin | esperado |
|---|---|
| `95` | `nota=A` |
| `72` | `nota=C` |
| `40` | `nota=F` |

Fíjate en lo que la cadena `else if` esconde: cada rama solo se prueba si **todas las anteriores
fallaron**, así que el `>= 80` significa en realidad "entre 80 y 89". Ese contexto implícito es lo
que se pierde al anidar demasiado, y lo que algunas familias obligan a escribir a mano.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La cadena de condiciones se escribe plana; nadie anida si no hace falta.

### Ruby

```ruby
score = STDIN.gets.to_i
if score >= 90
  nota = "A"
elsif score >= 80
  nota = "B"
elsif score >= 70
  nota = "C"
else
  nota = "F"
end
puts "nota=#{nota}"
```

### Perl

```perl
chomp(my $score = <STDIN>);
my $nota;
if    ($score >= 90) { $nota = "A" }
elsif ($score >= 80) { $nota = "B" }
elsif ($score >= 70) { $nota = "C" }
else                 { $nota = "F" }
print "nota=$nota\n";
```

### Lua

```lua
local score = tonumber(io.read("l"))
local nota
if score >= 90 then
  nota = "A"
elseif score >= 80 then
  nota = "B"
elseif score >= 70 then
  nota = "C"
else
  nota = "F"
end
print("nota=" .. nota)
```

### Tcl

```tcl
gets stdin score
if {$score >= 90} {
    set nota A
} elseif {$score >= 80} {
    set nota B
} elseif {$score >= 70} {
    set nota C
} else {
    set nota F
}
puts "nota=$nota"
```

### R

```r
score <- as.integer(readLines("stdin", n = 1))
if (score >= 90) {
  nota <- "A"
} else if (score >= 80) {
  nota <- "B"
} else if (score >= 70) {
  nota <- "C"
} else {
  nota <- "F"
}
cat("nota=", nota, "\n", sep = "")
```

**Qué reconocer:** la escalera es la misma en los cinco, y la ortografía de la palabra intermedia es
la huella de cada familia: `elsif` (Ruby, Perl), `elseif` (Lua, Tcl, PHP), `elif` (Python), o el
`else if` de dos palabras (R, y toda la familia C). No es cosmética: donde existe una palabra propia,
el lenguaje está **evitando el anidamiento** —`elif` es una rama del mismo `if`, no un `if` nuevo
dentro del `else`—. R es el único que hace lo segundo, y por eso su `else` debe ir en la misma línea
que la llave de cierre: si lo bajas, el intérprete da la sentencia por terminada. Tcl lleva el asunto
al límite: su `if` no es sintaxis sino **un comando** que recibe cadenas, y `elseif` es solo un
argumento más.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final score = int.parse(stdin.readLineSync()!.trim());
  String nota;
  if (score >= 90) {
    nota = 'A';
  } else if (score >= 80) {
    nota = 'B';
  } else if (score >= 70) {
    nota = 'C';
  } else {
    nota = 'F';
  }
  print('nota=$nota');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra la cadena.
    public class Nota {
        public static function letra(score:int):String {
            if (score >= 90) return "A";
            else if (score >= 80) return "B";
            else if (score >= 70) return "C";
            else return "F";
        }
    }
}
```

**Qué reconocer:** sintaxis idéntica a la de JavaScript, hasta las llaves opcionales de una sola
línea. La diferencia está en el **análisis de asignación definitiva**: Dart declara `String nota;` sin
valor y acepta el programa solo porque puede demostrar que todas las ramas la asignan; si borras el
`else` final, no compila. JavaScript te dejaría con `undefined` y TypeScript te avisaría solo con
`strictNullChecks` activado. Es la misma cadena de condiciones con distinta red de seguridad.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Mismo bytecode; lo que cambia es si el `if` es
una sentencia o una expresión.

### Kotlin

```kotlin
fun main() {
    val score = readLine()!!.trim().toInt()
    val nota = when {
        score >= 90 -> "A"
        score >= 80 -> "B"
        score >= 70 -> "C"
        else -> "F"
    }
    println("nota=$nota")
}
```

### Scala

```scala
object Nota extends App {
  val score = scala.io.StdIn.readLine().trim.toInt
  val nota =
    if (score >= 90) "A"
    else if (score >= 80) "B"
    else if (score >= 70) "C"
    else "F"
  println(s"nota=$nota")
}
```

### Groovy

```groovy
def score = System.in.newReader().readLine().trim() as int
def nota
if (score >= 90) {
    nota = 'A'
} else if (score >= 80) {
    nota = 'B'
} else if (score >= 70) {
    nota = 'C'
} else {
    nota = 'F'
}
println "nota=$nota"
```

### Clojure

```clojure
(let [score (Integer/parseInt (.trim (read-line)))
      nota  (cond
              (>= score 90) "A"
              (>= score 80) "B"
              (>= score 70) "C"
              :else         "F")]
  (println (str "nota=" nota)))
```

**Qué reconocer:** Groovy es Java con menos ruido y conserva la cadena tal cual. Los otros tres **no
tienen un `if` de sentencia**: en Kotlin, Scala y Clojure el condicional siempre produce un valor, así
que la variable se asigna una sola vez y puede ser inmutable (`val`). Ese giro cambia la forma del
código —desaparece la variable declarada sin valor y reasignada cuatro veces— y es exactamente el
tema de la clase 060. Clojure lo lleva más lejos: su `if` acepta **solo dos ramas**, de modo que una
cadena de cuatro casos no se escribe anidando `if` dentro de `if`, sino con `cond`, que aplana el
anidamiento por construcción.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let score = stdin.ReadLine().Trim() |> int
let nota =
    if score >= 90 then "A"
    elif score >= 80 then "B"
    elif score >= 70 then "C"
    else "F"
printfn "nota=%s" nota
```

### VB.NET

```vbnet
Module Nota
    Sub Main()
        Dim score = Integer.Parse(Console.ReadLine().Trim())
        Dim nota As String
        If score >= 90 Then
            nota = "A"
        ElseIf score >= 80 Then
            nota = "B"
        ElseIf score >= 70 Then
            nota = "C"
        Else
            nota = "F"
        End If
        Console.WriteLine("nota=" & nota)
    End Sub
End Module
```

**Qué reconocer:** VB.NET es la misma cadena de C# con palabras en lugar de llaves —`Then`,
`ElseIf`, `End If`— y con una trampa de sintaxis que revela el mecanismo: `ElseIf` junto es una rama
más del mismo condicional, mientras que `Else If` separado abre un `If` **anidado** que exige su
propio `End If`. F# vuelve a marcar la frontera funcional: `if` es una expresión, todas las ramas han
de devolver el mismo tipo, y el `else` final es obligatorio en cuanto el resultado no es `unit`.
Donde VB.NET declara la variable vacía y la rellena, F# la define de una vez con el valor del
condicional.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El origen de la escalera `else if` y de sus dos
trampas clásicas: el `else` colgante y las llaves omitidas.

### C++

```cpp
#include <iostream>

int main() {
    long score;
    std::cin >> score;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    std::cout << "nota=" << nota << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long score;
        if (scanf("%ld", &score) != 1) return 1;
        NSString *nota;
        if (score >= 90) {
            nota = @"A";
        } else if (score >= 80) {
            nota = @"B";
        } else if (score >= 70) {
            nota = @"C";
        } else {
            nota = @"F";
        }
        printf("nota=%s\n", nota.UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** en esta familia `else if` **no existe como construcción**: es un `if` anidado
dentro del `else` del anterior, y solo lo parece plano porque nadie escribe las llaves ni la
indentación que le corresponderían. De ahí el `else` colgante —un `else` sin llaves se engancha
siempre al `if` más cercano— y de ahí la regla de estilo de escribir las llaves siempre. C++ añade
`if` con inicializador (`if (auto n = f(); n > 0)`) para acotar el ámbito de una variable a la
condición; Objective-C se queda con el `if` de C sin retoques y solo cambia el tipo de la variable
por un objeto.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La misma escalera, pero
con el compilador vigilando que no falte ninguna rama.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const score = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    const nota: u8 = if (score >= 90) 'A' else if (score >= 80) 'B' else if (score >= 70) 'C' else 'F';
    try std.io.getStdOut().writer().print("nota={c}\n", .{nota});
}
```

### Nim

```nim
import std/strutils

let score = stdin.readLine().strip().parseInt()
var nota: string
if score >= 90:
  nota = "A"
elif score >= 80:
  nota = "B"
elif score >= 70:
  nota = "C"
else:
  nota = "F"
echo "nota=", nota
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const score = readln().strip().to!long;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    writefln("nota=%s", nota);
}
```

**Qué reconocer:** D es C con llaves y la misma escalera literal. Zig conserva la sintaxis de C pero
convierte el `if` en **expresión**, como Rust: por eso las cuatro ramas caben en una asignación a
`const`, y por eso el `else` final no es opcional —sin él no habría valor que asignar—. Nim escribe
`elif` como Python y bloques por indentación, pero compila a nativo: la comunidad de sistemas
adoptando la ergonomía de la familia dinámica. En los tres, un `if` sin `else` usado como expresión
es un error de compilación, no un `null` silencioso.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El `CASE WHEN` es la cadena `else if` del mundo
declarativo, y no todos sus parientes la tienen.

### Prolog

```prolog
:- initialization(main, main).

% Las cláusulas se prueban en orden; el corte (!) hace de "else".
nota(S, 'A') :- S >= 90, !.
nota(S, 'B') :- S >= 80, !.
nota(S, 'C') :- S >= 70, !.
nota(_, 'F').

main :-
    read_line_to_string(user_input, Linea),
    number_string(Score, Linea),
    nota(Score, N),
    format("nota=~w~n", [N]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni orden entre cláusulas: no hay "else" que heredar.
% Cada rango se escribe cerrado por los dos lados.
score(72).

nota(S, "A") :- score(S), S >= 90.
nota(S, "B") :- score(S), S >= 80, S < 90.
nota(S, "C") :- score(S), S >= 70, S < 80.
nota(S, "F") :- score(S), S < 70.
```

**Qué reconocer:** Prolog reproduce la cadena con una técnica distinta: no hay `else`, hay
**cláusulas ordenadas** y un corte que impide seguir probando. Léelo como la escalera de arriba y
encaja pieza por pieza. Datalog enseña lo que la cadena `else if` te estaba regalando gratis: sin
orden de evaluación, el "y si no" desaparece y hay que escribir `S >= 80, S < 90` explícitamente —el
mismo límite superior que en los demás lenguajes es invisible—. Si alguna vez has tenido que
convertir una cadena de `if` en tablas de rangos disjuntos, ya conoces este dolor; SQL lo evitó
dándole a su `CASE WHEN` un orden de evaluación garantizado.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una escalera de cuatro peldaños en todos. Lo que cambia es si
el lenguaje te da una palabra para aplanar el anidamiento (`elif`, `elsif`, `ElseIf`, `cond`,
`when`), si el condicional devuelve un valor y si te obliga a cubrir el último caso. Eso es lo
transferible.

⏮️ [Volver a la clase 059](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
