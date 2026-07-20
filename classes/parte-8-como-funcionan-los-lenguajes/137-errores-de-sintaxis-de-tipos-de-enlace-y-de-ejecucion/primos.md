# 🧬 El mismo programa en las familias de lenguajes — Clase 137

> [⬅️ Volver a la clase 137](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —traducir un código de 1 a 4 al nombre de la clase de
error correspondiente— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El programa es deliberadamente trivial porque lo que se compara aquí no es el código sino **cuándo**
cada lenguaje descubre que algo está mal. Las cuatro clases de la clase —sintaxis, tipos, enlace,
ejecución— no existen en todos: hay lenguajes sin fase de enlace, lenguajes que no comprueban tipos
nunca, y uno, Prolog, en el que "no funcionó" ni siquiera es un error, sino un **fallo lógico**. Cada
bloque lleva en un comentario la herramienta con la que esa comunidad adelanta el diagnóstico.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `codigo` de 1 a 4
- **Salida** (stdout): `error=<sintaxis|tipos|enlace|ejecucion>`
- **Regla:** `1→sintaxis`, `2→tipos`, `3→enlace`, `4→ejecucion`

| stdin | esperado |
|---|---|
| `1` | `error=sintaxis` |
| `3` | `error=enlace` |
| `4` | `error=ejecucion` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Sin compilación separada, la sintaxis se comprueba al cargar y los tipos no se comprueban nunca: casi
todo lo que puede fallar, falla en ejecución. De ahí que la familia entera haya inventado
herramientas externas para adelantar el diagnóstico.

### Ruby

```ruby
# `ruby -c archivo.rb` comprueba la sintaxis sin ejecutar nada; `ruby -w` avisa
# de variables no usadas y métodos redefinidos. De tipos, nada: eso es ejecución.
NOMBRES = { 1 => "sintaxis", 2 => "tipos", 3 => "enlace", 4 => "ejecucion" }.freeze

codigo = STDIN.gets.to_i
puts "error=#{NOMBRES.fetch(codigo, 'desconocido')}"
```

### Perl

```perl
use strict;
use warnings;

# `perl -c` compila sin ejecutar. `use strict` convierte en error de COMPILACIÓN
# el uso de una variable no declarada, que sin él sería un fallo silencioso.
my %nombres = (1 => 'sintaxis', 2 => 'tipos', 3 => 'enlace', 4 => 'ejecucion');

chomp(my $codigo = <STDIN>);
print "error=", ($nombres{$codigo} // 'desconocido'), "\n";
```

### Lua

```lua
-- `luac -p` valida la sintaxis; `luacheck` es el analizador de la comunidad y
-- caza lo que el intérprete jamás vería: globales por error, variables sin usar.
local nombres = { "sintaxis", "tipos", "enlace", "ejecucion" }

local codigo = tonumber(io.read("l"))
print("error=" .. (nombres[codigo] or "desconocido"))
```

### Tcl

```tcl
# Tcl compila cada cuerpo a bytecode la primera vez que lo ejecuta: un error de
# sintaxis en una rama que nunca se toma NO se descubre jamás.
array set nombres {1 sintaxis 2 tipos 3 enlace 4 ejecucion}

set codigo [string trim [gets stdin]]
if {[info exists nombres($codigo)]} {
    puts "error=$nombres($codigo)"
} else {
    puts "error=desconocido"
}
```

### R

```r
# R analiza el fichero entero antes de evaluarlo: la sintaxis se ve al cargar.
# `R CMD check` y `lintr` añaden la capa de análisis que el lenguaje no tiene.
nombres <- c("sintaxis", "tipos", "enlace", "ejecucion")

codigo <- as.integer(readLines("stdin", n = 1))
cat(sprintf("error=%s\n", if (!is.na(codigo) && codigo %in% 1:4) nombres[codigo] else "desconocido"))
```

**Qué reconocer:** de las cuatro clases de error, esta familia solo tiene dos de verdad —sintaxis y
ejecución—, y por eso todos sus lenguajes ofrecen un modo "compila pero no ejecutes": `ruby -c`,
`perl -c`, `luac -p`. El caso de Perl es el más didáctico: `use strict` **mueve** un error de la
columna de ejecución a la de compilación, y esa es exactamente la operación que un lenguaje de tipos
estáticos hace por defecto. Tcl marca el extremo opuesto y merece que se diga claro: como compila
perezosamente cada bloque al ejecutarlo, un error de sintaxis puede vivir para siempre en una rama
que nunca se toma. La fase de enlace, en toda esta familia, simplemente no existe.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
La pareja del núcleo ya ilustra el eje entero: el mismo programa, con y sin comprobación de tipos
antes de ejecutar.

### Dart

```dart
import 'dart:io';

// `dart analyze` reporta sintaxis Y tipos antes de ejecutar. El enlace no es una
// fase visible: el compilador ve el programa completo y resuelve todo de una vez.
void main() {
  const nombres = {1: 'sintaxis', 2: 'tipos', 3: 'enlace', 4: 'ejecucion'};
  final codigo = int.parse(stdin.readLineSync()!.trim());
  print('error=${nombres[codigo] ?? 'desconocido'}');
}
```

### ActionScript 3

```actionscript
// El compilador de ActionScript comprueba los tipos declarados (`:int`), pero el
// lenguaje no tiene stdin: se ilustra solo la clasificación.
package {
    public class Clasificador {
        public static function clasificar(codigo:int):String {
            switch (codigo) {
                case 1: return "error=sintaxis";
                case 2: return "error=tipos";
                case 3: return "error=enlace";
                case 4: return "error=ejecucion";
            }
            return "error=desconocido";
        }
    }
}
```

**Qué reconocer:** los dos hacen lo que TypeScript hizo con JavaScript —añadir una fase de tipos
antes de ejecutar— pero por vías distintas. Dart la lleva en el propio compilador y con *null
safety*: `nombres[codigo]` devuelve un tipo anulable y el compilador **exige** el `??`, así que un
`NullPointerException` clásico se convierte en error de tipos. ActionScript fue el intento anterior
de lo mismo sobre ECMAScript, con anotaciones `:int` verificadas al compilar. Ninguno tiene fase de
enlace separada, y esa ausencia es lo que distingue a la familia web de la familia C.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Aquí sí existe algo parecido al enlace, pero
ocurre **en ejecución**: la JVM resuelve y verifica cada clase la primera vez que la necesita.

### Kotlin

```kotlin
fun main() {
    // El compilador de Kotlin rechaza al compilar lo que en Java sería un
    // NullPointerException: mueve errores de ejecución a la columna de tipos.
    val codigo = readLine()!!.trim().toInt()
    val nombre = when (codigo) {
        1 -> "sintaxis"
        2 -> "tipos"
        3 -> "enlace"
        4 -> "ejecucion"
        else -> "desconocido"
    }
    println("error=$nombre")
}
```

### Scala

```scala
object Errores extends App {
  // Sobre un tipo sellado, el compilador avisa si el `match` no es exhaustivo:
  // un caso olvidado deja de ser una sorpresa en ejecución.
  val codigo = scala.io.StdIn.readLine().trim.toInt
  val nombre = codigo match {
    case 1 => "sintaxis"
    case 2 => "tipos"
    case 3 => "enlace"
    case 4 => "ejecucion"
    case _ => "desconocido"
  }
  println(s"error=$nombre")
}
```

### Groovy

```groovy
// Groovy compila a bytecode pero despacha los métodos en ejecución: un nombre
// mal escrito no es error de compilación, es `MissingMethodException` al correr.
// `@CompileStatic` en la clase cambia esto y activa la comprobación estática.
def nombres = [1: 'sintaxis', 2: 'tipos', 3: 'enlace', 4: 'ejecucion']

def codigo = System.in.newReader().readLine().trim() as int
println "error=${nombres.getOrDefault(codigo, 'desconocido')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

;; Clojure comprueba la sintaxis al LEER cada forma, y un símbolo que no resuelve
;; sí es error de compilación. Los tipos, casi nunca: eso llega en ejecución.
(def nombres {1 "sintaxis" 2 "tipos" 3 "enlace" 4 "ejecucion"})

(let [codigo (Long/parseLong (str/trim (read-line)))]
  (println (str "error=" (get nombres codigo "desconocido"))))
```

**Qué reconocer:** cuatro lenguajes sobre la misma máquina y cuatro repartos distintos de las mismas
cuatro clases. Lo que comparten es la fase de enlace más peculiar del panorama: la JVM **carga,
verifica y enlaza cada clase bajo demanda**, así que borrar un `.class` de una dependencia produce un
`NoClassDefFoundError` justo cuando el programa llega a usarla, no al arrancar. Es un error de enlace
que ocurre en tiempo de ejecución. Sobre esa base común, Kotlin y Scala empujan errores hacia la
compilación (nulabilidad, exhaustividad), Groovy los empuja hacia la ejecución con su despacho
dinámico, y Clojure ocupa un punto propio: la sintaxis se valida forma a forma al leer, mucho antes
de que nada corra.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Igual que la JVM, el CLR resuelve los ensamblados
en ejecución: un `FileNotFoundException` de un `.dll` ausente es su versión del error de enlace.

### F\#

```fsharp
// F# comprueba la exhaustividad del `match` e infiere los tipos sin anotarlos:
// olvidar un caso es un aviso del compilador, no una sorpresa en ejecución.
let codigo = int (stdin.ReadLine().Trim())

let nombre =
    match codigo with
    | 1 -> "sintaxis"
    | 2 -> "tipos"
    | 3 -> "enlace"
    | 4 -> "ejecucion"
    | _ -> "desconocido"

printfn "error=%s" nombre
```

### VB.NET

```vbnet
Module Errores
    Sub Main()
        ' Con `Option Strict On` las conversiones dudosas son error de COMPILACIÓN;
        ' con `Option Strict Off` se posponen a ejecución. El mismo código, dos
        ' momentos de diagnóstico distintos según una sola opción del proyecto.
        Dim codigo = Integer.Parse(Console.ReadLine().Trim())
        Dim nombre As String
        Select Case codigo
            Case 1 : nombre = "sintaxis"
            Case 2 : nombre = "tipos"
            Case 3 : nombre = "enlace"
            Case 4 : nombre = "ejecucion"
            Case Else : nombre = "desconocido"
        End Select
        Console.WriteLine("error=" & nombre)
    End Sub
End Module
```

**Qué reconocer:** VB.NET es el ejemplo más limpio de toda la página de que *cuándo se detecta el
error* es una **decisión de configuración**, no una propiedad inmutable del lenguaje: `Option Strict`
mueve la misma comprobación de una fase a otra sin tocar una línea de código. F# marca el otro
extremo del CLR —inferencia total y comprobación de exhaustividad—, de modo que sobre la misma
plataforma conviven el lenguaje más permisivo y el más estricto. Y los dos heredan del CLR el error
de enlace diferido: el ensamblado se busca cuando se necesita, no cuando arranca el proceso.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Es la familia donde las cuatro clases existen de
verdad y en fases separadas y visibles: preprocesar, compilar, **enlazar**, ejecutar.

### C++

```cpp
#include <iostream>

// El enlazador es una fase propia y visible: declarar una función y no definirla
// COMPILA sin queja y falla al enlazar con "undefined reference". Es la única
// familia donde el error de enlace es un error de verdad, con su propio programa.
int main() {
    int codigo = 0;
    std::cin >> codigo;
    switch (codigo) {
        case 1: std::cout << "error=sintaxis\n"; break;
        case 2: std::cout << "error=tipos\n"; break;
        case 3: std::cout << "error=enlace\n"; break;
        case 4: std::cout << "error=ejecucion\n"; break;
        default: std::cout << "error=desconocido\n"; break;
    }
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    // Objective-C hereda las cuatro fases de C, pero enviar un mensaje que el
    // objeto no entiende compila con aviso y muere en ejecución con
    // "unrecognized selector": el despacho de métodos es dinámico.
    int codigo = 0;
    scanf("%d", &codigo);
    NSArray<NSString *> *nombres = @[ @"sintaxis", @"tipos", @"enlace", @"ejecucion" ];
    NSString *nombre = (codigo >= 1 && codigo <= 4) ? nombres[codigo - 1] : @"desconocido";
    printf("error=%s\n", nombre.UTF8String);
}
```

**Qué reconocer:** esta es la familia que dio nombre a las cuatro clases, porque es donde se ven las
cuatro por separado. Un error de sintaxis lo da el compilador con número de línea; uno de tipos,
también; uno de enlace lo da un **programa distinto**, `ld`, y por eso su mensaje es tan opaco —habla
de símbolos, no de código fuente—; y uno de ejecución se manifiesta como `SIGSEGV`, sin ninguna
ayuda. Objective-C introduce una grieta interesante en el esquema: su capa de objetos mueve la
resolución de métodos a la ejecución, así que convive un enlace estático para las funciones C con uno
dinámico para los mensajes.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Ambos comprimen el
diagnóstico hacia la compilación: Go rechaza hasta un import sin usar, Rust rechaza el uso indebido
de la memoria.

### Zig

```zig
const std = @import("std");

// Zig solo analiza en profundidad el código ALCANZABLE: una función genérica con
// un error de tipos no se comprueba hasta que se instancia. En modo Debug, además,
// el desbordamiento de enteros es un error de ejecución, no un silencio.
pub fn main() !void {
    var buf: [32]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const codigo = try std.fmt.parseInt(u8, std.mem.trim(u8, linea, " \t\r"), 10);

    const nombre = switch (codigo) {
        1 => "sintaxis",
        2 => "tipos",
        3 => "enlace",
        4 => "ejecucion",
        else => "desconocido",
    };

    try std.io.getStdOut().writer().print("error={s}\n", .{nombre});
}
```

### Nim

```nim
import std/strutils

# Nim ejecuta parte de tu programa DURANTE la compilación (`static`, macros, `const`):
# hay errores de ejecución que ocurren dentro del compilador, con su propia traza.
let codigo = parseInt(stdin.readLine().strip())

let nombre =
  case codigo
  of 1: "sintaxis"
  of 2: "tipos"
  of 3: "enlace"
  of 4: "ejecucion"
  else: "desconocido"

echo "error=", nombre
```

### D

```d
import std.stdio, std.string, std.conv;

// `static assert` y `static if` comprueban condiciones en tiempo de compilación,
// y las plantillas se verifican al instanciarse. El enlace lo hace el enlazador
// del sistema, igual que en C: D hereda esa fase entera.
void main() {
    immutable codigo = readln().strip().to!int;
    string nombre;
    switch (codigo) {
        case 1: nombre = "sintaxis"; break;
        case 2: nombre = "tipos"; break;
        case 3: nombre = "enlace"; break;
        case 4: nombre = "ejecucion"; break;
        default: nombre = "desconocido"; break;
    }
    writefln("error=%s", nombre);
}
```

**Qué reconocer:** los tres borran la frontera entre compilar y ejecutar, cada uno por su lado. En
Zig, `comptime` es una palabra clave del lenguaje: parte del programa **corre** en el compilador, así
que puedes tener un error de ejecución sin haber ejecutado nada. Nim hace lo mismo con su intérprete
de tiempo de compilación, y D con `static assert`. La consecuencia práctica es que el mensaje de
error deja de encajar en las cuatro casillas: te llega una traza de pila del compilador. Los tres
conservan, eso sí, la fase de enlace de C, porque acaban produciendo objetos que un enlazador tiene
que unir.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). En SQL el error de "enlace" es una tabla o
columna que no existe, y lo detecta el planificador al preparar la consulta.

