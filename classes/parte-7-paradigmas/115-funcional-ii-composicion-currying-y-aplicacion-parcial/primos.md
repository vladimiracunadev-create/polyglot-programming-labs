# 🧬 El mismo programa en las familias de lenguajes — Clase 115

> [⬅️ Volver a la clase 115](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —doblar un número y luego incrementarlo, pero
**componiendo** las dos funciones en vez de anidarlas— resuelto por los **primos** de cada familia
del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí los primos dejan de ser secundarios. La composición, la currificación y la aplicación parcial
son gestos que varios de ellos traen **en el lenguaje o en la biblioteca estándar** mientras que
buena parte del núcleo obliga a escribirlos a mano: F\# currifica todas sus funciones sin pedir
permiso, Clojure tiene `comp` y `partial`, Scala y Groovy tienen `andThen` y `compose`, y D los trae
en `std.functional`. Ver el mismo problema resuelto con y sin esas herramientas es la mejor forma de
entender qué añaden exactamente.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n+1>`
- **Regla:** `resultado = incrementar(doblar(n))`, con las dos funciones definidas por separado

| stdin | esperado |
|---|---|
| `5` | `resultado=11` |
| `0` | `resultado=1` |
| `3` | `resultado=7` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Las funciones son valores, así que componer no necesita ninguna característica especial del
lenguaje: basta con una función que devuelva otra función.

### Ruby

```ruby
doblar = ->(x) { x * 2 }
incrementar = ->(x) { x + 1 }
compuesta = doblar >> incrementar   # >> compone hacia la derecha; << hacia la izquierda

n = STDIN.gets.to_i
puts "resultado=#{compuesta.call(n)}"
```

### Perl

```perl
my $doblar = sub { $_[0] * 2 };
my $incrementar = sub { $_[0] + 1 };

# Perl no trae un combinador de composición: se escribe como una clausura más.
my $componer = sub { my ($f, $g) = @_; sub { $f->($g->(@_)) } };
my $compuesta = $componer->($incrementar, $doblar);

chomp(my $n = <STDIN>);
printf "resultado=%d\n", $compuesta->($n);
```

### Lua

```lua
local function doblar(x) return x * 2 end
local function incrementar(x) return x + 1 end

-- La composición es solo una clausura que captura f y g.
local function componer(f, g)
  return function(x) return f(g(x)) end
end

local compuesta = componer(incrementar, doblar)
print(string.format("resultado=%d", compuesta(io.read("n"))))
```

### Tcl

```tcl
proc doblar {x} { expr {$x * 2} }
proc incrementar {x} { expr {$x + 1} }

# En Tcl un "prefijo de comando" es una lista: fijar f y g en una lambda
# es literalmente aplicación parcial.
set compuesta [list apply {{f g x} {{*}$f [{*}$g $x]}} incrementar doblar]

gets stdin n
puts "resultado=[{*}$compuesta $n]"
```

### R

```r
doblar <- function(x) x * 2
incrementar <- function(x) x + 1

n <- as.integer(readLines("stdin", n = 1))
# El pipe nativo |> encadena valores, no funciones: compone en el punto de uso.
cat(sprintf("resultado=%d\n", n |> doblar() |> incrementar()))
```

**Qué reconocer:** Ruby es el único de los cinco con un operador de composición **en el propio
objeto función** (`>>` sobre `Proc`, y además `curry`). Perl, Lua y Tcl demuestran lo que eso ahorra:
sin operador, componer sigue siendo posible, pero hay que escribir el combinador —una función que
recibe dos funciones y devuelve una tercera— y ese combinador es exactamente lo que `>>` esconde. Tcl
lo hace del modo más literal de todos: un comando es una lista, y "fijar argumentos" es construir esa
lista con las partes ya puestas. R se sale del grupo: `|>` **no compone funciones**, encadena un
valor por una tubería. La diferencia se nota cuando quieres guardar la composición sin tener todavía
el dato: `doblar >> incrementar` es un valor; `n |> doblar()` ya necesita la `n`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int doblar(int x) => x * 2;
int incrementar(int x) => x + 1;

// El tipo de la función compuesta se escribe entero: int Function(int).
int Function(int) componer(int Function(int) f, int Function(int) g) => (x) => f(g(x));

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final compuesta = componer(incrementar, doblar);
  print('resultado=${compuesta(n)}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la composición.
package {
    public class Composicion {
        public static function doblar(x:int):int { return x * 2; }
        public static function incrementar(x:int):int { return x + 1; }

        // AS3 solo tiene el tipo `Function`, sin firma: la composición no se comprueba.
        public static function componer(f:Function, g:Function):Function {
            return function(x:int):int { return f(g(x)); };
        }

        public static function resultado(n:int):String {
            var compuesta:Function = componer(incrementar, doblar);
            return "resultado=" + compuesta(n);
        }
    }
}
```

**Qué reconocer:** ninguno de los dos trae composición en la biblioteca —igual que JavaScript, donde
`compose` siempre ha sido cosa de Lodash o Ramda— pero los dos tienen clausuras, y con clausuras el
combinador cabe en una línea. Lo que los separa es el **tipo** de esa línea: Dart escribe
`int Function(int)` y el compilador verifica que la salida de `g` encaja con la entrada de `f`; AS3
solo sabe decir `Function`, así que componer dos funciones incompatibles compila igual y falla en
tiempo de ejecución. Componer es fácil; componer **con garantías** es lo que cuesta.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java ya trae `Function.andThen` y
`Function.compose` desde la versión 8; los primos muestran cuánto puede acortarse esa idea.

### Kotlin

```kotlin
val doblar: (Int) -> Int = { x -> x * 2 }
val incrementar: (Int) -> Int = { x -> x + 1 }

// Kotlin no trae composición en la biblioteca estándar: se añade como extensión infija.
infix fun <A, B, C> ((A) -> B).andThen(g: (B) -> C): (A) -> C = { a -> g(this(a)) }

fun main() {
    val n = readLine()!!.trim().toInt()
    val compuesta = doblar andThen incrementar
    println("resultado=${compuesta(n)}")
}
```

### Scala

```scala
object Composicion {
  val doblar: Int => Int = _ * 2
  val incrementar: Int => Int = _ + 1

  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    // andThen aplica de izquierda a derecha; compose, de derecha a izquierda.
    val compuesta = doblar andThen incrementar
    println(s"resultado=${compuesta(n)}")
  }
}
```

### Groovy

```groovy
def doblar = { int x -> x * 2 }
def incrementar = { int x -> x + 1 }
def compuesta = doblar >> incrementar        // >> es andThen; << es compose

// Y las clausuras de Groovy se currifican solas con .curry(...)
def sumar = { int a, int b -> a + b }
assert sumar.curry(1)(10) == 11

def n = System.in.newReader().readLine().trim() as int
println "resultado=${compuesta(n)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(def doblar (partial * 2))                   ; partial fija argumentos por la izquierda
(def incrementar inc)
(def compuesta (comp incrementar doblar))    ; comp aplica de derecha a izquierda

(let [n (Integer/parseInt (str/trim (read-line)))]
  (println (str "resultado=" (compuesta n))))
```

**Qué reconocer:** los cuatro corren sobre la misma máquina virtual y aun así solo tres traen la
composición hecha. Kotlin es la ausencia sorprendente: hay que declararla como función de extensión,
aunque el resultado se lea igual de bien. Y fíjate en el **orden de lectura**, que es la trampa
clásica: `andThen` y `>>` van de izquierda a derecha (primero doblar, luego incrementar), pero el
`comp` de Clojure va de derecha a izquierda porque respeta la notación matemática *f∘g*. Escribir
`(comp doblar incrementar)` da 2(n+1), no 2n+1. Clojure además separa con nitidez las dos ideas que
suelen confundirse: `comp` **compone** funciones, `partial` **aplica parcialmente** argumentos —
`(partial * 2)` no compone nada, deja `*` esperando el resto.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). C# tiene `Func<>` y lambdas, pero no operador de
composición: el núcleo de la clase anida las llamadas a mano.

