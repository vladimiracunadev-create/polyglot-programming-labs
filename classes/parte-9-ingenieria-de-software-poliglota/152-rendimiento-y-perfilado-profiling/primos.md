# 🧬 El mismo programa en las familias de lenguajes — Clase 152

> [⬅️ Volver a la clase 152](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —sumar de 1 a *n* contando cuántas operaciones
cuesta, que es el perfilado reducido a su mínima expresión— resuelto por los **primos** de cada
familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (con `n >= 1`)
- **Salida** (stdout): `operaciones=<n> resultado=<1+...+n>`
- **Regla:** sumar 1..n contando cada suma, sin usar la fórmula cerrada

| stdin | esperado |
|---|---|
| `5` | `operaciones=5 resultado=15` |
| `1` | `operaciones=1 resultado=1` |
| `3` | `operaciones=3 resultado=6` |

El contador `operaciones` es un perfilador de juguete: cuenta trabajo, igual que un perfilador real
cuenta muestras o llamadas. La diferencia entre familias no está en el bucle —es el mismo en los
veinte— sino en **qué te deja medir el ecosistema** y en cuánto cuesta cada suma por debajo.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Bucles baratos de escribir y caros de ejecutar: cada suma pasa por un intérprete, y por eso esta
familia es la que más ha invertido en perfiladores.

### Ruby

```ruby
n = STDIN.gets.to_i
ops = 0
suma = 0
1.upto(n) do |i|
  suma += i
  ops += 1
end
puts "operaciones=#{ops} resultado=#{suma}"
```

### Perl

```perl
use strict;
use warnings;

chomp(my $n = <STDIN>);
my ($ops, $suma) = (0, 0);
for my $i (1 .. $n) {
    $suma += $i;
    $ops++;
}
printf "operaciones=%d resultado=%d\n", $ops, $suma;
```

### Lua

```lua
local n = tonumber(io.read("l"))
local ops, suma = 0, 0
for i = 1, n do
  suma = suma + i
  ops = ops + 1
end
print(string.format("operaciones=%d resultado=%d", ops, suma))
```

### Tcl

```tcl
gets stdin n
set ops 0
set suma 0
for {set i 1} {$i <= $n} {incr i} {
    incr suma $i
    incr ops
}
puts "operaciones=$ops resultado=$suma"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
ops <- 0L
suma <- 0L
for (i in seq_len(n)) {
  suma <- suma + i
  ops <- ops + 1L
}
cat(sprintf("operaciones=%d resultado=%d\n", ops, suma))
```

**Qué reconocer:** el bucle es idéntico al de Python, y la herramienta para medirlo también existe en
cada uno: `ruby-prof` y `stackprof` en Ruby —el primero instrumenta cada llamada, el segundo muestrea
y por eso apenas distorsiona el tiempo—, `Devel::NYTProf` en Perl, que sigue siendo uno de los
perfiladores más detallados que existen en cualquier lenguaje, `LuaProfiler` con los *hooks* de depuración de Lua, y `Rprof` en R. Tcl paga aquí su decisión de fondo: como todo valor es una cadena, `incr` tiene que convertir a entero y volver, y esa conversión es exactamente lo que un perfilador te
señalaría. R hace lo contrario de lo idiomático en su comunidad: el bucle explícito es su operación
más lenta, y el R real escribiría `sum(seq_len(n))` vectorizado, que baja a C y no cuenta nada.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var ops = 0;
  var suma = 0;
  for (var i = 1; i <= n; i++) {
    suma += i;
    ops++;
  }
  print('operaciones=$ops resultado=$suma');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: n llega como parámetro.
package {
    public class Perfil {
        public static function medir(n:int):String {
            var ops:int = 0;
            var suma:int = 0;
            for (var i:int = 1; i <= n; i++) {
                suma += i;
                ops++;
            }
            return "operaciones=" + ops + " resultado=" + suma;
        }
    }
}
```

**Qué reconocer:** el bucle `for (var i = 1; i <= n; i++)` es literalmente el mismo de JavaScript,
porque los tres descienden de ECMAScript. Lo interesante es el perfilado: Dart tiene el
*Observatory* / DevTools con muestreo de CPU integrado en la VM, y ActionScript tenía el *Flash
Builder Profiler*. En ambos casos, igual que en JavaScript, el perfilador vive **dentro de la máquina
virtual**, no fuera —de ahí que en esta familia se hable de perfilar en el navegador y no de lanzar
un `perf` desde el sistema operativo—.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La plataforma con mejores herramientas de
medición de todo el mapa, y también la que más difícil hace interpretar una medición.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    var ops = 0
    var suma = 0
    for (i in 1..n) {
        suma += i
        ops++
    }
    println("operaciones=$ops resultado=$suma")
}
```

### Scala

```scala
object Perfil {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    var ops = 0
    var suma = 0
    for (i <- 1 to n) {
      suma += i
      ops += 1
    }
    println(s"operaciones=$ops resultado=$suma")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def ops = 0
def suma = 0
(1..n).each { i ->
    suma += i
    ops++
}
println "operaciones=$ops resultado=$suma"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (parse-long (str/trim (read-line)))
      [ops suma] (reduce (fn [[o s] i] [(inc o) (+ s i)])
                         [0 0]
                         (range 1 (inc n)))]
  (println (str "operaciones=" ops " resultado=" suma)))
```

**Qué reconocer:** los cuatro corren sobre el mismo JIT, y por eso comparten herramientas: **JFR**
(Java Flight Recorder), integrado en la JVM y con un coste de menos del 1 %, y **async-profiler**,
que evita el *safepoint bias* que falsea los perfiladores clásicos de la plataforma. Comparten
también la trampa: el JIT necesita miles de iteraciones para compilar el bucle, así que **la primera
medición siempre miente** —de ahí que en la JVM se mida con JMH y fases de calentamiento—. Scala
escribe `for (i <- 1 to n)`, que no es un bucle sino azúcar sobre `foreach` con una función; Groovy
hace lo mismo con `.each`. Clojure va más lejos y sustituye las variables mutables por un `reduce`
que arrastra el par `[ops suma]` como acumulador: sin mutación, y por eso la asignación de memoria
—no el bucle— es lo que aparecería en su perfil.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = int (stdin.ReadLine().Trim())
let ops, suma = Seq.fold (fun (o, s) i -> (o + 1, s + i)) (0, 0) (seq { 1 .. n })
printfn "operaciones=%d resultado=%d" ops suma
```

### VB.NET

```vbnet
Module Perfil
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim ops = 0
        Dim suma = 0
        For i = 1 To n
            suma += i
            ops += 1
        Next
        Console.WriteLine($"operaciones={ops} resultado={suma}")
    End Sub
End Module
```

**Qué reconocer:** el CLR es primo hermano de la JVM también en esto: `dotnet-trace`, `dotnet-counters`
y BenchmarkDotNet ocupan el mismo hueco que JFR y JMH, y sufren el mismo problema de calentamiento
del JIT. F# elige `Seq.fold` en vez de mutar dos variables, igual que Clojure elige `reduce`; el
precio es que `seq { 1 .. n }` es perezosa y cada elemento pasa por un enumerador, un coste que el
`For i = 1 To n` de VB.NET no paga porque compila a un salto. Es la comparación más limpia de la
página: **la misma plataforma, el mismo resultado, y dos perfiles de ejecución muy distintos**.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí no hay máquina virtual entre tu bucle y el
procesador, y eso cambia el tipo de herramienta que se usa.

### C++

```cpp
#include <iostream>

int main() {
    long long n = 0;
    std::cin >> n;
    long long ops = 0, suma = 0;
    for (long long i = 1; i <= n; ++i) {
        suma += i;
        ++ops;
    }
    std::cout << "operaciones=" << ops << " resultado=" << suma << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long n = 0;
        if (scanf("%lld", &n) != 1) { return 1; }
        long long ops = 0, suma = 0;
        for (long long i = 1; i <= n; i++) {
            suma += i;
            ops++;
        }
        printf("operaciones=%lld resultado=%lld\n", ops, suma);
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C y el bucle compila al mismo puñado de instrucciones.
Lo distinto es cómo se mide: aquí se usa `perf` de Linux, que lee los contadores del propio
procesador (ciclos, fallos de caché, predicciones de salto fallidas), y `valgrind --tool=callgrind`,
que simula la ejecución instrucción a instrucción y por eso es cien veces más lento pero exacto. En
Objective-C el perfilador natural es Instruments de Apple, que además vigila el `@autoreleasepool` y
las retenciones de objetos. Y una advertencia que solo aplica a esta familia: con optimizaciones
activadas el compilador puede reconocer la suma de Gauss y **borrar el bucle entero**, así que un
microbenchmark ingenuo mide cero.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Binario nativo, sin GC
en el camino crítico o con uno muy acotado, y perfilado como parte del ecosistema.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);

    var ops: i64 = 0;
    var suma: i64 = 0;
    var i: i64 = 1;
    while (i <= n) : (i += 1) {
        suma += i;
        ops += 1;
    }
    try std.io.getStdOut().writer().print("operaciones={d} resultado={d}\n", .{ ops, suma });
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var ops, suma = 0
for i in 1 .. n:
  suma += i
  inc ops
echo "operaciones=", ops, " resultado=", suma
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const n = readln().strip().to!long;
    long ops = 0, suma = 0;
    foreach (i; 1 .. n + 1) {
        suma += i;
        ops++;
    }
    writefln("operaciones=%d resultado=%d", ops, suma);
}
```

**Qué reconocer:** los tres compilan a nativo, así que heredan las herramientas de C —`perf`,
`valgrind`, `flamegraph`— sin necesitar un perfilador propio; eso es justamente lo que significa
"lenguaje de sistemas" en la práctica. Zig escribe el bucle como `while (i <= n) : (i += 1)`, con el
incremento separado en su propia cláusula: más verboso, pero deja explícito el punto donde se paga
la iteración. Nim y D compilan a través de C (o de LLVM) y por eso el binario final se perfila igual
que uno escrito en C, aunque el fuente se lea como Python. En los tres, además, `-O2` puede borrar
el bucle igual que en C++: la diferencia entre lo que escribes y lo que se ejecuta es máxima en
esta familia y en la anterior.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere; el coste lo decide
el motor, y por eso aquí "perfilar" significa leer un plan de ejecución.

### Prolog

```prolog
:- initialization(main, main).

