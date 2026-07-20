# 🧬 El mismo programa en las familias de lenguajes — Clase 096

> [⬅️ Volver a la clase 096](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —recorrer una lista como pila (LIFO) y como cola
(FIFO)— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `pila=<orden LIFO> cola=<orden FIFO>`, con los valores unidos por `-`
- **Regla:** `pila = inverso(lista)`; `cola = lista`

| stdin | esperado |
|---|---|
| `1 2 3` | `pila=3-2-1 cola=1-2-3` |
| `5` | `pila=5 cola=5` |
| `1 2 3 4` | `pila=4-3-2-1 cola=1-2-3-4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los dos tiene un tipo `Pila`: el arreglo, con `append`/`pop` o `array_push`/`array_pop`, es
la pila. La familia entera repite ese gesto.

### Ruby

```ruby
nums = STDIN.read.split
pila = nums.dup
salida = []
salida << pila.pop until pila.empty?
puts "pila=#{salida.join('-')} cola=#{nums.join('-')}"
```

### Perl

```perl
my @nums = split ' ', do { local $/; <STDIN> };
my @pila = @nums;
my @salida;
push @salida, pop @pila while @pila;
print "pila=", join('-', @salida), " cola=", join('-', @nums), "\n";
```

### Lua

```lua
local pila = {}
for tok in io.read("a"):gmatch("%S+") do
  table.insert(pila, tok)
end
local cola = table.concat(pila, "-")
local salida = {}
while #pila > 0 do
  salida[#salida + 1] = table.remove(pila)
end
print("pila=" .. table.concat(salida, "-") .. " cola=" .. cola)
```

### Tcl

```tcl
set nums [regexp -all -inline {\S+} [read stdin]]
set pila $nums
set salida {}
while {[llength $pila] > 0} {
    lappend salida [lindex $pila end]
    set pila [lrange $pila 0 end-1]
}
puts "pila=[join $salida -] cola=[join $nums -]"
```

### R

```r
nums <- scan("stdin", what = character(), quiet = TRUE)
cat(sprintf("pila=%s cola=%s\n",
            paste(rev(nums), collapse = "-"),
            paste(nums, collapse = "-")))
```

**Qué reconocer:** Perl es el único que trae `push`, `pop`, `shift` y `unshift` como **verbos del
lenguaje** sobre `@array`; es literalmente la pila y la cola sin biblioteca. Ruby los tiene como
métodos del arreglo, y Lua vuelve a lo suyo: **no hay listas, solo la tabla**, y `table.insert` /
`table.remove` son las que la convierten en pila —`table.remove(t)` sin índice quita el último, que es
justo `pop`—. Tcl no muta: `lrange` devuelve una lista **nueva** cada vez, así que su "pila" es una
reconstrucción, no una estructura con estado. R ni lo intenta: piensa en vectores completos, y `rev`
sobre el vector entero es más natural que sacar elementos uno a uno.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:collection';
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  final cola = Queue<String>.of(nums);
  final pila = <String>[...nums];
  final salida = <String>[];
  while (pila.isNotEmpty) {
    salida.add(pila.removeLast());
  }
  print('pila=${salida.join('-')} cola=${cola.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin ni tipo Pila: el Array hace de pila con push/pop
// y de cola con push/shift, exactamente como en JavaScript.
package {
    public class PilaCola {
        public static function procesar(nums:Array):String {
            var pila:Array = nums.concat();
            var salida:Array = [];
            while (pila.length > 0) {
                salida.push(pila.pop());
            }
            return "pila=" + salida.join("-") + " cola=" + nums.join("-");
        }
    }
}
```

**Qué reconocer:** ActionScript 3 y JavaScript comparten el `Array` con `push`/`pop`/`shift`/`unshift`,
y esa es toda la historia: no hay tipo dedicado ni lo hubo nunca. Dart sí añade `Queue` en
`dart:collection`, una lista doblemente enlazada con `removeFirst` en O(1) —lo que importa, porque
`shift` sobre un arreglo es O(n) al desplazar todos los elementos—, pero para la pila sigue usando la
lista normal con `removeLast`. Es el patrón que se repetirá en casi toda la página: **la cola justifica
un tipo propio, la pila casi nunca**.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java sí tiene `Deque`, y su documentación
recomienda `ArrayDeque` tanto para pila como para cola.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+"))
    val pila = ArrayDeque(nums)
    val salida = buildList {
        while (pila.isNotEmpty()) add(pila.removeLast())
    }
    println("pila=${salida.joinToString("-")} cola=${nums.joinToString("-")}")
}
```

### Scala

```scala
import scala.collection.mutable

object PilaCola extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").toList
  val pila = mutable.Stack.from(nums)
  val cola = mutable.Queue.from(nums)
  val salida = Iterator.fill(nums.size)(pila.pop()).mkString("-")
  println(s"pila=$salida cola=${cola.mkString("-")}")
}
```

### Groovy

```groovy
def nums = System.in.text.split(/\s+/).findAll { it }
def pila = new ArrayDeque<String>(nums)
def salida = []
while (pila) {
    salida << pila.removeLast()
}
println "pila=${salida.join('-')} cola=${nums.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (str/split (str/trim (slurp *in*)) #"\s+")
      pila (into '() nums)]
  (println (str "pila=" (str/join "-" pila)
                " cola=" (str/join "-" nums))))