### F\#

```fsharp
let doblar x = x * 2
// Toda función de F# está currificada: `(+)` con un argumento ya es "incrementar".
let incrementar = (+) 1
let compuesta = doblar >> incrementar   // >> compone; << compone al revés

let n = stdin.ReadLine().Trim() |> int
printfn "resultado=%d" (compuesta n)
```

### VB.NET

```vbnet
Module Composicion
    Function Doblar(x As Integer) As Integer
        Return x * 2
    End Function

    Function Incrementar(x As Integer) As Integer
        Return x + 1
    End Function

    ' VB.NET no tiene operador de composición ni currificación: se construye a mano.
    Function Componer(f As Func(Of Integer, Integer),
                      g As Func(Of Integer, Integer)) As Func(Of Integer, Integer)
        Return Function(x) f(g(x))
    End Function

    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim compuesta = Componer(AddressOf Incrementar, AddressOf Doblar)
        Console.WriteLine("resultado=" & compuesta(n))
    End Sub
End Module
```

**Qué reconocer:** el mismo CLR, los dos extremos del recorrido. En F\# **toda** función toma un solo
argumento y devuelve otra función: `let sumar a b = a + b` es en realidad `a -> (b -> int)`, y por eso
`(+) 1` es un valor perfectamente normal sin necesidad de escribir ningún lambda. Eso es
currificación automática, y la aplicación parcial deja de ser una técnica para ser simplemente
"llamar con menos argumentos". VB.NET necesita `AddressOf` solo para convertir un método en un
delegado, y luego el combinador entero. Nota además que en F\# `>>` es composición mientras que en
Groovy `>>` también lo es y en C# `>>` sigue siendo desplazamiento de bits: el mismo símbolo, tres
significados en tres lenguajes vecinos.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C una función no es un valor con estado: es un
puntero, y un puntero no puede capturar `f` y `g`. Componer de verdad exige clausuras.

