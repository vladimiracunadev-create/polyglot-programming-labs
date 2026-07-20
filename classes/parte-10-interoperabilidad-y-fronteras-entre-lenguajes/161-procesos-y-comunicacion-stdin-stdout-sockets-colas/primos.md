# 🧬 El mismo programa en las familias de lenguajes — Clase 161

> [⬅️ Volver a la clase 161](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —consumir los mensajes de una cola y sumarlos—
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

- **Entrada** (stdin, una línea): enteros separados por espacio, los mensajes de la cola
- **Salida** (stdout): `recibido=<suma de los mensajes>`
- **Regla:** sumar los mensajes recibidos en orden

| stdin | esperado |
|---|---|
| `1 2 3` | `recibido=6` |
| `5` | `recibido=5` |
| `10 20 30 40` | `recibido=100` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Los lenguajes del pegamento entre procesos: nacidos para leer de una tubería y escribir en otra.

### Ruby

```ruby
cola = STDIN.read.split.map(&:to_i)
puts "recibido=#{cola.sum}"
```

### Perl

```perl
use List::Util qw(sum0);

my @cola = split ' ', <STDIN>;
printf "recibido=%d\n", sum0(@cola);
```

### Lua

```lua
-- Lua no trae sockets en su biblioteca estándar (haría falta LuaSocket),
-- pero io.read sobre stdin sí es parte del núcleo.
local recibido = 0
for m in io.read("l"):gmatch("%-?%d+") do
  recibido = recibido + tonumber(m)
end
print("recibido=" .. recibido)
```

### Tcl

```tcl
# Tcl trae `socket` en el núcleo del lenguaje; aquí basta el canal stdin,
# que es un canal más, indistinguible de un socket para el resto del código.
gets stdin linea
set recibido 0
foreach m [split [string trim $linea]] {
    incr recibido $m
}
puts "recibido=$recibido"
```

### R

```r
cola <- scan("stdin", what = integer(), quiet = TRUE)
cat(sprintf("recibido=%d\n", sum(cola)))
```

**Qué reconocer:** los cinco leen la cola igual —una línea de stdin, partir, sumar— y ahí acaba el
parecido. En sockets la familia se rompe: Ruby trae `TCPServer` y Perl `IO::Socket` en su
distribución, **Lua no trae ninguno** y necesita LuaSocket, y R los abre con `socketConnection` pero
de forma bloqueante y sin bucle de eventos. **Tcl es el más elegante de la tanda**: `socket` está en
el núcleo del lenguaje, devuelve un canal que se lee con el mismo `gets` que stdin, y `fileevent`
más `vwait` dan un servidor concurrente sin hilos ni bibliotecas. Un programa Tcl puede cambiar de
tubería a red sustituyendo una línea.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Familia del bucle de eventos: la cola de mensajes no es una biblioteca, es el modelo de ejecución.

### Dart

```dart
import 'dart:io';

void main() {
  final cola = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  final recibido = cola.fold<int>(0, (a, b) => a + b);
  print('recibido=$recibido');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash: no tiene stdin ni procesos hijos,
// solo flash.net.Socket. Se ilustra el consumo de la cola ya recibida.
package {
    public class Cola {
        public static function recibir(mensajes:Array):String {
            var recibido:int = 0;
            for each (var m:int in mensajes) {
                recibido += m;
            }
            return "recibido=" + recibido;
        }
    }
}
```

**Qué reconocer:** ActionScript marca el límite duro de esta clase: **no tiene stdin ni puede lanzar
procesos**, porque el reproductor Flash era una caja aislada; lo único que le queda es
`flash.net.Socket`, y aun así solo hacia servidores que publiquen una política de seguridad. Dart es
lo contrario: `dart:io` trae `stdin`, `Process.start` y `ServerSocket`, y añade los **isolates**, que
se comunican por paso de mensajes con `SendPort` —una cola real dentro del proceso, sin memoria
compartida, igual que si fueran procesos separados. Es el mismo modelo de los Web Workers de
JavaScript, con la misma consecuencia: lo que cruza la frontera se copia.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Hilos con memoria compartida, y sobre ellos
todas las abstracciones de cola que existen.

### Kotlin

```kotlin
fun main() {
    val recibido = readLine()!!.trim().split(Regex("\\s+")).sumOf { it.toInt() }
    println("recibido=$recibido")
}
```

### Scala

```scala
object Cola extends App {
  val recibido = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt).sum
  println(s"recibido=$recibido")
}
```

### Groovy

```groovy
def recibido = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger().sum()
println "recibido=$recibido"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [cola (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "recibido=" (reduce + cola))))
```

**Qué reconocer:** los cuatro heredan de Java el mismo `System.in`, el mismo `ProcessBuilder` para
lanzar procesos hijos y la misma `BlockingQueue` para las colas dentro del proceso. Lo que cambia es
la abstracción que cada comunidad pone encima: Kotlin usa corrutinas y `Channel`, Scala el modelo de
actores de Akka —donde cada actor tiene su propio buzón y nada se comparte—, y Clojure `core.async`,
que copia los canales de Go dentro de la JVM. Cuatro vocabularios distintos para la misma idea de
esta clase: **un productor deposita, un consumidor retira, y la cola desacopla su velocidad**.
Groovy es el que menos ceremonia pone para lo básico, y por eso vive en los scripts de despliegue.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let recibido =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.sumBy int
printfn "recibido=%d" recibido
```

### VB.NET

```vbnet
Imports System

Module Cola
    Sub Main()
        Dim cola = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Dim recibido = 0
        For Each m In cola
            recibido += Integer.Parse(m)
        Next
        Console.WriteLine($"recibido={recibido}")
    End Sub
End Module
```

**Qué reconocer:** los tres comparten `Console.In`, `Process` con
`RedirectStandardOutput = True` para hablar con un hijo por tuberías, y
`System.Threading.Channels` para la cola en memoria. F# añade lo más parecido a Erlang que hay en el
CLR: el `MailboxProcessor`, un agente con buzón propio que se lee con `Receive()` en un bucle
asíncrono, sin bloqueo alguno ni cerrojos. VB.NET no tiene nada equivalente en su sintaxis y usa las
mismas clases con `For Each`, lo que deja claro que en esta plataforma **la concurrencia vive en la
biblioteca, no en el lenguaje**.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La capa donde stdin, socket y tubería son lo mismo:
un descriptor de fichero.

### C++

```cpp
#include <iostream>

int main() {
    long long recibido = 0, m;
    while (std::cin >> m) {
        recibido += m;
    }
    std::cout << "recibido=" << recibido << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long recibido = 0, m;
        while (scanf("%lld", &m) == 1) {
            recibido += m;
        }
        printf("recibido=%lld\n", recibido);
    }
    return 0;
}
```

**Qué reconocer:** en esta familia se ve el mecanismo desnudo: `fork` duplica el proceso, `pipe` crea
el par de descriptores y `exec` reemplaza el programa, que es literalmente lo que hacen por dentro
`subprocess` de Python y `ProcessBuilder` de Java. C++ envuelve el descriptor en un flujo —`std::cin`
es el mismo `stdin` de C con otra cara— y desde C++11 añade `std::thread` y colas propias, pero sin
socket en la biblioteca estándar. Objective-C sí lo trae todo en Foundation: `NSTask` para el proceso
hijo, `NSPipe` para el canal y `NSRunLoop` para atenderlos sin bloquear, un bucle de eventos muy
parecido al de Tcl. Es la misma idea, empaquetada por Apple.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Nativos, sin runtime
pesado, con acceso directo a las llamadas al sistema.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var recibido: i64 = 0;
    while (it.next()) |m| {
        recibido += try std.fmt.parseInt(i64, m, 10);
    }
    try std.io.getStdOut().writer().print("recibido={d}\n", .{recibido});
}
```

