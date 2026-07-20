# 🧬 El mismo programa en las familias de lenguajes — Clase 119

> [⬅️ Volver a la clase 119](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —emitir *n* eventos y recolectarlos en un manejador—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Si entendiste la versión de JavaScript, la de Ruby te resultará familiar aunque no la hayas visto
nunca. Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n` (número de eventos, `n >= 1`)
- **Salida** (stdout): `eventos=<1-2-...-n>` en el orden en que llegaron
- **Regla:** por cada `i` en `1..n` se emite un evento; el callback lo recolecta

| stdin | esperado |
|---|---|
| `3` | `eventos=1-2-3` |
| `1` | `eventos=1` |
| `4` | `eventos=1-2-3-4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La función es un valor corriente: se guarda en una variable, se pasa como argumento y se invoca más
tarde. Eso —y no una API de eventos— es lo que hace posible el callback.

### Ruby

```ruby
recolectados = []
al_evento = ->(i) { recolectados << i }

n = STDIN.gets.to_i
(1..n).each { |i| al_evento.call(i) }
puts "eventos=#{recolectados.join('-')}"
```

### Perl

```perl
my @recolectados;
my $al_evento = sub { push @recolectados, $_[0] };

my $n = <STDIN>;
chomp $n;
$al_evento->($_) for 1 .. $n;
print "eventos=", join('-', @recolectados), "\n";
```

### Lua

```lua
local recolectados = {}
local function al_evento(i)
  recolectados[#recolectados + 1] = i
end

local n = tonumber(io.read("l"))
for i = 1, n do
  al_evento(i)
end
print("eventos=" .. table.concat(recolectados, "-"))
```

### Tcl

```tcl
set recolectados {}

proc al_evento {i} {
    global recolectados
    lappend recolectados $i
}

gets stdin n
for {set i 1} {$i <= $n} {incr i} {
    al_evento $i
}
puts "eventos=[join $recolectados -]"
```

### R

```r
recolectados <- integer(0)
al_evento <- function(i) recolectados <<- c(recolectados, i)

n <- as.integer(readLines("stdin", n = 1))
for (i in seq_len(n)) al_evento(i)
cat(paste0("eventos=", paste(recolectados, collapse = "-"), "\n"))
```

**Qué reconocer:** los cinco guardan el manejador en una variable, igual que la `lambda` de Python.
Ruby distingue el bloque (`{ |i| ... }`) del *lambda* como objeto, y por eso hace falta `.call`.
Perl pasa los argumentos en el array mágico `@_`. Tcl no tiene funciones-valor: el "callback" es el
**nombre** de un procedimiento, y `global` es obligatorio porque el ámbito por defecto es local.
R sí tiene clausuras, pero necesita `<<-` para escribir en el entorno de fuera: es la misma pregunta
que resuelve `nonlocal` en Python.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Aquí el paradigma no es una técnica más: el bucle de eventos **es** el modelo de ejecución.

### Dart

```dart
import 'dart:async';
import 'dart:io';

void main() async {
  final recolectados = <int>[];
  final controlador = StreamController<int>();
  controlador.stream.listen(recolectados.add);

  final n = int.parse(stdin.readLineSync()!.trim());
  for (var i = 1; i <= n; i++) {
    controlador.add(i);
  }
  await controlador.close();

  print('eventos=${recolectados.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash y no tiene stdin: n se fija en el código.
package {
    import flash.events.Event;
    import flash.events.EventDispatcher;

    public class Eventos extends EventDispatcher {
        private var recolectados:Array = [];
        private var actual:int = 0;

        public function emitir(n:int):String {
            addEventListener(Event.CHANGE, alEvento);
            for (var i:int = 1; i <= n; i++) {
                actual = i;
                dispatchEvent(new Event(Event.CHANGE));
            }
            return "eventos=" + recolectados.join("-");
        }

        private function alEvento(e:Event):void {
            recolectados.push(actual);
        }
    }
}
```

**Qué reconocer:** ActionScript 3 es el antepasado directo del DOM que ya conoces —`addEventListener`
y `dispatchEvent` se llaman igual en el navegador—, con la diferencia de que aquí el emisor **hereda**
de `EventDispatcher` en vez de recibir la capacidad por composición. Dart sube un escalón: en vez de
registrar funciones sueltas, expone el emisor como un `Stream` de primera clase con `listen`, y por
eso hace falta `await` sobre `close()` —los eventos se entregan de forma asíncrona, no dentro del
`for`—. Es el puente natural hacia la clase 120.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Java tardó hasta la versión 8 en tener
funciones como valores; sus primos nacieron ya con ellas.

### Kotlin

```kotlin
fun main() {
    val recolectados = mutableListOf<Int>()
    val alEvento: (Int) -> Unit = { recolectados.add(it) }

    val n = readLine()!!.trim().toInt()
    for (i in 1..n) alEvento(i)

    println("eventos=" + recolectados.joinToString("-"))
}
```

### Scala

```scala
import scala.collection.mutable.ListBuffer

object Eventos extends App {
  val recolectados = ListBuffer.empty[Int]
  val alEvento: Int => Unit = i => recolectados += i

  val n = scala.io.StdIn.readLine().trim.toInt
  (1 to n).foreach(alEvento)

  println(s"eventos=${recolectados.mkString("-")}")
}
```

### Groovy

```groovy
def recolectados = []
def alEvento = { i -> recolectados << i }

def n = System.in.newReader().readLine().trim() as int
(1..n).each(alEvento)

println "eventos=${recolectados.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [recolectados (atom [])
      al-evento    #(swap! recolectados conj %)
      n            (Integer/parseInt (str/trim (read-line)))]
  (doseq [i (range 1 (inc n))] (al-evento i))
  (println (str "eventos=" (str/join "-" @recolectados))))
```

**Qué reconocer:** los cuatro compilan a la misma interfaz funcional de la JVM que usa el `Consumer`
de Java, pero la escriben sin nombrarla. Kotlin declara el tipo del callback en la firma
(`(Int) -> Unit`), algo imposible en Java sin inventar una interfaz. Clojure es el que cambia de
paradigma: no muta una lista, sino que el callback es una **transición de estado** sobre un `atom`
—`swap!` aplica `conj` de forma atómica—, y esa es exactamente la diferencia que se volverá crítica
en la clase 121.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR es la plataforma donde el evento es una
palabra clave del lenguaje, no un patrón de biblioteca.

### F\#

```fsharp
open System

let recolectados = ResizeArray<int>()
let evento = Event<int>()
evento.Publish.Add(recolectados.Add)

let n = Console.ReadLine().Trim() |> int
for i in 1 .. n do
    evento.Trigger(i)

printfn "eventos=%s" (String.Join("-", recolectados))
```

### VB.NET

```vbnet
Class Emisor
    Public Event Tick(i As Integer)

    Public Sub Emitir(n As Integer)
        For i = 1 To n
            RaiseEvent Tick(i)
        Next
    End Sub
End Class

Module Programa
    Private ReadOnly recolectados As New List(Of Integer)

    Private Sub AlEvento(i As Integer)
        recolectados.Add(i)
    End Sub

    Sub Main()
        Dim emisor As New Emisor()
        AddHandler emisor.Tick, AddressOf AlEvento

        Dim n = Integer.Parse(Console.ReadLine().Trim())
        emisor.Emitir(n)

        Console.WriteLine("eventos=" & String.Join("-", recolectados))
    End Sub
End Module
```

**Qué reconocer:** VB.NET hace visible lo que C# esconde en azúcar sintáctico: `Event`, `AddHandler`
y `RaiseEvent` son tres construcciones distintas del lenguaje, y suscribirse **no** es asignar. F#
llega al mismo sitio por otro camino: su `Event<'T>` separa el canal de publicación
(`evento.Publish`, un `IObservable`) del disparador (`Trigger`), de modo que quien escucha no puede
emitir. Esa separación entre *quién publica* y *quién se suscribe* es la idea que la programación
reactiva convierte en su núcleo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin funciones anónimas, el callback es literalmente
un **puntero a función** y el estado hay que pasarlo aparte.

### C++

```cpp
#include <functional>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> recolectados;
    std::function<void(int)> al_evento = [&](int i) { recolectados.push_back(i); };

    int n = 0;
    std::cin >> n;
    for (int i = 1; i <= n; ++i) al_evento(i);

    std::string salida;
    for (std::size_t k = 0; k < recolectados.size(); ++k) {
        if (k != 0) salida += '-';
        salida += std::to_string(recolectados[k]);
    }
    std::cout << "eventos=" << salida << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSMutableArray<NSNumber *> *recolectados = [NSMutableArray array];
        void (^alEvento)(int) = ^(int i) {
            [recolectados addObject:@(i)];
        };

        int n = 0;
        scanf("%d", &n);
        for (int i = 1; i <= n; i++) alEvento(i);

        printf("eventos=%s\n", [[recolectados componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos resuelven el problema que C deja abierto —cómo lleva el callback su
contexto—. C++ lo hace con la **lista de captura** de la lambda (`[&]`), y `std::function` es la
caja que permite guardarla en una variable. Objective-C añadió los *blocks* (`^`) a la sintaxis de C
con el mismo objetivo, y por eso `recolectados` se ve dentro del bloque sin pasarla como argumento.
En C puro tendrías que inventar un parámetro `void *userdata`: eso es todo lo que estas dos
extensiones automatizan.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y sin runtime
pesado: el callback debe resolverse en tiempo de compilación o costar una indirección explícita.

### Zig

```zig
const std = @import("std");

const Recolector = struct {
    buf: [64]i32 = undefined,
    n: usize = 0,

    fn alEvento(self: *Recolector, i: i32) void {
        self.buf[self.n] = i;
        self.n += 1;
    }
};

pub fn main() !void {
    var linea: [64]u8 = undefined;
    const leido = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&linea, '\n')).?;
    const n = try std.fmt.parseInt(i32, std.mem.trim(u8, leido, " \r"), 10);

    var rec = Recolector{};
    const callback: *const fn (*Recolector, i32) void = Recolector.alEvento;
    var i: i32 = 1;
    while (i <= n) : (i += 1) callback(&rec, i);

    const out = std.io.getStdOut().writer();
    try out.writeAll("eventos=");
    for (rec.buf[0..rec.n], 0..) |v, k| {
        if (k != 0) try out.writeAll("-");
        try out.print("{d}", .{v});
    }
    try out.writeAll("\n");
}
```

### Nim

```nim
import std/[strutils, sequtils]

