# 🧬 El mismo programa en las familias de lenguajes — Clase 132

> [⬅️ Volver a la clase 132](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —prestar un valor a una función que devuelve su
doble, sin cederle la propiedad— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

El cálculo es trivial a propósito. Lo que cambia de un lenguaje a otro es **quién garantiza que el
recurso se libere y cuándo**, y esa pregunta parte a los veinte lenguajes en dos mitades muy claras.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** prestar `n` a una función que devuelve `2n` sin adueñarse del valor

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Ninguno tiene propiedad ni préstamos: se pasa una referencia al mismo objeto y punto. Lo que sí
tienen —unos más que otros— es **destrucción determinista**.

### Ruby

```ruby
class Recurso
  attr_reader :valor
  def initialize(valor) = @valor = valor
end

n = STDIN.read.strip.to_i
# El equivalente de RAII en Ruby no es el objeto sino el BLOQUE: File.open { } cierra
# al salir, porque el `ensure` está en el método, no en un destructor.
puts "resultado=#{Recurso.new(n).valor * 2}"
```

### Perl

```perl
package Guardia;
sub new     { my ($clase, $valor) = @_; return bless { valor => $valor }, $clase; }
sub valor   { return $_[0]{valor}; }
sub DESTROY { }   # se ejecuta cuando el contador de referencias llega a cero

package main;
my $n = <STDIN>;
chomp $n;
my $guardia = Guardia->new($n);
printf "resultado=%d\n", $guardia->valor * 2;
```

### Lua

```lua
local n = tonumber(io.read("l"))

-- Lua 5.4: variable "to-be-closed"; __close se llama al salir del ámbito, con o sin error.
local recurso <close> = setmetatable({ valor = n }, {
  __close = function(self, err) end,
})

print(string.format("resultado=%d", recurso.valor * 2))
```

### Tcl

```tcl
gets stdin n

oo::class create Guardia {
    variable valor
    constructor {v} { set valor $v }
    method doble {} { return [expr {$valor * 2}] }
    destructor { }   ;# TclOO sí tiene destructor, pero hay que borrar el objeto
}

Guardia create g $n
puts "resultado=[g doble]"
g destroy
```

### R

```r
n <- as.integer(readLines("stdin", n = 1))

doble <- function(x) {
  on.exit(invisible(NULL))   # on.exit es lo más cercano a un destructor en R
  x * 2
}

cat(sprintf("resultado=%d\n", doble(n)))
```

**Qué reconocer:** ninguno de los cinco tiene propiedad ni comprobación de préstamos —pasar `n` a
`doble` no le quita nada a nadie—, pero **sí se separan en la destrucción**. Perl cuenta
referencias, así que `DESTROY` corre en un punto exacto y previsible, y eso hace que el patrón
RAII sea viable en Perl. Lua fue más lejos y en **5.4** añadió las variables `<close>`: un ámbito
léxico que garantiza la llamada a `__close` aunque salte un error, que es literalmente el contrato
de un destructor de C++. Tcl tiene destructor pero no lo dispara el ámbito: hay que decir `g
destroy`. R solo ofrece `on.exit`, un gancho en la función y no en el valor. Ruby es el caso más
instructivo: como su recolector **rastrea**, un destructor no podría prometer *cuándo*, así que la
comunidad movió la garantía al **bloque** —`File.open` con bloque cierra siempre— en vez de al tipo.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
Recolector rastreador, sin destructores: la liberación nunca es determinista.

### Dart

```dart
import 'dart:io';

int doble(int x) => x * 2; // se pasa la referencia; no hay propiedad ni préstamo

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  try {
    print('resultado=${doble(n)}');
  } finally {
    // Sin destructores: `finally` es la única garantía de liberación que existe.
  }
}
```

### ActionScript 3

```actionscript
// AS3 no tiene stdin, ni destructores, ni `using`: los recursos (BitmapData, Sound)
// se sueltan a mano con dispose() y poniendo la referencia a null. Nada lo comprueba.
package {
    public class Prestamo {
        public static function doble(x:int):String {
            return "resultado=" + (x * 2);
        }
    }
}
```

**Qué reconocer:** esta familia es el extremo opuesto a C++. No hay destructor, no hay propiedad y
no hay nada que impida que dos referencias apunten al mismo objeto mutable a la vez. La única
herramienta es `try`/`finally`, es decir, RAII **puesto a mano en cada punto de uso** en vez de una
sola vez en el tipo: si se te olvida un `finally`, nadie te avisa. En JavaScript moderno existen
`FinalizationRegistry` y `WeakRef`, pero la propia especificación advierte que no garantizan cuándo
—ni siquiera si— se ejecutará la limpieza, así que no son un sustituto de un destructor.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Cuatro lenguajes distintos que llegaron a la
**misma** solución, porque el recolector rastreador de la JVM se la impone a todos.

### Kotlin

```kotlin
class Recurso(val valor: Int) : AutoCloseable {
    override fun close() { } // `use` lo llama al salir del bloque, haya o no excepción
}

fun main() {
    val n = readLine()!!.trim().toInt()
    Recurso(n).use { r -> println("resultado=${r.valor * 2}") }
}
```

### Scala

```scala
import scala.util.Using

class Recurso(val valor: Int) extends AutoCloseable {
  def close(): Unit = ()
}

object Prestamo {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    Using.resource(new Recurso(n)) { r =>
      println(s"resultado=${r.valor * 2}")
    }
  }
}
```

### Groovy

```groovy
class Recurso implements AutoCloseable {
    int valor
    void close() { }
}

def n = System.in.newReader().readLine().trim().toInteger()
new Recurso(valor: n).withCloseable { r -> println "resultado=${r.valor * 2}" }
```

### Clojure

```clojure
;; Los valores de Clojure son inmutables: prestar es siempre seguro porque nadie
;; puede modificar lo prestado. Para los recursos con estado, `with-open`.
(defn doble [x] (* x 2))

(let [n (Integer/parseInt (.trim (read-line)))]
  (println (str "resultado=" (doble n))))
```

**Qué reconocer:** los cuatro implementan `AutoCloseable` y los cuatro inventaron **su propia
palabra** para el mismo patrón: `use` en Kotlin, `Using.resource` en Scala, `withCloseable` en
Groovy, `with-open` en Clojure —y `try`-con-recursos en Java—. Esa convergencia no es casualidad:
como el recolector es rastreador, un destructor no puede prometer *cuándo* corre, así que la
garantía se traslada del **tipo** al **lugar de uso**. Es RAII invertido, y por eso es más frágil:
en C++ olvidarte de liberar es imposible; aquí basta con no escribir `use`. Clojure evita la mitad
del problema por otra vía —si nada muta, compartir no tiene riesgo— y solo necesita la ceremonia
para los recursos externos de verdad.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). Mismo diagnóstico que la JVM, misma cura, con el
nombre `IDisposable`.

