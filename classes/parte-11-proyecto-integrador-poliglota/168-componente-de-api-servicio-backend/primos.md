# 🧬 El mismo programa en las familias de lenguajes — Clase 168

> [⬅️ Volver a la clase 168](README.md) · [🌐 Atlas de familias](../../../atlas/README.md) · [📚 Índice](../../README.md)

Esta página lleva la tesis del programa hasta el final: **aprende el representante, reconoce la
familia entera**. El mismo problema de la clase —responder a una petición con un código y el dato
solicitado— resuelto por los **primos** de cada familia del
[Atlas](../../../atlas/README.md), no solo por los diez lenguajes del núcleo.

Si entendiste la versión de Python, la de Ruby te resultará familiar aunque no la hayas visto nunca.
Ese reconocimiento es exactamente lo que este curso quiere producir.

> ⚠️ **Qué está verificado y qué no.** **Ruby, Perl y Lua se ejecutan en CI** contra el mismo
> `casos.json` que el núcleo, igual que las diez implementaciones de la clase
> ([workflow Labs](../../../labs/README.md)). Los **otros 17 primos son material de lectura**: su
> toolchain no está en el workflow, así que están escritos para ser correctos pero sin el sello de
> la máquina. Verificar tres de veinte no es verificarlos todos.

## El contrato, igual para todos

- **Entrada** (stdin, una línea): un entero `n`, el dato solicitado
- **Salida** (stdout): `respuesta=200 datos=<n>`
- **Regla:** responder con el código 200 y devolver el dato pedido

| stdin | esperado |
|---|---|
| `5` | `respuesta=200 datos=5` |
| `0` | `respuesta=200 datos=0` |
| `42` | `respuesta=200 datos=42` |

El programa simula la petición por stdin a propósito: lo que decide de verdad el lenguaje de un
componente de API no es esta línea, sino **el servidor que la hospeda**. Por eso cada apartado nombra
los frameworks reales de la familia y su madurez operativa: quién tiene un ecosistema que soporta un
servicio en producción a las tres de la mañana y quién no.

---

<a id="scripting-dinamico"></a>

## Scripting dinámico

