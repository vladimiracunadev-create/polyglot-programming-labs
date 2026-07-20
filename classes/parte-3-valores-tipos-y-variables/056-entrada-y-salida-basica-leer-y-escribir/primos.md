# 🧬 El mismo programa en las familias de lenguajes — Clase 056

> [⬅️ Volver a la clase 056](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —leer una línea y devolverla con un prefijo— resuelto
por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez
lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir. Y este problema, el más pequeño
de toda la parte, es el que mejor mide la **ceremonia** de cada lenguaje: aquí no hay algoritmo que
esconda la diferencia, solo leer y escribir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un texto cualquiera
- **Salida** (stdout): `eco: <la línea leída>`
- **Regla:** anteponer el prefijo `eco:` y un espacio a la línea, sin su salto de línea final

| stdin | esperado |
|---|---|
| `hola` | `eco: hola` |
| `Polyglot` | `eco: Polyglot` |
| `123` | `eco: 123` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico y poca ceremonia: la entrada/salida está en el lenguaje mismo, no detrás de una
biblioteca que haya que importar.

### Ruby

```ruby
puts "eco: #{STDIN.gets.chomp}"
```

### Perl

```perl
my $linea = <STDIN>;
chomp $linea;
print "eco: $linea\n";
```

### Lua

```lua
local linea = io.read("l")
print("eco: " .. linea)
```

### Tcl

```tcl
gets stdin linea
puts "eco: $linea"
```

### R

```r
linea <- readLines("stdin", n = 1)
cat("eco: ", linea, "\n", sep = "")
```

**Qué reconocer:** los cinco resuelven el problema en una o dos líneas y ninguno necesita declarar un
`main`. La diferencia real está en **qué hace cada uno con el salto de línea**: Ruby y Perl entregan la
línea *con* el `\n` y hay que quitarlo con `chomp` —el mismo nombre de función en los dos, porque Ruby
lo tomó prestado de Perl—; Lua con el modo `"l"`, Tcl con `gets` y R con `readLines` lo descartan
solos. Ese detalle es la fuente número uno de fallos al portar un programa entre estos lenguajes.
Fíjate también en que Tcl usa `gets` con un **nombre de variable** como segundo argumento en vez de
devolver la línea: devuelve el número de caracteres leídos, para que el bucle sepa cuándo parar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final linea = stdin.readLineSync() ?? '';
  stdout.writeln('eco: $linea');
}
```

### ActionScript 3

```actionscript
// El reproductor Flash no tiene stdin ni stdout: la entrada llega de un campo de texto
// y la salida se escribe en otro. `trace` solo va a la consola de depuración.
package {
    import flash.display.Sprite;
    import flash.text.TextField;
    import flash.text.TextFieldType;

    public class Eco extends Sprite {
        private var entrada:TextField = new TextField();
        private var salida:TextField = new TextField();

        public function Eco() {
            entrada.type = TextFieldType.INPUT;
            addChild(entrada);
            addChild(salida);
        }

        public function repetir():void {
            salida.text = "eco: " + entrada.text;
            trace(salida.text);
        }
    }
}
```

**Qué reconocer:** esta familia es la que peor encaja en el molde de la consola, y por eso es la más
instructiva. Ninguno de sus miembros tiene entrada/salida en el **lenguaje**: la reciben del entorno.
JavaScript en el navegador no puede leer stdin —hizo falta Node y su módulo `readline` para eso—, y
ActionScript, atado al reproductor Flash, ni siquiera tiene un equivalente: su "entrada" es un widget
de la pantalla. Dart sí trae `dart:io`, pero solo cuando compila para servidor o escritorio; el mismo
programa compilado a JavaScript para el navegador no encontraría `stdin`. La lección transferible es
que la E/S es una **capacidad del anfitrión**, no del lenguaje.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    println("eco: ${readln()}")
}
```

### Scala

```scala
object Eco extends App {
  println(s"eco: ${scala.io.StdIn.readLine()}")
}
```

### Groovy

```groovy
println "eco: ${System.in.newReader().readLine()}"
```

### Clojure

```clojure
(println (str "eco: " (read-line)))
```

**Qué reconocer:** este es el caso donde la familia JVM se luce, porque el problema es justo aquel en
el que Java resulta más pesado. Los cuatro terminan llamando al mismo `System.in` de Java, pero
ninguno te obliga a construir un `BufferedReader` sobre un `InputStreamReader` ni a declarar la
excepción comprobada. Kotlin llegó a añadir `readln()` —una función de la biblioteca estándar que
devuelve `String` no nulo y lanza excepción si no hay línea— precisamente para que el caso común no
arrastre el `?` de nulabilidad. Clojure cambia de paradigma dentro de la misma máquina virtual: `str`
concatena, `println` imprime, y todo se lee de dentro hacia fuera.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
printfn "eco: %s" (stdin.ReadLine())
```

### VB.NET

```vbnet
Imports System

