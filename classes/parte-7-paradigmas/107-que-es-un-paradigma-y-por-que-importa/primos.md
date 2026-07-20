# 🧬 El mismo programa en las familias de lenguajes — Clase 107

> [⬅️ Volver a la clase 107](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —la suma de los enteros de 1 a `n`— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Un problema tan pequeño es aquí una herramienta de precisión: como cabe entero en cuatro líneas, lo
único que queda a la vista es **la forma de organizar la solución**. Y esa forma es exactamente lo
que llamamos paradigma. Verás el mismo cálculo escrito como bucle, como pliegue, como vector y como
regla lógica, y ninguna de esas versiones es una traducción de la otra: son maneras distintas de
pensar el problema.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (con `n >= 1`)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** `suma = 1 + 2 + ... + n`

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `3` | `suma=6` |
| `1` | `suma=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Son lenguajes multiparadigma por diseño: no te obligan a elegir. Por eso, dentro de esta misma
familia, el problema aparece resuelto de tres maneras distintas.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "suma=#{(1..n).sum}"
```

### Perl

```perl
my $n = <STDIN>;
my $suma = 0;
$suma += $_ for 1 .. $n;
print "suma=$suma\n";
```

### Lua

```lua
local n = tonumber(io.read("l"))
local suma = 0
for i = 1, n do
  suma = suma + i
end
print("suma=" .. suma)
```

### Tcl

```tcl
gets stdin n
set suma 0
for {set i 1} {$i <= $n} {incr i} {
    incr suma $i
}
puts "suma=$suma"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("suma=%d\n", sum(1:n)))
```

**Qué reconocer:** aquí está la lección entera de la clase en cinco programas. Lua y Tcl escriben un
**bucle imperativo**: hay una variable que cambia de valor en cada vuelta. Ruby no escribe bucle
ninguno: pide al **objeto rango** `(1..n)` que se sume a sí mismo, porque en Ruby hasta un rango es
un objeto con métodos. R no escribe bucle ni objeto: construye el **vector** `1:n` y lo agrega de
golpe, que es el paradigma vectorial que heredó de S y del cálculo estadístico. Perl queda en medio
con su `for` de modificador. Mismo lenguaje-familia, mismo resultado, tres modelos mentales
diferentes: el paradigma **no es una propiedad del lenguaje**, es la manera de organizar la solución
que el lenguaje te hace cómoda.

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
  for (var i = 1; i <= n; i++) {
    suma += i;
  }
  print('suma=$suma');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 corre en el reproductor Flash: no hay stdin ni consola,
// así que se muestra el mismo cálculo dentro de un método de clase.
package {
    public class Suma {
        public static function hasta(n:int):String {
            var suma:int = 0;
            for (var i:int = 1; i <= n; i++) {
                suma += i;
            }
            return "suma=" + suma;
        }
    }
}
```

**Qué reconocer:** los dos escriben el bucle `for` clásico heredado de C, con las mismas tres partes
(inicio, condición, avance). Pero fíjate en el **envoltorio**, que es lo paradigmático: Dart permite
una función `main` suelta, mientras que ActionScript 3 obliga a meter todo dentro de una clase dentro
de un paquete. Ese "todo tiene que ser un método de algo" es la herencia de Java sobre la familia
web, y es una decisión de paradigma, no de sintaxis.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La misma máquina virtual, el mismo bytecode y
la misma biblioteca estándar sirven de soporte a cuatro paradigmas distintos.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    println("suma=${(1..n).sum()}")
}
```

### Scala

```scala
object Suma extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"suma=${(1 to n).sum}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
println "suma=${(1..n).sum()}"
```

### Clojure

```clojure
(let [n (Integer/parseInt (.trim (read-line)))]
  (println (str "suma=" (reduce + (range 1 (inc n))))))
```

**Qué reconocer:** esta familia es la prueba más limpia de que el paradigma **no lo impone la
plataforma**. Los cuatro producen bytecode para la misma JVM que el `for` de Java de la clase, y sin
embargo ninguno escribe un bucle: los tres primeros piden a un rango que se sume, y Clojure lo dice
en voz alta con `reduce +`, que es el **pliegue** del paradigma funcional: una operación binaria
aplicada acumulativamente sobre una secuencia. Java necesita una variable `suma` que cambie de valor;
Clojure no tiene ninguna variable que cambie. Esa diferencia —hay estado mutable o no lo hay— es la
frontera paradigmática que esta parte del curso va a recorrer entera.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Dos lenguajes del mismo runtime, nacidos de dos
tradiciones opuestas.

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
printfn "suma=%d" (List.sum [ 1 .. n ])
```

### VB.NET

```vbnet
Module Suma
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim suma = 0
        For i = 1 To n
            suma += i
        Next
        Console.WriteLine("suma=" & suma)
    End Sub
End Module
```

**Qué reconocer:** comparten `System.Int32` y el mismo CLR, pero no comparten manera de pensar.
VB.NET viene del BASIC y escribe la receta paso a paso: declara el acumulador, lo modifica dentro del
`For`, lo imprime al final. F# viene de ML y escribe una **expresión**: construye la lista `[1..n]` y
la reduce con `List.sum`, sin acumulador y sin bucle, encadenando con `|>`. Ambos programas se
compilan a instrucciones parecidas; lo que cambia es dónde pone el autor su atención, en el *cómo* o
en el *qué*.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El paradigma imperativo en estado puro: memoria,
variables que cambian y control explícito del flujo.

### C++

```cpp
#include <iostream>

int main() {
    long long n = 0;
    std::cin >> n;
    long long suma = 0;
    for (long long i = 1; i <= n; ++i) suma += i;
    std::cout << "suma=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long n = 0;
        scanf("%ld", &n);
        long suma = 0;
        for (long i = 1; i <= n; i++) suma += i;
        printf("suma=%ld\n", suma);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C** y, para un problema como este, ninguno saca sus
capacidades añadidas: no hay clases, no hay plantillas, no hay mensajes. Es el recordatorio de que un
lenguaje multiparadigma no te obliga a usar todos sus paradigmas; C++ podría resolverlo con
`std::accumulate` y Objective-C con una categoría sobre `NSNumber`, y eligen no hacerlo porque el
bucle es lo natural aquí. Elegir paradigma es una decisión de diseño, no una obligación del
compilador.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilan a binario nativo
y se toman en serio el coste de cada abstracción.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r"), 10);
    var suma: u64 = 0;
    var i: u64 = 1;
    while (i <= n) : (i += 1) suma += i;
    try std.io.getStdOut().writer().print("suma={d}\n", .{suma});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var suma = 0
for i in 1 .. n:
  suma += i
echo "suma=", suma
```

### D

```d
import std.stdio, std.string, std.conv, std.range, std.algorithm;

void main() {
    const n = readln().strip().to!int;
    writefln("suma=%d", iota(1, n + 1).sum);
}
```

**Qué reconocer:** Zig es deliberadamente el más pobre en paradigmas —no tiene clases, ni cierres con
captura implícita, ni sobrecarga de operadores— y esa pobreza es su tesis: **una sola manera de hacer
las cosas** para que leer el código baste para saber qué máquina se ejecuta. Nim escribe el mismo
bucle con aspecto de Python. D elige el otro extremo dentro de la misma familia: `iota(1, n+1).sum`
es una tubería declarativa sobre rangos perezosos, sin bucle visible, y aun así compila al mismo
binario nativo. Rendimiento y paradigma son ejes **independientes**.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
recorrerlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

% No hay bucle ni acumulador: dos reglas que definen qué es la suma hasta N.
suma(0, 0).
suma(N, S) :- N > 0, M is N - 1, suma(M, S0), S is S0 + N.

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    suma(N, S),
    format("suma=~d~n", [S]).
```

### Datalog

```datalog
// Datalog no tiene E/S ni bucles: los sumandos entran como hechos y la suma
// se obtiene con la agregación de Soufflé, que es una consulta, no un recorrido.
.decl sumando(x:number)
sumando(1). sumando(2). sumando(3). sumando(4). sumando(5).

.decl suma(s:number)
suma(s) :- s = sum x : { sumando(x) }.
```

**Qué reconocer:** Prolog no ofrece bucle porque no tiene nada que iterar: define la relación
`suma(N, S)` con dos cláusulas —el caso base y el caso general— y deja que el motor de resolución
encuentre el valor. `S is S0 + N` **no asigna**: liga `S` una sola vez con el resultado. Datalog va
más lejos y renuncia incluso a la recursión aritmética libre; el programa no dice en qué orden se
calcula nada. Este es el contraste más fuerte de toda la página: si en Java o en C quitas el bucle no
queda programa, y aquí el bucle nunca existió. Eso es cambiar de paradigma, no de sintaxis.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema de cuatro líneas, y cuatro maneras irreducibles de plantearlo:
acumular en un bucle, plegar una secuencia, agregar un vector y declarar una relación. Ninguna es más
correcta; cada una hace fácil un tipo de cambio y difícil otro. Reconocer cuál estás usando —y saber
que podías haber usado otra— es lo que esta parte del curso te va a pedir en cada clase.

⏮️ [Volver a la clase 107](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
