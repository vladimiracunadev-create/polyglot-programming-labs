# Clase 158 — Enlaces (bindings) y wrappers

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase 156 mostró que la FFI cruda es peligrosa: tipos que hay que emparejar a mano, memoria de la que nadie se hace cargo, errores que se convierten en caídas. Nadie quiere programar así todo el día. Por eso entre la librería nativa y tu código idiomático se interpone una capa: el **binding** y su cara amable, el **wrapper**. El objetivo de esta clase es entender esa capa como lo que es —una **abstracción que oculta la frontera**— y ver por qué toda librería nativa que usas cómodamente (NumPy, `cryptography`, `sqlite3`) es en realidad un binding envolviendo C.

La idea de fondo es la ocultación de información, uno de los principios que Newman recorre en *Building Microservices*: un componente expone una interfaz limpia y esconde su implementación. El binding hace exactamente eso a través de una frontera de lenguaje. Por dentro llama a C con `ctypes` y `unsafe`; por fuera ofrece una función que se siente nativa de tu lenguaje: recibe tus tipos, devuelve tus tipos, lanza tus excepciones. El wrapper es la costura invisible que convierte "una función de C que devuelve un `int` y un código de error" en "un método Python que devuelve un objeto o lanza una excepción". Aprender a razonar sobre esa costura —qué debe traducir, qué debe ocultar, dónde puede filtrarse— es aprender a vivir con librerías nativas sin sufrir su frontera.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Envolver** una función nativa con un wrapper idiomático.
2. **Explicar** qué añade un binding sobre la FFI cruda.
3. **Reconocer** los generadores de bindings comunes de cada lenguaje.
4. **Identificar** cuándo una abstracción de frontera "tiene fugas".

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Binding | El puente que expone una librería nativa en tu lenguaje |
| 2 | Wrapper | La capa que adapta la interfaz a un uso idiomático |
| 3 | Adaptación y ocultación | Traducir tipos y errores, y esconder la frontera |

## 📖 Definiciones y características

Un **binding** es la capa que expone una librería escrita en otro lenguaje dentro del tuyo. Su promesa es reutilizar sin reescribir: el binding de `sqlite3` en Python te da una base de datos completa sin que veas una línea de C. Un **wrapper** es, en fino, cada función que envuelve a otra para adaptar su interfaz —convertir tipos, reordenar argumentos, traducir códigos de error en excepciones, gestionar la memoria. Y la **adaptación** es el trabajo concreto que hace el wrapper: tomar los tipos y convenciones de la librería nativa y presentarlos como los tipos y convenciones naturales de tu lenguaje.

La distinción importante es entre *tener acceso* y *tener una buena interfaz*. La FFI cruda te da acceso; el wrapper te da una buena interfaz. Un binding bien hecho es una abstracción: esconde que por debajo hay C, punteros y memoria manual. Pero toda abstracción puede *filtrar*: si el wrapper deja escapar un puntero crudo, un código de error numérico o un requisito de "libera esto tú mismo", la frontera reaparece y el usuario del binding acaba lidiando con detalles que la capa debería haber ocultado. El buen wrapper, como la buena interfaz de servicio de Newman, es aquel que puedes usar sin saber qué hay detrás.

- **Binding** — capa que expone una librería de otro lenguaje en el tuyo. Clave: reutilizar código probado sin reescribirlo.
- **Wrapper** — función que envuelve otra adaptando su interfaz. Clave: uso más cómodo, seguro e idiomático.
- **Adaptación** — traducir tipos, convenciones y errores entre la librería nativa y tu código. Clave: ocultar la frontera por completo.

## 🧩 Situación

