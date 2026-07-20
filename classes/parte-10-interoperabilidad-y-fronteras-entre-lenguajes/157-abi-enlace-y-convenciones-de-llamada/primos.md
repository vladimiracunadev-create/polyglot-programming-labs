# 🧬 El mismo programa en las familias de lenguajes — Clase 157

> [⬅️ Volver a la clase 157](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —decidir si dos componentes encajan a nivel de
ABI— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no solo por
los diez lenguajes del núcleo.

El programa en sí es una comparación de dos números. Lo interesante está en los comentarios: cada
primo enseña **qué le ocurre a una función por debajo de su nombre** cuando el compilador la deja en
el archivo objeto. Ese nombre decorado, esa convención de llamada y ese ancho de bits son el ABI.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b`, el ancho de bits de cada componente
- **Salida** (stdout): `abi=compatible` o `abi=incompatible`
- **Regla:** compatible si los dos anchos coinciden

| stdin | esperado |
|---|---|
| `64 64` | `abi=compatible` |
| `64 32` | `abi=incompatible` |
| `32 32` | `abi=compatible` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno de los cinco compila a código máquina, así que ninguno **tiene** ABI propia: la que importa
es la del intérprete, que sí es un programa en C compilado con la de la plataforma.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
puts "abi=#{a == b ? 'compatible' : 'incompatible'}"
```

### Perl

```perl
my ($ancho_a, $ancho_b) = split ' ', <STDIN>;
printf "abi=%s\n", $ancho_a == $ancho_b ? "compatible" : "incompatible";
```

### Lua

```lua
local a, b = io.read("n", "n")
print("abi=" .. (a == b and "compatible" or "incompatible"))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
puts "abi=[expr {$a == $b ? {compatible} : {incompatible}}]"
```

### R

```r
v <- as.integer(strsplit(trimws(readLines("stdin", n = 1)), " +")[[1]])
cat(sprintf("abi=%s\n", if (v[1] == v[2]) "compatible" else "incompatible"))
```

**Qué reconocer:** los cinco escriben la comparación sin declarar un solo tipo, y esa es justamente
la razón por la que el ABI los muerde tan fuerte cuando cruzan a C. Una firma declarada con
`Fiddle`, `FFI::Platypus` o `ctypes` es solo **una promesa en tiempo de ejecución**: nadie la
contrasta con la biblioteca real. Si prometes `long` donde el otro lado espera `int`, no hay error
de compilación —no hay compilación—, hay una lectura de basura o un fallo de segmentación. El propio
Lua lo lleva escrito en su configuración: `lua_Integer` es un alias definido en `luaconf.h`, y una
compilación con enteros de 32 bits y otra con 64 producen **intérpretes con ABI incompatible entre
sí**, aunque el archivo `.lua` sea idéntico. En esta familia el ABI no está en tu código; está en
cómo se compiló el binario que lo ejecuta.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  print('abi=${v[0] == v[1] ? 'compatible' : 'incompatible'}');
}
```

### ActionScript 3

```actionscript
// La AVM2 es un sandbox: no hay stdin ni símbolos nativos que enlazar.
// Aquí solo se ilustra la comparación.
package {
    public class Abi {
        public static function comparar(a:int, b:int):String {
            return "abi=" + (a == b ? "compatible" : "incompatible");
        }
    }
}
```

**Qué reconocer:** Dart es el único primo de la página que le puso **nombre propio** al concepto:
`dart:ffi` incluye una clase `Abi` con valores como `Abi.linuxX64` o `Abi.windowsArm64`, y tipos
como `IntPtr` y `Size` cuyo ancho **no se conoce hasta saber para qué ABI se compila**. Con
`AbiSpecificInteger` puedes declarar que un tipo mide 32 bits en un ABI y 64 en otro. Es exactamente
el problema de esta clase convertido en API. ActionScript marca el contraste opuesto: una máquina
virtual diseñada como sandbox no expone ABI alguna, porque conocer la disposición de los registros
es el primer paso para escapar de ella.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Cuatro lenguajes, un solo formato de enlace:
el del archivo `.class`.

### Kotlin

```kotlin
fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    println("abi=" + if (a == b) "compatible" else "incompatible")
}
```

### Scala

```scala
object Abi {
  def main(args: Array[String]): Unit = {
    val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
    println(s"abi=${if (a == b) "compatible" else "incompatible"}")
  }
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
println "abi=${a == b ? 'compatible' : 'incompatible'}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))]
  (println (str "abi=" (if (= a b) "compatible" "incompatible"))))
