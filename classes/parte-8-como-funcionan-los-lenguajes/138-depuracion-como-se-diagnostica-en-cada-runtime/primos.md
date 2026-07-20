# 🧬 El mismo programa en las familias de lenguajes — Clase 138

> [⬅️ Volver a la clase 138](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —inspeccionar un valor mostrando el número, su
cuadrado y su cubo— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El cálculo es trivial a propósito: lo que se compara aquí no es la aritmética sino **con qué se
mira** un programa vivo en cada runtime. Y ahí no hay nada universal. Unos traen el depurador dentro
del intérprete (`perl -d`), otros solo dan el gancho para construirlo (`debug.sethook` de Lua), los
compilados delegan en `gdb`/`lldb` con información que el compilador tiene que emitir aparte, y las
máquinas virtuales —JVM y CLR— depuran por protocolo, igual para todos sus lenguajes. Cada bloque
lleva en un comentario la herramienta real con la que esa comunidad diagnostica.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `valor=<n> cuadrado=<n²> cubo=<n³>`
- **Regla:** inspeccionar `n`, `n²` y `n³`, como al examinar variables en un depurador

| stdin | esperado |
|---|---|
| `3` | `valor=3 cuadrado=9 cubo=27` |
| `2` | `valor=2 cuadrado=4 cubo=8` |
| `5` | `valor=5 cuadrado=25 cubo=125` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Como el intérprete está presente mientras el programa corre, aquí el depurador puede ser una
biblioteca más: se importa, se llama y abre una consola con el estado vivo. Ninguno necesita un
proceso externo ni un formato de símbolos.

### Ruby

```ruby
# `debug` entró en la biblioteca estándar en Ruby 3.1 y sustituyó a `byebug`:
# `require "debug"; binding.break` detiene aquí y abre una consola con TODO el
# binding vivo, donde se pueden llamar métodos sobre los objetos del momento.
n = STDIN.gets.to_i
puts "valor=#{n} cuadrado=#{n * n} cubo=#{n * n * n}"
```

### Perl

```perl
use strict;
use warnings;

# `perl -d programa.pl` arranca el depurador que viene CON el intérprete, sin
# instalar nada: `n` avanza una línea, `x $n` vuelca la estructura completa de
# un valor y `T` imprime la traza de llamadas con sus argumentos.
chomp(my $n = <STDIN>);
printf "valor=%d cuadrado=%d cubo=%d\n", $n, $n * $n, $n * $n * $n;
```

### Lua

```lua
-- Lua no trae depurador: trae el GANCHO con el que se construyen.
-- `debug.sethook(f, "l")` llama a `f` en cada línea ejecutada, y
-- `debug.traceback()` devuelve la pila como cadena. Todo depurador de Lua
-- —incluido el de los motores de juego— está escrito sobre esa API.
local n = math.tointeger(tonumber(io.read("l")))
print(string.format("valor=%d cuadrado=%d cubo=%d", n, n * n, n * n * n))
```

### Tcl

```tcl
# Tcl se instrumenta desde el propio lenguaje: `trace add variable n write ...`
# dispara un manejador cada vez que se escribe la variable, y `trace add
# execution` hace lo mismo con las llamadas. Es depuración sin depurador.
set n [string trim [gets stdin]]
puts "valor=$n cuadrado=[expr {$n * $n}] cubo=[expr {$n * $n * $n}]"
```

### R

```r
# `browser()` puesto en cualquier línea abre una consola de R con el entorno
# vivo. Y `traceback()` es imprescindible porque R NO imprime la pila cuando
# algo falla: solo el mensaje. Hay que pedirla explícitamente después del error.
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("valor=%d cuadrado=%d cubo=%d\n", n, n * n, n * n * n))
```

**Qué reconocer:** los cinco comparten que el depurador vive **dentro** del proceso, pero se separan
en cuánto te dan hecho. Perl es el extremo generoso: el depurador es parte del intérprete y se activa
con una bandera. Ruby lo movió a la estándar (`debug` desde 3.1, antes la gema `byebug`), así que
también viene de serie. Lua es el extremo opuesto y el más instructivo: no ofrece un depurador sino
`debug.sethook`, la primitiva sobre la que otros lo escriben — coherente con un lenguaje diseñado
para empotrarse, donde el anfitrión decide qué herramientas quiere. Tcl ni siquiera necesita una API
de depuración aparte, porque `trace` es una construcción normal del lenguaje. Y R merece un aviso
práctico: es el único de los cinco que **no imprime traza de pila por defecto**, así que un error en
R sin `traceback()` te deja sin saber quién llamó a quién.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La familia web inventó la idea de depurar **por protocolo sobre un socket**: el depurador no está en
el proceso, se conecta a él. Eso es lo que hoy llamamos Chrome DevTools Protocol.

### Dart

```dart
import 'dart:io';

