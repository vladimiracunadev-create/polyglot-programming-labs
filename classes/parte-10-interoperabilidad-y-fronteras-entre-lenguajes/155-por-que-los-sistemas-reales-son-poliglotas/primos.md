# 🧬 El mismo programa en las familias de lenguajes — Clase 155

> [⬅️ Volver a la clase 155](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —contar los componentes de un sistema— resuelto por
los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los diez lenguajes
del núcleo.

Y aquí la lista de primos deja de ser un ejercicio de estilo: la clase pregunta *por qué* los
sistemas reales son políglotas, y la respuesta está en esta misma página. Ninguna de estas veinte
comunidades apareció por capricho; cada una resolvió bien un problema que las otras resolvían mal, y
por eso sobrevivió dentro de sistemas que ya hablaban otro idioma.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): los nombres de los componentes, separados por espacios
- **Salida** (stdout): `componentes=<cantidad>`
- **Regla:** contar cuántos componentes tiene el sistema

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3` |
| `app` | `componentes=1` |
| `web api datos cache` | `componentes=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
En un sistema real esta familia ocupa el pegamento: scripts de despliegue, tareas de datos,
administración. Nadie eligió PHP para el núcleo de un motor de base de datos, ni C para una plantilla
web, y de esa división del trabajo nace el poliglotismo.

### Ruby

```ruby
componentes = STDIN.gets.split
puts "componentes=#{componentes.size}"
```

### Perl

```perl
my @componentes = split ' ', <STDIN>;
printf "componentes=%d\n", scalar @componentes;
```

### Lua

```lua
local n = 0
for _ in io.read("l"):gmatch("%S+") do n = n + 1 end
print("componentes=" .. n)
```

### Tcl

```tcl
gets stdin linea
puts "componentes=[llength $linea]"
```

### R

```r
partes <- strsplit(trimws(readLines("stdin", n = 1)), "\\s+")[[1]]
cat(sprintf("componentes=%d\n", length(partes)))
```

**Qué reconocer:** los cinco parten la línea sin declarar tipos y preguntan por el tamaño de la
lista resultante. Pero fíjate en para qué existe cada uno dentro de un sistema mayor: Perl vive en
los scripts que pegan procesos de Unix, R vive en el componente que analiza datos —y por eso trata
la línea como un **vector**—, y Lua y Tcl ni siquiera aspiran a ser el programa principal: están
diseñados para ser **incrustados** dentro de un ejecutable en C que ya existe. Ese detalle es la
clase entera: hay lenguajes cuya razón de ser es convivir con otro.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia que ocupa, casi siempre, el componente de interfaz —y que en un sistema políglota está
obligada a hablar con un servidor escrito en otra cosa.

### Dart

```dart
import 'dart:io';

void main() {
  final componentes = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  print('componentes=${componentes.length}');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash, sin stdin: se ilustra el conteo.
package {
    public class Sistema {
        public static function componentes(linea:String):String {
            return "componentes=" + linea.split(/\s+/).length;
        }
    }
}
```

**Qué reconocer:** los dos comparten el ancestro ECMAScript, y por eso `split` y `length` se
escriben igual. ActionScript es además el mejor recordatorio de por qué un sistema políglota es
también un sistema **mortal**: era el lenguaje de un componente —el reproductor Flash— que
desapareció, y todo lo escrito dentro de él se fue con la frontera. Elegir un lenguaje por
componente reparte el riesgo, pero no lo elimina.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El caso más puro de sistema políglota **dentro
de un solo proceso**: cuatro lenguajes distintos compilando al mismo bytecode y llamándose entre sí
sin frontera alguna.

### Kotlin

```kotlin
fun main() {
    val componentes = readLine()!!.trim().split(Regex("\\s+"))
    println("componentes=${componentes.size}")
}
```

### Scala

```scala
object Sistema extends App {
  val componentes = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"componentes=${componentes.length}")
}
```

### Groovy

```groovy
def componentes = System.in.newReader().readLine().trim().split(/\s+/)
println "componentes=${componentes.size()}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [componentes (str/split (str/trim (read-line)) #"\s+")]
  (println (str "componentes=" (count componentes))))
```

