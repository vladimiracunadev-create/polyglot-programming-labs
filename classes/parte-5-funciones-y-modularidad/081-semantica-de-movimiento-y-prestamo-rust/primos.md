# 🧬 El mismo programa en las familias de lenguajes — Clase 081

> [⬅️ Volver a la clase 081](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —medir un texto prestándolo y luego mostrarlo
moviéndolo— resuelto por los **primos** de cada familia del [Atlas](../../../atlas/README.md), no
solo por los diez lenguajes del núcleo.

Aquí la comparación es especialmente reveladora: **ninguno de estos veinte lenguajes tiene el
préstamo de Rust**. Ver cómo cada familia resuelve lo mismo *sin* esa garantía es la mejor forma de
entender qué es exactamente lo que Rust añade.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): una palabra ASCII
- **Salida** (stdout): `movido=<palabra> longitud=<len>`
- **Regla:** la longitud se obtiene **prestando** el texto; el texto se muestra tras **moverse**

| stdin | esperado |
|---|---|
| `Ada` | `movido=Ada longitud=3` |
| `Bo` | `movido=Bo longitud=2` |
| `hola` | `movido=hola longitud=4` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Recolección de basura y aliasing libre: el nombre es una etiqueta pegada a un objeto, y pegar una
segunda etiqueta no le quita nada a la primera.

### Ruby

```ruby
texto = STDIN.gets.strip
longitud = texto.length          # no hay préstamo: se comparte la referencia
puts "movido=#{texto} longitud=#{longitud}"
```

### Perl

```perl
my $texto = <STDIN>;
chomp $texto;
my $longitud = length $texto;    # los escalares se copian al asignar, no se mueven
print "movido=$texto longitud=$longitud\n";
```

### Lua

```lua
local texto = io.read("l")
local longitud = #texto          -- las cadenas son inmutables e internadas por el GC
print(string.format("movido=%s longitud=%d", texto, longitud))
```

### Tcl

```tcl
gets stdin linea
set texto [string trim $linea]
set longitud [string length $texto]
puts "movido=$texto longitud=$longitud"
```

### R

```r
texto <- trimws(readLines("stdin", n = 1))
longitud <- nchar(texto)
cat(sprintf("movido=%s longitud=%d\n", texto, longitud))
```

**Qué reconocer:** en los cinco **nadie es dueño de nada**. No existe `&` ni `move` porque el
recolector de basura libera cuando ya no queda ninguna referencia, y por eso el compilador no
necesita saber cuántas hay. Perl y R se separan del resto con **semántica de valor**: al asignar,
Perl copia el escalar y R aplica *copy-on-modify*, así que el original nunca puede ser invalidado
por el segundo nombre —resuelven por copia el problema que Rust resuelve por propiedad—. Tcl, con su
`string` inmutable, y Lua, con cadenas internadas, lo resuelven sencillamente haciendo imposible la
mutación compartida. Es la misma seguridad, pagada en tiempo de ejecución en vez de compilación.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void mostrar(String s) {
  // El parámetro recibe una referencia más al mismo objeto, no la propiedad.
  print('movido=$s longitud=${s.length}');
}

void main() {
  final texto = stdin.readLineSync()!.trim();
  mostrar(texto); // 'texto' sigue siendo utilizable después
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash: sin stdin y sin control de memoria.
package {
    public class Movimiento {
        public static function describir(texto:String):String {
            // String es inmutable y recolectado: pasarlo no invalida al original.
            return "movido=" + texto + " longitud=" + texto.length;
        }
    }
}
```

**Qué reconocer:** los dos comparten con JavaScript el modelo de **referencias recolectadas**, y el
`String` inmutable de ambos hace que el aliasing sea inofensivo por construcción. Dart añade tipos
estáticos —y `final`, que congela la *variable*, no el objeto—: es el matiz que Rust distingue con
`let` frente a `&mut`. Aquí `final` solo impide reasignar el nombre; ninguna anotación puede impedir
que otro trozo del programa siga viendo el mismo objeto.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Una sola heap, un solo recolector: la máquina
virtual decide cuándo muere un objeto, y ningún lenguaje de la familia puede opinar.

### Kotlin

```kotlin
fun longitud(s: String): Int = s.length   // "préstamo" de lectura: solo por convención

fun mostrar(s: String) = println("movido=$s longitud=${s.length}")

fun main() {
    val texto = readLine()!!.trim()
    longitud(texto)
    mostrar(texto) // se pasa la referencia; 'texto' sigue vivo
}
```

### Scala

```scala
object Movimiento extends App {
  val texto = scala.io.StdIn.readLine().trim
  val longitud = texto.length
  println(s"movido=$texto longitud=$longitud")
}
```

### Groovy

```groovy
def texto = System.in.newReader().readLine().trim()
def longitud = texto.length()
println "movido=$texto longitud=$longitud"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [texto (str/trim (read-line))]
  ;; Los valores son inmutables y persistentes: compartir nunca es peligroso.
  (println (format "movido=%s longitud=%d" texto (count texto))))
```

**Qué reconocer:** los cuatro pasan **referencias por valor** y confían el resto al recolector; el
`val` de Kotlin/Scala y el `final` de Java congelan el enlace, no el objeto apuntado. Clojure va más
lejos y elimina el problema de raíz: si **ningún** valor puede mutarse, el aliasing deja de importar
y la propiedad exclusiva pierde sentido. Es la respuesta opuesta a la de Rust —inmutabilidad total
en vez de mutabilidad controlada— al mismo problema: evitar que dos partes del programa se pisen.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let longitud (s: string) = s.Length   // lectura sin efectos ni transferencia

let texto = stdin.ReadLine().Trim()
printfn "movido=%s longitud=%d" texto (longitud texto)
```

### VB.NET