Pillow, la librería de imágenes de Python, no procesa píxeles en Python: envuelve `libjpeg`, `zlib` y compañía, todas en C. El binding convierte un `PIL.Image` en punteros que C entiende, llama a la rutina nativa de compresión y traduce el resultado de vuelta a objetos Python, transformando cualquier error de C en una excepción `IOError`. Tú escribes `img.save("foto.jpg")` y nunca ves la frontera. Para mostrar ese patrón sin compilar `libjpeg`, esta clase usa un wrapper mínimo: toma un número, llama a la "función nativa" `doble` y **envuelve** el resultado en un formato de presentación `wrap(...)`. La operación es diminuta; lo que se ilustra es la costura: hay una función nativa por dentro y una interfaz amable por fuera.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `envuelto=wrap(<2n>)`
- **Regla:** wrapper que aplica doble y formatea

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `envuelto=wrap(10)` |
| `0` | `envuelto=wrap(0)` |
| `7` | `envuelto=wrap(14)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
r <- doble(n) ; ESCRIBIR 'wrap(' + r + ')'
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def doble(x):
    return x * 2


def wrapper(x):  # adapta y formatea el resultado
    return f"wrap({doble(x)})"


n = int(sys.stdin.readline())
print(f"envuelto={wrapper(n)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const wrapper = (x) => `wrap(${doble(x)})`;

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const wrapper = (x: number): string => `wrap(${doble(x)})`;

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; }
    static String wrapper(long x) { return "wrap(" + doble(x) + ")"; }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("envuelto=" + wrapper(n));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long Doble(long x) => x * 2;
string Wrapper(long x) => $"wrap({Doble(x)})";

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"envuelto={Wrapper(n)}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func doble(x int64) int64 { return x * 2 }
func wrapper(x int64) string { return fmt.Sprintf("wrap(%d)", doble(x)) }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("envuelto=%s\n", wrapper(n))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2
}

fn wrapper(x: i64) -> String {
    format!("wrap({})", doble(x))
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("envuelto={}", wrapper(n));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(long x) { return x * 2; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("envuelto=wrap(%ld)\n", doble(n));
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa vistas para envolver; aqui, la expresion formateada.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('envuelto=wrap(%d)', n * 2) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function doble($x) { return $x * 2; }
function wrapper($x) { return "wrap(" . doble($x) . ")"; }

$n = (int) trim(fgets(STDIN));
echo "envuelto=" . wrapper($n) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

El caso `5` debe producir `envuelto=wrap(10)`. Hay dos pasos encadenados: la "función nativa" `doble` calcula `10`, y el `wrapper` lo presenta como `wrap(10)`. Esa separación en dos funciones no es adorno: es exactamente la anatomía de un binding —una capa que *calcula* (el núcleo nativo) y otra que *adapta* (el wrapper).

En **Python** se ve con claridad. `doble(x)` es el núcleo (en producción, la llamada por FFI); `wrapper(x)` es la capa de adaptación: `return f"wrap({doble(x)})"`. El wrapper no repite el cálculo, lo *delega* y solo se encarga del formato de presentación. `main` invoca únicamente `wrapper(n)`, nunca `doble` directamente: el usuario del binding solo conoce la interfaz amable, jamás toca la frontera. Sobre `5`, `doble(5)` da `10`, `wrapper` lo envuelve y sale `envuelto=wrap(10)`.

En **Go**, la estructura es idéntica pero la adaptación de tipos es explícita: `func wrapper(x int64) string { return fmt.Sprintf("wrap(%d)", doble(x)) }`. Aquí el wrapper hace algo que un binding real hace siempre: **cambia de tipo**. `doble` devuelve un `int64` (dato crudo del núcleo); `wrapper` devuelve un `string` (dato presentable). Esa conversión de "tipo de la librería" a "tipo cómodo para el consumidor" es la esencia de la adaptación.

En **C**, en cambio, *no hay wrapper*. El código escribe `printf("envuelto=wrap(%ld)\n", doble(n))`: envuelve en línea, sin una función intermedia. Es coherente con lo que C representa en esta parte: C es el **núcleo nativo**, el que se envuelve, no el que envuelve. Ver que C resuelve el mismo caso sin capa de adaptación —mientras Python y Go sí la tienen— ilustra la asimetría real: los lenguajes de alto nivel construyen wrappers *alrededor* de C, no al revés.

## 🔬 Comparación

| Lenguaje | Cómo se genera el binding a una librería nativa |
|---|---|
| Python | `ctypes`/`cffi` a mano, o `pybind11` / Cython para envolver C/C++ con una API pythónica. |
| JavaScript | node-gyp + N-API compilan un addon; el módulo JS resultante oculta el C++. |
| Java | JNA (declarativo, sin escribir C) o JNI (manual); Panama moderniza ambos. |
| C# | P/Invoke con `[DllImport]` y atributos de *marshalling* que adaptan tipos. |
| Go | cgo genera el puente; el paquete Go envuelve la función C en una idiomática. |
| Rust | `bindgen` genera las firmas crudas; encima se escribe una "safe wrapper" que oculta el `unsafe`. |
| C | Es el núcleo: expone la librería que los demás envuelven. |
| PHP | Extensión Zend en C, o la clase `FFI` envuelta en una clase PHP. |

La tabla muestra el patrón universal: **capa cruda generada + capa idiomática escrita a mano**. `bindgen` de Rust lo hace literal: produce declaraciones `unsafe` feas, y el programador escribe encima un módulo seguro y ergonómico —doble capa, igual que en el laboratorio. La diferencia de fondo entre lenguajes es cuánto trabajo automatizan: JNA de Java evita escribir C por completo, mientras JNI obliga a escribirlo; pybind11 hace el binding casi declarativo, mientras `ctypes` lo deja todo en tus manos. SQL vuelve a ser el caso aparte: no envuelve funciones nativas, sino que se "envuelve a sí mismo" con vistas que encapsulan consultas tras un nombre estable.

## 🧬 El concepto en la familia

Los generadores de bindings son un ecosistema por derecho propio: pybind11 y Cython en Python, node-gyp/N-API en Node, JNA y JNI en la JVM, `bindgen`/`cbindgen` en Rust, SWIG como veterano multilenguaje. Todos resuelven la misma tensión: exponer código nativo probado sin obligar a cada usuario a lidiar con la frontera. El wrapper es la versión intra-proceso de la ocultación de información que gobierna toda la parte: una interfaz limpia sobre una implementación que preferirías no ver.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 158
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Wrapper que filtra detalles de la frontera** → causa: dejar escapar un puntero crudo o un código de error numérico → solución: la abstracción debe ser completa; si el usuario ve un `void*`, el wrapper falló.
- **No manejar errores de la librería nativa** → causa: ignorar el código de retorno de C y seguir con datos corruptos → solución: traducir cada error nativo a una excepción o `Result` del lenguaje anfitrión.
- **Fugas de memoria en la frontera** → causa: el wrapper reserva en C y no libera al destruirse el objeto → solución: atar la liberación al ciclo de vida del objeto (destructor, `Drop`, `try-with-resources`).
- **Wrapper que rehace el trabajo del núcleo** → causa: reimplementar la lógica en vez de delegar → solución: el wrapper solo adapta; el cálculo se queda en la librería nativa probada.

## ❓ Preguntas frecuentes

- **¿Binding o reescribir la librería?** El binding reutiliza código probado por miles de usuarios; reescribir cuesta meses y reintroduce bugs ya resueltos. Se reescribe solo cuando la librería nativa no encaja o el coste de mantener el binding supera al de un port.
- **¿El wrapper añade coste?** Sí, uno pequeño: una llamada de indirección y quizá una conversión de tipos. A cambio da seguridad, ergonomía y manejo de errores. En bucles muy calientes se ofrece una vía "sin envolver" para expertos, pero la interfaz por defecto es la amable.
- **¿Qué es una "abstracción con fugas"?** Una interfaz que promete ocultar la implementación pero deja escapar sus detalles: el binding que te obliga a llamar `free()` a mano, o a conocer el orden de bytes interno. La ley de las abstracciones con fugas dice que ninguna es perfecta; el arte está en minimizar las grietas.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). La idea de una interfaz estable sobre una implementación cambiante.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Cap. 2–3: ocultación de información y contratos como interfaz.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 4: adaptación de tipos y transparencia de acceso.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly). Envoltura de librerías C y diseño de APIs pythónicas.
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

> [⏮️ Clase 157](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 159 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/159-serializacion-entre-lenguajes-json-protobuf-messagepack/README.md)