acumular(I, N, Ops, Suma, Ops, Suma) :- I > N, !.
acumular(I, N, Ops0, Suma0, Ops, Suma) :-
    I =< N,
    Ops1 is Ops0 + 1,
    Suma1 is Suma0 + I,
    I1 is I + 1,
    acumular(I1, N, Ops1, Suma1, Ops, Suma).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    acumular(1, N, 0, 0, Ops, Suma),
    format("operaciones=~d resultado=~d~n", [Ops, Suma]).
```

### Datalog

```datalog
% Datalog no tiene bucles ni variables mutables: la recursión genera los pasos y los agregados
% (una extensión, presente por ejemplo en Soufflé) hacen de contador y de acumulador.
entrada(5).

paso(1).
paso(I) :- paso(J), entrada(N), J < N, I = J + 1.

resultado(Ops, Suma) :- Ops = count : { paso(_) }, Suma = sum X : { paso(X) }.
```

**Qué reconocer:** Prolog **no tiene bucle**, así que el acumulador viaja como argumento extra en una
recursión —el patrón se llama acumulador y aparece en toda la familia funcional-lógica—. Los dos
argumentos de salida `Ops` y `Suma` solo se ligan cuando la recursión toca fondo. Ese `!` de la
primera cláusula es el *corte*, y es el equivalente prologuiano de una decisión de rendimiento:
impide que el motor guarde puntos de retroceso, que es exactamente lo que mediría un perfilador de
Prolog. Datalog renuncia incluso a controlar el orden de evaluación: declaras los pasos y el motor
decide cómo derivarlos, igual que el planificador de SQL decide si usa un índice. Por eso, en esta
familia, la herramienta de perfilado no es un muestreador sino `EXPLAIN`.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo bucle, y el mismo `operaciones=n`. Lo que cambia es **quién sabe lo que
cuesta**: en los dinámicos el intérprete, y se mide con `stackprof`, `Devel::NYTProf` o `Rprof`; en
la JVM y el CLR el JIT, y se mide con JFR, async-profiler o BenchmarkDotNet, siempre después de
calentar; en los nativos el procesador, y se mide con `perf` o `valgrind`; y en los declarativos el
planificador, que solo te habla a través de `EXPLAIN`. Elegir la herramienta correcta empieza por
saber en cuál de esos cuatro mundos estás. Eso es lo transferible.

⏮️ [Volver a la clase 152](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