Module Eco
    Sub Main()
        Dim linea = Console.ReadLine()
        Console.WriteLine("eco: " & linea)
    End Sub
End Module
```

**Qué reconocer:** los tres pasan por la misma clase `System.Console` del CLR, con su par
`ReadLine`/`WriteLine` que ya descarta el salto de línea al leer y lo añade al escribir. VB.NET marca
su tradición en el operador: usa `&` para concatenar texto, reservando `+` para la suma, justamente
para evitar la ambigüedad que en JavaScript hace que `"1" + 1` valga `"11"`. F# demuestra que su
`printfn` no es el `printf` de C: la cadena de formato se comprueba **en compilación**, así que poner
`%d` donde va un `string` es un error antes de ejecutar, no un fallo en tiempo de ejecución.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string linea;
    std::getline(std::cin, linea);
    std::cout << "eco: " << linea << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSFileHandle *entrada = [NSFileHandle fileHandleWithStandardInput];
        NSData *datos = [entrada availableData];
        NSString *linea = [[NSString alloc] initWithData:datos
                                                encoding:NSUTF8StringEncoding];
        linea = [linea stringByTrimmingCharactersInSet:
                     [NSCharacterSet newlineCharacterSet]];
        printf("eco: %s\n", [linea UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C**, y ambos huyen de la trampa que la clase señala en
el representante: `fgets` obliga a reservar un búfer de tamaño fijo y a decidir de antemano cuánto es
"suficiente". C++ lo resuelve con `std::getline`, que hace crecer el `std::string` tanto como haga
falta. Objective-C sube un nivel más y trabaja con objetos de Foundation: `NSData` para los bytes
crudos y `NSString` para el texto **ya decodificado como UTF-8**. Esa separación explícita entre bytes
y caracteres es la que C no hace en ningún momento, y explica por qué un `char*` de C no sabe nada de
acentos.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [4096]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')) orelse "";
    const limpia = std.mem.trimRight(u8, linea, "\r");
    try std.io.getStdOut().writer().print("eco: {s}\n", .{limpia});
}
```

### Nim

```nim
echo "eco: " & stdin.readLine()
```

### D

```d
import std.stdio, std.string;

void main() {
    const linea = readln().chomp();
    writeln("eco: ", linea);
}
```

**Qué reconocer:** Zig es el más explícito de todos: reserva el búfer a mano —y con él impone un límite
de línea que tú eliges—, cada operación que puede fallar lleva `try`, y el `orelse` obliga a decidir
qué pasa si la entrada se acaba. Es el mismo rigor que Rust impone con `Result`. Nim y D esconden esa
maquinaria tras una sintaxis de scripting: el programa de Nim es una sola línea, tan corto como el de
Ruby, y sigue compilando a un binario nativo sin máquina virtual. Fíjate en que D reutiliza el nombre
`chomp` de Perl, otro ejemplo de que el vocabulario viaja entre familias aunque el modelo de ejecución
no tenga nada que ver.

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
    format("eco: ~w~n", [Linea]).
```

### Datalog

```datalog
% Datalog no tiene entrada ni salida: no existen `read` ni `print`, solo hechos y
% consultas. Lo más cercano es declarar la línea como hecho y derivar la respuesta;
% mostrarla es tarea del motor que ejecuta la consulta, no del lenguaje.
% (`cat` concatena cadenas en dialectos como Soufflé; el Datalog puro no lo tiene.)
linea("hola").

eco(E) :- linea(L), E = cat("eco: ", L).
```

**Qué reconocer:** Prolog es un lenguaje lógico, pero **sí tiene efectos**: `read_line_to_string` y
`format` son predicados que se cumplen siempre y cuya razón de existir es el efecto secundario, no la
verdad que declaran. Esa grieta pragmática en la pureza es lo que lo hace utilizable como lenguaje de
propósito general. Datalog no la tiene: al renunciar a los efectos para garantizar que toda consulta
termine, se queda sin manera de leer o escribir nada, y depende por completo del programa anfitrión
que lo invoca. Es la misma renuncia que hace SQL, que tampoco lee de stdin: recibe filas de una tabla
y devuelve filas a quien preguntó.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en casi todos: leer una línea, quitarle el
salto final, escribirla con un prefijo. Lo que cambia es la **ceremonia** —de una línea en Nim a un
`package` entero en ActionScript— y, más de fondo, **de dónde viene la E/S**: del lenguaje, de su
biblioteca estándar o del entorno que lo hospeda. Eso es lo transferible.

⏮️ [Volver a la clase 056](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
