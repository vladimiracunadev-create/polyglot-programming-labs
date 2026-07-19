# Clase 114 — Funcional I: inmutabilidad y funciones puras

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La programación funcional no empieza por `map` ni por las lambdas: empieza por una decisión sobre el **estado**. El modelo imperativo que has usado hasta aquí razona en términos de celdas de memoria que cambian con el tiempo —una variable acumuladora, un contador, una lista que se va llenando—. El modelo funcional renuncia a ese estado mutable y describe el resultado como una **transformación** de los datos de entrada. En lugar de "recorre la lista y ve doblando cada número en un acumulador", dices "la lista de los dobles". Van Roy y Haridi (CTM, caps. 2-3) llaman a esto el **modelo declarativo** o sin estado, y lo presentan como el más simple de razonar precisamente porque nada cambia a tus espaldas.

El pilar teórico es la **transparencia referencial**, que Abelson y Sussman desarrollan desde la sección 1.1 de SICP: una expresión es referencialmente transparente si puedes sustituirla por su valor sin alterar el significado del programa. Eso solo es posible si las funciones son **puras** —su salida depende únicamente de sus argumentos y no producen efectos observables (no imprimen, no mutan, no dependen de un reloj o de una variable global)—. Una función pura es, en el sentido matemático, una función de verdad: la misma entrada da siempre la misma salida. Esa propiedad es la que hace que el "modelo de sustitución" de SICP funcione, y con él la capacidad de razonar sobre el código como sobre álgebra.

El objetivo de esta clase es que interiorices las dos caras de esa moneda con un ejemplo mínimo: **inmutabilidad** (transformar una lista sin tocar la original) y **pureza** (una función `x → 2x` sin efectos). Sebesta (cap. 15) sitúa estas ideas como el núcleo de los lenguajes funcionales, y verás que casi todos los lenguajes del núcleo —imperativos incluidos— ofrecen hoy `map` porque el estilo declarativo produce código más corto, más fácil de paralelizar y menos propenso a los errores por estado compartido que arruinan los programas grandes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección sin mutarla.
2. Reconocer la inmutabilidad.
3. Usar map en lugar de un bucle con estado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inmutabilidad | No modificar, crear nuevo |
| 2 | map | Transformar cada elemento |
| 3 | Sin estado mutable | Sin acumuladores |

## 📖 Definiciones y características

- **Funcional** — paradigma basado en funciones puras e inmutabilidad. Clave: sin efectos ni estado mutable.
- **Inmutabilidad** — los datos no cambian; las transformaciones crean nuevos. Clave: más seguro.
- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: no muta.

La propiedad que hace valiosa a una función pura es la **transparencia referencial** (SICP, sección 1.1): si `doble(3)` siempre vale `6` y no hace nada más, puedes reemplazar `doble(3)` por `6` en cualquier lugar sin cambiar el resultado del programa. Ese poder de sustitución, que parece trivial, es lo que permite razonar sobre el código con la seguridad del álgebra: no necesitas simular la ejecución paso a paso ni preguntarte "¿en qué estado está el programa ahora?". Abelson y Sussman contrastan este "modelo de sustitución" con el modelo imperativo, donde la introducción de asignación (`set!`) rompe la transparencia y obliga a razonar con la línea de tiempo del estado. Perder la transparencia, advierten, es perder la capacidad de razonar localmente.

La **inmutabilidad** es la condición que sostiene esa pureza a nivel de datos. Si `map` mutara la lista de entrada, la función dejaría de ser pura: tendría un efecto observable sobre el mundo exterior. Por eso `map` construye una colección **nueva** y deja la original intacta. Van Roy y Haridi (CTM, caps. 2-3) muestran que un programa escrito en el modelo declarativo —sin celdas mutables— es equivalente a un conjunto de definiciones matemáticas, y que esa equivalencia se pierde en cuanto introduces estado. La inmutabilidad no es una restricción caprichosa: es lo que mantiene el programa dentro del territorio donde el razonamiento formal, la memoización y la ejecución concurrente son seguros por construcción.

Conviene distinguir **`map` de un bucle con efectos**. Un `for` que acumula en una variable externa produce el mismo resultado, pero mezcla dos cosas: *qué* transformación se aplica y *cómo* se recorre y acumula. `map` separa ambas —recibe solo la función de transformación y se encarga del recorrido— y por eso es composable y trivialmente paralelizable: como cada elemento se transforma de forma independiente y sin efectos, el orden y la simultaneidad dan igual. Sebesta (cap. 15) señala esta ausencia de dependencias de orden como una de las razones por las que el estilo funcional encaja tan bien con el hardware multinúcleo actual.

