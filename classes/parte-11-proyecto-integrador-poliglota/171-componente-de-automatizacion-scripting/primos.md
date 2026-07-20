# 🧬 El mismo programa en las familias de lenguajes — Clase 171

> [⬅️ Volver a la clase 171](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —procesar un lote de tareas y confirmar que se
completaron— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Perl te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `n` (número de tareas del lote)
- **Salida** (stdout): `tareas=<n> estado=completado`
- **Regla:** procesar las `n` tareas y confirmar el resultado

| stdin | esperado |
|---|---|
| `5` | `tareas=5 estado=completado` |
| `0` | `tareas=0 estado=completado` |
| `3` | `tareas=3 estado=completado` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Esta es **la clase de esta familia**. Todo lo que las demás familias hacen con esfuerzo —leer una
línea, recorrerla, invocar un programa externo, imprimir— aquí es el caso de uso para el que el
lenguaje fue diseñado.

### Ruby

```ruby
n = STDIN.gets.to_i
completadas = 0
n.times { completadas += 1 }
puts "tareas=#{completadas} estado=completado"
```

### Perl

```perl
# Perl nació exactamente para esto. En un pipeline el lote entero cabe en:
#   perl -ne 'printf "tareas=%d estado=completado\n", $_'
my $n = <STDIN>;
chomp $n;
my $completadas = 0;
$completadas++ for 1 .. $n;
printf "tareas=%d estado=completado\n", $completadas;
```

### Lua

```lua
local n = io.read("n")
local completadas = 0
for _ = 1, n do
  completadas = completadas + 1
end
print(string.format("tareas=%d estado=completado", completadas))
```

### Tcl

```tcl
gets stdin n
set completadas 0
for {set i 0} {$i < $n} {incr i} {
    incr completadas
}
puts "tareas=$completadas estado=completado"
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))
completadas <- length(seq_len(n))
cat(sprintf("tareas=%d estado=completado\n", completadas))
```

**Qué reconocer:** de todo el curso, esta es la sección donde los primos **superan** al
representante, y conviene decirlo sin nostalgia y sin exagerar. Perl fue creado en 1987 para
automatizar informes de sistema, y su integración de expresiones regulares en la sintaxis del propio
lenguaje —`if (/error/)` sin importar ninguna biblioteca—, junto con `-n`, `-p` y `-i` para envolver
el script en un bucle sobre stdin o editar archivos en el sitio, sigue sin tener rival en scripts de
una línea dentro de una tubería. Eso no lo convierte en la mejor opción para un programa de mil
líneas, que es donde Python le ganó la partida. Los otros cuatro tienen cada uno su nicho real: Ruby
es el lenguaje de Rake, Vagrant y Homebrew; Lua se **embebe** dentro de otro programa —Nginx,
Redis, Neovim, Wireshark— y automatiza desde dentro con un intérprete de unos pocos cientos de
kilobytes; Tcl es el motor de Expect, que sigue siendo la herramienta canónica para guionizar
sesiones interactivas; y R automatiza el otro tipo de tarea, la del informe reproducible que se
regenera solo. Fíjate además en el detalle de R: `seq_len(n)` en vez de `1:n` porque con `n = 0` la
segunda forma daría el vector `1 0` y ejecutaría dos veces el bucle. Es el error clásico del
lenguaje, y esta clase lo destapa con su caso `0`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  var completadas = 0;
  for (var i = 0; i < n; i++) {
    completadas++;
  }
  print('tareas=$completadas estado=completado');
}
```

### ActionScript 3

```actionscript
// El reproductor Flash es un entorno aislado: sin stdin, sin procesos hijos y
// sin sistema de archivos. La "automatización" solo ocurre dentro de la película.
package {
    public class Lote {
        public static function ejecutar(n:int):String {
            var completadas:int = 0;
            for (var i:int = 0; i < n; i++) {
                completadas++;
            }
            return "tareas=" + completadas + " estado=completado";
        }
    }
}
```

**Qué reconocer:** la familia web solo automatiza cuando sale del navegador, y esa salida tiene
nombre propio: Node.js, que le dio acceso a procesos y archivos en 2009. Antes de eso, ActionScript
—que es el mismo ECMAScript con tipos— no podía hacer nada de esto, y su bloque lo dice: la caja de
arena era el punto entero del diseño. El precio que paga la familia en automatización es el modelo
asíncrono: lanzar un comando y esperar su salida obliga a `await` o a callbacks, mientras que en
Perl o Ruby una tubería es una sola expresión síncrona.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim().toInt()
    val completadas = (1..n).count()
    println("tareas=$completadas estado=completado")
}
```

### Scala

```scala
object Lote {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val completadas = (1 to n).size
    println(s"tareas=$completadas estado=completado")
  }
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim() as int
def completadas = 0
n.times { completadas++ }
println "tareas=$completadas estado=completado"
```

### Clojure

```clojure
(let [n (Integer/parseInt (.trim (read-line)))
      completadas (count (range n))]
  (println (format "tareas=%d estado=completado" completadas)))
```

