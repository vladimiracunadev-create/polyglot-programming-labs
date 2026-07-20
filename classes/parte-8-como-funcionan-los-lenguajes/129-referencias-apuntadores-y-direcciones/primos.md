# 🧬 El mismo programa en las familias de lenguajes — Clase 129

> [⬅️ Volver a la clase 129](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —llegar a un valor **indirectamente**, a través de un
índice— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo
por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `indice v0 v1 v2 ...` — el primer número es el índice, base 0
- **Salida** (stdout): `valor=<elemento en esa posición>`
- **Regla:** `valor = lista[indice]`

| stdin | esperado |
|---|---|
| `1 10 20 30` | `valor=20` |
| `0 5 6 7` | `valor=5` |
| `2 100 200 300` | `valor=300` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Estos lenguajes manejan **referencias**, no punteros: el nombre apunta a un objeto, pero la dirección
de ese objeto no está disponible para el programa.

### Ruby

```ruby
t = STDIN.read.split.map(&:to_i)
indice = t[0]
lista = t[1..]
# Ruby no expone direcciones. `lista.object_id` es un identificador de identidad,
# no una dirección: no se puede sumar, restar ni desreferenciar.
puts "valor=#{lista[indice]}"
```

### Perl

```perl
use Scalar::Util qw(refaddr);

my @t = split ' ', do { local $/; <STDIN> };
my $indice = shift @t;
my $ref = \@t;          # referencia al arreglo, no un puntero a su primer elemento
# refaddr($ref) devuelve el número interno del bloque, pero es de solo lectura:
# no hay aritmética de punteros ni forma de volver del número a los datos.
print "valor=$ref->[$indice]\n";
```

### Lua

```lua
local t = {}
for w in io.read("a"):gmatch("%S+") do t[#t + 1] = tonumber(w) end
local indice = t[1]
local lista = { table.unpack(t, 2) }
-- tostring(lista) imprime algo como "table: 0x5581...": es identidad para depurar,
-- no una dirección con la que se pueda operar. Las tablas de Lua son índice 1.
print("valor=" .. lista[indice + 1])
```

### Tcl

```tcl
set linea [gets stdin]
set datos [split $linea]
set indice [lindex $datos 0]
set lista [lrange $datos 1 end]
# Tcl no tiene punteros ni direcciones. Su indirección es por NOMBRE de variable:
# `upvar` y `set $nombre` permiten actuar sobre una variable dada por su nombre.
puts "valor=[lindex $lista $indice]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
indice <- v[1]
lista <- v[-1]
# R no expone direcciones y copia al modificar: `lista <- v[-1]` puede compartir
# memoria hasta que uno de los dos cambie. `tracemem()` solo revela si hubo copia.
cat(sprintf("valor=%d\n", lista[indice + 1]))
```

**Qué reconocer:** los cinco resuelven la indirección con un **índice sobre una colección**, nunca
con una dirección. La honestidad importa aquí: Ruby, Lua, Tcl y R no permiten ver dónde está el
objeto, y lo más cercano que ofrecen es la **identidad** (`object_id`, `tostring(t)`), útil para
saber si dos nombres apuntan a lo mismo pero inservible para calcular. Perl es el único de la familia
que sí devuelve el número de la dirección con `refaddr`, y aun así el camino es de ida: no existe
una operación que convierta ese número de vuelta en datos. Fíjate también en el desfase de base:
Lua y R indexan desde 1, así que el `indice` del contrato lleva un `+ 1`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final t = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final indice = t[0];
  final lista = t.sublist(1);
  // Dart maneja referencias. `identityHashCode(lista)` es lo más cercano a una
  // dirección, y solo sirve para comparar identidad.
  print('valor=${lista[indice]}');
}
```

### ActionScript 3

```actionscript
package {
    // El reproductor Flash no tiene stdin ni expone direcciones de memoria:
    // la entrada llega como cadena y la indirección es índice sobre un Array.
    public class Indirecto {
        public static function valor(entrada:String):String {
            var t:Array = entrada.split(" ");
            var indice:int = int(t[0]);
            var lista:Array = t.slice(1);
            return "valor=" + int(lista[indice]);
        }
    }
}
```

**Qué reconocer:** en esta familia el concepto de puntero directamente no existe en el lenguaje: los
objetos se pasan por referencia y el motor puede moverlos cuando compacta el heap, así que una
dirección estable sería una mentira. La única ventana a la memoria cruda es `ArrayBuffer` y sus
vistas tipadas (`Int32Array`), donde el "puntero" pasa a ser un **desplazamiento dentro del búfer** —
el mismo truco que usa ActionScript con `ByteArray`—. Es indirección real, pero acotada a una región
que el motor controla.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El recolector **mueve** los objetos al
compactar; por eso la máquina virtual no puede prometer una dirección estable a nadie.

### Kotlin

```kotlin
fun main() {
    val t = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val indice = t[0]
    val lista = t.drop(1)
    // La JVM no expone direcciones. System.identityHashCode(lista) es identidad,
    // no dirección: dos objetos distintos pueden incluso compartir ese número.
    println("valor=${lista[indice]}")
}
```

### Scala

```scala
object Indirecto {
  def main(args: Array[String]): Unit = {
    val t = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    val indice = t(0)
    val lista = t.tail
    println(s"valor=${lista(indice)}")
  }
}
```

### Groovy

```groovy
def t = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def indice = t[0]
def lista = t[1..-1]
println "valor=${lista[indice]}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [t (map #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))
      indice (first t)
      lista (vec (rest t))]
  (println (str "valor=" (nth lista indice))))
