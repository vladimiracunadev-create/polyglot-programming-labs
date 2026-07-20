# Clase 056 — Entrada y salida básica: leer y escribir

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La Parte 3 cierra con lo más elemental y, a la vez, con lo que ha sostenido todas las clases anteriores sin haberse explicado: **leer de la entrada estándar y escribir en la salida estándar**. Cada implementación que has visto empieza consumiendo texto de `stdin` y termina emitiendo texto por `stdout`, y es esa frontera común la que permite al verificador comparar diez lenguajes con los mismos casos. Aquí ese contrato se ve desnudo, sin ninguna lógica que lo acompañe: el programa se limita a devolver lo que recibe con un prefijo.

Lo que hay debajo es una de las abstracciones más elegantes que heredamos de Unix. Un programa no habla con un teclado ni con una pantalla: habla con dos **flujos** de bytes que el sistema operativo le entrega ya abiertos, y de dónde vengan o adónde vayan no es asunto suyo. El mismo binario funciona igual si lo alimentas tecleando, si le rediriges un archivo o si lo conectas a la salida de otro programa con una tubería, y esa indiferencia es exactamente lo que hace componibles a las herramientas de línea de comandos, como se vio en la clase 028. Kernighan y Ritchie construyen sobre esta idea todo el capítulo de entrada y salida de *The C Programming Language*: la biblioteca no distingue archivos de terminales porque, para el programa, no hay diferencia.

Lo interesante para un curso comparativo es que algo tan simple como "leer una línea" resulta ser una de las operaciones donde más difieren los diez lenguajes, y no solo en la forma de escribirla. Difieren en qué unidad leen —una línea, todo el flujo, un token—, en qué te devuelven al llegar al final de la entrada, en si te obligan a gestionar el error de lectura, y en si dejan o no el salto de línea pegado al final de lo leído. Ese último detalle, aparentemente trivial, es el que decide si tu salida coincide carácter a carácter con la esperada.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Leer una línea completa de stdin y explicar en qué se diferencia de leer un token o el flujo entero.
2. Escribir en stdout con un formato dado y controlar el salto de línea final.
3. Reconocer el contrato stdin/stdout usado en todo el curso y por qué hace verificable la equivalencia.
4. Explicar qué hacen los lenguajes al llegar al final de la entrada y cómo se manifiesta el búfer de salida.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrada estándar (stdin) | El canal por defecto de entrada |
| 2 | Salida estándar (stdout) | El canal por defecto de salida |
| 3 | Leer una línea | Distinto de leer un token o un carácter |
| 4 | El contrato del curso | stdin → stdout, verificable |

## 📖 Definiciones y características

- **stdin** — canal de entrada estándar de un programa. Clave: de donde se leen los datos por defecto.
- **stdout** — canal de salida estándar. Clave: donde se escribe el resultado que se verifica.
- **Leer una línea** — obtener texto hasta el salto de línea. Clave: incluye espacios internos.
- **Eco** — devolver la entrada tal cual (con un prefijo). Clave: el ejemplo mínimo de E/S.

**stdin** y **stdout** no son dispositivos sino **flujos**, y esa distinción es la que da todo el poder. El sistema operativo entrega a cada proceso tres canales ya abiertos —entrada, salida y error, identificados por los descriptores 0, 1 y 2— y el programa escribe y lee sin saber qué hay al otro lado. Por eso `python main.py` funciona igual si tecleas la entrada, si escribes `< datos.txt` para redirigir un archivo o si otro programa te la envía por una tubería: la fuente cambia, el código no. La existencia de un canal de error separado del de salida obedece a la misma lógica: permite que los mensajes de diagnóstico no contaminen el resultado que otro programa va a consumir. Para este curso la consecuencia es directa: el verificador puede alimentar cualquier implementación con los casos de `casos.json` sin que ninguna de ellas sepa que la está probando una máquina.

**Leer una línea** parece una operación primitiva y no lo es. Significa consumir bytes hasta encontrar un salto de línea, lo que la distingue de leer un *token* —que se detendría en el primer espacio y perdería el resto del texto— y de leer el flujo entero. Los lenguajes se reparten entre estas tres estrategias, y algunos ni siquiera ofrecen la primera: en JavaScript y en C# lo idiomático aquí es consumir todo el flujo y recortar, mientras que Python, Java, Go, C y PHP tienen una lectura de línea explícita. Dos detalles semánticos separan a unos de otros. El primero es el **salto de línea final**, que la mayoría de las funciones de lectura conservan en el texto devuelto y que hay que recortar a mano: si no lo haces, tu salida lleva un salto de más y el verificador la rechaza, con razón. En Windows ese terminador son dos caracteres, `\r\n`, de ahí que las implementaciones recorten ambos y no solo `\n`. El segundo es qué ocurre al llegar al **final de la entrada**: C devuelve `NULL`, Java devuelve `null`, Python devuelve una cadena vacía y Rust envuelve el resultado en un `Result` que te obliga a decidir qué hacer si la lectura falla. Son cuatro convenciones distintas para la misma situación, y confundirlas es una fuente clásica de programas que se cuelgan o que fallan con entrada vacía.