```

**Qué reconocer:** **la JVM no tiene ABI de C**, y conviene decirlo así de claro. Tiene su propio
esquema de enlace, y ese esquema es más rico, no más pobre: los símbolos del `.class` conservan el
nombre y el tipo completos —el método `doble` aparece como `doble` con el descriptor `(J)J`— y quien
los resuelve no es el enlazador sino el **cargador de clases**, en tiempo de ejecución. Por eso en la
JVM no existe el *name mangling* al estilo C++: no hace falta codificar la firma en el nombre cuando
el formato ya guarda la firma aparte.

El precio se paga al cruzar. Como no hay ABI de C, hace falta una capa que la fabrique: **JNI**, con
sus símbolos `Java_Clase_metodo` y su puntero `JNIEnv*`, o el **Foreign Function & Memory API** del
proyecto Panama (JEP 454, estable desde Java 22), donde describes la firma con `ValueLayout`. Y ahí
aparece la trampa de esta clase: `ValueLayout.JAVA_LONG` mide **siempre** 64 bits, pero el `long` de
C mide 64 en Linux (modelo LP64) y **32 en Windows** (modelo LLP64). El mismo archivo `.class`,
literalmente idéntico, es compatible en un sistema e incompatible en el otro. Un `long` de Java
nunca cambia de tamaño; un `long` de C sí.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Igual que la JVM: enlace propio, ABI de C prestada.

### F\#

```fsharp
[<EntryPoint>]
let main _ =
    let v = stdin.ReadLine().Trim().Split(' ') |> Array.map int
    printfn "abi=%s" (if v.[0] = v.[1] then "compatible" else "incompatible")
    0
```

### VB.NET

```vbnet
Module Abi
    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Dim a = Integer.Parse(v(0))
        Dim b = Integer.Parse(v(1))
        Console.WriteLine("abi=" & If(a = b, "compatible", "incompatible"))
    End Sub
End Module
```

**Qué reconocer:** el CLR tampoco tiene ABI de C. Los ensamblados se enlazan por **metadatos**
—nombre, espacio de nombres, versión y clave pública— y la frontera con lo nativo la abre
`P/Invoke`, es decir el atributo `DllImport`. Fíjate en lo que ese atributo te obliga a declarar
además del tipo: `CallingConvention`. En Windows conviven dos convenciones históricas y no son
intercambiables. En **`cdecl`**, la del lenguaje C, es **quien llama** el que limpia la pila de
argumentos, lo que permite funciones variádicas como `printf`. En **`stdcall`**, la de la API Win32,
limpia **la función llamada**, que ahorra unas instrucciones por llamada pero exige conocer de
antemano cuántos argumentos hay. Equivocarse de convención no da un error: desequilibra la pila y el
programa muere unas cuantas llamadas después, en un sitio que no tiene nada que ver. El valor por
defecto de `DllImport` es `Winapi`, que en Windows significa `StdCall` —así que declarar una función
de C sin tocar ese campo es el error clásico—. En x86-64 la distinción se desvanece: Win64 define una
sola convención, y `cdecl` y `stdcall` son sinónimos. Es una herencia viva del Windows de 32 bits.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). La familia donde el ABI **es** el tema, porque es la
única que exporta símbolos que todos los demás pueden ver.

### C++

```cpp
#include <iostream>

// Sin extern "C" el símbolo sale decorado. La misma función se exporta como
// _Z14abi_compatibleii con GCC/Clang y como ?abi_compatible@@YA_NHH@Z con MSVC:
// el name mangling NO está estandarizado, cada compilador inventó el suyo.
extern "C" bool abi_compatible(int a, int b) { return a == b; }

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << "abi=" << (abi_compatible(a, b) ? "compatible" : "incompatible") << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

