# 🧬 El mismo programa en las familias de lenguajes — Clase 087

> [⬅️ Volver a la clase 087](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —una cuenta cuyo saldo está oculto y solo se toca a
través de `depositar`— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Material ilustrativo.** El [verificador de equivalencia](../../../labs/README.md) solo ejecuta
> los **10 lenguajes del núcleo**; estos primos **no se ejecutan en CI** porque su toolchain no está
> instalado en el workflow. Son código de lectura y comparación, escrito para ser correcto, pero sin
> el sello de la máquina que sí tienen las implementaciones de la clase.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, el monto de cada depósito
- **Salida** (stdout): `saldo=<2n>`
- **Regla:** se crea la cuenta con saldo 0, se deposita `n` dos veces y se consulta el saldo

| stdin | esperado |
|---|---|
| `50` | `saldo=100` |
| `0` | `saldo=0` |
| `30` | `saldo=60` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Python encapsula por convención (el guion bajo) y PHP con `private` de verdad. En esta familia la
pregunta interesante es qué impide el lenguaje y qué solo desaconseja.

### Ruby

```ruby
class Cuenta
  def initialize
    # Las variables de instancia son SIEMPRE inaccesibles desde fuera:
    # no existe forma de escribir c.@saldo. Lo público son solo los métodos.
    @saldo = 0
  end

  def depositar(monto)
    @saldo += monto
  end

  attr_reader :saldo
end

n = STDIN.gets.to_i
c = Cuenta.new
c.depositar(n)
c.depositar(n)
puts "saldo=#{c.saldo}"
```

### Perl

```perl
use strict;
use warnings;

package Cuenta;

sub new {
    my $clase = shift;
    return bless { _saldo => 0 }, $clase;
}

# Perl no impone visibilidad alguna: $c->{_saldo} funciona desde cualquier parte.
# El guion bajo inicial es solo una convención, igual que en Python.
sub depositar {
    my ($self, $monto) = @_;
    $self->{_saldo} += $monto;
    return;
}

sub saldo { return $_[0]->{_saldo}; }

package main;

my $n = <STDIN>;
chomp $n;
my $c = Cuenta->new;
$c->depositar($n);
$c->depositar($n);
printf "saldo=%d\n", $c->saldo;
```

### Lua

```lua
-- Lua no tiene 'private', pero sí privacidad real: 'saldo' es un upvalue del
-- cierre y no está en la tabla devuelta, así que nadie de fuera puede alcanzarlo.
local function nueva_cuenta()
  local saldo = 0
  return {
    depositar = function(monto) saldo = saldo + monto end,
    saldo = function() return saldo end,
  }
end

local n = io.read("n")
local c = nueva_cuenta()
c.depositar(n)
c.depositar(n)
print(string.format("saldo=%d", c.saldo()))
```

### Tcl

```tcl
oo::class create Cuenta {
    # 'variable' declara estado de instancia: solo visible dentro de los métodos.
    variable saldo
    constructor {} { set saldo 0 }
    method depositar {monto} { incr saldo $monto }
    method saldo {} { return $saldo }
}

set n [string trim [gets stdin]]
set c [Cuenta new]
$c depositar $n
$c depositar $n
puts "saldo=[$c saldo]"
```

### R

```r
# Los campos de una clase de referencia son públicos: c$saldo se lee y se escribe.
# R confía en la convención y en la documentación, no en el compilador.
Cuenta <- setRefClass("Cuenta",
  fields = list(saldo = "numeric"),
  methods = list(
    initialize = function() { saldo <<- 0 },
    depositar = function(monto) { saldo <<- saldo + monto },
    consultar = function() saldo
  ))

n <- as.integer(readLines("stdin", n = 1))
c <- Cuenta$new()
c$depositar(n)
c$depositar(n)
cat(sprintf("saldo=%d\n", as.integer(c$consultar())))
```

**Qué reconocer:** aquí la familia se parte en dos mitades que a simple vista se escriben igual. Perl
y R **no ocultan nada**: `$c->{_saldo}` y `c$saldo` funcionan, y el guion bajo es un cartel de "no
entres", no una puerta cerrada —exactamente el `_saldo` de Python—. Ruby, en cambio, tiene privacidad
absoluta en las variables de instancia: `@saldo` no es alcanzable desde fuera bajo ninguna sintaxis,
aunque sus métodos `private` sean más laxos de lo que un programador de Java espera (allí `private`
significa "sin receptor explícito", no "solo esta clase"). Lua consigue lo mismo sin ninguna palabra
clave, cerrando la variable en un **cierre**: es el patrón que también aparece en JavaScript antes de
los campos `#privados`. Y Tcl es el único que declara el estado con una palabra dedicada, `variable`,
alcanzable únicamente desde los métodos del objeto.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).
JavaScript pasó veinte años sin campos privados; TypeScript los fingía en tiempo de compilación.

