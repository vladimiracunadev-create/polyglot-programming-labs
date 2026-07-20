# 🧬 El mismo programa en las familias de lenguajes — Clase 128

> [⬅️ Volver a la clase 128](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —construir en el heap una lista cuyo tamaño no se
conoce hasta ejecutar— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (n ≥ 1)
- **Salida** (stdout): `lista=<n-(n-1)-...-1>`
- **Regla:** construir dinámicamente una lista con los valores de `n` a `1` y unirlos con guiones

| stdin | esperado |
|---|---|
| `3` | `lista=3-2-1` |
| `1` | `lista=1` |
| `5` | `lista=5-4-3-2-1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Aquí **todo** vive en el heap y nadie lo menciona: la lista crece sola, el runtime duplica el bloque
cuando se llena y libera cuando ya nadie mira.

### Ruby

```ruby
n = STDIN.gets.to_i
lista = []
n.downto(1) { |i| lista << i }
puts "lista=#{lista.join('-')}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my @lista;
push @lista, $_ for reverse 1 .. $n;
print "lista=", join('-', @lista), "\n";
```

### Lua

```lua
local n = io.read("n")
local lista = {}
for i = n, 1, -1 do
  lista[#lista + 1] = i   -- la tabla duplica su parte de arreglo al llenarse
end
print("lista=" .. table.concat(lista, "-"))
```

### Tcl

```tcl
gets stdin n
set lista {}
for {set i $n} {$i >= 1} {incr i -1} {
    lappend lista $i
}
puts "lista=[join $lista -]"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
lista <- seq(n, 1)   # vector completo de una vez; crecer un vector en bucle copia todo
cat(sprintf("lista=%s\n", paste(lista, collapse = "-")))
```

**Qué reconocer:** en los cinco el bloque de memoria es invisible y su tamaño se decide en ejecución;
lo que cambia es **cuánto cuesta crecer**. Ruby, Perl, Lua y Tcl amortizan el crecimiento duplicando
la capacidad, así que añadir un elemento es barato en promedio. R es el contraejemplo idiomático:
crecer un vector en un bucle **copia el vector entero en cada paso**, por eso la comunidad reserva
de golpe (`seq`, `vector("integer", n)`) en vez de ir añadiendo. Y ninguno de los cinco ofrece un
`free`: el momento de la liberación no está en tus manos.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final lista = <int>[];
  for (var i = n; i >= 1; i--) {
    lista.add(i);
  }
  print('lista=${lista.join('-')}');
}
```

### ActionScript 3

```actionscript
package {
    // El reproductor Flash no tiene stdin: la lista se construye a partir de un n dado.
    public class Heap {
        public static function lista(n:int):String {
            var xs:Array = [];          // Array dinámico en el heap del reproductor
            for (var i:int = n; i >= 1; i--) {
                xs.push(i);
            }
            return "lista=" + xs.join("-");
        }
    }
}
```

**Qué reconocer:** los dos heredan el heap generacional de un motor de JavaScript (V8 en Dart nativo
no, pero sí el mismo modelo de objetos jóvenes que mueren pronto). El detalle propio de la familia es
que el arreglo es **un objeto más**: no hay diferencia entre reservar una lista y crear cualquier
otro valor. ActionScript conserva un rastro de la preocupación por el coste con su tipo
`Vector.<int>`, que sí es un bloque homogéneo y compacto, frente al `Array` genérico de este ejemplo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Un solo heap gestionado por el recolector, con
generaciones y con la reserva reducida casi a mover un puntero.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val lista = ArrayList<Int>(n)   // capacidad inicial: evita las copias al crecer
    for (i in n downTo 1) lista.add(i)
    println("lista=${lista.joinToString("-")}")
}
```

### Scala

```scala
object Heap {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val lista = (1 to n).reverse
    println(s"lista=${lista.mkString("-")}")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def lista = (n..1).collect()
println "lista=${lista.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; `range` es perezosa: no reserva los n elementos hasta que alguien los recorre.
(let [n (Long/parseLong (str/trim (read-line)))
      lista (range n 0 -1)]
  (println (str "lista=" (str/join "-" lista))))
```

**Qué reconocer:** los cuatro reservan en el mismo heap y todos acaban en un `ArrayList` o en un
arreglo de Java por debajo, pero la actitud cambia. Kotlin pasa la capacidad al constructor porque
sabe cuántos elementos vendrán. Scala construye un rango que solo se materializa al imprimir.
Clojure va más lejos con estructuras **persistentes**: sus listas comparten memoria entre versiones
en lugar de copiarse, algo que solo tiene sentido cuando un recolector se ocupa de decidir cuándo
muere el bloque compartido. Y ninguno expone la dirección del bloque: en la JVM el recolector puede
**mover** los objetos, así que una dirección estable ni siquiera existiría.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let lista = [ for i in n .. -1 .. 1 -> string i ]
printfn "lista=%s" (String.concat "-" lista)
```

### VB.NET

```vbnet
Imports System.Collections.Generic

Module Heap
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.ReadLine().Trim())
        Dim lista As New List(Of Integer)(n)
        For i As Integer = n To 1 Step -1
            lista.Add(i)
        Next
        Console.WriteLine("lista=" & String.Join("-", lista))
    End Sub
End Module
```

**Qué reconocer:** el CLR reparte en dos sitios y esa es su seña de identidad: `List(Of Integer)` es
un **tipo por referencia** que vive en el heap, pero los `Integer` que guarda son **tipos por valor**
almacenados en línea dentro del bloque, sin una caja por elemento. La JVM, en cambio, tendría que
envolver cada número en un `Integer` si usaras `List<Integer>`. F# añade la lista enlazada inmutable
de la tradición ML, que reserva una celda por elemento; su hermana eficiente en .NET es
`ResizeArray`, que es literalmente el mismo `List<T>` de VB.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el heap se nombra: `malloc` pide el bloque,
`free` lo devuelve, y entre medias eres tú quien lleva la cuenta.

### C++

```cpp
#include <iostream>
#include <vector>

int main() {
    long n;
    std::cin >> n;
    std::vector<long> lista;   // reserva en el heap; el destructor libera al salir
    lista.reserve(n);
    for (long i = n; i >= 1; i--) lista.push_back(i);

    std::cout << "lista=";
    for (std::size_t i = 0; i < lista.size(); i++) {
        if (i) std::cout << '-';
        std::cout << lista[i];
    }
    std::cout << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        NSMutableArray<NSNumber *> *lista = [NSMutableArray arrayWithCapacity:n];
        for (long i = n; i >= 1; i--) {
            [lista addObject:@(i)];   /* cada NSNumber lleva su conteo de referencias */
        }
        printf("lista=%s\n", [[lista componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** los dos podrían escribir el `malloc`/`free` de la clase tal cual, y ninguno de los
dos lo hace. C++ envuelve la reserva en un `std::vector`: el bloque sigue estando en el heap, pero el
destructor lo libera al salir del ámbito —eso es **RAII**, y es la razón por la que `new`/`delete`
explícitos se consideran hoy un olor a código en C++—. Objective-C elige la otra vía: **conteo de
referencias**, hoy insertado por el compilador con ARC, de modo que el `NSMutableArray` y cada
`NSNumber` se liberan cuando su contador llega a cero. Mismo heap, dos disciplinas distintas para
saber cuándo soltarlo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con una respuesta explícita a *quién* reserva y *quién* libera.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    // En Zig no existe un heap global implícito: el asignador es un valor que
    // se pasa como argumento, y quien reserva decide cuál usar.
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(usize, std.mem.trim(u8, linea, " \r"), 10);

    const lista = try allocator.alloc(usize, n);
    defer allocator.free(lista);
    for (lista, 0..) |*x, i| x.* = n - i;

    const out = std.io.getStdOut().writer();
    try out.writeAll("lista=");
    for (lista, 0..) |x, i| {
        if (i > 0) try out.writeAll("-");
        try out.print("{d}", .{x});
    }
    try out.writeAll("\n");
}
```

### Nim

```nim
import std/[strutils, sequtils]

let n = stdin.readLine().strip().parseInt()
var lista: seq[int] = @[]      # el seq vive en el heap; ARC lo libera al salir del ámbito
for i in countdown(n, 1):
  lista.add(i)
echo "lista=", lista.mapIt($it).join("-")
```

### D

```d
import std.stdio, std.string, std.conv, std.range, std.algorithm, std.array;

void main() {
    const n = readln().strip().to!long;
    auto lista = iota(n, 0, -1).array;   // el GC de D reserva; nadie libera a mano
    writeln("lista=", lista.map!(to!string).join("-"));
}
```

**Qué reconocer:** esta familia es la que mejor muestra que "reservar en el heap" no es una sola
cosa. Zig lo lleva al extremo con su rasgo más distintivo: **no hay un `malloc` global**, el
asignador es un valor corriente que se pasa como argumento, de modo que una biblioteca de Zig no
puede reservar a tus espaldas y tú puedes darle un asignador de arena, uno fijo sin heap, o el
`GeneralPurposeAllocator` que además detecta fugas. Nim reserva igual de dinámicamente pero desde
Nim 2 el compilador inserta los destructores con **ARC/ORC** —conteo de referencias con un ciclo
recolector opcional—, así que no escribes `free` ni pagas pausas de GC. D es el tercero en discordia:
tiene recolector de basura por defecto, lo que hace este código idéntico a un lenguaje de scripting,
pero permite marcar funciones `@nogc` y volver a `malloc`/`free` cuando el coste importa.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere; dónde vive el
resultado es asunto del motor.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    numlist(1, N, Asc),
    reverse(Asc, Desc),
    atomic_list_concat(Desc, '-', S),
    format("lista=~w~n", [S]).
```

### Datalog

```datalog
% Datalog no construye estructuras ni tiene E/S: no hay "lista" como objeto en
% memoria, solo una relación posición-valor que el motor deriva y almacena donde
% quiera. Se escribe con la aritmética de un motor tipo Soufflé.
n(3).

elemento(1, N) :- n(N).
elemento(P, V) :- elemento(P0, V0), P = P0 + 1, V = V0 - 1, V >= 1.
```

**Qué reconocer:** Prolog sí reserva en un heap —el suyo, con celdas de términos— y esa reserva es
invisible: `numlist` construye una lista enlazada de N celdas sin que aparezca ninguna palabra sobre
memoria. Lo característico es que la recuperación no la hace un recolector convencional sino el
**retroceso**: al deshacer una alternativa, el motor recorta el heap hasta la marca anterior de un
golpe. Datalog ni siquiera admite términos compuestos: no hay listas que reservar, solo tuplas en
relaciones, que es exactamente la renuncia que hace SQL al no dejarte decidir si una tabla temporal
cabe en memoria o va a disco.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una única pregunta de fondo: *¿quién decide cuándo se libera el
bloque?* Tú en C, el destructor en C++ y Nim, el contador en Objective-C, el recolector en la JVM, el
CLR y D, el asignador que tú elegiste en Zig, y nadie en Datalog porque no hay bloque. Eso es lo
transferible.

⏮️ [Volver a la clase 128](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
