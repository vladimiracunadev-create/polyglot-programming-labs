# Clase 049 — Conversión de tipos: casting explícito vs. coerción implícita

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Todo programa que recibe datos del mundo exterior —un formulario, una línea de un archivo, una celda de una tabla— los recibe casi siempre como **texto**, y no puede calcular con ellos sin antes cambiarles el tipo. Esa transformación de un valor de un tipo a otro es la **conversión**, y es una de las operaciones más silenciosamente peligrosas del oficio, porque unas veces la ordenas tú y otras la inserta el lenguaje a tus espaldas. Esta clase separa con rigor esos dos mundos: el **casting explícito**, donde escribes `int(x)` y asumes la responsabilidad de lo que ocurra, y la **coerción implícita**, donde el compilador o el intérprete decide convertir por ti para que una operación de tipos mezclados "cuadre".

La distinción no es cosmética. Sebesta define la coerción precisamente como una conversión de tipos que el compilador realiza de forma **implícita**, y advierte que las coerciones *debilitan* la comprobación de tipos: cada conversión automática que el lenguaje acepta es un error de discordancia de tipos que deja de reportarse. Pierce, en *Types and Programming Languages*, describe un sistema de tipos como un método sintáctico para **probar la ausencia de ciertos comportamientos**; la coerción implícita erosiona esa promesa, porque hace que expresiones que "deberían" ser un error de tipos produzcan en cambio un resultado sorprendente pero legal. De ahí el ejemplo clásico del tipado débil: `"5" + 3` puede dar `"53"`, `8` o un error según el lenguaje, y esa ambigüedad nace de qué coerciones inserta cada uno.

El laboratorio de esta clase toma el caso más común y honesto: convertir un texto a real, y ese real a entero **truncando** hacia cero. Verás que Python, Rust o Go te obligan a nombrar la conversión, mientras C la realiza a través de un `cast` de C que descarta la parte fraccionaria, y que **truncar no es redondear** —`3.7` se vuelve `3`, no `4`—, una diferencia semántica que produce bugs cuando se confunde `int(x)` con `round(x)`.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Convertir texto a número.
2. Convertir un real a entero por truncamiento.
3. Diferenciar casting explícito de coerción implícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | De texto a número | Parsear la entrada |
| 2 | Truncamiento | Quitar la parte decimal hacia cero |
| 3 | Casting explícito | El programador ordena la conversión |
| 4 | Coerción implícita | El lenguaje convierte solo |

## 📖 Definiciones y características

Conviene fijar cuatro términos y, sobre todo, entender cómo se relacionan:

- **Conversión (casting)** — cambiar explícitamente el tipo de un valor. Clave: `int(x)`, `(long)f`.
- **Coerción** — conversión automática que inserta el lenguaje. Clave: fuente de sorpresas en los débilmente tipados.
- **Truncamiento** — descartar la parte decimal hacia cero. Clave: distinto de redondear.
- **Parseo** — interpretar un texto como un número. Clave: primer paso de casi toda entrada.

La palabra "conversión" es el término paraguas: significa producir, a partir de un valor de tipo `A`, un valor equivalente de tipo `B`. Lo que separa el **casting** de la **coerción** no es *qué* ocurre sino *quién lo ordena*. En el casting explícito el programador escribe la conversión —`int(f)`, `(long) f`, `f as i64`— y por tanto la conversión es visible, auditable y localizable en una revisión de código. En la coerción implícita nadie la escribe: el lenguaje la introduce durante la evaluación de una expresión de tipos mezclados. Es la diferencia entre una decisión declarada y una decisión tomada por el sistema en tu nombre.