// `dart run --observe` abre el VM Service en un puerto, y DevTools se conecta a
// ese puerto para depurar el proceso que ya está corriendo. `debugger()` de
// `dart:developer` pausa desde el código si hay un depurador enganchado, y no
// hace nada si no lo hay.
void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('valor=$n cuadrado=${n * n} cubo=${n * n * n}');
}
```

### ActionScript 3

```actionscript
// El depurador de ActionScript es externo (`fdb`, o el reproductor de
// depuración) y solo funciona con SWF compilados con `-debug`. El lenguaje no
// tiene stdin: la entrada llega por otra vía y aquí se ilustra solo el cálculo.
package {
    public class Inspector {
        public static function inspeccionar(n:int):String {
            return "valor=" + n + " cuadrado=" + (n * n) + " cubo=" + (n * n * n);
        }
    }
}
```

**Qué reconocer:** los dos separan el depurador del programa y los unen por un canal, y esa decisión
tiene una consecuencia que se nota a diario: puedes depurar algo que ya está corriendo, incluso en
otra máquina. Dart lo hace explícito con el VM Service; ActionScript lo hacía con un reproductor de
depuración distinto del de producción, y ahí está su diferencia importante — el binario que se
depura **no es el mismo** que se publica, porque hay que compilar con `-debug`. Esa distinción entre
build de depuración y build de entrega la volveremos a ver en la familia de sistemas, y es lo
contrario de lo que ocurre en scripting, donde solo hay un artefacto.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Aquí el depurador no pertenece al lenguaje sino
a la **máquina**: JDWP es un protocolo de la JVM, y sirve igual para los cuatro primos de abajo.

### Kotlin

```kotlin
fun main() {
    // Toda la JVM se depura con el mismo protocolo, JDWP: se arranca con
    // `-agentlib:jdwp=transport=dt_socket,server=y,address=5005` y se conecta
    // `jdb` o el IDE. Kotlin no aporta depurador propio: hereda el de la máquina.
    val n = readLine()!!.trim().toInt()
    println("valor=$n cuadrado=${n * n} cubo=${n * n * n}")
}
```

### Scala

```scala
object Inspeccion extends App {
  // La traza que ves no es la de tu código: el compilador genera clases y
  // métodos sintéticos (`$anonfun$...`, `$lzycompute`) y la pila los muestra
  // tal cual. Depurar Scala es leer, en parte, lo que el compilador escribió.
  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"valor=$n cuadrado=${n * n} cubo=${n * n * n}")
}
```

### Groovy

```groovy
// El despacho dinámico de Groovy mete sus propios marcos en la pila: una traza
// real viene llena de `MetaClassImpl` y `CallSite` entre tus llamadas. Groovy
// las filtra al imprimir la excepción; `-Dgroovy.full.stacktrace=true` las deja.
def n = System.in.newReader().readLine().trim() as int
println "valor=$n cuadrado=${n * n} cubo=${n * n * n}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; En Clojure el REPL ES el depurador: se conecta a un proceso vivo (nREPL),
;; se redefine una función y se vuelve a probar sin reiniciar nada.
;; `clojure.repl/pst` imprime la pila de la última excepción ya despejada.
(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "valor=" n " cuadrado=" (* n n) " cubo=" (* n n n))))
```

**Qué reconocer:** cuatro lenguajes y **un solo depurador**, porque el depurador es de la JVM. Esa es
la ventaja plataforma en su forma más pura: quien sabe usar `jdb` sabe depurar Groovy sin haber
escrito Groovy. El precio aparece en la traza de pila, que es la de la máquina y no la del lenguaje:
Scala te muestra sus clases sintéticas, Groovy sus marcos de despacho dinámico, y en los dos casos
tienes que aprender a saltarte líneas que tú no escribiste. Clojure elige otra vía dentro de la misma
casa: en lugar de pausar y avanzar, mantiene un proceso vivo al que se le reemplazan funciones desde
el REPL. Es depuración por **redefinición**, no por interrupción, y explica por qué la comunidad
Clojure usa el depurador de pasos mucho menos que el resto de la JVM.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR repite el patrón de la JVM: el depurador es
de la plataforma (ICorDebug) y lo comparten todos sus lenguajes.

### F\#

```fsharp
// El CLR se depura con ICorDebug, y las herramientas de diagnóstico
// —`dotnet-dump`, `dotnet-trace`, `dotnet-counters`— hablan con cualquier
// lenguaje .NET por igual. En F# la pila muestra también funciones internas
// generadas por el compilador para clausuras y currificación.
let n = int (stdin.ReadLine().Trim())
printfn "valor=%d cuadrado=%d cubo=%d" n (n * n) (n * n * n)
```

### VB.NET

```vbnet
Module Inspeccion
    Sub Main()
        ' `Debug.WriteLine` solo emite en compilaciones DEBUG: en Release la
        ' llamada desaparece del binario, porque está marcada con
        ' `<Conditional("DEBUG")>`. Es diagnóstico que existe o no según el build.
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine($"valor={n} cuadrado={n * n} cubo={n * n * n}")
    End Sub