```

**Qué reconocer:** Kotlin trae su **propio** `ArrayDeque` en `kotlin.collections` desde la 1.4, distinto
del de `java.util` y sin los métodos sincronizados heredados; Scala prefiere nombrar la intención con
`mutable.Stack` y `mutable.Queue`. Clojure resuelve el problema sin ninguna estructura mutable:
`(into '() nums)` apila elemento a elemento sobre una **lista enlazada**, y como `conj` sobre una lista
inserta por delante, el resultado ya sale en orden LIFO. Ahí está la clave del lenguaje: la pila no es
un tipo, es **el comportamiento de `conj`** —sobre lista añade al principio, sobre vector al final—, y
`peek`/`pop` funcionan sobre ambos respetando ese extremo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System.Collections.Generic

let nums = stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
let pila = Stack<string>(nums)
let cola = Queue<string>(nums)
let salida = [ while pila.Count > 0 do yield pila.Pop() ]
printfn "pila=%s cola=%s" (String.concat "-" salida) (String.concat "-" cola)
```

### VB.NET

```vbnet
Imports System.Collections.Generic

Module PilaCola
    Sub Main()
        Dim nums = Console.ReadLine().Split(" "c, StringSplitOptions.RemoveEmptyEntries)
        Dim pila As New Stack(Of String)(nums)
        Dim cola As New Queue(Of String)(nums)
        Dim salida As New List(Of String)
        While pila.Count > 0
            salida.Add(pila.Pop())
        End While
        Console.WriteLine("pila=" & String.Join("-", salida) & " cola=" & String.Join("-", cola))
    End Sub
End Module
```

**Qué reconocer:** .NET es de las pocas plataformas con `Stack(Of T)` y `Queue(Of T)` **separados y con
nombre propio**, y ambos se construyen directamente desde una colección, lo que ahorra el bucle de
carga. Ojo con un detalle que este ejercicio esconde: recorrer un `Stack(Of T)` con `For Each` ya
devuelve los elementos en orden LIFO sin sacarlos. En F# lo idiomático sería la lista inmutable —`::`
añade por delante y hace de `push` sin mutar nada—; aquí se usan los tipos de .NET para que la
comparación con VB.NET sea directa, y el `[ while ... do yield ... ]` muestra cómo F# envuelve un bucle
imperativo dentro de una expresión que produce una lista.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C la pila es un arreglo más un índice `tope`, y no
hay nada más.

### C++

```cpp
#include <iostream>
#include <stack>
#include <queue>
#include <string>

int main() {
    std::stack<std::string> pila;
    std::queue<std::string> cola;
    std::string t;
    while (std::cin >> t) {
        pila.push(t);
        cola.push(t);
    }

    std::string sp, sc;
    while (!pila.empty()) {
        if (!sp.empty()) sp += '-';
        sp += pila.top();
        pila.pop();
    }
    while (!cola.empty()) {
        if (!sc.empty()) sc += '-';
        sc += cola.front();
        cola.pop();
    }
    std::cout << "pila=" << sp << " cola=" << sc << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *linea = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile]
                encoding:NSUTF8StringEncoding];
        NSMutableArray<NSString *> *cola = [NSMutableArray array];
        for (NSString *t in [linea componentsSeparatedByCharactersInSet:
                             [NSCharacterSet whitespaceAndNewlineCharacterSet]]) {
            if (t.length > 0) [cola addObject:t];
        }
        NSMutableArray<NSString *> *pila = [cola mutableCopy];
        NSMutableArray<NSString *> *salida = [NSMutableArray array];
        while (pila.count > 0) {
            [salida addObject:pila.lastObject];
            [pila removeLastObject];
        }
        printf("pila=%s cola=%s\n",
               [salida componentsJoinedByString:@"-"].UTF8String,
               [cola componentsJoinedByString:@"-"].UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** `std::stack` y `std::queue` no son contenedores sino **adaptadores**: envuelven un
`deque` y solo dejan asomar las operaciones legales, por eso `pila.top()` existe pero `pila[1]` no
compila. La restricción es el producto —el tipo hace imposible saltarse la disciplina LIFO—, algo que
un arreglo con `pop_back` nunca garantizaría. Y fíjate en que `pop()` **no devuelve** el elemento: hay
que leer con `top()` y quitar con `pop()`, una decisión deliberada por seguridad ante excepciones.
Objective-C no tiene ninguno de los dos: `NSMutableArray` con `addObject` / `removeLastObject` es todo
lo que hay, igual que en la familia de scripting.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go usa el *slice* con
`append` y reslicing; Rust usa `Vec` para pila y `VecDeque` para cola.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    var pila = std.ArrayList([]const u8).init(gpa.allocator());
    defer pila.deinit();

    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    while (it.next()) |tok| try pila.append(tok);

    const out = std.io.getStdOut().writer();
    try out.writeAll("pila=");
    var i = pila.items.len;
    while (i > 0) : (i -= 1) {
        try out.writeAll(pila.items[i - 1]);
        if (i > 1) try out.writeByte('-');
    }
    try out.writeAll(" cola=");
    for (pila.items, 0..) |x, j| {
        if (j > 0) try out.writeByte('-');
        try out.writeAll(x);
    }
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/[strutils, algorithm]

let cola = stdin.readLine().splitWhitespace()
var pila = cola
reverse(pila)
echo "pila=", pila.join("-"), " cola=", cola.join("-")
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto cola = readln().strip().split();
    string[] pila = cola.dup;
    string[] salida;
    while (pila.length) {
        salida ~= pila[$ - 1];
        pila = pila[0 .. $ - 1];
    }
    writeln("pila=", salida.join("-"), " cola=", cola.join("-"));
}
```

**Qué reconocer:** en los tres la pila es el arreglo dinámico y nada más: `ArrayList` en Zig tiene
`append` y `pop` y ahí acaba la discusión, exactamente como el `Vec` de Rust. D enseña la mecánica al
desnudo —`~=` añade al final y `pila[0 .. $ - 1]` "saca" el último devolviendo una **rebanada** de la
misma memoria, sin copiar—, que es el mismo truco del *reslicing* de Go. La cola es otra cosa: quitar
por delante de un arreglo obliga a desplazar todo, y por eso Rust necesita `VecDeque` y Nim tiene
`std/deques`. Aquí no hace falta porque solo recorremos, pero es la razón por la que en esta familia
existe un tipo para la cola y no para la pila.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Una tabla no tiene orden: hay que declararlo con
una columna de posición y pedirlo con `ORDER BY`.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Nums),
    reverse(Nums, Pila),
    atomic_list_concat(Pila, '-', SP),
    atomic_list_concat(Nums, '-', SC),
    format("pila=~w cola=~w~n", [SP, SC]).
```