### F\#

```fsharp
type Recurso(valor: int) =
    member _.Valor = valor
    interface System.IDisposable with
        member _.Dispose() = ()   // `use` llama a Dispose al salir del ámbito

let n = stdin.ReadLine().Trim() |> int
use r = new Recurso(n)
printfn "resultado=%d" (r.Valor * 2)
```

### VB.NET

```vbnet
Imports System

Public Class Recurso
    Implements IDisposable
    Public ReadOnly Valor As Integer
    Public Sub New(v As Integer)
        Valor = v
    End Sub
    Public Sub Dispose() Implements IDisposable.Dispose
    End Sub
End Class

Module Prestamo
    Sub Main()
        Dim n As Integer = Integer.Parse(Console.In.ReadToEnd().Trim())
        Using r As New Recurso(n)
            Console.WriteLine("resultado=" & (r.Valor * 2))
        End Using
    End Sub
End Module
```

**Qué reconocer:** `Using` de VB.NET, `use` de F# y `using` de C# compilan **exactamente** al mismo
`try`/`finally` con `Dispose()` dentro; la diferencia es puramente de sintaxis. Lo que .NET añade
frente a la JVM es que el ámbito se marca en la **declaración** (`use r = ...`) y no envolviendo un
bloque, lo que se lee bastante más parecido a C++. Y como el CLR también rastrea, aquí vuelve la
misma regla: el finalizador existe pero es no determinista y la guía oficial es no depender de él.
`Dispose` es una promesa que el programador hace; el destructor de C++ es una que hace el compilador.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Esta es **la familia de la clase**: RAII se inventó
aquí, y el término lo acuñó Bjarne Stroustrup para C++.

### C++

```cpp
#include <iostream>
#include <memory>

// Préstamo: referencia constante. Se lee sin copiar y sin adueñarse. Es el `&T` de Rust.
long long doble(const long long& x) { return x * 2; }

struct Recurso {
    long long valor;
    explicit Recurso(long long v) : valor(v) {} // adquirir un recurso ES inicializar
    ~Recurso() {}                               // liberarlo ES destruir: eso es RAII
};

int main() {
    long long n = 0;
    std::cin >> n;
    auto propietario = std::make_unique<Recurso>(n); // propiedad única, como Box<T>
    std::cout << "resultado=" << doble(propietario->valor) << '\n';
} // el destructor corre aquí, garantizado, incluso si sale una excepción
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

@interface Recurso : NSObject
@property (nonatomic, assign) long long valor;
@end

@implementation Recurso
- (void)dealloc { /* ARC lo llama cuando el contador de referencias llega a cero */ }
@end

static long long doble(long long x) { return x * 2; }

int main(void) {
    @autoreleasepool {
        long long n = 0;
        scanf("%lld", &n);
        Recurso *r = [Recurso new];   // el puntero es __strong por defecto: eso es propiedad
        r.valor = n;
        printf("resultado=%lld\n", doble(r.valor));
    }
    return 0;
}
```

