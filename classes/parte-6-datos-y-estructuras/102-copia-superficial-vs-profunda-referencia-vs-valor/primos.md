# 🧬 El mismo programa en las familias de lenguajes — Clase 102

> [⬅️ Volver a la clase 102](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —copiar una lista, tocar la copia y comprobar que el
original sigue intacto— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El programa es corto, pero la pregunta que responde es la que más errores produce en producción:
cuando escribo `copia = original`, ¿acabo de duplicar los datos o solo he puesto otro nombre a los
mismos datos?

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `original=<lista> copia=<lista con el último cambiado a 99>`, con los
  elementos unidos por `-`
- **Regla:** copiar la lista, asignar `99` al último elemento de la copia, dejar el original intacto

| stdin | esperado |
|---|---|
| `1 2 3` | `original=1-2-3 copia=1-2-99` |
| `5 5` | `original=5-5 copia=5-99` |
| `7` | `original=7 copia=99` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Las listas viven en el montón y las variables guardan referencias; por eso casi todos necesitan pedir
la copia explícitamente.

### Ruby

```ruby
nums = STDIN.gets.split.map(&:to_i)
copia = nums.dup   # dup es superficial; la copia profunda se pide con Marshal
copia[-1] = 99
puts "original=#{nums.join('-')} copia=#{copia.join('-')}"
```

### Perl

```perl
my $linea = <STDIN>;
chomp $linea;
my @nums = split ' ', $linea;
my @copia = @nums;   # asignar un arreglo lo copia; con referencias haría falta Storable::dclone
$copia[-1] = 99;
printf "original=%s copia=%s\n", join('-', @nums), join('-', @copia);
```

### Lua

```lua
local linea = io.read("l")
local nums = {}
for s in linea:gmatch("%S+") do nums[#nums + 1] = tonumber(s) end
local copia = {}
for i, v in ipairs(nums) do copia[i] = v end  -- Lua no trae ninguna función de copia de tablas
copia[#copia] = 99
print("original=" .. table.concat(nums, "-") .. " copia=" .. table.concat(copia, "-"))
```

### Tcl

```tcl
gets stdin linea
set nums [split [string trim $linea]]
set copia $nums          ;# las listas de Tcl son valores: se duplican al escribir en ellas
lset copia end 99
puts "original=[join $nums -] copia=[join $copia -]"
```

### R

```r
nums <- as.integer(strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]])
copia <- nums            # R tiene semántica de valor: la copia real ocurre al modificar
copia[length(copia)] <- 99
cat(sprintf("original=%s copia=%s\n",
            paste(nums, collapse = "-"), paste(copia, collapse = "-")))
```

**Qué reconocer:** los cinco escriben algo parecido a `copia = original`, pero **tres de ellos
mienten y dos dicen la verdad**. Ruby es el más representativo del grupo: `nums.dup` copia solo el
primer nivel, así que si la lista contuviera listas, ambas versiones compartirían las de dentro; para
la copia profunda no hay operador —hay que serializar y deserializar con
`Marshal.load(Marshal.dump(nums))`, que es exactamente lo que hace `Storable::dclone` en Perl—. Perl
añade su propia trampa: los **arreglos** se copian al asignarlos, pero las **referencias** a arreglos
no, y como el código idiomático de Perl usa referencias por todas partes, `dclone` acaba siendo
imprescindible. Lua es el extremo de la austeridad: no existe ninguna función de copia en la
biblioteca estándar, ni superficial ni profunda; se escribe el bucle. Tcl y R son los dos que dicen
la verdad: sus valores tienen semántica de **copia al escribir**, así que `set copia $nums` y
`copia <- nums` producen una copia lógica de verdad y el intérprete solo duplica la memoria cuando
alguien modifica una de las dos. Se paga en tiempo de ejecución lo que en Ruby se paga en atención.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Todo objeto es una referencia y la copia superficial se escribe con azúcar sintáctico.

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final copia = List<int>.from(nums);  // copia superficial explícita
  copia[copia.length - 1] = 99;
  print('original=${nums.join('-')} copia=${copia.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la copia sobre un Array dado.
package {
    public class Copia {
        public static function demo(nums:Array):String {
            var copia:Array = nums.slice();  // slice() copia superficialmente, igual que en JavaScript
            copia[copia.length - 1] = 99;
            return "original=" + nums.join("-") + " copia=" + copia.join("-");
        }
    }
}
```

**Qué reconocer:** ActionScript 3 conserva el `slice()` de JavaScript con la misma semántica exacta
—copia el arreglo, comparte los objetos que contiene— y el mismo truco histórico de usarlo sin
argumentos para duplicar. Dart hace lo mismo con un nombre más explícito, `List.from`, y añade el
tipo: `List<int>.from` deja claro qué se está duplicando. En ambas la copia profunda sigue sin
existir en el lenguaje; en Dart lo habitual es escribir un constructor de copia a mano o pasar por
JSON, el mismo `structuredClone` que JavaScript solo consiguió estandarizar en 2022.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). `Object.clone()` es superficial, `Cloneable` es
una interfaz vacía, y la comunidad lleva veinte años recomendando no usar ninguna de las dos.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val copia = nums.toMutableList()  // la lista de origen es de solo lectura; esta es otra lista
    copia[copia.size - 1] = 99
    println("original=${nums.joinToString("-")} copia=${copia.joinToString("-")}")
}
```

### Scala

```scala
object Copia extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).toVector
  val copia = nums.updated(nums.length - 1, 99)  // no muta nada: devuelve un vector nuevo
  println(s"original=${nums.mkString("-")} copia=${copia.mkString("-")}")
}
```

### Groovy

```groovy
def nums = System.in.newReader().readLine().trim().split(/\s+/).collect { it.toInteger() }
def copia = new ArrayList(nums)  // clone() y este constructor copian solo el primer nivel
copia[-1] = 99
println("original=${nums.join('-')} copia=${copia.join('-')}")
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (mapv #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))
      ;; no hay nada que copiar: assoc devuelve un vector nuevo que comparte el resto
      copia (assoc nums (dec (count nums)) 99)]
  (println (str "original=" (str/join "-" nums) " copia=" (str/join "-" copia))))
```

**Qué reconocer:** los cuatro comparten montón y recolector con Java, pero cada uno esquiva
`clone()` de una forma distinta. Groovy es el que más se le parece: `new ArrayList(nums)` es una
copia superficial de manual, con la misma advertencia de siempre —los elementos son los mismos
objetos—. Kotlin cambia el enfoque desde el sistema de tipos: separa `List` (solo lectura) de
`MutableList`, así que `toMutableList()` no es tanto "copiar" como "pedir una versión modificable", y
el original queda protegido por el tipo antes que por la copia. Scala y Clojure eliminan la pregunta:
sus colecciones son **persistentes**, de modo que `updated` y `assoc` devuelven una estructura nueva
que **comparte internamente** casi toda la memoria con la anterior. No hay copia superficial ni
profunda porque no hay mutación de la que protegerse: es la respuesta más radical de la página, y la
única que hace que copiar sea gratis.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR distingue `struct` (semántica de valor: se
copia al asignar) de `class` (semántica de referencia), y `Array.Clone()` es superficial.

### F\#

```fsharp
let nums = stdin.ReadLine().Trim().Split(' ') |> Array.map int
let copia = Array.copy nums  // los arreglos de .NET son mutables y compartidos: hay que copiar
copia.[copia.Length - 1] <- 99
printfn "original=%s copia=%s"
    (nums |> Array.map string |> String.concat "-")
    (copia |> Array.map string |> String.concat "-")
```

### VB.NET

```vbnet
Module Copia
    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Dim nums(p.Length - 1) As Integer
        For i = 0 To p.Length - 1
            nums(i) = Integer.Parse(p(i))
        Next
        Dim copia = DirectCast(nums.Clone(), Integer())  ' Clone() es copia superficial
        copia(copia.Length - 1) = 99
        Console.WriteLine("original=" & String.Join("-", nums) & " copia=" & String.Join("-", copia))
    End Sub
End Module
```

**Qué reconocer:** VB.NET usa el mismo `Array.Clone()` que C# y hereda su letra pequeña: devuelve
`Object`, hay que convertirlo, y solo copia el primer nivel —un `Integer()` queda duplicado de
verdad, un arreglo de objetos comparte los elementos—. F# muestra el contraste dentro de la misma
plataforma: usa `Array.copy` cuando toca un arreglo, porque los arreglos de .NET son el único rincón
mutable que F# no puede disimular, pero su tipo de colección idiomático es la **lista inmutable**,
donde añadir un elemento no copia nada y el problema desaparece. En .NET el reparto no lo decide el
lenguaje sino la clase: por eso los `record` modernos traen `with`, que produce una copia
superficial con un campo cambiado, exactamente el `updated` de Scala.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C la copia se escribe elemento a elemento o con
`memcpy`; nada la hace por ti.

### C++

```cpp
#include <iostream>
#include <string>
#include <vector>

static std::string unir(const std::vector<long>& v) {
    std::string s;
    for (size_t i = 0; i < v.size(); ++i) {
        if (i) s += '-';
        s += std::to_string(v[i]);
    }
    return s;
}

int main() {
    std::vector<long> nums;
    long x;
    while (std::cin >> x) nums.push_back(x);
    std::vector<long> copia = nums;  // en C++ la asignación copia de verdad: semántica de valor
    copia.back() = 99;
    std::cout << "original=" << unir(nums) << " copia=" << unir(copia) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSMutableArray *nums = [NSMutableArray array];
        long x;
        while (scanf("%ld", &x) == 1) [nums addObject:@(x)];
        NSMutableArray *copia = [nums mutableCopy];  // mutableCopy es superficial: comparte objetos
        copia[copia.count - 1] = @99;
        printf("original=%s copia=%s\n",
               [[nums componentsJoinedByString:@"-"] UTF8String],
               [[copia componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** C++ es la excepción de toda esta página y conviene subrayarlo: **es el único que
copia por defecto**. `std::vector<long> copia = nums;` invoca el constructor de copia y duplica los
elementos sin que nadie lo pida —al revés que Python, Java, JavaScript, Ruby y casi todos los
demás—. Y como el constructor de copia se define por clase, la copia es tan profunda como el autor
del tipo decida: si el `vector` contuviera `vector`, la duplicación bajaría hasta el fondo sola. El
precio es la copia accidental —de ahí que la comunidad viva pasando `const&` y que C++11 añadiera la
semántica de movimiento para evitarla—. Objective-C se queda en el modelo clásico: los objetos son
punteros, `copy` y `mutableCopy` duplican solo el primer nivel, y la copia profunda se pide
serializando con `NSKeyedArchiver` —el `Marshal` de Ruby con otro nombre—.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y sin
recolector: el momento y el coste de cada copia son visibles en el código.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const alloc = gpa.allocator();
    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;

    var nums = std.ArrayList(i64).init(alloc);
    defer nums.deinit();
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    while (it.next()) |t| try nums.append(try std.fmt.parseInt(i64, t, 10));

    const copia = try alloc.dupe(i64, nums.items);  // copiar exige nombrar quién reserva la memoria
    defer alloc.free(copia);
    copia[copia.len - 1] = 99;

    const out = std.io.getStdOut().writer();
    try out.writeAll("original=");
    for (nums.items, 0..) |v, i| {
        if (i > 0) try out.writeAll("-");
        try out.print("{d}", .{v});
    }
    try out.writeAll(" copia=");
    for (copia, 0..) |v, i| {
        if (i > 0) try out.writeAll("-");
        try out.print("{d}", .{v});
    }
    try out.writeAll("\n");
}
```

### Nim

```nim
import std/[strutils, sequtils]

let nums = stdin.readLine().splitWhitespace().map(parseInt)
var copia = nums   ## los seq de Nim tienen semántica de valor: asignar ya copia
copia[^1] = 99
echo "original=", nums.join("-"), " copia=", copia.join("-")
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto nums = readln().split().map!(to!long).array;
    auto copia = nums.dup;  // sin dup ambos nombres verían exactamente la misma memoria
    copia[$ - 1] = 99;
    writeln("original=", nums.map!(to!string).join("-"),
            " copia=", copia.map!(to!string).join("-"));
}
```

**Qué reconocer:** las tres respuestas son distintas y las tres son coherentes con la filosofía de
cada lenguaje. Zig no oculta nada: copiar es `alloc.dupe`, que **exige decir con qué asignador** se
reserva la memoria y obliga a liberarla, así que ninguna copia ocurre por accidente ni sin dueño.
D hereda de C los *slices*, que son una vista sobre memoria compartida: asignar un arreglo a otro
nombre no copia nada, y `dup` es la palabra que pide la duplicación real —olvidarla es el error
clásico de la familia, porque el código compila y las dos variables se pisan—. Nim va al otro
extremo: sus `seq` tienen semántica de valor y `var copia = nums` **ya copia**, igual que en C++,
mientras que los `ref` siguen compartiendo. Rust, el representante del núcleo, cierra el trío
haciendo que el compilador lo impida: sin `clone()` el original quedaría movido y no podrías
imprimirlo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay variables que se modifiquen, así que no
hay nada que copiar: solo relaciones derivadas de otras.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    append(Resto, [_], Nums),       % separar el último elemento
    append(Resto, [99], Copia),     % construir una lista nueva; nada se muta
    atomic_list_concat(Nums, '-', TextoOrig),
    atomic_list_concat(Copia, '-', TextoCopia),
    format("original=~w copia=~w~n", [TextoOrig, TextoCopia]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni mutación: la copia es otra relación derivada, no un objeto nuevo.
original(1, 1).
original(2, 2).
original(3, 3).

ultima_pos(3).

copia(P, V) :- original(P, V), not ultima_pos(P).
copia(P, 99) :- ultima_pos(P).
```

**Qué reconocer:** en Prolog la pregunta de la clase **no se puede formular**: los términos son
inmutables, no existe "modificar el último elemento", y lo único que se puede hacer es construir una
lista nueva con `append`. Por eso el original nunca corre peligro —no hay copia superficial porque no
hay mutación que la haga fallar— y, de paso, el intérprete comparte internamente la cola común de
ambas listas, la misma optimización que usan las estructuras persistentes de Clojure. Datalog lo
lleva al extremo declarativo: `copia` no es un dato sino una **regla** que dice cómo derivar cada
tupla a partir de `original`, y la relación se recalcula en vez de almacenarse. Es exactamente lo que
hace una vista en SQL, y es la razón por la que la distinción superficial/profunda simplemente no
aparece en esta familia.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo gesto —`copia = original`— y tres respuestas incompatibles: no copia nada
(Ruby, Java, JavaScript, D), copia el primer nivel (`dup`, `clone`, `slice`, `mutableCopy`) o copia
de verdad (C++, Nim, Tcl, R). Y por encima de las tres, la salida elegante: si los datos son
inmutables —Clojure, Scala, Prolog— la pregunta desaparece. Saber en qué grupo cae el lenguaje que
tienes delante es lo transferible.

⏮️ [Volver a la clase 102](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
