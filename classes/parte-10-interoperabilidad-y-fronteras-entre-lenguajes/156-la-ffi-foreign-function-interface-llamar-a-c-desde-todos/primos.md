# 🧬 El mismo programa en las familias de lenguajes — Clase 156

> [⬅️ Volver a la clase 156](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —llamar a una función que vive fuera del lenguaje—
resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por los
diez lenguajes del núcleo.

Aquí hay algo que ninguna otra clase tiene: los veinte programas apuntan al **mismo destino**. C es
el idioma franco de la interoperabilidad, y lo que cambia de un primo a otro no es el objetivo sino
el puente. Léelos como veinte respuestas distintas a la misma pregunta: *¿cómo cruzo?*

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

Casi todos los bloques suponen esta biblioteca compartida al lado, que es la función "externa" que
se quiere llamar:

```c
/* doble.c → cc -shared -fPIC doble.c -o libdoble.so */
long doble(long x) { return x * 2; }
```

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** llamar a `doble(n)`, que vive fuera del lenguaje anfitrión

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia con más motivos para cruzar: son lenguajes lentos, con intérpretes escritos en C, cuyo
rendimiento real depende de que las partes calientes estén del otro lado de la frontera.

### Ruby

```ruby
# Fiddle está en la biblioteca estándar: no hace falta compilar nada en C.
require "fiddle"
require "fiddle/import"

module Nativa
  extend Fiddle::Importer
  dlload "./libdoble.so"
  extern "long doble(long)"
end

n = STDIN.gets.to_i
puts "resultado=#{Nativa.doble(n)}"
```

### Perl

```perl
# FFI::Platypus declara la firma en tiempo de ejecución; XS la compilaría.
use FFI::Platypus 2.00;

my $ffi = FFI::Platypus->new(api => 2, lib => './libdoble.so');
$ffi->attach(doble => ['long'] => 'long');

my $n = <STDIN>;
printf "resultado=%d\n", doble($n);
```

### Lua

```lua
-- doble.so aquí es un módulo C escrito contra la API de pila de Lua:
--   static int l_doble(lua_State *L) {
--       lua_Integer x = luaL_checkinteger(L, 1);   -- saca el argumento de la pila
--       lua_pushinteger(L, x * 2);                 -- deja el resultado en la pila
--       return 1;                                  -- cuántos valores devuelve
--   }
local nativa = require("doble")
local n = tonumber(io.read("l"))
print("resultado=" .. nativa.doble(n))
```

### Tcl

```tcl
# load llama a Doble_Init, que registra el comando con Tcl_CreateObjCommand.
load ./libdoble.so Doble
gets stdin n
puts "resultado=[doble $n]"
```

### R

```r
# .Call entra en la API C de R: doble_r recibe y devuelve SEXP, el tipo universal.
dyn.load("libdoble.so")
n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("resultado=%d\n", .Call("doble_r", n)))
```

**Qué reconocer:** los cinco cargan una biblioteca por su nombre en disco y le piden un símbolo, pero
la forma del puente delata para qué se diseñó cada lenguaje. Ruby y Perl **declaran la firma** desde
el propio lenguaje (`Fiddle`, `FFI::Platypus`) y por eso no exigen compilar nada; Perl también
conserva el camino antiguo, XS, que sí genera y compila C. R obliga a que la función del otro lado
hable su moneda interna, el `SEXP`, porque todo valor de R es un objeto del intérprete.

Y luego está **Lua**, que es el caso más ilustrativo de toda la tanda. Lua no tiene una FFI que
imite firmas de C: tiene una **pila** compartida entre el intérprete y el código C. El lado C no
recibe argumentos ni devuelve un valor al estilo normal, sino que **saca** los argumentos de la pila
con `luaL_checkinteger` y **empuja** el resultado con `lua_pushinteger`, devolviendo cuántos valores
dejó. Esa disciplina de pila no es un detalle de implementación: es la razón de ser del lenguaje. Lua
nació para ser **incrustado** dentro de un programa en C —un motor de videojuego, un servidor web, un
editor—, y por eso su frontera con C no está en un rincón de la biblioteca estándar, sino en el
centro del diseño. Los demás primos añadieron un puente hacia C; Lua **es** el puente.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:ffi';
import 'dart:io';

typedef DobleC = Int64 Function(Int64);       // la firma tal como la ve C
typedef DobleDart = int Function(int);        // la firma tal como la ve Dart

void main() {
  final lib = DynamicLibrary.open('./libdoble.so');
  final doble = lib.lookupFunction<DobleC, DobleDart>('doble');
  final n = int.parse(stdin.readLineSync()!.trim());
  print('resultado=${doble(n)}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 no tiene stdin ni FFI: el reproductor es una caja cerrada.
// En AIR el único puente a código nativo son las ANE (Adobe Native Extensions),
// que empaquetan la biblioteca aparte. Aquí solo se ilustra el cálculo.
package {
    public class Ffi {
        public static function doble(n:int):String {
            return "resultado=" + (n * 2);
        }
    }
}
```

**Qué reconocer:** `dart:ffi` obliga a escribir la firma **dos veces** —una con los tipos de C
(`Int64`) y otra con los de Dart (`int`)— porque el compilador necesita saber a la vez cómo se
empaquetan los argumentos en registros y cómo se ven desde el lenguaje. Es la separación entre ABI y
tipos que la clase 157 hará explícita. ActionScript marca el contraste: un lenguaje cuya máquina
virtual fue diseñada como *sandbox* no puede tener FFI, porque llamar a C es precisamente lo que un
sandbox existe para impedir. En el navegador, JavaScript vive la misma restricción, y por eso su
puente moderno no es C sino WebAssembly.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Un solo mecanismo para todos los lenguajes de
la plataforma: lo que sirve a Java sirve a Kotlin, Scala, Groovy y Clojure sin cambios.

### Kotlin

```kotlin
// JNI: el símbolo del lado C debe llamarse Java_MainKt_doble, con esa decoración exacta.
external fun doble(n: Long): Long

fun main() {
    System.loadLibrary("doble")
    val n = readLine()!!.trim().toLong()
    println("resultado=${doble(n)}")
}
```

### Scala

```scala
// Foreign Function & Memory API (proyecto Panama, JEP 454, estable desde Java 22):
// llama a la libdoble.so sin escribir una sola línea de C.
import java.lang.foreign.{Arena, FunctionDescriptor, Linker, SymbolLookup, ValueLayout}

object Ffi {
  def main(args: Array[String]): Unit = {
    val arena = Arena.ofConfined()
    val lib = SymbolLookup.libraryLookup("./libdoble.so", arena)
    val doble = Linker.nativeLinker().downcallHandle(
      lib.find("doble").orElseThrow(),
      FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.JAVA_LONG))
    val n = scala.io.StdIn.readLine().trim.toLong
    val r = doble.invokeWithArguments(n).asInstanceOf[Long]
    println(s"resultado=$r")
  }
}
```

### Groovy

```groovy
@Grab('net.java.dev.jna:jna:5.14.0')
import com.sun.jna.Library
import com.sun.jna.Native

interface Nativa extends Library {
    long doble(long n)
}

def nativa = Native.load('doble', Nativa)
def n = System.in.newReader().readLine().trim() as long
println "resultado=${nativa.doble(n)}"
```

### Clojure

```clojure
;; JNA sin declarar interfaces: el símbolo se resuelve en tiempo de ejecución.
(import '[com.sun.jna Function])

(let [doble (Function/getFunction "doble" "doble")
      n (Long/parseLong (.trim (read-line)))]
  (println (str "resultado=" (.invokeLong doble (to-array [n])))))
```

**Qué reconocer:** el mecanismo histórico es **JNI**, y su precio se ve en el comentario de Kotlin:
no basta con que exista una función `doble` en C, tiene que llamarse `Java_MainKt_doble` y aceptar
un puntero al entorno de la JVM. JNI no llama a C, obliga a **escribir C para la JVM**. JNA fue la
respuesta de la comunidad —declarar la interfaz en Java y que la biblioteca haga el resto—, y el
**Foreign Function & Memory API** (proyecto Panama, JEP 454, estable en Java 22) es la respuesta
oficial: un `Linker`, un `FunctionDescriptor` que describe la firma con `ValueLayout`, y una `Arena`
que gobierna la vida de la memoria fuera del recolector de basura. Los cuatro lenguajes usan
exactamente las mismas clases porque, en la JVM, la frontera pertenece a la plataforma y no al
lenguaje.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Un solo mecanismo, `P/Invoke`, para toda la
plataforma.

### F\#

```fsharp
open System.Runtime.InteropServices

[<DllImport("doble", CallingConvention = CallingConvention.Cdecl)>]
extern int64 doble(int64 n)

[<EntryPoint>]
let main _ =
    let n = int64 (stdin.ReadLine().Trim())
    printfn "resultado=%d" (doble n)
    0
```

### VB.NET

```vbnet
Imports System.Runtime.InteropServices

Module Ffi
    <DllImport("doble", CallingConvention:=CallingConvention.Cdecl)>
    Private Function doble(n As Long) As Long
    End Function

    Sub Main()
        Dim n = Long.Parse(Console.ReadLine().Trim())
        Console.WriteLine("resultado=" & doble(n))
    End Sub
End Module
```

**Qué reconocer:** el mismo atributo `DllImport` y la misma función declarada **sin cuerpo** en los
dos lenguajes: el cuerpo lo pone el enlazador en tiempo de ejecución. Esto es `P/Invoke`, y es el
único puente que hace falta en .NET porque el CLR es quien marshalea, no el lenguaje. Fíjate en
`CallingConvention.Cdecl`: la plataforma te pide declarar **cómo** se pasan los argumentos, no solo
de qué tipo son. Ese parámetro es el tema íntegro de la clase 157, y aquí aparece como un argumento
más de un atributo.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia que no necesita puente, porque es la
orilla a la que llegan todos los demás.

### C++

```cpp
#include <iostream>

// extern "C" apaga el name mangling: sin él, el enlazador buscaría _Z5doblel.
extern "C" long doble(long);

int main() {
    long n;
    std::cin >> n;
    std::cout << "resultado=" << doble(n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

/* Objective-C ES C: la funcion se declara y se llama sin ninguna ceremonia. */
long doble(long x) { return x * 2; }

int main(void) {
    @autoreleasepool {
        long n;
        if (scanf("%ld", &n) != 1) return 1;
        printf("resultado=%ld\n", doble(n));
    }
    return 0;
}
```

**Qué reconocer:** aquí la palabra clave es "ninguna". Objective-C no necesita FFI hacia C porque
**es** C: un archivo `.m` puede contener funciones C, punteros C y `printf` sin cambiar de registro.
C++ está a un milímetro, y ese milímetro se llama *name mangling*: como C++ admite sobrecarga, el
compilador decora los nombres con la firma, y `extern "C"` es la instrucción de no decorar este. Por
eso todas las bibliotecas de C++ que quieren ser llamadas desde fuera exponen una fachada
`extern "C"` — y por eso todos los primos de esta página llaman a C y no a C++ directamente.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilan a binario
nativo, así que su frontera con C es un enlace, no una traducción.

### Zig

```zig
const std = @import("std");
// @cImport lee la cabecera de C de verdad: sin bindings, sin generador, sin declarar la firma.
const c = @cImport(@cInclude("doble.h"));

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(c_long, std.mem.trim(u8, linea, " \r"), 10);
    try std.io.getStdOut().writer().print("resultado={d}\n", .{c.doble(n)});
}
```

### Nim

```nim
import std/strutils

# importc dice "este símbolo ya existe en C"; dynlib, dónde buscarlo.
proc doble(n: clong): clong {.importc: "doble", dynlib: "libdoble.so".}

let n = stdin.readLine().strip().parseInt().clong
echo "resultado=", doble(n)
```

### D

```d
import std.stdio, std.string, std.conv;

extern (C) long doble(long n);   // declarada aquí, definida en libdoble.so

void main() {
    long n = readln().strip().to!long;
    writefln("resultado=%d", doble(n));
}
```

**Qué reconocer:** los tres declaran la función en una sola línea, sin biblioteca intermedia, porque
comparten con C el modelo de memoria y el mismo ABI de la plataforma. Zig va un paso más allá que
cualquier otro primo de la página: `@cImport` **lee la cabecera de C directamente** y genera las
declaraciones en tiempo de compilación, y el propio compilador de Zig sabe compilar C. Donde los
demás mantienen un archivo de bindings que se desincroniza, Zig y D tratan la cabecera de C como
código fuente propio. Nim, que compila a C, lo tiene aún más fácil: `importc` acaba siendo una
llamada C a C.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). La familia que se queda al margen de esta clase,
y conviene decirlo sin adornos.

### Prolog

```prolog
:- initialization(main, main).
:- use_foreign_library(foreign(doble)).   % el lado C llama a PL_register_foreign

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    doble(N, R),
    format("resultado=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene FFI ni efectos: no puede llamar a C bajo ningún mecanismo.
% Lo más cercano es derivar el resultado con una regla dentro del propio programa.
entrada(5).

resultado(R) :- entrada(N), R = N * 2.
```

**Qué reconocer:** **esta familia queda fuera del tema de la clase**, y por razones distintas cada
una. SWI-Prolog sí tiene interfaz con C, pero fíjate en la firma: `doble(N, R)` toma **dos**
argumentos, porque en Prolog una función no devuelve, **unifica**; el lado C tiene que construir
términos con `PL_unify_integer` en vez de retornar un `long`. La impedancia no es de tipos, es de
modelo de cómputo. Datalog directamente no puede: sin E/S y sin efectos, no hay nada que llamar.
Y SQL, el representante del núcleo, tampoco tiene FFI propia: las funciones definidas por el usuario
las carga el **motor** (`CREATE FUNCTION ... LANGUAGE C` en PostgreSQL), no el lenguaje. En los
declarativos, cruzar a C es una decisión del intérprete, no del programa.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo destino. Unos declaran la firma en su propio código, otros exigen escribir
C a su medida, uno lee la cabecera de C tal cual, y uno —Lua— hizo de la frontera su arquitectura.
Lo transferible es la pregunta que hay debajo de todos: **quién describe la firma, quién reserva la
memoria y quién decide cómo se pasan los argumentos**. Las dos clases siguientes responden esa última
parte.

⏮️ [Volver a la clase 156](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
