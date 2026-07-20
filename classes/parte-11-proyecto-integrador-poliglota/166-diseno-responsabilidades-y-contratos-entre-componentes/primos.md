# 🧬 El mismo programa en las familias de lenguajes — Clase 166

> [⬅️ Volver a la clase 166](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —verificar que dos componentes son compatibles en su
frontera— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` — los valores de contrato de cada componente
- **Salida** (stdout): `contrato=<compatible|incompatible>`
- **Regla:** compatible si `a == b`

| stdin | esperado |
|---|---|
| `5 5` | `contrato=compatible` |
| `5 6` | `contrato=incompatible` |
| `0 0` | `contrato=compatible` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y comparación directa: el contrato se verifica en una línea.

### Ruby

```ruby
a, b = STDIN.gets.split
puts "contrato=#{a == b ? 'compatible' : 'incompatible'}"
```

### Perl

```perl
my ($izq, $der) = split ' ', <STDIN>;
printf "contrato=%s\n", $izq eq $der ? "compatible" : "incompatible";
```

### Lua

```lua
local a, b = io.read("l"):match("(%S+)%s+(%S+)")
print("contrato=" .. (a == b and "compatible" or "incompatible"))
```

### Tcl

```tcl
lassign [regexp -all -inline {\S+} [gets stdin]] a b
puts "contrato=[expr {$a eq $b ? {compatible} : {incompatible}}]"
```

### R

```r
v <- scan("stdin", what = character(), n = 2, quiet = TRUE)
cat(sprintf("contrato=%s\n", if (v[1] == v[2]) "compatible" else "incompatible"))
```

**Qué reconocer:** aquí aparece la trampa que esta familia le tiende a cualquier contrato: **la
igualdad depende del tipo, y el tipo no está escrito en ninguna parte**. Perl la hace visible al
obligar a elegir entre `eq` (cadenas) y `==` (números), y Tcl hace lo mismo con `eq` frente a
`==`; Ruby, Lua y R deciden por ti según lo que hayas leído. Cuando el contrato entre dos
componentes se verifica en un lenguaje dinámico, la única defensa es la prueba: nada en el código
declara que `a` y `b` deban ser comparables. A cambio, escribir y cambiar esa verificación cuesta
minutos, que es exactamente por lo que el pegamento entre componentes suele acabar aquí.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final estado = v[0] == v[1] ? 'compatible' : 'incompatible';
  stdout.writeln('contrato=$estado');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash / AIR: la verificación de frontera,
// como función pura sobre los dos valores de contrato ya recibidos.
package {
    public class Contrato {
        public static function verificar(a:String, b:String):String {
            return "contrato=" + (a == b ? "compatible" : "incompatible");
        }
    }
}
```

**Qué reconocer:** en Dart `==` sobre `String` compara **contenido**, sin la coerción que hace el
`==` de JavaScript —donde `"5" == 5` es verdadero— y sin necesidad del `===` que JS tuvo que
inventar. Esa diferencia es pequeña en una línea y enorme en una frontera entre componentes: la
mitad de los contratos rotos en sistemas reales son un `5` que viajó como cadena por JSON y se
comparó contra un número. Declarar el tipo del contrato, como hace TypeScript o como hace Dart, no
elimina el problema en tiempo de ejecución, pero lo mueve a donde se puede leer.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+"))
    println("contrato=" + if (a == b) "compatible" else "incompatible")
}
```

### Scala

```scala
object Contrato extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"contrato=${if (a == b) "compatible" else "incompatible"}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)
println "contrato=${a == b ? 'compatible' : 'incompatible'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (str/split (str/trim (read-line)) #"\s+")]
  (println (str "contrato=" (if (= a b) "compatible" "incompatible"))))
```

**Qué reconocer:** en Java `==` sobre objetos compara **referencias**, no contenido, y hay que
escribir `equals`. Los cuatro primos corrigen esa herencia: Kotlin, Scala y Groovy hacen que `==`
llame a `equals` por debajo, y Clojure usa `=` con semántica de valor. La lección para el diseño de
contratos es que **la igualdad no es un detalle sintáctico sino parte de la especificación**: si dos
componentes acuerdan comparar identificadores, hay que decir si se comparan por valor o por
identidad. La ventaja práctica de esta familia sigue siendo la de siempre —los cuatro conviven en el
mismo proceso y comparten las bibliotecas de serialización, así que el contrato entre un componente
Kotlin y otro Scala puede ser un tipo compartido en vez de un JSON.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
type Frontera =
    | Compatible
    | Incompatible

let clasificar (a: string) (b: string) =
    if a = b then Compatible else Incompatible

let [| a; b |] =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)

match clasificar a b with
| Compatible -> printfn "contrato=compatible"
| Incompatible -> printfn "contrato=incompatible"
```

