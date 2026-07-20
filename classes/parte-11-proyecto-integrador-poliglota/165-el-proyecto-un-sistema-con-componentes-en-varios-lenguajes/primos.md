# 🧬 El mismo programa en las familias de lenguajes — Clase 165

> [⬅️ Volver a la clase 165](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —describir el sistema contando y listando sus
componentes— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): nombres de los componentes separados por espacios
- **Salida** (stdout): `componentes=<N> nombres=<unidos por ->`
- **Regla:** contar los componentes y unir sus nombres con `-`

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3 nombres=cli-api-web` |
| `app` | `componentes=1 nombres=app` |
| `web api datos cache` | `componentes=4 nombres=web-api-datos-cache` |

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
Tipado dinámico, poca ceremonia: partir la línea, contar la lista y unirla es una sola expresión.

### Ruby

```ruby
componentes = STDIN.read.split
puts "componentes=#{componentes.size} nombres=#{componentes.join('-')}"
```

### Perl

```perl
my @componentes = split ' ', do { local $/; <STDIN> };
printf "componentes=%d nombres=%s\n", scalar @componentes, join('-', @componentes);
```

### Lua

```lua
local componentes = {}
for palabra in io.read("a"):gmatch("%S+") do
  componentes[#componentes + 1] = palabra
end
print(string.format("componentes=%d nombres=%s", #componentes, table.concat(componentes, "-")))
```

### Tcl

```tcl
set componentes [regexp -all -inline {\S+} [read stdin]]
puts "componentes=[llength $componentes] nombres=[join $componentes -]"
```

### R

```r
comp <- scan("stdin", what = character(), quiet = TRUE)
cat(sprintf("componentes=%d nombres=%s\n", length(comp), paste(comp, collapse = "-")))
```

**Qué reconocer:** los cinco tratan el sistema como una **lista de nombres**, sin declarar ningún
tipo ni tamaño previo, y esa es exactamente la razón por la que en un proyecto real esta familia
suele quedarse con el pegamento —el script que arranca los componentes, el que los inventaria— y no
con el componente que debe correr en producción durante meses. R delata su origen estadístico:
`scan` devuelve un **vector** de caracteres, no una lista de palabras, y `paste(collapse=)` es la
misma operación de unión vectorizada que usa para producir etiquetas de un gráfico. El coste de
elegir cualquiera de ellos para un componente del sistema es siempre el mismo: hay que tener el
intérprete instalado y en la versión correcta allí donde el componente vaya a ejecutarse.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final componentes = stdin.readLineSync()!.trim().split(RegExp(r'\s+'));
  stdout.writeln('componentes=${componentes.length} nombres=${componentes.join('-')}');
}
```

### ActionScript 3

```actionscript
// ActionScript 3 corre en el reproductor Flash / AIR: no hay stdin.
// El inventario del sistema se expresa como función pura sobre la lista ya recibida.
package {
    public class Sistema {
        public static function describir(componentes:Array):String {
            return "componentes=" + componentes.length +
                   " nombres=" + componentes.join("-");
        }
    }
}
```

**Qué reconocer:** `split` + `join` es el par exacto de JavaScript, y Dart añade tipos estáticos y el
`!` que afirma que la lectura no fue nula, igual que TypeScript endurece JS. ActionScript sirve de
recordatorio incómodo para quien diseña un sistema: **un lenguaje no solo se elige, también se
hereda**, y cuando su plataforma muere —Flash dejó de existir en 2020— el componente escrito en él
no se migra solo. Dart es el caso opuesto: el mismo código compila a nativo (`dart compile exe`) o a
JavaScript, así que el mismo componente puede vivir en dos fronteras distintas del sistema.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). Todos compilan al mismo bytecode y comparten
biblioteca estándar; lo que cambia es cuánta ceremonia exigen para decir lo mismo.

### Kotlin

```kotlin
fun main() {
    val componentes = readLine()!!.trim().split(Regex("\\s+"))
    println("componentes=${componentes.size} nombres=${componentes.joinToString("-")}")
}
```

### Scala

```scala
object Sistema extends App {
  val componentes = scala.io.StdIn.readLine().trim.split("\\s+")
  println(s"componentes=${componentes.length} nombres=${componentes.mkString("-")}")
}
```

### Groovy

```groovy
def componentes = System.in.newReader().readLine().trim().split(/\s+/)
println "componentes=${componentes.size()} nombres=${componentes.join('-')}"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [componentes (str/split (str/trim (read-line)) #"\s+")]
  (println (format "componentes=%d nombres=%s"
                   (count componentes)
                   (str/join "-" componentes))))
```

**Qué reconocer:** los cuatro acaban llamando a `String.format` y a las mismas colecciones de Java, y
esa es su ventaja concreta cuando se diseña un sistema con varios componentes: cuatro lenguajes
distintos comparten **una sola toolchain, un solo formato de despliegue y una sola pila de
observabilidad**. Un componente en Kotlin y otro en Clojure pueden convivir en el mismo `.jar` y en
el mismo proceso. La diferencia real está en la forma —Kotlin recorta la ceremonia de Java, Scala
añade un sistema de tipos mucho más expresivo, Clojure cambia de paradigma sin cambiar de máquina
virtual— y el coste es de personas, no de máquinas: encontrar quien mantenga Clojure es bastante más
difícil que encontrar quien mantenga Java.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let componentes =
    stdin.ReadLine().Split(' ', System.StringSplitOptions.RemoveEmptyEntries)

printfn "componentes=%d nombres=%s" componentes.Length (String.concat "-" componentes)
```

### VB.NET

```vbnet
Module Sistema
    Sub Main()
        Dim componentes = Console.ReadLine().Split(New Char() {" "c}, StringSplitOptions.RemoveEmptyEntries)
        Console.WriteLine("componentes=" & componentes.Length & " nombres=" & String.Join("-", componentes))
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre el CLR y llaman al mismo `String.Join`, así que valen aquí
las mismas cuentas que en la JVM: mezclar C# y F# en un sistema no multiplica el despliegue, porque
ambos producen ensamblados intercambiables. La diferencia es de estilo —F# es funcional y encadena
con `|>`, VB.NET arrastra la sintaxis verbosa de Visual Basic— y de mercado: VB.NET sigue vivo y
soportado, pero Microsoft ya no le añade características nuevas, y eso es un dato que pertenece a la
decisión de arquitectura, no al gusto de quien escribe.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Memoria explícita, tipos declarados y `printf`.

### C++

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> componentes;
    for (std::string palabra; std::cin >> palabra; ) {
        componentes.push_back(palabra);
    }
    std::cout << "componentes=" << componentes.size() << " nombres=";
    for (std::size_t i = 0; i < componentes.size(); ++i) {
        if (i) std::cout << '-';
        std::cout << componentes[i];
    }
    std::cout << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        NSData *entrada = [[NSFileHandle fileHandleWithStandardInput] readDataToEndOfFile];
        NSString *linea = [[NSString alloc] initWithData:entrada encoding:NSUTF8StringEncoding];
        NSArray<NSString *> *componentes =
            [[linea stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]]
             componentsSeparatedByCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];
        printf("componentes=%lu nombres=%s\n",
               (unsigned long)componentes.count,
               [[componentes componentsJoinedByString:@"-"] UTF8String]);
    }
    return 0;
}
```

**Qué reconocer:** ambos son **superconjuntos de C**, y por eso el componente que hoy es C puede
crecer a C++ sin reescribirse. Lo que se ve aquí es cuánto trabajo cuesta en esta familia algo que en
scripting era una línea: no hay `split` en la biblioteca estándar de C, así que C++ lo simula con el
bucle sobre `std::cin` y Objective-C tiene que subir hasta `NSString` para conseguirlo. Ese es el
precio real de esta familia en un sistema —más código por unidad de idea— y su ventaja real es la
otra cara: control sobre memoria y latencia, y la posibilidad de que otros lenguajes lo llamen por
FFI, que es la razón por la que las bibliotecas de bajo nivel siguen escribiéndose aquí.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). Compilados, sin máquina
virtual, con control sobre el coste de cada operación.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [1024]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const out = std.io.getStdOut().writer();

    var it = std.mem.tokenizeAny(u8, linea, " \t\r");
    var n: usize = 0;
    while (it.next()) |_| n += 1;

    try out.print("componentes={d} nombres=", .{n});
    it.reset();
    var primero = true;
    while (it.next()) |nombre| {
        if (!primero) try out.writeByte('-');
        try out.writeAll(nombre);
        primero = false;
    }
    try out.writeByte('\n');
}
```

