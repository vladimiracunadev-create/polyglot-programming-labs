# 🧬 El mismo programa en las familias de lenguajes — Clase 167

> [⬅️ Volver a la clase 167](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —parsear un comando y contar sus argumentos—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `comando arg1 arg2 ...` (al menos el comando)
- **Salida** (stdout): `comando=<comando> args=<número de argumentos>`
- **Regla:** el primer token es el comando; el resto son los argumentos

| stdin | esperado |
|---|---|
| `run a b` | `comando=run args=2` |
| `build` | `comando=build args=0` |
| `deploy x y z` | `comando=deploy args=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y desestructuración: separar la cabeza de la cola de una lista es un solo gesto.

### Ruby

```ruby
comando, *args = STDIN.read.split
puts "comando=#{comando} args=#{args.size}"
```

### Perl

```perl
my ($comando, @args) = split ' ', do { local $/; <STDIN> };
printf "comando=%s args=%d\n", $comando, scalar @args;
```

### Lua

```lua
local tokens = {}
for palabra in io.read("a"):gmatch("%S+") do
  tokens[#tokens + 1] = palabra
end
print(string.format("comando=%s args=%d", tokens[1], #tokens - 1))
```

### Tcl

```tcl
set tokens [regexp -all -inline {\S+} [read stdin]]
puts "comando=[lindex $tokens 0] args=[expr {[llength $tokens] - 1}]"
```

### R

```r
tok <- scan("stdin", what = character(), quiet = TRUE)
cat(sprintf("comando=%s args=%d\n", tok[1], length(tok) - 1))
```

**Qué reconocer:** Ruby y Perl expresan el contrato **exactamente como está enunciado** —un nombre
para la cabeza, un resto para la cola— y esa es su ventaja real cuando el componente que se está
escribiendo es una CLI: con `OptionParser` o `Thor` en Ruby, o `Getopt::Long` en Perl, una
herramienta de línea de comandos con subcomandos y `--flags` se escribe en la mitad de tiempo que en
cualquier lenguaje compilado. El coste es de despliegue y es concreto: la herramienta no se ejecuta
si la máquina destino no tiene el intérprete instalado, en una versión compatible, con sus gemas o
módulos resueltos. Lua es el caso aparte de la familia: su intérprete completo pesa unos cientos de
kilobytes y está pensado para **empotrarse** dentro de otro programa, que es por lo que Redis,
Neovim y nginx lo llevan dentro en vez de exponerlo como binario propio. Tcl sigue siendo el lenguaje
de consola de mucho equipamiento de red y de herramientas EDA por la misma razón histórica.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final tokens = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  stdout.writeln('comando=${tokens.first} args=${tokens.length - 1}');
}
```

### ActionScript 3

```actionscript
// Flash / AIR no expone stdin ni argv como tal: el parseo del comando
// se expresa como función pura sobre la línea ya recibida.
package {
    public class Cli {
        public static function parsear(linea:String):String {
            var tokens:Array = linea.split(/\s+/);
            return "comando=" + tokens[0] + " args=" + (tokens.length - 1);
        }
    }
}
```

**Qué reconocer:** Dart es el primo que de verdad compite en este terreno, porque
`dart compile exe` produce un **ejecutable autocontenido** —igual que Go o Rust— sin que haya que
instalar el SDK en la máquina destino. Es la excepción de esta familia: una CLI en Node exige Node
instalado, y ese ha sido siempre el punto flaco de las herramientas de consola escritas en
JavaScript. ActionScript aquí solo puede ilustrar el cálculo, y merece la pena leer por qué: un
lenguaje atado a una plataforma gráfica no puede ser el componente CLI de nada.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val tokens = readLine()!!.trim().split(Regex("\\s+"))
    println("comando=${tokens.first()} args=${tokens.size - 1}")
}
```

### Scala

```scala
object Cli extends App {
  val tokens = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"comando=${tokens.head} args=${tokens.length - 1}")
}
```

### Groovy

```groovy
def tokens = System.in.newReader().readLine().trim().split(/\s+/)
println "comando=${tokens[0]} args=${tokens.size() - 1}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[comando & args] (str/split (str/trim (read-line)) #"\s+")]
  (println (format "comando=%s args=%d" comando (count args))))
```

**Qué reconocer:** Clojure y Scala parten la lista en cabeza y cola igual que Ruby, y las
bibliotecas de parseo de esta familia son de las mejores que existen —`picocli` en Java y Kotlin,
`clikt` en Kotlin, `decline` en Scala, `tools.cli` en Clojure—. Y aun así la JVM es una elección
discutible para una CLI por un motivo muy concreto: el **arranque**. Una herramienta que se invoca
cien veces en un script paga cien veces el arranque de la máquina virtual, que se mide en cientos de
milisegundos frente a los pocos que tarda un binario nativo. La respuesta real de la plataforma es
compilar con GraalVM `native-image` —picocli está diseñado para ello—, pero eso añade otro paso de
compilación y sus propias restricciones sobre reflexión: una solución de verdad, no gratis.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let tokens =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)

printfn "comando=%s args=%d" tokens.[0] (tokens.Length - 1)
```

### VB.NET

```vbnet
Module Cli
    Sub Main()
        Dim tokens = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("comando=" & tokens(0) & " args=" & (tokens.Length - 1))
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `String.Split` y el mismo `Main(string[] args)`, y la
plataforma trae `System.CommandLine` para el parseo serio; F# además tiene `Argu`, que declara los
argumentos como una unión discriminada y hace que el compilador verifique el uso. .NET resuelve el
problema de arranque de la JVM mejor de lo que suele reconocerse: `dotnet publish` con
`PublishSingleFile` y `PublishAot` produce un ejecutable único sin runtime instalado. El coste de
elegir esta familia para el componente CLI no es técnico sino de contexto: si el resto del sistema no
es .NET, se está añadiendo una toolchain entera —SDK, `nuget`, su propio CI— por una sola
herramienta.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string comando, palabra;
    std::cin >> comando;
    int args = 0;
    while (std::cin >> palabra) ++args;
    std::cout << "comando=" << comando << " args=" << args << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *entrada = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:entrada encoding:NSUTF8StringEncoding];
        NSArray<NSString *> *tokens =
            [[linea stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]]
             componentsSeparatedByCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];
        printf("comando=%s args=%lu\n",
               [tokens.firstObject UTF8String],
               (unsigned long)(tokens.count - 1));
    }
    return 0;
}
```

**Qué reconocer:** esta es la familia que **inventó** la forma de la CLI: `argc`, `argv`, `getopt` y
la convención de `-v` y `--verbose` salieron de aquí, y todo lo que hacen los demás lenguajes imita
ese modelo. C++ mantiene la puerta abierta a `getopt` de C mientras ofrece bibliotecas modernas como
`CLI11`; Objective-C sube hasta `NSArray` y `NSProcessInfo` para lo mismo. Producen binarios
diminutos y de arranque instantáneo, pero el coste está en el otro extremo del ciclo: cada plataforma
destino necesita su propia compilación, y gestionar dependencias en C++ sigue siendo trabajo manual
comparado con `cargo` o `go get`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    const comando = it.next().?;
    var args: usize = 0;
    while (it.next()) |_| args += 1;
    try std.io.getStdOut().writer().print("comando={s} args={d}\n", .{ comando, args });
}
```

### Nim

```nim
import std/strutils

