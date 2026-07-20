# 🧬 El mismo programa en las familias de lenguajes — Clase 065

> [⬅️ Volver a la clase 065](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar los enteros de una lista recorriéndola
elemento a elemento— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste el `for x in nums` de Python, el `each` de Ruby o el `foreach` de D te resultarán
familiares aunque no los hayas visto nunca. Ese reconocimiento es exactamente lo que este curso
quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** `suma = Σ elementos`

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8` |
| `10 20 30` | `suma=60` |
| `5` | `suma=5` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
El bucle sobre la colección es el gesto central de la familia: no se indexa, se recorre. La
diferencia entre unos y otros es dónde vive el recorrido —en una palabra clave o en un método.

### Ruby

```ruby
suma = 0
STDIN.read.split.each { |x| suma += x.to_i }
puts "suma=#{suma}"
```

### Perl

```perl
my @nums = split ' ', <STDIN>;
my $suma = 0;
$suma += $_ foreach @nums;
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
foreach n [split $linea] {
    incr suma $n
}
puts "suma=$suma"
```

### R

```r
nums <- scan("stdin", what = integer(), quiet = TRUE)
cat(sprintf("suma=%d\n", sum(nums)))
```

**Qué reconocer:** Ruby no tiene una palabra clave `for` que se use de verdad: el recorrido es un
**método**, `each`, que recibe un bloque. Perl y Tcl sí traen `foreach` como palabra del lenguaje.
Lua no ofrece un `for-each` sobre listas de texto: ofrece algo más general, un **iterador**
(`gmatch`) que el `for` consume llamándolo hasta que devuelve `nil`. R rompe con toda la familia:
no escribe ningún bucle porque `sum` opera sobre el **vector completo** de una vez, y en R escribir
un bucle donde cabe una operación vectorizada se considera mal estilo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final nums = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  var suma = 0;
  for (final n in nums) {
    suma += n;
  }
  print('suma=$suma');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el recorrido.
package {
    public class Suma {
        public static function sumar(nums:Array):String {
            var suma:int = 0;
            for each (var n:int in nums) {
                suma += n;
            }
            return "suma=" + suma;
        }
    }
}
```

**Qué reconocer:** los dos separan el `for` clásico por índice del recorrido por valor, igual que
JavaScript separa `for` de `for...of`. ActionScript lo hace con dos palabras (`for each`) porque su
`for...in` ya estaba ocupado recorriendo **claves**, exactamente la misma trampa que arrastra
JavaScript. Dart escribe `for (final n in ...)` y, con `final`, deja claro que la variable del bucle
se crea nueva en cada vuelta y no se reasigna.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos comparten la interfaz `Iterable`, así que
el `for-each` de Java funciona sobre cualquier colección que los demás construyan.

### Kotlin

```kotlin
fun main() {
    val nums = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    var suma = 0
    for (n in nums) {
        suma += n
    }
    println("suma=$suma")
}
```

### Scala

```scala
object Suma extends App {
  val nums = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  var suma = 0
  for (n <- nums) suma += n
  println(s"suma=$suma")
}
```

### Groovy

```groovy
def nums = System.in.text.trim().split(/\s+/)*.toInteger()
def suma = 0
nums.each { suma += it }
println "suma=$suma"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [nums (map #(Integer/parseInt %) (str/split (str/trim (slurp *in*)) #"\s+"))]
  (println (str "suma=" (reduce + nums))))
```

**Qué reconocer:** Kotlin y Scala escriben el mismo bucle que Java con menos ceremonia (`in`, `<-`),
y Groovy vuelve al método-con-bloque de Ruby, `each`. Clojure hace algo distinto de fondo: no
recorre acumulando en una variable, **pliega** la colección con `reduce`, porque no tiene variables
que reasignar. Los cuatro consumen la misma `Iterable` de la JVM; lo que cambia es si el recorrido
lo dirige el lenguaje, la colección o una función.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El contrato de la plataforma es `IEnumerable`:
quien lo implemente se recorre con `foreach`.

### F\#

```fsharp
let nums =
    stdin.ReadLine().Split([| ' ' |], System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int

let mutable suma = 0

for n in nums do
    suma <- suma + n

printfn "suma=%d" suma
```

### VB.NET

```vbnet
Imports System

Module Suma
    Sub Main()
        Dim nums = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Dim suma As Integer = 0
        For Each s As String In nums
            suma += Integer.Parse(s)
        Next
        Console.WriteLine("suma=" & suma)
    End Sub
End Module
```

**Qué reconocer:** VB.NET escribe con dos palabras (`For Each ... Next`) lo que C# escribe con
`foreach`, pero compila a las mismas llamadas a `GetEnumerator` y `MoveNext`. F# admite el bucle
—`for n in nums do`— aunque obliga a marcar `mutable` la variable que se reasigna: el lenguaje te
hace pedir permiso para mutar. Un F# de verdad escribiría `nums |> Array.sum` y se ahorraría el
bucle entero.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). C no tiene `for-each`: el bucle es siempre índice y
puntero.

