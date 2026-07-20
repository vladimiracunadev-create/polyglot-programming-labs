# 🧬 El mismo programa en las familias de lenguajes — Clase 169

> [⬅️ Volver a la clase 169](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —el componente web que declara cuántos elementos
renderiza y confirma el render— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de JavaScript, la de Dart te resultará familiar aunque no la hayas visto
nunca. Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `n` (número de elementos a renderizar)
- **Salida** (stdout): `items=<n> render=ok`
- **Regla:** renderizar `n` elementos y confirmar el render

| stdin | esperado |
|---|---|
| `3` | `items=3 render=ok` |
| `0` | `items=0 render=ok` |
| `10` | `items=10 render=ok` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Son los lenguajes del **servidor** que generan el HTML antes de que llegue al navegador. En el
frontend no ejecutan nada: preparan la vista y la entregan.

### Ruby

```ruby
n = STDIN.gets.to_i
puts "items=#{n} render=ok"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
printf "items=%d render=ok\n", $n;
```

### Lua

```lua
local n = io.read("n")
print(string.format("items=%d render=ok", n))
```

### Tcl

```tcl
gets stdin linea
set n [expr {int($linea)}]
puts "items=$n render=ok"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("items=%d render=ok\n", n))
```

**Qué reconocer:** los cinco hacen lo mismo que Python y PHP —leer, convertir, imprimir— pero
ninguno de ellos corre en un navegador. Esa es la frontera técnica de esta clase: cuando el
componente es la vista, estos lenguajes se quedan del lado del servidor, generando la plantilla que
otro motor pintará. Ruby lo hace con ERB, Lua dentro de OpenResty, R con Shiny —que envía HTML y
JavaScript ya generados—. Fíjate además en que la conversión a entero sigue siendo explícita
(`to_i`, `int`, `as.integer`), mientras que en la familia web es el `parseInt` de JavaScript.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Aquí el dominio no es una moda: **es el único lenguaje que el navegador ejecuta de forma nativa**.
Todo lo demás llega compilando a JavaScript o a WebAssembly.

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('items=$n render=ok');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 corre en el reproductor Flash, no en el navegador moderno:
// no hay stdin y la vista se compone sobre la lista de display.
package {
    import flash.display.Sprite;

    public class Lista extends Sprite {
        public function render(n:int):String {
            for (var i:int = 0; i < n; i++) {
                addChild(new Sprite());
            }
            return "items=" + n + " render=ok";
        }
    }
}
```

**Qué reconocer:** Dart no se ejecuta en el navegador; **compila a JavaScript** (`dart compile js`),
y con Flutter Web puede compilar además a WebAssembly. Lo mismo hacen Kotlin/JS, Scala.js y
ClojureScript: cada uno cruza el puente hacia el motor del navegador. Lo que se gana en ese cruce es
un sistema de tipos, un modelo de concurrencia o una biblioteca que JavaScript no tiene; lo que se
pierde es peso del paquete descargado, tiempos de compilación, y una capa de indirección al depurar
—el error ocurre en el JavaScript generado, no en el fuente que escribiste, y hace falta un *source
map* para volver—. Con WebAssembly la pérdida cambia de forma: se gana rendimiento predecible, pero
el módulo no toca el DOM por sí solo y necesita un puente de JavaScript para cada interacción con la
página. ActionScript es el aviso histórico de esta clase: fue el lenguaje del frontend durante años
y desapareció cuando el navegador dejó de cargar su reproductor.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; para llegar al navegador necesitan un segundo compilador.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    println("items=$n render=ok")
}
```

### Scala

```scala
object Vista {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    println(s"items=$n render=ok")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
println "items=$n render=ok"
```

### Clojure

```clojure
(let [n (Integer/parseInt (.trim (read-line)))]
  (println (format "items=%d render=ok" n)))
```

**Qué reconocer:** el mismo fuente de Kotlin puede compilarse a bytecode de la JVM **o** a
JavaScript con Kotlin/JS, y Scala hace lo propio con Scala.js; Clojure tiene ClojureScript, un
dialecto separado que comparte casi todo el lenguaje. Groovy es la excepción: vive en la JVM y no
tiene un camino serio al navegador. Ese detalle explica por qué la interpolación de cadena que ves
aquí (`$n`) sobrevive intacta al cruce, pero la biblioteca estándar de Java no: cuando Kotlin
compila a JavaScript, `java.util` no existe al otro lado y hay que usar la parte común del lenguaje.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
printfn "items=%d render=ok" n
```

### VB.NET

```vbnet
Imports System

Module Vista
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine($"items={n} render=ok")
    End Sub
End Module
```

**Qué reconocer:** .NET llega al navegador por la vía de WebAssembly, no por la de JavaScript: Blazor
WebAssembly descarga el runtime de .NET compilado a Wasm y ejecuta el mismo C# o F# que ves aquí sin
traducirlo. Se gana poder escribir un solo lenguaje en cliente y servidor y compartir los tipos del
modelo; se pierde en el arranque —hay que bajar el runtime entero antes del primer render— y en cada
llamada al DOM, que pasa por una capa de interoperabilidad con JavaScript. Fíjate en que F# usa `|>`
para encadenar lo que C# anida, y que VB.NET tiene la misma interpolación `$"..."` desde 2015.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>

int main() {
    int n = 0;
    std::cin >> n;
    std::cout << "items=" << n << " render=ok\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);
        NSString *salida = [NSString stringWithFormat:@"items=%d render=ok", n];
        printf("%s\n", [salida UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C**, y ambos son precisamente el material del que
está hecho el navegador: el motor de renderizado de Chrome y de Safari es C++, y Objective-C fue
durante años el lenguaje de la interfaz en las plataformas de Apple. Es decir, no compiten con
JavaScript en la página, la implementan por debajo. C++ es además el origen práctico de
WebAssembly: Emscripten compila C y C++ a Wasm, y por ahí pasó todo lo pesado —motores de juego,
códecs, editores de imagen— antes de que existiera el ecosistema de Rust en la web.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u32, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("items={d} render=ok\n", .{n});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
echo "items=", n, " render=ok"
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const n = readln().strip().to!int;
    writefln("items=%d render=ok", n);
}
```

**Qué reconocer:** los tres tienen `wasm32` como destino de compilación de primera clase —Zig lo
trae en el propio compilador, Nim genera C que Emscripten convierte, D usa el backend de LDC—, igual
que Rust, que es hoy el camino más usado para llevar cálculo pesado al navegador. Pero el módulo
resultante no ve el DOM: WebAssembly no tiene acceso directo a la página, así que un componente de
interfaz escrito así necesita siempre JavaScript alrededor para leer eventos y escribir nodos. Sirven
para el motor, no para la vista. Zig muestra además el precio de la explicitud: reserva el búfer a
mano y marca con `try` cada operación que puede fallar.

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
    number_string(N, Linea),
    format("items=~d render=ok~n", [N]).
```

### Datalog

```datalog
% Datalog no tiene E/S ni efectos: los elementos son hechos y el recuento se
% deriva con la agregación de Soufflé. No existe la noción de "renderizar".
elemento(1).
elemento(2).
elemento(3).

items(N) :- N = count : { elemento(_) }.
```

**Qué reconocer:** la familia declarativa describe **el estado que debe verse**, no los pasos para
pintarlo, y esa idea es exactamente la que adoptó el frontend moderno: React, Vue y Flutter declaran
cómo se ve la interfaz para unos datos dados y dejan que el motor calcule qué nodos tocar. Lo que
Prolog y Datalog no tienen es el otro lado del contrato —el efecto—: Datalog ni siquiera admite
entrada/salida, así que solo puede afirmar cuántos elementos hay, nunca confirmar que se dibujaron.
Es la misma renuncia que hace SQL al no decirte cómo recorrer las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una conclusión que ninguna otra clase deja tan clara: en el
frontend no todos los caminos son equivalentes. Hay un lenguaje que el navegador ejecuta y hay
puentes hacia él —a JavaScript o a WebAssembly—, cada uno con un peaje distinto. Reconocer el puente
y su peaje es lo transferible.

⏮️ [Volver a la clase 169](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
