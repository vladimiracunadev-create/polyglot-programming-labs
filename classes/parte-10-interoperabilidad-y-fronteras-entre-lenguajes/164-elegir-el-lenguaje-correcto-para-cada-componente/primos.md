# 🧬 El mismo programa en las familias de lenguajes — Clase 164

> [⬅️ Volver a la clase 164](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —recomendar un lenguaje según el tipo de
componente— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Esta clase cierra la parte, y el programa tiene un guiño: es una **tabla de decisión** sobre qué
lenguaje elegir, escrita veinte veces en veinte lenguajes distintos. Los "Qué reconocer" de abajo no
hablan de sintaxis, entonces, sino de lo único que importa al elegir: **qué aporta cada familia,
cuándo no conviene meterla, y qué cuesta de verdad mantener un toolchain más**.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra, `sistemas`, `web` o `datos`
- **Salida** (stdout): `lenguaje=<Rust|TypeScript|SQL>`
- **Regla:** `sistemas` → Rust, `web` → TypeScript, `datos` → SQL

| stdin | esperado |
|---|---|
| `sistemas` | `lenguaje=Rust` |
| `web` | `lenguaje=TypeScript` |
| `datos` | `lenguaje=SQL` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia que se elige por velocidad de escritura, no de ejecución.

### Ruby

```ruby
RECOMENDACION = { "sistemas" => "Rust", "web" => "TypeScript", "datos" => "SQL" }.freeze

puts "lenguaje=#{RECOMENDACION.fetch(STDIN.gets.strip, 'Ruby')}"
```

### Perl

```perl
my %rec = (sistemas => 'Rust', web => 'TypeScript', datos => 'SQL');

chomp(my $tipo = <STDIN>);
printf "lenguaje=%s\n", $rec{$tipo} // 'Perl';
```

### Lua

```lua
local rec = { sistemas = "Rust", web = "TypeScript", datos = "SQL" }

local tipo = io.read("l"):match("%S+")
print("lenguaje=" .. (rec[tipo] or "Lua"))
```

### Tcl

```tcl
array set rec {sistemas Rust web TypeScript datos SQL}

set tipo [string trim [gets stdin]]
puts "lenguaje=[expr {[info exists rec($tipo)] ? $rec($tipo) : {Tcl}}]"
```

### R

```r
rec <- c(sistemas = "Rust", web = "TypeScript", datos = "SQL")

tipo <- trimws(readLines("stdin", n = 1))
cat(sprintf("lenguaje=%s\n", if (tipo %in% names(rec)) rec[[tipo]] else "R"))
```

**Qué reconocer:** los cinco escriben la tabla en una línea, y ahí está su argumento entero:
**cuando el problema es pegar cosas, esta familia gana**. Scripts de despliegue, transformaciones de
datos de una sola vez, prototipos que hay que enseñar mañana. Lo que aportan es que el ciclo entre
pensar y ver el resultado no pasa por un compilador.

Dónde **no** conviene meterlas: en el camino caliente de un servicio con carga real, en componentes
que van a vivir cinco años y a ser tocados por diez personas —el tipado dinámico convierte cada
refactorización grande en una apuesta—, y en cualquier binario que haya que distribuir, porque
distribuir un script es distribuir también su intérprete y sus dependencias. R merece un párrafo
propio porque es el ejemplo más claro de *elegir por el ecosistema y no por el lenguaje*: nadie
escoge R por su diseño, se escoge porque el modelo estadístico que necesitas ya está publicado en
CRAN y validado por gente que sabe de estadística. Ese criterio —¿existe ya la biblioteca?— pesa más
en decisiones reales que casi cualquier propiedad del lenguaje.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

const recomendacion = {'sistemas': 'Rust', 'web': 'TypeScript', 'datos': 'SQL'};

void main() {
  final tipo = stdin.readLineSync()!.trim();
  print('lenguaje=${recomendacion[tipo] ?? 'Dart'}');
}
```

### ActionScript 3

```actionscript
// Sin stdin: se ilustra solo la tabla de decision.
package {
    public class Eleccion {
        private static const REC:Object = {
            sistemas: "Rust", web: "TypeScript", datos: "SQL"
        };
        public static function recomendar(tipo:String):String {
            return "lenguaje=" + (REC[tipo] != null ? REC[tipo] : "ActionScript");
        }
    }
}
```

**Qué reconocer:** esta familia se elige por una razón que no admite discusión: **es la única que
corre en el navegador**. No hay evaluación comparativa que hacer para la interfaz de una aplicación
web; hay que hablar el idioma del intérprete que ya está instalado en la máquina del usuario. Lo que
sí se elige es el **dialecto**, y ahí TypeScript se impuso porque devuelve, a cambio de un paso de
compilación, lo único que a JavaScript le faltaba para proyectos grandes.

Dart y ActionScript son las dos caras de la misma lección histórica, y por eso vale la pena mirarlos
juntos. ActionScript **fue** el lenguaje de la web animada durante una década, y desapareció no por
malo sino porque su tiempo de ejecución era un complemento propietario que los navegadores dejaron de
cargar. Dart nació para reemplazar a JavaScript en el navegador, no lo consiguió, y encontró su sitio
años después como lenguaje de Flutter, compilando a nativo para móvil. La conclusión práctica para
elegir hoy: **un lenguaje solo es tan viable como el tiempo de ejecución que alguien mantenga bajo
él**, y esa dependencia es más peligrosa cuando el dueño del tiempo de ejecución es una sola empresa.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). El caso donde elegir otro lenguaje **no**
significa añadir otro toolchain.

### Kotlin

```kotlin
val recomendacion = mapOf("sistemas" to "Rust", "web" to "TypeScript", "datos" to "SQL")

fun main() {
    val tipo = readLine()!!.trim()
    println("lenguaje=${recomendacion[tipo] ?: "Kotlin"}")
}
```

### Scala

```scala
object Eleccion {
  private val recomendacion =
    Map("sistemas" -> "Rust", "web" -> "TypeScript", "datos" -> "SQL")

  def main(args: Array[String]): Unit = {
    val tipo = scala.io.StdIn.readLine().trim
    println(s"lenguaje=${recomendacion.getOrElse(tipo, "Scala")}")
  }
}
```

### Groovy

```groovy
def recomendacion = [sistemas: 'Rust', web: 'TypeScript', datos: 'SQL']

def tipo = System.in.newReader().readLine().trim()
println "lenguaje=${recomendacion.getOrDefault(tipo, 'Groovy')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(def recomendacion {"sistemas" "Rust", "web" "TypeScript", "datos" "SQL"})

(println (str "lenguaje=" (get recomendacion (str/trim (read-line)) "Clojure")))
```

**Qué reconocer:** aquí hay una excepción real a todo lo que dice esta clase sobre el coste de sumar
lenguajes. Los cuatro compilan al mismo bytecode, corren en la misma máquina virtual, usan las mismas
bibliotecas y se despliegan en el mismo artefacto. Meter Kotlin en un proyecto Java **no** añade un
despliegue nuevo, ni un servidor nuevo, ni una cadena de dependencias nueva que auditar: añade un
compilador. Ese es el caso más barato de poliglotismo que existe, y explica por qué la JVM acumuló
tantos lenguajes.

Barato no es gratis. Lo que sí se paga es **humano**: Scala y Clojure no son Java con otra sintaxis,
son otros paradigmas, y un equipo que sabe Java no lee Clojure. La pregunta al añadir un lenguaje a
la JVM no es "¿encaja técnicamente?" —siempre encaja—, sino "¿quién revisa este código cuando la
persona que lo escribió cambie de trabajo?". Groovy da el matiz opuesto y muy útil: sobrevive
sobre todo como **lenguaje de scripts de construcción** (Gradle) y de pruebas (Spock), no como
lenguaje de aplicación. Elegir un lenguaje para una zona acotada y de bajo riesgo es una decisión
completamente distinta a elegirlo para el núcleo del producto, y confundirlas es un error caro.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). La misma economía que la JVM, con otro dueño.

### F\#

```fsharp
let recomendacion =
    Map [ "sistemas", "Rust"; "web", "TypeScript"; "datos", "SQL" ]

[<EntryPoint>]
let main _ =
    let tipo = stdin.ReadLine().Trim()
    printfn "lenguaje=%s" (recomendacion |> Map.tryFind tipo |> Option.defaultValue "F#")
    0
```

### VB.NET

```vbnet
Module Eleccion
    Sub Main()
        Dim rec = New Dictionary(Of String, String) From {
            {"sistemas", "Rust"}, {"web", "TypeScript"}, {"datos", "SQL"}
        }
        Dim tipo = Console.ReadLine().Trim()
        Dim r As String = Nothing
        Console.WriteLine("lenguaje=" & If(rec.TryGetValue(tipo, r), r, "VB.NET"))
    End Sub
End Module
```

**Qué reconocer:** igual que en la JVM, mezclar C# y F# en una misma solución cuesta casi nada
técnicamente, y F# es la mejor demostración de *elegir el lenguaje por el componente*: para modelar
un dominio con muchos estados —un motor de reglas, un cálculo financiero, un intérprete— sus tipos
unión y la comprobación de exhaustividad del compilador convierten en error de compilación lo que en
C# sería un `default:` olvidado. Es una ventaja concreta y medible, no una preferencia estética.

VB.NET aporta la otra mitad de la lección, la incómoda: es un lenguaje **vivo y soportado, pero
cerrado a nuevas características** desde 2020. Ningún proyecto nuevo lo elige; muchísimos lo
mantienen. Al evaluar un lenguaje, la pregunta no es solo qué puede hacer hoy, sino en qué punto de
su vida está y cuánta gente hay dispuesta a trabajar en él. Un lenguaje que ya no atrae gente nueva
es una decisión de contratación, no solo de arquitectura, y el coste no aparece el primer año.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia que se elige cuando algo tiene que ser
llamable desde todo lo demás.

### C++

```cpp
#include <iostream>
#include <string>
#include <unordered_map>

int main() {
    const std::unordered_map<std::string, std::string> rec{
        {"sistemas", "Rust"}, {"web", "TypeScript"}, {"datos", "SQL"}};
    std::string tipo;
    std::cin >> tipo;
    const auto it = rec.find(tipo);
    std::cout << "lenguaje=" << (it != rec.end() ? it->second : "C++") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSDictionary *rec = @{@"sistemas": @"Rust",
                              @"web": @"TypeScript",
                              @"datos": @"SQL"};
        char buf[32];
        if (scanf("%31s", buf) != 1) return 1;
        NSString *tipo = [NSString stringWithUTF8String:buf];
        NSString *r = rec[tipo] ?: @"Objective-C";
        printf("lenguaje=%s\n", [r UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** C y C++ se eligen hoy por tres motivos honestos, y ninguno es "porque son
rápidos" a secas. Primero, porque el **ecosistema ya existe** ahí: motores de bases de datos,
códecs, bibliotecas numéricas y de criptografía llevan décadas escritas en C, y reescribirlas no
está sobre la mesa. Segundo, porque C es el **idioma franco**: como vieron las clases 156 a 158,
todos los demás lenguajes saben llamar a C, así que un componente en C es un componente que todo el
sistema puede usar. Tercero, porque en sistemas embebidos y núcleos de sistema operativo a menudo no
hay nada más.

Cuándo **no**: en código nuevo que manipule datos que vienen de la red o del usuario. Elegir C o C++
para eso es aceptar voluntariamente una clase entera de vulnerabilidades de memoria que Rust o Go te
quitan de encima sin pedir nada a cambio de rendimiento. Objective-C añade el caso de *lenguaje
atado a una plataforma*: fue obligatorio para desarrollar en Apple, y dejó de serlo cuando la propia
Apple publicó Swift. Cuando el dueño de la plataforma cambia de idioma, tu elección se caduca sin que
tú hayas hecho nada; ese riesgo hay que contarlo al elegir.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia que **es** la
respuesta correcta del programa para `sistemas`.

### Zig

```zig
const std = @import("std");

// StaticStringMap se construye en tiempo de compilación: la tabla no cuesta
// nada en ejecución.
const recomendacion = std.StaticStringMap([]const u8).initComptime(.{
    .{ "sistemas", "Rust" },
    .{ "web", "TypeScript" },
    .{ "datos", "SQL" },
});

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const tipo = std.mem.trim(u8, linea, " \t\r");
    const r = recomendacion.get(tipo) orelse "Zig";
    try std.io.getStdOut().writer().print("lenguaje={s}\n", .{r});
}
```

### Nim

```nim
import std/[strutils, tables]

const recomendacion = {"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}.toTable

let tipo = stdin.readLine().strip()
echo "lenguaje=", recomendacion.getOrDefault(tipo, "Nim")
```

### D

```d
import std.stdio, std.string;

void main() {
    auto rec = ["sistemas": "Rust", "web": "TypeScript", "datos": "SQL"];
    auto tipo = readln().strip();
    writeln("lenguaje=", (tipo in rec) ? rec[tipo] : "D");
}
```

**Qué reconocer:** el programa recomienda **Rust** para `sistemas`, y estos tres primos explican por
qué la recomendación no dice "Zig", "Nim" ni "D" aunque los tres sean buenos lenguajes. Técnicamente
los cuatro compiten en el mismo terreno; en una decisión real compiten además en otras cosas: cuánta
gente puede contratarse, cuántas bibliotecas maduras hay, si la compatibilidad hacia atrás está
garantizada, y si alguien va a seguir manteniendo el compilador dentro de diez años. Zig es
excelente y todavía no ha llegado a la versión 1.0; eso no lo descalifica, pero es un dato que va en
la hoja de decisión junto a los demás.

Aquí es donde hay que decir en voz alta el **coste real de sumar un toolchain**, porque es lo que
esta clase entera intenta enseñar. Añadir un lenguaje a un sistema no añade un compilador: añade una
imagen de construcción distinta en el CI, un gestor de paquetes más con su propio archivo de bloqueo
y su propia superficie de dependencias que auditar, un formato de artefacto y un despliegue que se
comportan distinto en producción, una manera distinta de depurar cuando algo falla a las tres de la
madrugada, y —lo más caro de todo— **una persona más a la que contratar o formar**. Un componente en
Rust dentro de un sistema en Python no cuesta lo que tarda en escribirse; cuesta todo lo que rodea a
ese código durante los años que viva. La pregunta no es "¿es este el mejor lenguaje para esta
tarea?", sino "¿la mejora justifica el segundo toolchain?". A veces sí, con claridad. Muchas más
veces de las que parece, no.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia que casi nadie *elige* y casi todos
usan.

### Prolog

```prolog
:- initialization(main, main).

recomendacion(sistemas, 'Rust').
recomendacion(web, 'TypeScript').
recomendacion(datos, 'SQL').

main :-
    read_line_to_string(user_input, Linea0),
    split_string(Linea0, "", " \t\r", [Linea]),
    atom_string(Tipo, Linea),
    (   recomendacion(Tipo, L)
    ->  true
    ;   L = 'Prolog'
    ),
    format("lenguaje=~w~n", [L]).
```

### Datalog

```datalog
% Datalog no lee stdin: el componente entra como hecho y la regla decide.
% De las veinte versiones, esta es la que menos se parece a un programa y
% mas se parece al problema: la tabla de decision ES el programa.
componente(sistemas).

recomendacion(sistemas, "Rust").
recomendacion(web, "TypeScript").
recomendacion(datos, "SQL").

lenguaje(L) :- componente(T), recomendacion(T, L).
```

**Qué reconocer:** mira los dos bloques y compáralos con los dieciocho anteriores. En todos los
demás la tabla es un **dato** dentro de un programa; aquí la tabla **es** el programa, y no hay
ninguna línea de andamiaje. Eso es lo que aporta un lenguaje declarativo: cuando el problema ya tiene
forma de reglas y hechos, escribirlo en un lenguaje imperativo es traducirlo dos veces.

De ahí sale el criterio más útil de la clase, y es el que menos se aplica: **SQL casi nunca se
elige, se usa**, y esa falta de decisión consciente es justamente el problema. Miles de sistemas
arrastran en su código de aplicación bucles que recorren filas, agrupan y suman a mano lo que el
motor haría con una consulta de tres líneas —más rápido, con menos datos por la red y con menos
código que mantener—. Elegir bien el lenguaje de cada componente no es solo decidir en qué escribir
un servicio nuevo; es también reconocer qué parte de la lógica ya pertenece a un lenguaje que el
sistema **ya tiene instalado**. Prolog y Datalog casi nunca son la respuesta como lenguaje de
aplicación, pero su forma de pensar aparece disfrazada en todas partes: motores de reglas de negocio,
comprobadores de políticas de acceso, análisis estático de código. Reconocer esa forma es más
transferible que el lenguaje en sí.

---

## Y de vuelta a la clase

Veinte lenguajes para responder qué lenguaje elegir, y la respuesta honesta no está en ninguna tabla:
está en el coste. Cada lenguaje aporta algo real —el navegador, la memoria segura, el ecosistema
estadístico, la exhaustividad del compilador, la declaratividad— y cada uno cobra algo real: otro
despliegue, otra cadena de dependencias que auditar, otra persona que contratar. Un sistema políglota
bien hecho no es el que usa más lenguajes, sino el que **puede justificar cada frontera que tiene**.
Con eso cierra la parte de interoperabilidad, y con eso empieza el proyecto integrador.

⏮️ [Volver a la clase 164](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
