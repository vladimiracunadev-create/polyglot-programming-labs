# 🧬 El mismo programa en las familias de lenguajes — Clase 131

> [⬅️ Volver a la clase 131](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —crear objetos temporales y comprobar que la memoria
se recupera— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí el reconocimiento tiene un premio extra: el programa es casi idéntico en los veinte lenguajes,
pero **lo que pasa por debajo es distinto en cada uno**. Ese contraste es la clase.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, el número de objetos temporales a crear
- **Salida** (stdout): `creados=<n> estado=recolectado`
- **Regla:** crear `n` objetos temporales; al perder la última referencia, la memoria se recupera

| stdin | esperado |
|---|---|
| `5` | `creados=5 estado=recolectado` |
| `0` | `creados=0 estado=recolectado` |
| `3` | `creados=3 estado=recolectado` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python cuenta referencias y añade un detector de ciclos; PHP hace lo mismo. La familia entera
comparte el gesto de no liberar nada a mano, pero **no comparte el mecanismo**.

### Ruby

```ruby
n = STDIN.read.strip.to_i
n.times { Object.new }   # sin referencia viva: basura para el marcado y barrido
GC.start                 # generacional desde 2.1, incremental desde 2.2
puts "creados=#{n} estado=recolectado"
```

### Perl

```perl
my $n = <STDIN>;
chomp $n;
for (1 .. $n) {
    my $tmp = {};   # el contador cae a 0 al salir del bloque: liberado en el acto
}
# Perl NO recolecta ciclos: $a->{b} = $a nunca se libera sin Scalar::Util::weaken.
printf "creados=%d estado=recolectado\n", $n;
```

### Lua

```lua
local n = tonumber(io.read("l"))
for _ = 1, n do
  local tmp = {}   -- tabla temporal: basura en cuanto se reasigna
end
collectgarbage("collect")   -- 5.4: incremental por defecto, generacional opcional
print(string.format("creados=%d estado=recolectado", n))
```

### Tcl

```tcl
gets stdin n
for {set i 0} {$i < $n} {incr i} {
    set tmp [list $i]   ;# cada Tcl_Obj lleva su propio contador de referencias
}
unset -nocomplain tmp
puts "creados=$n estado=recolectado"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
for (i in seq_len(n)) {
  tmp <- new.env()   # entorno temporal: basura en cuanto se reasigna
}
invisible(gc())      # marcado y barrido generacional, sin compactar
cat(sprintf("creados=%d estado=recolectado\n", n))
```

**Qué reconocer:** los cinco escriben el mismo bucle, pero **cada uno tiene un recolector
distinto**. Ruby y R **rastrean**: recorren el grafo de objetos vivos y barren el resto, con
generaciones para no revisar entero el montón en cada pasada. Perl y Tcl **cuentan referencias**:
liberan en el instante exacto en que el contador llega a cero —de ahí que no necesiten ningún
`GC.start`— pero **no liberan ciclos**, y en Perl eso es una fuga real que se rompe a mano con
`weaken`. Lua está en medio: marcado **incremental** desde 5.1, con un modo **generacional** añadido
en 5.4 que se activa con `collectgarbage("generational")`. Fíjate en quién ofrece un botón para
forzar la recolección: solo los que rastrean, porque los que cuentan no tienen nada que forzar.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
V8 usa un *scavenger* generacional para los objetos jóvenes y un marcado y compactado concurrente
para los viejos.

### Dart

```dart
import 'dart:io';

class Temporal {}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  for (var i = 0; i < n; i++) {
    Temporal(); // nace en el espacio joven; el scavenger lo recoge sin tocar el resto
  }
  print('creados=$n estado=recolectado');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en la AVM2 del reproductor Flash: no hay stdin.
// Su recolector combina conteo de referencias diferido con marcado y barrido,
// justo para poder reclamar los ciclos que el conteo por sí solo deja vivos.
package {
    public class Temporales {
        public static function crear(n:int):String {
            for (var i:int = 0; i < n; i++) {
                var tmp:Object = new Object();
                tmp = null; // sin referencias: candidato a recolección
            }
            return "creados=" + n + " estado=recolectado";
        }
    }
}
```

**Qué reconocer:** Dart y V8 comparten la apuesta generacional —la hipótesis de que casi todo objeto
muere joven— y por eso crear millones de temporales es barato en los dos. ActionScript enseña la
solución intermedia clásica: conteo de referencias para la mayoría de los casos **más** un marcado
periódico que rescata los ciclos, exactamente el problema que Perl decide no resolver. Ninguno de
los tres expone una llamada para liberar un objeto concreto: en esta familia la memoria no es un
recurso que el programador nombre.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Los cuatro comparten el **mismo** recolector,
porque el recolector no es del lenguaje sino de la máquina virtual.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    repeat(n) { Any() }   // objetos jóvenes: mueren en las regiones Eden que recoge G1
    println("creados=$n estado=recolectado")
}
```

### Scala

```scala
object Basura {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    for (_ <- 1 to n) new AnyRef // el mismo GC de la JVM que usa Java
    println(s"creados=$n estado=recolectado")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim().toInteger()
n.times { new Object() }
System.gc()   // sugerencia, no orden: la JVM decide si hace algo
println "creados=$n estado=recolectado"
```

### Clojure

```clojure
(let [n (Integer/parseInt (.trim (read-line)))]
  (dotimes [_ n] (Object.))
  (println (format "creados=%d estado=recolectado" n)))
```

**Qué reconocer:** cambiar de lenguaje aquí **no cambia el recolector**. Los cuatro corren sobre
G1 si usas una JDK 9 o posterior sin configurar nada, y los cuatro pueden pasar a **ZGC** o
**Shenandoah** con un `-XX:+UseZGC` en la línea de arranque, sin tocar una línea de código: son
recolectores de pausa casi constante pensados para montones de decenas de gigabytes. `System.gc()`
es una **sugerencia**, no una orden, y con ZGC puede ignorarse del todo. Clojure es el caso
interesante: sus estructuras persistentes generan muchísima basura joven de vida cortísima, y eso
—que en un recolector no generacional sería carísimo— es precisamente el caso que el diseño
generacional de la JVM optimiza.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Recolector generacional de tres niveles, con un
montón aparte para los objetos grandes.

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
for _ in 1 .. n do
    obj () |> ignore   // asignado en la generación 0 del recolector del CLR
printfn "creados=%d estado=recolectado" n
```

### VB.NET

```vbnet
Imports System

Module Basura
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.In.ReadToEnd().Trim())
        For i As Integer = 1 To n
            Dim tmp As New Object()   ' generación 0: la más barata de recolectar
        Next
        Console.WriteLine("creados=" & n & " estado=recolectado")
    End Sub
End Module
```

**Qué reconocer:** los tres lenguajes comparten el recolector del CLR, que es **generacional** con
tres generaciones —0, 1 y 2— y promueve lo que sobrevive. Lo específico de .NET es el **montón de
objetos grandes** (LOH): todo lo que supera unos 85.000 bytes se asigna en un montón separado que,
por defecto, **no se compacta**, así que un programa que crea y suelta arreglos grandes puede
fragmentar la memoria sin tener ninguna fuga. Ese detalle no se ve en el código —es idéntico en F#,
VB.NET y C#— pero es la diferencia práctica frente a la JVM, que sí compacta con G1.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Sin recolector: cada `malloc` tiene su `free`.

### C++

```cpp
#include <iostream>
#include <memory>

struct Temporal {};

int main() {
    long long n = 0;
    std::cin >> n;
    for (long long i = 0; i < n; ++i) {
        auto tmp = std::make_unique<Temporal>(); // destruido al cerrar la llave
    }
    // C++ no tiene recolector: la liberación es determinista, no diferida.
    std::cout << "creados=" << n << " estado=recolectado\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        long long n = 0;
        scanf("%lld", &n);
        for (long long i = 0; i < n; i++) {
            @autoreleasepool {
                NSObject *tmp = [NSObject new]; // ARC libera al llegar el contador a 0
                (void)tmp;
            }
        }
        printf("creados=%lld estado=recolectado\n", n);
    }
    return 0;
}
```

**Qué reconocer:** aquí la palabra "recolectado" significa otra cosa. C++ **no tiene recolector en
absoluto**: `make_unique` libera en el destructor, en un punto del programa que puedes señalar con
el dedo. Objective-C tuvo un recolector rastreador de verdad y **lo retiró** en OS X 10.8; hoy usa
**ARC**, que no es magia en tiempo de ejecución sino el compilador insertando `retain` y `release`
por ti: conteo de referencias, con la misma consecuencia que en Perl —**los ciclos no se liberan**—
y la misma cura, marcar una de las dos referencias como `__weak`. Los `@autoreleasepool` anidados
son la otra pieza: sin el interior, los temporales se acumularían hasta el final del bucle.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go recolecta con un
marcado tricolor concurrente; Rust no recolecta en absoluto.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(u64, std.mem.trim(u8, linea, " \r\t"), 10);

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit(); // al cerrar, avisa de la memoria que no se liberó
    const alloc = gpa.allocator();

