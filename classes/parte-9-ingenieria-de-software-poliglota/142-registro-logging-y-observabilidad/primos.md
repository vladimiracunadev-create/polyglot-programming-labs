# 🧬 El mismo programa en las familias de lenguajes — Clase 142

> [⬅️ Volver a la clase 142](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —emitir un registro de nivel `INFO` diciendo cuántos
elementos se procesaron— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Una línea de log parece el programa más simple posible, y por eso sirve tan bien: revela quién trae
un sistema de registro en la **biblioteca estándar** (Ruby, Zig, Nim, D), quién lo dejó fuera y
delegó en la comunidad (Perl, Lua, C++), y quién construyó una **fachada** que por sí sola no
escribe nada. También revela una asimetría que aparece en cuanto se escribe código real: casi todos
los sistemas de log de verdad emiten a **stderr** y con prefijos que no se pueden quitar. El contrato
de la clase pide una línea exacta en stdout, así que varios bloques usan la salida directa y explican
en un comentario cuál sería la herramienta idiomática.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, los elementos procesados
- **Salida** (stdout): `log=[INFO] procesados=<n>`
- **Regla:** emitir un registro de nivel `INFO` con el conteo

| stdin | esperado |
|---|---|
| `5` | `log=[INFO] procesados=5` |
| `0` | `log=[INFO] procesados=0` |
| `3` | `log=[INFO] procesados=3` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia se parte en dos: los que metieron un `Logger` en la estándar y los que decidieron que
imprimir ya es suficiente y que lo demás lo ponga CPAN o LuaRocks.

### Ruby

```ruby
require 'logger'

# `Logger` está en la biblioteca estándar de Ruby desde hace décadas, con
# niveles, rotación de ficheros y formateador reemplazable. Por defecto emite
# severidad, fecha y pid; aquí se sustituye el formateador para cumplir el
# contrato exacto de la clase.
log = Logger.new($stdout)
log.formatter = proc { |severidad, _hora, _prog, mensaje| "log=[#{severidad}] #{mensaje}\n" }

n = STDIN.gets.to_i
log.info("procesados=#{n}")
```

### Perl

```perl
use strict;
use warnings;

# Perl no trae registro en el core. Lo idiomático es `Log::Log4perl` (CPAN),
# un puerto fiel de log4j con su misma jerarquía de niveles, appenders y
# configuración en fichero. Sin esa dependencia, un `printf` con el nivel
# delante es el equivalente mínimo, y así se escribe aquí.
chomp(my $n = <STDIN>);
printf "log=[%s] procesados=%d\n", 'INFO', $n;
```

### Lua

```lua
-- Lua tampoco tiene registro estándar: la estándar entera cabe en unas pocas
-- páginas y `print` es toda la primitiva de salida. `lualogging` (LuaRocks)
-- añade niveles y destinos; el lenguaje deja esa decisión al anfitrión.
local n = math.tointeger(tonumber(io.read("l")))
print(string.format("log=[%s] procesados=%d", "INFO", n))
```

### Tcl

```tcl
# Tcllib incluye el paquete `logger`, con jerarquía de servicios por nombre
# (`::mi::modulo` hereda del nivel de `::mi`) y un callback por nivel.
# El canal stdout directo basta para el contrato.
set n [string trim [gets stdin]]
puts [format {log=[%s] procesados=%d} INFO $n]
```

### R

```r
# El sistema de "niveles" del core de R son tres funciones con destinos
# distintos: `message()` y `warning()` escriben a stderr, `cat()` a stdout, y
# `stop()` aborta. No hay nivel INFO ni formato configurable: eso lo aportan
# `futile.logger` o el paquete `logger` desde CRAN.
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("log=[%s] procesados=%d\n", "INFO", n))
```

**Qué reconocer:** el reparto es limpio y dice mucho de cada lenguaje. Ruby, que siempre ha traído
una estándar generosa, tiene `Logger` con niveles y formateador desde el principio — y fíjate en que
lo primero que hay que hacer para cumplir un contrato de texto exacto es **quitarle** el formato por
defecto, porque un logger real quiere añadir fecha, proceso y severidad. Perl y Lua eligieron lo
contrario: `Log::Log4perl` es CPAN, no core, y en Lua ni siquiera hay candidato canónico. R aporta el
caso más peculiar de la familia, porque su "logging" no es un nivel configurable sino **tres
funciones con tres canales distintos**: `message` y `warning` van a stderr, `cat` a stdout, y esa
separación de canales —no de niveles— es la que hay que entender para no ver desaparecer la salida al
redirigir.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
En esta familia el registro nació orientado a una **consola de desarrollador**, no a un fichero, y
eso dejó huella: `console.log` no distingue destino ni nivel real.

### Dart

```dart
import 'dart:io';

// El paquete `logging` lo mantiene el propio equipo de Dart pero vive FUERA del
// SDK, en pub.dev: define `Logger` y `Level`, y no escribe nada hasta que se le
// registra un `onRecord`. Es fachada y suscriptor, no salida directa.
void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  stdout.writeln('log=[INFO] procesados=$n');
}
```

### ActionScript 3

```actionscript
// `trace()` solo escribe en el reproductor de DEPURACIÓN: en producción la
// llamada se ejecuta y no produce nada visible. El lenguaje no tiene stdin, así
// que la entrada llega por otra vía y aquí se ilustra solo la construcción.
package {
    public class Registro {
        public static function registrar(n:int):String {
            return "log=[INFO] procesados=" + n;
        }
    }
}
```

**Qué reconocer:** los dos heredan la idea de que el destino del log es un **entorno de
observación**, no un archivo. `trace()` de ActionScript solo existe en el reproductor de depuración,
lo mismo que `Debug.WriteLine` de .NET pero decidido en ejecución en vez de en compilación. Dart
corrigió el rumbo con el paquete `logging`, que es la primera aparición en esta página de un patrón
que se repetirá en la JVM: la API que llamas **no escribe**; solo produce registros que alguien más
tiene que suscribir y volcar. Si nadie se suscribe, tus logs se pierden en silencio, y ese es el
error de configuración más común de toda la clase.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM es donde se inventó la separación entre
API de registro e implementación, y donde esa separación causa más confusión.

### Kotlin

```kotlin
// En la JVM lo idiomático es SLF4J: `LoggerFactory.getLogger(Clase::class.java)`.
// Pero SLF4J es una FACHADA, no una implementación: sin Logback o Log4j2 en el
// classpath no se escribe absolutamente nada, solo un aviso al arrancar.
// Aquí se imprime directo para respetar el contrato de la clase.
fun main() {
    val n = readLine()!!.trim().toInt()
    println("log=[INFO] procesados=$n")
}
```

### Scala

```scala
object Registro extends App {
  // `scala-logging` envuelve SLF4J con macros: `logger.info(s"...")` NO
  // construye la cadena interpolada si el nivel INFO está apagado, porque la
  // macro rodea la llamada con el `if (logger.isInfoEnabled)`. Coste cero
  // cuando el registro no se emite: ese es el argumento de esas bibliotecas.
  val n = scala.io.StdIn.readLine().trim.toInt
  println(s"log=[INFO] procesados=$n")
}
```

### Groovy

```groovy
// La anotación `@Slf4j` sobre una clase INYECTA en tiempo de compilación un
// campo `log` ya inicializado: la transformación AST escribe por ti el
// `LoggerFactory.getLogger(Clase)` que en Java se teclea a mano.
def n = System.in.newReader().readLine().trim() as int
println "log=[INFO] procesados=$n"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; `clojure.tools.logging` descubre EN EJECUCIÓN qué backend hay disponible
;; —Logback, Log4j2, java.util.logging— y delega en el primero que encuentre.
;; Es una fachada sobre la fachada, y ese es el precio de la interoperabilidad.
(let [n (Long/parseLong (str/trim (read-line)))]
  (println (str "log=[INFO] procesados=" n)))
```

**Qué reconocer:** lo que hay que llevarse de esta familia es la palabra **fachada**. SLF4J define
la interfaz `Logger` y nada más: no escribe a ningún sitio. La escritura la aporta Logback o Log4j2,
que se eligen en el classpath, no en el código. Así una biblioteca puede registrar sin imponerle un
destino a la aplicación que la use — y así también un despliegue puede quedarse mudo por una
dependencia que falta, sin ningún error visible. Sobre esa base común, cada primo aporta su truco: la
macro de `scala-logging` elimina el coste de formatear un mensaje que nunca se emitirá, la anotación
`@Slf4j` de Groovy genera el campo en compilación, y `tools.logging` de Clojure añade otra capa de
indirección para no atarse ni siquiera a SLF4J.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Aquí la abstracción es `ILogger` de
`Microsoft.Extensions.Logging`, y la idea dominante es el **registro estructurado**.

### F\#

```fsharp
// El estándar de .NET es `ILogger` (Microsoft.Extensions.Logging), y la
// implementación más usada es Serilog, que registra eventos ESTRUCTURADOS: la
// plantilla `"procesados={Conteo}"` y el valor viajan SEPARADOS hasta el
// destino, así que un sumidero JSON conserva el número como número.
let n = int (stdin.ReadLine().Trim())
printfn "log=[INFO] procesados=%d" n
```

### VB.NET

```vbnet
Module Registro
    Sub Main()
        ' `System.Diagnostics.Trace` es el registro incorporado al framework:
        ' escribe a "listeners" configurados fuera del código, no a stdout.
        ' Su hermano `Debug` desaparece del binario en Release. En proyectos
        ' reales los sustituyen Serilog o NLog.
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Console.WriteLine($"log=[INFO] procesados={n}")
    End Sub
End Module
```

**Qué reconocer:** el aporte de .NET a esta página es el **registro estructurado**, y merece
entenderse bien porque es la diferencia entre logging y observabilidad. Un logger clásico produce una
cadena ya formateada: `"procesados=5"`, y para buscar por ese 5 hay que volver a analizarlo con una
expresión regular. Serilog conserva la plantilla y los valores por separado, así que el evento llega
al destino como un objeto con un campo `Conteo = 5` que se puede filtrar y agregar sin adivinar. VB.NET
recuerda además la otra pieza del modelo .NET: los `TraceListener`, donde el destino se configura
**fuera del código** —igual que el classpath de la JVM decide el backend de SLF4J—, y donde `Debug`
frente a `Trace` repite la distinción entre diagnóstico que se compila y diagnóstico que se envía.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La estándar de C no tiene registro: tiene dos flujos,
`stdout` y `stderr`, y la única garantía interesante es que el segundo no está bufferizado.

### C++

```cpp
#include <iostream>

// La estándar de C++ tampoco tiene registro: se usan bibliotecas externas
// (spdlog, glog). Lo único que el lenguaje garantiza es que `std::cerr` no
// está bufferizado y `std::cout` sí: por eso los diagnósticos van a cerr, para
// que sobrevivan a un cierre abrupto del proceso.
int main() {
    long long n = 0;
    std::cin >> n;
    std::cout << "log=[INFO] procesados=" << n << "\n";
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    // `NSLog` escribe a stderr Y al log unificado del sistema, con marca de
    // tiempo, nombre de proceso y pid delante — un prefijo que NO se puede
    // quitar. Por eso aquí va `printf`: el contrato pide una línea exacta.
    long long n = 0;
    scanf("%lld", &n);
    printf("log=[INFO] procesados=%lld\n", n);
}
```

**Qué reconocer:** en esta familia el registro no es una biblioteca sino una **convención sobre
descriptores de fichero**: escribe los diagnósticos a `stderr` y deja `stdout` para la salida del
programa, porque así el usuario puede redirigir uno sin perder el otro. Esa convención de Unix es el
antepasado de todos los sistemas de niveles de esta página, y sigue siendo la razón técnica por la
que casi ningún logger escribe a stdout. Objective-C aporta el otro extremo del péndulo: `NSLog` no
solo tiene formato fijo, es que además manda el mensaje al log **del sistema operativo**, de modo que
el registro deja de ser un fichero de la aplicación para ser una consulta al sistema —la misma idea
que journald en Linux— y la aplicación pierde el control sobre dónde acaba su propio texto.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ambos traen registro con
niveles a mano —`log/slog` en Go, `log` + `tracing` en Rust— y ambos se preocupan por el coste.

### Zig

```zig
const std = @import("std");

// `std.log` está en la estándar y sus niveles se resuelven EN COMPILACIÓN:
// fijando `std.options.log_level = .warn`, las llamadas a `std.log.info`
// desaparecen del binario, no se filtran en ejecución. Coste cero literal.
// Escribe a stderr, así que la línea del contrato va aparte a stdout.
pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \t\r"), 10);

    std.log.info("procesados={d}", .{n});
    try std.io.getStdOut().writer().print("log=[INFO] procesados={d}\n", .{n});
}
```

### Nim

```nim
import std/[logging, strutils]

# `std/logging` viene en la estándar con `ConsoleLogger`, `FileLogger` y
# `RollingFileLogger`. El formato se define con `fmtStr` y el filtrado por
# `levelThreshold` ocurre en EJECUCIÓN, no en compilación como en Zig.
let consola = newConsoleLogger(levelThreshold = lvlInfo, fmtStr = "log=[INFO] ")
addHandler(consola)

let n = parseInt(stdin.readLine().strip())
info "procesados=", n
```

### D

```d
import std.stdio, std.string, std.conv;

// `std.experimental.logger` lleva años en la estándar SIN salir de
// "experimental": ese nombre es el aviso de que la API puede romperse entre
// versiones. Añade automáticamente fichero, línea y función de origen usando
// los parámetros por defecto `__FILE__` y `__LINE__` del lenguaje.
void main() {
    immutable n = readln().strip().to!long;
    writefln("log=[INFO] procesados=%d", n);
}
```

**Qué reconocer:** los tres traen registro en la estándar, pero deciden el filtrado en momentos
distintos y esa es la comparación que vale. Zig resuelve el nivel **en compilación**: si el umbral es
`warn`, la llamada `std.log.info` ni siquiera existe en el binario, así que el coste es cero y el
precio es que cambiar el nivel exige recompilar. Nim y D filtran en ejecución, como la JVM y .NET,
con la flexibilidad y el coste que eso implica. El nombre de D vale por sí solo como lección de
ingeniería: `std.experimental.logger` lleva años ahí y sigue marcado como experimental, un recordatorio
de lo difícil que es acordar una API de registro que le sirva a todo el mundo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL el registro no lo hace tu consulta: lo hace
el **motor**, y se lee después en su log de sentencias lentas o en las vistas del sistema.

### Prolog

```prolog
:- initialization(main, main).

% SWI-Prolog trae `library(debug)`: `debug(Tema, Formato, Args)` emite el
% mensaje solo si ese TEMA se ha activado con `debug/1`. Es registro por tema,
% no por nivel — se enciende el área que interesa en vez de subir un umbral
% global, y las llamadas apagadas no cuestan casi nada.
main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    format("log=[INFO] procesados=~w~n", [N]).
```

### Datalog

```datalog
% Datalog no puede "emitir" un registro: emitir es un EFECTO, y aquí solo se
% derivan hechos. Tampoco hay un orden en el que ocurran las cosas del que
% dejar constancia. Lo más cercano es declarar una relación de eventos y
% consultarla al final; el motor decide cuándo y cómo se puebla.
procesados(5).

registro("INFO", N) :- procesados(N).
```

**Qué reconocer:** estas dos familias obligan a separar dos ideas que el resto de la página mezcla:
*registrar* y *observar*. Prolog cambia el eje de filtrado — no un umbral de severidad sino un
conjunto de **temas** que se encienden por separado, que es exactamente lo que hacen `debug` de
Node.js o los *targets* de `tracing` en Rust. Datalog marca el límite duro: un lenguaje sin efectos
no puede escribir una línea de log, porque escribir es un efecto y aquí solo se deducen hechos. Lo
que sí puede hacer, y es su versión legítima de la observabilidad, es **materializar la relación** y
dejar que la consulta sea la pregunta. Que es, mirándolo bien, lo mismo que hacemos cuando mandamos
los logs a una base de datos y luego los consultamos.

---

## Y de vuelta a la clase

Veinte lenguajes y una línea de texto, pero tres decisiones repartidas de veinte maneras: **dónde se
escribe** (stdout, stderr, el log del sistema, un suscriptor), **cuándo se decide el nivel** (en
compilación en Zig y .NET con `Debug`, en ejecución en todos los demás) y **quién elige la
implementación** (el código, o el classpath y la configuración). La lección más transferible es la de
la JVM: una API de registro que no escribe nada por sí sola no es un defecto, es lo que permite que
una biblioteca registre sin decidir por su usuario. Y la de Datalog es la más honesta: allí donde no
hay efectos, la observabilidad no es escribir, es preguntar.

⏮️ [Volver a la clase 142](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