var recolectados: seq[int] = @[]

proc alEvento(i: int) =
  recolectados.add(i)

let n = stdin.readLine().strip().parseInt()
for i in 1 .. n:
  alEvento(i)

echo "eventos=" & recolectados.mapIt($it).join("-")
```

### D

```d
import std.algorithm, std.array, std.conv, std.stdio, std.string;

void main() {
    int[] recolectados;
    void alEvento(int i) { recolectados ~= i; }

    const n = readln().strip().to!int;
    foreach (i; 1 .. n + 1) alEvento(i);

    writefln("eventos=%s", recolectados.map!(to!string).join("-"));
}
```

**Qué reconocer:** Zig es el único que **no oculta nada**: no hay clausuras en el lenguaje, así que el estado del
manejador viaja como un `*Recolector` explícito y el callback es un puntero a función con tipo
escrito a mano. Es la misma verdad que el `void *userdata` de C, solo que con tipos. D y Nim sí
tienen funciones anidadas que capturan el ámbito de fuera —`alEvento` ve `recolectados` sin que
nadie se la pase—, y esa comodidad tiene un precio que Zig se niega a pagar por defecto: una posible
asignación en el montón para guardar el entorno capturado.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). No hay "cuando ocurra X, ejecuta Y": no hay
tiempo, ni efectos, ni orden observable.

### Prolog

```prolog
:- initialization(main, main).

