# 🧬 El mismo programa en las familias de lenguajes — Clase 079

> [⬅️ Volver a la clase 079](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —comprobar que una función que recibe un entero
**no** modifica la variable del llamador— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El programa es minúsculo, pero separa a los lenguajes en dos grupos que no se ven a simple vista:
los que dejan **reasignar el parámetro** dentro de la función y los que lo tratan como una constante.
En ambos el original queda intacto; lo que cambia es si el compilador te deja intentarlo.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `original=<n> local=<2n>`
- **Regla:** la función duplica **su copia**; la variable del llamador permanece

| stdin | esperado |
|---|---|
| `5` | `original=5 local=10` |
| `3` | `original=3 local=6` |
| `0` | `original=0 local=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos pasan **la referencia al objeto por valor**: reasignar el parámetro solo cambia el nombre
local. Con enteros inmutables el efecto es indistinguible de copiar el número.

### Ruby

```ruby
def doblar(x)
  x = x * 2   # reasigna el nombre local; el Integer original ni se toca (es inmutable)
  x
end

n = STDIN.gets.to_i
local = doblar(n)
puts "original=#{n} local=#{local}"
```

### Perl

```perl
# Ojo: @_ contiene ALIAS de los argumentos del llamador. `my ($x) = @_`
# copia el valor y rompe el alias; tocar $_[0] sí modificaría el original.
sub doblar {
    my ($x) = @_;
    $x = $x * 2;
    return $x;
}

my $n = <STDIN>;
chomp $n;
my $local = doblar($n);
print "original=$n local=$local\n";
```

### Lua

```lua
local function doblar(x)
  x = x * 2   -- los parámetros son variables locales de la función
  return x
end

local n = io.read("n")
local doble = doblar(n)
print(string.format("original=%d local=%d", n, doble))
```

### Tcl

```tcl
proc doblar {x} {
    set x [expr {$x * 2}]
    return $x
}

gets stdin n
set doble [doblar $n]
puts "original=$n local=$doble"
```

### R

```r
doblar <- function(x) {
  x <- x * 2  # copia-al-modificar: R solo duplica el valor cuando lo escribes
  x
}

n <- as.integer(readLines("stdin", n = 1))
doble <- doblar(n)
cat(sprintf("original=%d local=%d\n", n, doble))
```

**Qué reconocer:** los cinco imprimen lo mismo por razones distintas. Ruby, Lua y Tcl pasan el
argumento por valor y ahí acaba la historia. R miente un poco: **no copia al llamar**, sino la
primera vez que escribes dentro (*copy-on-write*), por eso pasar un vector gigante a una función es
gratis mientras no lo modifiques. Y Perl es el que hay que mirar con lupa: `@_` no es una copia sino
un **array de alias** —`$_[0] *= 2` modificaría la variable del llamador—, así que el `my ($x) = @_`
de la primera línea no es ceremonia, **es** lo que convierte la llamada en paso por valor. Escribir
esa línea o no cambia la semántica del programa.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int doblar(int x) {
  x = x * 2;   // el parámetro es una variable local reasignable
  return x;
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final local = doblar(n);
  print('original=$n local=$local');
}
```

### ActionScript 3

```actionscript
package {
    public class Valor {
        // AS3 no tiene stdin: se ilustra el cálculo.
        // int es tipo primitivo, así que el parámetro es una copia real del número.
        public static function doblar(x:int):int {
            x = x * 2;
            return x;
        }

        public static function informe(n:int):String {
            return "original=" + n + " local=" + doblar(n);
        }
    }
}
```

**Qué reconocer:** en esta familia se repite la regla de JavaScript: **todo se pasa por valor**, pero
para los objetos ese valor es una referencia, y por eso mutar un array dentro de una función sí se
ve fuera. ActionScript 3 hace visible la frontera que JS esconde: declara `int`, `Number` y `Boolean`
como **primitivos** frente a los tipos por referencia, la misma distinción que Java. Dart, en cambio,
no tiene primitivos —`int` es un objeto— y llega al mismo resultado por la vía de la
**inmutabilidad**: no existe forma de mutar un entero, así que la copia da igual.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM **solo** tiene paso por valor; el debate
eterno "¿Java pasa objetos por referencia?" se resuelve viendo que se copia la referencia, no el
objeto.

### Kotlin

```kotlin
fun doblar(x: Int): Int {
    val local = x * 2   // los parámetros de Kotlin son `val`: `x = ...` NO compila
    return local
}

fun main() {
    val n = readLine()!!.trim().toInt()
    println("original=$n local=${doblar(n)}")
}
```

### Scala

```scala
object Valor {
  // Los parámetros de Scala también son `val`: inmutables dentro del cuerpo.
  def doblar(x: Int): Int = x * 2

  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"original=$n local=${doblar(n)}")
  }
}
```

### Groovy

```groovy
def doblar(x) {
    x = x * 2   // Groovy sí permite reasignar el parámetro
    x
}

def n = System.in.newReader().readLine().trim().toInteger()
println "original=$n local=${doblar(n)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn doblar [x] (* x 2))   ; no hay reasignación en el lenguaje: nada que demostrar

(let [n (Integer/parseInt (str/trim (read-line)))]
  (println (str "original=" n " local=" (doblar n))))
```

**Qué reconocer:** aquí aparece la división que anunciábamos. Java y Groovy dejan reasignar el
parámetro —es una variable local más—, y eso hace que el ejemplo de la clase *se pueda escribir*.
Kotlin y Scala **prohíben** la reasignación: el parámetro es un `val`, así que `x = x * 2` ni
siquiera compila y hay que introducir un nombre nuevo. La lección es que en esos dos lenguajes la
pregunta "¿modifica el original?" ni se plantea, porque la operación que la haría dudosa está
bloqueada en el origen. Clojure lleva la idea al final: sin *ninguna* forma de mutar, el paso por
valor deja de ser un tema.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). En .NET el paso por valor es el **defecto** y el
otro modo hay que pedirlo con `ref` / `out` — lo verás en la clase 080.

