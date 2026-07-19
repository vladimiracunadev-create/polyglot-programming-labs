# Clase 050 — Tipado estático vs. dinámico

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Esta clase aborda uno de los dos grandes ejes con los que se clasifica cualquier lenguaje: **cuándo se comprueban los tipos**. En el **tipado estático** la comprobación ocurre *antes* de ejecutar —al compilar o al analizar el programa— y por eso muchos errores de tipos se descubren sin correr una sola línea. En el **tipado dinámico** el tipo viaja pegado al valor y se comprueba *durante* la ejecución, en el momento de cada operación. La pregunta clave no es "¿tiene tipos?" —casi todos los tienen— sino "¿en qué instante se verifica que la operación es legal para esos tipos?".

Pierce lo formula con precisión en *Types and Programming Languages*: un sistema de tipos estático es un método **sintáctico** que, examinando el texto del programa, prueba la **ausencia de ciertos comportamientos** sin ejecutarlo. Sebesta enmarca lo mismo como una decisión de **ligadura**: en el tipado estático el tipo se liga a la *variable* y esa ligadura se fija en compilación; en el dinámico el tipo se liga al *valor* y la variable no tiene tipo propio, solo apunta a valores que sí lo tienen. De ahí que en Python una misma variable pueda contener hoy un entero y mañana una lista, mientras que en Go una variable declarada como `int` lo será para siempre.

El laboratorio elige la operación más reveladora: sumar un entero con un real. En Python `2 + 3.5` da `5.5` sin ceremonia; en Go debes escribir `float64(a) + b`. La misma suma expone la filosofía de cada lenguaje: quién decide el tipo del resultado, cuándo lo decide, y si te obliga a hacer visible la **promoción** del entero a real. Es importante no confundir este eje con el de la clase 051: estático/dinámico es *cuándo* se comprueba; fuerte/débil es *cuántas* conversiones inseguras se toleran. Son ejes independientes, y precisamente por eso existen las cuatro combinaciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Sumar valores de tipos distintos (entero + real).
2. Reconocer dónde hace falta convertir explícitamente.
3. Explicar estático vs. dinámico con un ejemplo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipado estático | El compilador conoce y comprueba los tipos |
| 2 | Tipado dinámico | El tipo se conoce al ejecutar |
| 3 | Promoción numérica | Entero que se convierte a real para operar |
| 4 | Errores en compilación vs. ejecución | Cuándo se detecta un tipo mal usado |

## 📖 Definiciones y características

