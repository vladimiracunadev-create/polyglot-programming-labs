# 🧬 El mismo programa en las familias de lenguajes — Clase 124

> [⬅️ Volver a la clase 124](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar los dígitos de un entero— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

El problema es deliberadamente pequeño, y por eso sirve: veinte programas que hacen lo mismo dejan
al descubierto lo único que de verdad los diferencia aquí, que es **cómo llega cada uno a
ejecutarse**. Compilar antes, interpretar sobre la marcha, o interpretar y compilar en caliente lo
que se repite.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (`n >= 0`)
- **Salida** (stdout): `digitos=<cantidad de dígitos>`
- **Regla:** contar los dígitos de `n` (el `0` tiene uno)

| stdin | esperado |
|---|---|
| `12345` | `digitos=5` |
| `7` | `digitos=1` |
| `100` | `digitos=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia que arrastra el mote de "interpretada" y que hace décadas dejó de serlo del todo: casi
todos compilan a una forma interna antes de dar el primer paso.

### Ruby

```ruby
n = STDIN.gets.strip.to_i
puts "digitos=#{n.to_s.size}"

# Ruby no interpreta el fuente: lo compila a instrucciones de su VM (YARV).
#   RUBYOPT=--dump=insns ruby main.rb
```

### Perl

```perl
my $n = 0 + <STDIN>;
printf "digitos=%d\n", length $n;

# Perl compila el fuente a un árbol de ops y luego lo recorre; no hay bytecode plano.
#   perl -MO=Concise main.pl
```

### Lua

```lua
local n = math.tointeger(tonumber(io.read("l")))
local d, m = 1, n
while m >= 10 do
  m = m // 10
  d = d + 1
end
print("digitos=" .. d)

-- Con LuaJIT, este bucle se vuelve "caliente" y se compila a máquina en ejecución:
--   luajit -jv main.lua   (muestra las trazas compiladas)
```

### Tcl

```tcl
gets stdin linea
set n [expr {int($linea)}]
puts "digitos=[string length $n]"

# Desde Tcl 8.0 todo script se compila a bytecode antes de ejecutarse.
#   puts [::tcl::unsupported::disassemble script {string length 100}]
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("digitos=%d\n", nchar(as.character(n))))

# R interpreta el AST, salvo que se active su compilador de bytecode:
#   f <- compiler::cmpfun(function(n) nchar(as.character(n)))
#   compiler::disassemble(f)
```

**Qué reconocer:** los cinco parten de texto y ninguno lo interpreta letra a letra, pero llegan a
formas internas distintas. Ruby compila a **bytecode plano** para su máquina virtual YARV, igual que
CPython a sus instrucciones. Perl no: construye un **árbol de operaciones** y lo recorre saltando de
nodo en nodo, un diseño de los años ochenta que explica por qué no existe un `.pyc` equivalente en
Perl. Tcl compila a bytecode propio desde la versión 8.0 —el gran cambio que lo sacó de la fama de
lento—. R es el único con el compilador **opcional**: interpreta el árbol por omisión y solo emite
bytecode si se lo pides con `compiler::cmpfun` o si la función se llama lo bastante. Y Lua es el
caso doble: el intérprete de referencia compila a bytecode y para ahí, mientras **LuaJIT** detecta
bucles calientes como el de arriba y los compila a código máquina sin dejar de ser Lua.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia donde el JIT se volvió norma, porque el fuente llega por la red y no hay tiempo de
compilarlo todo antes.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('digitos=${n.toString().length}');
}

// El mismo fuente admite los dos modos:
//   dart run main.dart        -> JIT, arranque rápido, recarga en caliente
//   dart compile exe main.dart -> AOT, binario nativo sin calentamiento
```

### ActionScript 3

```actionscript
// AVM2 no expone stdin: la entrada llega como argumento.
// El .swf ya contiene bytecode ABC; el reproductor lo interpreta y compila los métodos calientes.
package {
    public class Digitos {
        public static function contar(n:int):String {
            return "digitos=" + n.toString().length;
        }
    }
}
```

**Qué reconocer:** Dart es el ejemplo más limpio del programa entero de que **compilador y JIT no
son propiedades del lenguaje sino del modo de ejecución**: un mismo archivo, dos tuberías, elegidas
por línea de comandos —JIT en desarrollo porque permite recarga en caliente, AOT al publicar porque
elimina el calentamiento—. ActionScript llegó antes a la misma idea: el `.swf` viaja como bytecode
ABC ya compilado, y la AVM2 lo interpreta al principio y compila a máquina los métodos que se
repiten, que es exactamente lo que hoy hace V8 con JavaScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Compilación estática a bytecode y JIT en
ejecución: la combinación que popularizó esta plataforma.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toLong()
    println("digitos=${n.toString().length}")
}
```

### Scala

```scala
object Digitos {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toLong
    println(s"digitos=${n.toString.length}")
  }
}
```

### Groovy

```groovy
// Sin @CompileStatic, cada llamada se resuelve en ejecución por el runtime dinámico de Groovy.
def n = System.in.newReader().readLine().trim().toLong()
println "digitos=${n.toString().length()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure compila cada forma a bytecode mientras carga el archivo: no hay intérprete.
(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "digitos=" (count (str n)))))
```

**Qué reconocer:** los cuatro acaban en el mismo HotSpot, que arranca **interpretando** el bytecode
y va promocionando los métodos calientes con su JIT **por niveles** —C1 primero, rápido y poco
optimizador; C2 después, lento de compilar y agresivo—. Lo que cambia es la fase anterior. Kotlin y
Scala compilan por completo antes de ejecutar. Clojure compila **en tiempo de carga**, lo que
explica su arranque lento y por qué un REPL de Clojure genera clases sobre la marcha. Groovy es el
que mejor muestra el contraste dentro de una misma sintaxis: tal como está arriba, la llamada a
`toLong()` se resuelve en ejecución por su despachador dinámico; con `@CompileStatic` la resuelve el
compilador y el bytecode resultante es prácticamente el de Java. Se comprueba con
`java -XX:+PrintCompilation` para ver qué promociona el JIT.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR nunca ejecuta CIL directamente: lo compila
método a método, la primera vez que se llama.

### F\#

```fsharp
let n = int64 ((stdin.ReadLine()).Trim())
printfn "digitos=%d" (string n).Length
```

### VB.NET

```vbnet
Imports System