### Dart

```dart
import 'dart:io';

class Cuenta {
  // En Dart el guion bajo SÍ es privacidad real, pero por *biblioteca*, no por
  // clase: otro código del mismo archivo puede tocar _saldo sin problema.
  int _saldo = 0;

  void depositar(int monto) => _saldo += monto;

  int get saldo => _saldo;
}

void main() {
  final n = int.parse(stdin.readLineSync()!.trim());
  final c = Cuenta()
    ..depositar(n)
    ..depositar(n);
  print('saldo=${c.saldo}');
}
```

### ActionScript 3

```actionscript
// Sin stdin en el reproductor Flash. ActionScript 3 sí tiene los cuatro
// modificadores clásicos: public, private, protected e internal.
package {
    public class Cuenta {
        private var _saldo:int = 0;

        public function depositar(monto:int):void {
            _saldo += monto;
        }

        public function get saldo():int {
            return _saldo;
        }
    }
}
```

**Qué reconocer:** los dos usan el mismo nombre `_saldo` que Python, pero por motivos opuestos. En
ActionScript el guion bajo es puro adorno —lo que oculta el campo es la palabra `private`, verificada
por el compilador— y sirve solo para no chocar con la propiedad `saldo`. En Dart no hay palabra
clave: el guion bajo **es** el modificador, y la unidad de encapsulación no es la clase sino el
archivo o biblioteca, igual que en Rust. Es la misma señal visual con tres significados distintos
según el lenguaje: convención en Python, sintaxis en Dart, decoración en ActionScript.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). `private` en Java significa "solo esta clase",
y el verificador de bytecode lo hace cumplir. Sus primos aflojan o aprietan esa regla.

### Kotlin

```kotlin
class Cuenta {
    private var saldoInterno = 0

    fun depositar(monto: Int) {
        saldoInterno += monto
    }

    // La propiedad pública expone solo la lectura; el campo sigue siendo privado.
    val saldo: Int
        get() = saldoInterno
}

fun main() {
    val n = readLine()!!.trim().toInt()
    val c = Cuenta()
    c.depositar(n)
    c.depositar(n)
    println("saldo=${c.saldo}")
}
```

### Scala

```scala
class Cuenta {
  private var saldoInterno: Int = 0

  def depositar(monto: Int): Unit = saldoInterno += monto

  // Sin paréntesis: en Scala un método sin argumentos se lee como un campo.
  def saldo: Int = saldoInterno
}

object Main {
  def main(args: Array[String]): Unit = {
    val n = scala.io.StdIn.readLine().trim.toInt
    val c = new Cuenta
    c.depositar(n)
    c.depositar(n)
    println(s"saldo=${c.saldo}")
  }
}
```

### Groovy

```groovy
class Cuenta {
    // Groovy acepta 'private', pero históricamente no lo hace cumplir desde
    // Groovy mismo: otro código Groovy puede leer c.saldoInterno igualmente.
    private int saldoInterno = 0

    void depositar(int monto) { saldoInterno += monto }

    int getSaldo() { saldoInterno }
}

def n = System.in.newReader().readLine().trim() as int
def c = new Cuenta()
c.depositar(n)
c.depositar(n)
println "saldo=${c.saldo}"
```

### Clojure

```clojure
;; Clojure no tiene campos ni objetos con estado privado: se encapsula cerrando
;; un atom y devolviendo solo las funciones que pueden tocarlo. (defn- ...) marca
;; una función privada al namespace, que es la única visibilidad del lenguaje.
(defn cuenta []
  (let [saldo (atom 0)]
    {:depositar (fn [monto] (swap! saldo + monto))
     :saldo     (fn [] @saldo)}))

(let [n (Integer/parseInt (.trim (read-line)))
      c (cuenta)]
  ((:depositar c) n)
  ((:depositar c) n)
  (println (str "saldo=" ((:saldo c)))))
```