### C++

```cpp
#include <iostream>

int main() {
    auto doblar = [](int x) { return x * 2; };
    auto incrementar = [](int x) { return x + 1; };

    // El lambda captura f y g por valor: eso es la clausura que C no tiene.
    // Para aplicación parcial, C++20 añade std::bind_front en <functional>.
    auto componer = [](auto f, auto g) { return [f, g](int x) { return f(g(x)); }; };

    int n;
    std::cin >> n;
    auto compuesta = componer(incrementar, doblar);
    std::cout << "resultado=" << compuesta(n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

typedef int (^IntFn)(int);

// Los bloques sí capturan el entorno; ARC los copia al montón al devolverlos.
static IntFn componer(IntFn f, IntFn g) {
    return ^(int x) { return f(g(x)); };
}

int main(void) {
    @autoreleasepool {
        IntFn doblar = ^(int x) { return x * 2; };
        IntFn incrementar = ^(int x) { return x + 1; };
        int n;
        scanf("%d", &n);
        printf("resultado=%d\n", componer(incrementar, doblar)(n));
    }
    return 0;
}
```

**Qué reconocer:** los dos son superconjuntos de C y los dos tuvieron que **añadir** algo al lenguaje
para poder componer: C++ los lambdas (C++11), Objective-C los bloques (`^`, 2009). El detalle que
delata el coste está en Objective-C: un bloque nace en la pila, y devolverlo desde una función exige
copiarlo al montón —ARC lo hace por ti, pero la copia existe—. En C++ el lambda compuesto es un
objeto anónimo con `f` y `g` dentro, y el compilador suele integrarlo por completo, así que la
composición acaba costando cero. Esa es la diferencia real entre las dos ramas: la misma abstracción,
una con reserva de memoria y otra sin ella.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí la pregunta no es si
se puede componer, sino cuánto cuesta y quién paga.

### Zig

```zig
const std = @import("std");

fn doblar(x: i64) i64 {
    return x * 2;
}

fn incrementar(x: i64) i64 {
    return x + 1;
}

// Zig no tiene clausuras: componer en tiempo de ejecución es imposible.
// Se hace en tiempo de compilación, generando un tipo con f y g ya fijadas.
fn Componer(comptime f: fn (i64) i64, comptime g: fn (i64) i64) type {
    return struct {
        fn llamar(x: i64) i64 {
            return f(g(x));
        }
    };
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    const compuesta = Componer(incrementar, doblar);
    try std.io.getStdOut().writer().print("resultado={d}\n", .{compuesta.llamar(n)});
}
```

