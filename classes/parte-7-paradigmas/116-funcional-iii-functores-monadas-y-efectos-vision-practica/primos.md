# 🧬 El mismo programa en las familias de lenguajes — Clase 116

> [⬅️ Volver a la clase 116](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —duplicar un valor **solo si existe**, y decir `nada`
si no— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por
los diez lenguajes del núcleo.

Conviene nombrar las cosas sin misticismo. Un **functor** es un contenedor que sabe aplicar una
función a lo que lleva dentro sin que tú abras el envoltorio: eso es `map`. Una **mónada** añade una
segunda operación, `flatMap` (también llamada `bind` o `>>=`), que permite encadenar funciones que a
su vez devuelven el contenedor, sin acabar con envoltorios dentro de envoltorios. La
`for`-comprehension de Scala y las *computation expressions* de F\# no son otra cosa que azúcar
sintáctico sobre `flatMap`. Aquí varios primos son protagonistas: Scala tiene `Option` y
`for`-comprehension de verdad, F\# tiene `Option.map` y `Option.bind`, Nim trae `map` y `flatMap` en
`std/options`, y Clojure resuelve lo mismo con `some->` sin tipo ninguno.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>` si `n > 0`; `resultado=nada` en caso contrario
- **Regla:** `Option(n si n > 0).map(x -> 2x)`

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=nada` |
| `-3` | `resultado=nada` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno tiene un tipo `Option`: la ausencia es un valor especial (`None`, `null`, `nil`, `undef`) que
convive con todos los demás.

### Ruby

```ruby
n = STDIN.gets.to_i
opcion = n.positive? ? n : nil

# &. es el "map" del Maybe de Ruby: si el receptor es nil, no llama y devuelve nil.
resultado = opcion&.then { |x| x * 2 }
puts "resultado=#{resultado || 'nada'}"
```

### Perl

```perl
chomp(my $n = <STDIN>);
my $opcion = $n > 0 ? $n : undef;

# No hay propagación automática: hay que preguntar por `defined` antes de operar.
my $r = defined $opcion ? $opcion * 2 : undef;
printf "resultado=%s\n", $r // 'nada';   # // es el operador "definido-o"
```

### Lua

```lua
local n = io.read("n")
local opcion = n > 0 and n or nil     -- nil es la ausencia

-- `and` corta en cuanto el izquierdo es falso: ese cortocircuito hace de map.
local r = opcion and opcion * 2
print("resultado=" .. (r or "nada"))
```

### Tcl

```tcl
gets stdin n

# Tcl no tiene ningún valor nulo: la ausencia se modela como "la variable no existe".
if {$n > 0} {
    set opcion [expr {$n * 2}]
}
if {[info exists opcion]} {
    puts "resultado=$opcion"
} else {
    puts "resultado=nada"
}
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
opcion <- if (n > 0) n else NA_integer_

# NA se propaga sola por la aritmética: NA * 2 es NA, sin escribir ningún map.
r <- opcion * 2
cat(sprintf("resultado=%s\n", ifelse(is.na(r), "nada", as.character(r))))
```

**Qué reconocer:** Ruby y Perl reducen el `Maybe` a un **operador**: `&.` es `map` y `//` es
`getOrElse`, sin tipo ni contenedor de por medio. Lua es más pobre todavía —su `nil` sirve a la vez
de "ausente" y de "clave que no está en la tabla", así que no distingue "no hay valor" de "el valor
es nulo"— y aun así el cortocircuito de `and` hace el trabajo. Tcl es el caso extremo y el más
instructivo: **no existe el nulo**, la única forma de decir "no hay" es que la variable no esté, y
por eso la comprobación es `info exists` en vez de una comparación. R merece la atención especial: su
`NA` se propaga sola por toda la aritmética, lo cual es literalmente el comportamiento de un functor
aplicado sin que lo pidas. Es cómodo y es la causa de los fallos más silenciosos de R, porque un `NA`
que entra al principio de un cálculo sale al final sin que nadie avise.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  // El `?` forma parte del tipo: int? e int son tipos distintos y el compilador lo exige.
  final int? opcion = n > 0 ? n : null;
  final int? r = opcion == null ? null : opcion * 2;
  print("resultado=${r ?? 'nada'}");
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash. Y AS3 no tiene Option: `null` solo cabe en tipos
// por referencia, así que un `int` ausente obliga a renunciar al tipo y usar `*`.
package {
    public class Opcion {
        public static function resultado(n:int):String {
            var opcion:* = n > 0 ? n : null;
            var r:* = opcion == null ? null : opcion * 2;
            return "resultado=" + (r == null ? "nada" : r);
        }
    }
}
```

**Qué reconocer:** Dart trae **nulabilidad sólida** desde la versión 2.12: `int?` no es un `int` con
un aviso, es otro tipo, y el compilador no te deja multiplicarlo sin comprobar antes. Esa es la misma
disciplina que impone `Option[Int]` en Scala, pero metida en el sistema de tipos en lugar de en una
biblioteca —a cambio, `int??` no existe, mientras que `Option[Option[Int]]` sí—. AS3 enseña el mundo
anterior: los tipos por valor (`int`, `Number`, `Boolean`) **no admiten null**, de modo que para
expresar la ausencia hay que salirse del tipo con `*`. Perder el tipo para poder decir "no hay" es
exactamente el problema que `Option` vino a resolver.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java), que desde Java 8 tiene `Optional` con `map` y
`orElse` — un functor de verdad, aunque llegara tarde y solo para valores de retorno.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val opcion: Int? = if (n > 0) n else null
    // `let` sobre un tipo nulable es el map; `?:` (elvis) es el getOrElse.
    val r = opcion?.let { it * 2 }
    println("resultado=${r ?: "nada"}")
}
```

### Scala

```scala
object Opcion {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val opcion: Option[Int] = Option(n).filter(_ > 0)

    // La for-comprehension es azúcar de flatMap/map: esto compila a opcion.map(_ * 2).
    val r = for (x <- opcion) yield x * 2

    println(s"resultado=${r.fold("nada")(_.toString)}")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def opcion = n > 0 ? n : null
def r = opcion?.multiply(2)          // ?. propaga null por toda la cadena
println "resultado=${r ?: 'nada'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Integer/parseInt (str/trim (read-line)))
      opcion (when (pos? n) n)      ; `when` devuelve nil si la condición falla
      r (some-> opcion (* 2))]      ; some-> corta la cadena en cuanto aparece nil
  (println (str "resultado=" (or r "nada"))))
```

**Qué reconocer:** Scala es el único de los cuatro con un **tipo** `Option` y con
`for`-comprehension, y aquí se ve que la comprehension no tiene nada de místico:
`for (x <- opcion) yield x * 2` es otra forma de escribir `opcion.map(x => x * 2)`, y en cuanto
aparece un segundo generador pasa
a ser `flatMap`. Eso —envolver un valor y encadenar funciones que devuelven el mismo envoltorio— es
toda la definición de mónada que necesitas para trabajar. Kotlin, Groovy y Clojure eligen el atajo
barato: tipo nulable más operador de navegación segura (`?.`, `some->`), que da el comportamiento del
functor sin el contenedor. La diferencia se nota al anidar: `Option[Option[Int]]` distingue "no hay
respuesta" de "la respuesta es que no hay", y `Int??` ni siquiera se puede escribir. Fíjate también
en que `some->` de Clojure es una macro: sin tipos, la propagación tiene que ocurrir en tiempo de
compilación reescribiendo el código.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1), que usa `int?` (`Nullable<int>`) y comprueba
`HasValue` a mano.

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let opcion = if n > 0 then Some n else None