**Qué reconocer:** C++ es aquí el **representante natural**, no un primo secundario. Casi todo el
vocabulario de Rust tiene su original en esta caja: `unique_ptr` es `Box`, `shared_ptr` es `Rc`,
`std::move` es el movimiento, y `const&` es el préstamo compartido `&T`. La diferencia está en
**quién comprueba**: C++ te deja usar un objeto del que ya te moviste, guardar una referencia a un
temporal que acaba de morir o tener dos `shared_ptr` en ciclo que nunca se liberan, y todo eso
compila. El verificador de préstamos de Rust rechaza esos tres casos antes de generar código; es la
misma disciplina, una hecha por convención y otra por el compilador. Objective-C aporta la tercera
vía: los calificadores `__strong`, `__weak` y `__unsafe_unretained` son **propiedad escrita en el
tipo**, como Rust, pero implementada con conteo de referencias, así que los ciclos siguen filtrando
si no marcas uno de los lados como `__weak`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Go delega en el
recolector y ofrece `defer`; Rust es el otro polo de la clase.

### Zig

```zig
const std = @import("std");

fn doble(x: *const i64) i64 {
    return x.* * 2; // puntero constante: se lee prestado, sin copiar ni liberar
}

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r\t"), 10);

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const celda = try alloc.create(i64);
    defer alloc.destroy(celda);   // Zig NO tiene destructores: la limpieza es un `defer`
    celda.* = n;

    try std.io.getStdOut().writer().print("resultado={d}\n", .{doble(celda)});
}
```

### Nim

```nim
import std/strutils

type Recurso = object
  valor: int

# Nim 2: gancho de destrucción que ARC/ORC inserta al salir del ámbito.
proc `=destroy`(r: Recurso) =
  discard

proc doble(r: Recurso): int = r.valor * 2   # se pasa por referencia oculta, sin copiar

let n = stdin.readLine().strip().parseInt()
let r = Recurso(valor: n)
echo "resultado=", doble(r)
```

### D

```d
import std.stdio, std.string, std.conv;

struct Recurso {
    long valor;
    ~this() { }   // los `struct` de D sí tienen destructor determinista; las `class` no
}

long doble(const ref long x) { return x * 2; }   // `ref` = préstamo, `const` = solo lectura

void main() {
    auto r = Recurso(readln().strip().to!long);
    writefln("resultado=%d", doble(r.valor));
}
```

**Qué reconocer:** los tres resuelven "cuándo se libera" sin recolector, y de tres maneras
distintas. Zig se niega a esconder nada: no hay destructor, así que la limpieza se escribe con
`defer` **junto a la adquisición**, lo que hace imposible olvidarla al leer el código aunque el
compilador no la exija. Nim está sorprendentemente cerca de Rust: `=destroy`, `=copy` y `=sink` son
ganchos que el compilador inserta, y los parámetros `sink` y `lent` son movimiento y préstamo con
otro nombre —la diferencia es que Nim añade un detector de ciclos en vez de prohibirlos—. D parte el
mundo en dos: los `struct` viven en la pila con destructor determinista, las `class` viven en el
montón del recolector y su destructor corre "algún día", que es exactamente la trampa que hay que
conocer antes de escribir D.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Sin variables mutables no hay propiedad que
transferir; la pregunta cambia de forma.

### Prolog

```prolog
:- initialization(main, main).

doble(X, Y) :- Y is X * 2.   % X se unifica, no se copia ni se transfiere

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    setup_call_cleanup(
        true,                                          % adquirir
        (doble(N, R), format("resultado=~d~n", [R])),  % usar
        true).                                         % liberar, pase lo que pase
```

### Datalog

```datalog
% Datalog no tiene recursos, ni destructores, ni propiedad, ni orden de ejecución:
% solo hechos y reglas. No hay ningún momento al que llamar "el final del ámbito".
entrada(5).

resultado(R) :- entrada(N), R = N * 2.
```

**Qué reconocer:** en Prolog una variable se **liga una sola vez** dentro de una rama, así que las
dos cosas que la propiedad viene a evitar —dos dueños que muten lo mismo y un uso después de
liberar— no pueden ocurrir. Lo interesante es que Prolog **sí necesitó** el patrón cuando salió del
mundo puro: `setup_call_cleanup/3` es RAII convertido en estructura de control, y garantiza el
tercer argumento aunque el objetivo falle, lance o se corte con un `!`. Datalog ni siquiera llega
ahí: sin efectos ni orden de evaluación, "liberar al salir del ámbito" no tiene referente, igual que
en SQL no puedes preguntar cuándo se cierra una tabla temporal intermedia.

---

## Y de vuelta a la clase

Veinte lenguajes y dos respuestas de fondo. Los que **cuentan referencias o no recolectan** —C++,
Objective-C, Perl, Lua 5.4, Nim, Zig, D con `struct`, Rust— pueden poner la garantía **en el tipo**,
y el ámbito la dispara sola. Los que **rastrean** —JVM, CLR, JavaScript, Ruby, Dart— tienen que
ponerla **en el lugar de uso**, con `use`, `using`, `with-open` o `finally`. Reconocer de qué lado
está un lenguaje nuevo te dice, sin leer su documentación, qué error vas a cometer con él.

⏮️ [Volver a la clase 132](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
