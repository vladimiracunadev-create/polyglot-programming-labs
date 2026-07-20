# 🧬 El mismo programa en las familias de lenguajes — Clase 063

> [⬅️ Volver a la clase 063](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar los enteros de 1 a n con un bucle por
condición— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de C, la de Zig te resultará familiar aunque no la hayas visto nunca. Ese
reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (con `n >= 1`)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** acumular `1 + 2 + … + n` repitiendo mientras se cumpla la condición

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `1` | `suma=1` |
| `10` | `suma=55` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El bucle por condición es el punto donde esta familia se parece más a C: la variable de control es
mutable, la condición se evalúa arriba y el paso se escribe a mano.

### Ruby

```ruby
n = STDIN.gets.to_i
suma = 0
i = 1
while i <= n
  suma += i
  i += 1
end
puts "suma=#{suma}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
my ($suma, $i) = (0, 1);
while ($i <= $n) {
    $suma += $i;
    $i++;
}
print "suma=$suma\n";
```

### Lua

```lua
local n = tonumber(io.read("l"))
local suma, i = 0, 1
while i <= n do
    suma = suma + i
    i = i + 1
end
print("suma=" .. suma)
```

### Tcl

```tcl
gets stdin n
set suma 0
set i 1
while {$i <= $n} {
    incr suma $i
    incr i
}
puts "suma=$suma"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
suma <- 0L
i <- 1L
while (i <= n) {
  suma <- suma + i
  i <- i + 1L
}
cat(sprintf("suma=%d\n", suma))
```

**Qué reconocer:** los cinco `while` son el mismo, hasta en la trampa: si olvidas incrementar `i` el
bucle no termina, y ningún tipado dinámico te avisa. Ruby, Perl y Lua traen además la variante de
condición al final (`begin … end while`, `do { } while`, `repeat … until`) que garantiza al menos una
vuelta. Tcl es el caso curioso: la condición va entre llaves para que el intérprete la reevalúe en
cada vuelta —si usaras comillas se sustituiría una sola vez y el bucle sería infinito—, y `incr` es
un comando, no un operador. R permite el bucle pero su comunidad lo evita: escribiría `sum(1:n)`,
porque el lenguaje está pensado para operar sobre vectores enteros de una vez.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var suma = 0;
  var i = 1;
  while (i <= n) {
    suma += i;
    i++;
  }
  print('suma=$suma');
}
```

### ActionScript 3

```actionscript
// ActionScript no tiene stdin: se ilustra el bucle, idéntico al de JavaScript.
package {
    public class Suma {
        public static function hasta(n:int):String {
            var suma:int = 0;
            var i:int = 1;
            while (i <= n) {
                suma += i;
                i++;
            }
            return "suma=" + suma;
        }
    }
}
```

**Qué reconocer:** `while`, `do…while`, `break` y `continue` son literalmente los de C en los dos, y
también en JavaScript: esta familia no cambió nada del bucle por condición. La única diferencia entre
los primos está en la declaración de la variable de control: `var` con tipo en ActionScript, `var`
con tipo **inferido** en Dart. En JavaScript esa misma variable declarada con `var` se filtraría
fuera del bucle, y por eso se usa `let`.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Tres de los cuatro primos heredan el `while`
de Java; el cuarto no tiene bucles en absoluto.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    var suma = 0L
    var i = 1
    while (i <= n) {
        suma += i
        i++
    }
    println("suma=$suma")
}
```

### Scala

```scala
object Suma extends App {
  val n = scala.io.StdIn.readInt()
  var suma = 0
  var i = 1
  while (i <= n) {
    suma += i
    i += 1
  }
  println(s"suma=$suma")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def suma = 0
def i = 1
while (i <= n) {
    suma += i
    i++
}
println "suma=$suma"
```

### Clojure

```clojure
;; Clojure no tiene bucles con variable mutable: loop/recur es una
;; recursión de cola que el compilador convierte en un salto, sin crecer la pila.
(let [n (Integer/parseInt (.trim (read-line)))]
  (println (str "suma="
                (loop [i 1, suma 0]
                  (if (> i n)
                    suma
                    (recur (inc i) (+ suma i)))))))
```

**Qué reconocer:** Kotlin, Scala y Groovy escriben el `while` de Java sin tocar una coma, pero lo
marcan como territorio ajeno: los tres exigen `var` en vez de `val`/`def` inmutable, y en Scala 3 el
`while` como expresión devuelve `Unit`, señal de que solo sirve por sus efectos. Clojure lo prohíbe
directamente. Su `loop`/`recur` dice lo mismo al revés: en lugar de mutar `i` y `suma`, **rebota al
principio con valores nuevos**. La condición sigue ahí (`(> i n)`), solo que como caso base.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let mutable suma = 0
let mutable i = 1
while i <= n do
    suma <- suma + i
    i <- i + 1
printfn "suma=%d" suma
```

### VB.NET

```vbnet
Module Suma
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim suma = 0
        Dim i = 1
        Do While i <= n
            suma += i
            i += 1
        Loop
        Console.WriteLine("suma=" & suma)
    End Sub