let tokens = stdin.readLine().splitWhitespace()
echo "comando=", tokens[0], " args=", tokens.len - 1
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto tokens = readln().strip().split();
    writefln("comando=%s args=%d", tokens[0], tokens.length - 1);
}
```

**Qué reconocer:** esta es la familia natural del componente CLI, y la ventaja es medible, no
retórica: **un binario único, arranque en milisegundos, cero runtime que instalar**. Zig lo lleva más
lejos que nadie —el programa de arriba no reserva memoria dinámica ni una vez, y su compilador
además hace *cross-compilation* a otras plataformas sin instalar nada extra, así que una sola máquina
produce el binario de Linux, macOS y Windows—. D trae `std.getopt` en la biblioteca estándar y Nim
tiene `parseopt`, ambas suficientes para una herramienta real. El coste hay que decirlo con la misma
claridad: Zig todavía rompe compatibilidad entre versiones y no ha llegado a 1.0, y las comunidades
de Nim y D son pequeñas, así que se gana despliegue y se pierde ecosistema y facilidad para
encontrar quien lo mantenga.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes0),
    exclude(==(""), Partes0, [Comando|Args]),
    length(Args, N),
    format("comando=~w args=~d~n", [Comando, N]).
```

### Datalog

```datalog
% Datalog no tiene stdin, ni parseo de cadenas, ni agregados: no puede contar.
% Lo más cercano es declarar la invocación como hechos y relacionar comando y argumentos.
invocacion("run").
argumento("run", "a").
argumento("run", "b").

recibe(C, A) :- invocacion(C), argumento(C, A).
```

**Qué reconocer:** Prolog parte la lista en `[Comando|Args]` con la misma notación de cabeza y cola
que Clojure o Ruby, solo que aquí es **unificación de patrones**, no desestructuración: el término
`[Comando|Args]` describe la forma que la lista debe tener y falla si no la tiene. SWI-Prolog sí
puede ser un ejecutable de consola —tiene `current_prolog_flag(argv, _)` y compilación a `.exe`—,
así que la limitación aquí es de idoneidad, no de capacidad. Datalog no puede ni contar: sin
agregados ni E/S, lo único que declara es qué argumentos pertenecen a qué invocación. Esa renuncia
es la que hace que esta familia aparezca en los sistemas reales como motor de reglas dentro de otro
componente, nunca como la herramienta que el usuario teclea.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer la línea, separar la cabeza
de la cola, contar. Pero la elección para una CLI real no se juega en estas líneas: se juega en si el
usuario tiene que instalar un intérprete antes de usarla, en cuánto tarda en arrancar cuando un
script la invoca mil veces, y en si tu equipo puede mantener esa toolchain dentro de dos años.

⏮️ [Volver a la clase 167](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
