# 🧬 El mismo programa en las familias de lenguajes — Clase 147

> [⬅️ Volver a la clase 147](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si el pipeline está verde— resuelto por los
**primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes del
núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): los resultados de cada paso, `0` o `1`, separados por espacios
- **Salida** (stdout): `ci=verde` o `ci=rojo`
- **Regla:** verde si **todos** los pasos valen `1`

| stdin | esperado |
|---|---|
| `1 1 1` | `ci=verde` |
| `1 0 1` | `ci=rojo` |
| `1 1` | `ci=verde` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Son los lenguajes más baratos de meter en un pipeline: no hay paso de compilación, el runner solo
tiene que traer el intérprete y ejecutar el archivo.

### Ruby

```ruby
pasos = STDIN.read.split.map(&:to_i)
puts "ci=#{pasos.all? { |p| p == 1 } ? 'verde' : 'rojo'}"
```

### Perl

```perl
use strict;
use warnings;

my @pasos = split ' ', do { local $/; <STDIN> };
my $fallos = grep { $_ != 1 } @pasos;
printf "ci=%s\n", $fallos ? 'rojo' : 'verde';
```

### Lua

```lua
local verde = true
for token in io.read("a"):gmatch("%S+") do
  if tonumber(token) ~= 1 then verde = false end
end
print("ci=" .. (verde and "verde" or "rojo"))
```

### Tcl

```tcl
set verde 1
foreach paso [regexp -all -inline {\S+} [read stdin]] {
    if {$paso ne "1"} { set verde 0 }
}
puts "ci=[expr {$verde ? {verde} : {rojo}}]"
```

### R

```r
pasos <- scan("stdin", what = integer(), quiet = TRUE)
cat(sprintf("ci=%s\n", if (all(pasos == 1)) "verde" else "rojo"))
```

**Qué reconocer:** los cinco expresan lo mismo con un cuantificador universal —`all?`, `all`,
`every`— o con un bucle que baja una bandera. La consecuencia para CI es la misma en los cinco: el
job **no compila nada**, así que falla tarde, en tiempo de ejecución, y por eso el pipeline de un
lenguaje dinámico suele añadir un paso de linter (RuboCop, `perl -c`, `luacheck`) que haga de
sustituto barato del compilador. A cambio, el paso de instalación es trivial: basta con que la imagen
del runner traiga el intérprete de la versión correcta. R es el caso extremo del ecosistema pesado:
el intérprete es pequeño, pero las dependencias de CRAN se compilan al instalarse y son lo que hace
lento el job.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final pasos = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse);
  final verde = pasos.every((p) => p == 1);
  print('ci=${verde ? 'verde' : 'rojo'}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash: no hay stdin ni proceso de CI que lo ejecute.
// Se ilustra únicamente la regla de decisión.
package {
    public class Ci {
        public static function estado(pasos:Array):String {
            for each (var p:int in pasos) {
                if (p != 1) return "ci=rojo";
            }
            return "ci=verde";
        }
    }
}
```

**Qué reconocer:** `every` es literalmente el mismo método de `Array` que en JavaScript, y Dart
comparte con TypeScript la idea de un chequeo estático previo a la ejecución. Eso cambia el pipeline:
en JavaScript el job es *instalar dependencias y ejecutar*, mientras que en Dart y TypeScript aparece
un paso de compilación —`dart compile`, `tsc --noEmit`— que puede fallar antes de que corra una sola
prueba. ActionScript recuerda por qué un ecosistema muere: sin runtime que lo ejecute fuera del
navegador, no hay forma de meterlo en un pipeline moderno, y un lenguaje que no se puede automatizar
deja de ser mantenible.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode, así que el
runner necesita **un solo JDK** aunque el repositorio mezcle cuatro lenguajes.

### Kotlin

```kotlin
fun main() {
    val pasos = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("ci=" + if (pasos.all { it == 1 }) "verde" else "rojo")
}
```

### Scala

```scala
object Ci extends App {
  val pasos = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  println(s"ci=${if (pasos.forall(_ == 1)) "verde" else "rojo"}")
}
```

### Groovy

```groovy
def pasos = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "ci=${pasos.every { it == 1 } ? 'verde' : 'rojo'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [pasos (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "ci=" (if (every? #(= 1 %) pasos) "verde" "rojo"))))
```

**Qué reconocer:** `all`, `forall`, `every`, `every?` son cuatro nombres para el mismo cuantificador,
y los cuatro acaban en el mismo bytecode. Para la integración continua eso es una ventaja concreta:
**un único paso de instalación** —`setup-java`— sirve para los cuatro lenguajes, y la caché del job
es una sola, la del repositorio de artefactos (Maven o Gradle). El precio es el arranque: cada
ejecución paga el calentamiento de la JVM, por eso los pipelines de la familia agrupan todas las
pruebas en una sola invocación en lugar de lanzar un proceso por caso.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let pasos =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
    |> Array.map int

printfn "ci=%s" (if Array.forall ((=) 1) pasos then "verde" else "rojo")
```

### VB.NET

```vbnet
Imports System
Imports System.Linq

Module Ci
    Sub Main()
        Dim pasos = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Dim verde = pasos.All(Function(p) p = "1")
        Console.WriteLine("ci=" & If(verde, "verde", "rojo"))
    End Sub
End Module
```

**Qué reconocer:** `Array.forall` de F# y `.All(...)` de LINQ en VB.NET son la misma operación sobre
el mismo CLR, y por eso el pipeline es idéntico para los tres lenguajes de la familia: `dotnet
restore`, `dotnet build`, `dotnet test`, sin importar en cuál esté escrito cada proyecto de la
solución. El SDK de .NET es una única instalación que cubre compilador, gestor de paquetes y
ejecutor de pruebas —donde el mundo JavaScript necesita tres herramientas distintas—, y esa
integración es justamente lo que hace que sus workflows sean tan cortos.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el job de CI ya no solo ejecuta: **compila**, y
el binario resultante sirve solo para el sistema operativo del runner.

### C++

```cpp
#include <iostream>

int main() {
    int paso;
    bool verde = true;
    while (std::cin >> paso) {
        if (paso != 1) verde = false;
    }
    std::cout << "ci=" << (verde ? "verde" : "rojo") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *datos = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:datos encoding:NSUTF8StringEncoding];
        NSCharacterSet *espacios = [NSCharacterSet whitespaceAndNewlineCharacterSet];
        BOOL verde = YES;
        for (NSString *paso in [linea componentsSeparatedByCharactersInSet:espacios]) {
            if (paso.length > 0 && ![paso isEqualToString:@"1"]) verde = NO;
        }
        printf("ci=%s\n", verde ? "verde" : "rojo");
    }
    return 0;
}
```

**Qué reconocer:** ambos son superconjuntos de C y el bucle de la clase compila casi tal cual en los
dos. La diferencia que importa para CI es la **matriz**: como el artefacto es un binario nativo, el
workflow necesita un job por combinación de sistema operativo, arquitectura y compilador
(`gcc`/`clang`/MSVC), y esa matriz se multiplica sola. Objective-C añade una restricción más dura:
depende de Foundation, así que en la práctica su job **solo corre sobre un runner macOS**, que es más
caro y más escaso que uno Linux. Un lenguaje puede condicionar la factura del pipeline tanto como su
sintaxis.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con toolchains modernos que traen compilador, formateador y ejecutor de pruebas en un solo
binario.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \r\t");
    var verde = true;
    while (it.next()) |paso| {
        if (!std.mem.eql(u8, paso, "1")) verde = false;
    }
    try std.io.getStdOut().writer().print("ci={s}\n", .{if (verde) "verde" else "rojo"});
}
```

### Nim

```nim
import std/[strutils, sequtils]

