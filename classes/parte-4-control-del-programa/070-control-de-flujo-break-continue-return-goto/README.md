# Clase 070 — Control de flujo: break, continue, return, goto

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Un bucle bien escrito sabe cuándo parar, pero no siempre la condición de parada natural es la única. A veces el trabajo termina antes: has encontrado lo que buscabas, o has detectado que esta vuelta concreta no aporta nada. Para eso existen las **salidas anticipadas** —`break`, `continue`, `return`— y su antepasado salvaje, el `goto`. Todas comparten una misma naturaleza: transfieren el control a un punto distinto del siguiente en el texto del programa. Lo que las distingue es cuán restringido está su destino, y esa restricción es exactamente lo que las hace razonables.

En esta clase buscamos el menor divisor mayor que 1 de un número —un problema donde detenerse en cuanto se encuentra la respuesta no es una optimización opcional sino la forma correcta de expresar la intención— y aprovechamos ese ejemplo para recorrer toda la escala: `break`, que abandona el bucle más interno; `continue`, que abandona sólo la vuelta actual; `return`, que abandona la función entera; las etiquetas que permiten salir de varios bucles anidados a la vez; y el `goto`, que salta a cualquier parte. Detrás hay uno de los debates fundacionales de la disciplina: el que abrió Dijkstra en 1968 al llamar dañino al `goto` y que Knuth matizó en 1974 defendiendo que a veces la salida temprana es la forma más clara. Entender ese debate es entender por qué tu lenguaje te da estas construcciones y no otras.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Salir de un bucle con break.
2. Reconocer cuándo continue u otras salidas ayudan.
3. Evitar trabajo innecesario tras encontrar lo buscado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | break | Salir del bucle inmediatamente |
| 2 | continue | Saltar a la siguiente vuelta |
| 3 | Búsqueda con parada | Detenerse al encontrar |
| 4 | return dentro del bucle | Otra forma de salir |

## 📖 Definiciones y características

- **break** — termina el bucle inmediatamente. Clave: no sigue iterando.
- **continue** — salta al siguiente ciclo del bucle. Clave: ignora el resto de la vuelta.
- **Divisor** — número que divide a otro sin resto. Clave: el menor >1 revela si es primo.
- **goto** — salto incondicional (existe en C, desaconsejado). Clave: break/continue lo sustituyen.
- **return** — abandona la función entera, no sólo el bucle. Clave: la salida anticipada de mayor alcance.
- **Etiqueta de bucle** — nombre que permite romper un bucle exterior desde uno interior. Clave: no existe en todos los lenguajes.

El origen de todo esto es la carta que Dijkstra publicó en 1968 con el título *Go To Statement Considered Harmful*. Su argumento no era estético sino epistemológico: con `goto` libre se rompe la correspondencia entre el texto del programa y su ejecución, de modo que ya no basta señalar un punto del código para describir el estado del cómputo; hace falta además una historia de cómo se llegó hasta allí. Y sin esa correspondencia no se puede razonar con invariantes, que es la herramienta central de *Structured Programming*, el libro que Dahl, Dijkstra y Hoare publicaron poco después. El respaldo formal lo aporta el teorema de Böhm-Jacopini: cualquier programa computable puede expresarse combinando sólo secuencia, selección e iteración, así que el `goto` no añade poder expresivo —sólo desorden. Sebesta, en el capítulo de estructuras de control de *Concepts of Programming Languages*, recoge ese consenso y clasifica `break`, `continue` y `return` como salidas restringidas: saltos cuyo destino no es arbitrario sino determinado por la estructura del bloque que abandonan.

