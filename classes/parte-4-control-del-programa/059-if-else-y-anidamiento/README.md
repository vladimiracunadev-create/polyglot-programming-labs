# Clase 059 — if / else y anidamiento

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La cadena `if` / `else if` / `else` es la forma en que un programa elige entre varias alternativas mutuamente excluyentes: dado un valor, decidir en cuál de N categorías cae y actuar en consecuencia. Es la construcción de selección más antigua y más usada de la programación, y el motivo de que exista en todo lenguaje es que la realidad rara vez es binaria: un `if` solo distingue "sí/no", pero clasificar una nota, un tramo de impuesto o un nivel de riesgo exige repartir un rango continuo en franjas ordenadas. Encadenar `else if` es exactamente eso: una escalera de umbrales donde la primera condición verdadera gana y las demás ni se prueban.

Aquí se aprende algo más sutil que la sintaxis: que la selección es la mitad estructurada de la programación estructurada. Dahl, Dijkstra y Hoare, en *Structured Programming*, redujeron todo el control de flujo a secuencia, selección e iteración; el `if/else if/else` es *la* selección, y dominar su orden, su exclusividad y su caso por defecto es dominar cómo un programa se ramifica sin caer en el `goto`. La intuición que se gana —que solo una rama se ejecuta, que el orden de los umbrales decide la corrección, y que el `else` final garantiza que ningún valor quede sin clasificar— sostiene toda decisión más compleja que verás después.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar if/else para varios rangos.
2. Ordenar los umbrales correctamente.
3. Cubrir el caso por defecto (else).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | if / else if / else | Elegir entre varias ramas |
| 2 | Rangos ordenados | De mayor a menor umbral |
| 3 | Caso por defecto | El else que recoge lo demás |
| 4 | Exclusividad | Solo una rama se ejecuta |

## 📖 Definiciones y características

- **if** — ejecuta un bloque si la condición es verdadera. Clave: la decisión básica.
- **else if** — condición alternativa si la anterior falló. Clave: encadena rangos.
- **else** — rama por defecto si ninguna condición se cumple. Clave: cubre el resto.
- **Umbral** — valor límite que separa dos categorías. Clave: su orden importa.

Estas piezas forman una máquina de decisión con dos propiedades que conviene hacer explícitas. La primera es la **exclusividad**: en una cadena `if / else if / else`, se evalúan las condiciones de arriba abajo y en cuanto una es verdadera se ejecuta su bloque y se abandona toda la cadena; las siguientes ni se prueban. Esto significa que un `else if score >= 80` presupone que `score >= 90` ya fue falso, y por eso la escalera debe ir de mayor a menor umbral. La segunda es la **totalidad**: el `else` final captura todo lo que ninguna condición atrapó, garantizando que no exista una entrada sin respuesta. Sebesta, en el capítulo de control de flujo de *Concepts of Programming Languages*, encuadra esto como *selección múltiple* y advierte de un peligro clásico del anidamiento: el **dangling else** ("else colgante"). En C, Java o JavaScript sin llaves, un `else` se asocia gramaticalmente al `if` más cercano, no al que la indentación sugiere, y ahí nace un bug silencioso. Como observan Dahl, Dijkstra y Hoare en *Structured Programming*, la fuerza de estas construcciones frente al `goto` está en que su estructura es evidente en el texto; el `dangling else` es precisamente el punto donde esa evidencia se rompe. Los lenguajes responden distinto: Python lo evita de raíz porque la indentación *es* la sintaxis, y Go va más lejos obligando las llaves siempre. La abstracción —"elige una de varias ramas ordenadas"— es idéntica en todos; la seguridad con que la escriben, no.

## 🧩 Situación

Considera un sistema de facturación que aplica descuentos por volumen: 20% a partir de 1000 unidades, 10% a partir de 500, 5% a partir de 100, y nada por debajo. Es una clasificación por tramos idéntica en forma a la de las notas. El bug clásico —y caro— aparece cuando alguien escribe la cadena de menor a mayor umbral: `if (u >= 100) desc = 0.05; else if (u >= 500) ...`. Como la exclusividad hace que gane la primera condición verdadera, *cualquier* pedido de 100 o más entra en la rama del 5% y las ramas del 10% y el 20% nunca se alcanzan. El programa compila, pasa una prueba con un pedido pequeño, y en producción cobra de menos a todos los clientes grandes durante semanas antes de que alguien note el agujero contable.

El orden de los umbrales no es una preferencia de estilo: es lo que separa una clasificación correcta de una silenciosamente rota. Y el `else` final tampoco es opcional: si lo omites, un valor que no encaja en ningún tramo deja la variable de descuento sin asignar —o con un valor viejo—, produciendo desde una excepción de "variable no inicializada" en Java hasta un descuento fantasma heredado de una iteración anterior. Estas dos disciplinas, orden descendente y caso por defecto explícito, son las que convierten una escalera de `else if` en una función total y confiable.