## 🧩 Situación

Un clásico de los bugs difíciles: una función recibe una lista, la "procesa" y, sin que nadie lo esperara, deja la lista original modificada. Otra parte del programa que aún tenía una referencia a esa lista empieza a ver datos que no reconoce, y el error aparece lejos de donde se causó. Este tipo de fallo por **estado compartido y mutación** es de los más caros de depurar porque rompe la suposición más básica: que un valor que no tocaste sigue siendo el mismo.

El estilo funcional elimina la categoría entera de ese error. En vez de mutar, describes la transformación y obtienes un valor nuevo; la entrada queda intacta y cualquiera que la tuviera sigue viéndola igual. Esta clase reduce la idea a su mínima expresión: dada una lista de enteros, producir la lista de sus dobles. Los casos —`1 2 3 → doblados=2-4-6`, `5 → doblados=10`, `2 4 → doblados=4-8`— se resuelven con un `map` que no altera la lista original ni usa acumulador. La sencillez es intencional: deja ver la mecánica del paradigma sin que la lógica del problema estorbe.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por ->`
- **Regla:** doblados = map(x → 2x, lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6` |
| `5` | `doblados=10` |
| `2 4` | `doblados=4-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblados <- MAP(x -> 2x, lista) ; ESCRIBIR unidos por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = list(map(lambda x: x * 2, nums))
print("doblados=" + "-".join(str(x) for x in doblados))
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
console.log(`doblados=${doblados.join("-")}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
console.log(`doblados=${doblados.join("-")}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        String r = Arrays.stream(p).map(Integer::parseInt).map(x -> x * 2)
                .map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + r);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2);
Console.WriteLine($"doblados={string.Join("-", doblados)}");
```

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
	var doblados []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		doblados = append(doblados, strconv.Itoa(n*2))
	}
	fmt.Printf("doblados=%s\n", strings.Join(doblados, "-"))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<String> = s
        .split_whitespace()
        .map(|x| (x.parse::<i64>().unwrap() * 2).to_string())
        .collect();
    println!("doblados={}", doblados.join("-"));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("doblados=");
    while (scanf("%ld", &x) == 1) {
        if (!primero) printf("-");
        printf("%ld", x * 2);
        primero = 0;
    }
    printf("\n");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la transformación va en el SELECT, sin mutar.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$doblados = array_map(fn($x) => $x * 2, $nums);
echo "doblados=" . implode("-", $doblados) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `1 2 3 → doblados=2-4-6` de [`casos.json`](casos.json), con `5 → doblados=10` y `2 4 → doblados=4-8`. El verificador entrega la línea de enteros por `stdin` y espera el prefijo `doblados=` seguido de los dobles unidos por guiones.

**Python** expresa el paradigma casi con las palabras del pseudocódigo. Tras leer los números, la línea central es `doblados = list(map(lambda x: x * 2, nums))`. Aquí `map` recibe dos cosas: la **función pura** `lambda x: x * 2` —sin efectos, su salida solo depende de `x`— y la colección `nums`. Aplica la función a cada elemento y produce una secuencia nueva; `nums` no se toca en ningún momento. Para `1 2 3`, `map` genera `[2, 4, 6]`, y el `"-".join(...)` los une en `2-4-6`, imprimiendo `doblados=2-4-6`. Fíjate en que no hay acumulador ni índice: la transparencia referencial permitiría sustituir `map(lambda x: x*2, [1,2,3])` por `[2,4,6]` sin cambiar nada. Con `5` el resultado es la lista de un elemento `[10]` y sale `doblados=10`; el mismo código cubre el caso de un solo número sin ramas especiales.

**Haskell no está en el núcleo, pero Rust muestra la versión más cercana al ideal funcional** con su cadena de iteradores. La expresión `s.split_whitespace().map(|x| (x.parse::<i64>().unwrap() * 2).to_string()).collect()` encadena tres transformaciones puras: partir en palabras, doblar cada una, recolectar en un `Vec<String>`. Nada se muta; cada etapa produce un valor nuevo que alimenta a la siguiente. Y hay un detalle idiomático importante: en Rust `map` sobre un iterador es **perezoso** —no calcula nada hasta que `collect()` fuerza la evaluación—, lo que permite componer largas cadenas sin materializar listas intermedias. Para `2 4`, la cadena produce `["4", "8"]` y el `join("-")` da `doblados=4-8`.