/* Objective-C ES C: el simbolo sale a la tabla como _abi_compatible, sin decorar
   y sin necesitar ningun puente. Los METODOS son otra historia (ver abajo). */
int abi_compatible(int a, int b) { return a == b; }

int main(void) {
    @autoreleasepool {
        int a, b;
        if (scanf("%d %d", &a, &b) != 2) return 1;
        printf("abi=%s\n", abi_compatible(a, b) ? "compatible" : "incompatible");
    }
    return 0;
}
```

**Qué reconocer:** este es **el caso central de la clase**. C++ admite sobrecarga: puedes tener
`doble(int)` y `doble(double)` a la vez. Pero el archivo objeto es una tabla plana de nombres, y en
una tabla plana no caben dos entradas iguales. La solución fue el ***name mangling***: el compilador
codifica los tipos de los parámetros dentro del nombre del símbolo, de modo que las dos sobrecargas
salen como cadenas distintas. `extern "C"` es la instrucción de **no decorar este símbolo** —a cambio
de renunciar a sobrecargarlo—, y por eso toda biblioteca de C++ pensada para ser llamada desde fuera
publica una fachada `extern "C"`.

Lo importante es lo que sigue: **el esquema de decoración nunca se estandarizó**. GCC y Clang siguen
el Itanium C++ ABI, MSVC usa uno propio, y ni siquiera dentro de un compilador está garantizada la
estabilidad: el cambio de `std::string` en GCC 5 (la macro `_GLIBCXX_USE_CXX11_ABI`) produjo dos
mundos de símbolos incompatibles con el mismo código fuente. Por eso nadie distribuye bibliotecas
C++ para consumo general con su interfaz C++ desnuda, y por eso todos los primos de la clase 156
llamaban a C y no a C++.

Objective-C está en el extremo opuesto por una razón sencilla: **es C**, un superconjunto estricto.
Una función C dentro de un `.m` produce el mismo símbolo que produciría en un `.c`, y no hay puente
que construir. El matiz honesto es que un **método** de Objective-C no es un símbolo: es un
`selector` que se resuelve en tiempo de ejecución vía `objc_msgSend`. Objective-C, sin decirlo, se
parece más a la JVM en cómo llama a sus métodos y más a C en cómo exporta sus funciones.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilan a nativo, así
que todos decoran por defecto y todos tienen una palabra para dejar de hacerlo.

### Zig

```zig
const std = @import("std");

// export publica el símbolo con el ABI de C: nombre sin decorar y argumentos
// donde la plataforma dice. El callconv(.C) es explícito aquí por claridad;
// export ya lo implica. Sin export, Zig no garantiza nombre de símbolo alguno.
export fn abi_compatible(a: c_int, b: c_int) callconv(.C) bool {
    return a == b;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    const a = try std.fmt.parseInt(c_int, it.next().?, 10);
    const b = try std.fmt.parseInt(c_int, it.next().?, 10);
    const veredicto = if (abi_compatible(a, b)) "compatible" else "incompatible";
    try std.io.getStdOut().writer().print("abi={s}\n", .{veredicto});
}
```

### Nim

```nim
import std/strutils

# exportc fija el nombre del símbolo (Nim lo renombraría para evitar colisiones);
# cdecl fija la convención de llamada. Hacen falta las dos cosas, son distintas.
proc abiCompatible(a, b: cint): bool {.exportc: "abi_compatible", cdecl.} =
  a == b

let v = stdin.readLine().splitWhitespace()
let a = v[0].parseInt().cint
let b = v[1].parseInt().cint
echo "abi=", (if abiCompatible(a, b): "compatible" else: "incompatible")
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

// extern (C) cambia dos cosas a la vez: el mangling (D tiene el suyo propio,
// tan decorado como el de C++) y la convención de llamada.
extern (C) bool abi_compatible(int a, int b) { return a == b; }