    var i: u64 = 0;
    while (i < n) : (i += 1) {
        const tmp = try alloc.create(u32); // Zig no tiene recolector NI asignador oculto
        alloc.destroy(tmp);
    }
    try std.io.getStdOut().writer().print("creados={d} estado=recolectado\n", .{n});
}
```

### Nim

```nim
import std/strutils

type Temporal = ref object
  valor: int

let n = stdin.readLine().strip().parseInt()
for i in 1 .. n:
  let tmp = Temporal(valor: i)   # ORC: conteo de referencias + detector de ciclos
  discard tmp
echo "creados=", n, " estado=recolectado"
```

### D

```d
import std.stdio, std.string, std.conv;
import core.memory : GC;

class Temporal {}

void main() {
    const n = readln().strip().to!long;
    foreach (_; 0 .. n) {
        auto tmp = new Temporal(); // `new` asigna en el montón del recolector de D
    }
    GC.collect();                  // marcado y barrido, aquí y ahora
    writefln("creados=%d estado=recolectado", n);
}
```

**Qué reconocer:** esta familia es la que más se separa por dentro. Zig no solo carece de
recolector: carece de **asignador por defecto**, y por eso el programa tiene que nombrar uno y
pasarlo —el `GeneralPurposeAllocator` incluso te delata las fugas al cerrar—. Nim usa **ORC**, que
es conteo de referencias calculado en tiempo de compilación (`--mm:arc`) más un ciclo de rescate
para las referencias circulares (`--mm:orc`): sin pausas de recolección, pero con el coste repartido
en cada asignación. D es el único de los tres con un recolector rastreador clásico… y también el
único que te deja **apagarlo**: marcar una función `@nogc` hace que el compilador rechace cualquier
operación que pudiera asignar en el montón del recolector. Tres respuestas distintas a la misma
pregunta de la clase.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere; quién reserva y
libera la memoria es asunto del motor.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    forall(between(1, N, I), atom_concat(tmp_, I, _)),
    garbage_collect,   % recolecta las pilas global y de rastro; los átomos van aparte
    format("creados=~d estado=recolectado~n", [N]).
```

