# 🧬 El mismo programa en las familias de lenguajes — Clase 126

> [⬅️ Volver a la clase 126](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —calcular `2` elevado a `n`— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

El cálculo es trivial a propósito. Cuando el trabajo útil dura microsegundos, lo único que se mide
de verdad es **el coste de llegar a ejecutarlo**: compilar antes y arrancar en frío, o arrancar
enseguida y compilar por el camino.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (`0 <= n <= 60`)
- **Salida** (stdout): `resultado=<2^n>`
- **Regla:** `2` elevado a `n`

| stdin | esperado |
|---|---|
| `3` | `resultado=8` |
| `0` | `resultado=1` |
| `5` | `resultado=32` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno compila a nativo por omisión, y todos pagan el arranque de su runtime en cada ejecución.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "resultado=#{2**n}"

# Ruby no tiene modo AOT: compila a bytecode YARV en cada arranque.
# Lo más parecido es cachearlo:  RUBYOPT="--yjit" ruby main.rb  (YJIT compila en caliente)
```

### Perl

```perl
my $n = 0 + <STDIN>;
printf "resultado=%d\n", 1 << $n;   # entero de 64 bits: exacto hasta n = 62

# Perl no tiene JIT ni AOT: reconstruye su árbol de ops en cada ejecución.
```

### Lua

```lua
local n = math.tointeger(tonumber(io.read("l")))
print("resultado=" .. (1 << n))   -- desplazamiento entero (Lua 5.3+)

-- Lua sí permite guardar el bytecode y saltarse la compilación al arrancar:
--   luac -o main.luac main.lua && lua main.luac
-- Y LuaJIT compila a máquina en ejecución, no antes.
```

### Tcl

```tcl
gets stdin n
puts "resultado=[expr {2 ** $n}]"

# Tcl compila a bytecode al ejecutar, nunca antes; no hay formato distribuible.
# Los enteros son de precisión arbitraria, así que 2**60 es exacto.
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("resultado=%.0f\n", 2^n))   # doble IEEE: las potencias de 2 son exactas
```

**Qué reconocer:** para un programa de una línea, **el tiempo se lo lleva el arranque**, no el
cálculo, y ahí los cinco pierden por goleada frente a cualquier binario nativo. Lua es el único que
ofrece una salida parcial: `luac` guarda el bytecode ya compilado y el arranque se salta esa fase
—no es AOT a código máquina, pero elimina un trozo del coste—. LuaJIT va en la dirección opuesta,
compila a nativo **durante** la ejecución, lo que no ayuda nada aquí y lo cambia todo en un bucle de
millones de vueltas. Ruby con YJIT está en el mismo caso. Tcl y R no tienen ni una cosa ni la otra.
Y fíjate en el detalle de tipos que la AOT vuelve visible: Tcl y Ruby dan `2^60` exacto porque sus
enteros crecen, R llega al resultado correcto solo porque las potencias de dos son exactas en coma
flotante.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('resultado=${1 << n}');
}

// El mismo archivo, las dos estrategias:
//   dart run main.dart          -> JIT: arranca en ~ms, recarga en caliente, ideal en desarrollo
//   dart compile exe main.dart  -> AOT: binario nativo, arranque instantáneo, sin recarga
```

### ActionScript 3

```actionscript
// AVM2 no tiene stdin ni enteros de 64 bits: int es de 32.
// Number (doble IEEE) sí representa 2^60 exactamente, por ser potencia de dos.
package {
    public class Potencia {
        public static function calcular(n:int):String {
            return "resultado=" + Math.pow(2, n).toFixed(0);
        }
    }
}
```

**Qué reconocer:** Dart es el mejor caso del programa entero para esta clase porque el **mismo
fuente** se ejecuta de las dos maneras y la elección es de despliegue, no de lenguaje: JIT mientras
programas —porque el arranque rápido y la recarga en caliente valen más que la velocidad de
régimen—, AOT al publicar en móvil, donde un tiempo de arranque de cientos de milisegundos se nota.
ActionScript no dio nunca esa opción: el `.swf` viaja como bytecode y la máquina decide sola qué
compilar. La misma disyuntiva reaparece hoy en JavaScript con las *snapshots* de V8, que precocinan
el estado inicial para no volver a analizar el fuente en cada arranque.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La plataforma que hizo del JIT una ventaja, y
que lleva una década añadiéndole opciones de AOT.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    println("resultado=${1L shl n}")
}
```

### Scala

```scala
object Potencia {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"resultado=${1L << n}")
  }
}
```

### Groovy

```groovy
@groovy.transform.CompileStatic
class Potencia {
    static void main(String[] args) {
        int n = System.in.newReader().readLine().trim() as int
        println "resultado=${1L << n}"
    }
}
```

### Clojure

```clojure
;; Clojure compila cada forma al cargarla: su arranque es el más lento de los cuatro.
(let [n (Long/parseLong (.trim (read-line)))]
  (println (str "resultado=" (bit-shift-left 1 n))))