// Option.map es el functor; Option.bind es la mónada. La expresión de cálculo
// `option { let! x = opcion in ... }` es el equivalente a la for-comprehension.
let r = opcion |> Option.map (fun x -> x * 2)

printfn "resultado=%s" (r |> Option.map string |> Option.defaultValue "nada")
```

### VB.NET

```vbnet
Module Opcion
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        ' Nullable(Of Integer) es una estructura con HasValue: no tiene Map.
        Dim opcion As Integer? = If(n > 0, n, CType(Nothing, Integer?))
        Dim r As Integer? = If(opcion.HasValue, opcion.Value * 2, CType(Nothing, Integer?))
        Console.WriteLine("resultado=" & If(r.HasValue, r.Value.ToString(), "nada"))
    End Sub
End Module
```

**Qué reconocer:** F\# y VB.NET comparten runtime y sin embargo `Option<int>` y `Nullable(Of Integer)`
son cosas distintas, no dos nombres de lo mismo. `Nullable` es una estructura limitada a tipos por
valor y con los operadores aritméticos ya **elevados** por el compilador (`Nothing + 1` da `Nothing`),
pero sin `map`: la propagación es un privilegio de los operadores predefinidos, y en cuanto quieres
aplicar tu propia función tienes que escribir el `If`. `Option` de F\# es una unión discriminada
normal y corriente: funciona con cualquier tipo, se puede anidar, se puede recorrer con `match`, y
`map`/`bind` son funciones ordinarias de la biblioteca. Esa es la lección: el elevado automático es
comodidad para tres operadores; el functor es una herramienta que sirve para cualquier función que
escribas.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C la ausencia se comunica con un centinela —`-1`,
`NULL`, un `bool` extra— y nada obliga a comprobarla.

### C++

```cpp
#include <iostream>
#include <optional>

