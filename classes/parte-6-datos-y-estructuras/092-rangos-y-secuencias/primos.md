# 🧬 El mismo programa en las familias de lenguajes — Clase 092

> [⬅️ Volver a la clase 092](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —generar el rango de enteros de `a` a `b` inclusive
y sumarlo— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` — dos enteros con `a <= b`
- **Salida** (stdout): `rango=<a-...-b> suma=<suma del rango>`
- **Regla:** el rango `[a..b]` es **inclusivo por ambos extremos**

| stdin | esperado |
|---|---|
| `2 5` | `rango=2-3-4-5 suma=14` |
| `1 1` | `rango=1 suma=1` |
| `3 6` | `rango=3-4-5-6 suma=18` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python tiene `range` perezoso y **exclusivo** por arriba; el resto de la familia se reparte entre
tener un operador de rango inclusivo y no tener rangos en absoluto.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
r = (a..b)  # Range es un objeto perezoso e inclusivo; (a...b) sería el exclusivo
puts "rango=#{r.to_a.join('-')} suma=#{r.sum}"
```

### Perl

```perl
my ($a, $b) = split ' ', <STDIN>;
my @r = ($a .. $b);  # el operador .. NO crea un rango: expande la lista completa
my $suma = 0;
$suma += $_ for @r;
print "rango=", join('-', @r), " suma=$suma\n";
```

### Lua

```lua
local a, b = io.read("n", "n")
local r, suma = {}, 0   -- Lua no tiene tipo rango: se materializa con el for numérico
for x = a, b do         -- el for numérico de Lua es inclusivo en ambos extremos
  r[#r + 1] = x         -- se crece por el final; el primer índice de r es 1
  suma = suma + x
end
print(string.format("rango=%s suma=%d", table.concat(r, "-"), suma))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
set r {}
set suma 0
for {set x $a} {$x <= $b} {incr x} {  ;# sin rangos: el bucle clásico de tres partes
    lappend r $x
    incr suma $x
}
puts "rango=[join $r -] suma=$suma"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
r <- v[1]:v[2]  # el operador `:` construye el VECTOR entero, no una vista perezosa
cat(sprintf("rango=%s suma=%d\n", paste(r, collapse = "-"), sum(r)))
```

**Qué reconocer:** los cinco producen la misma línea, pero solo dos tienen algo que merezca llamarse
rango. El `Range` de Ruby es un **objeto de primera clase**: se guarda en una variable, se pregunta
si contiene un valor y solo se expande con `to_a` — y su `..` es inclusivo, frente al `...` que deja
fuera el extremo. El `..` de Perl y el `:` de R **no** son perezosos: construyen la lista o el vector
completo en memoria en el acto, así que `1..10_000_000` en Perl reserva diez millones de elementos.
En R eso es coherente con todo lo demás, porque el vector es su unidad natural y `sum(r)` opera
sobre él entero sin bucle. Lua y Tcl no tienen rangos: el rango solo existe **dentro** del `for`, y
ahí se nota que Lua indexa desde 1 —`r[#r + 1]` empieza escribiendo en `r[1]`— igual que R, mientras
que las listas de Tcl arrancan en 0.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  // Dart no tiene literal de rango: se genera con Iterable.generate, que sí es perezoso.
  final r = Iterable<int>.generate(v[1] - v[0] + 1, (i) => v[0] + i);
  print('rango=${r.join("-")} suma=${r.reduce((x, y) => x + y)}');
}
```

### ActionScript 3

```actionscript
// AS3 no tiene rangos ni stdin: el bucle for construye el Array a mano.
package {
    public class Rango {
        public static function rango(a:int, b:int):String {
            var r:Array = [];
            var suma:int = 0;
            for (var x:int = a; x <= b; x++) {
                r.push(x);
                suma += x;
            }
            return "rango=" + r.join("-") + " suma=" + suma;
        }
    }
}
```

**Qué reconocer:** ninguno de los dos tiene sintaxis de rango, y tampoco la tiene JavaScript: por eso
el idioma más visto en la web es `Array.from({length: n}, (_, i) => a + i)`, que es exactamente lo
que hace `Iterable.generate` de Dart pero con menos nombre. La única diferencia real entre los dos
primos es la **pereza**: el `Iterable` de Dart no materializa nada hasta que alguien lo recorre, y de
hecho aquí se recorre dos veces (una para unir, otra para sumar) sin que exista jamás una lista de
`b - a + 1` elementos. El `Array` de AS3 sí ocupa memoria desde el primer `push`. La lección: cuando
un lenguaje no tiene rango, hay que preguntarse si el sustituto genera o almacena.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó hasta `IntStream.rangeClosed` en
tener algo parecido; sus primos lo llevan en la sintaxis.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    val r = a..b  // IntRange es un objeto de primera clase, inclusivo; a until b sería exclusivo
    println("rango=${r.joinToString("-")} suma=${r.sum()}")
}
```

