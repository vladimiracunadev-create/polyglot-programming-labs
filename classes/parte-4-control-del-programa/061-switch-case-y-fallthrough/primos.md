# 🧬 El mismo programa en las familias de lenguajes — Clase 061

> [⬅️ Volver a la clase 061](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el nombre del día a partir de su número— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `d`
- **Salida** (stdout): `dia=<nombre>`
- **Regla:** `1→lunes`, `2→martes`, `3→miercoles`, `4→jueves`, `5→viernes`, `6→sabado`,
  `7→domingo`; cualquier otro valor produce `dia=invalido`

| stdin | esperado |
|---|---|
| `1` | `dia=lunes` |
| `6` | `dia=sabado` |
| `8` | `dia=invalido` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí se ve algo que la clase no puede enseñar con un solo lenguaje: la mitad de esta familia **no
tiene `switch`** y resuelve la selección por valor con una tabla asociativa.

### Ruby

```ruby
d = STDIN.gets.to_i
nombre = case d
         when 1 then "lunes"
         when 2 then "martes"
         when 3 then "miercoles"
         when 4 then "jueves"
         when 5 then "viernes"
         when 6 then "sabado"
         when 7 then "domingo"
         else "invalido"
         end
puts "dia=#{nombre}"
```

### Perl

```perl
# Perl no tiene switch: given/when fue experimental y acabó retirado.
# El idioma de la comunidad para seleccionar por valor es la tabla hash.
my $d = <STDIN>;
chomp $d;
my %dias = (1 => 'lunes',   2 => 'martes',  3 => 'miercoles', 4 => 'jueves',
            5 => 'viernes', 6 => 'sabado',  7 => 'domingo');
printf "dia=%s\n", $dias{$d} // 'invalido';
```

### Lua

```lua
-- Lua tampoco tiene switch: la tabla indexada por posición hace el trabajo.
local d = tonumber(io.read("l"))
local dias = { "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo" }
print("dia=" .. (dias[d] or "invalido"))
```

### Tcl

```tcl
gets stdin d
switch -- $d {
    1 { set nombre lunes }
    2 { set nombre martes }
    3 { set nombre miercoles }
    4 { set nombre jueves }
    5 { set nombre viernes }
    6 { set nombre sabado }
    7 { set nombre domingo }
    default { set nombre invalido }
}
puts "dia=$nombre"
```

### R

```r
d <- as.integer(readLines("stdin", n = 1))
# switch() con un entero selecciona por POSICIÓN y no admite rama por defecto:
# cuando el índice se sale del rango devuelve NULL, y el default se pone a mano.
nombre <- switch(d, "lunes", "martes", "miercoles", "jueves",
                 "viernes", "sabado", "domingo")
if (is.null(nombre)) nombre <- "invalido"
cat(sprintf("dia=%s\n", nombre))
```

**Qué reconocer:** solo Ruby y Tcl traen una construcción de selección múltiple de verdad, y son
**expresiones o comandos**, no la sentencia de C: el `case` de Ruby devuelve un valor y no hay
`break` ni caída en cascada. Perl y Lua declaran la ausencia con toda claridad —la tabla asociativa
*es* su `switch`— y de paso muestran por qué el fallthrough nunca les hizo falta. R es el caso más
extraño: su `switch` es una **función** y, con índice numérico, elige por posición y devuelve `NULL`
cuando no encaja.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final d = int.parse(stdin.readLineSync()!.trim());
  final nombre = switch (d) {
    1 => 'lunes',
    2 => 'martes',
    3 => 'miercoles',
    4 => 'jueves',
    5 => 'viernes',
    6 => 'sabado',
    7 => 'domingo',
    _ => 'invalido',
  };
  print('dia=$nombre');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la selección.
// Su switch es el de C, con case/break y caída en cascada si se omite el break.
package {
    public class Dia {
        public static function nombre(d:int):String {
            switch (d) {
                case 1: return "dia=lunes";
                case 2: return "dia=martes";
                case 3: return "dia=miercoles";
                case 4: return "dia=jueves";
                case 5: return "dia=viernes";
                case 6: return "dia=sabado";
                case 7: return "dia=domingo";
                default: return "dia=invalido";
            }
        }
    }
}
```

**Qué reconocer:** ActionScript conserva intacto el `switch` heredado de C —el mismo que sigue vivo
en JavaScript, con `break` obligatorio y fallthrough implícito—. Dart parte de ahí y en su versión 3
añade la **expresión** `switch`: sin `break`, con `_` como comodín y devolviendo un valor. Es el
mismo movimiento que hicieron C# y Java con sus `switch` de flecha.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode; lo que
cambia es cuánta ceremonia exigen y si la selección es sentencia o expresión.

### Kotlin

```kotlin
fun main() {
    val nombre = when (readLine()!!.trim().toInt()) {
        1 -> "lunes"
        2 -> "martes"
        3 -> "miercoles"
        4 -> "jueves"
        5 -> "viernes"
        6 -> "sabado"
        7 -> "domingo"
        else -> "invalido"
    }
    println("dia=$nombre")
}
```

### Scala

```scala
object Dia extends App {
  val nombre = scala.io.StdIn.readInt() match {
    case 1 => "lunes"
    case 2 => "martes"
    case 3 => "miercoles"
    case 4 => "jueves"
    case 5 => "viernes"
    case 6 => "sabado"
    case 7 => "domingo"
    case _ => "invalido"
  }
  println(s"dia=$nombre")
}
```

### Groovy

```groovy
def d = System.in.newReader().readLine().trim() as int
def nombre
switch (d) {
    case 1: nombre = 'lunes'; break
    case 2: nombre = 'martes'; break
    case 3: nombre = 'miercoles'; break
    case 4: nombre = 'jueves'; break
    case 5: nombre = 'viernes'; break
    case 6: nombre = 'sabado'; break
    case 7: nombre = 'domingo'; break
    default: nombre = 'invalido'
}
println "dia=$nombre"
```

### Clojure

```clojure
(let [d (Integer/parseInt (.trim (read-line)))
      nombre (case d
               1 "lunes"
               2 "martes"
               3 "miercoles"
               4 "jueves"
               5 "viernes"
               6 "sabado"
               7 "domingo"
               "invalido")]
  (println (str "dia=" nombre)))
```

**Qué reconocer:** Groovy mantiene la forma de Java —`case`, `break`, caída si lo olvidas— pero
compara con `isCase`, no con `==`, así que un `case` puede ser una clase, una expresión regular o un
rango. Kotlin (`when`), Scala (`match`) y Clojure (`case`) eliminan el `break` de raíz: sin
sentencia no hay caída posible, y el resultado es un valor que se asigna directamente. En Clojure la
última forma suelta es la rama por defecto, y `case` exige constantes en tiempo de compilación: es
un salto por tabla, no una cadena de comparaciones.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let nombre =
    match int (stdin.ReadLine().Trim()) with
    | 1 -> "lunes"
    | 2 -> "martes"
    | 3 -> "miercoles"
    | 4 -> "jueves"
    | 5 -> "viernes"
    | 6 -> "sabado"
    | 7 -> "domingo"
    | _ -> "invalido"
printfn "dia=%s" nombre
```

### VB.NET

```vbnet
Module Dia
    Sub Main()
        Dim d = Integer.Parse(Console.ReadLine().Trim())
        Dim nombre As String
        Select Case d
            Case 1 : nombre = "lunes"
            Case 2 : nombre = "martes"
            Case 3 : nombre = "miercoles"
            Case 4 : nombre = "jueves"
            Case 5 : nombre = "viernes"
            Case 6 : nombre = "sabado"
            Case 7 : nombre = "domingo"
            Case Else : nombre = "invalido"
        End Select
        Console.WriteLine("dia=" & nombre)
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR, pero ninguno de los dos primos tiene fallthrough.
VB.NET nunca lo tuvo: cada `Case` termina solo, y por eso no existe `break` en su `Select Case`
—precisamente el error que C obliga a recordar—. F# va más lejos y hace del `match` la construcción
central del lenguaje: el compilador avisa si dejas casos sin cubrir, algo que un `switch` de C jamás
comprueba.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí nació el `switch` con `case`, `break` y caída
en cascada que el resto de familias heredó o corrigió.

### C++

```cpp
#include <iostream>
#include <string_view>

int main() {
    int d;
    std::cin >> d;
    std::string_view nombre;
    switch (d) {
        case 1: nombre = "lunes"; break;
        case 2: nombre = "martes"; break;
        case 3: nombre = "miercoles"; break;
        case 4: nombre = "jueves"; break;
        case 5: nombre = "viernes"; break;
        case 6: nombre = "sabado"; break;
        case 7: nombre = "domingo"; break;
        default: nombre = "invalido"; break;
    }
    std::cout << "dia=" << nombre << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int d;
        scanf("%d", &d);
        NSString *nombre;
        switch (d) {
            case 1: nombre = @"lunes"; break;
            case 2: nombre = @"martes"; break;
            case 3: nombre = @"miercoles"; break;
            case 4: nombre = @"jueves"; break;
            case 5: nombre = @"viernes"; break;
            case 6: nombre = @"sabado"; break;
            case 7: nombre = @"domingo"; break;
            default: nombre = @"invalido"; break;
        }
        printf("dia=%s\n", nombre.UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C** y su `switch` es literalmente el mismo: solo
acepta enteros y enumerados, exige `break` en cada rama y cae a la siguiente si lo omites. Lo único
que cambia es el tipo del valor guardado —`std::string_view` frente a `NSString *`— y cómo se
imprime. C++ moderno añade `[[fallthrough]]` para declarar que la caída es intencionada; sin esa
marca, el compilador puede avisarte de que probablemente sea un olvido.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con una postura muy explícita sobre el fallthrough: lo consideran un error de diseño.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const d = try std.fmt.parseInt(i32, std.mem.trim(u8, linea, " \r"), 10);
    const nombre = switch (d) {
        1 => "lunes",
        2 => "martes",
        3 => "miercoles",
        4 => "jueves",
        5 => "viernes",
        6 => "sabado",
        7 => "domingo",
        else => "invalido",
    };
    try std.io.getStdOut().writer().print("dia={s}\n", .{nombre});
}
```

### Nim

```nim
import std/strutils

let d = stdin.readLine().strip().parseInt()
let nombre =
  case d
  of 1: "lunes"
  of 2: "martes"
  of 3: "miercoles"
  of 4: "jueves"
  of 5: "viernes"
  of 6: "sabado"
  of 7: "domingo"
  else: "invalido"
echo "dia=", nombre
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const d = readln().strip().to!int;
    string nombre;
    switch (d) {
        case 1: nombre = "lunes"; break;
        case 2: nombre = "martes"; break;
        case 3: nombre = "miercoles"; break;
        case 4: nombre = "jueves"; break;
        case 5: nombre = "viernes"; break;
        case 6: nombre = "sabado"; break;
        case 7: nombre = "domingo"; break;
        default: nombre = "invalido"; break;
    }
    writefln("dia=%s", nombre);
}
```

**Qué reconocer:** Zig y Nim convierten la selección en **expresión exhaustiva**: no hay `break`,
cada rama produce un valor y el compilador exige que cubras todos los casos o escribas `else`. D
conserva la sintaxis de C pero corrige su trampa: la caída implícita entre `case` es un **error de
compilación**, y si de verdad la quieres tienes que escribir `goto case`. Es exactamente la misma
decisión que tomó Go al hacer el `fallthrough` explícito.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay `switch` porque no hay flujo de control:
se declara la correspondencia y el motor la resuelve.

### Prolog

```prolog
:- initialization(main, main).

dia(1, "lunes").
dia(2, "martes").
dia(3, "miercoles").
dia(4, "jueves").
dia(5, "viernes").
dia(6, "sabado").
dia(7, "domingo").

nombre(D, N) :- dia(D, N), !.
nombre(_, "invalido").

main :-
    read_line_to_string(user_input, Linea),
    number_string(D, Linea),
    nombre(D, N),
    format("dia=~w~n", [N]).
```

### Datalog

```datalog
% Datalog no tiene E/S: la entrada se declara como un hecho.
% La rama por defecto necesita negación estratificada (Datalog¬),
% porque en Datalog puro no se puede decir "si NO existe correspondencia".
dia(1, "lunes").
dia(2, "martes").
dia(3, "miercoles").
dia(4, "jueves").
dia(5, "viernes").
dia(6, "sabado").
dia(7, "domingo").

entrada(8).

conocido(D) :- dia(D, _).
resultado(N) :- entrada(D), dia(D, N).
resultado("invalido") :- entrada(D), not conocido(D).
```

**Qué reconocer:** en Prolog las siete ramas del `switch` son **siete hechos**, y la selección la
hace la unificación de la cabeza de cláusula, no una sentencia. El `!` (corte) cumple el papel del
`break`: impide que el motor pruebe también la cláusula por defecto tras haber encontrado un día
válido; sin él, `nombre/2` daría dos soluciones por backtracking. Datalog lleva la renuncia al
extremo —solo hechos y reglas— y deja al descubierto que un "caso por defecto" es, en lógica, una
**negación**: algo que el Datalog puro ni siquiera puede expresar.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas distintas a la misma pregunta: la caída en
cascada de C, la expresión exhaustiva de Kotlin, Zig o F#, y la ausencia total de `switch` en Perl,
Lua o Prolog, donde una tabla o unos hechos hacen el mismo trabajo. Reconocer cuál de las tres
tienes delante es lo transferible.

⏮️ [Volver a la clase 061](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
