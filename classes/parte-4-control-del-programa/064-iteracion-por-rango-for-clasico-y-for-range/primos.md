# 🧬 El mismo programa en las familias de lenguajes — Clase 064

> [⬅️ Volver a la clase 064](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el factorial de n con un bucle por rango— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Si entendiste la versión de Go, la de Nim te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` con `0 <= n <= 20`
- **Salida** (stdout): `factorial=<n!>`
- **Regla:** `n! = 1 · 2 · … · n`, y `0! = 1` (el rango vacío deja el acumulador en 1)

| stdin | esperado |
|---|---|
| `5` | `factorial=120` |
| `1` | `factorial=1` |
| `0` | `factorial=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Esta familia casi abandonó el `for` clásico de tres partes: itera sobre un rango o una colección, y
el contador ni siquiera se declara.

### Ruby

```ruby
n = STDIN.gets.to_i
f = 1
(1..n).each { |i| f *= i }
puts "factorial=#{f}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my $f = 1;
$f *= $_ for 1 .. $n;   # for en posición sufija; $_ es el elemento actual
print "factorial=$f\n";
```

### Lua

```lua
local n = tonumber(io.read("l"))
local f = 1
for i = 1, n do
    f = f * i
end
print("factorial=" .. f)
```

### Tcl

```tcl
gets stdin n
set f 1
for {set i 1} {$i <= $n} {incr i} {
    set f [expr {$f * $i}]
}
puts "factorial=$f"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
f <- 1
# seq_len(n) devuelve un rango VACÍO cuando n es 0; el clásico 1:n
# daría c(1, 0) y el factorial de 0 saldría 0. Es la trampa canónica de R.
for (i in seq_len(n)) f <- f * i
cat(sprintf("factorial=%.0f\n", f))
```

**Qué reconocer:** Lua es el único que conserva un `for` numérico propio (`for i = 1, n do`), con
inicio, fin y paso opcional como parte de la sintaxis. Ruby y Perl ni eso: construyen el **rango**
`1..n` como valor y lo recorren, exactamente igual que `range(1, n+1)` en Python. Tcl es la
excepción hacia atrás —su `for` es el de C, con las tres partes explícitas, porque en Tcl todo es
comando y no hay objeto rango—. Y R deja al descubierto el caso límite de esta clase: con `n = 0`,
`1:n` no produce un rango vacío sino la secuencia descendente `1, 0`, y por eso se usa `seq_len`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var f = 1;
  for (var i = 1; i <= n; i++) {
    f *= i;
  }
  print('factorial=$f');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin: se ilustra el bucle, idéntico al de JavaScript.
package {
    public class Factorial {
        public static function de(n:int):String {
            var f:Number = 1;
            for (var i:int = 1; i <= n; i++) {
                f *= i;
            }
            return "factorial=" + f;
        }
    }
}
```

**Qué reconocer:** los dos escriben el `for` de tres partes de C, letra por letra. Esta familia no
tiene rango numérico como valor: `for…in` recorre **claves** y `for…of` (en JavaScript y Dart)
recorre elementos de una colección, pero para contar del 1 al n hay que declarar el contador a mano.
Ojo al tipo en ActionScript: `Number` es coma flotante de doble precisión, así que a partir de 18!
los dígitos dejan de ser exactos; Dart usa enteros de 64 bits y llega a 20! sin perder nada.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El `for` clásico de Java sigue disponible en
los cuatro, pero ninguno lo usa si puede evitarlo.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    var f = 1L
    for (i in 1..n) {
        f *= i
    }
    println("factorial=$f")
}
```

### Scala

```scala
object Factorial extends App {
  val n = scala.io.StdIn.readInt()
  var f = 1L
  for (i <- 1 to n) f *= i
  println(s"factorial=$f")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def f = 1G   // BigInteger
// Cuidado: en Groovy (1..0) es un rango DESCENDENTE, no vacío.
// Con n = 0 recorrería [1, 0] y el resultado sería 0, así que aquí
// el for clásico es lo correcto.
for (int i = 1; i <= n; i++) {
    f *= i
}
println "factorial=$f"
```

### Clojure

```clojure
;; Sin contador ni acumulador mutables: range produce la secuencia perezosa
;; y reduce la colapsa. Con n = 0, (range 1 1) está vacío y queda el valor inicial.
(let [n (Integer/parseInt (.trim (read-line)))]
  (println (str "factorial=" (reduce *' 1 (range 1 (inc n))))))
```

**Qué reconocer:** Kotlin y Scala sustituyen las tres partes de Java por un **rango como valor**
(`1..n`, `1 to n`), y el `for` de Scala ni siquiera es un bucle: el compilador lo reescribe como
`(1 to n).foreach { … }`, por eso el mismo `for` sirve luego para listas, opciones o futuros.
Clojure abandona la iteración por completo: `reduce` sobre `range` dice *qué* se acumula, no *cómo*
se recorre —y `*'` es la multiplicación que promociona a `BigInt` en vez de desbordar—. Groovy
recuerda que los rangos también tienen bordes afilados: `1..0` cuenta hacia atrás.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
// [1L .. 0L] es la lista vacía, así que fold devuelve el valor inicial: 0! = 1.
let f = [ 1L .. int64 n ] |> List.fold ( * ) 1L
printfn "factorial=%d" f
```

### VB.NET

```vbnet
Module Factorial
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim f As Long = 1
        For i As Integer = 1 To n
            f *= i
        Next
        Console.WriteLine("factorial=" & f)
    End Sub
End Module
```

**Qué reconocer:** VB.NET tiene el `For … To … Step … Next` heredado de BASIC, que es una iteración
por rango de pleno derecho: los límites se evalúan **una sola vez** al entrar, y con `1 To 0` el
cuerpo no se ejecuta nunca —justo lo que el caso `n = 0` necesita—. F# también tiene ese `for`, pero
el estilo de la comunidad es el de arriba: construir la lista `[1 .. n]` y plegarla con `fold`, sin
contador ni variable mutable. Es la misma idea que el `reduce` de Clojure, en otra máquina virtual.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El `for (init; cond; paso)` de tres partes nació
aquí, y sus primos no le han tocado nada.

### C++

```cpp
#include <iostream>

int main() {
    int n;
    std::cin >> n;
    unsigned long long f = 1;
    for (int i = 1; i <= n; ++i) {
        f *= static_cast<unsigned long long>(i);
    }
    std::cout << "factorial=" << f << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        unsigned long long f = 1;
        for (int i = 1; i <= n; i++) {
            f *= (unsigned long long)i;
        }
        printf("factorial=%llu\n", f);
    }
    return 0;
}
```

**Qué reconocer:** el bucle es el de C, idéntico, y ambos añadieron después un `for` sobre
colecciones —`for (auto x : v)` en C++11, `for (id x in array)` en Objective-C— pero ninguno tiene
rango numérico: para contar del 1 al n sigues escribiendo las tres partes. La otra herencia visible
es el tipo: aquí el desbordamiento no avisa, y `unsigned long long` es lo mínimo para que 20! (algo
más de 2,4 · 10^18) quepa sin envolver.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos eliminaron el
`for` de tres partes en favor del rango, y sus vecinos hicieron lo mismo.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(usize, std.mem.trim(u8, linea, " \r"), 10);
    var f: usize = 1;
    // El for de Zig solo recorre rangos y secuencias: no existe la forma
    // de tres partes. Con n = 0 el rango 1..1 está vacío.
    for (1..n + 1) |i| {
        f *= i;
    }
    try std.io.getStdOut().writer().print("factorial={d}\n", .{f});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var f = 1
for i in 1 .. n:
  f *= i
echo "factorial=", f
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!int;
    long f = 1;
    foreach (i; 1 .. n + 1) {
        f *= i;
    }
    writefln("factorial=%d", f);
}
```