Hay una tercera pieza que casi nunca se enseña y que explica comportamientos desconcertantes: el **búfer de salida**. Escribir en `stdout` no suele llegar de inmediato a su destino, porque el sistema acumula los bytes y los envía en bloque para no pagar el coste de una llamada al sistema por cada carácter. Lo llamativo es que la política cambia según a quién escribas: cuando la salida va a una terminal, se vacía línea a línea para que veas los mensajes al momento; cuando va a una tubería o a un archivo, se acumula en bloques mucho mayores. Ese cambio silencioso es la causa de que un programa que en la terminal imprime en el orden esperado muestre la salida desordenada respecto a los mensajes de error al redirigirla, y de que un programa que aborta pueda perder lo último que "imprimió". No afecta a los ejemplos de esta clase, que son diminutos, pero conviene conocerlo antes de que aparezca en un programa real.

## 🧩 Situación

Todo programa de este curso lee de stdin y escribe en stdout, y por eso el verificador puede comprobarlos a todos con el mismo procedimiento sin saber nada de sus lenguajes. El "eco" es la forma más simple posible de ese contrato: no calcula nada, solo demuestra que el programa sabe recibir y emitir. Precisamente por no tener lógica, deja al descubierto lo único que queda: cómo cada lenguaje obtiene el texto y cómo lo devuelve.