Ahí está la clave para entender por qué estas construcciones sobrevivieron a la condena del `goto`: son gotos domesticados. Un `break` sólo puede saltar a un sitio —justo después del bucle que lo contiene—, y un `return` sólo puede saltar al punto de llamada. El destino está fijado por la estructura, no elegido por el programador, así que el razonamiento por invariantes sigue siendo posible: basta añadir a la postcondición del bucle la posibilidad de haber salido por la vía anticipada. Knuth lo argumentó en 1974 en *Structured Programming with go to Statements*, un artículo que suele leerse mal como una defensa del `goto` cuando en realidad es una crítica al dogma: sostuvo que forzar la estructura pura a veces produce código *menos* claro —con banderas booleanas artificiales y condiciones compuestas ilegibles— y que una salida temprana bien colocada expresa mejor la intención. Ese es también el fondo del viejo debate sobre el *single entry, single exit*, la regla heredada de las guías de estilo de C que exigía un único `return` por función: nació cuando C no tenía destructores ni `finally` y la única forma de garantizar la liberación de recursos era llegar siempre al mismo punto final. En lenguajes con `defer`, `finally` o RAII esa justificación desapareció, y hoy la salida temprana con guardas al principio de la función se considera más legible que el anidamiento profundo.

## 🧩 Situación

Las salidas anticipadas aparecen en cualquier código que busque: encontrar el primer registro que cumple un criterio, validar una lista y abortar en la primera entrada inválida, recorrer una configuración hasta hallar la clave pedida. En todos esos casos, seguir iterando después de tener la respuesta no sólo desperdicia ciclos, sino que oscurece la intención: quien lee el bucle no sabe si el resto de las vueltas puede cambiar el resultado. Igual de común es el patrón inverso con `continue`: un bucle que procesa miles de líneas y descarta al principio de la vuelta las vacías, las comentadas o las ya vistas, evitando así anidar todo el cuerpo dentro de un `if` gigante.