### F\#

```fsharp
let doblar x =
    let local = x * 2   // los valores de F# son inmutables: no hay `x <- ...` salvo `mutable`
    local

let n = int (stdin.ReadLine().Trim())
printfn "original=%d local=%d" n (doblar n)
```

### VB.NET

```vbnet
Module Valor
    ' ByVal es el defecto; VB permite (y antes obligaba a) escribirlo.
    Function Doblar(ByVal x As Integer) As Integer
        x = x * 2
        Return x
    End Function

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine($"original={n} local={Doblar(n)}")
    End Sub
End Module
```

**Qué reconocer:** VB.NET es el único lenguaje de esta página con una **palabra clave explícita para
el paso por valor**: `ByVal`. Es una herencia incómoda —en VB6 el defecto era `ByRef`, y al pasar a
.NET se invirtió—, y por eso durante años el IDE la insertaba sola. Ese detalle histórico explica
por qué el mismo CLR tiene dos lenguajes con defectos opuestos en su ascendencia. F# está en el otro
extremo: la inmutabilidad por defecto convierte el ejemplo en trivial, porque `x` no es una variable
sino un nombre ligado a un valor.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C **siempre** pasa por valor; los punteros no son una
excepción, son un valor que resulta ser una dirección.

### C++

```cpp
#include <iostream>

long doblar(long x) {   // por valor: x es una copia del argumento
    x = x * 2;
    return x;
}

int main() {
    long n;
    std::cin >> n;
    const long local = doblar(n);
    std::cout << "original=" << n << " local=" << local << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Los escalares se copian, igual que en C. Pero un objeto Objective-C
// SIEMPRE se recibe como puntero (NSNumber *), nunca como valor:
// se copia la dirección, no el objeto.
static long doblar(long x) {
    x = x * 2;
    return x;
}

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        long local = doblar(n);
        printf("original=%ld local=%ld\n", n, local);
    }
    return 0;
}
```