void main() {
    auto v = readln().strip().split().map!(to!int).array;
    writefln("abi=%s", abi_compatible(v[0], v[1]) ? "compatible" : "incompatible");
}
```

**Qué reconocer:** los tres tienen la misma estructura de solución que Rust con
`#[no_mangle] pub extern "C"`, y por el mismo motivo: un lenguaje moderno necesita módulos,
genéricos y sobrecarga, y todo eso obliga a decorar los nombres. Salir de la decoración es siempre
una decisión explícita del programador, nunca el valor por defecto.

Fíjate en que Nim necesita **dos** anotaciones, `exportc` y `cdecl`, y que no son lo mismo: la
primera responde *cómo se llama el símbolo*, la segunda *cómo se pasan los argumentos y quién limpia
la pila*. Un lenguaje puede acertar una y fallar la otra, y el resultado —símbolo encontrado, pila
corrompida— es el fallo más difícil de diagnosticar de toda esta parte del curso. Nim tiene además
el caso más curioso: como compila **a C**, su ABI acaba siendo la que le dé el compilador de C que
uses debajo, con todo lo que eso arrastra. Zig cierra por el otro lado: su compilador conoce los
ABI de las plataformas como objetivo de primera clase (`-target x86_64-windows-gnu` y compañía), y
puede hacer *cross-compilation* precisamente porque el ABI de destino es un dato explícito y no una
propiedad de la máquina donde compilas.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Aquí no hay ABI del lenguaje: hay ABI **del
motor**.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " \t\r", Partes),
    maplist([S, N]>>number_string(N, S), Partes, [A, B]),
    (   A =:= B
    ->  Veredicto = compatible
    ;   Veredicto = incompatible
    ),
    format("abi=~w~n", [Veredicto]).
```

### Datalog

```datalog
% Datalog no tiene E/S: los anchos entran como hechos.
% Fijate en que la compatibilidad no se comprueba con un "=", se comprueba
% usando la MISMA variable W en los dos atomos: es unificacion.
ancho(componente_a, 64).
ancho(componente_b, 64).

abi_compatible :- ancho(componente_a, W), ancho(componente_b, W).
```

**Qué reconocer:** en los declarativos la pregunta de la clase se traslada un nivel: el programa no
tiene ABI, pero el **motor que lo ejecuta** sí, y es con esa con la que hay que ser compatible.
SWI-Prolog carga extensiones nativas que deben exportar `install_<nombre>()` y hablar con
`PL_register_foreign`, y ese `.so` está atado a la versión del intérprete que lo cargará.

El ejemplo más elegante lo da SQL, el representante del núcleo. **SQLite** resuelve el problema sin
depender del enlazador: una extensión cargable no llama a las funciones de SQLite por su nombre, sino
a través de un **puntero a una estructura de punteros a función** (`sqlite3_api_routines`) que el
motor le entrega al cargarla. Como no hay símbolos que resolver, no hay mangling ni convención que
negociar. **PostgreSQL** eligió el camino contrario y lo hizo explícito: todo módulo en C debe
declarar la macro `PG_MODULE_MAGIC`, un bloque con la versión y las opciones de compilación que el
servidor **comprueba al cargar** y rechaza si no coinciden. Son las dos respuestas posibles a esta
clase: o evitas el ABI pasando punteros, o lo declaras y lo verificas. Datalog, por su parte, ni se
plantea la pregunta —no tiene funciones que enlazar—, pero deja de regalo la observación más bonita
de la página: comprobar compatibilidad **es** unificar dos anchos en la misma variable.

---

## Y de vuelta a la clase

Veinte lenguajes, y una sola pregunta bajo el nombre de cada función: **cómo se llama el símbolo,
quién pone los argumentos y dónde, y cuánto mide cada uno**. Los compilados la responden en el
archivo objeto, las máquinas virtuales la evitan con su propio formato de enlace y luego tienen que
fabricarla para cruzar, y los intérpretes la heredan del binario que los ejecuta. Nadie se libra:
solo cambia quién firma el acuerdo.

⏮️ [Volver a la clase 157](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