```

**Qué reconocer:** los cuatro comparten la misma referencia de la JVM, que es deliberadamente opaca:
no hay `&`, no hay `*` y no hay aritmética. Lo más cercano a una dirección es
`System.identityHashCode`, y conviene decir con claridad que **no es una dirección** —es un número de
identidad que la máquina virtual asigna y que sobrevive aunque el objeto se mueva—. Cuando de verdad
hace falta memoria cruda en la JVM se sale del lenguaje: `ByteBuffer.allocateDirect`, `VarHandle` o
el antiguo `sun.misc.Unsafe`. Clojure añade otra vuelta: `vec` construye un **vector persistente**,
un árbol de nodos compartidos, donde ni siquiera existe el bloque contiguo que un puntero recorrería.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let t =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int
let indice = t.[0]
let lista = t.[1..]
printfn "valor=%d" lista.[indice]
```

### VB.NET

```vbnet
Imports System.Linq

Module Indirecto
    Sub Main()
        Dim t = Console.ReadLine().
            Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries).
            Select(Function(s) Integer.Parse(s)).ToArray()
        Dim indice = t(0)
        ' VB.NET no tiene sintaxis de punteros: la memoria cruda del CLR solo se
        ' alcanza desde C# con `unsafe`/`fixed` o con System.Runtime.CompilerServices.
        Console.WriteLine("valor=" & t(indice + 1))
    End Sub
End Module
```

**Qué reconocer:** el CLR es un caso interesante porque **sí tiene punteros**, pero no para todos.
C#, el representante de la clase, puede escribir `int*` dentro de un bloque `unsafe` y anclar el
objeto con `fixed` para que el recolector no lo mueva mientras dure el puntero. F# y VB.NET no
ofrecen esa sintaxis: se quedan en referencias gestionadas. Ese `fixed` es la pista de lo que separa
un puntero de una referencia en un entorno con recolector: para tener una dirección hay que
prohibir primero que el objeto se mueva.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el puntero **es** la dirección: un número que
se guarda, se suma y se desreferencia.

