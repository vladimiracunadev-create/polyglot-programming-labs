# 🧬 El mismo programa en las familias de lenguajes — Clase 053

> [⬅️ Volver a la clase 053](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —distinguir un valor presente de uno ausente—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, donde `0` significa *ausente*
- **Salida** (stdout): `valor=<n>` si hay valor, o `valor=ausente` si `n` es 0
- **Regla:** si `n == 0` → `ausente`; si no → `n`

| stdin | esperado |
|---|---|
| `5` | `valor=5` |
| `0` | `valor=ausente` |
| `42` | `valor=42` |

El `if` es el mismo en todos. Lo que cambia —y mucho— es **cómo se representa el hueco** entre leer
el 0 y decidir qué imprimir: un `null`, un `nil`, un `Option`, una variable sin fijar, o nada en
absoluto.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia del valor centinela: existe un objeto especial que significa "aquí no hay nada", y
cualquier variable puede contenerlo.

### Ruby

```ruby
n = STDIN.gets.to_i
valor = n.zero? ? nil : n
# En Ruby `nil` es un objeto de pleno derecho (instancia de NilClass) y
# responde a mensajes: nil.to_s da "", nil.inspect da "nil".
puts "valor=#{valor.nil? ? 'ausente' : valor}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my $valor = $n == 0 ? undef : $n;
# `undef` no es lo mismo que 0 ni que "": `defined` es la única forma fiable
# de distinguirlos, porque en contexto numérico `undef` vale 0.
printf "valor=%s\n", defined($valor) ? $valor : "ausente";
```

### Lua

```lua
local n = io.read("n")
local valor = n ~= 0 and n or nil
-- En Lua `nil` no es solo un valor: asignar nil a una clave la BORRA de la tabla.
-- Ausencia y no-existencia son literalmente lo mismo.
print("valor=" .. (valor or "ausente"))
```

### Tcl

```tcl
gets stdin n
# Tcl no tiene null. La ausencia se modela con una variable que NO se fija,
# y se pregunta por su existencia, no por su contenido.
if {$n != 0} {
    set valor $n
}
if {[info exists valor]} {
    puts "valor=$valor"
} else {
    puts "valor=ausente"
}
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
# R distingue DOS ausencias: NA es "dato desconocido" dentro de un vector
# y NULL es "el objeto no existe". Aquí el caso es un dato que falta: NA.
valor <- if (n == 0) NA_integer_ else n
cat(sprintf("valor=%s\n", if (is.na(valor)) "ausente" else valor))
```

**Qué reconocer:** los cinco son dinámicos, pero cada uno inventó una ausencia distinta. Ruby y Lua
tienen `nil`; Perl tiene `undef` y una función `defined` porque su `nil` se confunde con 0 y con la
cadena vacía; Tcl directamente no tiene el concepto y pregunta si la variable existe; y R tiene
**dos**, `NA` y `NULL`, con significados que no se solapan. Esa proliferación es la mejor prueba de
que "ausente" no es un concepto único.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia que tiene el problema por partida doble: `null` y `undefined` conviven.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  // `int?` y `int` son tipos DISTINTOS: sin el `?` el compilador rechaza null.
  final int? valor = n == 0 ? null : n;
  print('valor=${valor ?? 'ausente'}');
}
```

### ActionScript 3

```actionscript
package {
    // ActionScript corre en el reproductor Flash, sin stdin: se ilustra el cálculo.
    // AS3 no puede expresar "int ausente": los tipos primitivos int/uint/Number
    // NO admiten null (asignarles null los convierte en 0 o NaN). Lo más cercano
    // es subirlo a un tipo por referencia, que sí acepta null.
    public class Valor {
        public static function texto(n:int):String {
            var valor:Object = (n == 0) ? null : n;
            return "valor=" + (valor == null ? "ausente" : valor);
        }
    }
}
```

**Qué reconocer:** Dart adoptó *null safety sano* en 2021 y con ello el `?` en el tipo y el operador
`??`, la misma pareja que verás en C#, Kotlin y Swift. ActionScript 3 muestra el estado anterior del
arte: `null` solo cabe en tipos por referencia, así que un entero **no puede** estar ausente y hay
que envolverlo. Ese envoltorio es el antepasado directo del `Integer` de Java y del `Option` de Rust.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La plataforma donde nació el
`NullPointerException`, y donde se ensayaron casi todas las curas.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    // `Int?` es un tipo distinto de `Int`. Sin el `?`, `null` no compila:
    // Kotlin nació explícitamente para matar el NullPointerException de Java.
    val valor: Int? = if (n == 0) null else n
    println("valor=${valor ?: "ausente"}")
}
```