```

**Qué reconocer:** los cuatro arrancan interpretando bytecode y solo compilan a nativo lo que se
repite, así que en un programa como este **el JIT no llega a intervenir**: se paga el arranque de la
JVM entero y no se cobra ninguna de sus ventajas. De ahí las respuestas AOT de la plataforma —CDS
para precargar clases, y GraalVM Native Image, que produce un binario con arranque de milisegundos a
cambio de perder la reoptimización en caliente y de exigir declarar de antemano toda la reflexión—.
Los cuatro no salen igual de mal parados: Clojure es el peor porque **compila mientras carga**, y
Groovy sin `@CompileStatic` añade el coste de resolver cada llamada en ejecución, que la anotación
de arriba adelanta a la compilación.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR ha ido moviendo la frontera: primero todo
JIT, hoy tres opciones convivientes.

### F\#

```fsharp
let n = int ((stdin.ReadLine()).Trim())
printfn "resultado=%d" (1L <<< n)
```

### VB.NET

```vbnet
Imports System

Module Potencia
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim r As Long = 1L << n
        Console.WriteLine("resultado=" & r)
    End Sub
End Module
```

**Qué reconocer:** aquí la decisión AOT/JIT no la toma el lenguaje sino el `.csproj` o `.fsproj`, y
es la misma para F# y para VB.NET porque ambos producen CIL. Por omisión, RyuJIT compila cada método
en su primera llamada: coste pequeño pero real, multiplicado por cada método del arranque.
**ReadyToRun** precompila ese CIL a nativo dentro del ensamblado y deja el JIT solo para lo que valga
la pena reoptimizar más tarde, así que es un híbrido. **NativeAOT** va hasta el final —binario
autocontenido, sin JIT, arranque instantáneo— a cambio de perder la reflexión no anotada y la
generación de código en ejecución. Es exactamente el mismo intercambio que GraalVM ofrece en la JVM,
y ninguna de las dos opciones cambia una sola línea del código de arriba.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). AOT puro: aquí no hay nada que decidir.

### C++

```cpp
#include <iostream>

int main() {
    int n = 0;
    std::cin >> n;
    std::cout << "resultado=" << (1LL << n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);
        printf("resultado=%lld\n", 1LL << n);
    }
    return 0;
}
```

**Qué reconocer:** los dos pagan todo el coste **antes**, en el compilador, y en ejecución no queda
ni una decisión pendiente: el arranque es cargar el binario y saltar a `main`. El precio de esa
elección es la falta de información —el compilador optimiza sin saber qué ramas se tomarán de
verdad—, y por eso la familia inventó su propio sustituto del JIT: **PGO**, la optimización guiada
por perfil, que ejecuta el programa una vez para recoger datos y recompila con ellos
(`g++ -fprofile-generate` y luego `-fprofile-use`). Es la misma información que un JIT obtiene
gratis en caliente, solo que recolectada a mano y aplicada antes.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). AOT por diseño, con
distintas cantidades de runtime en el binario.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u6, std.mem.trim(u8, linea, " \r"), 10);
    const r: u64 = @as(u64, 1) << n;
    try std.io.getStdOut().writer().print("resultado={d}\n", .{r});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
echo "resultado=", 1'i64 shl n

# Nim compila a C y luego invoca gcc: AOT en dos etapas.
#   nim c -d:release main.nim
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!int;
    writeln("resultado=", 1L << n);
}
```

**Qué reconocer:** los tres producen un binario sin JIT, pero llegan por caminos que cuestan
distinto **en tiempo de compilación**, que es donde esta familia paga. **Nim transpila a C** y
después llama a `gcc`: hereda gratis las optimizaciones de un compilador maduro, a cambio del doble
de tiempo de construcción. D reparte la misma idea en tres compiladores —`dmd` es rapidísimo
compilando y flojo optimizando, `ldc` va por LLVM y `gdc` por GCC— y elegir uno es elegir dónde
gastar. Zig lleva la asimetría al extremo con `comptime`: **ejecuta parte del programa dentro del
compilador**, así que trabajo que un JIT haría en caliente aquí desaparece del binario por completo.
En los tres, el arranque en ejecución es prácticamente cero, que es justo lo que este problema
premia.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia donde el equivalente al JIT es la
recompilación del plan, y llega con décadas de ventaja.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    R is 2^N,                        % enteros de precisión arbitraria
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni aritmética recursiva sobre un dominio infinito:
% no hay forma de derivar 2^n para un n cualquiera. Se tabula el dominio útil.
entrada(3).

pot(0, 1).
pot(1, 2).
pot(2, 4).
pot(3, 8).
pot(4, 16).
pot(5, 32).

resultado(R) :- entrada(N), pot(N, R).
```

**Qué reconocer:** Prolog es AOT en un sentido que sorprende: `swipl -o app -c main.pl` produce un
ejecutable con la imagen del programa ya compilada a instrucciones WAM, así que el arranque se salta
la carga de las cláusulas. Datalog no puede ni plantear el problema —sin recursión aritmética sobre
un dominio abierto, `2^n` genérico no es derivable—, y su respuesta a la pregunta de esta clase es
otra: el motor **elige el plan en ejecución**, con las estadísticas de los datos delante, y puede
cambiarlo cuando esas estadísticas cambien. Eso es un JIT a nivel de algoritmo, no de instrucción, y
es exactamente lo que hace el planificador de SQL cuando invalida un plan cacheado.

---

## Y de vuelta a la clase

Veinte programas que hacen la misma multiplicación y tardan cuatro órdenes de magnitud distintos,
casi todo en el arranque. AOT compra latencia inicial y previsibilidad; JIT compra información que
solo existe en ejecución. La pregunta útil nunca es cuál es mejor, sino **cuánto dura el proceso**.

⏮️ [Volver a la clase 126](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
