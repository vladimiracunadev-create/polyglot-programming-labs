# 🧬 El mismo programa en las familias de lenguajes — Clase 044

> [⬅️ Volver a la clase 044](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el mismo entero escrito en cuatro bases— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `n` (entero no negativo)
- **Salida** (stdout): `dec=<n> hex=<hex minúscula> oct=<octal> bin=<binario>`
- **Regla:** la misma `n` en base 10, 16, 8 y 2, sin prefijos ni ceros a la izquierda

| stdin | esperado |
|---|---|
| `255` | `dec=255 hex=ff oct=377 bin=11111111` |
| `10` | `dec=10 hex=a oct=12 bin=1010` |
| `1` | `dec=1 hex=1 oct=1 bin=1` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Enteros sin tamaño declarado y una biblioteca que ya sabe cambiar de base. Lo que separa a los
primos es cuál de las cuatro bases se les olvidó incluir.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "dec=#{n} hex=#{n.to_s(16)} oct=#{n.to_s(8)} bin=#{n.to_s(2)}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
printf "dec=%d hex=%x oct=%o bin=%b\n", $n, $n, $n, $n;
```

### Lua

```lua
local n = io.read("n")

-- Lua no tiene formato binario: se construye dígito a dígito.
local bin, t = "", n
repeat
  bin = tostring(t % 2) .. bin
  t = t // 2
until t == 0

print(string.format("dec=%d hex=%x oct=%o bin=%s", n, n, n, bin))
```

### Tcl

```tcl
# %b existe en format desde Tcl 8.6.
gets stdin n
puts [format "dec=%d hex=%x oct=%o bin=%b" $n $n $n $n]
```

### R

```r
n <- scan("stdin", what = integer(), n = 1, quiet = TRUE)
# sprintf de R no tiene %b: el binario se arma con intToBits y se podan los ceros.
bits <- paste(rev(as.integer(intToBits(n))), collapse = "")
bin <- sub("^0+(?=.)", "", bits, perl = TRUE)
cat(sprintf("dec=%d hex=%x oct=%o bin=%s\n", n, n, n, bin))
```

**Qué reconocer:** Ruby ofrece la solución más general —`to_s(base)` acepta cualquier base de 2 a
36— mientras que Perl, Tcl y R heredan de C la familia `%x`/`%o` y solo discrepan en el binario, que
C nunca tuvo. Ahí está la lección: **el binario es el caso especial de casi todos los lenguajes**,
porque la tradición de `printf` no lo incluía. En R aparece además su naturaleza vectorial:
`intToBits` no devuelve un número sino los 32 bits como un vector que hay que invertir y pegar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('dec=$n '
      'hex=${n.toRadixString(16)} '
      'oct=${n.toRadixString(8)} '
      'bin=${n.toRadixString(2)}');
}
```

### ActionScript 3

```actionscript
package {
    // Sin stdin en el reproductor Flash: se ilustra el cambio de base.
    public class Bases {
        public static function bases(n:uint):String {
            return "dec=" + n
                + " hex=" + n.toString(16)
                + " oct=" + n.toString(8)
                + " bin=" + n.toString(2);
        }
    }
}
```

**Qué reconocer:** `toRadixString` y `toString(radix)` son el mismo método `Number.prototype.toString`
de JavaScript con otro nombre: toda la familia web resuelve las cuatro bases con una sola llamada, y
ninguna necesita el rodeo del binario. La diferencia de fondo es el tipo: JavaScript convierte a
entero de 32 bits antes de cambiar de base, ActionScript declara `uint` explícitamente y Dart usa un
`int` de 64 bits —el mismo número, tres techos de desbordamiento distintos—.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos usan los mismos `Integer`/`Long` de la
biblioteca estándar, donde el cambio de base es un método estático.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toLong()
    println("dec=$n hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}")
}
```

### Scala

```scala
object Bases extends App {
  val n = scala.io.StdIn.readLine().trim.toLong
  println(s"dec=$n " +
    s"hex=${java.lang.Long.toHexString(n)} " +
    s"oct=${java.lang.Long.toOctalString(n)} " +
    s"bin=${java.lang.Long.toBinaryString(n)}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as long
println "dec=$n hex=${Long.toHexString(n)} oct=${Long.toOctalString(n)} bin=${Long.toBinaryString(n)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (parse-long (str/trim (read-line)))]
  (println (format "dec=%d hex=%x oct=%o bin=%s" n n n (Long/toBinaryString n))))
```

**Qué reconocer:** Scala, Groovy y Clojure llaman literalmente a `Long.toHexString` y compañía, los
mismos métodos que usa la implementación de Java en la clase: es la ventaja de compartir biblioteca
estándar. Kotlin es el único que añade azúcar propio —`n.toString(16)` como método de extensión— y
por eso parece Ruby sin dejar de ser JVM. Y todos arrastran la misma limitación: los enteros de la
JVM son **con signo**, así que un `Long` negativo se imprimiría en binario con sus 64 bits en
complemento a dos.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int64
printfn "dec=%d hex=%x oct=%o bin=%s" n n n (System.Convert.ToString(n, 2))
```

### VB.NET

```vbnet
Module Bases
    Sub Main()
        Dim n = Long.Parse(Console.ReadLine().Trim())

        ' Convert.ToString(valor, base) solo admite las bases 2, 8, 10 y 16.
        Dim hex = Convert.ToString(n, 16)
        Dim oct = Convert.ToString(n, 8)
        Dim bin = Convert.ToString(n, 2)

        Console.WriteLine($"dec={n} hex={hex} oct={oct} bin={bin}")
    End Sub
End Module
```

**Qué reconocer:** los dos usan el mismo `System.Convert.ToString(valor, base)` del CLR que ya
aparece en la versión de C#, y esa función tiene una restricción curiosa que conviene recordar:
**solo acepta las bases 2, 8, 10 y 16**, ni una más. F# demuestra además que sus especificadores de
formato son los de C —`%x`, `%o`— pero comprobados por el compilador: si el argumento no fuera
entero, el programa no compilaría, algo que `printf` de C jamás garantiza.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Enteros con tamaño y signo explícitos, y un
`printf` que no conoce el binario.

### C++

```cpp
#include <algorithm>
#include <bitset>
#include <iostream>
#include <string>

int main() {
    unsigned long n;
    std::cin >> n;

    std::string bin = std::bitset<64>(n).to_string();
    bin.erase(0, std::min(bin.find('1'), bin.size() - 1));

    std::cout << "dec=" << std::dec << n
              << " hex=" << std::hex << n
              << " oct=" << std::oct << n
              << " bin=" << bin << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        unsigned long n;
        if (scanf("%lu", &n) != 1) return 1;

        /* Igual que en C, el binario se construye a mano. */
        NSMutableString *bin = [NSMutableString string];
        unsigned long t = n;
        do {
            [bin insertString:((t & 1UL) ? @"1" : @"0") atIndex:0];
            t >>= 1;
        } while (t > 0);

        printf("dec=%lu hex=%lx oct=%lo bin=%s\n", n, n, n, bin.UTF8String);
    }
    return 0;
}
```

**Qué reconocer:** `unsigned long` es la declaración clave —la clase habla de **signo**, y elegir un
tipo sin signo es lo que permite desplazar bits sin sorpresas—. C++ cambia la base con manipuladores
de flujo (`std::hex`, `std::oct`) que son **pegajosos**: afectan a todo lo que se imprima después
hasta que se cambien, una trampa clásica. Y los dos confirman la ausencia heredada de C: el binario
se fabrica desplazando bits, con `std::bitset` o a mano.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí el tamaño y el
signo del entero son parte del nombre del tipo.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("dec={d} hex={x} oct={o} bin={b}\n", .{ n, n, n, n });
}
```

### Nim

```nim
import std/[strutils, strformat]