### Scala

```scala
object Valor extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  // Scala tiene `null` por compatibilidad con Java, pero el idioma es Option:
  // Some(x) o None, y el compilador te obliga a tratar las dos ramas.
  val valor: Option[Int] = if (n == 0) None else Some(n)
  println(s"valor=${valor.fold("ausente")(_.toString)}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
def valor = n == 0 ? null : n
// El operador Elvis `?:` de Groovy es el mismo que adoptó Kotlin,
// y su navegación segura `?.` es el `?.` que hoy tiene JavaScript.
println "valor=${valor ?: 'ausente'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Long/parseLong (str/trim (read-line)))
      ;; `nil` en Clojure es "nada" y además es falso, así que `or` y `when`
      ;; lo tratan sin ceremonia. Es el enfoque relajado dentro de la JVM.
      valor (when-not (zero? n) n)]
  (println (str "valor=" (or valor "ausente"))))
```

**Qué reconocer:** las cuatro respuestas al mismo error histórico. Kotlin lo resuelve en el **sistema
de tipos** (`Int?`), Scala en la **biblioteca** (`Option[Int]`), Groovy con **azúcar sintáctico**
(`?:`, `?.`) que no impide el fallo pero lo hace cómodo de evitar, y Clojure lo asume como parte del
lenguaje. Java, el representante, llegó tarde con `Optional<Integer>`, que solo funciona si nadie te
pasa un `null` por debajo.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR separa tipos por valor de tipos por
referencia, y esa división marca toda la familia.

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
// En F# los tipos NO admiten null: `option` es la única forma de expresar
// la ausencia, y el `match` obliga a cubrir las dos ramas o el compilador avisa.
let valor = if n = 0 then None else Some n
let texto =
    match valor with
    | Some v -> string v
    | None -> "ausente"
printfn "valor=%s" texto
```

### VB.NET

```vbnet
Module Valor
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.ReadLine().Trim())
        ' `Integer?` es Nullable(Of Integer): un Integer normal no puede ser Nothing.
        ' Ojo con la trampa clásica: `If(cond, Nothing, n)` colapsa Nothing a 0
        ' porque el ternario deduce Integer, no Integer?. Por eso se asigna aparte.
        Dim valor As Integer? = Nothing
        If n <> 0 Then valor = n
        Console.WriteLine("valor=" & If(valor.HasValue, valor.Value.ToString(), "ausente"))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `Nullable<T>`, la solución que .NET dio en 2005 al mismo
problema que ActionScript no podía resolver: dejar que un tipo por valor esté ausente. F# se sale de
la familia y usa `option`, más seguro porque no hay un `.Value` que puedas leer sin comprobar. Y el
comentario de VB no es anecdótico: `Nothing` significa a la vez "null" y "valor por defecto del
tipo", y esa doble vida es una fuente real de errores.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C la ausencia es un puntero nulo o un valor
centinela acordado, sin ninguna ayuda del compilador.

### C++

```cpp
#include <iostream>
#include <optional>

int main() {
    int n;
    std::cin >> n;
    // std::optional (C++17) trae a la familia de las llaves lo que Rust
    // y Scala ya tenían: la ausencia como parte del tipo, sin punteros.
    const std::optional<int> valor = (n == 0) ? std::nullopt : std::optional<int>{n};
    if (valor) {
        std::cout << "valor=" << *valor << '\n';
    } else {
        std::cout << "valor=ausente\n";
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
        // `nil` solo existe para tipos objeto: un `int` no puede ser nil, hay que
        // encajarlo en un NSNumber. A cambio, enviar un mensaje a nil NO revienta:
        // devuelve 0/nil en silencio, que es la decisión opuesta a la de Java.
        NSNumber *valor = (n == 0) ? nil : @(n);
        if (valor != nil) {
            printf("valor=%s\n", [[valor stringValue] UTF8String]);
        } else {
            printf("valor=ausente\n");
        }
    }
    return 0;
}
```