### Nim

```nim
import std/strutils

let componentes = stdin.readLine().splitWhitespace()
echo "componentes=", componentes.len, " nombres=", componentes.join("-")
```

### D

```d
import std.stdio, std.array, std.string;

void main() {
    auto componentes = readln().strip().split();
    writefln("componentes=%d nombres=%s", componentes.length, componentes.join("-"));
}
```

**Qué reconocer:** los tres producen un **binario único sin runtime**, y esa es la ventaja de
despliegue más concreta que existe en un sistema de varios componentes: se copia un archivo y
funciona, sin instalar intérprete ni máquina virtual en la máquina destino. Zig lo lleva al extremo
—reserva el búfer a mano, recorre dos veces con `it.reset()` en vez de construir una lista, y cada
operación que puede fallar lleva `try`— y a cambio no asigna memoria dinámica ni una sola vez. Nim y
D consiguen casi la brevedad de Python compilando a nativo. El coste que ninguno de los tres esconde
es el ecosistema: sus comunidades y sus bibliotecas son órdenes de magnitud más pequeñas que las de
Go, y Zig además todavía rompe compatibilidad entre versiones.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere, no **cómo**
calcularlo paso a paso.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    split_string(Linea, " ", " ", Partes0),
    exclude(==(""), Partes0, Partes),
    length(Partes, N),
    atomic_list_concat(Partes, '-', Nombres),
    format("componentes=~d nombres=~w~n", [N, Nombres]).
```

### Datalog

```datalog
% Datalog puro no tiene E/S ni agregados: no puede contar ni concatenar.
% Lo más cercano es declarar los componentes como hechos y derivar la pertenencia.
componente("cli").
componente("api").
componente("web").

del_sistema(X) :- componente(X).
```

**Qué reconocer:** Prolog puede resolver el contrato entero, pero fíjate en que `length/2` y
`atomic_list_concat/3` son **relaciones**, no funciones: se satisfacen, no se llaman. Datalog no
llega: sin efectos, sin agregados y sin E/S, solo puede declarar qué componentes existen y qué se
deriva de ellos, y eso es honestamente todo lo que ofrece. Esa renuncia es la misma que hace SQL, y
explica el papel que esta familia tiene en un sistema real: nunca es el componente que habla con el
mundo, sino el que **describe reglas** —qué depende de qué, qué configuración es válida— para que
otro componente actúe sobre esa descripción.

---

## Y de vuelta a la clase

Veinte lenguajes, un solo problema, y el mismo esqueleto en todos: leer la línea, partirla, contar y
unir. Lo que cambia es la **forma** y, sobre todo, lo que cada elección le cuesta al sistema: cada
lenguaje extra es otra toolchain que mantener, otro artefacto que desplegar y otra persona que hay
que poder contratar. Eso es lo transferible.

⏮️ [Volver a la clase 165](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