int main() {
    int n;
    std::cin >> n;
    std::optional<int> opcion = n > 0 ? std::optional<int>(n) : std::nullopt;

    // C++23 añade opcion.transform(f) y opcion.and_then(f) — map y flatMap.
    // Antes de C++23, la forma portable es la rama explícita:
    std::optional<int> r = opcion ? std::optional<int>(*opcion * 2) : std::nullopt;

    if (r) {
        std::cout << "resultado=" << *r << '\n';
    } else {
        std::cout << "resultado=nada\n";
    }
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        // Los primitivos no pueden ser nil: hay que envolverlos en NSNumber (boxing).
        NSNumber *opcion = n > 0 ? @(n) : nil;
        // Enviar un mensaje a nil es legal y devuelve nil/0: la propagación es del runtime.
        NSNumber *r = opcion ? @(opcion.intValue * 2) : nil;
        printf("resultado=%s\n", r ? r.stringValue.UTF8String : "nada");
    }
    return 0;
}
```

**Qué reconocer:** C++ tardó hasta C++17 en tener `std::optional` y hasta **C++23** en darle
`transform` y `and_then`, es decir, el contenedor llegó seis años antes que las operaciones que lo
hacen útil. Hasta entonces todo el mundo escribía el `if`, que es lo que ves arriba. Objective-C
resuelve lo mismo por un camino que no existe en ningún otro lenguaje de esta página: **mandar un
mensaje a `nil` no revienta**, devuelve cero, así que `[nil doubleIt]` propaga la ausencia sin
operador ni tipo. Es `Maybe` por accidente del runtime, y tiene el defecto correspondiente: el
compilador no puede avisarte de que olvidaste el caso, porque para él no hay ningún caso que tratar.
Compáralo con `Option` de Rust en el núcleo, donde el `match` es obligatorio.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust tiene `Option<T>`
con `map` en el lenguaje base; Go prefiere el segundo valor de retorno y el `if`.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);

    // ?i64 es un tipo del lenguaje, no de la biblioteca. No hay map: sin clausuras
    // no se puede pasar una función que capture, así que se desempaqueta con `if`.
    const opcion: ?i64 = if (n > 0) n else null;
    const out = std.io.getStdOut().writer();
    if (opcion) |x| {
        try out.print("resultado={d}\n", .{x * 2});
    } else {
        try out.print("resultado=nada\n", .{});
    }
}
```