let pasos = stdin.readLine().splitWhitespace()
echo "ci=" & (if pasos.allIt(it == "1"): "verde" else: "rojo")
```

### D

```d
import std.stdio, std.array, std.algorithm, std.conv, std.string;

void main() {
    auto pasos = readln().strip().split().map!(to!int);
    writeln("ci=", pasos.all!(p => p == 1) ? "verde" : "rojo");
}
```

**Qué reconocer:** los tres compilan a binario nativo, igual que Go y Rust, y por tanto heredan la
misma matriz de plataformas de la familia C. **Zig es la excepción interesante**: su compilador trae
la biblioteca estándar de C para todos los objetivos, así que `zig build-exe -target
x86_64-windows` funciona desde un runner Linux sin instalar nada más. Eso convierte una matriz de
tres o cuatro jobs en **un solo job que produce todos los binarios**, y es un argumento de ingeniería
real —no una curiosidad— cuando el pipeline se paga por minuto. Nim y D siguen el camino clásico:
compilan rápido y con sintaxis de scripting, pero necesitan un runner por sistema operativo de
destino.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** condición debe cumplirse, no
cómo recorrer los pasos para comprobarla.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Bruto),
    exclude(==(""), Bruto, Pasos),
    (   forall(member(P, Pasos), P == "1")
    ->  Estado = verde
    ;   Estado = rojo
    ),
    format("ci=~w~n", [Estado]).
```

### Datalog

```datalog
% Datalog no tiene entrada/salida: los pasos del pipeline se declaran como hechos
% y el estado se deriva por negación estratificada.
paso(1, 1).
paso(2, 0).
paso(3, 1).

rojo :- paso(_, R), R != 1.
verde :- not rojo.
```

**Qué reconocer:** `forall` de Prolog es el cuantificador universal escrito tal cual, sin bucle ni
acumulador, y es exactamente lo que hace el `min(x) = 1` de la versión SQL: comprobar una propiedad
sobre un conjunto entero. Datalog no puede leer stdin, así que no hay programa que un pipeline pueda
invocar; lo que sí ilustra es la forma canónica de la regla de CI —**verde es la ausencia de un paso
rojo**—, que es cómo lo modela internamente cualquier sistema de integración continua: no busca el
éxito, busca el primer fallo.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer los pasos y comprobar una
propiedad universal. Lo que cambia no es tanto el código como **lo que el pipeline tiene que instalar
para ejecutarlo**: un intérprete, una máquina virtual o una matriz de compiladores. Eso es lo
transferible.

⏮️ [Volver a la clase 147](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