Sebesta subdivide las conversiones en dos clases según el riesgo. Una conversión es **ensanchante** (*widening*) cuando el tipo destino puede representar todos los valores del origen —`int` a `double`, por ejemplo— y por eso es segura; es **estrechante** (*narrowing*) cuando el destino tiene menos capacidad —`double` a `int`— y puede perder información. El truncamiento de esta clase es exactamente una conversión estrechante: `3.7` cabe holgado en un `double` pero al pasarlo a entero pierde el `.7`. Los lenguajes cautelosos permiten las coerciones ensanchantes en silencio (son inofensivas) pero exigen que las estrechantes se pidan a mano, justamente porque tiran datos. Esa política —qué se coacciona solo y qué se debe pedir— es una de las decisiones de diseño más reveladoras de un lenguaje, y es lo que las diez implementaciones de abajo ponen lado a lado.

Un matiz preciso, para no arrastrar confusiones a las clases siguientes: convertir es una **operación sobre valores** (produce un nuevo valor de otro tipo), mientras que el eje *estático/dinámico* de la clase 050 es una propiedad de **cuándo se comprueban** los tipos y el eje *fuerte/débil* de la 051 mide **cuántas coerciones inseguras** admite el lenguaje. Un lenguaje estático puede permitir muchas coerciones (C) o casi ninguna (Rust); esa es la ortogonalidad que iremos separando pieza a pieza.

## 🧩 Situación

Imagina el backend de un carrito de compras. El navegador envía la cantidad `"3.7"` como una cadena dentro de un cuerpo HTTP —para el servidor no es un número, son tres caracteres—. Antes de multiplicarla por un precio necesitas un `float`; y si esa cantidad representa unidades indivisibles (cajas, licencias, asientos) quizá necesites además su parte entera. Ahí aparecen, en tres líneas, los dos peligros de esta clase: primero el **parseo**, que puede fallar si el texto no es un número; después la conversión **estrechante** a entero, donde debes decidir conscientemente si truncas o redondeas.

El bug tristemente célebre es tratar `int("3.7")` como si diera `4`. No: la conversión a entero **trunca hacia cero**, así que da `3`, y facturar 3 unidades cuando el cliente pidió 3.7 (o cuando esperabas redondear a 4) es un descuadre real de negocio. Cada lenguaje del núcleo exige aquí un grado distinto de explicitud —algunos te obligan a nombrar cada paso, otros convierten en cuanto pueden— y esa diferencia de temperamento es justo lo que el laboratorio hace visible.

## 🧮 Modelo