El contraste instructivo lo pone **Go**, que en el núcleo carece de un `map` genérico idiomático y resuelve con un bucle explícito:

```go
for _, s := range strings.Fields(line) {
    n, _ := strconv.Atoi(s)
    doblados = append(doblados, strconv.Itoa(n*2))
}
```

Aquí sí hay estado que evoluciona —la rebanada `doblados` crece con cada `append`—. El resultado impreso es idéntico (`doblados=2-4-6`), pero el estilo es imperativo: el *qué* (doblar) y el *cómo* (recorrer y acumular) están entrelazados. Comparar esta versión con la de Python o Rust es el corazón de la clase: misma salida, dos mentalidades. **Java** (streams: `.map(x -> x * 2)`) y **C#** (LINQ: `.Select(x => x * 2)`) recuperan el estilo declarativo sobre una plataforma imperativa. El **SQL** lo hace a su manera, y de forma naturalmente inmutable: `group_concat(x * 2, '-')` transforma en el `SELECT` sin alterar la tabla —por eso el verificador no lo marca como una anomalía de mutación sino como la expresión declarativa del mismo cálculo—. Recorrer estas variantes deja ver que `map` no es una función de librería, sino una forma de pensar que muchos lenguajes terminaron adoptando.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map` (Python/JS/Rust), streams (Java), LINQ Select (C#). |
| Semántica | No muta la lista original; devuelve otra. |
| Paradigmática | SQL transforma en el SELECT, sin mutar. |

La diferencia real más profunda es **cuán en serio se toma cada lenguaje la inmutabilidad**. En Python, JavaScript o Java, `map` devuelve una colección nueva, pero nada te impide mutar la original con otra operación: la pureza es una disciplina, no una garantía. Rust la eleva a regla del compilador —un valor es inmutable salvo que lo declares `mut`, y el sistema de propiedad impide que dos partes muten lo mismo a la vez—, de modo que muchos errores de estado compartido ni siquiera compilan. Haskell va al extremo opuesto de lo imperativo: **todos** los valores son inmutables por defecto y los efectos se aíslan en el sistema de tipos (la mónada `IO`), lo que hace la transparencia referencial una propiedad del lenguaje entero, no del programador aplicado.

La segunda diferencia es **evaluación estricta frente a perezosa**. El `map` de Python o Java (streams) y los iteradores de Rust son perezosos: no producen nada hasta que algo consume el resultado (`list()`, `collect()`, un terminal de stream). El `map` sobre listas de JavaScript es estricto: calcula toda la lista de inmediato. Haskell es perezoso por defecto en todo el lenguaje, lo que permite trabajar con estructuras infinitas (`map (*2) [1..]`). Esta distinción, invisible en un caso de tres números, es decisiva en tuberías largas: la pereza evita materializar colecciones intermedias y puede convertir una cadena de `map`/`filter` en un único recorrido.

## 🧬 El concepto en la familia

En Haskell `map (*2) xs` es el ejemplo canónico y puro: sin efectos posibles, sobre datos inmutables por defecto y con evaluación perezosa. Lisp y Scheme —el linaje de SICP— tienen `map` desde hace décadas y lo usan como bloque de construcción junto a `filter` y `fold`/`reduce`, el trío que resume casi todo el procesamiento de listas funcional. Clojure hace de la inmutabilidad su bandera con estructuras de datos persistentes que comparten memoria entre versiones. Y los lenguajes imperativos convergieron: Java añadió *streams* en 8, C# tiene LINQ, C++ tiene `std::transform` y *ranges*. Que un concepto nacido en el mundo funcional haya colonizado a casi todos es la mejor evidencia de su valor: describir transformaciones en lugar de orquestar mutaciones produce código más corto, más seguro y más fácil de paralelizar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 114
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mutar dentro del map** → causa: efecto secundario → solución: mantener la transformación pura
- **Confundir map con for-each** → causa: map devuelve; for-each no → solución: usar map cuando quieres el resultado

## ❓ Preguntas frecuentes

- **¿Map es más lento que un bucle?** Generalmente comparable; y evita errores de estado.
- **¿Inmutabilidad no gasta memoria?** Crea nuevos datos, pero permite compartir y razonar mejor.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).

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

> [⏮️ Clase 113](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 115 ⏭️](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md)