let n = stdin.readLine().strip().parseInt()
echo &"dec={n} hex={n:x} oct={n:o} bin={n:b}"
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!ulong;
    writefln("dec=%d hex=%x oct=%o bin=%b", n, n, n, n);
}
```

**Qué reconocer:** los tres sí tienen especificador binario —`{b}`, `:b`, `%b`— porque son lenguajes
diseñados después de que el binario dejara de ser exótico, igual que Rust escribe `{:b}`. Zig lleva
la explicitud al máximo: el tipo `u64` está escrito en la propia llamada a `parseInt`, así que el
lector sabe sin buscar cuántos bits hay y que no admite negativos. En un lenguaje de sistemas eso no
es un detalle: define exactamente en qué valor **desborda** el programa.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe el resultado, no el recorrido para
obtenerlo.

### Prolog

```prolog
:- initialization(main, main).

% ~Nr imprime en la base N: 16, 8 y 2 en minúscula (~NR sería en mayúscula).
main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    format("dec=~d hex=~16r oct=~8r bin=~2r~n", [N, N, N, N]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni aritmética de bases: la equivalencia debe declararse como hecho.
numero(255).
en_base(255, 16, "ff").
en_base(255, 8, "377").
en_base(255, 2, "11111111").

representacion(N, B, S) :- numero(N), en_base(N, B, S).
```

**Qué reconocer:** Prolog resuelve las tres bases con una sola directiva de formato, `~Nr`, donde el
número que precede a la `r` **es** la base —más general que cualquier `%x` de la familia C—. Datalog,
en cambio, muestra el límite honesto del paradigma: sin aritmética ni salida, lo único que puede
hacer es declarar la correspondencia como hechos y consultarla. Los enteros con tamaño, signo y
desbordamiento, que son el corazón de esta clase, sencillamente **no existen** aquí: el número es un
valor matemático abstracto, no un patrón de bits en la memoria. Es la misma abstracción que hace SQL
cuando te deja pedir un `INTEGER` sin decirte cuántos bytes ocupa.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una divisoria muy nítida: los que heredaron `printf` de C
saben escribir hexadecimal y octal pero no binario, y los diseñados después ya lo traen de fábrica.
Debajo, el mismo entero y la misma pregunta: cuántos bits y con qué signo. Eso es lo transferible.

⏮️ [Volver a la clase 044](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