**Qué reconocer:** los tres escriben el rango y nada más, igual que `for i := 1; i <= n; i++` dejó
paso en Go a `for range` y en Rust a `for i in 1..=n`. Fíjate en los bordes, que es donde se separan:
Nim usa `1 .. n` **inclusivo** (y `1 ..< n` para excluir el final), mientras Zig y D usan
`1..n+1` y `1 .. n+1` con el extremo **exclusivo**, como Rust y Python. El mismo bucle, un `+1` de
diferencia, y el error de índice por uno más común del oficio. D conserva además el `for` de C, pero
su comunidad escribe `foreach`.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Sin bucle ni contador: se declara el rango y el
motor lo genera.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    % between/3 no es un bucle: genera 1, 2, … N por BACKTRACKING, una
    % solución cada vez, y findall recoge todas. Con N = 0 falla ya en la
    % primera y la lista queda vacía, así que el pliegue devuelve 1.
    findall(I, between(1, N, I), Is),
    foldl([X, A0, A]>>(A is A0 * X), Is, 1, F),
    format("factorial=~d~n", [F]).
```

### Datalog

```datalog
% Datalog no tiene bucles ni E/S: el rango se deriva como punto fijo de una
% regla recursiva, y el producto se acumula en la misma relación.
entrada(5).

fact(0, 1).
fact(I, F) :- fact(J, G), entrada(N), I = J + 1, I <= N, F = G * I.

resultado(F) :- entrada(N), fact(N, F).
```

**Qué reconocer:** Prolog **no itera con bucles**: `between(1, N, I)` es un generador que produce una
solución por vez y deja un punto de elección; el recorrido lo hace el motor al retroceder, y
`findall` fuerza esa exploración hasta agotarla. Solo después `foldl` multiplica la lista, que es el
mismo pliegue de F# y Clojure. Datalog no tiene ni siquiera generadores: `fact/2` se declara y el
evaluador aplica la regla una y otra vez hasta que deja de derivar hechos nuevos —el rango completo
`fact(0,1), fact(1,1), fact(2,2)…` existe como relación—, y la consulta solo elige la fila que
interesa. Es literalmente el CTE recursivo del `main.sql` de la clase.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una evolución muy visible: del `for` de tres partes de C, que
sobrevive en C++, Objective-C, Tcl y la familia web, al **rango como valor** de Kotlin, Zig, Nim,
Rust o Ruby, y de ahí al pliegue sin contador de Clojure, F# y Prolog. En los tres estilos el caso
`n = 0` se resuelve igual: el rango queda vacío y el acumulador conserva su 1.

⏮️ [Volver a la clase 064](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