**Qué reconocer:** Kotlin y Scala escriben `private` igual que Java y significan casi lo mismo, con
un giro: ambos separan el **campo** del **acceso público de lectura**, algo que en Java hay que
teclear a mano como `getSaldo()`. Groovy comparte la sintaxis pero no el rigor —su `private` es más
una declaración de intenciones que una barrera—, y ese detalle explica por qué un mismo `private`
puede ser inviolable en un lenguaje y decorativo en su primo hermano de la misma máquina virtual.
Clojure cambia la pregunta: sin objetos mutables no hay campos que proteger, así que la encapsulación
vuelve al cierre —igual que en Lua— y la única visibilidad declarable es la de un nombre dentro de su
espacio de nombres.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1). El CLR añade un nivel que Java no tiene:
`internal`, visible dentro del mismo **ensamblado**.

### F\#

```fsharp
type Cuenta() =
    // 'let' dentro de un tipo es privado SIEMPRE: no admite modificador.
    let mutable saldo = 0

    member _.Depositar(monto) = saldo <- saldo + monto
    member _.Saldo = saldo

[<EntryPoint>]
let main _ =
    let n = int (stdin.ReadLine().Trim())
    let c = Cuenta()
    c.Depositar n
    c.Depositar n
    printfn "saldo=%d" c.Saldo
    0
```

### VB.NET

```vbnet
Class Cuenta
    Private _saldo As Integer = 0

    Public Sub Depositar(monto As Integer)
        _saldo += monto
    End Sub

    ' ReadOnly Property: expone el valor sin permitir asignarlo desde fuera.
    Public ReadOnly Property Saldo As Integer
        Get
            Return _saldo
        End Get
    End Property
End Class

Module Programa
    Sub Main()
        Dim n = Integer.Parse(Console.ReadLine().Trim())
        Dim c As New Cuenta()
        c.Depositar(n)
        c.Depositar(n)
        Console.WriteLine("saldo={0}", c.Saldo)
    End Sub
End Module
```

**Qué reconocer:** VB.NET es la versión más verbosa y más explícita de la idea de C#: `Private` para
el campo, `Public ReadOnly Property` para el contrato de lectura, y la diferencia entre ambos escrita
en letra. F# invierte el valor por defecto: dentro de un tipo, todo lo declarado con `let` es privado
y **no se puede** hacer público —para exponer algo hay que declararlo `member`—. Ese cambio de
defecto es lo que hace que en F# la encapsulación no requiera disciplina: el camino corto ya es el
seguro, mientras que en C# y VB olvidar el modificador te deja un miembro accesible.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). En C solo hay una herramienta: `static` para limitar
al archivo, y el truco de declarar el struct incompleto en la cabecera.

### C++

```cpp
#include <iostream>

class Cuenta {
public:
    void depositar(int monto) { saldo_ += monto; }
    int saldo() const { return saldo_; }

private:
    // 'class' asume private; si dijera 'struct', esto sería público.
    int saldo_ = 0;
};

int main() {
    int n;
    std::cin >> n;
    Cuenta c;
    c.depositar(n);
    c.depositar(n);
    std::cout << "saldo=" << c.saldo() << '\n';
}
```

### Objective-C

```objc
// La visibilidad se organiza por ARCHIVO: la interfaz pública iría en Cuenta.h y
// las variables de instancia, declaradas en la implementación (Cuenta.m), no
// aparecen en ninguna cabecera y por tanto nadie las ve.
#import <Foundation/Foundation.h>

@interface Cuenta : NSObject
- (void)depositar:(int)monto;
- (int)saldo;
@end

@implementation Cuenta {
    int _saldo;
}

- (void)depositar:(int)monto { _saldo += monto; }
- (int)saldo { return _saldo; }
@end

int main(void) {
    @autoreleasepool {
        int n;
        scanf("%d", &n);
        Cuenta *c = [[Cuenta alloc] init];
        [c depositar:n];
        [c depositar:n];
        printf("saldo=%d\n", [c saldo]);
    }
    return 0;
}
```

**Qué reconocer:** C++ es de los pocos lenguajes donde la visibilidad **por defecto** depende de la
palabra con la que abriste el tipo: `class` empieza en privado, `struct` en público, y el resto es
idéntico. Objective-C no tiene realmente modificadores de acceso útiles para el día a día: lo que
oculta el estado es **dónde lo escribes**, porque una variable declarada entre llaves en el
`@implementation` no llega a ninguna cabecera. Es el mismo mecanismo que el `static` de C, elevado a
disciplina de diseño: el contrato es literalmente el archivo `.h`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Los dos abandonaron el
eje "clase" y encapsulan por **paquete** o **módulo**: la mayúscula en Go, `pub` en Rust.

### Zig