**Qué reconocer:** la JVM arrastra un problema concreto para esta clase —el arranque de la máquina
virtual cuesta cientos de milisegundos, y eso es caro para un script que se invoca mil veces en un
bucle— y cada primo lo ha atacado a su manera: Groovy es el lenguaje de Gradle y de los `Jenkinsfile`
precisamente porque hace desaparecer la ceremonia de Java, Kotlin tiene guiones `.main.kts` que se
ejecutan sin proyecto, Clojure tiene Babashka, un intérprete compilado con GraalVM que arranca en
milisegundos y está pensado justo para reemplazar a Bash. Ninguno alcanza a Perl en una tubería,
pero todos ganan cuando la tarea necesita la biblioteca de Java que ya usa el resto del sistema.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim() |> int
let completadas = Seq.length (seq { 1 .. n })
printfn "tareas=%d estado=completado" completadas
```

### VB.NET

```vbnet
Imports System

Module Lote
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim completadas = 0
        For i = 1 To n
            completadas += 1
        Next
        Console.WriteLine($"tareas={completadas} estado=completado")
    End Sub
End Module
```

**Qué reconocer:** la automatización en .NET tiene un nombre que no aparece en esta lista pero
domina la plataforma: PowerShell, que es el primo real de esta familia para esta clase. Su diferencia
con Perl es de fondo y no de sintaxis —por la tubería de PowerShell viajan **objetos** con sus
propiedades, no líneas de texto—, así que no necesita expresiones regulares para extraer un campo,
pero tampoco puede encadenarse con las herramientas Unix sin convertir a texto. F# y VB.NET sirven
para lo mismo por la vía del programa compilado; `dotnet fsi` permite además ejecutar un `.fsx` como
guion, sin proyecto ni compilación previa.

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
    int completadas = 0;
    for (int i = 0; i < n; ++i) {
        ++completadas;
    }
    std::cout << "tareas=" << completadas << " estado=completado\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        int n = 0;
        scanf("%d", &n);
        NSMutableArray<NSString *> *hechas = [NSMutableArray array];
        for (int i = 1; i <= n; i++) {
            [hechas addObject:[NSString stringWithFormat:@"tarea-%d", i]];
        }
        printf("tareas=%lu estado=completado\n", (unsigned long)hechas.count);
    }
    return 0;
}
```

**Qué reconocer:** esta familia es el lado equivocado de la clase, y la razón es el **ciclo de
edición**: un script se cambia y se vuelve a lanzar, mientras que aquí hay que compilar y enlazar
entre una versión y la siguiente. Por eso ninguna herramienta de automatización seria se escribe en
C o C++ salvo que sea el propio motor —`make`, `git`, `rsync` están en C porque se ejecutan un
millón de veces y el coste de arranque importa—. Fíjate en que Objective-C sí guarda la lista de
tareas hechas en un `NSMutableArray` y cuenta al final: es el gesto que un script haría con una
lista, escrito con la ceremonia de un lenguaje compilado.

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
    var completadas: u32 = 0;
    var i: u32 = 0;
    while (i < n) : (i += 1) {
        completadas += 1;
    }
    try std.io.getStdOut().writer().print("tareas={d} estado=completado\n", .{completadas});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip().parseInt()
var completadas = 0
for _ in 1 .. n:
  inc completadas
echo "tareas=", completadas, " estado=completado"
```

### D

```d
import std.stdio, std.string, std.conv;

void main() {
    const n = readln().strip().to!int;
    int completadas = 0;
    foreach (_; 0 .. n) {
        completadas++;
    }
    writefln("tareas=%d estado=completado", completadas);
}
```

**Qué reconocer:** esta familia le ha quitado terreno a los scripts por una razón muy concreta —el
**binario único sin dependencias**—: una herramienta de automatización en Go se copia al servidor y
funciona, sin instalar intérprete ni resolver versiones de módulos, que es el punto donde un script
de Perl o Python falla en producción. Nim y D dan la vuelta al argumento desde el otro lado: se leen
casi como un script —mira `for _ in 1 .. n` de Nim, indentación incluida— y aun así compilan a
nativo. Zig conserva el precio de la explicitud, con el búfer reservado a mano y el `try` en cada
operación que puede fallar.

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
    findall(I, between(1, N, I), Tareas),
    length(Tareas, Completadas),
    format("tareas=~d estado=completado~n", [Completadas]).
```

### Datalog

```datalog
% Datalog no tiene bucles ni efectos: "ejecutar" una tarea solo puede modelarse
% como derivar un hecho a partir de otro, y el recuento exige agregación.
pendiente(1).
pendiente(2).
pendiente(3).

completada(I) :- pendiente(I).

tareas(N) :- N = count : { completada(_) }.
```

**Qué reconocer:** aquí no hay bucle en ninguno de los dos, y esa ausencia es informativa. En Prolog
el lote se genera con `findall` sobre `between/2`, que **enumera por reevaluación** en vez de
iterar; con `n = 0` la relación `between(1, 0, I)` simplemente no tiene soluciones y la lista sale
vacía, sin caso especial. Datalog no puede ni acercarse al contrato: no tiene entrada, no tiene
salida y no tiene efectos, así que la única lectura honesta de "tarea completada" es una regla que
deriva `completada` de `pendiente`. Y sin embargo esa idea —declarar el estado deseado y dejar que
el motor decida los pasos— es exactamente la de Ansible, Terraform y `make`: las herramientas de
automatización más usadas del mundo son declarativas, no imperativas.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y la única sección del curso donde los primos brillan más que
los representantes: Perl, Ruby, Lua, Tcl y R fueron hechos para esta tarea y se nota en cada línea.
Pero el criterio no es la elegancia del guion sino la vida útil del componente: por eso el binario
único de Go y el estado declarado de Ansible le han ido comiendo terreno al script. Reconocer cuál
de los dos criterios pesa en tu caso es lo transferible.

⏮️ [Volver a la clase 171](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