### Nim

```nim
import std/[strutils, options, sugar]

let n = stdin.readLine().strip().parseInt()
let opcion = if n > 0: some(n) else: none(int)

# std/options trae map y flatMap: functor y mónada en la biblioteca estándar.
let r = opcion.map(x => x * 2).map(x => $x)
echo "resultado=", r.get("nada")
```

### D

```d
import std.stdio, std.string, std.conv, std.typecons;

void main() {
    const n = readln().strip().to!int;
    // Nullable!int es el envoltorio; la operación (apply) llegó mucho después.
    Nullable!int opcion = n > 0 ? nullable(n) : Nullable!int.init;
    auto r = opcion.isNull ? Nullable!int.init : nullable(opcion.get * 2);
    writefln("resultado=%s", r.isNull ? "nada" : r.get.to!string);
}
```

**Qué reconocer:** Zig pone el opcional **en el lenguaje** —`?i64` es sintaxis, no una plantilla— y
lo desempaqueta con captura de patrón (`if (opcion) |x|`), que es más seguro que cualquier
biblioteca; pero no tiene `map`, y no por descuido: `map` exige pasar una función que capture su
entorno, y Zig no tiene clausuras. Nim es el único de los tres donde el encadenamiento monádico se
escribe como tal, con `map` y `flatMap` en `std/options`. D tiene el envoltorio (`Nullable`) desde
hace mucho y las operaciones desde hace poco. La conclusión vale para toda la página: **tener un
tipo `Option` es barato; tener un `Option` que sea functor exige que el lenguaje tenga funciones de
primera clase capaces de capturar el entorno.**

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí la ausencia no es un valor guardado en una
variable: es una consulta que no devuelve filas.

### Prolog

```prolog
:- initialization(main, main).

% La ausencia es el fallo: si la regla no se cumple, sencillamente no hay solución.
doblado(N, R) :- N > 0, R is N * 2.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    (   doblado(N, R)
    ->  format("resultado=~d~n", [R])
    ;   format("resultado=nada~n", [])
    ).
```

### Datalog

```datalog
% Datalog no tiene E/S, ni efectos, ni valor nulo: la ausencia es "la tupla no está".
entrada(5).

doblado(R) :- entrada(N), N > 0, R = N * 2.
% Con entrada(0), consultar doblado(R) no devuelve ninguna fila. Eso es el `nada`.
```

**Qué reconocer:** esta es la familia donde el concepto de la clase cambia de forma, y merece la
pena verlo. Ni Prolog ni Datalog tienen `Option`, y no porque les falte: **no lo necesitan**, porque
la ausencia ya está en su modelo de ejecución. `Option[Int]` es, punto por punto, "una relación con
cero o una fila", y por eso SQL —el representante del núcleo— hace lo mismo: una consulta sin
resultados es `None`, y el `NULL` que se propaga por las expresiones es `map` aplicado
automáticamente, igual que el `NA` de R. La diferencia con Scala es que aquí **la ausencia no es un
valor que puedas guardar y pasar**: es una propiedad de la búsqueda. Por eso en Prolog el `->` no
sobra: hace falta traducir "el objetivo falló" a la palabra `nada` que exige el contrato, porque el
propio lenguaje no tiene ninguna palabra para eso.

---

## Y de vuelta a la clase

Veinte lenguajes y tres estrategias para lo mismo. Unos hacen de la ausencia un **valor** que
convive con los demás (`nil`, `null`, `undef`) y añaden operadores para no tropezar con él. Otros la
hacen un **tipo** distinto (`Option`, `int?`, `?i64`) y ponen al compilador a vigilar. Y los últimos
la hacen una **propiedad de la ejecución**: no hay respuesta porque no hay filas. `map` y `flatMap`
solo son los nombres de la costura entre esos tres mundos.

⏮️ [Volver a la clase 116](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
