# 🧬 El mismo programa en las familias de lenguajes — Clase 163

> [⬅️ Volver a la clase 163](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —un anfitrión pasa dos números a un script incrustado
y recoge lo que el script calcula— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Aquí la comparación se invierte. En el resto del curso preguntamos cómo dice cada lenguaje lo mismo;
en esta clase la pregunta es **quién hospeda a quién**. Y hay un lenguaje que se diseñó entero para
estar en el lado hospedado: Lua.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): `a b` — los datos que el anfitrión pasa al script
- **Salida** (stdout): `resultado=<a+b>` — lo que el script devuelve
- **Regla:** el script incrustado evalúa `a + b`

| stdin | esperado |
|---|---|
| `3 4` | `resultado=7` |
| `10 5` | `resultado=15` |
| `0 0` | `resultado=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Todos traen su propio evaluador dentro: compilar una cadena a código en caliente es parte del
lenguaje, no una biblioteca aparte.

### Ruby

```ruby
a, b = STDIN.gets.split.map(&:to_i)
script = "a + b"
puts "resultado=#{eval(script, binding)}"
```

### Perl

```perl
my ($x, $y) = split ' ', <STDIN>;
my $script = '$x + $y';
my $resultado = eval $script;
printf "resultado=%d\n", $resultado;
```

### Lua

```lua
local a, b = io.read("n", "n")
local script = load("return a + b", "script", "t", {a = a, b = b})
print(string.format("resultado=%d", script()))
```

### Tcl

```tcl
gets stdin linea
lassign [split $linea] a b
set script {expr {$a + $b}}
puts "resultado=[eval $script]"
```

### R

```r
v <- as.integer(strsplit(readLines("stdin", n = 1), " ")[[1]])
entorno <- list2env(list(a = v[1], b = v[2]))
resultado <- eval(parse(text = "a + b"), entorno)
cat(sprintf("resultado=%d\n", resultado))
```

**Qué reconocer:** los cinco tienen `eval`, pero fíjate en el **cuarto argumento de `load` en Lua**:
`{a = a, b = b}`. Ese hash es el entorno completo del script — no hereda las globales del anfitrión,
así que el código incrustado no ve nada que no le hayas puesto delante. Ruby con `binding` y R con
`list2env` hacen lo mismo con más ceremonia; Perl con `eval` de cadena no lo hace en absoluto y el
script pisa el ámbito entero.

Ese detalle es el resumen de por qué Lua ganó esta categoría. Se diseñó en 1993 en la PUC-Rio
**como lenguaje de configuración incrustado**, no como lenguaje de propósito general que además se
puede incrustar. Todo lo demás sigue de ahí: el intérprete son unos 30 000 renglones de C ANSI
portable, cabe en unos cientos de kilobytes, y arranca con `luaL_newstate()` en microsegundos. Tcl
compartía exactamente esa ambición —su nombre es *Tool Command Language*, un lenguaje pegamento para
incrustar en herramientas C— y perdió, aunque sigue vivo dentro de herramientas de diseño de chips.
Python y PHP se incrustan también (`Py_Initialize`, la SAPI `embed`), pero arrastran su instalación
completa: es la diferencia entre invitar a alguien a tu casa y mudarte con él.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) ·
[TypeScript](README.md#typescript). JavaScript es el otro gran lenguaje hospedado: V8 y
JavaScriptCore son motores pensados para vivir dentro de otro programa.

### Dart

```dart
import 'dart:io';

// Dart compilado AOT no tiene eval: no puede compilar codigo en ejecucion.
// Lo mas cercano es registrar de antemano las operaciones permitidas.
void main() {
  final v = stdin.readLineSync()!.trim().split(RegExp(r'\s+')).map(int.parse).toList();
  final scripts = <String, int Function(int, int)>{'a + b': (a, b) => a + b};
  print('resultado=${scripts['a + b']!(v[0], v[1])}');
}
```

### ActionScript 3

```actionscript
// AS3 elimino el eval() que si tenia AS2, y no tiene stdin:
// se ilustra la funcion registrada que el anfitrion invocaria.
package {
    public class Suma {
        public static function resultado(a:int, b:int):String {
            return "resultado=" + (a + b);
        }
    }
}
```

**Qué reconocer:** los dos primos de esta familia **perdieron** la capacidad que define la clase, y
por la misma razón: compilar de antemano. Dart quitó `dart:mirrors` de sus builds AOT y con él la
posibilidad de evaluar código nuevo; AS3 retiró el `eval` que AS2 tenía. Ambos ofrecen el patrón que
verás cada vez que un lenguaje no puede evaluar: **una tabla de operaciones registradas**, donde el
"script" no es código sino una clave. Es menos potente y bastante más seguro, y es justo el
compromiso que hace un motor de juegos cuando prefiere no incrustar nada.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La JVM estandarizó el hospedaje con
**JSR-223** (`javax.script`), la interfaz genérica para meter cualquier lenguaje dentro de una app
Java.

### Kotlin

```kotlin
import javax.script.ScriptEngineManager