% El "callback" es un objetivo que se invoca con call/N por cada evento.
emitir(N, Callback, Recolectados) :-
    numlist(1, N, Eventos),
    maplist(Callback, Eventos, Recolectados).

al_evento(I, I).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    emitir(N, al_evento, Recolectados),
    maplist(number_string, Recolectados, Textos),
    atomic_list_concat(Textos, '-', Salida),
    format("eventos=~w~n", [Salida]).
```

### Datalog

```datalog
% Datalog no tiene efectos, ni funciones de orden superior, ni "ejecutar algo cuando
% pase otra cosa". Lo más cercano a un manejador es una regla que se satisface sola
% en cuanto el hecho existe: no se "dispara", simplemente es verdad.
evento(1).
evento(2).
evento(3).

recolectado(I) :- evento(I).
```

**Qué reconocer:** Prolog sí puede pasar un manejador, porque un **objetivo es un término**: el
átomo `al_evento` se pasa como dato y `maplist` lo invoca con `call/3`. Es orden superior sin
funciones anónimas. Datalog renuncia incluso a eso: `recolectado(I) :- evento(I)` describe una
relación, no una reacción, y no existe forma de observar en qué orden se derivó. Esa es la misma
renuncia que hace SQL, y el motivo por el que el paradigma de eventos —que vive del *cuándo*— no
tiene traducción aquí.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una pregunta común: **qué se pasa como manejador y cómo lleva
su contexto**. Desde el puntero a función de Zig hasta el `Stream` de Dart hay una sola escalera, y
cada peldaño cuesta un poco de maquinaria oculta. Eso es lo transferible.

⏮️ [Volver a la clase 119](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
