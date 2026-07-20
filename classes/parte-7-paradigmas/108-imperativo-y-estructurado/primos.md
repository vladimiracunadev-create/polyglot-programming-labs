# 🧬 El mismo programa en las familias de lenguajes — Clase 108

> [⬅️ Volver a la clase 108](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar una lista de enteros con un acumulador y un
bucle explícito— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El estilo imperativo estructurado es el mínimo común denominador de casi toda la programación:
secuencia, selección e iteración, sin saltos arbitrarios. Por eso este programa se parece tanto de un
lenguaje a otro. Lo interesante son las dos excepciones, las que **no pueden** escribirlo tal cual
porque no tienen variables que cambien de valor.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** acumular la suma recorriendo la lista

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20` | `suma=30` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos heredan las tres estructuras de control del imperativo estructurado, y ninguno necesita
declarar el acumulador con un tipo.

### Ruby

```ruby
suma = 0
STDIN.gets.split.each { |x| suma += x.to_i }
puts "suma=#{suma}"
```

### Perl

```perl
my @nums = split ' ', <STDIN>;
my $suma = 0;
foreach my $x (@nums) {
    $suma += $x;
}
print "suma=$suma\n";
```

### Lua

```lua
local suma = 0
for palabra in io.read("l"):gmatch("%S+") do
  suma = suma + tonumber(palabra)
end
print("suma=" .. suma)
```

### Tcl

```tcl
gets stdin linea
set suma 0
foreach x [split [string trim $linea]] {
    incr suma $x
}
puts "suma=$suma"
```

### R

```r
nums <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
suma <- 0L
for (x in nums) {
  suma <- suma + x
}
cat(sprintf("suma=%d\n", suma))
```

**Qué reconocer:** los cinco tienen acumulador y bucle, pero el **bucle no es la misma construcción**
en todos. Perl, Lua, Tcl y R escriben un `for`/`foreach` de verdad: una estructura de control del
lenguaje. Ruby no: `each` es un **método** al que se le pasa un bloque, y el recorrido lo dirige el
propio objeto colección; el estilo es imperativo pero la máquina que hay debajo es orientada a
objetos. Tcl lleva su rareza habitual: `incr suma $x` es un **comando** que muta una variable por
nombre, porque en Tcl todo, incluido `for`, es una llamada a comando y no palabra reservada. R, que
podría escribir `sum(nums)` de una vez, aquí acepta el bucle: se puede programar imperativo en un
lenguaje vectorial, solo que a la comunidad de R le parecerá mal escrito.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  var suma = 0;
  for (final t in stdin.readLineSync()!.trim().split(RegExp(r'\s+'))) {
    suma += int.parse(t);
  }
  print('suma=$suma');
}
```

### ActionScript 3

```actionscript
// El reproductor Flash no tiene stdin: la lista llega ya troceada como argumento.
package {
    public class Suma {
        public static function total(nums:Array):String {
            var suma:int = 0;
            for (var i:int = 0; i < nums.length; i++) {
                suma += int(nums[i]);
            }
            return "suma=" + suma;
        }
    }
}
```

**Qué reconocer:** ActionScript 3 usa el `for` con índice, la forma más antigua y más literalmente
imperativa: hay **dos** variables que cambian, el acumulador y el índice. Dart usa `for-in`, que
recorre la colección sin exponer la posición y elimina de golpe la familia de errores de índice
fuera de rango. Ese cambio —de "avanza el contador y accede a la posición" a "dame el siguiente
elemento"— es la evolución que el estructurado hizo dentro del propio paradigma imperativo, sin
salirse de él.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Aquí se ve la grieta: tres primos escriben el
bucle imperativo sin problema y el cuarto no puede.

### Kotlin

```kotlin
fun main() {
    var suma = 0
    for (t in readLine()!!.trim().split(Regex("\\s+"))) {
        suma += t.toInt()
    }
    println("suma=$suma")
}
```

### Scala

```scala
object Suma extends App {
  var suma = 0
  for (t <- scala.io.StdIn.readLine().trim.split("\\s+")) suma += t.toInt
  println(s"suma=$suma")
}
```

### Groovy

```groovy
def suma = 0
System.in.newReader().readLine().trim().split(/\s+/).each { suma += it as int }
println "suma=$suma"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure no tiene variables locales que se reasignen: no hay dónde acumular.
;; `loop`/`recur` hace de bucle pasando el acumulador como argumento en cada vuelta.
(loop [nums (map #(Integer/parseInt %) (str/split (str/trim (read-line)) #"\s+"))
       suma 0]
  (if (seq nums)
    (recur (rest nums) (+ suma (first nums)))
    (println (str "suma=" suma))))
```

**Qué reconocer:** Kotlin y Scala marcan el acumulador con `var` frente a `val`, y ese detalle es
exactamente el tema de la clase: la mutación es una decisión que el lenguaje te obliga a declarar.
Scala, además, ofrece las dos vías a la vez —esto se escribiría idiomáticamente `nums.sum`— y deja al
autor elegir paradigma; es su diseño explícito de lenguaje mixto. Clojure no ofrece esa elección:
**no existe** una variable local que se reasigne, así que el bucle se convierte en `loop`/`recur`,
donde cada vuelta es una llamada con un acumulador nuevo. Sigue habiendo iteración y sigue habiendo
resultado; lo que ha desaparecido es el estado que cambia. Es la misma JVM, la misma clase de
problema, y otro paradigma.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// F# admite `mutable`, pero lo señala como algo excepcional: hay que pedirlo
// por escrito y usar `<-` en vez de `=` para reasignar.
let mutable suma = 0
for t in stdin.ReadLine().Trim().Split(' ') do
    suma <- suma + int t
printfn "suma=%d" suma
```

### VB.NET

```vbnet
Module Suma
    Sub Main()
        Dim suma As Integer = 0
        For Each t In Console.ReadLine().Trim().Split(" "c)
            suma += Integer.Parse(t)
        Next
        Console.WriteLine("suma=" & suma)
    End Sub
End Module
```

**Qué reconocer:** VB.NET desciende directamente del BASIC, uno de los lenguajes en los que se libró
la batalla de la programación estructurada contra el `GOTO`; su `For Each ... Next` es el imperativo
canónico y nada en él sugiere que hubiera otra opción. F# hace lo contrario: puede escribir el mismo
bucle, pero te cobra el peaje de la palabra `mutable` y del operador `<-`, para que la mutación se
vea en el diff. Idiomáticamente un programador de F# habría escrito
`Array.sumBy int` y ningún acumulador. Mismo runtime, misma biblioteca, distinta idea de qué debe ser
lo cómodo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El hogar del paradigma: variables, bucles y una
condición de salida.

### C++

```cpp
#include <iostream>

int main() {
    long long suma = 0;
    for (long long x; std::cin >> x;) suma += x;
    std::cout << "suma=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long suma = 0;
        long x = 0;
        while (scanf("%ld", &x) == 1) {
            suma += x;
        }
        printf("suma=%ld\n", suma);
    }
    return 0;
}
```

**Qué reconocer:** ambos usan un bucle cuya condición **es la propia lectura**: se itera mientras la
entrada siga dando números. Es el idioma clásico de C, y muestra que en el imperativo estructurado la
condición del bucle puede tener efectos secundarios, algo impensable en un paradigma declarativo.
Objective-C, pese a ser un lenguaje orientado a objetos completo, aquí se comporta como C puro: su
capa de objetos es **aditiva**, y cuando el problema no la necesita, desaparece.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust).

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var suma: i64 = 0;
    while (it.next()) |t| suma += try std.fmt.parseInt(i64, t, 10);
    try std.io.getStdOut().writer().print("suma={d}\n", .{suma});
}
```