fun main() {
    val (a, b) = readLine()!!.trim().split(Regex("\\s+")).map { it.toInt() }
    // Necesita kotlin-scripting-jsr223 en el classpath: el compilador viaja con la app.
    val motor = ScriptEngineManager().getEngineByExtension("kts")!!
    motor.put("a", a)
    motor.put("b", b)
    val resultado = motor.eval("(bindings[\"a\"] as Int) + (bindings[\"b\"] as Int)")
    println("resultado=$resultado")
}
```

### Scala

```scala
import javax.script.ScriptEngineManager

object Suma extends App {
  val Array(a, b) = scala.io.StdIn.readLine().trim.split("\\s+").map(_.toInt)
  // El motor JSR-223 de Scala arrastra scala-compiler entero y exige
  // declarar el tipo de cada binding antes de evaluar.
  val motor = new ScriptEngineManager().getEngineByName("scala")
  motor.put("a", a)
  motor.put("b", b)
  println(s"resultado=${motor.eval("a + b")}")
}
```

### Groovy

```groovy
def (a, b) = System.in.newReader().readLine().trim().split(/\s+/)*.toInteger()
def shell = new GroovyShell(new Binding(a: a, b: b))
println "resultado=${shell.evaluate('a + b')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [[a b] (map parse-long (str/split (str/trim (read-line)) #"\s+"))
      script (list '+ a b)]
  (println (str "resultado=" (eval script))))
```

**Qué reconocer:** Groovy es el Lua de la JVM y `GroovyShell` lo demuestra: tres líneas, un
`Binding` explícito con las variables que el script puede ver, y ya está — por eso Jenkins, Gradle y
media industria Java usan Groovy como lenguaje de configuración ejecutable. Clojure va aún más
lejos y borra la frontera: el script no es una cadena que hay que analizar, es **una lista**,
`(+ 3 4)`, un dato del propio lenguaje que `eval` acepta directamente. Eso es homoiconicidad, y
convierte a cualquier programa Clojure en su propio anfitrión. Kotlin y Scala pueden hacerlo, pero
al precio de incrustar su compilador completo en la aplicación: decenas de megabytes y arranques de
segundos frente a los microsegundos de `luaL_newstate()`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
// F# Interactive se puede incrustar con FSharp.Compiler.Service, pero eso
// significa enviar el compilador entero dentro de la aplicacion.
let scripts = dict [ "a + b", (+) ]
let [| a; b |] = stdin.ReadLine().Trim().Split(' ') |> Array.map int
printfn "resultado=%d" (scripts.["a + b"] a b)
```

### VB.NET

```vbnet
Module Suma
    ' VB.NET no tiene eval. El VB incrustado de verdad fue VBA/VBScript,
    ' un motor separado que las aplicaciones hospedaban; VB.NET no lo heredo.
    Function Ejecutar(script As String, a As Integer, b As Integer) As Integer
        Select Case script
            Case "a + b" : Return a + b
            Case Else : Throw New NotSupportedException(script)
        End Select
    End Function

    Sub Main()
        Dim v = Console.ReadLine().Trim().Split(" "c)
        Console.WriteLine("resultado=" & Ejecutar("a + b", Integer.Parse(v(0)), Integer.Parse(v(1))))
    End Sub
End Module
```

**Qué reconocer:** .NET tiene la historia más irónica de esta clase. **VBA fue el lenguaje incrustado
de mayor éxito comercial de todos los tiempos** —cientos de millones de instalaciones de Office con
un intérprete de Basic dentro, hospedando macros— y su heredero, VB.NET, no puede evaluar una cadena.
La capacidad no se hereda con el nombre: se perdió al pasar a un runtime compilado y con tipos
verificados. F# y C# la recuperan a través de Roslyn y FSharp.Compiler.Service, que son el compilador
publicado como biblioteca. Funciona, pero el modelo es el opuesto al de Lua: en vez de un intérprete
diminuto que cabe en tu binario, te llevas la toolchain.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). **Aquí está la clave de toda la clase**: la API de
Lua es una API de C, y por eso Lua entra en cualquier sitio donde entre C.

### C++

```cpp
#include <iostream>
#include <lua.hpp>

int main() {
    long long a = 0, b = 0;
    std::cin >> a >> b;

    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    lua_pushinteger(L, a);
    lua_setglobal(L, "a");
    lua_pushinteger(L, b);
    lua_setglobal(L, "b");
    luaL_dostring(L, "resultado = a + b");
    lua_getglobal(L, "resultado");
    std::cout << "resultado=" << lua_tointeger(L, -1) << '\n';
    lua_close(L);
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>
#import <JavaScriptCore/JavaScriptCore.h>

int main(void) {
    @autoreleasepool {
        long long a = 0, b = 0;
        if (scanf("%lld %lld", &a, &b) != 2) return 1;
        JSContext *ctx = [[JSContext alloc] init];
        ctx[@"a"] = @(a);
        ctx[@"b"] = @(b);
        JSValue *r = [ctx evaluateScript:@"a + b"];
        printf("resultado=%lld\n", (long long)[r toInt32]);
    }
    return 0;
}
```