### C++

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<long> v;
    long x;
    while (std::cin >> x) v.push_back(x);

    const long indice = v[0];
    const long *lista = v.data() + 1;      // puntero real y aritmética de punteros
    std::cout << "valor=" << *(lista + indice) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long v[1024];
        int n = 0;
        while (scanf("%ld", &v[n]) == 1) n++;

        long indice = v[0];
        long *lista = v + 1;              /* los punteros de C siguen intactos */
        NSNumber *boxed = @(*(lista + indice));  /* el objeto sí lleva conteo de referencias */
        printf("valor=%ld\n", [boxed longValue]);
    }
    return 0;
}
```

**Qué reconocer:** aquí sí se ve lo que el resto esconde. `v.data() + 1` y `v + 1` son la **misma**
expresión de la clase en C: un desplazamiento en unidades del tipo apuntado, no en bytes. C++ mantiene
el puntero crudo pero lo relega a lo que llama *vistas no propietarias* (`span`, `string_view`) y
reserva la propiedad para punteros inteligentes; la regla de la comunidad es que un `long*` puede
mirar, no poseer. Objective-C convive con las dos cosas en el mismo archivo: `lista + indice` es un
puntero de C sin más, mientras que el `NSNumber *` de al lado es una referencia con **conteo
automático de referencias (ARC)**, donde el compilador inserta las retenciones y liberaciones. Un
`*` que significa dos cosas distintas en dos líneas seguidas.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Punteros de verdad, pero
con reglas: Go los tiene sin aritmética, Rust los envuelve en referencias con tiempo de vida.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [4096]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");

    var datos: [256]i64 = undefined;
    var n: usize = 0;
    while (it.next()) |tok| : (n += 1) {
        datos[n] = try std.fmt.parseInt(i64, tok, 10);
    }

    const indice: usize = @intCast(datos[0]);
    // Zig distingue en el tipo: *T apunta a UN elemento, [*]T a muchos, []T lleva
    // además la longitud. Solo [*]T admite indexación y aritmética.
    const lista: [*]const i64 = datos[1..].ptr;
    try std.io.getStdOut().writer().print("valor={d}\n", .{lista[indice]});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let t = stdin.readLine().splitWhitespace().map(parseInt)
let indice = t[0]
let lista = t[1 .. ^1]
let p = unsafeAddr lista[indice]   # Nim sí da direcciones: addr / unsafeAddr
echo "valor=", p[]                 # y `p[]` desreferencia
```

### D

```d
import std.stdio, std.string, std.conv, std.array, std.algorithm;

void main() {
    auto t = readln().split().map!(to!long).array;
    const indice = t[0];
    long* lista = t.ptr + 1;   // D tiene GC y aun así permite punteros crudos
    writeln("valor=", *(lista + indice));
}
```

**Qué reconocer:** los tres tienen dirección real, y cada uno la acota de una forma distinta. Zig es
el más explícito de todos porque **la diferencia entra en el sistema de tipos**: `*i64` es un puntero
a un solo entero y no se puede indexar; para recorrer hace falta `[*]i64` o el slice `[]i64`, que
lleva la longitud consigo. Nim ofrece `addr` para lo que es mutable y `unsafeAddr` para lo que no, y
el nombre ya es la advertencia. D es el híbrido más franco de todos: tiene recolector de basura
—luego sus objetos se comportan como referencias— y aun así deja tomar `.ptr` y hacer aritmética, con
la responsabilidad de que el GC no sabe nada de ese puntero. Compara con Go, que tiene `*T` pero
prohibió la aritmética a propósito, y con Rust, donde `&` es una referencia verificada y el puntero
crudo solo existe dentro de `unsafe`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay direcciones porque no hay memoria en el
modelo: la indirección es una **junta**.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [Indice | Lista]),
    nth0(Indice, Lista, Valor),
    format("valor=~d~n", [Valor]).
```

### Datalog

```datalog
% Datalog no tiene punteros, direcciones ni E/S. La indirección se expresa como
% una junta entre la consulta y la relación: el índice es una clave, no un
% desplazamiento en memoria.
lista(0, 10).
lista(1, 20).
lista(2, 30).
consulta(1).

valor(V) :- consulta(I), lista(I, V).
```

**Qué reconocer:** Prolog **no expone memoria en absoluto**: `nth0` recorre la lista enlazada
término a término, y una variable no ligada es un hueco que la unificación llenará, no un puntero
nulo que puedas leer. Datalog es todavía más radical —solo hechos y reglas—, y su `valor(V) :-
consulta(I), lista(I, V)` es exactamente la junta que escribirías en SQL: la posición actúa como
clave. Ese es el punto que cierra la página: cuando el modelo es relacional, "seguir un puntero" y
"buscar por clave" son la misma operación descrita a dos niveles de abstracción distintos.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas a la pregunta *¿puedo ver dónde está el valor?*
Sí y con aritmética en C, C++, Objective-C, Zig, Nim y D. Sí pero atado en Rust, Go y el `unsafe` de
C#. No, y lo más cercano es un número de identidad, en Ruby, Perl, Lua, R, Tcl, la JVM entera y el
resto del CLR. En Prolog y Datalog la pregunta ni siquiera tiene sentido. Eso es lo transferible.

⏮️ [Volver a la clase 129](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