**Qué reconocer:** los tres comparten literalmente el mismo cuerpo, y sin embargo C++ es el lenguaje
donde el paso por valor **cuesta dinero**: copiar un `long` es gratis, pero copiar un `std::string`
o un `std::vector` invoca el constructor de copia y reserva memoria. De ahí que el C++ idiomático
escriba `const T&` para todo lo que no sea un escalar — una tercera opción que C no tiene.
Objective-C no puede plantearse la pregunta con objetos: no existe un `NSNumber` "por valor", solo
`NSNumber *`, así que la copia siempre es de un puntero de 8 bytes.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Copiar es explícito y su
coste es parte del contrato del tipo.

### Zig

```zig
const std = @import("std");

fn doblar(x: i64) i64 {
    const local = x * 2;   // en Zig los parámetros son CONSTANTES: `x = ...` no compila
    return local;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("original={d} local={d}\n", .{ n, doblar(n) });
}
```

### Nim

```nim
import std/[strutils, strformat]

proc doblar(x: int): int =
  var copia = x   # los parámetros de Nim son inmutables salvo que se marquen `var`
  copia = copia * 2
  copia

let n = stdin.readLine().strip().parseInt()
echo &"original={n} local={doblar(n)}"
```

### D

```d
import std.stdio, std.conv, std.string;

long doblar(long x) {
    x = x * 2;   // en D el parámetro sí es reasignable (in / const lo impedirían)
    return x;
}

void main() {
    const n = readln().strip().to!long;
    writefln("original=%d local=%d", n, doblar(n));
}
```

**Qué reconocer:** Zig y Nim se alinean con Kotlin y Scala: el parámetro **no se puede reasignar**,
hay que declarar una copia con nombre propio. En Zig la razón es de rendimiento además de estilo —al
prohibir escribir sobre el parámetro, el compilador queda libre para pasar los valores grandes por
referencia sin que el programa lo note—. Nim marca la frontera al revés que casi todos: inmutable
por defecto y `var` para pedir lo contrario, que es justo el tema de la clase 080. D conserva el
gesto de C, donde el parámetro es una variable local corriente.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay variables del llamador que modificar: una
expresión produce un valor nuevo y ya está.

### Prolog

```prolog
:- initialization(main, main).

% No hay parámetros que reasignar: `is` liga Local una sola vez.
% Volver a escribir Local con otro valor haría FALLAR el objetivo, no reasignar.
doblar(X, Local) :- Local is X * 2.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    doblar(N, Local),
    format("original=~d local=~d~n", [N, Local]).
```

### Datalog

```datalog
% Sin variables, sin asignación y sin E/S: el "local" es otra columna derivada.
num(5).

doble(N, L) :- num(N), L = N * 2.
```

**Qué reconocer:** en estos dos la distinción valor/referencia **no existe** porque no existe la
asignación. En Prolog `Local is X * 2` no escribe en una casilla de memoria: **unifica** `Local` con
el resultado, y una variable lógica solo se liga una vez dentro de la resolución. Intentar
"modificar el original" no daría un efecto secundario sino un fallo del objetivo. Es la misma
renuncia de SQL, y explica por qué en esta familia la pregunta de la clase se contesta sola: si nada
se puede modificar, no hay original que proteger.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma salida en todos: el original sobrevive. Pero el
camino separa tres grupos —los que dejan reasignar el parámetro (C, C++, D, Java, Groovy, VB.NET),
los que lo declaran constante y te obligan a nombrar la copia (Kotlin, Scala, Zig, Nim, F#), y los
que ni siquiera tienen asignación (Clojure, Prolog, Datalog)—. Saber en cuál de los tres estás te
dice de antemano qué error te va a dar el compilador. Eso es lo transferible.

⏮️ [Volver a la clase 079](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