```vbnet
Module Movimiento
    Sub Main()
        Dim texto As String = Console.ReadLine().Trim()
        Dim longitud As Integer = texto.Length
        ' String es un tipo por referencia e inmutable: no hay copia ni movimiento.
        Console.WriteLine("movido=" & texto & " longitud=" & longitud)
    End Sub
End Module
```

**Qué reconocer:** el CLR separa **tipos por valor** (`struct`, que se copian al asignar) de **tipos
por referencia** (`class`, entre ellos `String`), y esa distinción se decide al declarar el tipo, no
al usarlo. Es lo contrario de Rust, donde el mismo tipo se presta o se mueve según lo pida cada
llamada. F# refuerza el hábito haciendo inmutables los enlaces por defecto —hay que escribir
`mutable` para reasignar—, pero eso sigue sin ser propiedad: nadie impide que dos referencias vean
el mismo objeto.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita y ningún recolector detrás.

### C++

```cpp
#include <iostream>
#include <string>
#include <utility>

std::size_t longitud(const std::string& s) { // préstamo inmutable: referencia const
    return s.size();
}

void mostrar(std::string s) {                // recibe por valor: se le mueve la propiedad
    std::cout << "movido=" << s << " longitud=" << s.size() << '\n';
}

int main() {
    std::string texto;
    std::cin >> texto;
    (void)longitud(texto);       // se presta: 'texto' sigue siendo suyo
    mostrar(std::move(texto));   // se mueve: 'texto' queda válido pero sin especificar
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[256];
        scanf("%255s", buf);
        NSString *texto = [NSString stringWithUTF8String:buf];
        // ARC cuenta referencias: el objeto muere cuando el contador llega a cero.
        printf("movido=%s longitud=%lu\n", [texto UTF8String],
               (unsigned long)[texto length]);
    }
    return 0;
}
```

**Qué reconocer:** **C++ es el primo que más se acerca a Rust**, y no por casualidad: `std::move`,
`unique_ptr` y el patrón **RAII** —el destructor libera al salir del alcance— son justamente de
donde Rust tomó la idea. La diferencia es quién comprueba: en C++ usar un objeto después de moverlo
compila sin protestar y solo el programador evita el desastre; en Rust el *borrow checker* lo
rechaza. Objective-C elige otra vía, el **conteo de referencias automático** de ARC, que resuelve el
*cuándo* liberar pero no el *quién puede escribir*: los ciclos de referencias siguen filtrando
memoria salvo que se anote `__weak`.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados y sin máquina
virtual, pero con respuestas muy distintas a la pregunta de quién libera.

### Zig

```zig
const std = @import("std");

fn longitud(s: []const u8) usize { // una rebanada es un puntero + tamaño, sin dueño
    return s.len;
}

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const texto = std.mem.trim(u8, linea, " \r\n");
    try std.io.getStdOut().writer().print(
        "movido={s} longitud={d}\n",
        .{ texto, longitud(texto) },
    );
}
```

### Nim

```nim
import std/strutils

proc mostrar(s: sink string) =   # 'sink' pide el valor para consumirlo: eso es un move
  echo "movido=", s, " longitud=", s.len

let texto = stdin.readLine().strip()
mostrar(texto)
```

### D

```d
import std.stdio, std.string;

void mostrar(scope const(char)[] s) { // 'scope': la referencia no puede escapar
    writefln("movido=%s longitud=%d", s, s.length);
}

void main() {
    auto texto = readln().strip();
    mostrar(texto);
}
```

**Qué reconocer:** los tres se acercan por caminos distintos y ninguno llega. **Zig** no tiene
propiedad ni destructores: quien reserva, libera, y lo hace a mano con `defer` —el `[]const u8` de
arriba es un préstamo por convención, sin nadie que verifique que el búfer sigue vivo—. **Nim** sí
tiene movimiento real: su ARC/ORC aplica `=sink` y `=copy` automáticamente, y anotar `sink` en el
parámetro transfiere el valor igual que Rust, aunque sin comprobar los usos posteriores. **D** es el
que mejor expresa el préstamo con `scope` —bajo DIP1000 el compilador impide que la referencia
sobreviva al ámbito—, pero es opcional y convive con un recolector de basura. Rust sigue siendo el
único donde propiedad, préstamo y tiempo de vida son obligatorios y verificados siempre.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no cómo se
gestiona la memoria que lo sostiene.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(Texto), Linea),
    string_length(Texto, Longitud),
    % Texto se liga una vez y queda disponible para todos los objetivos siguientes.
    format("movido=~w longitud=~d~n", [Texto, Longitud]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni memoria observable: se declaran los hechos.
% Un hecho no se mueve ni se presta: al afirmarlo queda visible para todas
% las reglas a la vez, y nadie puede consumirlo.
texto("Ada", 3).

movido(T, L) :- texto(T, L).
```

**Qué reconocer:** en Prolog un término **ligado no se consume**: `Texto` queda disponible para
todos los objetivos posteriores de la cláusula, así que la pregunta "¿quién es el dueño?" no llega a
formularse. Datalog lo lleva al extremo: un hecho afirmado es cierto para siempre y para todas las
reglas a la vez. Ambos comparten con SQL la misma renuncia —el motor decide cuándo copiar, cuándo
compartir y cuándo liberar— y esa renuncia es exactamente la libertad que Rust te quita a cambio de
garantizarte que nadie lea memoria muerta.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y una conclusión incómoda: **el préstamo verificado de Rust no
aparece en ninguno**. C++ tiene las piezas sin el vigilante, Nim y D tienen anotaciones opcionales,
y el resto delega en un recolector de basura. Reconocer esa ausencia es entender qué compra Rust y
qué precio cobra por ello.

⏮️ [Volver a la clase 081](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