## 🧮 Modelo

- **Entrada** (stdin): un entero `score` (0-100)
- **Salida** (stdout): `nota=<A|B|C|F>`
- **Regla:** score>=90→A; >=80→B; >=70→C; si no→F

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `95` | `nota=A` |
| `72` | `nota=C` |
| `40` | `nota=F` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER score
SI score>=90: A
SINO SI score>=80: B
SINO SI score>=70: C
SINO: F
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

score = int(sys.stdin.readline())
if score >= 90:
    nota = "A"
elif score >= 80:
    nota = "B"
elif score >= 70:
    nota = "C"
else:
    nota = "F"
print(f"nota={nota}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const score = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const score: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota: string;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int score = Integer.parseInt(br.readLine().trim());
        String nota;
        if (score >= 90) nota = "A";
        else if (score >= 80) nota = "B";
        else if (score >= 70) nota = "C";
        else nota = "F";
        System.out.println("nota=" + nota);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int score = int.Parse(Console.In.ReadToEnd().Trim());
string nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
Console.WriteLine($"nota={nota}");
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
	score, _ := strconv.Atoi(strings.TrimSpace(line))
	var nota string
	if score >= 90 {
		nota = "A"
	} else if score >= 80 {
		nota = "B"
	} else if score >= 70 {
		nota = "C"
	} else {
		nota = "F"
	}
	fmt.Printf("nota=%s\n", nota)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let score: i64 = s.trim().parse().unwrap();
    let nota = if score >= 90 {
        "A"
    } else if score >= 80 {
        "B"
    } else if score >= 70 {
        "C"
    } else {
        "F"
    };
    println!("nota={nota}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long score;
    if (scanf("%ld", &score) != 1) return 1;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    printf("nota=%c\n", nota);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: rangos con CASE WHEN en orden descendente.
WITH scores(score) AS (VALUES (95), (72), (40))
SELECT printf('nota=%s',
       CASE WHEN score >= 90 THEN 'A'
            WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C'
            ELSE 'F' END) AS resultado
FROM scores;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$score = (int) trim(fgets(STDIN));
if ($score >= 90) {
    $nota = "A";
} elseif ($score >= 80) {
    $nota = "B";
} elseif ($score >= 70) {
    $nota = "C";
} else {
    $nota = "F";
}
echo "nota=$nota\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos `score = 72` por la implementación de **Python**. Tras leer el entero, la cadena empieza en `if score >= 90`: `72 >= 90` es falso, se salta. Pasa a `elif score >= 80`: `72 >= 80`, falso otra vez. Llega a `elif score >= 70`: `72 >= 70` es verdadero, así que `nota = "C"` y —por la exclusividad— el `else` final ni se considera. La última línea, `print(f"nota={nota}")`, produce `nota=C`, que es lo que `casos.json` espera. Nótese el detalle idiomático: Python usa la palabra `elif`, no `else if`, y la indentación delimita cada bloque, de modo que el "else colgante" es imposible. Con `score = 95`, la primera condición ya gana → `A`; con `score = 40`, las tres fallan y cae al `else` → `F`. La cadena descendente garantiza que cada valor toca exactamente una rama.

El contraste más rico es **Rust**, porque allí el `if` es una **expresión** que *devuelve* un valor. En vez de asignar `nota` dentro de cada rama, escribe `let nota = if score >= 90 { "A" } else if score >= 80 { "B" } else if score >= 70 { "C" } else { "F" };`: toda la cadena es una sola expresión cuyo valor —la cadena de la rama elegida— se liga a `nota`. Con `score = 72` la expresión evalúa a `"C"` y eso es lo que se asigna. Esto tiene una consecuencia de corrección que Python no ofrece: Rust *exige* el `else` final, porque una expresión debe producir un valor en todos los caminos; olvidar el caso por defecto no es un bug silencioso sino un error de compilación. Un tercer punto de vista, **C**, muestra el modelo de sentencia en su forma más cruda: `char nota;` se declara sin inicializar y cada rama le asigna un carácter (`nota = 'C';`). Aquí sí, omitir el `else` dejaría `nota` con basura de la pila, y escribir los `else if` sin llaves reabriría la puerta al dangling else que Python y Rust cierran por diseño. Finalmente **SQL** colapsa la escalera en un `CASE WHEN score >= 90 THEN 'A' ... ELSE 'F' END` evaluado en orden sobre cada fila de la tabla de casos: mismo resultado, misma dependencia crítica del orden descendente de los `WHEN`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `elif` (Python) vs. `else if` (C/Java/JS) vs. `else if` con llaves. |
| Semántica | Solo se ejecuta la primera rama verdadera; el orden descendente es clave. |
| Paradigmática | SQL usa CASE WHEN con los umbrales en orden. |

La diferencia sustancial entre los diez está en si el `if` es sentencia o expresión, y en cómo cada uno maneja el else colgante. Rust es el único del núcleo donde `if` es una expresión de pleno derecho: puede aparecer a la derecha de un `=`, y el compilador exige que todas las ramas devuelvan el mismo tipo y que exista el `else`. Python evita el dangling else por indentación significativa y ofrece `elif` como palabra propia. Go toma la decisión más estricta del grupo: **obliga** las llaves en todo `if`/`else`, de modo que el else colgante es sintácticamente imposible, aunque su `if` sigue siendo una sentencia. C, Java, JavaScript, C# y PHP permiten omitir las llaves en cuerpos de una línea, y ahí es donde el `else` se asocia al `if` más cercano y nacen bugs por indentación engañosa. TypeScript hereda ese riesgo de JavaScript pero añade análisis de exhaustividad en construcciones vecinas. Y SQL, declarativo, no anida `if` en absoluto: su `CASE WHEN` es una expresión —como el `if` de Rust— evaluada de arriba abajo, sin sentencias ni ramas colgantes que emparejar.

## 🧬 El concepto en la familia

En la familia dinámica, Ruby ofrece `if/elsif/else` pero prefiere para rangos un `case ... when 90..100` que es también una expresión con valor. En la familia funcional, la selección múltiple se expresa con *pattern matching* y guardas: Haskell escribe `| score >= 90 = "A" | score >= 80 = "B" ...`, y ML/OCaml usan `match ... with`, donde el compilador verifica la exhaustividad de los casos, la misma disciplina que Rust hereda. Kotlin y Scala convergen ahí con su `when`/`match` como expresión. En la familia lógica, Prolog ni siquiera tiene `if/else` central: define cláusulas alternativas y deja que la unificación y el backtracking elijan. La constante es la selección; lo que varía es si el lenguaje la trata como una escalera de sentencias o como una expresión total y verificada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 059
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comprobar los umbrales de menor a mayor** → causa: como la primera condición verdadera gana, un umbral bajo (`>= 70`) puesto primero captura también los valores altos, y las ramas superiores nunca se alcanzan → solución: ordenar siempre de mayor a menor umbral.
- **Olvidar el `else` final** → causa: algún valor no encaja en ninguna condición y la variable de resultado queda sin asignar o con un valor viejo → solución: incluir siempre un caso por defecto que cubra el resto (en Rust es obligatorio para un `if`-expresión).
- **Dangling else por omitir llaves** → causa: en C/Java/JS/C#/PHP, un `else` sin llaves se asocia al `if` más cercano, no al que la indentación sugiere → solución: usar llaves siempre, como obliga Go, o confiar en la indentación significativa de Python.
- **Solapar rangos con condiciones no excluyentes** → causa: escribir condiciones que se pisan (`if x > 10 ... else if x > 5 ...` con la intención de que sean disjuntas pero mal ordenadas) → solución: pensar cada `else if` como "y además la anterior fue falsa", y verificar que los tramos particionan el dominio.

## ❓ Preguntas frecuentes

- **¿Puedo usar `switch` aquí?** Para clasificar por *rangos* conviene `if/else if` o un `when`/`match` con rangos; el `switch`/`case` clásico compara contra valores exactos, no contra intervalos, así que encaja mal con umbrales.
- **¿Importa el orden de las ramas?** Muchísimo: la primera condición verdadera gana y corta la cadena, así que los umbrales deben ir de la condición más exigente a la más general. Reordenarlos cambia la clasificación.
- **¿El `if` de Rust y el `CASE` de SQL son lo mismo que un `if` normal?** En comportamiento sí, pero son *expresiones*: devuelven un valor asignable y exigen cubrir todos los casos, lo que convierte "olvidé el else" en un error de compilación en vez de un bug silencioso.
- **¿Cuándo el anidamiento sí está justificado?** Cuando las decisiones no son un solo eje de umbrales sino sub-decisiones dependientes (primero el tipo de cliente, y *dentro* de cada tipo un tramo distinto). Ahí el anidado modela una jerarquía real; para un único rango ordenado, la cadena plana es mejor.

## 🔗 Referencias

Para esta clase, lee en Sebesta el apartado de *selección* (sentencias de dos vías y de selección múltiple, incluida la discusión del *dangling else*) dentro del capítulo de control de flujo; en *Structured Programming*, apóyate en el argumento de que la selección estructurada sustituye con ventaja al `goto` porque su forma es evidente en el texto.

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

> [⏮️ Clase 058](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 060 ⏭️](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md)