**Qué reconocer:** C++ ofrece el contraste más limpio de toda esta página: `std::optional<int>` es
exactamente el `Option<i32>` de Rust y el `Option[Int]` de Scala, llegado a la familia de las llaves
cuarenta años después de C. Objective-C toma el camino contrario y hace que `nil` sea **inofensivo**:
un mensaje a `nil` no falla, simplemente no hace nada. Evita el crash, pero también esconde el error.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Dos filosofías opuestas:
Go conserva `nil` y el valor cero; Rust eliminó el null del lenguaje.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    // `?i64` es un tipo opcional integrado en el lenguaje, no una biblioteca.
    // El `if` con captura `|v|` es la única forma de sacar el valor de dentro.
    const valor: ?i64 = if (n == 0) null else n;
    const out = std.io.getStdOut().writer();
    if (valor) |v| {
        try out.print("valor={d}\n", .{v});
    } else {
        try out.print("valor=ausente\n", .{});
    }
}
```

### Nim

```nim
import std/[strutils, options]

let n = stdin.readLine().strip().parseInt()
# Nim tiene `nil` para referencias, pero para un valor ausente el idioma
# es Option del módulo std/options, igual que Rust.
let valor = if n == 0: none(int) else: some(n)
if valor.isSome:
  echo "valor=", valor.get
else:
  echo "valor=ausente"
```

### D

```d
import std.stdio, std.conv, std.string, std.typecons;

void main() {
    int n = readln().strip().to!int;
    // Nullable!int de std.typecons: un int que además sabe si está vacío.
    Nullable!int valor;
    if (n != 0) valor = n;
    if (valor.isNull) {
        writeln("valor=ausente");
    } else {
        writefln("valor=%d", valor.get);
    }
}
```

**Qué reconocer:** los tres eligen el bando de Rust y no el de Go: la ausencia forma parte del tipo y
hay que abrirla explícitamente. Zig es el que más lejos llega, con `?T` **en la sintaxis del
lenguaje** y una captura obligatoria `|v|` que hace imposible leer el valor sin comprobar antes. Nim
y D lo consiguen desde la biblioteca estándar, que es exactamente lo que hizo C++ con
`std::optional`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El `NULL` de SQL es un caso aparte: no es un
valor, es un **desconocido** que envenena toda comparación (`NULL = NULL` no es cierto).

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    % Prolog no tiene null. La ausencia se expresa de dos formas: una variable
    % que queda SIN LIGAR, o un objetivo que simplemente falla y no deriva nada.
    (   N =:= 0
    ->  format("valor=ausente~n")
    ;   format("valor=~w~n", [N])
    ).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni null: la ausencia es la NO derivación de un hecho.
% Si `valor/1` no deriva nada para la entrada, eso ES el valor ausente.
entrada(0).

valor(N) :- entrada(N), N != 0.
```

**Qué reconocer:** aquí la ausencia deja de ser un valor guardado en memoria y pasa a ser una
propiedad de la base de conocimiento: **algo está ausente porque no se puede demostrar**. Es la
hipótesis del mundo cerrado, y es la misma intuición que hay detrás del `LEFT JOIN` de SQL que
produce `NULL` cuando no encuentra pareja. Prolog y Datalog llegan a ella sin necesitar un `null`, lo
que sugiere que buena parte de nuestros `NullPointerException` son un problema de representación, no
del concepto.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres respuestas posibles a "¿y si no hay valor?": un **valor
centinela** que cualquier variable puede tener (`nil`, `undef`, `null`), un **tipo aparte** que
obliga a comprobar (`Int?`, `Option`, `?i64`, `optional`), o **no representarlo** y dejar que la
ausencia sea la falta de un hecho. Saber en cuál de los tres mundos estás antes de escribir la
primera línea es lo transferible.

⏮️ [Volver a la clase 053](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
