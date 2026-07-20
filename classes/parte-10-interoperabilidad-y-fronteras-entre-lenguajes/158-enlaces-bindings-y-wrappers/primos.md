# 🧬 El mismo programa en las familias de lenguajes — Clase 158

> [⬅️ Volver a la clase 158](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —envolver una función nativa en algo que se pueda
llamar cómodamente desde el lenguaje anfitrión— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

La pregunta que recorre los veinte programas es una sola y es muy práctica: **¿cuánto trabajo manual
cuesta envolver una biblioteca de C?** Va desde escribir C a medida contra la API interna del
intérprete hasta no escribir nada porque el compilador lee la cabecera él solo.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

Casi todos los bloques suponen esta biblioteca al lado, que es la función nativa que se quiere
envolver:

```c
/* doble.c → cc -shared -fPIC doble.c -o libdoble.so   (cabecera: doble.h) */
long doble(long x) { return x * 2; }
```

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `envuelto=wrap(<2n>)`
- **Regla:** llamar a `doble(n)` a través de un *wrapper* que adapta y formatea el resultado

| stdin | esperado |
|---|---|
| `5` | `envuelto=wrap(10)` |
| `0` | `envuelto=wrap(0)` |
| `7` | `envuelto=wrap(14)` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia donde más se nota la diferencia entre *declarar una firma* y *escribir un binding*: aquí
conviven los dos caminos, y a veces en el mismo lenguaje.

### Ruby

```ruby
# Fiddle está en la biblioteca estándar: se declara la firma, no se compila nada.
require "fiddle"
require "fiddle/import"

module Nativa
  extend Fiddle::Importer
  dlload "./libdoble.so"
  extern "long doble(long)"
end

# El wrapper: la capa que hace que lo nativo parezca Ruby.
def envolver(n)
  "wrap(#{Nativa.doble(n)})"
end

puts "envuelto=#{envolver(STDIN.gets.to_i)}"
```

### Perl

```perl
# El camino moderno: FFI::Platypus declara la firma en Perl puro.
# El camino clásico, XS, generaría C con dXSARGS, ST(0) y newXS: un binding
# de verdad, que hay que compilar contra los encabezados del intérprete.
use FFI::Platypus 2.00;

my $ffi = FFI::Platypus->new(api => 2, lib => './libdoble.so');
$ffi->attach(doble => ['long'] => 'long');

sub envolver { return "wrap(" . doble($_[0]) . ")" }

my $n = <STDIN>;
printf "envuelto=%s\n", envolver($n + 0);
```

### Lua

```lua
-- No hay firma que declarar: el binding se escribe contra la API de PILA.
--   static int l_doble(lua_State *L) {
--       lua_Integer x = luaL_checkinteger(L, 1);   -- saca el argumento 1
--       lua_pushinteger(L, x * 2);                 -- empuja el resultado
--       return 1;                                  -- cuantos valores devuelve
--   }
--   static const luaL_Reg reg[] = {{"doble", l_doble}, {NULL, NULL}};
--   int luaopen_doble(lua_State *L) { luaL_newlib(L, reg); return 1; }
local nativa = require("doble")

local function envolver(n)
  return string.format("wrap(%d)", nativa.doble(n))
end

print("envuelto=" .. envolver(tonumber(io.read("l"))))
```

### Tcl

```tcl
# Igual que Lua: el binding en C recibe los argumentos como un arreglo de
# Tcl_Obj* y devuelve con Tcl_SetObjResult; se registra con Tcl_CreateObjCommand
# desde Doble_Init. Tampoco hay firma, hay protocolo.
load ./libdoble.so Doble

proc envolver {n} {
    return "wrap([doble $n])"
}

gets stdin n
puts "envuelto=[envolver [string trim $n]]"
```

### R

```r
# Rcpp genera el binding a partir de un atributo en el propio C++:
#   // [[Rcpp::export]]
#   int doble(int x) { return x * 2; }
library(Rcpp)
sourceCpp("doble.cpp")

envolver <- function(n) sprintf("wrap(%d)", doble(n))

n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("envuelto=%s\n", envolver(n)))
```

**Qué reconocer:** aquí está el abanico completo del coste de un binding, ordenado de menos a más
trabajo. Ruby con `Fiddle` y Perl con `FFI::Platypus` **solo declaran la firma**: no compilan nada,
el binding vive en el propio lenguaje y se puede cambiar sin tocar el toolchain. Perl guarda además
el camino antiguo, **XS**, que es lo contrario: un dialecto propio que se traduce a C, se compila
contra los encabezados de Perl y manipula la pila del intérprete a mano. Que los dos convivan en el
mismo lenguaje es la mejor prueba de que "binding" y "declaración de firma" no son sinónimos.

**Lua es el caso más ilustrativo de toda la página.** No tiene FFI en su núcleo: tiene una **pila**
compartida entre el intérprete y el código C. La función C no recibe `long` ni devuelve `long`;
recibe un `lua_State *`, **saca** sus argumentos de la pila con `luaL_checkinteger` y **empuja** el
resultado, devolviendo cuántos valores dejó. Eso significa que cada función que quieras exponer exige
escribir su envoltorio a mano, uno por uno. No es un defecto: Lua nació para **ser incrustado** en un
programa de C, y ese protocolo de pila es lo que permite que el intérprete no sepa nada de los tipos
del anfitrión. Tcl hace lo mismo con otro vocabulario. Rcpp está en el extremo opuesto por comodidad
—un comentario `[[Rcpp::export]]` y el generador escribe el binding—, y de paso regala el chiste de
la clase: la conversión de un valor de C++ a un valor de R se llama, literalmente,
`Rcpp::wrap()`.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
// package:ffigen lee doble.h con libclang y genera estos typedefs solo.
import 'dart:ffi';
import 'dart:io';

typedef _DobleC = Int64 Function(Int64);      // la firma como la ve C
typedef _DobleDart = int Function(int);       // la firma como la ve Dart

final _lib = DynamicLibrary.open('./libdoble.so');
final _doble = _lib.lookupFunction<_DobleC, _DobleDart>('doble');

String envolver(int n) => 'wrap(${_doble(n)})';

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('envuelto=${envolver(n)}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 no puede enlazar con C. En AIR el unico puente son las ANE
// (Adobe Native Extensions), que se empaquetan aparte y se comunican por
// eventos, no por llamada directa. Aqui solo se ilustra el envoltorio.
package {
    public class Wrapper {
        public static function envolver(n:int):String {
            return "envuelto=wrap(" + (n * 2) + ")";
        }
    }
}
```

**Qué reconocer:** Dart muestra el binding en su forma más pura: **dos declaraciones de la misma
función**, una con los tipos de C y otra con los de Dart, más una capa `envolver` encima. Esas tres
piezas son las tres capas de esta clase —enlace, binding y wrapper— separadas en el código. Y sobre
ellas hay un generador, `ffigen`, que lee la cabecera con libclang y escribe los typedefs por ti; lo
que **no** escribe es el wrapper, porque el wrapper es diseño de API y ningún generador sabe qué
quieres que parezca tu biblioteca desde fuera. ActionScript recuerda que no todo lenguaje puede
envolver: cuando la máquina virtual es un sandbox, el binding tiene que vivir fuera del lenguaje.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Cuatro lenguajes que comparten binding, porque
en la JVM la frontera pertenece a la plataforma.

### Kotlin

```kotlin
// JNI: el binding es C escrito a medida de la JVM. El simbolo debe llamarse
// Java_MainKt_doble y recibir un JNIEnv*; javac -h genera la cabecera.
external fun doble(n: Long): Long

fun envolver(n: Long) = "wrap(${doble(n)})"

fun main() {
    System.loadLibrary("doble")
    println("envuelto=${envolver(readLine()!!.trim().toLong())}")
}
```

### Scala

```scala
// jextract lee doble.h y genera la clase de binding (bautizada segun la
// cabecera). Aqui solo se usa lo generado; no se escribio C.
import doble_h.doble

object Wrapper {
  def envolver(n: Long): String = s"wrap(${doble(n)})"

  def main(args: Array[String]): Unit =
    println(s"envuelto=${envolver(scala.io.StdIn.readLine().trim.toLong)}")
}
```

### Groovy

```groovy
@Grab('net.java.dev.jna:jna:5.14.0')
import com.sun.jna.Library
import com.sun.jna.Native

// El binding es una interfaz: JNA la implementa en tiempo de ejecución.
interface Nativa extends Library {
    long doble(long n)
}

def nativa = Native.load('doble', Nativa)
def envolver = { long n -> "wrap(${nativa.doble(n)})" }

println "envuelto=${envolver(System.in.newReader().readLine().trim() as long)}"
```

### Clojure

```clojure
;; Ni interfaz: el símbolo se busca por nombre en tiempo de ejecución.
(import '[com.sun.jna Function])

(def doble (Function/getFunction "doble" "doble"))

(defn envolver [n]
  (str "wrap(" (.invokeLong doble (to-array [n])) ")"))

(println (str "envuelto=" (envolver (Long/parseLong (.trim (read-line))))))
```

**Qué reconocer:** los cuatro llaman a la misma función y el trabajo manual va de mucho a casi nada.
**JNI** es el extremo caro: no basta con que exista `doble` en C, hay que escribir una función C
nueva llamada `Java_MainKt_doble` que reciba el entorno de la JVM, convierta los tipos y se compile
aparte. Es un binding de verdad, con su propio archivo, su propio compilador y su propio despliegue.
**JNA** lo cambió por una **interfaz declarada en el lenguaje**: escribes la firma en Java y la
biblioteca fabrica la llamada en tiempo de ejecución —más lento, incomparablemente más barato de
mantener—. Y **jextract**, la herramienta del proyecto Panama, cierra el círculo: le das la cabecera
de C y te devuelve clases Java listas.

Fíjate en el patrón que se repite en toda la página: el generador te ahorra el **binding**, nunca el
**wrapper**. En los cuatro bloques la línea que produce `wrap(...)` la escribió una persona.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
open System.Runtime.InteropServices

// El binding es la declaración sin cuerpo; el cuerpo lo pone el CLR al cargar.
[<DllImport("doble", CallingConvention = CallingConvention.Cdecl)>]
extern int64 doble(int64 n)

let envolver n = sprintf "wrap(%d)" (doble n)

[<EntryPoint>]
let main _ =
    printfn "envuelto=%s" (envolver (int64 (stdin.ReadLine().Trim())))
    0
```

### VB.NET

```vbnet
Imports System.Runtime.InteropServices

Module Wrapper
    <DllImport("doble", CallingConvention:=CallingConvention.Cdecl)>
    Private Function doble(n As Long) As Long
    End Function

    Private Function Envolver(n As Long) As String
        Return "wrap(" & doble(n) & ")"
    End Function

    Sub Main()
        Console.WriteLine("envuelto=" & Envolver(Long.Parse(Console.ReadLine().Trim())))
    End Sub
End Module
```

**Qué reconocer:** .NET es la plataforma donde el binding cuesta menos trabajo manual de toda la
página: **una declaración sin cuerpo** y ya está, porque el CLR se encarga del *marshalling* —copiar
y convertir los datos a un lado y otro de la frontera— sin que el lenguaje intervenga. VB.NET lo
enseña con una claridad que da gusto: una `Function` con su `End Function` y **nada en medio**.

La distinción de la clase queda perfectamente separada en estos dos bloques: `doble` es el binding,
`Envolver` es el wrapper. El primero es mecánico y hay generadores que lo escriben (`ClangSharp`
sobre las cabeceras, o el generador de fuentes de `LibraryImport` en .NET 7+, que además evita el
marshalling en tiempo de ejecución). El segundo es tuyo: decidir que el resultado se presente como
`wrap(...)` es una decisión de diseño, no una traducción.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La orilla de destino: aquí no hay binding, solo
diseño de API.

### C++

```cpp
#include <iostream>
#include <string>

// La cabecera de C se incluye tal cual; extern "C" evita el name mangling.
// SWIG hace el viaje contrario: a partir de un archivo .i genera bindings
// de esta biblioteca para Python, Ruby, Java, C#, Lua y una docena más.
extern "C" long doble(long);

static std::string envolver(long n) {
    return "wrap(" + std::to_string(doble(n)) + ")";
}

int main() {
    long n;
    std::cin >> n;
    std::cout << "envuelto=" << envolver(n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

long doble(long x) { return x * 2; }

/* Objective-C ES C: no hay binding que generar, solo una clase que expone
   la funcion como metodo con tipos de Foundation. Eso es un wrapper puro. */
@interface Envoltorio : NSObject
+ (NSString *)envolver:(long)n;
@end

@implementation Envoltorio
+ (NSString *)envolver:(long)n {
    return [NSString stringWithFormat:@"wrap(%ld)", doble(n)];
}
@end

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        printf("envuelto=%s\n", [[Envoltorio envolver:n] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** estos dos primos no envuelven **hacia** C, envuelven **dentro** de C, y por eso
enseñan lo que queda de la clase cuando se le quita el problema del enlace: queda el diseño. La clase
`Envoltorio` de Objective-C no resuelve ninguna incompatibilidad —la función ya era llamable—, sino
que decide cómo se ve desde fuera: un método de clase, un `NSString` en vez de un `char *`, gestión
de memoria automática. Eso es exactamente lo que hace un wrapper en cualquier lenguaje.

Y desde este lado sale **SWIG**, el generador con más historia del oficio: le das un archivo `.i` que
describe la interfaz de tu biblioteca C o C++ y te genera los bindings para más de una docena de
lenguajes de golpe. Es la solución del autor de la biblioteca, frente a las de los primos anteriores,
que son las del consumidor.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Aquí vive la única
respuesta radical: no generar el binding, sino **leer la cabecera**.

### Zig

```zig
const std = @import("std");
// @cImport lee doble.h de verdad, en tiempo de compilación. No hay archivo de
// bindings que mantener: la cabecera de C ES el binding.
const c = @cImport(@cInclude("doble.h"));

// El wrapper: adapta el tipo de C (c_long) al del programa (i64).
fn doble(n: i64) i64 {
    return @intCast(c.doble(@intCast(n)));
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \t\r"), 10);
    try std.io.getStdOut().writer().print("envuelto=wrap({d})\n", .{doble(n)});
}
```

### Nim

```nim
import std/strutils

# c2nim traduce doble.h a exactamente esta línea; se genera una vez y se
# versiona como código fuente propio, revisable en un pull request.
proc doble(n: clong): clong {.importc: "doble", dynlib: "libdoble.so".}

proc envolver(n: int): string = "wrap(" & $doble(n.clong) & ")"

echo "envuelto=", envolver(stdin.readLine().strip().parseInt())
```

### D

```d
import std.stdio, std.string, std.conv;

// dstep convierte doble.h en un módulo D como este.
extern (C) long doble(long n);

string envolver(long n) {
    return "wrap(" ~ doble(n).to!string ~ ")";
}

void main() {
    writeln("envuelto=", envolver(readln().strip().to!long));
}
```

**Qué reconocer:** los tres comparten el modelo de memoria de C, así que el binding se reduce a una
declaración, y los tres tienen su generador real: **`c2nim`** para Nim, **`dstep`** para D,
**`bindgen`** para Rust. El patrón es idéntico en todos: la herramienta lee la cabecera, escribe un
archivo de declaraciones y ese archivo pasa a ser tuyo —hay que versionarlo, revisarlo y
**regenerarlo cuando la biblioteca cambie**—. Ese último punto es el coste oculto de todo binding
generado: es una copia, y las copias se desincronizan.

**Zig es el que rompe el patrón**, y es lo más cercano a no escribir binding que existe en esta
página. `@cImport` **lee la cabecera de C directamente durante la compilación** y produce las
declaraciones en memoria: no hay archivo generado, no hay nada que regenerar, no hay copia que se
pueda quedar vieja. Si cambias `doble.h`, la siguiente compilación ya lo sabe. Como además el
compilador de Zig sabe compilar C, la biblioteca y su envoltorio pueden vivir en el mismo proyecto,
con un solo comando de construcción. Nim se acerca por otro camino —compila **a** C, así que
`importc` acaba siendo una llamada de C a C—, pero conserva el archivo intermedio.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia donde el wrapper no es opcional,
porque el modelo de cómputo del otro lado no es el mismo.

### Prolog

```prolog
:- initialization(main, main).
:- use_foreign_library(foreign(doble)).   % el lado C llama a PL_register_foreign

envolver(N, Envuelto) :-
    doble(N, R),                          % el predicado nativo UNIFICA, no devuelve
    format(atom(Envuelto), "wrap(~d)", [R]).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    envolver(N, E),
    format("envuelto=~w~n", [E]).
```

### Datalog

```datalog
% Datalog no tiene funciones, ni efectos, ni forma de llamar a codigo externo:
% no hay nada que envolver. Lo mas cercano a un wrapper es una regla intermedia
% que renombra lo derivado para presentarlo con otro nombre.
entrada(5).

doble(D) :- entrada(N), D = N * 2.
envuelto(D) :- doble(D).
```

**Qué reconocer:** en Prolog el wrapper **no es una comodidad, es una necesidad**, y la firma lo
delata: `doble(N, R)` toma dos argumentos porque un predicado no devuelve nada, unifica su último
argumento. El lado C tiene que construir términos con `PL_unify_integer` en lugar de retornar un
`long`, y encima puede ser llamado varias veces si el motor hace *backtracking*. Ninguna herramienta
automática salva esa distancia, porque la impedancia no es de tipos: es de modelo de cómputo.

SQL enseña la versión de esto que más gente se encuentra en la vida real. Una función de usuario en
PostgreSQL se escribe contra un protocolo, no contra una firma: la función recibe `PG_FUNCTION_ARGS`,
saca sus argumentos con `PG_GETARG_INT32(0)` y devuelve con `PG_RETURN_INT32(...)`; en SQLite es
`sqlite3_create_function`, con un arreglo de `sqlite3_value*` de entrada y `sqlite3_result_int` de
salida. Compara eso con el bloque de Lua del principio de la página: **es la misma forma**. Cuando el
anfitrión es un motor que ejecuta un lenguaje —un intérprete de scripts o una base de datos—, el
binding nunca es una firma: es siempre *toma tus argumentos de esta estructura y deja el resultado en
esta otra*. Y Datalog cierra por el extremo honesto: sin funciones ni efectos, no hay frontera que
cruzar ni, por tanto, nada que envolver.

---

## Y de vuelta a la clase

Veinte lenguajes y una escala continua de trabajo manual: escribir C contra la pila del intérprete
(Lua, Tcl, XS, JNI), declarar la firma en el propio lenguaje (Fiddle, Platypus, JNA, DllImport),
generarla desde la cabecera (SWIG, ffigen, jextract, c2nim, dstep, bindgen) o dejar que el compilador
lea la cabecera y no generar nada (`@cImport`). Lo que ninguno de ellos automatiza es la última capa:
decidir cómo debe **parecer** esa biblioteca desde tu lenguaje. El binding se genera; el wrapper se
diseña.

⏮️ [Volver a la clase 158](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
