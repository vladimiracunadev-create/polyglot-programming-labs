# Clase 083 — Cierres (closures) y captura de variables

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender qué hace que una función pueda **recordar**. Un cierre (closure) es una función que, además de su código, se lleva consigo un pedazo del entorno donde nació: las variables que estaban a su alcance en el momento de la definición siguen vivas para ella aunque el bloque que las creó ya haya terminado. La fórmula que resume el concepto es célebre: un cierre es *función + entorno capturado*. Esa unión, que parece un detalle técnico, es la que permite fabricar funciones a medida en tiempo de ejecución, encapsular estado sin declarar una clase y escribir los `map`, `filter` y callbacks que sostienen la programación moderna.

La raíz de la idea está en el modelo de entornos de Abelson y Sussman (*Structure and Interpretation of Computer Programs*): cuando se evalúa una definición de función, no se guarda solo su cuerpo, sino un puntero al entorno vigente en ese instante. Al invocarla más tarde, sus variables libres —las que no son parámetros ni locales— se resuelven contra ese entorno capturado, no contra el del sitio desde donde se la llama. Marijn Haverbeke lo desarrolla en el capítulo 3 de *Eloquent JavaScript* con una imagen memorable: cada vez que una función se define, se crea una nueva instancia de su entorno local, de modo que una función que devuelve otra función deja tras de sí un entorno que la función devuelta seguirá viendo.

El objetivo profundo es distinguir dos preguntas que se confunden todo el tiempo: ¿el cierre captura el **valor** que la variable tenía, o captura la **variable** misma (su ligadura viva)? La respuesta cambia según el lenguaje y es el origen de los bugs de cierres más famosos —el del bucle `for` en JavaScript con `var`, el del `lambda` en un `for` de Python—. Dominar ese matiz es la diferencia entre usar cierres con confianza y ser sorprendido por ellos.

## 🧩 Situación

Necesitas construir varios «sumadores» configurables: uno que sume siempre 10, otro que sume 100, otro el impuesto del día. Sin cierres, tendrías que arrastrar ese `10` o ese `100` como un parámetro extra en cada llamada, o guardarlo en una variable global que cualquiera puede pisar. Con un cierre, `hacer_sumador(10)` te devuelve una función que ya *lleva incorporado* el 10: la llamas con `1` y da `11`, con `2` y da `12`, sin volver a mencionar el diez. El valor quedó capturado, privado y a salvo. Es el mismo patrón que hay detrás de un manejador de evento que «recuerda» sobre qué botón se registró, o de una función de ordenación que «recuerda» el criterio elegido por el usuario. El cierre resuelve el dolor de tener que pasar, una y otra vez, un dato que en realidad ya está decidido.

## 🧮 Modelo