### Prolog

```prolog
:- initialization(main, main).

nombre(1, "sintaxis").
nombre(2, "tipos").
nombre(3, "enlace").
nombre(4, "ejecucion").

main :-
    read_line_to_string(user_input, Linea),
    number_string(Codigo, Linea),
    % Si no hay hecho para el código, la consulta NO lanza una excepción:
    % simplemente **no se deriva**, es decir, falla. Fallar y errar son cosas
    % distintas en Prolog, y por eso hace falta la rama alternativa explícita.
    (   nombre(Codigo, N)
    ->  true
    ;   N = "desconocido"
    ),
    format("error=~w~n", [N]).
```

### Datalog

```datalog
% Datalog no tiene excepciones, ni E/S, ni fase de enlace. Un hecho que no está
% no es un error: simplemente no pertenece a la relación derivada. Lo que sí
% comprueba el motor antes de evaluar es que cada predicado esté declarado.
codigo(1, "sintaxis").
codigo(2, "tipos").
codigo(3, "enlace").
codigo(4, "ejecucion").

error(N) :- entrada(C), codigo(C, N).
```

**Qué reconocer:** Prolog obliga a distinguir dos cosas que en el resto de la página se confunden.
Un predicado que **falla** no ha ido mal: ha respondido "no puedo derivar eso a partir de lo que sé",
y ese "no" es una respuesta legítima del sistema. Un predicado que **lanza una excepción**
(`type_error`, `existence_error`) sí es un error. Por eso escribir `nombre(Codigo, N)` sin la
alternativa no daría un mensaje de diagnóstico: daría un programa que termina en silencio sin
imprimir nada, que es la forma de fallo más difícil de depurar de toda esta página. Datalog lleva la
idea al límite: sin efectos y sin negación por defecto, casi el único error posible es el estructural
—un predicado sin declarar—, y ese se detecta antes de evaluar nada.

---

## Y de vuelta a la clase

Veinte lenguajes y un solo eje que los ordena: **cuánto se sabe antes de ejecutar**. En un extremo,
Tcl, que puede llevar un error de sintaxis escondido durante años en una rama muerta. En el otro,
Rust y F#, que rechazan al compilar programas que en otros lenguajes fallarían en producción. Y en
medio, la lección que más se repite: mover un error de la columna "ejecución" a la columna "tipos" es
casi siempre una decisión —`use strict`, `Option Strict On`, `@CompileStatic`, `dart analyze`—, no un
destino del lenguaje.

⏮️ [Volver a la clase 137](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