**Qué reconocer:** los cuatro usan el mismo `String.split` de Java, porque comparten biblioteca
estándar. Esta es la interoperabilidad **barata**: un proyecto real mezcla Java para el dominio,
Kotlin para el código nuevo y Groovy para los scripts de construcción sin serializar nada ni cruzar
un proceso. Compáralo con lo que costará, en las clases siguientes, hablar con C: aquí la frontera
simplemente no existe porque todos aceptaron una **plataforma común** por adelantado.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). La otra plataforma común, con la misma apuesta:
varios lenguajes, un solo CLR, un solo sistema de tipos.

### F\#

```fsharp
let componentes =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)
printfn "componentes=%d" componentes.Length
```

### VB.NET

```vbnet
Module Sistema
    Sub Main()
        Dim componentes = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("componentes=" & componentes.Length)
    End Sub
End Module
```

**Qué reconocer:** ambos llaman a `String.Split` y a `StringSplitOptions`, tipos de la misma
biblioteca base que usa C#. .NET nació explícitamente **multilenguaje** —la CLI es un estándar
pensado para que VB, C# y F# compartan ensamblados—, y eso convierte a la plataforma en la unidad de
decisión: el equipo elige .NET, y luego cada componente elige su lenguaje dentro. Es la misma
estrategia de la JVM con otro dueño.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). El componente que casi nunca se reescribe: el
códec, el motor criptográfico, el driver, la base de datos.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string palabra;
    int n = 0;
    while (std::cin >> palabra) ++n;
    std::cout << "componentes=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSString *linea = [[NSString alloc] initWithData:[[NSFileHandle fileHandleWithStandardInput] availableData]
                                                encoding:NSUTF8StringEncoding];
        NSArray<NSString *> *partes = [[linea stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]]
                                       componentsSeparatedByString:@" "];
        printf("componentes=%lu\n", (unsigned long)partes.count);
    }
    return 0;
}
```

**Qué reconocer:** los dos son **superconjuntos de C**, y esa herencia es la razón por la que esta
familia es el suelo sobre el que se apoyan las demás. Casi todo sistema políglota tiene una capa en
C que nadie toca porque funciona y porque **todos los demás saben llamarla** —ese será el asunto de
las clases 156, 157 y 158—. Objective-C enseña además la variante Apple del poliglotismo: C puro
para el cálculo y objetos con `NSString` para la capa de aplicación, en el mismo archivo.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los lenguajes con los que
hoy se reescriben, componente a componente, las partes críticas de sistemas que antes eran solo C.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    var n: usize = 0;
    while (it.next()) |_| n += 1;
    try std.io.getStdOut().writer().print("componentes={d}\n", .{n});
}
```

### Nim

```nim
import std/strutils

let componentes = stdin.readLine().splitWhitespace()
echo "componentes=", componentes.len
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto componentes = readln().strip().split();
    writefln("componentes=%d", componentes.length);
}
```

**Qué reconocer:** los tres cuentan sin reservar memoria dinámica innecesaria —Zig hasta declara el
búfer a mano—, y los tres compilan a un binario nativo. Su papel en un sistema políglota es el de
**sustituto quirúrgico**: se cambia el componente lento por uno de estos y el resto del sistema no se
entera, siempre que el nuevo respete la frontera que el viejo ofrecía. Zig y D lo hacen tan explícito
que pueden compilar C y hablar su ABI directamente, cosa que veremos enseguida.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El componente que casi ningún sistema real
sustituye: la consulta declarativa sobre datos.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes),
    exclude(==(""), Partes, Componentes),
    length(Componentes, N),
    format("componentes=~d~n", [N]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S: los componentes se declaran como hechos y el
% recuento se obtiene con una agregación (extensión de Soufflé, no del núcleo).
componente("cli").
componente("api").
componente("web").

total(N) :- N = count : { componente(_) }.
```

**Qué reconocer:** ninguno de los dos describe **cómo** contar; declaran los hechos y dejan que el
motor decida. Esa renuncia es exactamente la razón por la que SQL sobrevive dentro de sistemas cuyo
código de aplicación se ha reescrito tres veces: el lenguaje declarativo sobrevive al imperativo
porque no promete un procedimiento, promete un resultado. Datalog es el caso extremo —sin E/S ni
efectos, no puede ser un componente autónomo, solo el motor de inferencia dentro de otro—.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y sin embargo veinte nichos distintos: el que se incrusta, el que
analiza datos, el que compila al bytecode ajeno, el que nadie reescribe, el que solo declara. Un
sistema real es políglota porque **ninguno de ellos gana en todo**, y la ingeniería consiste en
poner cada uno donde gana y diseñar bien la frontera entre ellos.

⏮️ [Volver a la clase 155](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