```zig
const std = @import("std");

// Zig no tiene campos privados: dentro del archivo todo es alcanzable, y 'pub'
// solo controla qué se ve desde OTRO archivo que haga @import.
const Cuenta = struct {
    saldo: i64 = 0,

    pub fn depositar(self: *Cuenta, monto: i64) void {
        self.saldo += monto;
    }

    pub fn obtenerSaldo(self: Cuenta) i64 {
        return self.saldo;
    }
};

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = try std.fmt.parseInt(i64, std.mem.trim(u8, linea, " \r"), 10);
    var c = Cuenta{};
    c.depositar(n);
    c.depositar(n);
    try std.io.getStdOut().writer().print("saldo={d}\n", .{c.obtenerSaldo()});
}
```

### Nim

```nim
import std/strutils

type Cuenta = object
  saldo: int   # sin asterisco: invisible fuera de este módulo

proc depositar*(c: var Cuenta, monto: int) =
  c.saldo += monto

proc obtenerSaldo*(c: Cuenta): int = c.saldo

let n = parseInt(stdin.readLine().strip())
var c = Cuenta()
c.depositar(n)
c.depositar(n)
echo "saldo=", c.obtenerSaldo()
```

### D

```d
import std.stdio, std.conv, std.string;

class Cuenta {
    // En D 'private' significa privado al MÓDULO, no a la clase: otro código de
    // este mismo archivo puede leer saldo_ sin más.
    private int saldo_ = 0;

    void depositar(int monto) { saldo_ += monto; }

    int saldo() const { return saldo_; }
}

void main() {
    auto n = readln().strip().to!int;
    auto c = new Cuenta();
    c.depositar(n);
    c.depositar(n);
    writefln("saldo=%d", c.saldo());
}
```

**Qué reconocer:** los tres confirman el desplazamiento que ya hacen Go y Rust: la frontera de
visibilidad no es la clase, es el **archivo o módulo**. D lo dice sin rodeos —su `private` se parece
a `private` de Java pero protege al módulo entero—, Nim marca lo contrario, lo que **sí** sale, con
un asterisco pegado al nombre, y Zig usa `pub` igual que Rust. El efecto práctico es que en esta
familia leer el estado de un objeto desde el mismo archivo nunca es un error: se asume que quien
escribió el archivo sabe lo que hace, y la protección empieza en la frontera del módulo.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). SQL encapsula con **vistas** y **permisos**: la
tabla existe, pero tú solo ves lo que te dejan consultar.

### Prolog

```prolog
% La lista de exportación es el contrato: depositar/3 queda privado al módulo.
:- module(cuenta, [saldo_tras_dos_depositos/2]).
:- initialization(main, main).

% Prolog no tiene estado mutable: no hay saldo que ocultar, hay una versión
% del saldo que se transforma en la siguiente.
depositar(Saldo0, Monto, Saldo) :- Saldo is Saldo0 + Monto.

saldo_tras_dos_depositos(N, Saldo) :-
    depositar(0, N, S1),
    depositar(S1, N, Saldo).

main :-
    read_line_to_string(user_input, Linea),
    number_string(N, Linea),
    saldo_tras_dos_depositos(N, Saldo),
    format("saldo=~d~n", [Saldo]).
```

### Datalog

```datalog
% Datalog no tiene objetos, estado ni visibilidad: todo predicado derivado es
% consultable por cualquiera. Lo más cercano a un contrato es decidir cuál es
% la relación de salida y tratar el resto como intermedias.
deposito(50).

saldo(S) :- deposito(N), S = N + N.
```

**Qué reconocer:** Prolog sí tiene una frontera de visibilidad, y es la más estricta de las veinte:
la lista de exportación del módulo, con nombre y aridad. Pero la encapsulación *de estado* no aplica,
porque no hay estado: `depositar/3` recibe el saldo anterior y devuelve el nuevo, igual que la
implementación funcional de Clojure sin el atom. Datalog no ofrece ni una cosa ni la otra: todas las
relaciones son consultables, exactamente como una base de datos sin sistema de permisos. Ahí se ve
que "privado" no es una propiedad del código, sino una promesa que alguien tiene que hacer cumplir —
el compilador, el motor de la base de datos, o solo la convención.

---

## Y de vuelta a la clase

Veinte lenguajes y una misma pregunta con cuatro respuestas: privado por **clase** (Java, C++, C#),
por **módulo o archivo** (Go, Rust, Dart, D, Nim, Zig, Objective-C), por **cierre** (Lua, Clojure,
JavaScript) o por **convención** (Python, Perl, R). Cuando te encuentres un lenguaje nuevo, la
pregunta útil no es "¿tiene `private`?" sino "¿privado respecto a qué?".

⏮️ [Volver a la clase 087](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