### Nim

```nim
import std/[strutils, sugar]

proc doblar(x: int): int = x * 2
proc incrementar(x: int): int = x + 1

# `=>` viene de std/sugar; la composición se escribe a mano...
let compuesta = (x: int) => incrementar(doblar(x))

let n = stdin.readLine().strip().parseInt()
# ...aunque el idioma de Nim es la UFCS: `n.doblar.incrementar` encadena sin operador.
echo "resultado=", n.doblar.incrementar
```

### D

```d
import std.stdio, std.string, std.conv, std.functional;

int doblar(int x) { return x * 2; }
int incrementar(int x) { return x + 1; }

void main() {
    // std.functional: compose aplica de derecha a izquierda, pipe de izquierda a derecha.
    // Y partial!(sumar, 1) es aplicación parcial en tiempo de compilación.
    alias compuesta = pipe!(doblar, incrementar);
    const n = readln().strip().to!int;
    writefln("resultado=%d", compuesta(n));
}
```

**Qué reconocer:** D es el único de los tres con la composición **en la biblioteca estándar**
(`compose`, `pipe`, `partial` en `std.functional`), y además resuelta con plantillas, así que no
cuesta nada en tiempo de ejecución. Nim la sustituye por la **llamada uniforme**: `n.doblar` y
`doblar(n)` son lo mismo, de modo que encadenar sale gratis sintácticamente aunque nunca llegues a
tener un valor "función compuesta". Zig es la respuesta más honesta y la más incómoda: **no tiene
clausuras en absoluto**, porque una clausura implica capturar entorno y eso implica decidir dónde
vive esa memoria, decisión que Zig se niega a tomar por ti. Su composición existe, pero ocurre en
`comptime` y produce un tipo nuevo. Compara eso con Rust, que sí tiene clausuras pero te obliga a
elegir entre `Fn`, `FnMut` y `FnOnce` — es la misma pregunta, respondida de otra manera.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** relación hay entre la entrada
y la salida, no en qué orden calcularla.

### Prolog

```prolog
:- initialization(main, main).

doblar(X, Y) :- Y is X * 2.
incrementar(X, Y) :- Y is X + 1.

% No hay valores "función": componer es encadenar por la variable intermedia Y.
compuesta(X, Z) :- doblar(X, Y), incrementar(Y, Z).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    compuesta(N, R),
    % call/N sí es aplicación parcial de verdad: call(doblar, 5, R) fija el primer
    % argumento de un objetivo y deja el resto pendiente.
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni funciones de primer orden: el número entra como hecho.
entrada(5).

% La "composición" es la variable Y compartida entre las dos reglas.
doblado(Y) :- entrada(X), Y = X * 2.
resultado(R) :- doblado(Y), R = Y + 1.
```

**Qué reconocer:** ninguno de los dos tiene funciones como valores, así que la composición **no puede
ser un operador**. Y sin embargo está ahí, más desnuda que en ningún otro lenguaje de la página: es
la variable intermedia `Y` compartida entre dos objetivos. Eso es literalmente lo que significa
`andThen` —la salida de uno es la entrada del siguiente—, solo que aquí se ve el cable. Prolog sí
tiene aplicación parcial genuina en `call/N`: un objetivo con algunos argumentos ya puestos al que se
le añaden los que faltan, que es exactamente `partial` de Clojure. Datalog renuncia incluso a eso:
sin términos compuestos ni orden superior no hay nada que aplicar parcialmente, y a cambio la
evaluación siempre termina. La renuncia es la misma que hace SQL al no dejarte decir cómo recorrer
las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los ordena: ¿es la composición un **valor** de
tu lenguaje o una **forma de escribir**? Cuando lo es (F\#, Clojure, Scala, Groovy, Ruby, D) puedes
guardarla, pasarla y reutilizarla antes de tener el dato. Cuando no lo es (Zig, VB.NET, Prolog) sigue
existiendo, pero solo en el momento de la llamada. Ese es el eje transferible.

⏮️ [Volver a la clase 115](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
