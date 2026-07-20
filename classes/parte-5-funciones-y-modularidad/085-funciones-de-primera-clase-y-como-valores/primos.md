# 🧬 El mismo programa en las familias de lenguajes — Clase 085

> [⬅️ Volver a la clase 085](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —pasar dos operaciones como argumento a la función
que las ejecuta— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b> producto=<a*b>`
- **Regla:** `aplicar(f, a, b) = f(a, b)`, con `f = suma` y luego `f = producto`

| stdin | esperado |
|---|---|
| `3 4` | `suma=7 producto=12` |
| `5 5` | `suma=10 producto=25` |
| `0 9` | `suma=9 producto=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En los dinámicos una función suele ser un valor más, que se guarda en una variable y se pasa como
cualquier número. Pero no todos llegaron ahí por el mismo camino.

### Ruby

```ruby
def suma(a, b)
  a + b
end

def producto(a, b)
  a * b
end

def aplicar(f, a, b)
  f.call(a, b)
end

a, b = STDIN.gets.split.map(&:to_i)
# Un método no es un objeto función: method(:nombre) lo envuelve en un Method.
puts "suma=#{aplicar(method(:suma), a, b)} producto=#{aplicar(method(:producto), a, b)}"
```

### Perl

```perl
use strict;
use warnings;

sub suma     { return $_[0] + $_[1]; }
sub producto { return $_[0] * $_[1]; }

# \&nombre crea una *referencia a código*; se invoca con la flecha.
sub aplicar {
    my ($f, $a, $b) = @_;
    return $f->($a, $b);
}

my ($a, $b) = split ' ', <STDIN>;
printf "suma=%d producto=%d\n", aplicar(\&suma, $a, $b), aplicar(\&producto, $a, $b);
```

### Lua

```lua
local function suma(a, b) return a + b end
local function producto(a, b) return a * b end

local function aplicar(f, a, b) return f(a, b) end

local a, b = io.read("n", "n")
print(string.format("suma=%d producto=%d", aplicar(suma, a, b), aplicar(producto, a, b)))
```

### Tcl

```tcl
proc suma {a b}     { expr {$a + $b} }
proc producto {a b} { expr {$a * $b} }

# En Tcl un procedimiento NO es un valor: se pasa su nombre y se invoca
# expandiéndolo con {*} en la posición de comando.
proc aplicar {f a b} { {*}$f $a $b }

lassign [split [string trim [gets stdin]]] a b
puts "suma=[aplicar suma $a $b] producto=[aplicar producto $a $b]"
```

### R

```r
suma <- function(a, b) a + b
producto <- function(a, b) a * b

aplicar <- function(f, a, b) f(a, b)

v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
cat(sprintf("suma=%d producto=%d\n",
            aplicar(suma, v[1], v[2]), aplicar(producto, v[1], v[2])))
```

**Qué reconocer:** R y Lua son los más limpios de los cinco porque la función **es** el valor:
`suma` sin paréntesis ya se puede pasar, igual que en Python. Ruby y Perl delatan que sus rutinas no
nacieron como objetos: Ruby necesita `method(:suma)` para envolver el método en un `Method`, y el
`&:to_i` de la lectura es el mismo truco al revés —convertir un símbolo en bloque—; Perl exige la
referencia explícita `\&suma` y la desreferencia `$f->(...)`. Tcl es el extremo opuesto: allí las
funciones no son valores en absoluto, solo hay **nombres de comando**, y `{*}$f` sirve para colocar
ese nombre en la única posición donde Tcl acepta invocar algo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Toda la familia hereda de JS la idea de que la función es un objeto de primera clase.

### Dart

```dart
import 'dart:io';

int suma(int a, int b) => a + b;
int producto(int a, int b) => a * b;

int aplicar(int Function(int, int) f, int a, int b) => f(a, b);

void main() {
  final v = stdin.readLineSync()!.trim().split(' ').map(int.parse).toList();
  print('suma=${aplicar(suma, v[0], v[1])} producto=${aplicar(producto, v[0], v[1])}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el paso de funciones.
package {
    public class Aplicador {
        public static function suma(a:int, b:int):int { return a + b; }
        public static function producto(a:int, b:int):int { return a * b; }

        // 'Function' es un tipo real, pero sin firma: no dice cuántos argumentos toma.
        public static function aplicar(f:Function, a:int, b:int):int {
            return f(a, b);
        }

        public static function describir(a:int, b:int):String {
            return "suma=" + aplicar(suma, a, b) + " producto=" + aplicar(producto, a, b);
        }
    }
}
```

**Qué reconocer:** los dos pasan el nombre de la función pelado, sin ceremonia, igual que JavaScript.
La diferencia está en **cuánto sabe el tipo**: Dart escribe la firma completa
`int Function(int, int)`, así que el compilador rechaza pasar una función de aridad equivocada;
ActionScript solo tiene `Function`, un tipo opaco que acepta cualquier cosa invocable y falla en
tiempo de ejecución. Es exactamente el salto que TypeScript hizo sobre JavaScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó hasta la versión 8 en tener
funciones como valores, y aun así las envuelve en interfaces. Sus primos no esperaron.

### Kotlin

```kotlin
fun suma(a: Int, b: Int) = a + b
fun producto(a: Int, b: Int) = a * b

fun aplicar(f: (Int, Int) -> Int, a: Int, b: Int) = f(a, b)

fun main() {
    val (a, b) = readLine()!!.trim().split(" ").map { it.toInt() }
    // ::nombre es la referencia a función; sin ella, 'suma' sería una llamada.
    println("suma=${aplicar(::suma, a, b)} producto=${aplicar(::producto, a, b)}")
}
```

### Scala

```scala
object Aplicador {
  def suma(a: Int, b: Int): Int = a + b
  def producto(a: Int, b: Int): Int = a * b

  def aplicar(f: (Int, Int) => Int, a: Int, b: Int): Int = f(a, b)

  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split(" ").map(_.toInt)
    println(s"suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}")
  }
}
```

### Groovy

```groovy
def suma = { a, b -> a + b }
def producto = { a, b -> a * b }

def aplicar = { f, a, b -> f(a, b) }

def (a, b) = System.in.newReader().readLine().trim().split(' ')*.toInteger()
println "suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}"
```

### Clojure

```clojure
(defn suma [a b] (+ a b))
(defn producto [a b] (* a b))

(defn aplicar [f a b] (f a b))

(let [[a b] (map #(Integer/parseInt %) (.split (.trim (read-line)) " "))]
  (println (str "suma=" (aplicar suma a b) " producto=" (aplicar producto a b))))
```

**Qué reconocer:** los cuatro compilan al mismo bytecode, donde no existen las funciones sueltas —
todo acaba siendo un objeto con un método—, y sin embargo cada uno esconde ese hecho de forma
distinta. Kotlin declara el tipo función `(Int, Int) -> Int` y exige `::suma` porque `suma` a secas
ya sería una llamada. Scala convierte el método en función sola con la *expansión eta*, invisible en
el código. Groovy prescinde de los métodos: define **clausuras** desde el principio, que sí son
objetos. Clojure ni siquiera plantea el problema, porque en un Lisp una función es solo un valor
más al que un símbolo apunta; por eso `aplicar` allí es casi una tautología.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR modela las funciones como *delegados*,
un tipo de objeto con firma.

### F\#

```fsharp
let suma a b = a + b
let producto a b = a * b

let aplicar f a b = f a b

[<EntryPoint>]
let main _ =
    let v = stdin.ReadLine().Trim().Split(' ') |> Array.map int
    printfn "suma=%d producto=%d" (aplicar suma v.[0] v.[1]) (aplicar producto v.[0] v.[1])
    0
```

### VB.NET

```vbnet
Module Aplicador
    Function Suma(a As Integer, b As Integer) As Integer
        Return a + b
    End Function

    Function Producto(a As Integer, b As Integer) As Integer
        Return a * b
    End Function

    ' Func(Of ...) es el delegado genérico; AddressOf convierte el método en delegado.
    Function Aplicar(f As Func(Of Integer, Integer, Integer), a As Integer, b As Integer) As Integer
        Return f(a, b)
    End Function

    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Console.WriteLine("suma={0} producto={1}",
                          Aplicar(AddressOf Suma, a, b), Aplicar(AddressOf Producto, a, b))
    End Sub
End Module
```

**Qué reconocer:** VB.NET enseña la maquinaria en crudo: `Func(Of Integer, Integer, Integer)` es el
delegado y `AddressOf` es el verbo explícito que convierte un método en valor —el equivalente exacto
de `method(:f)` en Ruby o `\&f` en Perl—. F# corre sobre el mismo CLR y genera los mismos delegados,
pero no los menciona nunca: allí `let suma a b = ...` ya define una función currificada de primera
clase, y `aplicar suma` se escribe sin ningún operador de por medio.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C sí tiene punteros a función desde siempre; sus
primos añaden capas encima.

### C++

```cpp
#include <iostream>
#include <functional>

int suma(int a, int b) { return a + b; }
int producto(int a, int b) { return a * b; }

// std::function acepta funciones libres, lambdas y objetos invocables por igual.
int aplicar(const std::function<int(int, int)>& f, int a, int b) {
    return f(a, b);
}

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << "suma=" << aplicar(suma, a, b)
              << " producto=" << aplicar(producto, a, b) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// Los 'blocks' son la aportación de Objective-C: funciones anónimas con captura.
typedef int (^Operacion)(int, int);

static int aplicar(Operacion f, int a, int b) {
    return f(a, b);
}

int main(void) {
    @autoreleasepool {
        Operacion suma = ^(int a, int b) { return a + b; };
        Operacion producto = ^(int a, int b) { return a * b; };
        int a, b;
        scanf("%d %d", &a, &b);
        printf("suma=%d producto=%d\n", aplicar(suma, a, b), aplicar(producto, a, b));
    }
    return 0;
}
```

**Qué reconocer:** en ambos sigue vivo el puntero a función de C —`int (*f)(int, int)` compila tal
cual en los dos—, pero cada uno añadió su propia abstracción por encima. C++ generaliza con
`std::function`, que borra el tipo concreto y acepta cualquier cosa invocable a costa de una posible
reserva de memoria. Objective-C inventó los *blocks*, marcados con `^`, que son punteros a función
**más** el entorno capturado: por eso son de primera clase de verdad, y no meros punteros a código.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y sin
recolector de basura: pasar una función tiene que costar lo mismo que llamarla.

### Zig

```zig
const std = @import("std");

fn suma(a: i64, b: i64) i64 {
    return a + b;
}

fn producto(a: i64, b: i64) i64 {
    return a * b;
}

// *const fn(...) es un puntero a función: sin entorno capturado, coste cero.
fn aplicar(f: *const fn (i64, i64) i64, a: i64, b: i64) i64 {
    return f(a, b);
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    try std.io.getStdOut().writer().print(
        "suma={d} producto={d}\n",
        .{ aplicar(suma, a, b), aplicar(producto, a, b) },
    );
}
```

### Nim

```nim
import std/strutils

proc suma(a, b: int): int = a + b
proc producto(a, b: int): int = a * b

proc aplicar(f: proc (a, b: int): int {.nimcall.}, a, b: int): int = f(a, b)

let v = stdin.readLine().splitWhitespace()
let a = parseInt(v[0])
let b = parseInt(v[1])
echo "suma=", aplicar(suma, a, b), " producto=", aplicar(producto, a, b)
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

int suma(int a, int b) { return a + b; }
int producto(int a, int b) { return a * b; }

// 'function' = puntero puro; 'delegate' sería puntero + contexto.
int aplicar(int function(int, int) f, int a, int b) {
    return f(a, b);
}

void main() {
    auto v = readln().split().map!(to!int).array;
    writefln("suma=%d producto=%d", aplicar(&suma, v[0], v[1]), aplicar(&producto, v[0], v[1]));
}
```

**Qué reconocer:** los tres distinguen, en el propio tipo, entre **puntero a función** y **función
con entorno**, algo que Python o Ruby ni se plantean. D lo hace con dos palabras clave distintas
(`function` frente a `delegate`) y exige `&suma` para tomar la dirección; Nim marca la convención de
llamada con `{.nimcall.}` frente a `{.closure.}`; Zig escribe `*const fn`, un puntero explícito.
Esa distinción no es purismo: decide si el valor cabe en un registro o necesita memoria.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí no se pasan funciones porque, en rigor, no
hay funciones: hay relaciones.

### Prolog

```prolog
:- initialization(main, main).

suma(A, B, R) :- R is A + B.
producto(A, B, R) :- R is A * B.

% call/N es el mecanismo de orden superior: toma un nombre de predicado
% y le añade los argumentos que faltan.
aplicar(F, A, B, R) :- call(F, A, B, R).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    aplicar(suma, A, B, S),
    aplicar(producto, A, B, P),
    format("suma=~d producto=~d~n", [S, P]).
```

### Datalog

```datalog
% Datalog puro no tiene orden superior ni E/S: un predicado no puede ser argumento
% de otro. Lo más cercano es *nombrar* la operación como un dato y ramificar por él.
par(3, 4).

resultado(suma, R)     :- par(A, B), R = A + B.
resultado(producto, R) :- par(A, B), R = A * B.
```

**Qué reconocer:** Prolog sí tiene orden superior, pero por una vía distinta: `call/N` no recibe un
objeto función, recibe un **término** —el átomo `suma`— y construye la llamada añadiéndole
argumentos. Es la misma idea que el nombre de comando de Tcl, no la del objeto función de Python.
Datalog renuncia incluso a eso: se restringe a propósito para garantizar que toda consulta termina,
y un predicado que pudiera recibir predicados rompería esa garantía. Por eso aquí la "operación" baja
de categoría y se convierte en un dato más, `suma`, sobre el que se ramifica —el mismo gesto que
usarías en SQL con una columna de tipo en vez de con una función pasada por parámetro.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que los separa en tres grupos: los que tratan la
función como un valor cualquiera, los que necesitan un verbo explícito para convertirla en valor
(`method(:f)`, `\&f`, `::f`, `AddressOf`, `&f`) y los que sencillamente no tienen funciones que
pasar, solo nombres. Reconocer a cuál de los tres pertenece un lenguaje nuevo es lo transferible.

⏮️ [Volver a la clase 085](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