### Nim

```nim
import std/[strutils, sequtils, math]

let cola = stdin.readLine().splitWhitespace().map(parseInt)
echo "recibido=", cola.sum()
```

### D

```d
import std.stdio, std.array, std.string, std.conv, std.algorithm;

void main() {
    auto cola = readln().strip().split().map!(to!long);
    writefln("recibido=%d", cola.sum());
}
```

**Qué reconocer:** los tres traen en la biblioteca estándar lo que C deja al sistema operativo:
`std.process.Child` en Zig, `std/osproc` en Nim y `std.process` en D lanzan un hijo y capturan su
salida en tres líneas, sin tocar `fork`. Y los tres traen serializador JSON incluido, así que pueden
poner un mensaje estructurado en la cola sin dependencias. En sockets se separan de Go y Rust: Zig
expone `std.net` a bajo nivel y sin abstracción de concurrencia, mientras D ofrece paso de mensajes
entre hilos con `std.concurrency` —`send` y `receive` sobre buzones, con los datos aislados por el
sistema de tipos, la misma renuncia a la memoria compartida que hace Rust.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Describir el resultado, no el recorrido: sumar
la cola es una agregación, no un bucle.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    maplist([S, N]>>number_string(N, S), Partes, Cola),
    sum_list(Cola, Recibido),
    format("recibido=~w~n", [Recibido]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S, procesos ni agregación: los mensajes se declaran
% como hechos. Sumarlos exige un dialecto con agregados, como Soufflé:
%   recibido(t) :- t = sum v : { mensaje(_, v) }.
mensaje(1, 1).
mensaje(2, 2).
mensaje(3, 3).
```

**Qué reconocer:** Prolog sí puede hablar con el mundo —`read_line_to_string/2` sobre `user_input`,
y SWI-Prolog trae `process_create/3` y sockets—, pero la suma se expresa como `sum_list/2` sobre la
lista completa, no como un acumulador que se reasigna en un bucle. Datalog no puede ni eso: sin E/S,
sin efectos y sin agregación en el núcleo, los mensajes solo existen como hechos declarados, y la
suma requiere salirse a un dialecto como Soufflé. Es la misma renuncia de SQL, que agrega con `sum()`
y no te deja decidir en qué orden se recorren las filas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una conclusión que vale más que el código: los mecanismos de
comunicación difieren enormemente —Tcl tiene sockets en el núcleo, Lua no tiene ninguno, ActionScript
ni siquiera puede lanzar un proceso—, pero **stdin/stdout es el único mecanismo que todos comparten**.
Por eso el [verificador de equivalencia](../../../labs/README.md) de este curso está construido sobre
él: es el mínimo común denominador de la interoperabilidad, y el único contrato que ningún lenguaje
se niega a cumplir. Eso es lo transferible.

⏮️ [Volver a la clase 161](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