End Module
```

**Qué reconocer:** lo que aporta .NET frente a la JVM es que el **compilador participa** en el
diagnóstico. `Debug.WriteLine` no se ignora en Release: la llamada entera se elimina del código
generado gracias al atributo `Conditional`, así que el coste en producción es literalmente cero. La
misma idea reaparecerá en Zig con `std.log` resuelto en compilación. Los ficheros `.pdb` cumplen aquí
el papel del `-g` de C: sin ellos el depurador ve direcciones y nombres manglados, con ellos ve tus
líneas — y por eso los `.pdb` se archivan junto a cada versión publicada.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí el programa que corre es código máquina sin
ninguna noción de sí mismo: la información de depuración es un **artefacto aparte** que el compilador
emite solo si se lo pides.

### C++

```cpp
#include <iostream>

// Se compila con `-g` para conservar los símbolos y se depura con `gdb` o
// `lldb`. Sin `-g` el depurador solo ve direcciones y nombres manglados
// (`_ZNSt6vectorIiE...`); con optimización, además, variables enteras
// desaparecen y las líneas dejan de corresponder al fuente.
int main() {
    long long n = 0;
    std::cin >> n;
    std::cout << "valor=" << n << " cuadrado=" << n * n
              << " cubo=" << n * n * n << "\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    // `lldb` sabe hablar con el runtime de Objective-C: en el prompt se puede
    // enviar un mensaje a un objeto vivo (`po [obj description]`) porque el
    // despacho es dinámico y el runtime conserva los nombres de los métodos.
    // Ningún depurador de C puro puede hacer eso.
    long long n = 0;
    scanf("%lld", &n);
    printf("valor=%lld cuadrado=%lld cubo=%lld\n", n, n * n, n * n * n);
}
```

**Qué reconocer:** esta familia enseña la lección más incómoda de la depuración: **el binario que
depuras puede no ser el programa que escribiste**. Con `-O2`, el compilador reordena, integra
funciones y elimina variables, así que el depurador salta de línea en línea sin sentido aparente y
`gdb` responde `<optimized out>` a la mitad de las preguntas. Por eso existen builds de depuración
separados. Y por eso ninguna de las dos imprime traza de pila por sí sola cuando algo revienta:
`SIGSEGV` y punto. Objective-C introduce una grieta valiosa en ese modelo — su capa de objetos
conserva metadatos en ejecución, así que `lldb` puede interrogar objetos vivos como si estuviera en
un lenguaje dinámico, sobre el mismo binario compilado.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos son compilados
pero **imprimen traza de pila al entrar en pánico**, sin depurador ni configuración: es la respuesta
moderna al silencio de C.

### Zig

```zig
const std = @import("std");

// En modo Debug, Zig imprime una traza de pila legible —con fichero, línea y
// código fuente— cuando algo entra en pánico, sin `-g` ni depurador. Para
// pausar y avanzar se usa `gdb`/`lldb` igual que en C. `std.debug.print`
// escribe a stderr, así que no contamina la salida del contrato.
pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \t\r"), 10);

    try std.io.getStdOut().writer().print(
        "valor={d} cuadrado={d} cubo={d}\n",
        .{ n, n * n, n * n * n },
    );
}
```

### Nim

```nim
import std/strutils

