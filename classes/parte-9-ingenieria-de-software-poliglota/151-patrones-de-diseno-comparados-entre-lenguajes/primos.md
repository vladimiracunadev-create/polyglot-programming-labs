# 🧬 El mismo programa en las familias de lenguajes — Clase 151

> [⬅️ Volver a la clase 151](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —elegir una operación por su nombre, es decir el
patrón **Estrategia**— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `estrategia a b`, con `estrategia` ∈ {`suma`, `resta`, `producto`}
- **Salida** (stdout): `resultado=<a estrategia b>`
- **Regla:** aplicar a `a` y `b` la estrategia elegida por su nombre

| stdin | esperado |
|---|---|
| `suma 3 4` | `resultado=7` |
| `resta 10 3` | `resultado=7` |
| `producto 5 6` | `resultado=30` |

Un aviso antes de empezar, porque es lo más valioso de esta página: **buena parte del catálogo GoF
desaparece cuando el lenguaje trae la característica de serie**. Estrategia es una función guardada
en una tabla en Lua, Clojure o F#; Singleton es simplemente un módulo en Ruby o Perl; Visitor se
vuelve innecesario en Scala y F# porque la coincidencia de patrones ya recorre el árbol; Iterator
está en el lenguaje desde el primer día. Un patrón es la cicatriz de algo que el lenguaje no sabía
hacer. En las veinte versiones siguientes verás cuántas cicatrices se borran.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En estos lenguajes la función es un valor cualquiera: se guarda en un diccionario y se llama desde
ahí. La jerarquía de clases `Estrategia` / `EstrategiaConcreta` del libro no aparece por ningún lado.

### Ruby

```ruby
ESTRATEGIAS = {
  "suma"     => ->(a, b) { a + b },
  "resta"    => ->(a, b) { a - b },
  "producto" => ->(a, b) { a * b }
}.freeze

nombre, a, b = STDIN.gets.split
puts "resultado=#{ESTRATEGIAS.fetch(nombre).call(a.to_i, b.to_i)}"
```

### Perl

```perl
use strict;
use warnings;

my %estrategias = (
    suma     => sub { $_[0] + $_[1] },
    resta    => sub { $_[0] - $_[1] },
    producto => sub { $_[0] * $_[1] },
);

my ($nombre, $a, $b) = split ' ', <STDIN>;
printf "resultado=%d\n", $estrategias{$nombre}->($a, $b);
```

### Lua

```lua
local estrategias = {
  suma     = function(a, b) return a + b end,
  resta    = function(a, b) return a - b end,
  producto = function(a, b) return a * b end,
}

local nombre, a, b = io.read("l"):match("(%a+)%s+(-?%d+)%s+(-?%d+)")
print(string.format("resultado=%d", estrategias[nombre](tonumber(a), tonumber(b))))
```

### Tcl

```tcl
proc suma {a b}     { expr {$a + $b} }
proc resta {a b}    { expr {$a - $b} }
proc producto {a b} { expr {$a * $b} }

gets stdin linea
lassign [split $linea] nombre a b
puts "resultado=[$nombre $a $b]"
```

### R

```r
estrategias <- list(suma = `+`, resta = `-`, producto = `*`)

campos <- strsplit(readLines("stdin", n = 1), " ")[[1]]
f <- estrategias[[campos[1]]]
cat(sprintf("resultado=%d\n", f(as.integer(campos[2]), as.integer(campos[3]))))
```

**Qué reconocer:** los cinco escriben el patrón Estrategia en tres líneas y **ninguno declara una
interfaz**. Ruby usa lambdas (`->`), Perl referencias a subrutina (`sub { }`), Lua funciones anónimas
en una tabla: es el mismo gesto con distinta ortografía. Tcl no necesita ni tabla, porque el nombre
de la estrategia **es** el nombre del comando y `[$nombre $a $b]` lo invoca directamente —el despacho
dinámico está en la gramática del lenguaje—. R llega al extremo contrario y a la vez al mismo sitio:
`+`, `-` y `*` son funciones ordinarias que se pueden guardar en una lista, así que la "estrategia
concreta" ya venía escrita en la biblioteca estándar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

typedef Estrategia = int Function(int, int);

final Map<String, Estrategia> estrategias = {
  'suma': (a, b) => a + b,
  'resta': (a, b) => a - b,
  'producto': (a, b) => a * b,
};

void main() {
  final campos = stdin.readLineSync()!.split(' ');
  final f = estrategias[campos[0]]!;
  print('resultado=${f(int.parse(campos[1]), int.parse(campos[2]))}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: la línea llega ya partida.
package {
    public class Estrategias {
        public static const TABLA:Object = {
            suma:     function(a:int, b:int):int { return a + b; },
            resta:    function(a:int, b:int):int { return a - b; },
            producto: function(a:int, b:int):int { return a * b; }
        };

        public static function aplicar(nombre:String, a:int, b:int):String {
            var f:Function = TABLA[nombre];
            return "resultado=" + f(a, b);
        }
    }
}
```

**Qué reconocer:** Dart introduce `typedef Estrategia` — que es exactamente lo que en Java sería una
interfaz con un solo método, pero reducida a **un nombre para una firma de función**. Ese `typedef`
es la interfaz del patrón GoF sin clase, sin `implements` y sin fichero aparte. ActionScript 3, que
es ECMAScript de la misma raíz que JavaScript, guarda las funciones en un objeto literal y las busca
con `TABLA[nombre]`: la tabla de despacho de toda la familia web.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Es la máquina donde nació la costumbre de
escribir patrones como clases, y donde mejor se ve cómo los lenguajes posteriores la abandonan sin
salir de la misma JVM.

### Kotlin

```kotlin
val estrategias = mapOf<String, (Int, Int) -> Int>(
    "suma" to { a, b -> a + b },
    "resta" to { a, b -> a - b },
    "producto" to { a, b -> a * b }
)

fun main() {
    val (nombre, a, b) = readLine()!!.split(" ")
    println("resultado=${estrategias.getValue(nombre)(a.toInt(), b.toInt())}")
}
```

### Scala

```scala
object Estrategias {
  val tabla: Map[String, (Int, Int) => Int] = Map(
    "suma"     -> ((a: Int, b: Int) => a + b),
    "resta"    -> ((a: Int, b: Int) => a - b),
    "producto" -> ((a: Int, b: Int) => a * b)
  )

  def main(args: Array[String]): Unit = {
    val Array(nombre, a, b) = scala.io.StdIn.readLine().split(" ")
    println(s"resultado=${tabla(nombre)(a.toInt, b.toInt)}")
  }
}
```

### Groovy

```groovy
def estrategias = [
    suma    : { a, b -> a + b },
    resta   : { a, b -> a - b },
    producto: { a, b -> a * b }
]

def (nombre, a, b) = System.in.newReader().readLine().split(' ')
println "resultado=${estrategias[nombre](a as int, b as int)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(def estrategias {"suma" + "resta" - "producto" *})

(let [[nombre a b] (str/split (read-line) #" ")]
  (println (str "resultado=" ((estrategias nombre) (parse-long a) (parse-long b)))))
```

**Qué reconocer:** cuatro lenguajes, la misma JVM, el mismo `Map` de `java.util` por debajo, y ni uno
solo escribe una clase `EstrategiaSuma`. Kotlin y Scala escriben el tipo de la estrategia como
`(Int, Int) -> Int`: la función **tiene tipo**, así que la interfaz sobra. Clojure es el argumento
final de la página entera —la tabla de estrategias es `{"suma" + "resta" - "producto" *}`, los
operadores del lenguaje metidos tal cual en un mapa—: el patrón se ha evaporado hasta quedar en una
estructura de datos de tres pares. Y donde el patrón sí sobrevive en la JVM es en Visitor, que
Scala liquida con `match` sobre `case class` y que en Java sigue exigiendo el doble despacho.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR trae `Func<...>` desde .NET 2.0, así que
la conversación sobre estrategias en esta plataforma lleva veinte años resuelta.

### F\#

```fsharp
let estrategias = dict [ "suma", (+); "resta", (-); "producto", ( * ) ]

[<EntryPoint>]
let main _ =
    match stdin.ReadLine().Split(' ') with
    | [| nombre; a; b |] ->
        printfn "resultado=%d" (estrategias.[nombre] (int a) (int b))
        0
    | _ -> 1
```

### VB.NET

```vbnet
Module Estrategias
    Private ReadOnly Tabla As New Dictionary(Of String, Func(Of Integer, Integer, Integer)) From {
        {"suma", Function(a, b) a + b},
        {"resta", Function(a, b) a - b},
        {"producto", Function(a, b) a * b}
    }

    Sub Main()
        Dim campos = Console.ReadLine().Split(" "c)
        Dim f = Tabla(campos(0))
        Console.WriteLine("resultado=" & f(Integer.Parse(campos(1)), Integer.Parse(campos(2))))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `Dictionary` y `Func<int, int, int>` del CLR, y esa firma
genérica **es** la interfaz `IEstrategia` que el libro pedía escribir a mano. F# va un paso más allá:
`(+)`, `(-)` y `( * )` son los operadores del lenguaje usados como valores —los espacios alrededor
del asterisco son obligatorios para que no se lea como el inicio de un comentario `(*`—. VB.NET,
que arrastra la sintaxis más ceremoniosa de la familia, sigue necesitando `Function(a, b)` y
`Integer.Parse`, pero por debajo construye exactamente el mismo delegado que F#.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el patrón sí deja marca, porque la unidad de
despacho es el **puntero a función** y hay que decir su tipo entero.

### C++

```cpp
#include <functional>
#include <iostream>
#include <map>
#include <string>

int main() {
    const std::map<std::string, std::function<int(int, int)>> estrategias = {
        {"suma", [](int a, int b) { return a + b; }},
        {"resta", [](int a, int b) { return a - b; }},
        {"producto", [](int a, int b) { return a * b; }},
    };

    std::string nombre;
    int a = 0, b = 0;
    std::cin >> nombre >> a >> b;
    std::cout << "resultado=" << estrategias.at(nombre)(a, b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

typedef int (^Estrategia)(int, int);

int main(void) {
    @autoreleasepool {
        NSDictionary<NSString *, Estrategia> *estrategias = @{
            @"suma": ^int(int a, int b) { return a + b; },
            @"resta": ^int(int a, int b) { return a - b; },
            @"producto": ^int(int a, int b) { return a * b; }
        };

        char nombre[32];
        int a = 0, b = 0;
        if (scanf("%31s %d %d", nombre, &a, &b) != 3) { return 1; }
        Estrategia f = estrategias[[NSString stringWithUTF8String:nombre]];
        printf("resultado=%d\n", f(a, b));
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C, así que el `int (*)(int, int)` de la clase sigue
siendo válido; lo que añaden es una forma de escribir la función **en el sitio donde se usa**. C++ lo
hace con lambdas y `std::function`, que borra la diferencia entre puntero a función, functor y
lambda —a costa de una asignación en memoria dinámica que un puntero desnudo no paga—. Objective-C lo
hace con *blocks*, esa sintaxis con `^` que es su marca registrada, y que además captura variables
del entorno, algo que el puntero a función de C no puede hacer. Fíjate también en `%31s`: en esta
familia el ancho del `scanf` es lo único que separa el programa de un desbordamiento de búfer.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, y con una preferencia clara por resolver el despacho **en tiempo de compilación** cuando se
puede.

### Zig

```zig
const std = @import("std");

fn suma(a: i64, b: i64) i64 {
    return a + b;
}
fn resta(a: i64, b: i64) i64 {
    return a - b;
}
fn producto(a: i64, b: i64) i64 {
    return a * b;
}

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r");
    const nombre = it.next().?;
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);

    const f: *const fn (i64, i64) i64 =
        if (std.mem.eql(u8, nombre, "suma")) suma
        else if (std.mem.eql(u8, nombre, "resta")) resta
        else producto;

    try std.io.getStdOut().writer().print("resultado={d}\n", .{f(a, b)});
}
```

### Nim

```nim
import std/[strutils, tables]

let estrategias = {
  "suma": proc (a, b: int): int = a + b,
  "resta": proc (a, b: int): int = a - b,
  "producto": proc (a, b: int): int = a * b
}.toTable

let campos = stdin.readLine().splitWhitespace()
echo "resultado=", estrategias[campos[0]](campos[1].parseInt, campos[2].parseInt)
```

### D

```d
import std.stdio, std.array, std.conv, std.string;

void main() {
    int function(int, int)[string] estrategias = [
        "suma":     (int a, int b) => a + b,
        "resta":    (int a, int b) => a - b,
        "producto": (int a, int b) => a * b
    ];

    auto campos = readln().strip().split();
    writefln("resultado=%d", estrategias[campos[0]](campos[1].to!int, campos[2].to!int));
}
```

**Qué reconocer:** Zig no tiene funciones anónimas con captura ni tablas hash en el lenguaje base, así
que escribe las tres estrategias como funciones nombradas y elige el **puntero a función** con un
`if` — es la versión más honesta y también la más cercana a C. Nim y D sí traen tabla asociativa y
literales de función, y por eso su código se parece a Ruby aunque compile a binario nativo. Fíjate en
`int function(int, int)[string]` de D: el tipo dice a la vez "puntero a función" y "diccionario
indexado por cadena", y esa distinción entre `function` (sin contexto) y `delegate` (con contexto
capturado) es justo la que C++ esconde detrás de `std::function`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo, y el despacho por nombre se convierte en algo muy distinto.

### Prolog

```prolog
:- initialization(main, main).

aplicar(suma, A, B, R)     :- R is A + B.
aplicar(resta, A, B, R)    :- R is A - B.
aplicar(producto, A, B, R) :- R is A * B.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [E, SA, SB]),
    atom_string(Estrategia, E),
    number_string(A, SA),
    number_string(B, SB),
    aplicar(Estrategia, A, B, R),
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni funciones de primera clase: la entrada se declara como hecho
% y cada estrategia es una regla distinta con el mismo predicado en la cabeza.
entrada(suma, 3, 4).

resultado(R) :- entrada(suma, A, B), R = A + B.
resultado(R) :- entrada(resta, A, B), R = A - B.
resultado(R) :- entrada(producto, A, B), R = A * B.
```

**Qué reconocer:** aquí el patrón Estrategia no se implementa: **se disuelve en el mecanismo de
resolución del lenguaje**. Las tres cláusulas `aplicar/4` de Prolog tienen el mismo nombre y difieren
solo en el primer argumento, y es el motor de unificación quien elige la correcta —eso es despacho
múltiple gratis, sin tabla y sin `if`—. Datalog hace lo mismo con tres reglas que comparten cabeza,
pero renuncia a leer de stdin, así que la entrada se escribe como un hecho: la misma renuncia que
hace SQL cuando no te deja decirle cómo recorrer las filas. Compara con el `CASE` de la
implementación SQL de la clase: también ahí la estrategia es un dato de la consulta, no un objeto.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una conclusión incómoda para el catálogo GoF: **el patrón
Estrategia solo es un patrón en los lenguajes que no tienen funciones de primera clase**. En los
demás es un diccionario. Lo mismo pasa con Singleton, que en Ruby o Perl es un módulo; con Iterator,
que ya viene en el `for` de todos ellos; y con Visitor, que la coincidencia de patrones de Scala y F#
deja sin trabajo. Cuando leas un patrón, pregúntate siempre qué carencia del lenguaje está tapando:
esa pregunta es lo transferible.

⏮️ [Volver a la clase 151](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