### C++

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> nums;
    for (int x; std::cin >> x; ) nums.push_back(x);

    long long suma = 0;
    for (int n : nums) suma += n;

    std::cout << "suma=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *entrada = [[NSString alloc]
            initWithData:[[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile]
                encoding:NSUTF8StringEncoding];
        NSCharacterSet *blancos = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        NSArray<NSString *> *partes =
            [[entrada stringByTrimmingCharactersInSet:blancos] componentsSeparatedByString:@" "];

        NSInteger suma = 0;
        for (NSString *p in partes) {
            suma += [p integerValue];
        }
        printf("suma=%ld\n", (long)suma);
    }
    return 0;
}
```

**Qué reconocer:** ambos añaden a C lo que C no tiene. C++ llama *range-based for* a `for (int n :
nums)` y por debajo pide `begin()` y `end()` al contenedor. Objective-C lo llama *fast enumeration*
y lo resuelve pidiendo bloques de objetos al array. La sintaxis es casi idéntica —cambia solo el
símbolo, `:` o `in`— pero el mecanismo es distinto: iteradores en C++, protocolo de objetos en
Objective-C.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Recorrer no debe costar
más que indexar: el bucle se compila a lo mismo que escribirías a mano.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [512]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");

    var suma: i64 = 0;
    while (it.next()) |tok| {
        suma += try std.fmt.parseInt(i64, tok, 10);
    }

    try std.io.getStdOut().writer().print("suma={d}\n", .{suma});
}
```

### Nim

```nim
import std/strutils

var suma = 0
for palabra in stdin.readLine().splitWhitespace():
  suma += parseInt(palabra)
echo "suma=", suma
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv;

void main() {
    auto nums = readln().split().map!(to!int);

    int suma = 0;
    foreach (n; nums) suma += n;

    writefln("suma=%d", suma);
}
```

**Qué reconocer:** Zig es el que se separa: su `for` recorre arrays, pero un **iterador** se consume
con `while (it.next()) |tok|`, la captura que desempaqueta el opcional hasta que llega el `null`.
Nim y D sí traen `for`/`foreach` sobre iteradores. En D hay un detalle importante: `map!` no
construye ningún array —devuelve un *range* perezoso— y el `foreach` va tirando de él elemento a
elemento, así que el programa nunca guarda la lista doblada en memoria.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay bucle: se describe la colección entera y
la operación que la resume.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Nums),
    sum_list(Nums, Suma),
    format("suma=~d~n", [Suma]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni bucles: la lista se declara como hechos indexados
% y el total se pide con un agregado (`sum`, disponible en motores como Soufflé).
elem(1, 3).
elem(2, 1).
elem(3, 4).

suma(S) :- S = sum V : { elem(_, V) }.
```

**Qué reconocer:** en Prolog el recorrido está escondido dentro de `maplist` y `sum_list`, y el
mecanismo real no es un bucle sino **backtracking**: el motor prueba, liga y reintenta. Datalog lleva
la renuncia al extremo —no puedes escribir "recorre esto", solo declarar hechos y reglas—, que es
exactamente lo que hace SQL cuando le pides `SUM(x)` sin decirle en qué orden leer las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la misma idea en todos: **la colección sabe recorrerse**, y el
programa solo dice qué hacer con cada elemento. Lo que cambia es quién dirige el recorrido —una
palabra clave, un método, un iterador con `next()` o un motor de inferencia— y si el lenguaje te
deja acumular en una variable o te obliga a plegar. Eso es lo transferible.

⏮️ [Volver a la clase 065](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