### Scala

```scala
object Rango extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  val r = a to b  // Range perezoso e inclusivo; "a until b" excluye el extremo
  println(s"rango=${r.mkString("-")} suma=${r.sum}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def r = a..b  // IntRange implementa List: se comporta como una colección ya construida
println "rango=${r.join('-')} suma=${r.sum()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; range es una secuencia PEREZOSA y el límite superior es exclusivo: hay que usar (inc b).
(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))
      r     (range a (inc b))]
  (println (format "rango=%s suma=%d" (str/join "-" r) (reduce + r))))
```

**Qué reconocer:** los cuatro tienen rango, y aun así **tres de ellos son inclusivos y uno no**, que
es justo el error que se cuela al portar. `a..b` en Kotlin y Groovy, y `a to b` en Scala, incluyen
el extremo; Kotlin y Scala ofrecen además la variante exclusiva con otra palabra (`until`) para que
la elección sea visible. Clojure sigue la convención de Python: `(range a b)` deja fuera a `b`, y de
ahí el `(inc b)`. La otra diferencia es si el rango se **almacena**: el `Range` de Scala y la
secuencia de Clojure son perezosos —guardan inicio, fin y paso, no los elementos—, mientras que el
`IntRange` de Groovy implementa `java.util.List` y se comporta como una colección hecha, cómodo pero
más caro con rangos grandes.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
let r = [ a .. b ]  // el .. de F# es inclusivo; [ ] lo materializa, seq { } lo dejaría perezoso
printfn "rango=%s suma=%d" (r |> List.map string |> String.concat "-") (List.sum r)
```

### VB.NET

```vbnet
Imports System
Imports System.Linq

Module Rango
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        ' Enumerable.Range toma (inicio, CUÁNTOS), no (desde, hasta): la trampa de .NET.
        Dim r = Enumerable.Range(a, b - a + 1)
        Console.WriteLine($"rango={String.Join("-", r)} suma={r.Sum()}")
    End Sub
End Module
```

**Qué reconocer:** el CLR no tiene un tipo rango de enteros de propósito general —el `System.Range`
que aparece en C# 8 sirve para **cortar** colecciones (`arr[1..3]`), no para iterar—, así que lo
que se usa es `Enumerable.Range` de LINQ, perezoso y con la firma más traicionera de esta página:
su segundo argumento es la **cantidad** de elementos, no el límite. Escribir
`Enumerable.Range(2, 5)` da `2 3 4 5 6`, no `2 3 4 5`. F# se sale de la familia con un `..` propio
del lenguaje que sí es inclusivo y que además funciona con paso (`[ a .. 2 .. b ]`), y deja elegir
entre materializar (`[ ]`) o generar bajo demanda (`seq { }`).

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C el rango no es un dato: es la cabecera de un
`for`, y el `<=` frente al `<` es toda la semántica.

### C++

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    int a = 0, b = 0;
    std::cin >> a >> b;
    std::vector<int> r(static_cast<std::size_t>(b - a + 1));
    std::iota(r.begin(), r.end(), a);  // rellena a, a+1, ...: el rango se materializa

    std::cout << "rango=";
    for (std::size_t i = 0; i < r.size(); ++i) {
        if (i) std::cout << '-';
        std::cout << r[i];
    }
    std::cout << " suma=" << std::accumulate(r.begin(), r.end(), 0) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int a = 0, b = 0;
        scanf("%d %d", &a, &b);
        // NSRange existe, pero es un struct (location, length) de enteros SIN SIGNO,
        // sin iteración propia: solo describe un tramo, hay que recorrerlo a mano.
        NSRange rango = NSMakeRange((NSUInteger)a, (NSUInteger)(b - a + 1));
        NSMutableArray<NSString *> *partes = [NSMutableArray array];
        NSInteger suma = 0;
        for (NSUInteger x = rango.location; x < NSMaxRange(rango); x++) {
            [partes addObject:[NSString stringWithFormat:@"%lu", (unsigned long)x]];
            suma += (NSInteger)x;
        }
        printf("rango=%s suma=%ld\n",
               [[partes componentsJoinedByString:@"-"] UTF8String], (long)suma);
    }
    return 0;
}
```