El coste de ingeniería se mide en dos direcciones. Por un lado, no salir a tiempo: un escaneo lineal completo donde bastaba el primer acierto convierte una operación de microsegundos en una de segundos cuando el conjunto crece, y ese tipo de degradación sólo se manifiesta en producción con datos reales. Por otro, salir de forma confusa: un `break` que rompe el bucle equivocado dentro de un anidamiento, un `continue` colocado antes del incremento del contador que produce un bucle infinito, o un `return` en medio de una función larga que se salta la liberación de un recurso. Este último es el caso que dio origen al patrón `goto cleanup` del kernel de Linux, uno de los pocos usos del `goto` que la comunidad acepta sin discusión: en C no hay destructores ni `defer`, así que concentrar en una etiqueta al final de la función la liberación de todo lo adquirido —y saltar allí desde cualquier punto de fallo— es más seguro y más legible que repetir la limpieza en cada rama de error. El `goto` sigue siendo dañino como mecanismo general; sobrevive precisamente donde el lenguaje no ofrece una alternativa estructurada.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 2)
- **Salida** (stdout): `primer_divisor=<el menor divisor > 1>`
- **Regla:** el menor d en [2..n] tal que n % d == 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `15` | `primer_divisor=3` |
| `7` | `primer_divisor=7` |
| `12` | `primer_divisor=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA d de 2 a n: SI n%d==0: guardar d ; ROMPER
ESCRIBIR "primer_divisor=" d
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
d = 2
while d <= n:
    if n % d == 0:
        break
    d += 1
print(f"primer_divisor={d}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int d = 2;
        for (; d <= n; d++) {
            if (n % d == 0) break;
        }
        System.out.println("primer_divisor=" + d);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int d = 2;
for (; d <= n; d++) {
    if (n % d == 0) break;
}
Console.WriteLine($"primer_divisor={d}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	d := 2
	for ; d <= n; d++ {
		if n%d == 0 {
			break
		}
	}
	fmt.Printf("primer_divisor=%d\n", d)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut d = 2;
    while d <= n {
        if n % d == 0 {
            break;
        }
        d += 1;
    }
    println!("primer_divisor={d}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long d = 2;
    for (; d <= n; d++) {
        if (n % d == 0) break;
    }
    printf("primer_divisor=%ld\n", d);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el menor divisor > 1 con MIN sobre un rango (ilustrativo).
WITH RECURSIVE d(k) AS (VALUES (2) UNION ALL SELECT k + 1 FROM d WHERE k < 15)
SELECT printf('primer_divisor=%d', min(k)) AS resultado
FROM d WHERE 15 % k = 0;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$d = 2;
for (; $d <= $n; $d++) {
    if ($n % $d === 0) {
        break;
    }
}
echo "primer_divisor=$d\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `15` de `casos.json`, cuya salida esperada es `primer_divisor=3`. En **Python**, `n = int(sys.stdin.readline())` fija `n = 15` y `d = 2` inicializa el candidato. Entra el `while d <= n:` y comprueba `2 <= 15` (verdadero). Dentro, `if n % d == 0:` evalúa `15 % 2`, que da `1`, así que la condición es falsa y no se ejecuta el `break`; el flujo llega a `d += 1` y `d` pasa a `3`. Segunda vuelta: `3 <= 15` es verdadero, y ahora `15 % 3` da `0`, la condición se cumple y se ejecuta `break`. Aquí está el detalle que importa: el `break` transfiere el control fuera del bucle *inmediatamente*, sin ejecutar el `d += 1` que viene después y sin volver a evaluar `d <= n`. Por eso `d` conserva el valor `3` —el divisor encontrado— y `print(f"primer_divisor={d}")` imprime `primer_divisor=3`. Si el `break` no estuviera, el bucle seguiría hasta `d = 16` y la salida sería basura: la corrección del programa depende del `break`, no sólo su eficiencia.

En **C** la estructura es un `for (; d <= n; d++)` con la inicialización vacía, porque `d` ya se declaró antes. El recorrido es el mismo —`15 % 2` da `1`, se ejecuta el incremento de la cláusula del `for` y `d` pasa a `3`; `15 % 3` da `0` y se ejecuta `break`—, pero conviene fijarse en la interacción entre `break` y la tercera cláusula del `for`: el `break` sale del bucle sin ejecutar `d++`, igual que en Python omite el `d += 1`. Esta es precisamente la diferencia con `continue`, que en C **sí** ejecuta la cláusula de incremento antes de volver a comprobar la condición, mientras que en el `while` de Python un `continue` colocado antes del `d += 1` se saltaría el incremento y colgaría el programa. `printf("primer_divisor=%ld\n", d)` imprime `primer_divisor=3`. Las implementaciones de **Java**, **C#**, **JavaScript**, **TypeScript** y **PHP** del README son literalmente el mismo `for` con `break`, señal de que esta construcción es patrimonio común de la familia de C.

El contraste lo aportan **Go** y **SQL**. Go escribe `for ; d <= n; d++ { if n%d == 0 { break } }`: es el mismo bucle, pero Go obliga a las llaves incluso para un `break` de una línea, y su `break` es además el que rompe el molde de C en otro punto —en un `switch`, Go sale por defecto de cada caso y necesita `fallthrough` explícito para encadenar, justo al revés que C, donde olvidar el `break` provoca el paso silencioso al caso siguiente. **SQL**, en cambio, no tiene `break` porque no tiene bucle: genera con `WITH RECURSIVE d(k)` la secuencia `2, 3, 4, …, 15`, filtra con `WHERE 15 % k = 0` las filas que son divisores —quedan `3`, `5` y `15`— y aplica `min(k)` para quedarse con `3`. Donde los lenguajes imperativos dicen "recorre y párate al encontrar", el declarativo dice "de todos los que cumplen, dame el menor", y deja que el motor decida si merece la pena parar antes. Ambos caminos producen `primer_divisor=3`, pero sólo uno de ellos expresa la parada como una instrucción.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `break` es igual en casi todos; C mantiene `goto` (evitar). |
| Semántica | break sale del bucle más interno; algunos lenguajes tienen break etiquetado. |
| Paradigmática | SQL evita el bucle: usa MIN sobre los divisores o una consulta. |

Los diez lenguajes del núcleo se ordenan según cuánto poder de salto conservaron. En el extremo permisivo está **C**, que mantiene el `goto` original con destino a cualquier etiqueta dentro de la misma función; **C#** lo conserva también (incluido el salto entre casos de un `switch`), **Go** lo incluye pese a su vocación minimalista, y **PHP** lo añadió tarde, en la versión 5.3, con restricciones fuertes: sólo dentro del mismo fichero y de la misma función, y sin poder saltar *hacia dentro* de un bucle. En la zona intermedia están los que renunciaron al `goto` pero conservaron etiquetas de bucle para resolver el problema real que lo justificaba —salir de varios bucles anidados a la vez—: **Java** y **JavaScript** admiten `break etiqueta` y `continue etiqueta` sobre un bloque nombrado, **TypeScript** hereda esa capacidad de JavaScript, y **Go** ofrece lo mismo para `for`, `switch` y `select`. **Rust** lleva la idea más lejos con etiquetas de vida propia: escribe `'outer: loop { ... break 'outer valor; }`, de modo que el `break` no sólo elige de qué bucle sale sino que además **devuelve un valor** que se convierte en el resultado de la expresión `loop` —una unificación entre salto y expresión que ningún otro del núcleo tiene—. En el extremo restrictivo está **Python**, que no tiene ni `goto` ni etiquetas: para salir de un anidamiento hay que extraer los bucles a una función y usar `return`, o llevar una bandera. A cambio, Python ofrece un mecanismo que casi ningún otro lenguaje tiene: el `else` de bucle, un bloque que se ejecuta sólo si el bucle terminó *sin* pasar por un `break`, pensado exactamente para el caso "buscar y, si no se encontró, hacer otra cosa". Y **SQL**, sin bucles ni saltos, queda fuera de la escala por construcción.

## 🧬 El concepto en la familia

En la familia de C —C, C++, Java, JavaScript, C#, PHP— el repertorio canónico es `break` + `continue` + `return`, con el `goto` presente en el lenguaje base y progresivamente cercado por las guías de estilo: C lo conserva entero, Java lo reservó como palabra clave pero nunca lo implementó, y PHP lo introdujo ya domesticado en 5.3. La familia del scripting dinámico se quedó con lo mínimo: Python y Ruby no tienen `goto` y Python tampoco etiquetas, apostando por que un anidamiento que necesita romperse desde dentro es un anidamiento que pedía ser una función. La familia ML y funcional resuelve el asunto sin construcciones de salto en absoluto: en Scheme, Haskell o Erlang la salida anticipada se expresa devolviendo el valor desde la rama correspondiente de una función recursiva, y la búsqueda con parada temprana emerge sola de la evaluación perezosa o del ajuste de patrones. Go y Rust representan el diseño moderno deliberado: ambos mantienen `break` y `continue` con etiquetas, ambos convierten el manejo de la salida de recursos en algo estructurado —`defer` en Go, RAII en Rust, igual que `finally` en Java, C# y Python—, y ambos corrigieron errores heredados de C, como el paso implícito entre casos del `switch`, que Go sustituyó por un `fallthrough` explícito. Los declarativos, finalmente, no participan del concepto: en SQL o Prolog no existe un punto del programa al que saltar, porque el orden de evaluación no lo fija el texto sino el motor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 070
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Seguir iterando tras encontrar** → causa: omitir el `break` no sólo desperdicia vueltas: en este programa deja `d` valiendo `n+1` al terminar el bucle, y la salida pasa a ser incorrecta, no meramente lenta → solución: salir en cuanto la condición de búsqueda se cumple, y comprobar con un caso donde el acierto llegue pronto (`12` debe dar `2`, no `13`).
- **`continue` que se salta el avance del contador** → causa: en un `while`, colocar `continue` antes del `d += 1` devuelve el control a la condición sin haber modificado el estado, y el bucle no termina nunca; el mismo `continue` en un `for` de C o Java sí ejecuta la cláusula de incremento, así que el error aparece sólo al traducir de un bucle a otro → solución: en bucles `while`, avanzar el contador antes de cualquier `continue`, o usar un `for` donde el incremento sea parte de la cabecera.
- **`break` que rompe el bucle equivocado** → causa: en dos bucles anidados, el `break` interior sólo abandona el bucle más interno y el exterior sigue girando, de modo que el programa parece "encontrar" varias veces o procesa datos que ya debían descartarse → solución: usar `break etiqueta` en Java, JavaScript o Go, `break 'outer` en Rust, y en Python extraer el anidamiento a una función para salir con `return`.
- **Olvidar el `break` en un `switch` de C** → causa: C, Java, JavaScript, C# y PHP encadenan al caso siguiente si no hay `break` explícito, y ese paso silencioso produce ejecuciones dobles difíciles de ver leyendo el código → solución: cerrar todos los casos y, cuando el encadenamiento sea intencional, marcarlo con un comentario; en Go el problema no existe porque cada caso sale por defecto y hay que pedir `fallthrough`.
- **Salir de una función sin liberar lo adquirido** → causa: un `return` temprano colocado después de abrir un fichero, tomar un cerrojo o reservar memoria se salta la liberación que estaba al final; es el motivo histórico de la regla *single entry, single exit* → solución: usar el mecanismo estructurado del lenguaje —`defer` en Go, `finally` en Java, C# y Python, `with`/RAII en Python y Rust— y, en C, donde no existe ninguno, el patrón `goto cleanup` con una única etiqueta de limpieza al final.