### Datalog

```datalog
% Datalog no tiene E/S, estructuras mutables ni orden de evaluación: no hay push ni pop.
% La posición debe declararse como dato, y la "pila" es la misma relación con el
% índice invertido.
elem(1, 1).
elem(2, 2).
elem(3, 3).
largo(3).

cola(I, X) :- elem(I, X).
pila(J, X) :- elem(I, X), largo(N), J = N - I + 1.
```

**Qué reconocer:** la lista de Prolog **es** una pila: `[Cabeza|Resto]` desestructura por el extremo
izquierdo, que es a la vez `peek` y `pop`, y construir `[X|Resto]` es `push`. No hay operación, solo
notación —el mismo lugar donde Clojure pone `conj` sobre lista—. Lo que Prolog no puede hacer es sacar
por el otro extremo en tiempo constante, y por eso una cola eficiente se implementa con dos listas.
Datalog llega al límite: sin efectos ni estado, "sacar de la pila" no significa nada, y lo único que
queda es lo mismo que hace SQL —guardar el índice como columna y reordenarlo con una regla—.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y un resultado que sorprende: casi ninguno tiene un tipo `Pila`.
La pila es el arreglo dinámico usado por un extremo, y solo C++, .NET, Java y Scala se molestan en
darle nombre propio. La cola sí lo merece más a menudo, porque quitar por delante de un arreglo cuesta.
Reconocer eso te ahorra buscar en la biblioteca estándar un tipo que casi nunca está.

⏮️ [Volver a la clase 096](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