### VB.NET

```vbnet
Module Contrato
    Sub Main()
        Dim v = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("contrato=" & If(v(0) = v(1), "compatible", "incompatible"))
    End Sub
End Module
```

**Qué reconocer:** F# muestra aquí lo que aporta de verdad cuando hay contratos de por medio: la
**unión discriminada** `Frontera` convierte el resultado en un tipo con dos casos cerrados, y el
compilador avisa si el `match` deja alguno sin cubrir. El estado del contrato deja de ser una cadena
que alguien podría escribir mal y pasa a ser algo que el compilador vigila. VB.NET resuelve lo mismo
con un `If` ternario y una cadena suelta —más corto de escribir, sin ninguna garantía—. Como F# y C#
producen ensamblados intercambiables, ese modelado con tipos se puede introducir en un solo
componente del sistema sin obligar a nadie más a aprender F#.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string a, b;
    std::cin >> a >> b;
    std::cout << "contrato=" << (a == b ? "compatible" : "incompatible") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char bufA[64], bufB[64];
        scanf("%63s %63s", bufA, bufB);
        NSString *a = @(bufA);
        NSString *b = @(bufB);
        // Con NSString hay que usar isEqualToString: `==` compararía punteros.
        printf("contrato=%s\n", [a isEqualToString:b] ? "compatible" : "incompatible");
    }
    return 0;
}
```

**Qué reconocer:** en C comparar dos cadenas exige `strcmp`, porque `==` compara direcciones. C++
arregla eso sobrecargando `operator==` para `std::string`, y Objective-C **no** lo arregla: el
comentario del bloque no es decorativo, `a == b` compilaría sin avisos y devolvería casi siempre
falso. Es el mismo concepto de la clase visto desde abajo: una frontera entre componentes puede
fallar no porque los valores difieran, sino porque las dos partes entienden distinto qué significa
"iguales". Cuanto más bajo es el nivel del lenguaje, más explícita hay que hacer esa definición.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    const a = it.next().?;
    const b = it.next().?;
    const estado = if (std.mem.eql(u8, a, b)) "compatible" else "incompatible";
    try std.io.getStdOut().writer().print("contrato={s}\n", .{estado});
}
```

### Nim

```nim
import std/strutils

let v = stdin.readLine().splitWhitespace()
echo "contrato=", (if v[0] == v[1]: "compatible" else: "incompatible")
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto v = readln().strip().split();
    writeln("contrato=", v[0] == v[1] ? "compatible" : "incompatible");
}
```

**Qué reconocer:** Zig no tiene `==` para cadenas —una cadena es un *slice* de bytes y comparar dos
slices con `==` compararía puntero y longitud—, así que obliga a escribir `std.mem.eql`. Nim y D sí
sobrecargan `==` con semántica de valor. Los tres comparten la propiedad que importa para un
contrato entre componentes: al compilar a binario nativo sin runtime, **el componente que verifica la
frontera se despliega como un archivo**, sin que la máquina destino necesite intérprete ni máquina
virtual. El coste está en el otro lado: si el contrato viaja como JSON o Protobuf, las bibliotecas
de serialización de Zig, Nim y D son mucho menos maduras que las de Go, Java o .NET, y eso se paga
en tiempo de integración.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

estado(A, A, compatible) :- !.
estado(_, _, incompatible).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes0),
    exclude(==(""), Partes0, [A, B|_]),
    estado(A, B, Estado),
    format("contrato=~w~n", [Estado]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni condicionales: no puede imprimir "incompatible".
% Solo puede declarar los valores de contrato y derivar qué pares encajan.
contrato(cli, 5).
contrato(api, 5).
contrato(web, 6).

compatibles(X, Y) :- contrato(X, V), contrato(Y, V), X != Y.
```

**Qué reconocer:** en Prolog la comparación **no se escribe**: la primera cláusula usa la misma
variable `A` en los dos argumentos, así que la unificación falla sola cuando los valores difieren y
cae en la segunda cláusula. Es la forma más pura de expresar un contrato —la compatibilidad como
patrón, no como condición— y el corte `!` está ahí solo para no ofrecer las dos respuestas. Datalog
no llega tan lejos: sin negación ni efectos, puede decir qué pares **son** compatibles pero no puede
afirmar que un par no lo es. Esa asimetría es real y vale la pena verla, porque es la misma de SQL:
listar lo que cumple es fácil, demostrar la ausencia requiere otra construcción.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer dos valores, compararlos,
nombrar el resultado. Lo que cambia es qué significa "iguales" en cada uno y cuánto de esa definición
queda escrita en el código en vez de vivir en la cabeza de quien lo mantiene. En un sistema con
componentes en varios lenguajes, esa es exactamente la diferencia entre un contrato y una suposición.

⏮️ [Volver a la clase 166](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
