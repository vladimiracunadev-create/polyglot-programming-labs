# Clase 060 — Expresiones condicionales: ternario e if como expresión

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Muchas veces no queremos *ejecutar* una de dos acciones, sino *elegir* uno de dos valores: el mayor de dos números, el texto "sí" o "no", una tarifa según sea festivo o no. Para eso existe la **expresión condicional** —el operador ternario `cond ? a : b`, o el `if` que en algunos lenguajes devuelve un valor—, que resuelve la elección dentro de una expresión y permite asignarla directamente: `max = a > b ? a : b`. Dice en una línea lo que un `if/else` de sentencia diría en cuatro, y —más importante— deja claro que el propósito es *producir un valor*, no ramificar el flujo.

Detrás de esto hay una distinción conceptual central en el diseño de lenguajes, que Sebesta trata con cuidado en *Concepts of Programming Languages*: **expresión vs. sentencia**. Una expresión se evalúa a un valor y puede aparecer donde se espera un valor (a la derecha de un `=`, como argumento); una sentencia ejecuta una acción y no necesariamente produce nada. El ternario es la versión-expresión de la selección. Algunos lenguajes van más lejos y hacen que el propio `if` sea una expresión —Rust, Kotlin—, con lo que el operador ternario se vuelve innecesario. Entender esta clase es entender por qué Rust no tiene `?:` (no le hace falta) y por qué Go, deliberadamente, tampoco lo tiene (una decisión de diseño sobre legibilidad, no una carencia).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Elegir un valor con el operador ternario.
2. Distinguir if-sentencia de if-expresión.
3. Escribir código conciso sin perder claridad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ternario ?: | Elegir un valor en una expresión |
| 2 | if como expresión | En Rust/Kotlin el if devuelve valor |
| 3 | Expresión vs. sentencia | Producir un valor vs. ejecutar una acción |
| 4 | Concisión | Una línea en vez de cuatro |

## 📖 Definiciones y características

- **Operador ternario** — `cond ? a : b`: elige a o b según la condición. Clave: expresión, no sentencia.
- **Expresión** — código que produce un valor. Clave: se puede asignar.
- **Sentencia** — código que ejecuta una acción. Clave: no siempre produce valor.
- **if-expresión** — un if que devuelve un valor (Rust, Kotlin). Clave: no necesita ternario aparte.

El hilo que une estas definiciones es la vieja frontera **expresión/sentencia**, que Sebesta señala como una de las decisiones de diseño más determinantes de un lenguaje. Un lenguaje "orientado a expresiones" (Rust, Kotlin, la familia funcional) hace que casi todo devuelva un valor, y entonces la selección no necesita dos formas distintas: el mismo `if` sirve para ramificar y para elegir un valor, porque *es* una expresión. Un lenguaje "orientado a sentencias" (C, Java, Go) separa ambos mundos: el `if` es una sentencia que no produce valor, así que para elegir un valor en una expresión hace falta una construcción aparte —el operador ternario `?:`, heredado de C—. Por eso Rust no incluye `?:`: sería redundante con su `if`-expresión. Y por eso Go, que *podría* haberlo incluido, lo omitió a propósito: sus autores juzgaron que el ternario anidado degrada la legibilidad y que forzar un `if` explícito, sumado al formateo canónico de `gofmt`, produce código más uniforme y auditable. Como resume la tradición estructurada de Dahl, Dijkstra y Hoare en *Structured Programming*, el valor de una construcción no está solo en lo que permite expresar, sino en lo difícil que hace expresar algo confuso; la decisión de Go es esa filosofía aplicada. La misma tarea —elegir un valor según una condición— se encarna, pues, como operador ternario, como `if`-expresión, o se prohíbe deliberadamente en favor del `if`-sentencia, según qué valore cada lenguaje.

## 🧩 Situación

En el renderizado de una interfaz, expresiones condicionales aparecen a docenas: `clase = activo ? "boton-on" : "boton-off"`, `etiqueta = cantidad === 1 ? "artículo" : "artículos"`, `precio = esSocio ? base * 0.9 : base`. Cada una elige un valor y lo asigna, y expresarlas como sentencia `if/else` de cuatro líneas cada una inflaría el código y separaría la variable de su cálculo. El ternario mantiene la elección junto a su uso, legible como una frase: *si esto, aquel valor; si no, este otro*. Bien empleado, comunica intención con más claridad que su equivalente en sentencias, porque hace visible que el resultado es un valor, no un efecto.

