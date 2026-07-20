# Clase 062 — Coincidencia de patrones: match / when

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La coincidencia de patrones da un salto conceptual respecto al `switch`. Donde el `switch` pregunta "¿este valor es igual a tal constante?", el `match` pregunta "¿este valor tiene tal *forma*?": si cae en un rango, si es un cero, si es una tupla con cierta estructura, si es un `Some(x)` que además cumple una condición. La decisión deja de basarse solo en la igualdad y pasa a basarse en la estructura del dato, lo que permite expresar en una sola construcción lo que antes exigía anidar `if`, desempaquetar y comparar por partes.

A ese poder expresivo se suma una garantía que el `switch` clásico nunca ofreció: la *exhaustividad*. En Rust, el compilador verifica que tus patrones cubran todos los valores posibles y rechaza el programa si dejas un caso fuera; en C# emite una advertencia. En esta clase clasificamos el signo de un entero —positivo, negativo o cero— porque es el ejemplo mínimo donde se ven las tres virtudes juntas: decidir por rango en vez de por igualdad, usar guardas dentro de los patrones y sentir la red de seguridad de la exhaustividad. El porqué de fondo es que un mecanismo de decisión debería ayudarte a no olvidar ninguna posibilidad, en vez de castigarte en tiempo de ejecución cuando la olvidas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar con match/when o su equivalente.
2. Usar guardas dentro de los patrones.
3. Explicar por qué el match exhaustivo es más seguro.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Coincidencia de patrones | Decidir por la forma del valor |
| 2 | Guardas en patrones | Condiciones dentro del caso |
| 3 | Exhaustividad | Cubrir todos los casos, obligatorio en Rust |
| 4 | match vs. switch | Más expresivo y sin caída |

## 📖 Definiciones y características

- **Coincidencia de patrones** — elegir una rama según la estructura o el rango de un valor. Clave: más potente que el switch.
- **Exhaustividad** — el compilador exige cubrir todos los casos (Rust). Clave: evita olvidos.
- **Guarda de patrón** — condición extra dentro de un caso (`n if n>0`). Clave: refina el patrón.
- **match** — construcción de coincidencia de patrones (Rust, Python 3.10+). Clave: sin fallthrough.

La coincidencia de patrones no nació en los lenguajes de sistemas, sino en la tradición funcional (ML, Haskell), y de allí la recogieron Rust, Scala, Swift y, en 2021, Python con el *structural pattern matching* de PEP 634. Sebesta, en el capítulo de estructuras de control de *Concepts of Programming Languages*, distingue la selección basada en igualdad —el `switch`— de la selección basada en la estructura del valor, y es esta segunda la que abre la puerta a *deconstruir* el dato en el mismo acto de decidir sobre él. La diferencia práctica es enorme: un `match` puede a la vez comprobar que un valor tiene cierta forma y ligar sus partes a variables nuevas, algo que con `switch` requeriría comprobar y luego desempaquetar por separado.

La otra idea clave es la exhaustividad, y aquí conviene enlazar con *Structured Programming* de Dahl, Dijkstra y Hoare: el argumento central de esa obra es que el programador debe poder razonar sobre la totalidad de los casos que un fragmento puede encontrar. La exhaustividad convierte ese ideal en una regla que el compilador hace cumplir. En Rust, si tu `match` no cubre alguna posibilidad, el programa no compila; el compilador te obliga a decidir explícitamente qué hacer con lo que olvidaste. Frente al `switch` de C, donde un valor no contemplado simplemente se escurre sin ejecutar nada, el `match` exhaustivo elimina de raíz toda una clase de errores por omisión. Las guardas (`n if n > 0`) refinan aún más cada rama con una condición booleana adicional, permitiendo que la decisión combine forma y predicado.

## 🧩 Situación

Imagina un intérprete que procesa nodos de un árbol de sintaxis, o un manejador que despacha mensajes de un protocolo: cada mensaje puede ser una de varias variantes, algunas con datos dentro, y hay que actuar según la variante *y* según lo que contiene. Ese es el terreno natural de la coincidencia de patrones. Cuando en el futuro alguien añada una nueva variante de mensaje, un `match` exhaustivo hará que el compilador señale, uno por uno, todos los puntos del código que olvidaron manejarla. En lugar de descubrir el hueco en producción, lo descubres al compilar.