### Nim

```nim
import std/strutils

var suma = 0
for t in stdin.readLine().splitWhitespace():
  suma += t.parseInt()
echo "suma=", suma
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    long suma = 0;
    foreach (t; readln().strip().split()) {
        suma += t.to!long;
    }
    writefln("suma=%d", suma);
}
```

**Qué reconocer:** los tres distinguen explícitamente lo que muta de lo que no: `var` frente a
`const` en Zig y en D, `var` frente a `let` en Nim. El acumulador es de los pocos valores que
necesitan ser mutables, y el compilador te lo hace declarar. Zig además no tiene `for` con condición
—solo `while` y `for` sobre colecciones—, una restricción deliberada para que todo bucle tenga una
forma reconocible de un vistazo. Es programación estructurada llevada al reglamento.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay acumulador porque no hay recorrido que
programar.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene variables que se reasignen: el acumulador viaja como argumento
% y la recursión sobre la lista hace de bucle.
suma([], 0).
suma([X|Xs], S) :- suma(Xs, S0), S is S0 + X.

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    maplist([T, X]>>number_string(X, T), Partes, Nums),
    suma(Nums, Total),
    format("suma=~d~n", [Total]).
```

### Datalog

```datalog
// Datalog no tiene E/S, ni bucles, ni orden de ejecución: los números entran
// como hechos y la suma se declara con la agregación de Soufflé.
.decl numero(x:number)
numero(1). numero(2). numero(3).

.decl suma(s:number)
suma(s) :- s = sum x : { numero(x) }.
```

**Qué reconocer:** en Prolog una variable se liga **una sola vez**; `S is S0 + X` no incrementa nada,
crea una ligadura nueva. Por eso el acumulador no puede vivir fuera del bucle: tiene que pasar como
argumento de una llamada a otra, y el bucle se convierte en recursión. Datalog ni siquiera admite
eso: no puedes preguntar *en qué orden* suma sus hechos, porque el orden no forma parte del lenguaje.
Aquí el contraste con C o Java es total —ningún concepto de esta clase, ni acumulador ni iteración ni
secuencia, sobrevive al cambio de paradigma— y conviene decirlo sin rodeos: no es que se escriba
distinto, es que el problema se plantea de otra manera.

---

## Y de vuelta a la clase

Veinte lenguajes y el mismo esqueleto en dieciocho de ellos: empezar en cero, recorrer, acumular,
imprimir. Esa uniformidad es la razón de que el estilo imperativo estructurado sea lo primero que se
enseña casi en todas partes. Las dos excepciones —Clojure y Prolog— son las que enseñan de verdad
dónde está el límite del paradigma.

⏮️ [Volver a la clase 108](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
