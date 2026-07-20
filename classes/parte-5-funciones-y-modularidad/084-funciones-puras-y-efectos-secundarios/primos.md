# 🧬 El mismo programa en las familias de lenguajes — Clase 084

> [⬅️ Volver a la clase 084](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —elevar un número al cuadrado con una función que no
toca nada más— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Escribir una función pura es fácil en los veinte. Lo interesante es otra cosa: **¿quién comprueba
que de verdad lo es?** Ahí las familias se separan del todo.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `puro=<n²>`
- **Regla:** `cuadrado(n) = n * n`, sin efectos secundarios

| stdin | esperado |
|---|---|
| `4` | `puro=16` |
| `-3` | `puro=9` |
| `0` | `puro=0` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La pureza aquí es **disciplina del programador**: nada en el lenguaje la exige ni la comprueba.

### Ruby

```ruby
def cuadrado(n) = n * n     # pura por convenio; sin '!' al final, que marca lo mutante

n = STDIN.gets.to_i
puts "puro=#{cuadrado(n)}"
```

### Perl

```perl
sub cuadrado { my ($n) = @_; return $n * $n }   # copia el argumento a una léxica

my $n = <STDIN>;
chomp $n;
printf "puro=%d\n", cuadrado($n);
```

### Lua

```lua
local function cuadrado(n) return n * n end

local n = io.read("n")
print(string.format("puro=%d", cuadrado(n)))
```

### Tcl

```tcl
proc cuadrado {n} {expr {$n * $n}}   ;# los args llegan por valor: no toca al llamador

gets stdin n
puts "puro=[cuadrado $n]"
```

### R

```r
cuadrado <- function(n) n * n   # R copia al modificar: mutar el argumento no sale de aquí

n <- as.integer(readLines("stdin", n = 1))
cat(sprintf("puro=%d\n", cuadrado(n)))
```

**Qué reconocer:** ninguno de los cinco puede **verificar** la pureza, así que la comunidad la
señala con convenciones. Ruby marca el efecto en el nombre: `sort` devuelve algo nuevo y `sort!`
muta el receptor, un `!` que es documentación, no una regla del compilador. Perl es el más peligroso
del grupo porque `@_` **alias** los argumentos del llamador: modificar `$_[0]` cambia la variable de
fuera, y por eso el idioma es copiarlos a léxicas con `my` en la primera línea. R protege por el
lado contrario, con *copy-on-modify*: dentro de la función puedes escribir `n <- n + 1` sin que el
llamador se entere. Tcl pasa por valor puro y en él lo difícil es lo contrario, mutar: hace falta
`upvar` para tocar la variable del llamador.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

int cuadrado(int n) => n * n; // pura, pero el tipo no lo dice

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  print('puro=${cuadrado(n)}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash: la función pura es igual y el efecto
// (imprimir) se queda fuera de ella, que es justo lo que enseña la clase.
package {
    public class Puro {
        public static function cuadrado(n:int):int {
            return n * n;
        }
    }
}
```

**Qué reconocer:** la familia entera es de **efectos libres y no anotados**: `int cuadrado(int)` y
una función que borra la base de datos tienen tipos indistinguibles. Ni Dart ni TypeScript añaden
nada aquí —sus tipos hablan de la *forma* de los datos, nunca de lo que la función hace por el
camino—, y por eso la pureza vive en las revisiones de código y en la disciplina de separar cálculo
de efecto. Dart aporta un matiz interesante: `const` y las constantes en tiempo de compilación
obligan a que la expresión sea evaluable sin efectos, que es lo más cerca que llega la familia a
comprobar algo.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Cuatro lenguajes con una sola heap compartida
y mutable, y uno de ellos que decidió no usarla así.

### Kotlin

```kotlin
fun cuadrado(n: Long): Long = n * n

fun main() {
    val n = readLine()!!.trim().toLong()
    println("puro=${cuadrado(n)}")
}
```

### Scala

```scala
object Puro extends App {
  def cuadrado(n: Long): Long = n * n   // función total y pura, verificada solo por costumbre
  val n = scala.io.StdIn.readLine().trim.toLong
  println(s"puro=${cuadrado(n)}")
}
```

### Groovy

```groovy
def cuadrado(long n) { n * n }

def n = System.in.newReader().readLine().trim() as long
println "puro=${cuadrado(n)}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(defn cuadrado [n] (* n n))   ; sin efectos posibles: no hay nada mutable que tocar

(println (str "puro=" (cuadrado (Long/parseLong (str/trim (read-line))))))
```

**Qué reconocer:** Kotlin, Scala y Groovy pueden escribir la función pura, pero su sistema de tipos
no distingue `cuadrado` de un método que escriba en disco; Scala lo compensa culturalmente
—`val` por defecto, colecciones inmutables, y bibliotecas como Cats que meten los efectos dentro de
un tipo `IO` para hacerlos visibles—. **Clojure es el extremo de la JVM**: sus estructuras de datos
son persistentes e inmutables, así que una función *no puede* mutar lo que recibe aunque quiera, y
todo efecto real necesita una puerta declarada (`atom`, `ref`, `swap!`, o interoperabilidad Java).
Cuando la pureza es lo predeterminado, el marcado sobra.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let cuadrado n = n * n   // sin efectos: F# los haría visibles devolviendo unit

let n = int64 (stdin.ReadLine().Trim())
printfn "puro=%d" (cuadrado n)
```

### VB.NET

```vbnet
Module Puro
    ' VB separa por sintaxis: Function devuelve valor, Sub solo produce efectos.
    Function Cuadrado(n As Long) As Long
        Return n * n
    End Function

    Sub Main()
        Dim n As Long = Long.Parse(Console.ReadLine().Trim())
        Console.WriteLine("puro=" & Cuadrado(n))
    End Sub
End Module
```

**Qué reconocer:** **VB.NET conserva la distinción más vieja del asunto**: `Function` devuelve un
valor y `Sub` no devuelve nada, es decir, solo existe por sus efectos. No es una garantía —una
`Function` puede escribir en disco— pero sí una señal sintáctica que C# perdió al unificarlo todo
en métodos con `void`. F# hace lo simétrico desde el otro lado: una expresión que "no devuelve nada"
tiene tipo `unit`, y ver `unit` en una firma es la pista de que ahí hay un efecto. Ninguno de los
dos lo verifica: el atributo `[<Pure>]` de .NET es documentación para analizadores, no una regla del
compilador.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Punteros por todas partes: aquí cualquier función
puede tocar cualquier cosa, y la única defensa es decir por escrito que no lo hará.

### C++

```cpp
#include <iostream>

// constexpr: el compilador puede evaluarla en compilación, lo que impide
// cualquier efecto observable dentro de ella.
constexpr long long cuadrado(long long n) { return n * n; }

int main() {
    long long n;
    std::cin >> n;
    std::cout << "puro=" << cuadrado(n) << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

// __attribute__((const)): promesa al optimizador de que solo depende de sus
// argumentos. Es una promesa del programador, no una comprobación.
__attribute__((const)) static long long cuadrado(long long n) { return n * n; }

int main(void) {
    @autoreleasepool {
        long long n;
        scanf("%lld", &n);
        printf("puro=%lld\n", cuadrado(n));
    }
    return 0;
}
```

**Qué reconocer:** **C++ es el primo que más cerca llega a una pureza verificada** con `constexpr`:
si la función se usa en un contexto de compilación, el compilador rechaza cualquier efecto que no
pueda evaluar, así que la promesa se comprueba de verdad —aunque solo en ese contexto—. Objective-C
se queda en la promesa pura: `__attribute__((const))` y `((pure))` le dicen al optimizador que puede
eliminar llamadas repetidas, y si mientes obtienes código roto sin ningún aviso. Es la diferencia
entre una anotación que el compilador **hace cumplir** y una que se limita a **creerte**.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia donde algunos
sí pusieron la pureza en el sistema de tipos.

### Zig

```zig
const std = @import("std");

// Zig no marca la pureza, pero la delata por otra vía: una función con efectos
// de E/S necesita un writer, y una que reserve memoria necesita un allocator.
fn cuadrado(n: i64) i64 {
    return n * n;
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\n"), 10);
    try std.io.getStdOut().writer().print("puro={d}\n", .{cuadrado(n)});
}
```

### Nim

```nim
import std/strutils

func cuadrado(n: int): int = n * n   # 'func' = proc con {.noSideEffect.}: lo verifica el compilador

let n = stdin.readLine().strip().parseInt()
echo "puro=", cuadrado(n)
```

### D

```d
import std.stdio, std.string, std.conv;

// 'pure' es un atributo comprobado: dentro no se puede leer ni escribir estado global.
pure long cuadrado(long n) { return n * n; }

void main() {
    const n = readln().strip().to!long;
    writefln("puro=%d", cuadrado(n));
}
```

**Qué reconocer:** aquí está la respuesta seria a la pregunta de quién comprueba. **Nim tiene una
palabra clave entera para esto**: `func` es exactamente `proc {.noSideEffect.}`, y si dentro tocas
una global o imprimes, **no compila**. **D lleva `pure` como atributo verificado**, y lo combina con
`@safe`, `nothrow` e `immutable` para formar un contrato completo de la función. **Zig no anota
nada**, pero su estilo lo hace visible de otra forma: como no hay asignación de memoria oculta ni
E/S global, una función que necesita efectos tiene que **recibir** el `allocator` o el `writer` en
sus parámetros, y la firma te lo cuenta igual. Rust queda en medio: `&mut` te dice quién puede
escribir, pero nada le impide a una función `fn(i64) -> i64` imprimir por pantalla.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). El extremo del espectro: aquí la pureza no es un
estilo, es la definición del lenguaje.

### Prolog

```prolog
:- initialization(main, main).

cuadrado(N, R) :- R is N * N.   % relación pura: no toca la base de hechos

main :-
    read_line_to_string(user_input, Linea),   % esto SÍ es un efecto, y está aislado aquí
    number_string(N, Linea),
    cuadrado(N, R),
    format("puro=~d~n", [R]).
```

### Datalog

```datalog
% Datalog no tiene efectos NI entrada/salida: no existe forma de escribir uno.
% Un programa es un conjunto de hechos y reglas, y su significado no depende
% del orden en que se evalúen.
n(4).

puro(R) :- n(N), R = N * N.
```

**Qué reconocer:** **Clojure y Datalog son los dos extremos de estas veinte páginas**, y Datalog es
el más radical: no tiene efectos porque no tiene *dónde* tenerlos —sin E/S, sin asignación y sin
orden de evaluación, la pureza no es una virtud sino la única opción—. Prolog no es puro del todo y
lo sabe: `assert/1`, `retract/1` y el propio `format/2` son efectos, y por eso el idioma es
encerrarlos en el predicado de entrada como hace `main` aquí. Su detalle más revelador es otro: una
variable **se liga una sola vez**, así que el efecto secundario más común de todos —reasignar algo
que otro estaba leyendo— sencillamente no se puede escribir. Es la misma renuncia de SQL, donde una
consulta `SELECT` describe un resultado sin decir qué se modifica por el camino.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una escala clara de quién comprueba la pureza: Datalog y
Clojure la imponen por diseño, Nim y D la verifican con `func` y `pure`, C++ la comprueba dentro de
`constexpr`, VB.NET y F# solo la insinúan con `Sub` y `unit`, y el resto de la lista la deja
enteramente en tus manos. Escribir funciones puras es tu trabajo en casi todos ellos.

⏮️ [Volver a la clase 084](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