- **Entrada** (stdin): un entero `base`
- **Salida** (stdout): `r1=<base+1> r2=<base+2>`
- **Regla:** sumar = λx. base + x ; r1 = sumar(1) ; r2 = sumar(2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `r1=11 r2=12` |
| `0` | `r1=1 r2=2` |
| `100` | `r1=101 r2=102` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER base
sumar <- hacer_sumador(base)   // captura base
ESCRIBIR "r1=" sumar(1) " r2=" sumar(2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def hacer_sumador(base):
    def sumar(x):
        return base + x
    return sumar


base = int(sys.stdin.readline())
sumar = hacer_sumador(base)
print(f"r1={sumar(1)} r2={sumar(2)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function hacerSumador(base) {
  return (x) => base + x;
}

const base = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function hacerSumador(base: number): (x: number) => number {
  return (x) => base + x;
}

const base: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    static IntUnaryOperator hacerSumador(int base) {
        return x -> base + x; // captura base (efectivamente final)
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int base = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator sumar = hacerSumador(base);
        System.out.println("r1=" + sumar.applyAsInt(1) + " r2=" + sumar.applyAsInt(2));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

Func<int, int> HacerSumador(int baseN) => x => baseN + x;

int b = int.Parse(Console.In.ReadToEnd().Trim());
var sumar = HacerSumador(b);
Console.WriteLine($"r1={sumar(1)} r2={sumar(2)}");
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

func hacerSumador(base int) func(int) int {
	return func(x int) int {
		return base + x
	}
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	base, _ := strconv.Atoi(strings.TrimSpace(line))
	sumar := hacerSumador(base)
	fmt.Printf("r1=%d r2=%d\n", sumar(1), sumar(2))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let base: i64 = s.trim().parse().unwrap();
    let sumar = |x: i64| base + x; // captura base
    println!("r1={} r2={}", sumar(1), sumar(2));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* C no tiene cierres: el estado (base) se pasa como parámetro. */
long sumar(long base, long x) {
    return base + x;
}

int main(void) {
    long base;
    if (scanf("%ld", &base) != 1) return 1;
    printf("r1=%ld r2=%ld\n", sumar(base, 1), sumar(base, 2));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene cierres: se parametriza con valores en la consulta.
WITH bases(base) AS (VALUES (10), (0), (100))
SELECT printf('r1=%d r2=%d', base + 1, base + 2) AS resultado FROM bases;
```

### PHP · `php main.php`

```php
<?php
function hacerSumador($base) {
    return fn($x) => $base + $x;
}

$base = (int) trim(fgets(STDIN));
$sumar = hacerSumador($base);
echo "r1=" . $sumar(1) . " r2=" . $sumar(2) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "10"`, `esperado = "r1=11 r2=12"`) por Python, C y Rust, tres lenguajes que representan tres puntos del espectro: cierre con captura viva, sin cierre en absoluto, y captura controlada por el sistema de tipos.

**Python — captura por referencia (late binding).** `base = int(sys.stdin.readline())` liga `base` a `10`. Al ejecutar `hacer_sumador(base)`, se entra en la función: se crea un entorno local donde `base` vale `10`, se define `sumar(x)` (que menciona `base` como variable libre) y se **devuelve** `sumar`. Aquí ocurre lo esencial: `sumar` no guardó el número `10`, sino un enlace al entorno donde vive `base`. Cuando fuera hacemos `sumar(1)`, el cuerpo `return base + x` busca `base` en ese entorno capturado, lo encuentra valiendo `10` y devuelve `11`; `sumar(2)` devuelve `12`. El f-string imprime `r1=11 r2=12`. Que Python capture la *variable* y no su valor es lo que produce la trampa clásica del `for`: si crearas varios cierres en un bucle que reusa la misma variable de control, todos verían su valor final, no el de cada iteración.

**C — sin cierres, el estado viaja como parámetro.** C no puede devolver «una función que recuerda `base`»: sus punteros a función no arrastran entorno. El comentario del código lo dice sin rodeos. La solución honesta es que `base` no se capture, sino que se **pase explícitamente** en cada llamada: `sumar(base, 1)` con `base=10` calcula `10 + 1 = 11`, y `sumar(base, 2)` da `12`. El resultado impreso es idéntico —`r1=11 r2=12`— pero el mecanismo es opuesto: donde Python oculta el `10` dentro del cierre, C lo mantiene visible y lo reenvía a mano. Comparar ambos deja claro qué *añade* un cierre: no un cálculo nuevo, sino la capacidad de no repetir el dato.

**Rust — captura con reglas de propiedad.** `let sumar = |x: i64| base + x;` crea un cierre que captura `base`. Como `i64` implementa `Copy` y el cierre solo lee `base`, Rust lo captura por referencia compartida sin conflictos; el cierre implementa el trait `Fn` (se puede llamar muchas veces sin consumir nada). `sumar(1)` da `11` y `sumar(2)` da `12`. Rust es el único del grupo donde el *modo* de captura —por referencia inmutable, mutable (`FnMut`) o por valor con `move` (`FnOnce` si consume)— es parte del contrato verificado por el compilador; si necesitaras que el cierre se llevara su propia copia de `base`, escribirías `move |x| base + x`. Los tres programas convergen en `r1=11 r2=12`, pero cada uno responde de forma distinta a la pregunta «¿de quién es `base` mientras el cierre vive?».

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El cierre se escribe `def`+`return` anidado (Python), flecha `=>` (JS/TS/C#), `x -> ...` (Java), `func(...) {...}` (Go), `\|x\| ...` (Rust) o `fn(...)` (PHP); C usa un puntero a función sin entorno. |
| Semántica | Python, JS y PHP capturan la **variable** (enlace vivo); por eso reflejan cambios posteriores y sufren el bug de late binding en bucles. Java exige que la variable capturada sea *final o efectivamente final*, lo que evita ese problema por diseño. |
| Semántica | Rust distingue tres traits de cierre —`Fn`, `FnMut`, `FnOnce`— y la palabra `move` fuerza captura por valor; el modo lo verifica el compilador, no queda al azar. |
| Semántica | Go capturaba la variable del bucle `for` por referencia (fuente histórica de bugs); desde Go 1.22 cada iteración tiene su propia variable, cambiando el comportamiento de cierres en bucles. |
| Paradigmática | C no tiene cierres: el estado se pasa como parámetro. SQL tampoco: se parametriza con valores dentro de la consulta (CTE `bases`). |

La síntesis vuelve a *SICP*: un procedimiento devuelto «se acuerda» de su entorno de definición porque literalmente guarda un puntero a él. Todos los lenguajes con cierres implementan esa misma idea; el eje que los separa es *qué* se captura (la variable viva o una copia) y *quién controla* ese modo (el programador con `move`, el compilador con la regla «efectivamente final», o nadie, dejándolo por referencia por defecto). C y SQL, al carecer del mecanismo, revelan por contraste qué problema resuelve exactamente un cierre.

## 🧬 El concepto en la familia

En **Ruby**, los bloques, `proc` y `lambda` capturan el entorno de forma natural; un bloque «ve» las variables locales del método que lo rodea. En **Swift**, los cierres capturan por referencia por defecto y ofrecen *capture lists* (`[valor]`) para capturar una copia, muy parecido al `move` de Rust. En **Haskell**, la aplicación parcial produce cierres sin esfuerzo: `(+) 10` *es* un sumador que recuerda el 10, porque toda función currificada que recibe menos argumentos de los que espera devuelve otra función con lo ya recibido capturado. En **C++**, las lambdas explicitan el modo en su lista de captura: `[base]` copia, `[&base]` toma referencia. El patrón a reconocer en cualquier lenguaje nuevo es siempre el mismo: dónde se declara el modo de captura y si por defecto es valor o referencia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 083
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **La trampa del bucle (late binding)** → causa: crear varios cierres en un `for` que capturan la variable de control por referencia; al ejecutarlos, todos ven su valor final → solución: en Python, fija el valor con un argumento por defecto (`lambda x, b=i: ...`); en JS usa `let` en vez de `var`; en Go ≥1.22 ya está resuelto por iteración.
- **Esperar cierres en C** → causa: intentar devolver una función que «recuerde» un dato; los punteros a función de C no llevan entorno → solución: pasa el estado como parámetro explícito, o agrúpalo en una `struct` que viaje junto al puntero.
- **Capturar por referencia cuando querías una copia** → causa: el cierre refleja cambios posteriores de la variable que no esperabas → solución: captura por valor —`move` en Rust, capture list en Swift/C++, argumento por defecto en Python— para congelar el estado en el instante de la definición.
- **Fugas de memoria por cierres que retienen mucho** → causa: un cierre de larga vida mantiene vivo todo su entorno capturado, incluidos objetos grandes → solución: captura solo lo que necesitas, no el objeto entero; en lenguajes con recolección esto evita retener memoria de más.

## ❓ Preguntas frecuentes

- **¿Cierre o clase?** Un cierre equivale a un objeto con un solo método y estado privado; muchas veces es más ligero y directo. Cuando necesitas varios métodos que compartan ese estado, una clase suele leerse mejor. Son dos formas del mismo principio: unir comportamiento con datos.
- **¿Qué captura, el valor o la variable?** Depende del lenguaje. Python, JS y PHP capturan la *variable* (enlace vivo, refleja cambios); Rust con `move` y Swift con capture list pueden capturar una *copia*. Saber cuál usa tu lenguaje es lo que evita las sorpresas.
- **¿Por qué Java exige que la variable sea «efectivamente final»?** Porque Java captura el valor en el momento de crear el cierre y prohíbe que cambie después; así elimina de raíz la ambigüedad entre capturar la variable o su valor, a costa de no poder mutar la variable capturada.
- **¿Un cierre y una lambda son lo mismo?** No exactamente. Una lambda es la *sintaxis* de una función anónima; se convierte en cierre cuando además *captura* algo de su entorno. Una lambda que no usa variables externas no necesita cerrar sobre nada.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §3.2 (procedimientos que capturan su entorno de definición).
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 7 «Funciones como objetos» y §sobre cierres.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. 3 «Functions» (cierres) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) (cap. 13, cierres `Fn`/`FnMut`/`FnOnce`).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 082](../../parte-5-funciones-y-modularidad/082-alcance-scope-y-sombreado-shadowing/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 084 ⏭️](../../parte-5-funciones-y-modularidad/084-funciones-puras-y-efectos-secundarios/README.md)