# Nim compila a C: el depurador que acabas usando es `gdb` sobre el C generado,
# y los nombres de la pila llevan los sufijos del generador de código.
# `--debugger:native` emite la información de depuración nativa que hace ese
# salto soportable, y `--stackTrace:on` da la traza en términos de Nim.
let n = parseInt(stdin.readLine().strip())

echo "valor=", n, " cuadrado=", n * n, " cubo=", n * n * n
```

### D

```d
import std.stdio, std.string, std.conv;

// `dmd -g` emite información de depuración con los símbolos de D, de modo que
// `gdb` y `lldb` muestran nombres desmanglados. Una excepción sin capturar en D
// sí imprime traza de pila por defecto, a diferencia de C++.
void main() {
    immutable n = readln().strip().to!long;
    writefln("valor=%d cuadrado=%d cubo=%d", n, n * n, n * n * n);
}
```

**Qué reconocer:** los tres usan las mismas herramientas que C —`gdb`, `lldb`, formato DWARF— pero
han cambiado la política por defecto: cuando algo va mal, **hablan**. Zig imprime traza legible en
modo Debug, D la imprime ante una excepción no capturada, y Go y Rust en el núcleo hacen lo mismo al
entrar en pánico. Esa diferencia frente a C es de diseño, no de tecnología: la información ya estaba
disponible, simplemente decidieron gastarla. Nim añade un matiz propio y muy visible al depurar: como
genera C, hay dos capas de nombres, y el depurador te enseña la de abajo salvo que le des la
información nativa. Es el mismo fenómeno que ver clases sintéticas en Scala, un piso más abajo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL no se depura paso a paso: se pide `EXPLAIN`
y se lee el **plan** que el motor eligió, porque el orden real de ejecución no lo escribiste tú.

### Prolog

```prolog
:- initialization(main, main).

% `trace/0` activa el depurador de CAJAS: cada objetivo se muestra cuatro veces
% —al ENTRAR (Call), al tener éxito (Exit), al REINTENTAR (Redo) y al FALLAR
% (Fail)—, porque el flujo no es lineal: retrocede. Es imprescindible aquí
% porque en Prolog un objetivo que no se deriva NO lanza excepción: falla en
% silencio, y el programa termina sin imprimir nada ni decir por qué.
main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    Cuadrado is N * N,
    Cubo is N * N * N,
    format("valor=~w cuadrado=~w cubo=~w~n", [N, Cuadrado, Cubo]).
```

### Datalog

```datalog
% Datalog no tiene depurador de pasos porque no hay pasos observables: el motor
% deriva el punto fijo de las reglas y el orden en que lo hace es cosa suya.
% Lo más cercano a depurar es CONSULTAR las relaciones intermedias, o pedir al
% motor la procedencia de un hecho derivado. La aritmética de abajo es de
% Soufflé; el Datalog puro clásico no tiene operadores aritméticos.
entrada(3).

cuadrado(N, C) :- entrada(N), C = N * N.
cubo(N, K) :- entrada(N), K = N * N * N.
```

**Qué reconocer:** aquí se rompe el supuesto sobre el que descansa toda la página anterior — que
depurar es *detener el programa en un punto y mirar*. En Prolog el punto no es único: el mismo
objetivo se visita al llamarlo y otra vez al reintentarlo tras un fallo, y por eso su depurador tiene
cuatro puertos en vez de una línea actual. Y la razón por la que `trace/0` es más necesario que
cualquier depurador de esta página es que **Prolog no falla por excepción**: si algo no es derivable,
la respuesta es simplemente "no", el programa termina limpio y no queda ningún mensaje que leer. Un
fallo silencioso no se puede diagnosticar leyendo una traza, porque no hay traza. Datalog lleva la
idea al extremo: sin flujo de control que seguir, la única pregunta que se puede depurar es *por qué
está (o no está) este hecho en la relación*.

---

## Y de vuelta a la clase

Veinte lenguajes y un solo eje que los ordena: **cuánto sabe el programa sobre sí mismo mientras
corre**. En un extremo, C++ optimizado, donde el binario ha perdido tanto que el depurador contesta
`<optimized out>`. En el otro, Clojure y su REPL vivo, donde no hace falta detener nada porque se
puede reemplazar una función en marcha. Y entre medias, la lección que más se repite: casi todos los
runtimes modernos —Zig, D, Go, Rust— decidieron **gastar** esa información imprimiendo una traza
legible por defecto, mientras que R y C, cada uno por su lado, siguen callándose y obligan a pedirla.

⏮️ [Volver a la clase 138](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
