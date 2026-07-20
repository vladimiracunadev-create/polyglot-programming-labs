# 🧬 El mismo programa en las familias de lenguajes — Clase 101

> [⬅️ Volver a la clase 101](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si dos valores son iguales— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

El contrato es deliberadamente pequeño para que se vea lo que de verdad separa a los lenguajes: qué
significa `==`. Detrás de ese operador hay tres preguntas distintas —¿el mismo valor?, ¿el mismo
tipo?, ¿el mismo objeto?— y cada familia las reparte de una manera.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` (dos enteros)
- **Salida** (stdout): `iguales=<true|false>`
- **Regla:** `iguales = (a == b)`

| stdin | esperado |
|---|---|
| `5 5` | `iguales=true` |
| `3 7` | `iguales=false` |
| `0 0` | `iguales=true` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico: el valor lleva el tipo consigo, así que el operador de igualdad tiene que decidir en
tiempo de ejecución qué está comparando.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
# Ruby separa tres preguntas: == (valor), eql? (valor y tipo) y equal? (identidad de objeto)
puts "iguales=#{a == b}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
# En Perl el operador depende del tipo de comparación, no del dato: == numérica, eq textual
printf "iguales=%s\n", $a == $b ? "true" : "false";
```

### Lua

```lua
local a, b = io.read("n", "n")
-- Los números se comparan por valor; dos tablas distintas nunca son == salvo metamétodo __eq
print("iguales=" .. tostring(a == b))
```

### Tcl

```tcl
gets stdin linea
lassign [split [string trim $linea]] a b
set iguales [expr {$a == $b ? "true" : "false"}]
puts "iguales=$iguales"
```

### R

```r
v <- as.integer(strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]])
# == se vectoriza elemento a elemento; identical() es la comparación estricta de un solo valor
cat(sprintf("iguales=%s\n", tolower(as.character(v[1] == v[2]))))
```

**Qué reconocer:** los cinco comparan valores, no direcciones, pero cada uno paga el precio en un
sitio distinto. Ruby es el más explícito de toda la página: `==` pregunta por el valor, `eql?` exige
además el mismo tipo y `equal?` es la única que pregunta por **identidad** —si son literalmente el
mismo objeto en memoria—; tres métodos para tres preguntas que casi todos los demás lenguajes
mezclan en un operador. Perl invierte la lógica: no elige el tipo del dato sino el del operador, y
usar `eq` donde tocaba `==` es el error clásico de la familia. Lua es el caso didáctico puro: los
escalares se comparan por valor, pero **dos tablas con el mismo contenido nunca son iguales** a menos
que se defina el metamétodo `__eq` —la identidad es el comportamiento por defecto—. Tcl vuelve a su
extremo del *todo es cadena* y necesita `expr` incluso para preguntar si dos números coinciden. R
delata su origen estadístico: `==` no devuelve un booleano sino un vector de booleanos, y por eso la
comparación honesta de dos objetos completos se hace con `identical()`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia arrastra la cicatriz histórica de tener dos igualdades: una con coerción (`==`) y otra sin
ella (`===`).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  // Dart no tiene ==: el operador se redefine por clase; identical() da la identidad real
  print('iguales=${v[0] == v[1]}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra la comparación.
package {
    public class Igualdad {
        public static function iguales(a:int, b:int):String {
            // == aplica coerción de tipos; === compara valor y tipo sin convertir nada
            return "iguales=" + ((a === b) ? "true" : "false");
        }
    }
}
```

**Qué reconocer:** ActionScript 3 es JavaScript con tipos estáticos y conserva el par `==` / `===`
íntegro: la doble igualdad es exactamente la misma trampa de coerción, con las mismas reglas.
Dart hizo la reforma que JavaScript nunca pudo hacer: eliminó `==` con coerción, dejó un solo
operador de igualdad que las clases redefinen (`operator ==`) y movió la pregunta por la identidad a
una función aparte, `identical(a, b)`. Es el mismo reparto que hace Ruby, pero con dos nombres en
vez de tres.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). En Java `==` sobre objetos compara referencias
y `equals()` compara valores; ese único desajuste explica media biblioteca estándar.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    // Kotlin invierte la convención de Java: == llama a equals(), === compara referencias
    println("iguales=${a == b}")
}
```

### Scala

```scala
object Igualdad extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  // En Scala == es igualdad de valor (delega en equals); eq compara referencias
  println(s"iguales=${a == b}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
// Groovy también redefine ==: llama a equals(); la identidad se pregunta con is()
println("iguales=${a == b}")
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map #(Long/parseLong %) (str/split (str/trim (read-line)) #"\s+"))]
  ;; = compara siempre por valor estructural; identical? es la única vía a la referencia
  (println (str "iguales=" (= a b))))
```

**Qué reconocer:** los cuatro corren sobre la misma máquina virtual que Java y, aun así, **los cuatro
decidieron que `==` de Java estaba mal**. Kotlin, Scala y Groovy hacen el mismo movimiento: `==` pasa
a significar igualdad de valor (delega en `equals()`) y la identidad se retira a un operador aparte
—`===` en Kotlin, `eq` en Scala, `is()` en Groovy—. Es la corrección más unánime de toda esta página.
Clojure va un paso más allá y borra la pregunta: sus estructuras son inmutables, así que `=` compara
**valor estructural** siempre, hasta el fondo, y dos vectores con el mismo contenido son iguales sin
más. Cuando nada muta, la identidad deja de importar; `identical?` existe, pero apenas se usa.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Sobre el CLR conviven tipos de valor (`struct`),
que se comparan por contenido, y tipos de referencia (`class`), que por defecto se comparan por
dirección.

### F\#

```fsharp
let v =
    stdin.ReadLine().Trim().Split(' ')
    |> Array.map int
// En F# = es igualdad estructural, incluso para listas y registros
printfn "iguales=%b" (v.[0] = v.[1])
```

### VB.NET

```vbnet
Module Igualdad
    Sub Main()
        Dim p = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(p(0))
        Dim b = Integer.Parse(p(1))
        ' = compara valores; Is compara referencias de objeto
        Console.WriteLine("iguales=" & If(a = b, "true", "false"))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `Int32` y el mismo `Object.Equals`, pero se separan en la
sintaxis del reparto. VB.NET nunca sobrecargó `=` para referencias: hay `=` para valores y `Is` para
identidad, dos palabras distintas desde el primer día —la solución que C# solo alcanzó a medias—.
F# cambia el valor por defecto: sus registros, tuplas y listas tienen **igualdad estructural
generada**, así que `=` compara contenido sin escribir una línea, y si hace falta la identidad hay
que bajar a `System.Object.ReferenceEquals`. Es el mismo giro que hace Clojure, motivado por lo
mismo: cuando los datos son inmutables, comparar direcciones deja de tener sentido.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C `==` compara los bits del valor; si el valor es
un puntero, compara direcciones. No hay más igualdad que esa.

### C++

```cpp
#include <iostream>

int main() {
    long a, b;
    std::cin >> a >> b;
    // Sobre escalares == compara valor; sobre punteros compararía direcciones
    std::cout << "iguales=" << (a == b ? "true" : "false") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long a, b;
        scanf("%ld %ld", &a, &b);
        NSNumber *na = @(a), *nb = @(b);
        // isEqual: compara el valor envuelto; == sobre estos punteros compararía direcciones
        printf("iguales=%s\n", [na isEqual:nb] ? "true" : "false");
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C y heredan un `==` que solo sabe comparar bits. C++
lo arregla desde el lenguaje: permite **sobrecargar `operator==`** por tipo, de modo que `==` sobre
un `std::string` compara caracteres aunque sobre un `char*` compare direcciones —el mismo símbolo,
dos semánticas, según el tipo estático—. Objective-C lo arregla desde la biblioteca: el lenguaje deja
`==` intacto como comparación de punteros y añade el método `isEqual:` que cada clase implementa. Por
eso comparar dos `NSString` con `==` es el error de novato canónico del mundo Apple: compila,
a veces acierta por casualidad —las cadenas literales suelen compartirse— y falla en cuanto una de
las dos se construye en tiempo de ejecución.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con la igualdad decidida en tiempo de compilación según el tipo.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    // == solo vale para escalares: para slices y structs hay que usar std.mem.eql
    const r = if (a == b) "true" else "false";
    try std.io.getStdOut().writer().print("iguales={s}\n", .{r});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let v = stdin.readLine().splitWhitespace().map(parseInt)
## Sobre `ref` el == sigue el puntero salvo que se defina `proc ==` para el tipo
echo "iguales=", v[0] == v[1]
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm;

void main() {
    auto v = readln().split().map!(to!long).array;
    // En D == sobre clases llama a opEquals (valor); `is` compara identidad
    writeln("iguales=", v[0] == v[1] ? "true" : "false");
}
```

**Qué reconocer:** Zig es el más honesto y el más incómodo: `==` **solo existe para escalares**, y
comparar dos arreglos exige llamar a `std.mem.eql` a mano. No hay sobrecarga de operadores en el
lenguaje, así que nunca puedes equivocarte sobre qué está comparando `==` —pero tampoco puedes
escribirlo corto—. D toma la decisión contraria y hace explícito el reparto: `==` llama a `opEquals`
(valor) y `is` compara identidad, la misma pareja que Scala y Groovy pero con nombres de la familia
C. Nim se queda en medio: `==` compara valor para tipos normales y sigue el puntero para los `ref`,
salvo que definas tu propio `proc ==`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
comprobarlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    ( A =:= B -> R = "true" ; R = "false" ),
    format("iguales=~w~n", [R]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: se declaran los pares y las reglas que deciden.
par(5, 5).
par(3, 7).
par(0, 0).

iguales(A, B) :- par(A, B), A = B.
distintos(A, B) :- par(A, B), A != B.
```

**Qué reconocer:** Prolog es el lenguaje que hace la distinción de esta clase de forma más explícita
que ningún otro de la página, porque tiene **tres operadores donde los demás tienen uno o dos**. `=`
no compara: **unifica**, es decir, intenta ligar las variables libres de ambos lados para que los dos
términos se vuelvan idénticos —`X = 5` tiene éxito y deja `X` valiendo 5—. `==` sí compara: pregunta
si dos términos ya son estructuralmente idénticos, sin ligar nada, y `X == 5` fracasa si `X` está
libre. Y `=:=`, el que usa este programa, evalúa aritméticamente ambos lados antes de comparar, por
lo que `2 + 3 =:= 5` es verdadero mientras que `2 + 3 == 5` es falso —a la izquierda hay un término
compuesto, a la derecha un número—. Esa terna es exactamente el eje de la clase visto desde la
lógica: ligar, comparar la estructura, comparar el valor. Datalog conserva solo la comparación:
sin efectos, sin entrada y sin unificación libre, `=` es un simple filtro sobre las tuplas de la
base, la misma renuncia que hace SQL en su cláusula `WHERE`.

---

## Y de vuelta a la clase

Veinte lenguajes, una sola pregunta —¿estos dos son iguales?— y tres respuestas posibles que cada
familia reparte a su manera: mismo valor, mismo valor y tipo, mismo objeto. Los lenguajes viejos
mezclaron las tres en `==` y sus sucesores pasaron décadas separándolas; los lenguajes de datos
inmutables —Clojure, F#— simplemente borraron la pregunta por la identidad. Reconocer en qué grupo
cae un lenguaje que nunca has visto es lo transferible.

⏮️ [Volver a la clase 101](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