Y ahí aparece la sorpresa. En un problema sin ninguna dificultad algorítmica, las diez implementaciones se separan en cuatro grupos según lo que consideran natural: leer una línea (Python, Java, Go, C, PHP), leer el flujo entero (JavaScript, TypeScript, C#, Rust), y no leer nada porque el paradigma no lo contempla (SQL). El error más probable en esta clase no es lógico sino de un solo carácter: dejar el salto de línea pegado al final y producir `eco: hola\n\n` donde se esperaba `eco: hola\n`. Que el fallo más fácil de cometer en todo el curso sea invisible al ojo humano y evidente para una comparación exacta resume bien por qué el verificador existe.

## 🧮 Modelo

- **Entrada** (stdin): una línea de texto
- **Salida** (stdout): `eco: <la línea leída>`
- **Regla:** salida = 'eco: ' + entrada

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `eco: hola` |
| `Polyglot` | `eco: Polyglot` |
| `123` | `eco: 123` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER linea
ESCRIBIR "eco: " linea
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

linea = sys.stdin.readline().rstrip("\n")
print(f"eco: {linea}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
console.log(`eco: ${linea}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
console.log(`eco: ${linea}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        System.out.println("eco: " + linea);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
Console.WriteLine($"eco: {linea}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	line = strings.TrimRight(line, "\r\n")
	fmt.Printf("eco: %s\n", line)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    println!("eco: {linea}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[1024];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    printf("eco: %s\n", buf);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no lee stdin: se muestra el eco sobre una tabla de textos.
WITH lineas(x) AS (VALUES ('hola'), ('Polyglot'), ('123'))
SELECT printf('eco: %s', x) AS resultado
FROM lineas;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$linea = rtrim(fgets(STDIN), "\r\n");
echo "eco: $linea\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El eje que ordena estas implementaciones es **qué unidad considera natural leer cada lenguaje** y cuánta ceremonia exige para conseguirla. En un extremo, Python resuelve todo en una línea porque su biblioteca estándar da la lectura de línea hecha. En el otro, Java necesita envolver `System.in` en un `InputStreamReader` y este a su vez en un `BufferedReader`, una torre de decoradores que parece burocracia pero que expresa una separación real: uno convierte bytes en caracteres según una codificación, el otro añade el búfer que hace eficiente leer línea a línea. Go hace explícito lo mismo con `bufio` y con el carácter terminador como argumento; C baja un nivel más y te obliga a reservar tú el búfer y decidir su tamaño, con todo lo que eso implica sobre líneas más largas de lo previsto; y Rust convierte el posible fallo de lectura en un valor que el sistema de tipos te impide ignorar. Ninguna de esas diferencias es de estilo: cada una expone cuánto decide el lenguaje por ti y cuánto te deja a ti, que es el eje que recorre toda la Parte 3.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `input()`/`readline` (Python), `readFileSync(0)` (JS), `fgets` (C). |
| Semántica | Hay que quitar el salto de línea final para que el eco sea exacto. |
| Paradigmática | SQL no lee stdin: se muestra el eco sobre una tabla de textos. |

## 🧬 El concepto en la familia

En Ruby se escribe `gets.chomp`: dos operaciones encadenadas, leer y recortar, con un verbo dedicado (`chomp`) que quita el terminador de línea y solo el terminador de línea, a diferencia de un `strip` genérico que se llevaría también los espacios. En C++ es `std::getline(std::cin, s)`, y su firma delata otra filosofía: la línea leída no se devuelve, se deposita en una variable que pasas por referencia, mientras el valor de retorno se reserva para indicar si la lectura tuvo éxito; ese patrón permite el idiom `while (std::getline(...))` para recorrer toda la entrada. C++ además recorta el `\n` por ti, cosa que su antepasado C no hace.

Haskell es el que más se aleja y el más instructivo. `getLine` no es una función que lea, sino un valor de tipo `IO String`: una **descripción** de una acción de entrada que producirá una cadena cuando el sistema de ejecución la lleve a cabo. En un lenguaje puramente funcional, leer del mundo exterior no puede ser una expresión corriente, porque dos llamadas idénticas darían resultados distintos y eso rompería la transparencia referencial de la que depende todo el modelo. La solución es marcar la impureza en el tipo: cualquier función que lea o escriba lo declara en su firma, y el compilador impide mezclarla con código puro por descuido. Como beneficio secundario, `getLine` sí devuelve la línea sin el salto final. Recorrer la familia de Python a Haskell deja ver que "leer una línea" va de operación trivial a decisión de diseño del lenguaje entero según cuánto se comprometa cada uno con la pureza.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 056
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar el salto de línea pegado** → causa: la mayoría de las funciones de lectura conservan el `\n` en el texto devuelto → solución: recortar con trim/chomp/TrimRight antes de imprimir, y recortar también `\r` para que funcione con entradas generadas en Windows.
- **Leer un token en vez de la línea** → causa: usar una lectura que se detiene en el primer espacio y perder el resto del texto → solución: leer la línea completa siempre que el dato pueda contener espacios.
- **Recortar con un trim genérico cuando el dato lleva espacios significativos** → causa: `strip` elimina todos los espacios de los extremos, no solo el terminador → solución: recortar explícitamente los caracteres de fin de línea, como hacen las implementaciones de esta clase.
- **No contemplar el final de la entrada** → causa: cada lenguaje señala el EOF a su manera (`NULL` en C, `null` en Java, cadena vacía en Python, un `Result` en Rust) → solución: comprobar el resultado de la lectura antes de usarlo, o el programa fallará con entrada vacía.
- **Usar un búfer de tamaño fijo sin comprobar el desbordamiento en C** → causa: `fgets` corta la línea si excede el búfer y deja el resto en el flujo → solución: dimensionar con criterio y verificar si se leyó la línea completa; nunca usar funciones sin límite de longitud.
- **Mezclar mensajes de diagnóstico con el resultado** → causa: imprimir avisos por stdout → solución: enviarlos al canal de error, que existe precisamente para no contaminar la salida que otro programa consumirá.

## ❓ Preguntas frecuentes

- **¿stdin y un archivo son distintos?** Conceptualmente no: stdin es un flujo de bytes, y el sistema operativo puede conectarlo al teclado, a un archivo redirigido o a la salida de otro programa. El programa no lo sabe ni le importa, y esa indiferencia es lo que hace que las herramientas de línea de comandos se puedan encadenar.
- **¿Por qué el curso usa stdin/stdout?** Porque es el único contrato que los diez lenguajes comparten sin adaptaciones: no requiere red, ni archivos, ni bibliotecas externas, y permite verificar la equivalencia con los mismos casos para todos. Cualquier otra frontera obligaría a escribir un envoltorio distinto por lenguaje y ya no estaríamos comparando el lenguaje sino el envoltorio.
- **¿Por qué hay que recortar el salto de línea si es "invisible"?** Precisamente porque es invisible al leerlo pero no a una comparación de texto exacta. `eco: hola\n` y `eco: hola\n\n` son cadenas distintas, y el verificador las trata como tales. Es el mejor recordatorio de que la salida de un programa es una cadena de bytes, no una impresión visual.
- **¿Por qué Java necesita tres objetos para leer una línea?** Porque separa responsabilidades que otros lenguajes fusionan: `System.in` entrega bytes, `InputStreamReader` los convierte en caracteres según una codificación, y `BufferedReader` añade el búfer que hace eficiente la lectura por líneas. Es más ceremonioso, pero cada capa es sustituible: puedes cambiar la codificación sin tocar el resto.
- **¿Y si la entrada tiene varias líneas?** Entonces hay que decidir explícitamente si lees una, un número fijo o hasta el final del flujo, y cada lenguaje ofrece su forma de recorrerlo. Esta clase se queda en una sola línea a propósito, para que la diferencia entre lenguajes no quede tapada por la lógica del recorrido.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 055](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 057 ⏭️](../../parte-4-control-del-programa/057-booleanos-condiciones-y-cortocircuito/README.md)