- **Tipado estático** — los tipos se fijan y comprueban en compilación (Java, C#, Go, Rust, C). Clave: errores antes de ejecutar.
- **Tipado dinámico** — los tipos se resuelven en ejecución (Python, PHP, JS). Clave: flexible, errores más tarde.
- **Promoción** — convertir un entero a real para operar con otro real. Clave: en estáticos suele ser explícita.
- **Comprobación de tipos** — verificar que las operaciones son válidas para los tipos. Clave: estática o dinámica.

La distinción real está en la **ligadura de tipo** y en su *tiempo*. En un lenguaje estático el tipo se liga a la variable en el momento de la compilación: cuando escribes `int a;` en C o `var a int` en Go, el compilador anota "esta ranura de memoria solo contiene enteros" y verifica cada uso contra esa promesa. Si intentas guardar ahí un texto, el programa **no llega a ejecutarse**: el error se reporta antes. En un lenguaje dinámico la variable es solo un nombre que apunta a un valor, y es el **valor** quien lleva su tipo consigo en tiempo de ejecución; la comprobación —"¿puedo sumar estos dos objetos?"— ocurre en el instante mismo de la operación, examinando los tipos de los operandos reales.

Ese desplazamiento en el tiempo tiene consecuencias tangibles, no filosóficas. El tipado estático detecta antes de correr una familia entera de errores —pasar un argumento del tipo equivocado, llamar a un método inexistente, mezclar unidades incompatibles— y esa red de seguridad escala bien en bases de código grandes, donde nadie recuerda todos los contratos. El precio es rigidez: el compilador exige que satisfagas sus reglas incluso para un prototipo desechable. El tipado dinámico invierte el trato: máxima flexibilidad y un ciclo de iteración velocísimo, a cambio de que ciertos errores solo se manifiesten cuando el flujo de ejecución llega a la línea culpable, quizá en producción y con un dato inusual. Por eso los proyectos dinámicos grandes se apoyan en pruebas abundantes y en anotaciones opcionales (*type hints* de Python, TypeScript sobre JavaScript) que recuperan parte de la comprobación temprana.

Un matiz que Sebesta subraya y que conviene grabar: **estático/dinámico no dice nada sobre fuerte/débil**. C es estático pero deja pasar muchas conversiones inseguras (débil); Python es dinámico pero rechaza `"5" + 5` (fuerte). El primer eje es *cuándo se comprueba*; el segundo, *qué se tolera*. La **promoción** numérica de esta clase vive en esa intersección: el entero `a` debe volverse real para sumarse con `b`, y en los estáticos rigurosos (Go, Rust) esa conversión se escribe a mano, mientras que en los dinámicos el intérprete la resuelve por coerción numérica al vuelo.

## 🧩 Situación

Estás calculando el total de una factura: una cantidad entera de unidades (`2`) y un ajuste con decimales (`3.5`). Sumar `2 + 3.5` parece trivial, pero es justo donde los lenguajes revelan su carácter. En Python el intérprete ve un `int` y un `float`, aplica su coerción numérica y devuelve `5.5` sin que tú intervengas: la comprobación de que ambos son "sumables" ocurre en el instante de la operación. En Go el compilador se niega a compilar `a + b` si `a` es `int` y `b` es `float64` —los considera tipos distintos e incompatibles— y te obliga a escribir `float64(a) + b`, haciendo la **promoción visible en el código**.

Ninguna de las dos posturas es "correcta" en abstracto; son compromisos distintos. La rigidez de Go elimina la clase de bug donde una conversión numérica silenciosa introduce una pérdida de precisión inadvertida; la fluidez de Python te deja escribir la fórmula como en un papel, al precio de que un tipo inesperado (un `None`, un texto) solo estalle al ejecutarse. La misma línea de suma, verificada contra `casos.json`, sirve de lente para ver esa diferencia de filosofía sin ambigüedades.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (a entero, b real)
- **Salida** (stdout): `suma=<a+b con 2 decimales>`
- **Regla:** suma = a + b (a entero promovido a real)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 3.5` | `suma=5.50` |
| `10 0.25` | `suma=10.25` |
| `0 0` | `suma=0.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a (entero), b (real)
ESCRIBIR "suma=" FORMATEAR(a+b, 2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

p = sys.stdin.readline().split()
a = int(p[0])
b = float(p[1])
print(f"suma={a + b:.2f}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
const a = parseInt(x, 10);
const b = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [x, y]: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const a: number = parseInt(x, 10);
const b: number = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        double b = Double.parseDouble(p[1]);
        System.out.printf(Locale.US, "suma=%.2f%n", a + b);
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)}");
```

### Go · `go run main.go`

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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.ParseFloat(f[1], 64)
	fmt.Printf("suma=%.2f\n", float64(a)+b)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = v[0].parse().unwrap();
    let b: f64 = v[1].parse().unwrap();
    println!("suma={:.2}", a as f64 + b);
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a;
    double b;
    if (scanf("%ld %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f\n", (double) a + b);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL evalúa la expresión numérica de forma uniforme.
WITH pares(a, b) AS (VALUES (2, 3.5), (10, 0.25), (0, 0))
SELECT printf('suma=%.2f', a + b) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $x;
$b = (float) $y;
printf("suma=%.2f\n", $a + $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Tomemos el primer caso de `casos.json` —`stdin` = `2 3.5`, esperado `suma=5.50`— y observemos cómo cada lenguaje construye ese `5.50`, prestando atención a **cuándo** decide los tipos.

En **Python**, `p = sys.stdin.readline().split()` parte la línea `"2 3.5"` en la lista `["2", "3.5"]`. Las dos líneas siguientes son la clave: `a = int(p[0])` y `b = float(p[1])`. Aquí no hay ninguna declaración de tipo; `a` y `b` son solo nombres, y el tipo vive en los **objetos** a los que apuntan —un `int` y un `float`—. Cuando llega `a + b`, el intérprete inspecciona en ese instante los tipos de ambos objetos, ve que uno es entero y otro real, aplica su coerción numérica (promueve el `2` a `2.0`) y produce el `float` `5.5`. Esa comprobación es *dinámica*: sucede en ejecución, línea a línea. El `{a + b:.2f}` formatea a dos decimales y da la salida literal `suma=5.50`. Con el caso `0 0`, `a` y `b` valen `0` y `0.0`, la suma es `0.0` y el formato produce `suma=0.00`.

**Go** cuenta la historia opuesta. Tras `strconv.Atoi(f[0])` la variable `a` tiene tipo `int` —fijado en compilación— y `strconv.ParseFloat(f[1], 64)` deja `b` como `float64`. Si el código dijera `a + b`, el compilador de Go **rechazaría el programa antes de ejecutarlo** con un error de tipos incompatibles: para Go, `int` y `float64` no se mezclan. Por eso la línea real es `fmt.Printf("suma=%.2f\n", float64(a)+b)`: el `float64(a)` es la **promoción explícita** que convierte el entero a real para que la suma sea legal. La comprobación ocurrió en compilación; en ejecución ya está todo resuelto. **Rust** hace lo mismo con `a as f64 + b`, y **C** con `(double) a + b`: los tres lenguajes estáticos te obligan a nombrar la promoción que Python realiza sola.

El contraste se resume así: los dinámicos (**Python**, **JavaScript**, **PHP**) leen, convierten con `int`/`float`/`parseInt`/`(int)` y suman confiando en que el tipo real se verificará al vuelo; los estáticos (**Java**, **C#**, **Go**, **Rust**, **C**) fijan los tipos al declarar las variables y exigen que la promoción entero→real sea visible. Pese a esas dos filosofías, las diez implementaciones convergen en la misma salida `suma=5.50`, que es lo que el verificador contrasta contra `casos.json`.

## 🔬 Comparación

La diferencia de fondo es el **momento de la comprobación** y, con él, el momento en que un error de tipos se hace visible. En los dinámicos el tipo acompaña al valor y todo se decide al ejecutar; en los estáticos el tipo se liga a la variable y el compilador dictamina antes de correr. La promoción entero→real es el detalle donde esto se toca con el dedo: implícita en los dinámicos, explícita en los estáticos rigurosos.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Python/JS/PHP suman directo; Go exige `float64(a)+b`, Rust `a as f64 + b`, C `(double) a + b`. |
| Semántica (tiempo) | En estáticos el tipo se liga a la variable y se comprueba en compilación; en dinámicos se liga al valor y se comprueba al ejecutar. |
| Semántica (errores) | Un tipo mal usado detiene la compilación en Java/Go/Rust/C; en Python/JS/PHP solo estalla cuando la ejecución alcanza esa línea. |
| Paradigmática | SQL evalúa la expresión numérica de forma uniforme sobre filas, sin declarar variables ni fijar tipos por nombre. |

## 🧬 El concepto en la familia

En Ruby (dinámico y fuerte) `a + b` funciona por coerción numérica, igual que Python. En Haskell (estático y muy fuerte) hace falta `fromIntegral a + b`, más estricto aún que Go, porque su inferencia Hindley-Milner rechaza mezclar un `Int` con un `Double` sin una conversión nombrada. TypeScript es un caso interesante: añade comprobación estática *sobre* JavaScript, un lenguaje dinámico, y por eso el mismo programa puede tener errores atrapados por `tsc` en compilación que en JS puro solo aparecerían al ejecutar. Esto ilustra que estático y dinámico no son cajones cerrados sino un espectro que un lenguaje puede recorrer con anotaciones y verificadores opcionales.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 050
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Sumar `int` y `float` sin convertir en Go/Rust** → causa: el compilador rechaza tipos mezclados → solución: promueve el entero a real explícitamente (`float64(a)`, `a as f64`).
- **Confiar en el tipo en un dinámico** → causa: un dato inesperado (un `None`, un texto) rompe en ejecución, quizá en producción → solución: valida la entrada donde el compilador no puede ayudarte, y apóyate en pruebas.
- **Creer que "dinámico" significa "sin tipos"** → causa: confundir *sin comprobación estática* con *sin tipos* → solución: Python sí tiene tipos y los comprueba; solo lo hace en ejecución, no antes.
- **Suponer que el tipado estático elimina todos los errores** → causa: exceso de confianza en el compilador → solución: recuerda que atrapa errores de *tipo*, no de *lógica*; un `float64(a)+b` puede compilar y aun así calcular algo incorrecto.

## ❓ Preguntas frecuentes

- **¿Cuál es mejor?** Ninguno en abstracto. El estático atrapa errores antes y escala en equipos grandes; el dinámico itera más rápido y es cómodo para prototipos y scripts. Depende del tamaño del proyecto y de su tolerancia a fallos en ejecución.
- **¿Por qué Go obliga a convertir?** Para que la promoción entero→real sea visible en el código y no exista ninguna conversión numérica silenciosa que pueda ocultar una pérdida de precisión.
- **¿Los *type hints* de Python lo vuelven estático?** No en ejecución: el intérprete los ignora. Pero una herramienta externa (`mypy`, `pyright`) los comprueba *antes* de correr, acercando Python a una comprobación estática opcional.
- **¿Es más rápido el código estático?** A menudo sí, porque el compilador conoce los tipos y genera código especializado sin inspeccionarlos en ejecución; el dinámico paga el coste de resolver el tipo en cada operación.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 5 (ligadura de tipo y su tiempo) y cap. 6 (comprobación estática vs. dinámica).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), cap. 1 (el tipado como método sintáctico previo a la ejecución).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 7 (type checking estático y dinámico).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), sobre tipado dinámico y *type hints*.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), §3.1 (sin conversiones numéricas implícitas).
- S. Klabnik y C. Nichols — *The Rust Programming Language*, cap. 3 (tipos fijados en compilación) — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 049](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 051 ⏭️](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md)