End Module
```

**Qué reconocer:** F# tiene `while`, pero obliga a declarar `mutable` explícitamente y a asignar con
`<-` en vez de `=`: el lenguaje te hace escribir que estás mutando estado, porque por defecto no lo
permite. VB.NET, en el otro extremo, tiene la familia de bucles más verbosa y más flexible del CLR:
`Do While … Loop`, `Do Until … Loop` y sus dos variantes con la condición al final (`Do … Loop While`),
que cubren en una sola construcción lo que C reparte entre `while` y `do…while`.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El `while` de la clase nació aquí y sus dos primos
lo heredan sin un solo cambio.

### C++

```cpp
#include <iostream>

int main() {
    long long n;
    std::cin >> n;
    long long suma = 0;
    long long i = 1;
    while (i <= n) {
        suma += i;
        ++i;
    }
    std::cout << "suma=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long n;
        scanf("%lld", &n);
        long long suma = 0;
        long long i = 1;
        while (i <= n) {
            suma += i;
            i++;
        }
        printf("suma=%lld\n", suma);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C**: el bucle del `main.c` de la clase compila tal
cual en los dos. C++ solo cambia la entrada y la salida (`std::cin` / `std::cout` en vez de `scanf`
y `printf`) y prefiere `++i` a `i++` por costumbre heredada de los iteradores, donde el preincremento
evita copiar. Objective-C ni eso: conserva `scanf` y `printf` intactos y añade únicamente el bloque
de gestión de memoria.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y explícitos
sobre el coste, con una idea muy propia de cómo debe escribirse el paso del bucle.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    var suma: i64 = 0;
    var i: i64 = 1;
    // La cláusula `: (i += 1)` es el paso: se ejecuta siempre al final de
    // cada vuelta, incluso si el cuerpo usa `continue`.
    while (i <= n) : (i += 1) {
        suma += i;
    }
    try std.io.getStdOut().writer().print("suma={d}\n", .{suma});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var suma = 0
var i = 1
while i <= n:
  suma += i
  inc i
echo "suma=", suma
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    long suma = 0;
    long i = 1;
    while (i <= n) {
        suma += i;
        i++;
    }
    writefln("suma=%d", suma);
}
```

**Qué reconocer:** D copia el `while` de C sin retoques y Nim solo cambia las llaves por indentación
—`inc i` es un procedimiento, no un operador, porque Nim no tiene `++`—. Zig introduce la novedad
real de la familia: la **cláusula de continuación** `: (i += 1)`, que separa el paso del cuerpo. No es
azúcar: garantiza que el incremento ocurra también cuando el cuerpo salta con `continue`, que es
justo el error clásico del `while` de C. Es la misma preocupación de Rust al no tener `do…while` y
obligar a escribir `loop { … if cond { break } }`, donde la condición se ve dónde está.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay bucle porque no hay estado que mutar: la
repetición se expresa como **recursión** y el motor la lleva hasta el punto fijo.

### Prolog

```prolog
:- initialization(main, main).

% Prolog no tiene while: la repetición es recursión con acumulador.
% La condición de parada es la cabeza de la primera cláusula.
suma_acc(I, N, Acc, Acc) :- I > N, !.
suma_acc(I, N, Acc, S) :-
    Acc1 is Acc + I,
    I1 is I + 1,
    suma_acc(I1, N, Acc1, S).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    suma_acc(1, N, 0, S),
    format("suma=~d~n", [S]).
```

### Datalog

```datalog
% Datalog no tiene bucles ni E/S: la iteración es el punto fijo de una
% regla recursiva, evaluada hasta que no se derivan hechos nuevos.
entrada(5).

acum(1, 1).
acum(I, S) :- acum(J, T), entrada(N), I = J + 1, I <= N, S = T + I.

suma(S) :- entrada(N), acum(N, S).
```

**Qué reconocer:** aquí el concepto de la clase no existe y no se disimula. Prolog **itera por
recursión y backtracking**, nunca con bucles: `suma_acc/4` lleva el acumulador como argumento
—`Acc` es la `suma` del `while`, `I` es el contador— y la condición `I > N` que en C va en el
paréntesis del `while` aquí es la primera cláusula, la que detiene la recursión. El `!` impide que
al retroceder se pruebe también la cláusula recursiva. Datalog ni siquiera recursa paso a paso:
declara `acum` y deja que el motor derive todos los hechos que se sigan de las reglas, hasta que
dejan de aparecer nuevos. Ese "hasta que no cambia nada" es su versión de la condición de parada.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y tres formas de repetir: mutar un contador hasta que falle la
condición (C, Ruby, Zig), rebotar al principio con valores nuevos (Clojure, Prolog) o declarar la
relación y dejar que el motor llegue al punto fijo (Datalog, SQL). Las tres calculan `15`. Reconocer
cuál tienes delante es lo transferible.

⏮️ [Volver a la clase 063](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