**Representantes del núcleo:** [Python](README.md#python) · [PHP](README.md#php).
La familia que domina el backend por volumen: iteración rápida, despliegue sin compilar y una
biblioteca de terceros para cada integración que se te ocurra.

### Ruby

```ruby
n = STDIN.gets.strip
puts "respuesta=200 datos=#{n}"
```

### Perl

```perl
chomp(my $n = <STDIN>);
print "respuesta=200 datos=$n\n";
```

### Lua

```lua
local n = io.read("l")
print("respuesta=200 datos=" .. n)
```

### Tcl

```tcl
gets stdin n
puts "respuesta=200 datos=[string trim $n]"
```

### R

```r
n <- readLines("stdin", n = 1)
cat(sprintf("respuesta=200 datos=%s\n", n))
```

**Qué reconocer:** los cinco escriben la respuesta igual —interpolar el dato en una plantilla de
texto— pero como plataforma de servicio están a distancias enormes. **Ruby** es el único de los cinco
con madurez comparable a Python: **Sinatra** para un servicio pequeño, **Rails** cuando hay dominio,
migraciones y autenticación de por medio; hosting, observabilidad y contratación resueltos. **Perl**
tiene servidores serios de verdad —**Mojolicious** con async y WebSockets nativos, **Dancer2** para
lo minimalista, ambos sobre PSGI, el equivalente Perl de WSGI—, pero contratar y mantener ese código
en 2026 es un riesgo organizativo más que técnico. **Lua** no se despliega solo: se despliega dentro
de **OpenResty**, que incrusta LuaJIT en nginx; ahí es excelente y está en producción a escala en
CDNs y API gateways, pero el modelo es "extiendo el proxy", no "escribo el servicio". **Tcl** tiene
servidores reales y veteranos —**tclhttpd**, y AOLserver, que sostuvo servicios grandes en su
momento—, hoy en mantenimiento y sin comunidad nueva. **R** con **Plumber** convierte funciones
anotadas en endpoints HTTP y es la elección correcta para **exponer un modelo estadístico**, no para
ser el backend del sistema: su concurrencia es de un solo proceso por defecto y se escala poniendo
varios detrás de un balanceador.

---

<a id="javascript-web"></a>

## JavaScript / web

**Representantes del núcleo:** [JavaScript](README.md#javascript) · [TypeScript](README.md#typescript).

### Dart

```dart
import 'dart:io';

void main() {
  final n = stdin.readLineSync()!.trim();
  print('respuesta=200 datos=$n');
}
```

### ActionScript 3

```actionscript
// ActionScript corre en el reproductor Flash: es cliente, no servidor. No tiene
// stdin ni puede escuchar en un puerto; solo sabe consumir una API ajena. Se
// ilustra la composicion de la respuesta.
package {
    public class Api {
        public static function respuesta(n:int):String {
            return "respuesta=200 datos=" + n;
        }
    }
}
```

**Qué reconocer:** aquí la familia se parte en dos. **Dart** sí es una opción de backend real: el
paquete **shelf** es el equivalente de Express en su ecosistema, compila a binario nativo con
`dart compile exe`, y el argumento fuerte es compartir el modelo de dominio con la app Flutter que
consume la API —una ventaja organizativa concreta, no estética—. Su punto débil es el tamaño de la
comunidad de servidor: casi todo el peso de Dart está en el cliente. **ActionScript** es la
demostración de que "pertenecer a la familia web" no implica poder hospedar nada: nació dentro de un
reproductor y su modelo de ejecución no contempla escuchar en un puerto. Un lenguaje puede compartir
sintaxis con Node y no compartir ni una sola de sus capacidades de servidor.

---

<a id="jvm"></a>

## JVM

**Representante del núcleo:** [Java](README.md#java). La plataforma con la operación de servicios
más madura que existe: métricas, *profiling* en caliente, recolectores de basura ajustables y
décadas de servidores en producción.

### Kotlin

```kotlin
fun main() {
    val n = readLine()!!.trim()
    println("respuesta=200 datos=$n")
}
```

### Scala

```scala
object Api extends App {
  val n = scala.io.StdIn.readLine().trim
  println(s"respuesta=200 datos=$n")
}
```

### Groovy

```groovy
def n = System.in.newReader().readLine().trim()
println "respuesta=200 datos=$n"
```

### Clojure

```clojure
(require '[clojure.string :as str])

(let [n (str/trim (read-line))]
  (println (str "respuesta=200 datos=" n)))
```

**Qué reconocer:** los cuatro heredan **entera** la infraestructura de servicio de Java —el mismo
JDBC, el mismo *thread pool*, las mismas herramientas de diagnóstico— y por eso cualquiera de ellos
es defendible para un backend serio. Lo que cambia es el estilo del framework. **Kotlin** tiene
**Ktor**, escrito por JetBrains sobre corrutinas, con rutas declaradas en un DSL; es la apuesta más
segura de las cuatro porque además puede usar Spring Boot sin fricción. **Scala** tiene **Play**, y
alrededor un ecosistema funcional propio; su coste real no es el rendimiento sino el tiempo de
compilación y la curva de un equipo que no venga de ahí. **Groovy** aporta **Grails** y **Ratpack**,
y sobre todo la capacidad de escribir el servicio con la sintaxis de un script; su tipado dinámico
por defecto es precisamente lo que quisiste evitar al elegir la JVM. **Clojure** cambia de paradigma
sin salir de la máquina virtual: **Ring** define el servicio como una función de mapa-petición a
mapa-respuesta, y **Pedestal** o Compojure construyen encima. Los cuatro despliegan el mismo `.jar`
y arrancan con el mismo `java -jar`.

---

<a id="dotnet"></a>

## .NET

**Representante del núcleo:** [C#](README.md#c-1).

### F\#

```fsharp
let n = stdin.ReadLine().Trim()
printfn "respuesta=200 datos=%s" n
```

### VB.NET

```vbnet
Module Api
    Sub Main()
        Dim n = Console.ReadLine().Trim()
        Console.WriteLine("respuesta=200 datos=" & n)
    End Sub
End Module
```

**Qué reconocer:** los tres corren sobre **ASP.NET Core**, que es el servidor de verdad: Kestrel, el
*middleware pipeline*, la inyección de dependencias y la configuración son idénticos se escriba el
código en el lenguaje que se escriba. **F#** tiene además dos capas idiomáticas propias —**Giraffe**,
que expone el pipeline de ASP.NET como composición de funciones, y **Falco**, más ligero— y su
argumento defendible es modelar los estados válidos de la API con uniones discriminadas, de modo que
una respuesta imposible no compile. **VB.NET** puede hospedar ASP.NET Core sin problema técnico
alguno, pero conviene ser honesto: Microsoft declaró el lenguaje **estable, sin nuevas
características**, las plantillas de proyecto web modernas no lo incluyen y casi toda la
documentación y los ejemplos están en C#. Elegirlo hoy para un servicio nuevo es una decisión que
solo se sostiene si ya existe una base de código VB que el equipo mantiene.

---

<a id="c-llaves"></a>

## C / llaves

**Representante del núcleo:** [C](README.md#c). Aquí no hay framework por defecto: hay sockets,
y todo lo demás lo pones tú.

### C++

```cpp
#include <iostream>
#include <string>

int main() {
    std::string n;
    std::cin >> n;
    std::cout << "respuesta=200 datos=" << n << '\n';
}
```

### Objective-C

```objc
#import <Foundation/Foundation.h>

int main(void) {
    @autoreleasepool {
        char buf[64];
        scanf("%63s", buf);
        printf("respuesta=200 datos=%s\n", buf);
    }
    return 0;
}
```

**Qué reconocer:** **C++** sí tiene frameworks HTTP reales y usados —**Drogon**, **Crow**,
**Pistache**, **cpp-httplib** para lo mínimo— y es la elección legítima cuando la latencia de cola o
el consumo de memoria por conexión son requisitos escritos, no aspiraciones. El coste es igual de
concreto: gestión de memoria en un proceso expuesto a entrada de red, es decir, que un fallo de
manejo de búferes deja de ser un *crash* y pasa a ser una vulnerabilidad. **Objective-C** es el caso
opuesto: técnicamente puede servir HTTP con GNUstep o con las APIs de red de Foundation, pero no hay
un ecosistema de backend vivo; Apple lo mantiene para las apps existentes y todo lo nuevo va a Swift.
Compartir la sintaxis de C con el representante no dice nada sobre si el lenguaje puede sostener un
servicio.

---

<a id="sistemas"></a>

## Sistemas

**Representantes del núcleo:** [Go](README.md#go) · [Rust](README.md#rust). La familia que hoy se
elige por defecto para servicios donde importan el arranque en frío y la huella de memoria.

### Zig

```zig
const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    const linea = (try std.io.getStdIn().reader().readUntilDelimiterOrEof(&buf, '\n')).?;
    const n = std.mem.trim(u8, linea, " \r");
    try std.io.getStdOut().writer().print("respuesta=200 datos={s}\n", .{n});
}
```

### Nim

```nim
import std/strutils

let n = stdin.readLine().strip()
echo "respuesta=200 datos=" & n
```

### D

```d
import std.stdio, std.string;

void main() {
    const n = readln().strip();
    writefln("respuesta=200 datos=%s", n);
}
```

**Qué reconocer:** los tres producen un binario pequeño que arranca en milisegundos, igual que Go,
pero el soporte de servidor es muy desigual. **Zig** tiene `std.http.Server` en la biblioteca
estándar y eso es casi todo: el lenguaje aún no ha llegado a 1.0, cada versión rompe API, y no hay
un framework consolidado ni enrutamiento, ni sesiones, ni middleware que no escribas tú. **Nim**
tiene **Jester** —rutas declaradas con un DSL, sobre el `asynchttpserver` de la estándar— y funciona
bien para servicios pequeños; el punto flaco es el tamaño de la comunidad y que muchas bibliotecas
tienen un solo mantenedor. **D** tiene **Vibe.d**, que es el más completo de los tres: HTTP, fibras
para concurrencia, plantillas y clientes de base de datos en un solo proyecto, con años de recorrido;
aun así hablamos de un ecosistema de orden de magnitud menor que el de Go, y la disponibilidad de
gente que lo conozca es el argumento en contra que un equipo te va a poner primero.

---

<a id="logica-declarativa"></a>

## Lógica y declarativa

**Representante del núcleo:** [SQL](README.md#sql). Se describe **qué** se quiere devolver, no cómo
recorrer los datos para obtenerlo.

### Prolog

```prolog
:- initialization(main, main).

main :-
    read_line_to_string(user_input, Linea),
    normalize_space(string(N), Linea),
    format("respuesta=200 datos=~w~n", [N]).
```

### Datalog

```datalog
% Datalog no atiende peticiones ni escribe en stdout: no hay transporte, no hay
% codigo de estado y no hay efectos. El dato solicitado se declara como hecho y
% la respuesta es una relacion derivada de el.
solicitud(5).

respuesta(200, N) :- solicitud(N).
```

**Qué reconocer:** **Prolog** sorprende aquí: SWI-Prolog trae `library(http)` en la distribución
—servidor, enrutamiento, JSON y sesiones incluidos—, así que sí puede hospedar una API real, y hay
sistemas de reglas de negocio que exponen así su motor de inferencia. Ese es exactamente su nicho
defendible: cuando la lógica del dominio *es* un conjunto de reglas, escribirlas como reglas ahorra
más código del que cuesta el lenguaje raro. **Datalog** no puede ni acercarse: sin efectos ni E/S,
no es un candidato a componente de servicio sino un motor que **otro** componente consulta —igual que
la base de datos SQL de la clase 170—. Reconocer esa frontera es la mitad de la decisión: hay piezas
del sistema que se **eligen** y piezas que se **consultan**.

---

## Y de vuelta a la clase

Veinte lenguajes, la misma línea de respuesta, y una conclusión incómoda: escribir el *handler* es
lo barato. Lo caro es todo lo que hay debajo —el servidor, el modelo de concurrencia, los clientes de
base de datos, las métricas, la gente que sabrá mantenerlo—. Por eso este componente es el que menos
libertad te deja del sistema, y el que mejor prepara la discusión de la clase 175: cuando alguien
pregunte "¿por qué no lo escribiste en X?", la respuesta tiene que ser una lista de capacidades
verificables, no una preferencia.

⏮️ [Volver a la clase 168](README.md) · 🌐 [Ver las familias en el Atlas](../../../atlas/README.md)