**Qué reconocer:** mira la forma del código C++ y entenderás por qué Lua está dentro de World of
Warcraft, Roblox, Redis, nginx, Neovim y casi todos los motores de videojuegos. **Toda la
comunicación entre los dos lenguajes pasa por una pila**: `lua_pushinteger` empuja un valor,
`lua_setglobal` lo saca y le pone nombre, `lua_tointeger(L, -1)` lee el tope. No hay tipos
compartidos, ni estructuras que deban coincidir en memoria, ni un generador de bindings. Solo empujar
y sacar valores de una pila, que es la operación más simple que dos lenguajes pueden acordar — y por
eso funciona igual desde C, C++, Rust, Zig o cualquier cosa que sepa llamar a C.

Objective-C enseña la variante Apple del mismo patrón: `JSContext` incrusta JavaScriptCore, y el
puente es tan liso que asignar `ctx[@"a"]` se parece a escribir en un diccionario. La diferencia es
el tamaño de lo que hospedas: JavaScriptCore es un motor JIT de varios megabytes con equipo dedicado
detrás; Lua es un archivo `.c` que puedes leer entero en una tarde.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin
evaluador dentro; si quieren un script, lo hospedan.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    var it = std.mem.tokenizeScalar(u8, std.mem.trim(u8, linea, " \r"), ' ');
    const a = try std.fmt.parseInt(i64, it.next().?, 10);
    const b = try std.fmt.parseInt(i64, it.next().?, 10);
    // Zig evalua codigo en tiempo de COMPILACION (comptime), nunca en ejecucion.
    // Para hospedar un script se incrusta Lua con @cImport("lua.h").
    try std.io.getStdOut().writer().print("resultado={d}\n", .{a + b});
}
```

### Nim

```nim
import std/strutils

let v = stdin.readLine().splitWhitespace()
let a = parseInt(v[0])
let b = parseInt(v[1])
# NimScript es Nim interpretado por la VM del propio compilador; esa VM se
# puede incrustar en una aplicacion enlazando el paquete `compiler`.
echo "resultado=", a + b
```

### D

```d
import std.stdio, std.array, std.conv, std.algorithm, std.string;

void main() {
    auto v = readln().strip().split().map!(to!long).array;
    // `mixin` compila una cadena como codigo D, pero en tiempo de COMPILACION:
    // el script tiene que ser conocido antes de que el programa arranque.
    enum script = "v[0] + v[1]";
    writefln("resultado=%d", mixin(script));
}
```

**Qué reconocer:** los tres tienen evaluación de código, y los tres la tienen **en el momento
equivocado para esta clase**. `comptime` de Zig, la VM de NimScript y el `mixin` de D ejecutan
código durante la compilación, no mientras el programa corre: sirven para generar código, no para
hospedar a un usuario que escribe un script después. La distinción es exactamente la de esta clase.
Y el desenlace es unánime: cuando un lenguaje de sistemas necesita scripting en ejecución, no lo
inventa — incrusta Lua. Zig lo hace con `@cImport`, Rust con `mlua` o `rlua`, Go con
`gopher-lua`. La API de pila en C es el mínimo común denominador que todos saben hablar.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL es el lenguaje incrustado más usado del
planeta y casi nunca lo llamamos así: cada aplicación con base de datos hospeda un intérprete de
consultas.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", "", [SA, SB]),
    number_string(A, SA),
    number_string(B, SB),
    % El "script" es un termino de datos: A + B no se evalua hasta que `is` lo pide.
    Script = A + B,
    Resultado is Script,
    format("resultado=~d~n", [Resultado]).
```

### Datalog

```datalog
% Datalog no evalua codigo ni tiene E/S: no hay anfitrion ni script que hospedar.
% Los datos entran como hechos y la regla los combina.
entrada(3, 4).

resultado(R) :- entrada(A, B), R = A + B.
```

**Qué reconocer:** Prolog llega al mismo sitio que Clojure por otro camino. `Script = A + B` no
suma nada: construye un **término**, una estructura de datos con el functor `+` y dos argumentos, que
se queda ahí inerte hasta que `is` decide evaluarlo. Programa y dato son la misma cosa, así que
Prolog puede construir y ejecutar consultas nuevas sin ningún mecanismo extra — la razón de que
SWI-Prolog se incruste en sistemas expertos con una API en C parecida en espíritu a la de Lua.
Datalog es el único de los veinte que no puede participar ni como anfitrión ni como huésped: sin
efectos, sin E/S y sin evaluación dinámica, no hay nada que hospedar. Su renuncia es la misma que la
de SQL, llevada un paso más allá.

---

## Y de vuelta a la clase

Veinte lenguajes y una sola suma, pero la pregunta de esta clase parte la lista en tres: los que
traen evaluador de serie (los dinámicos, Groovy, Clojure, Prolog), los que hospedan a otro porque no
lo traen (C, C++, Zig, Rust, Go, Objective-C) y los que perdieron la capacidad al compilar de
antemano (Dart, AS3, VB.NET). Y en el medio, un lenguaje que existe precisamente para ocupar el hueco
que los demás dejan: Lua no es popular a pesar de ser pequeño, sino **porque** lo es.

⏮️ [Volver a la clase 163](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