Module Digitos
    Sub Main()
        Dim n = Long.Parse(Console.ReadLine().Trim())
        Console.WriteLine("digitos=" & n.ToString().Length)
    End Sub
End Module
```

**Qué reconocer:** el modelo de .NET no tiene intérprete en el camino normal: RyuJIT compila cada
método a código máquina **la primera vez que se ejecuta**, y a partir de ahí se llama al nativo. Eso
lo hace distinto de la JVM, que sí interpreta al principio. .NET compensa el coste del arranque con
dos piezas opcionales que ninguno de estos dos lenguajes decide por su cuenta —son del runtime—:
**ReadyToRun**, que precompila el CIL y deja el JIT solo para lo que valga la pena reoptimizar, y
**OSR** (*on-stack replacement*), que permite recompilar un bucle largo sin esperar a que termine.
Ni F# ni VB.NET pueden observar su CIL desde el propio programa; se saca con `ildasm` sobre el
ensamblado.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde no hay nada que compilar en
ejecución porque ya está todo compilado.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    long long n = 0;
    std::cin >> n;
    std::cout << "digitos=" << std::to_string(n).size() << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long n = 0;
        scanf("%lld", &n);
        NSString *s = [NSString stringWithFormat:@"%lld", n];
        printf("digitos=%lu\n", (unsigned long)[s length]);
    }
    return 0;
}
```

**Qué reconocer:** aquí **no hay fase de ejecución que observar**: el binario entra en memoria y
salta a `main`, sin intérprete ni compilador presentes. La única decisión de optimización se tomó
antes, en `-O2` o `-O3`. Objective-C introduce, aun así, una grieta interesante: sus envíos de
mensaje (`[s length]`) se resuelven **en ejecución** por `objc_msgSend`, con una caché de métodos
por clase. No es un JIT —no se genera código nuevo—, pero sí es despacho tardío dentro de un
programa totalmente compilado, la misma tensión que Groovy resuelve con `@CompileStatic`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilación completa
antes de ejecutar, sin runtime que reoptimice.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r"), 10);
    var d: usize = 1;
    var m = n;
    while (m >= 10) : (m /= 10) d += 1;
    try std.io.getStdOut().writer().print("digitos={d}\n", .{d});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
echo "digitos=", len($n)

# Nim no compila directo a máquina: emite C y llama al compilador de C.
#   nim c --nimcache:salida main.nim   (deja los .c generados a la vista)
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    writeln("digitos=", n.to!string.length);
}
```

**Qué reconocer:** los tres son compiladores puros, pero solo Zig y D lo son de una pieza. **Nim
genera C** y deja que `gcc` haga el trabajo final: por eso hereda las optimizaciones de un
compilador de C maduro sin escribirlas, y por eso compilar Nim es lento. D nació con la misma
tentación —su antecesor conceptual, y todavía hoy `ldc` y `gdc` lo llevan a LLVM y GCC—, pero `dmd`
va del fuente al objeto sin pasar por C. Zig, además de compilar, **ejecuta parte del programa
durante la compilación** con `comptime`: código que corre en el compilador y desaparece del binario,
una tercera categoría que no es ni interpretación ni JIT.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Donde "compilar" significa elegir un plan, y ese
plan se elige en ejecución con las estadísticas a la vista.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    number_codes(N, Codigos),
    length(Codigos, D),
    format("digitos=~d~n", [D]).
```

### Datalog

```datalog
% Datalog no lee de stdin ni itera con aritmética: la entrada es un hecho y los tramos, reglas.
entrada(12345).

digitos(1) :- entrada(N), N < 10.
digitos(2) :- entrada(N), N >= 10, N < 100.
digitos(3) :- entrada(N), N >= 100, N < 1000.
digitos(4) :- entrada(N), N >= 1000, N < 10000.
digitos(5) :- entrada(N), N >= 10000, N < 100000.
```

**Qué reconocer:** Prolog compila de verdad —cada cláusula se traduce a instrucciones de la **WAM**,
una máquina virtual con su propio conjunto de operaciones, inspeccionable con `vm_list(main/0)`—,
así que es tan "compilado a bytecode" como Java. Datalog, en cambio, no tiene un modelo de ejecución
que el programa pueda influir: el motor decide la estrategia (evaluación semi-ingenua, orden de las
juntas) y el autor de las reglas no ve nada de eso. Es la misma renuncia de SQL, y también el mismo
premio: el motor puede cambiar de plan sin que el código cambie una coma, algo que ningún JIT de
esta página puede ofrecer al nivel del algoritmo.

---

## Y de vuelta a la clase

Veinte lenguajes contando dígitos, y ni uno solo que sea "interpretado" en el sentido ingenuo de la
palabra. Lo que varía es **cuánto trabajo se hace antes de ejecutar y cuánto se guarda para cuando
ya se sabe qué es lo caliente**. Compilador, intérprete y JIT no son tres cajas: son tres momentos
del mismo continuo.

⏮️ [Volver a la clase 124](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
