# 🧬 El mismo programa en las familias de lenguajes — Clase 077

> [⬅️ Volver a la clase 077](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —devolver a la vez el cociente y el resto— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Aquí la comparación es especialmente reveladora: casi ningún lenguaje devuelve de verdad dos
valores. Lo que cambia es **qué se devuelve en su lugar** —una lista, una tupla, un registro, un
puntero de salida— y **cómo se deshace** ese envoltorio al recibirlo.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (enteros positivos, `b != 0`)
- **Salida** (stdout): `cociente=<a/b> resto=<a%b>`
- **Regla:** `(cociente, resto) = (a / b, a % b)` con división entera

| stdin | esperado |
|---|---|
| `17 5` | `cociente=3 resto=2` |
| `10 2` | `cociente=5 resto=0` |
| `7 3` | `cociente=2 resto=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno devuelve dos valores: devuelven **una** estructura ligera y la asignación la abre por
posición. Como no hay tipos declarados, el envoltorio no cuesta nada de escribir.

### Ruby

```ruby
def divmod2(a, b)
  [a / b, a % b]   # se devuelve un Array; el `return` implícito es el último valor
end

a, b = STDIN.gets.split.map(&:to_i)
cociente, resto = divmod2(a, b)
puts "cociente=#{cociente} resto=#{resto}"
```

### Perl

```perl
sub divmod2 {
    my ($num, $den) = @_;
    return (int($num / $den), $num % $den);   # una lista, no una referencia
}

my ($num, $den) = split ' ', <STDIN>;
my ($cociente, $resto) = divmod2($num, $den);
print "cociente=$cociente resto=$resto\n";
```

### Lua

```lua
local function divmod2(a, b)
  return a // b, a % b   -- retorno múltiple nativo: no hay contenedor de por medio
end

local a, b = io.read("n", "n")
local cociente, resto = divmod2(a, b)
print(string.format("cociente=%d resto=%d", cociente, resto))
```

### Tcl

```tcl
proc divmod2 {a b} {
    return [list [expr {$a / $b}] [expr {$a % $b}]]
}

gets stdin linea
lassign [split $linea] a b
lassign [divmod2 $a $b] cociente resto
puts "cociente=$cociente resto=$resto"
```

### R

```r
divmod2 <- function(a, b) list(cociente = a %/% b, resto = a %% b)

v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
r <- divmod2(v[1], v[2])
cat(sprintf("cociente=%d resto=%d\n", r$cociente, r$resto))
```

**Qué reconocer:** Ruby y Perl parecen devolver dos cosas, pero devuelven **una lista** que la
asignación desestructura por posición —si pides tres nombres, el tercero queda `nil`/`undef` sin
error—. **Lua es la excepción real de toda esta página:** su máquina virtual tiene retornos
múltiples de verdad, sin construir ninguna tabla intermedia, y por eso `local q, r = f()` no
"abre" nada: recibe dos valores del *stack*. Tcl vuelve a delatar su *todo es cadena*: la lista es
texto y `lassign` la parte. R renuncia a la posición y devuelve una **lista con nombres**, que se
lee por campo (`r$resto`) — más cerca de un registro que de una tupla.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

(int, int) divmod(int a, int b) => (a ~/ b, a % b);   // récord: tupla con tipo

void main() {
  final v = stdin.readLineSync()!.trim().split(' ').map(int.parse).toList();
  final (cociente, resto) = divmod(v[0], v[1]);
  print('cociente=$cociente resto=$resto');
}
```

### ActionScript 3

```actionscript
package {
    public class Division {
        // AS3 no tiene stdin, ni tuplas, ni desestructuración: se devuelve un objeto
        // y se leen sus campos por nombre.
        public static function divmod(a:int, b:int):Object {
            return {cociente: int(a / b), resto: a % b};
        }

        public static function informe(a:int, b:int):String {
            var r:Object = divmod(a, b);
            return "cociente=" + r.cociente + " resto=" + r.resto;
        }
    }
}
```

**Qué reconocer:** la desestructuración de JavaScript nació sobre objetos y arrays, y Dart 3 la
formalizó con **récords** —`(int, int)` es un tipo de verdad, comprobado en compilación, no un
`Object` cualquiera—. ActionScript 3 se quedó en el estado anterior de la familia: hay objetos
literales, pero **no hay patrón de asignación**, así que el receptor debe nombrar cada campo a mano.
Ese es exactamente el paso que dio ES6 y que AS3 nunca llegó a dar.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En la JVM un método devuelve **una** referencia
y punto; lo que distingue a los primos es cuánto azúcar ponen encima de esa limitación.

### Kotlin

```kotlin
fun divmod(a: Int, b: Int): Pair<Int, Int> = Pair(a / b, a % b)

fun main() {
    val (a, b) = readLine()!!.trim().split(" ").map { it.toInt() }
    val (cociente, resto) = divmod(a, b)   // usa component1() y component2()
    println("cociente=$cociente resto=$resto")
}
```

### Scala

```scala
object Division {
  def divmod(a: Int, b: Int): (Int, Int) = (a / b, a % b)

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    val (cociente, resto) = divmod(a, b)   // patrón: por debajo llama a unapply
    println(s"cociente=$cociente resto=$resto")
  }
}
```

### Groovy

```groovy
def divmod(int a, int b) { [a.intdiv(b), a % b] }

def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def (cociente, resto) = divmod(a, b)
println "cociente=$cociente resto=$resto"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn divmod [a b] [(quot a b) (rem a b)])   ; un vector inmutable

(let [[a b] (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))
      [cociente resto] (divmod a b)]
  (println (str "cociente=" cociente " resto=" resto)))
```

**Qué reconocer:** los cuatro esconden el mismo objeto de la JVM, pero por caminos distintos.
Kotlin desestructura **por convención posicional**: `val (q, r) = x` se compila a `x.component1()`
y `x.component2()`, así que funciona con cualquier clase que declare esos métodos —y por eso el
orden manda, no los nombres—. Scala usa el mecanismo más general de la familia, **`unapply`**: la
tupla es un patrón, el mismo que en un `match`. Groovy hace lo mismo dinámicamente sobre cualquier
`List`. Clojure ni siquiera necesita tuplas: todo dato secuencial se abre con la misma
desestructuración del `let`, que es sintaxis del lenguaje y no un método del objeto.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let divmod a b = (a / b, a % b)   // tuplas nativas, sin declararlas

let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
let (cociente, resto) = divmod a b
printfn "cociente=%d resto=%d" cociente resto
```

### VB.NET

```vbnet
Module Division
    ' VB.NET tiene ValueTuple pero no sintaxis de desestructuración:
    ' los campos se leen por nombre.
    Function Divmod(a As Integer, b As Integer) As (cociente As Integer, resto As Integer)
        Return (a \ b, a Mod b)
    End Function

    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim r = Divmod(Integer.Parse(v(0)), Integer.Parse(v(1)))
        Console.WriteLine($"cociente={r.cociente} resto={r.resto}")
    End Sub
End Module
```

**Qué reconocer:** los tres acaban en el mismo `System.ValueTuple` del CLR, pero solo dos saben
abrirlo. En F# la tupla es un tipo del lenguaje desde el primer día y la desestructuración es un
patrón, igual que en Scala. VB.NET puede **construir** la tupla y hasta ponerle nombres a los
campos, pero **no** tiene la sintaxis `Dim (q, r) = ...`: el receptor accede por campo. Y fíjate en
`\`, el operador de división entera de VB — donde C# y F# reutilizan `/` según el tipo, VB lo
distingue con un símbolo propio.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Un `return`, un valor: el segundo resultado sale por
un **puntero de salida** que el llamador reserva.

### C++

```cpp
#include <iostream>
#include <utility>

std::pair<long, long> divmod(long a, long b) {
    return {a / b, a % b};
}

int main() {
    long a, b;
    std::cin >> a >> b;
    auto [cociente, resto] = divmod(a, b);   // structured bindings (C++17)
    std::cout << "cociente=" << cociente << " resto=" << resto << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Objective-C hereda el gesto de C: un valor de retorno y el resto por puntero.
// La alternativa idiomática sería devolver un NSDictionary, pero eso obliga a
// envolver los enteros en NSNumber.
static long divmodOC(long a, long b, long *resto) {
    *resto = a % b;
    return a / b;
}

int main(void) {
    @autoreleasepool {
        long a, b, resto;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        long cociente = divmodOC(a, b, &resto);
        printf("cociente=%ld resto=%ld\n", cociente, resto);
    }
    return 0;
}
```

**Qué reconocer:** C++ recorrió el camino entero: `std::pair` desde siempre, `std::tie` después y
por fin los *structured bindings* de C++17, que son desestructuración de verdad —`auto [q, r]`
declara dos variables y no cuesta nada en tiempo de ejecución, porque el par se deshace en
compilación—. Objective-C se quedó en el modelo C puro: el parámetro `long *resto` **es** el segundo
retorno, y el llamador debe declarar la variable antes de la llamada. Reconocerás ese `&resto` en
todas las APIs de Cocoa que reciben un `NSError **`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go es el raro que sí
tiene retornos múltiples en la ABI; el resto de la familia devuelve una estructura.

### Zig

```zig
const std = @import("std");

const DivMod = struct { cociente: i64, resto: i64 };

fn divmod(a: i64, b: i64) DivMod {
    return .{ .cociente = @divTrunc(a, b), .resto = @rem(a, b) };
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    const d = divmod(a, b);   // Zig no desestructura structs: se leen los campos
    try std.io.getStdOut().writer().print("cociente={d} resto={d}\n", .{ d.cociente, d.resto });
}
```

### Nim

```nim
import std/[strutils, strformat]

proc divmod(a, b: int): tuple[cociente, resto: int] =
  (a div b, a mod b)

let v = stdin.readLine().splitWhitespace()
let (cociente, resto) = divmod(parseInt(v[0]), parseInt(v[1]))
echo &"cociente={cociente} resto={resto}"
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.typecons;

Tuple!(long, "cociente", long, "resto") divmod(long a, long b) {
    return tuple!("cociente", "resto")(a / b, a % b);
}

void main() {
    auto v = readln().split().map!(to!long).array;
    auto d = divmod(v[0], v[1]);
    writefln("cociente=%d resto=%d", d.cociente, d.resto);
}
```

**Qué reconocer:** los tres devuelven **un solo valor agregado** que el compilador suele colocar en
dos registros, igual que la tupla de Rust: el coste es cero, la sintaxis no. Zig es el más austero
—declara un `struct` con nombre y lo lee por campo, porque el lenguaje **no** tiene desestructuración
de structs—. Nim sí tiene tuplas con nombre *y* desestructuración posicional, así que puedes elegir
`d.resto` o `let (q, r) = ...` sobre el mismo valor. D llega al mismo sitio con `std.typecons.Tuple`,
que no es sintaxis del lenguaje sino una **plantilla de biblioteca**: la tupla la genera el
compilador al instanciarla.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una fila con varias columnas ya es un
multi-retorno; no hay que inventar nada.

### Prolog

```prolog
:- initialization(main, main).

% No hay "retorno": Cociente y Resto son argumentos que se unifican al resolver.
cociente_resto(A, B, Cociente, Resto) :-
    Cociente is A // B,
    Resto is A mod B.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    cociente_resto(A, B, Cociente, Resto),
    format("cociente=~d resto=~d~n", [Cociente, Resto]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni funciones: los "dos retornos" son dos columnas
% del mismo hecho derivado.
par(17, 5).

division(A, B, Q, R) :- par(A, B), Q = A / B, R = A % B.
```

**Qué reconocer:** aquí desaparece la pregunta. Prolog **no tiene retorno** —un predicado no devuelve
nada, relaciona argumentos—, así que devolver dos valores no es más difícil que devolver uno: se
añade otro parámetro. Y como la unificación no distingue entrada de salida, el mismo
`cociente_resto/4` podría consultarse con el cociente ya conocido. Datalog lleva la idea al extremo:
una relación de aridad cuatro, sin dirección, sin efectos y sin llamada. Es la misma renuncia que
hace SQL cuando te devuelve una fila entera en vez de un valor.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una conclusión incómoda: **casi ninguno devuelve dos valores**.
Devuelven uno compuesto —lista, tupla, récord, struct— y lo que de verdad varía es si el lenguaje
sabe **abrirlo en la asignación** o te obliga a nombrar cada campo. Lua (retornos múltiples reales) y
Prolog (sin retorno alguno) marcan los dos extremos. Eso es lo transferible.

⏮️ [Volver a la clase 077](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