## ❓ Preguntas frecuentes

- **¿`break` sale de todos los bucles anidados?** No: sale únicamente del bucle que lo contiene de forma más inmediata. Para abandonar varios a la vez hacen falta etiquetas —`break etiqueta` en Java, JavaScript y Go, `break 'outer` en Rust— o, en lenguajes sin ellas como Python, extraer los bucles a una función propia y salir con `return`, que es casi siempre la reestructuración más legible.
- **¿Entonces el `goto` es realmente dañino?** El argumento de Dijkstra en 1968 sigue en pie para el `goto` como mecanismo general: destruye la correspondencia entre el texto del programa y su ejecución, y sin ella no se puede razonar con invariantes. Pero Knuth mostró en 1974 que la condena absoluta también produce código peor, lleno de banderas artificiales. El consenso actual es el que refleja esta clase: saltos con destino restringido y estructurado, sí; saltos arbitrarios, no.
- **¿Hay algún uso del `goto` que siga siendo legítimo?** Sí, y es el más citado: la limpieza de recursos en C, el patrón `goto cleanup` que emplea sistemáticamente el kernel de Linux. C carece de destructores, de `defer` y de `finally`, así que la alternativa a saltar a una etiqueta común de liberación es duplicar la limpieza en cada rama de error —más código, más ocasiones de olvidar algo—. En cuanto un lenguaje ofrece una construcción estructurada equivalente, la justificación desaparece.
- **¿Está mal tener varios `return` en una función?** La regla *single entry, single exit* venía de las guías de C y tenía una razón concreta: garantizar que la liberación de recursos al final se ejecutara siempre. Con `defer`, `finally` o RAII esa razón ya no existe, y hoy se prefiere el estilo de guardas: validar y salir pronto al principio, dejando el cuerpo principal sin anidar. Lo que sí conviene evitar es el `return` escondido en mitad de una función larga, que sorprende a quien lee.
- **¿Qué es el `else` de un bucle en Python?** Un bloque asociado a un `for` o un `while` que se ejecuta sólo si el bucle terminó de forma natural, es decir, **sin** haber pasado por un `break`. Está pensado exactamente para el patrón de búsqueda: el cuerpo hace `break` cuando encuentra, y el `else` contiene el "no se encontró". Es poco conocido y su nombre engaña —se entendería mejor como `nobreak`—, pero evita la bandera booleana que de otro modo haría falta.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). La obra que fijó el programa de la programación estructurada y explica por qué el salto arbitrario impide razonar sobre un programa con invariantes; el trasfondo directo del debate `goto` que ordena esta clase.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo, donde se clasifican `break`, `continue` y `return` como salidas restringidas y se compara qué lenguajes ofrecen etiquetas de bucle y cuáles conservan `goto`.

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

> [⏮️ Clase 069](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 071 ⏭️](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md)
