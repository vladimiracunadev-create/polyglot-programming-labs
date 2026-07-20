# 🧬 El mismo programa en las familias de lenguajes — Clase 162

> [⬅️ Volver a la clase 162](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el cuadrado de un número, como lo exportaría un
módulo WebAssembly— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí el código es casi trivial en todos: `n * n`. Lo que **no** es trivial, y es lo que esta clase
mira, es si ese código puede acabar dentro de un `.wasm`. Esa pregunta parte la lista en dos.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<n al cuadrado>`
- **Regla:** el módulo recibe `n` y devuelve `n * n`

| stdin | esperado |
|---|---|
| `5` | `resultado=25` |
| `0` | `resultado=0` |
| `7` | `resultado=49` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno compila a wasm: lo que se lleva al navegador es **el intérprete entero**, compilado desde su
código C. Por eso Pyodide pesa megabytes y `n * n` no cuesta nada.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "resultado=#{n * n}"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
printf "resultado=%d\n", $n * $n;
```

### Lua

```lua
local n = io.read("n")
print(string.format("resultado=%d", n * n))
```

### Tcl

```tcl
gets stdin n
puts "resultado=[expr {$n * $n}]"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("resultado=%d\n", n * n))
```

**Qué reconocer:** los cinco escriben la misma multiplicación sin declarar un solo tipo, y Tcl vuelve
a pedir `expr` porque para él `5` es una cadena hasta que alguien decide lo contrario. Pero la
divisoria real de esta clase no es sintáctica: **quién llega a wasm y quién no**. Ruby sí, con
`ruby.wasm`, el build oficial de CRuby para WASI que el proyecto mantiene desde Ruby 3.2. R sí, con
webR, que compila el intérprete de R a wasm y lo ejecuta en la pestaña. Lua sí, aunque de rebote:
como el intérprete son unos pocos miles de líneas de C ANSI, Emscripten lo compila casi sin
resistencia y de ahí salen empaquetados como `wasmoon`. **Perl y Tcl, a julio de 2026, no tienen
ningún camino mantenido a WebAssembly.** No es un descuido de esta página: es el estado del
ecosistema, y conviene decirlo sin adornos.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) ·
[TypeScript](README.md#typescript). Son el **anfitrión** natural de wasm: quien carga el módulo,
le pasa los números y lee el resultado.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('resultado=${n * n}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 no tiene stdin ni salida de consola: se ilustra la funcion
// que el modulo exportaria.
package {
    public class Cuadrado {
        public static function resultado(n:int):String {
            return "resultado=" + (n * n);
        }
    }
}
```

**Qué reconocer:** Dart es hoy el caso más limpio de la familia — `dart2wasm` compila a WasmGC, la
extensión de WebAssembly con recolección de basura, y es el backend con el que Flutter web genera
sus builds. Es decir: un lenguaje con GC que **sí** compila a wasm, no que se lleve su intérprete.
ActionScript cierra el arco por el lado contrario y merece el detalle: Flash Player murió en
diciembre de 2020, y lo que hoy ejecuta un `.swf` es Ruffle, un emulador escrito en Rust que **él
mismo se compila a wasm**. ActionScript no llega a WebAssembly; llega *encima* de WebAssembly, que es
exactamente la diferencia entre compilar a un objetivo y ser interpretado sobre él.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java ya resolvió una vez el problema de "un
binario, muchas máquinas" con su bytecode; wasm es el mismo problema resuelto treinta años después y
sin dueño.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    println("resultado=${n * n}")
}
```

### Scala

```scala
object Cuadrado extends App {
  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"resultado=${n * n}")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
println "resultado=${n * n}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "resultado=" (* n n))))
```

**Qué reconocer:** los cuatro producen el mismo bytecode y esa uniformidad esconde que sus caminos a
wasm son radicalmente distintos. Kotlin tiene un objetivo propio, **Kotlin/Wasm**, que no pasa por la
JVM: compila directo a WasmGC. Scala.js nació apuntando a **JavaScript** y ese sigue siendo su
objetivo por defecto —su salida a wasm es reciente y experimental—, así que un proyecto Scala que
quiera navegador hoy sale como JS, no como `.wasm`. Groovy y Clojure no tienen backend de wasm en
absoluto; Clojure llega al navegador por ClojureScript, que también es JavaScript. Compartir máquina
virtual no implica compartir destinos de compilación.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
printfn "resultado=%d" (n * n)
```

### VB.NET

```vbnet
Module Cuadrado
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine("resultado=" & (n * n))
    End Sub
End Module
```

**Qué reconocer:** .NET adopta un modelo intermedio que conviene distinguir del de C++ o Zig. Lo que
se compila a wasm no es tu código sino **el runtime**: `wasm-tools` produce un `.wasm` con el CLR
dentro, y tus ensamblados IL viajan al lado y se interpretan o se compilan ahí. Por eso F# funciona
en Blazor WebAssembly sin esfuerzo —comparte IL con C#— mientras que VB.NET, que genera el mismo IL,
nunca fue un objetivo soportado del lado cliente. La lección es que "¿este lenguaje corre en wasm?"
tiene al menos tres respuestas distintas: compila a wasm, su runtime compila a wasm, o su
herramienta oficial nunca lo contempló.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde nació todo esto.

### C++

```cpp
#include <iostream>

int main() {
    long long n = 0;
    std::cin >> n;
    std::cout << "resultado=" << n * n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long n = 0;
        if (scanf("%lld", &n) != 1) return 1;
        printf("resultado=%lld\n", n * n);
    }
    return 0;
}
```

**Qué reconocer:** C++ no es un lenguaje más de la lista de wasm, es su **origen**. Emscripten
compilaba C y C++ a asm.js antes de que WebAssembly existiera, y el formato se diseñó midiéndose
contra ese caso de uso; hoy `emcc main.cpp -o main.html` sigue siendo el camino de referencia.
Objective-C comparte compilador con C++ —clang emite wasm sin quejarse del subconjunto C— pero
**no** tiene camino práctico: el runtime de Objective-C y Foundation no están portados, así que en
cuanto aparece un `NSString` o un `@autoreleasepool` real se acaba el viaje. El mismo frontend de
compilador, dos destinos incomparables, y la diferencia está en la biblioteca, no en la sintaxis.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Sin runtime pesado y con
control del layout de memoria: exactamente lo que wasm premia.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("resultado={d}\n", .{n * n});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
echo "resultado=", n * n
```

### D

```d
import std.stdio, std.conv, std.string;

void main() {
    const n = readln().strip().to!long;
    writefln("resultado=%d", n * n);
}
```

**Qué reconocer:** ésta es la familia mejor situada y no por casualidad. Zig trae wasm **de serie**:
`zig build-exe main.zig -target wasm32-wasi` funciona con la instalación limpia, sin SDK aparte, sin
Emscripten, sin instalar nada más —es un objetivo de compilación cruzada como cualquier otro, igual
que compilar para ARM—. Nim llega por su ruta habitual, generando C y pasándoselo a Emscripten. D lo
consigue con LDC y `-mtriple=wasm32-unknown-unknown`, pero en la práctica se trabaja en el
subconjunto `-betterC`, porque el runtime completo con su GC no está pensado para ese entorno. Tres
grados de comodidad para el mismo objetivo, y el que menos ceremonia pide es el más joven.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    Cuadrado is N * N,
    format("resultado=~d~n", [Cuadrado]).
```

### Datalog

```datalog
% Datalog puro no tiene entrada/salida: el numero entra como hecho declarado
% y la regla deriva el cuadrado.
entrada(5).

resultado(R) :- entrada(N), R = N * N.
```

**Qué reconocer:** Prolog vuelve a mostrar que `is` **evalúa y unifica**, no asigna: `Cuadrado` se
liga una sola vez con el valor de `N * N`. Y sí tiene camino a wasm, cosa que sorprende — SWI-Prolog
publica un build oficial del intérprete compilado con Emscripten, el mismo mecanismo de Ruby y R:
llevarse la máquina, no traducir el programa. Datalog no participa en la conversación en absoluto,
porque no tiene programa que llevarse: solo hechos y reglas, sin efectos ni E/S, igual que SQL no
te deja decir cómo recorrer las filas. Un lenguaje sin efectos no tiene nada que ejecutar en un
sandbox.

---

## Y de vuelta a la clase

Veinte lenguajes para escribir `n * n`, y la sintaxis apenas cambia. Lo que cambia —y es el asunto de
esta clase— es la respuesta a "¿esto llega a un `.wasm`?": compilan de forma nativa (C++, Zig, Nim,
D, Kotlin, Dart), se llevan su intérprete entero (Ruby, R, Lua, Prolog, .NET), salen por JavaScript
en vez de por wasm (Scala.js, ClojureScript) o simplemente no llegan (Perl, Tcl, Objective-C,
Groovy). Esa clasificación, y no la sintaxis, es lo transferible.

⏮️ [Volver a la clase 162](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