El peligro está en el abuso, y es real: anidar ternarios —`a ? b : c ? d : e ? f : g`— produce una expresión que hay que descifrar contando los `?` y los `:`, y ahí el remedio empeora la enfermedad. Es exactamente el escenario que llevó a los diseñadores de Go a excluir el operador del lenguaje. La regla práctica que decide corrección legible frente a acertijo es simple: el ternario brilla para una elección binaria simple; en cuanto aparece una segunda condición encadenada, un `if/else` o un `match` con ramas nombradas recupera la claridad que el anidamiento destruye.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max = (a > b) ? a : b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
max <- SI a > b ENTONCES a SINO b
ESCRIBIR "max=" max
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
mx = a if a > b else b
print(f"max={mx}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx = a > b ? a : b;
console.log(`max=${mx}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx: number = a > b ? a : b;
console.log(`max=${mx}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        int mx = a > b ? a : b;
        System.out.println("max=" + mx);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
int mx = a > b ? a : b;
Console.WriteLine($"max={mx}");
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
	b, _ := strconv.Atoi(f[1])
	mx := b
	if a > b {
		mx = a
	}
	fmt.Printf("max=%d\n", mx)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mx = if v[0] > v[1] { v[0] } else { v[1] };
    println!("max={mx}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long mx = a > b ? a : b;
    printf("max=%ld\n", mx);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la función max() elige el mayor directamente.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado
FROM pares;
```

### PHP · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$mx = $a > $b ? $a : $b;
echo "max=$mx\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Tomemos el caso `3 7`, cuya salida esperada es `max=7`, y sigámoslo por tres implementaciones que encarnan las tres filosofías. En **Python**, `a, b = map(int, sys.stdin.readline().split())` liga `a = 3` y `b = 7`. Luego `mx = a if a > b else b` es la expresión condicional de Python, con un orden peculiar: el valor-si-verdadero va *primero*, la condición *en medio*, y el valor-si-falso al final. Se evalúa `a > b`, es decir `3 > 7`, que es `False`; como la condición es falsa, la expresión toma la rama `else` y devuelve `b`, o sea `7`. Se imprime `max=7`. Este orden invertido respecto al `?:` de C es la fuente de errores más común al saltar entre lenguajes: en Python la condición no encabeza la expresión.

**Rust** resuelve lo mismo con su `if`-expresión: `let mx = if v[0] > v[1] { v[0] } else { v[1] };`. Aquí no hay operador ternario en absoluto porque no hace falta —el `if` ya devuelve un valor—. Con `3 7`, `v[0] > v[1]` es `3 > 7`, falso, así que la expresión evalúa la rama `else`, que vale `v[1] = 7`, y ese valor se liga a `mx`. Es la misma construcción que usarías para ramificar, reutilizada para producir un valor; de ahí que Rust considere el ternario redundante. El contraste más revelador es **Go**, que *deliberadamente* no tiene ni ternario ni `if`-expresión. Su código escribe `mx := b` y luego `if a > b { mx = a }`: inicializa el resultado con un valor por defecto (`b = 7`) y solo lo *muta* si la condición se cumple. Con `3 7`, `a > b` es falso, la asignación dentro del `if` nunca ocurre, y `mx` conserva el `7` inicial. Tres caminos —expresión de orden invertido en Python, `if`-expresión en Rust, mutación condicional en Go— llegan al mismo `max=7`. Y un cuarto, **SQL**, ni siquiera ramifica: usa la función `max(a, b)`, que para la fila `(3, 7)` devuelve `7` directamente, recordándonos que "elegir el mayor" puede ser una operación primitiva, no una decisión que el programador deba escribir.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a if a>b else b` (Python) vs. `a>b ? a : b` (C/Java/JS) vs. `if a>b {a} else {b}` (Rust). |
| Semántica | Python invierte el orden; Rust/Kotlin no tienen ternario porque el if ya es expresión. |
| Paradigmática | SQL usa `CASE WHEN` o `max(a,b)` directamente. |

La verdadera línea divisoria entre los diez es filosófica, no sintáctica. C, Java, JavaScript, TypeScript, C# y PHP heredan el operador ternario `?:` de C, con la condición al frente. Python tiene expresión condicional pero con sintaxis propia y orden invertido (`a if cond else b`), una decisión de legibilidad de Guido van Rossum para que se lea como inglés. Rust no tiene `?:` porque su `if` ya es una expresión de pleno derecho, y añadir el operador sería redundante; Kotlin y Scala comparten esa postura. Go es el caso más interesante: *podría* tener ternario y lo omite adrede —los diseñadores argumentan que el `?:` anidado es fuente de código ilegible— forzando un `if`-sentencia y confiando en `gofmt` para uniformar el estilo. SQL, declarativo, no tiene ternario ni `if`; expresa la elección con `CASE WHEN` (que es una expresión) o delega en funciones como `max()`/`COALESCE()`. Así, la misma tarea reparte a los lenguajes en tres campos: los que dan un operador dedicado, los que hacen del `if` una expresión, y el que prohíbe ambos por principio.

## 🧬 El concepto en la familia

En la familia de scripting con raíz en C, Ruby escribe `a > b ? a : b`, aunque —como es orientado a expresiones— su `if` también devuelve valor y `if a > b then a else b end` es igual de válido. En la familia estáticamente tipada moderna, Kotlin y Scala eliminan el ternario y hacen del `if` una expresión, exactamente como Rust: `if (a > b) a else b`. En la familia funcional pura, la expresión condicional es la forma *natural* —Haskell y ML nunca tuvieron sentencias `if` que ejecutar, solo `if cond then a else b` que se evalúa a un valor— y a menudo se prefiere el `case`/`match` con patrones cuando hay más de dos ramas. Lisp lo expresa con `(if cond a b)` como forma que retorna valor, y con `cond` para cadenas. El patrón se repite: cuanto más orientado a expresiones es un lenguaje, menos necesita un operador ternario separado, porque su `if` ya hace el trabajo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 060
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar ternarios en exceso** → causa: encadenar `a ? b : c ? d : e` produce una expresión que se descifra contando `?` y `:`, ilegible → solución: usar `if/else` o `match`/`when` con ramas nombradas en cuanto haya más de una elección binaria.
- **Confundir el orden en Python** → causa: `a if cond else b` no es `cond ? a : b`; la condición va en el medio, no al frente → solución: leerlo como "el valor `a`, *si* `cond`, *si no* `b`" y no trasladar mecánicamente el orden de C.
- **Usar un ternario por su efecto secundario** → causa: intentar `cond ? hacerX() : hacerY()` para ejecutar acciones, cuando el ternario es para *elegir valores* → solución: si lo que quieres es ejecutar una de dos acciones, usa un `if/else` de sentencia; reserva el ternario para producir un valor.
- **Mezclar tipos incompatibles en las ramas** → causa: `cond ? 5 : "cinco"` obliga a un tipo común laxo o falla; en Rust/Kotlin no compila si las ramas no coinciden → solución: asegurar que ambas ramas producen el mismo tipo, que es lo que se va a asignar.

## ❓ Preguntas frecuentes

- **¿Rust no tiene `?:`?** No, y es a propósito: su `if` ya es una expresión que devuelve valor (`let x = if c { a } else { b }`), así que un operador ternario separado sería redundante.
- **¿Por qué Go no tiene ternario?** Es una decisión de diseño explícita: sus autores consideran que el `?:` anidado daña la legibilidad, y prefieren forzar un `if` explícito uniformado por `gofmt`. No es una carencia, es una postura.
- **¿El ternario es más rápido que un `if/else`?** No: compila a lo mismo. La diferencia es de concisión y de intención expresada (elegir un valor), no de rendimiento.
- **¿Cuándo NO debo usar un ternario?** Cuando hay más de dos ramas, cuando cada rama hace algo complejo, o cuando lo anidarías. En esos casos `if/else`, `match` o `when` comunican mejor y evitan el acertijo del anidamiento.

## 🔗 Referencias

Para esta clase, lee en Sebesta la distinción entre expresiones y sentencias y el apartado de expresiones condicionales dentro del capítulo de expresiones/control de flujo; ahí se ve por qué un lenguaje orientado a expresiones no necesita un operador ternario aparte, el hilo conceptual de toda la clase.

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 059](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 061 ⏭️](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md)