### Datalog

```datalog
% Datalog no asigna memoria dinámica ni tiene E/S: no hay nada que recolectar,
% porque no hay objetos ni identidad, solo hechos derivados de otros hechos.
creados(5).

estado(N, recolectado) :- creados(N).
```

**Qué reconocer:** en Prolog buena parte de la memoria se recupera **sin recolector**: al fallar y
retroceder, el motor deshace las ligaduras y devuelve la pila al punto anterior, un mecanismo que no
existe en ninguna de las familias anteriores. Lo que sí necesita recolección es la pila global —de
ahí `garbage_collect/0`— y, en SWI, los **átomos**, que llevan su propio recolector separado porque
viven en una tabla global. Datalog lleva la renuncia al extremo: sin efectos, sin identidad de
objeto y sin E/S, la pregunta "¿cuándo se libera esto?" simplemente no se puede formular, igual que
SQL no te deja preguntar cuándo se descarta una fila intermedia de un `JOIN`.

---

## Y de vuelta a la clase

Veinte lenguajes, un bucle de cuatro líneas, y por debajo **siete estrategias distintas**: marcado y
barrido generacional, marcado incremental, conteo de referencias puro, conteo con rescate de ciclos,
destrucción determinista por ámbito, liberación manual con asignador explícito y retroceso lógico.
Lo transferible no es el bucle: es saber, ante un lenguaje nuevo, qué pregunta hacerle a su memoria.

⏮️ [Volver a la clase 131](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