Clasificar el signo de un entero es la versión mínima de ese patrón: tres formas posibles del valor —mayor que cero, menor que cero, exactamente cero— y una rama para cada una. En Rust, si escribes solo los casos positivo y negativo y olvidas el cero, el programa sencillamente no compila: la exhaustividad convierte un olvido silencioso en un error inmediato y localizado. El porqué de ingeniería es que las decisiones sobre datos con muchas formas son un foco crónico de bugs por casos no contemplados, y la coincidencia de patrones traslada ese riesgo del tiempo de ejecución al tiempo de compilación, donde es barato de arreglar.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `signo=<positivo|negativo|cero>`
- **Regla:** n>0→positivo; n<0→negativo; n==0→cero

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `signo=positivo` |
| `-3` | `signo=negativo` |
| `0` | `signo=cero` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
COINCIDIR n: (>0)->positivo ; (<0)->negativo ; (0)->cero
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
match n:
    case _ if n > 0:
        signo = "positivo"
    case _ if n < 0:
        signo = "negativo"
    case _:
        signo = "cero"
print(f"signo={signo}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo: string = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
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
        int n = Integer.parseInt(br.readLine().trim());
        String signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
        System.out.println("signo=" + signo);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string signo = n switch {
    > 0 => "positivo",
    < 0 => "negativo",
    _ => "cero",
};
Console.WriteLine($"signo={signo}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var signo string
	switch {
	case n > 0:
		signo = "positivo"
	case n < 0:
		signo = "negativo"
	default:
		signo = "cero"
	}
	fmt.Printf("signo=%s\n", signo)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let signo = match n {
        n if n > 0 => "positivo",
        n if n < 0 => "negativo",
        _ => "cero",
    };
    println!("signo={signo}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
    printf("signo=%s\n", signo);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: coincidencia por rango con CASE WHEN.
WITH nums(n) AS (VALUES (5), (-3), (0))
SELECT printf('signo=%s',
       CASE WHEN n > 0 THEN 'positivo' WHEN n < 0 THEN 'negativo' ELSE 'cero' END) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$signo = match (true) {
    $n > 0 => "positivo",
    $n < 0 => "negativo",
    default => "cero",
};
echo "signo=$signo\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Tomemos el caso `-3` de `casos.json`, cuya salida esperada es `signo=negativo`. En **Python**, `n = int(sys.stdin.readline())` convierte `"-3\n"` en el entero `-3` y entra al bloque `match n:`. Aquí el patrón usado es revelador: `case _ if n > 0:` significa "coincide con cualquier valor (`_`), pero solo si además la guarda `n > 0` es cierta". Con `n=-3`, el comodín coincide pero la guarda `n > 0` falla, así que Python descarta esa rama y prueba la siguiente, `case _ if n < 0:`; ahora la guarda `-3 < 0` es verdadera, se ejecuta `signo = "negativo"` y se detiene —no hay caída al `case _:` final. La salida es `signo=negativo`. Con el caso `0`, ambas guardas fallan y el control llega al `case _:` sin guarda, que actúa como caso por defecto exhaustivo y asigna `"cero"`.

El contraste más ilustrativo es **Rust**, donde la coincidencia de patrones es nativa y verificada. Tras `s.trim().parse()` obtiene `n: i64 = -3` y evalúa `match n { ... }` con las ramas `n if n > 0`, `n if n < 0` y `_`. Con `-3`, la primera guarda falla, la segunda (`-3 < 0`) acierta y `signo` queda ligado a `"negativo"`. Lo decisivo es lo que ocurre en tiempo de compilación: si el autor borrara la rama `_`, el compilador de Rust razonaría que las guardas no garantizan cubrir todos los enteros y rechazaría el programa con un error de patrón no exhaustivo. Esa rama `_` no está por adorno; es la que satisface al verificador de exhaustividad.

Un tercer enfoque aparece en **Go**, que no tiene `match` pero usa un `switch` sin expresión —`switch { case n > 0: ... }`— como cadena de condiciones booleanas. Con `n=-3`, `case n > 0` es falso, `case n < 0` es verdadero, asigna `"negativo"` y rompe automáticamente. Es funcionalmente equivalente para este problema, pero Go no comprueba exhaustividad: si faltara el `default`, el `signo` quedaría en su valor cero (`""`) sin ninguna queja. Las tres rutas convierten `-3` en `signo=negativo`, pero solo Rust promete atrapar el caso olvidado antes de ejecutar.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `match` con guardas (Rust/Python) vs. if/else (C/Java) que no tienen match nativo clásico. |
| Semántica | Rust exige exhaustividad; C/Java no avisan si falta un caso. |
| Paradigmática | SQL expresa la clasificación con CASE WHEN. |

Los diez lenguajes se reparten en tres grados de soporte. **Rust** tiene coincidencia de patrones nativa *con* verificación de exhaustividad obligatoria: es el único que rechaza compilar un caso olvidado. **Python** (desde 3.10) y **C#** tienen `match`/`switch`-expresión con patrones y guardas; C# incluso admite patrones de rango (`> 0`) y advierte —sin obligar— cuando faltan casos. **PHP** ofrece `match` como expresión sin caída, pero sin patrones estructurales: aquí se apoya en `match (true)` para simular la decisión por condición. El resto —**JavaScript**, **TypeScript**, **Java** (en su forma clásica), **C** y **Go**— carece de coincidencia de patrones para este problema y la emula: los tres primeros con el operador ternario encadenado, Go con un `switch` de condiciones. **SQL**, declarativo, usa `CASE WHEN condición`. La lección es que "clasificar por la forma del valor" existe en todos, pero solo unos pocos lo elevan a una construcción de primera clase que además te protege de los olvidos.

## 🧬 El concepto en la familia

La coincidencia de patrones es seña de identidad de la familia funcional: nació en ML y Haskell —donde `signo n | n > 0 = ...` usa guardas sobre ecuaciones— y de ahí pasó a Scala, F#, Rust y Swift, que la llevaron a los lenguajes de sistemas y de aplicación. Kotlin la aproxima con su expresión `when { n > 0 -> ... }`, y Python la incorporó tardíamente con PEP 634. La familia de C, en cambio, careció históricamente de ella y resolvía por igualdad o por cadenas de `if`. El rasgo común de todos los que sí la adoptaron es la vocación de cubrir cada caso explícitamente, en vez de dejar que un valor imprevisto se escape sin manejar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 062
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar un caso sin cubrir** → causa: un valor imprevisto no coincide con ninguna rama y el resultado queda indefinido o lanza una excepción en tiempo de ejecución → solución: en Rust el compilador te obliga a añadir el caso; en Python, C# o PHP incluye siempre una rama comodín (`_` / `default`) que actúe de red.
- **Confundir el comodín `_` con una variable** → causa: en Python `case _:` es el patrón atrapa-todo, pero `case x:` (un nombre libre) también captura *cualquier* valor y lo liga a `x`, por lo que una rama con nombre puesta demasiado pronto "se come" los casos siguientes → solución: colocar los patrones más específicos primero y reservar el comodín para el final.
- **Ordenar mal las guardas** → causa: como las ramas se prueban de arriba abajo y se toma la primera que coincide, una guarda demasiado amplia al principio hace inalcanzables a las de abajo → solución: ordenar de lo más restrictivo a lo más general y comprobar con un caso límite.
- **Usar `==` con reales para detectar 'cero'** → causa: la imprecisión del punto flotante hace que un cálculo que "debería dar cero" no lo dé exactamente → solución: en esta clase son enteros y la igualdad es exacta; con reales, comparar contra una tolerancia (`abs(x) < epsilon`) en vez de contra cero exacto.

## ❓ Preguntas frecuentes

- **¿`match` es solo de Rust?** No. Python 3.10+ tiene `match` con *structural pattern matching* (PEP 634), Kotlin tiene `when`, Scala y F# tienen `match`, Swift tiene su `switch` con patrones, y Haskell usa patrones y guardas. Rust destaca no por tenerlo, sino por hacer obligatoria la exhaustividad.
- **¿Por qué es más seguro que `switch`?** Por dos razones acumuladas: puede exigir que cubras todos los casos (exhaustividad), de modo que un olvido es un error de compilación y no un bug latente; y no tiene `fallthrough` accidental, porque cada rama es autónoma por diseño. El `switch` clásico no ofrece ninguna de las dos garantías.
- **¿Qué diferencia hay entre una guarda y un patrón?** El patrón decide por la *forma* del valor (es un `Some(x)`, es una tupla `(a, b)`, cae en el rango `1..=9`); la guarda es una condición booleana *extra* que se evalúa solo si el patrón ya coincidió (`n if n > 0`). Juntos permiten decisiones que combinan estructura y predicado en una sola rama.
- **¿El `match (true)` de PHP es coincidencia de patrones real?** No en sentido estricto: es un truco idiomático. Como PHP no tiene patrones estructurales, se hace `match (true)` y cada rama es una condición booleana que se compara contra `true`; se comporta como una cadena de `if`, pero conserva la ventaja de ser una expresión sin caída.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su insistencia en razonar sobre todos los casos posibles es la raíz intelectual de la exhaustividad que aquí exige el compilador.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. sobre estructuras de control, donde se contrasta la selección por igualdad con la selección por la estructura del valor. Complementa con el *structural pattern matching* de PEP 634 (Python) y *The Rust Programming Language*, cap. 6 y 18, sobre `match` y patrones.

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

> [⏮️ Clase 061](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 063 ⏭️](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md)