- **Entrada** (stdin): un número real como texto
- **Salida** (stdout): `entero=<parte entera truncada> real=<valor con 2 decimales>`
- **Regla:** entero = truncar(real) ; real formateado a 2 decimales

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3.7` | `entero=3 real=3.70` |
| `5.0` | `entero=5 real=5.00` |
| `8.9` | `entero=8 real=8.90` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER texto
real <- A_REAL(texto)
entero <- TRUNCAR(real)
ESCRIBIR "entero=" entero " real=" FORMATEAR(real,2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

f = float(sys.stdin.readline().strip())
print(f"entero={int(f)} real={f:.2f}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const f = parseFloat(readFileSync(0, "utf8").trim());
console.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const f: number = parseFloat(readFileSync(0, "utf8").trim());
console.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        double f = Double.parseDouble(br.readLine().trim());
        System.out.printf(Locale.US, "entero=%d real=%.2f%n", (long) f, f);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
double f = double.Parse(Console.In.ReadToEnd().Trim(), inv);
Console.WriteLine($"entero={(long)f} real={f.ToString("F2", inv)}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f, _ := strconv.ParseFloat(strings.TrimSpace(line), 64)
	fmt.Printf("entero=%d real=%.2f\n", int64(f), f)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let f: f64 = s.trim().parse().unwrap();
    println!("entero={} real={:.2}", f as i64, f);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    double f;
    if (scanf("%lf", &f) != 1) return 1;
    printf("entero=%ld real=%.2f\n", (long) f, f);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: CAST(x AS INTEGER) trunca hacia cero.
WITH nums(x) AS (VALUES (3.7), (5.0), (8.9))
SELECT printf('entero=%d real=%.2f', CAST(x AS INTEGER), x) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$f = (float) trim(fgets(STDIN));
printf("entero=%d real=%.2f\n", (int) $f, $f);
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el viaje de un solo dato —`3.7`— desde el texto de `stdin` hasta la salida literal del primer caso de `casos.json`: `entero=3 real=3.70`. Aunque cada archivo esté escrito en un lenguaje distinto, todos ejecutan la misma secuencia: **leer → parsear → truncar → formatear**, y lo instructivo es dónde cada uno pone una conversión explícita y dónde deja que el lenguaje decida.

En **Python**, la línea `f = float(sys.stdin.readline().strip())` hace dos cosas encadenadas. `sys.stdin.readline()` devuelve la cadena `"3.7\n"`; `.strip()` le quita el salto de línea y deja `"3.7"`; y `float(...)` es el **casting explícito** de texto a real —Python nunca convierte un `str` a número por su cuenta, así que si no escribieras `float` no habría número—. La segunda línea, `print(f"entero={int(f)} real={f:.2f}")`, encierra las dos conversiones que nos importan. `int(f)` toma el `3.7` y lo **trunca hacia cero** a `3`: es la conversión estrechante, y es explícita porque escribimos `int`. El fragmento `{f:.2f}` no cambia el tipo de `f` —sigue siendo un `float`— sino que lo **formatea** a dos decimales para imprimir, produciendo `3.70`. Junta ambas y obtienes exactamente `entero=3 real=3.70`. Con el caso `5.0`, `int(5.0)` es `5` y `{f:.2f}` es `5.00`, de ahí `entero=5 real=5.00`.

**C** ofrece el contraste más nítido sobre "quién trunca". Ahí `scanf("%lf", &f)` parsea directamente el texto a un `double`, y la conversión decisiva vive dentro de `printf`: el `(long) f` es un *cast* de C, la forma explícita de convertir el `double 3.7` a entero. El estándar de C especifica que al convertir de punto flotante a entero la parte fraccionaria **se descarta** (truncamiento hacia cero), por lo que `(long) 3.7` es `3` —nunca `4`—. Es interesante notar que C es un lenguaje *relativamente débil*: en muchos contextos aritméticos convierte enteros a `double` sin que lo pidas (promoción implícita), pero para esta conversión estrechante seguimos escribiendo el cast, porque el programador de C convive con estas reglas a mano.

Los lenguajes más estrictos lo dejan aún más patente. En **Rust**, `let f: f64 = s.trim().parse().unwrap();` obliga a anotar el tipo destino `f64` para que `parse` sepa a qué convertir, y luego `f as i64` es la única forma admitida de pasar de real a entero: Rust **no** coacciona `f64` a `i64` en ningún caso implícito, así que sin ese `as` el código no compila. En **Go**, `int64(f)` cumple el mismo papel: Go presume de no tener conversiones numéricas implícitas, de modo que la conversión a entero se escribe siempre. Frente a ellos, **JavaScript** y **PHP** son los del temperamento débil: en JS el truncamiento se expresa con `Math.trunc(f)` y `f.toFixed(2)` para el formato, y aunque aquí el código es explícito, es el mismo lenguaje donde `"5" + 3` concatenaría —el motivo por el que se prefiere ser explícito—. Todas estas rutas, pese a su distinta ceremonia, convergen en la misma línea de salida del contrato, que es justo lo que el verificador comprueba contra `casos.json`.

## 🔬 Comparación

Lo que separa a estos lenguajes no es *qué* calculan —todos truncan hacia cero y formatean a dos decimales— sino cuánta explicitud te **exigen** y qué garantías te dan a cambio. En un extremo, Rust y Go no admiten ninguna conversión numérica implícita: la conversión estrechante siempre se escribe (`as i64`, `int64(...)`). En el otro, C acepta muchas promociones aritméticas en silencio, pero la conversión de real a entero sigue siendo un *cast* declarado. Python y Java se sitúan en medio: son de tipado fuerte (no suman texto con número sin permiso) pero ofrecen constructores/casts cómodos —`int(f)`, `(long) f`— para las conversiones que sí quieres.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `int(f)` (Python), `Math.trunc(f)` (JS/TS), `(long) f` (Java/C/C#), `int64(f)` (Go), `f as i64` (Rust), `CAST(x AS INTEGER)` (SQL). |
| Semántica | El truncamiento va **hacia cero** en todos; no confundir con redondeo (`round`) ni con `floor` (que difieren en negativos). Es una conversión estrechante que pierde la parte fraccionaria. |
| Semántica (formato) | `.2f`, `toFixed(2)`, `%.2f`, `F2` solo dan formato al imprimir: no cambian el tipo del valor, que sigue siendo real. |
| Paradigmática | Los imperativos parsean `stdin` y convierten paso a paso; SQL usa `CAST(x AS INTEGER)` sobre una tabla de valores, sin lectura ni variables. |

## 🧬 El concepto en la familia

En Ruby `f.to_i` trunca hacia cero; en Haskell `truncate f`, que además convive con `round`, `floor` y `ceiling` como funciones distintas y nombradas. En C++ se prefiere `static_cast<long>(f)` sobre el cast al estilo C `(long)f`, precisamente para que la conversión sea buscable y difícil de escribir por accidente. La familia entera comparte una regla: la conversión de real a entero descarta la parte fraccionaria (para positivos coincide con `floor`, pero para negativos no: `truncate(-3.7)` es `-3`, mientras que `floor(-3.7)` es `-4`). Ese detalle de los negativos es la trampa más frecuente al portar código entre lenguajes que eligen convenciones distintas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 049
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir truncar con redondear** → causa: esperar `4` de `3.7` → solución: si quieres redondear usa `round`; la conversión a entero siempre trunca hacia cero.
- **Sumar texto y número** → causa: olvidar convertir la entrada, que llega como cadena → solución: parsea siempre el texto antes de operar; en un lenguaje débil `"3" + 4` no fallará pero dará algo inesperado.
- **Asumir que el parseo nunca falla** → causa: dar por hecho que `stdin` trae un número válido → solución: en producción, `int("abc")` lanza excepción en Python, `parseInt` devuelve `NaN` en JS y `strconv.Atoi` retorna un error en Go; maneja el caso.
- **Perder precisión con reales grandes** → causa: convertir un `double` enorme a entero de 32 bits → solución: elige el tamaño destino (`long`/`i64`) consciente del rango, porque la conversión estrechante no avisa del desbordamiento.

## ❓ Preguntas frecuentes

- **¿Truncar y `floor` son lo mismo?** Solo para valores positivos. Truncar va **hacia cero** y `floor` va **hacia abajo**: con `-3.7`, truncar da `-3` y `floor` da `-4`.
- **¿Qué es exactamente la coerción implícita?** Que el lenguaje convierta un tipo sin que lo escribas, dentro de una expresión de tipos mezclados (p. ej. PHP evalúa `"3" + 4` como `7`). Es cómoda pero silencia errores de tipos.
- **Si formateo con `%.2f`, ¿estoy convirtiendo el número?** No. El formato produce una **representación textual** para imprimir; el valor sigue siendo real. Convertir cambia el tipo del valor; formatear solo elige cómo se ve.
- **¿Por qué C convierte enteros a `double` solo pero me obliga al cast para el truncamiento?** Porque la promoción entero→real es ensanchante (segura, no pierde datos) y el estándar la hace sola; la conversión real→entero es estrechante (pierde la fracción) y por eso se pide a mano.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 6 "Data Types" (conversión, coerción, *widening*/*narrowing*).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), cap. 1 (qué prueba y qué no un sistema de tipos) y cap. 15 (subtipado y coerciones).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 7 (type conversion y casting).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre números y tipos numéricos.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. 1 "Values, Types, and Operators" (coerción) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), §3 (conversiones numéricas explícitas).
- S. Klabnik y C. Nichols — *The Rust Programming Language*, cap. 3 (tipos escalares y `as`) — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), §2.7 (conversiones de tipo).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly), sobre *type juggling*.

---

> [⏮️ Clase 048](../../parte-3-valores-tipos-y-variables/048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 050 ⏭️](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md)