**Qué reconocer:** ninguno de los dos tiene un rango que se pueda recorrer directamente, y los dos
lo materializan. C++ usa `std::iota`, que rellena un contenedor **ya dimensionado** —de nuevo la
distinción de tamaño de la clase 089: hay que calcular `b - a + 1` antes de reservar—; desde C++20
existe `std::views::iota(a, b + 1)`, perezoso, pero con el límite superior exclusivo. Objective-C
enseña un caso instructivo: `NSRange` **sí existe** y describe exactamente un tramo, pero como
`(location, length)` y con `NSUInteger` sin signo, así que no admite extremos negativos y no aporta
iteración — es un descriptor para cortar cadenas y arreglos, no una secuencia. Igual que
`Enumerable.Range` en .NET, guarda longitud, no límite.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Rust tiene rangos como
tipos (`a..b` y `a..=b`); Go no tiene ninguno.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [128]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, std.mem.trim(u8, linea, " \r"), " ");
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);

    const out = std.io.getStdOut().writer();
    var suma: i64 = 0;
    try out.writeAll("rango=");
    // El a..b de Zig solo existe como sintaxis de for/slice: no hay valor de tipo rango.
    var x = a;
    while (x <= b) : (x += 1) {
        if (x != a) try out.writeAll("-");
        try out.print("{d}", .{x});
        suma += x;
    }
    try out.print(" suma={d}\n", .{suma});
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

let campos = stdin.readLine().splitWhitespace().map(parseInt)
let r = toSeq(campos[0] .. campos[1])  # a..b es INCLUSIVO; a..<b sería el exclusivo
echo "rango=", r.join("-"), " suma=", r.sum
```

### D

```d
import std.stdio, std.array, std.conv, std.range, std.algorithm;

void main() {
    auto v = readln().split().map!(to!int).array;
    auto r = iota(v[0], v[1] + 1);  // iota es perezoso y EXCLUSIVO por arriba: de ahí el +1
    writefln("rango=%s suma=%d", r.map!(to!string).join("-"), r.sum);
}
```

**Qué reconocer:** las tres respuestas cubren todo el abanico. Nim tiene un **tipo** `Slice[int]`
detrás de `a..b`, inclusivo, con `a..<b` como versión exclusiva escrita de forma que la diferencia
salta a la vista — exactamente el par `..=` / `..` de Rust. D no lo pone en el lenguaje sino en la
biblioteca: `iota` es un *rango perezoso*, y "rango" en D no significa intervalo de enteros sino el
protocolo `empty`/`front`/`popFront` sobre el que se construye toda su biblioteca —el mismo papel
que los iteradores en Rust—. Zig es el más austero: `a..b` solo aparece como sintaxis dentro de un
`for` o de un *slice*, nunca como valor que se guarde en una variable, así que el rango se escribe
como el `while` de siempre. Y en el mismo bloque conviven las dos convenciones de extremo: Nim
inclusivo, `iota` de D exclusivo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Generar una secuencia es justamente lo que peor
le sienta al modelo declarativo: hay que decir *qué* es un rango, no cómo contarlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    numlist(A, B, R),  % numlist/3 es inclusivo por ambos extremos
    sum_list(R, Suma),
    atomic_list_concat(R, '-', Texto),
    format("rango=~w suma=~d~n", [Texto, Suma]).
```

### Datalog

```datalog
% Datalog puro no genera secuencias ni suma: sin recursión aritmética ni agregados
% solo puede DECIDIR pertenencia. Los números se declaran como hechos y la regla
% dice quién cae dentro del intervalo; la suma queda fuera de su alcance.
extremos(2, 5).
numero(2).
numero(3).
numero(4).
numero(5).

en_rango(X) :- numero(X), extremos(A, B), X >= A, X <= B.
```

**Qué reconocer:** Prolog resuelve el problema con `numlist/3`, inclusivo por ambos extremos, pero lo
interesante es que es una **relación**, no una función: `numlist(2, 5, R)` liga `R` a la lista y
también sirve para comprobar que una lista dada es ese rango. Datalog marca el límite del paradigma:
sin funciones recursivas ni agregados no puede **construir** la secuencia ni sumarla, solo declarar
qué números pertenecen al intervalo — para generar habría que salirse a un dialecto con aritmética
recursiva, y para sumar a una extensión de agregados. Es exactamente la razón por la que en SQL los
rangos se sacan de una tabla auxiliar de números o de una CTE recursiva: la secuencia no es un
concepto nativo de las relaciones.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta que cambia el resultado en silencio: **¿el
extremo superior entra o no?** Ruby, Kotlin, Scala, Nim y Prolog dicen que sí; Clojure, `iota` de D
y `std::views::iota` dicen que no; .NET ni siquiera pregunta el límite, pregunta la cantidad. La
segunda pregunta es si el rango se **guarda** o se **genera**. Reconocer ambas antes de escribir la
primera línea es lo transferible.

⏮️ [Volver a la clase 092](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
