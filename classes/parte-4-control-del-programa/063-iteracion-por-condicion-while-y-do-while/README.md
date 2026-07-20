# Clase 063 — Iteración por condición: while y do-while

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El `while` es el bucle en su forma más pura: repite un bloque mientras una condición siga siendo verdadera, y nada más. Es más fundamental que el `for` porque no presupone un contador ni un número conocido de vueltas; sirve igual para sumar de 1 a n que para leer líneas hasta el fin del archivo o esperar a que un recurso esté listo. De hecho, cualquier `for` puede reescribirse como un `while`, pero no al revés sin esfuerzo: por eso se dice que el `while` es el bucle sobre el que se construyen los demás.

En esta clase sumamos los enteros de 1 a n para ver de cerca las tres piezas que todo bucle por condición debe orquestar a mano: la *inicialización* del estado (el acumulador y el contador), la *condición de parada* que decide cuándo terminar, y el *avance* que en cada vuelta acerca el estado a esa condición. También distinguimos el `while` (bucle *pre-test*, que comprueba antes de la primera vuelta y puede no ejecutarse nunca) del `do-while` (bucle *post-test*, que ejecuta al menos una vez antes de comprobar). El porqué de fondo es que controlar la repetición con una condición explícita es a la vez el mecanismo más flexible y el más propenso al error clásico de todos: el bucle infinito, cuando el estado nunca alcanza la condición de parada.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle while con una condición de parada.
2. Actualizar el estado en cada vuelta.
3. Evitar el bucle infinito.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | while | Repetir mientras se cumpla una condición |
| 2 | Condición de parada | Cuándo termina el bucle |
| 3 | Acumulador | Sumar en cada vuelta |
| 4 | Bucle infinito | El peligro de no avanzar |

## 📖 Definiciones y características

- **while** — bucle que repite mientras la condición sea verdadera. Clave: comprueba antes de cada vuelta.
- **do-while** — variante que ejecuta al menos una vez (comprueba al final). Clave: no en todos los lenguajes.
- **Condición de parada** — lo que hace terminar el bucle. Clave: algo debe acercarse a ella.
- **Acumulador** — variable que reúne el resultado. Clave: se actualiza cada vuelta.

Sebesta, en el capítulo de estructuras de control de *Concepts of Programming Languages*, agrupa `while` y `do-while` bajo los *bucles controlados lógicamente* (por una condición booleana) y los opone a los bucles controlados por contador; la única diferencia entre ambos es *dónde* se evalúa la condición: al principio (pre-test) o al final (post-test). Esa distinción, aparentemente menor, decide si el cuerpo puede ejecutarse cero veces o al menos una. El `do-while` existe en C, Java, JavaScript, C# y PHP; Python y Go carecen de él y lo emulan con un `while True:` más `break`, o con el `for {}` sin condición de Go.

La razón por la que esta clase se ancla en el `while` va al corazón de *Structured Programming*, de Dahl, Dijkstra y Hoare. Uno de sus argumentos capitales es que un bucle es correcto cuando se puede exhibir un *invariante* —una propiedad que se mantiene verdadera antes y después de cada vuelta— y una *función de cota* que decrece hasta garantizar la terminación. En nuestra suma, el invariante es "`suma` contiene la suma de `1..i-1`" y la cota es "`n - i` decrece en cada vuelta hasta llegar a cero". Pensar el bucle en esos términos no es un lujo académico: es la disciplina que separa un bucle que termina con el resultado correcto de uno que se cuelga o que produce un valor con un error de límite. El bucle infinito, el error más clásico de esta construcción, no es más que un bucle cuya función de cota no decrece.

## 🧩 Situación

El `while` es el bucle de las situaciones donde no sabes de antemano cuántas vueltas darás: leer de un socket hasta que llegue el fin de la transmisión, reintentar una operación hasta que tenga éxito o se agoten los intentos, consumir eventos de una cola mientras queden. En todos ellos, el número de iteraciones lo dicta el estado en tiempo de ejecución, no una cuenta fijada de antemano, y por eso el `for` clásico encaja mal y el `while` encaja natural.

Sumar 1..n es la versión didáctica de ese patrón: aunque aquí el número de vueltas sí se conoce, resolverlo con `while` obliga a manejar el contador y la condición a mano, y expone así todo el aparato que un bucle por condición pone en tus manos. Ahí está el porqué de ingeniería: cada una de las tres piezas —inicializar, comprobar, avanzar— es una oportunidad de error. Si el contador no avanza, el bucle no termina y el proceso consume CPU indefinidamente; si la condición está mal puesta, sumas una vuelta de más o de menos. Un servidor con un `while` cuya condición nunca se vuelve falsa no da un resultado incorrecto: se cuelga, y ese es uno de los fallos más caros de diagnosticar en producción.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `1` | `suma=1` |
| `10` | `suma=55` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
suma <- 0 ; i <- 1
MIENTRAS i <= n: suma <- suma+i ; i <- i+1
ESCRIBIR "suma=" suma
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
suma = 0
i = 1
while i <= n:
    suma += i
    i += 1
print(f"suma={suma}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
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
        long suma = 0;
        int i = 1;
        while (i <= n) {
            suma += i;
            i++;
        }
        System.out.println("suma=" + suma);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
int i = 1;
while (i <= n) {
    suma += i;
    i++;
}
Console.WriteLine($"suma={suma}");
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
	suma := 0
	i := 1
	for i <= n {
		suma += i
		i++
	}
	fmt.Printf("suma=%d\n", suma)
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
    let mut suma = 0i64;
    let mut i = 1i64;
    while i <= n {
        suma += i;
        i += 1;
    }
    println!("suma={suma}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    long i = 1;
    while (i <= n) {
        suma += i;
        i++;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: suma 1..n con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 10
)
SELECT printf('suma=%d', sum(i)) AS resultado FROM seq;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
$i = 1;
while ($i <= $n) {
    $suma += $i;
    $i++;
}
echo "suma=$suma\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `5` de `casos.json`, cuya salida esperada es `suma=15`. En **Python**, `n = int(sys.stdin.readline())` fija `n = 5`, y a continuación se inicializa el estado: `suma = 0` e `i = 1`. Entra entonces el `while i <= n:`. Antes de la primera vuelta comprueba `1 <= 5` (verdadero), ejecuta `suma += i` (ahora `suma = 1`) e `i += 1` (ahora `i = 2`). El bucle vuelve a comprobar: con `i=2`, `suma` pasa a `3`; con `i=3`, a `6`; con `i=4`, a `10`; con `i=5`, a `15`. Tras esa vuelta `i` vale `6`, la condición `6 <= 5` es falsa y el bucle termina. Se imprime `suma=15`. Nótese que la comprobación ocurre *antes* de cada vuelta: si la entrada fuera un hipotético `n=0`, `1 <= 0` sería falso desde el inicio y el cuerpo no se ejecutaría ni una vez, dejando `suma=0` —esa es la esencia del bucle pre-test.

El recorrido en **C** es idéntico en estructura: `scanf` lee `5`, se inicializan `suma` e `i`, y el `while (i <= n)` repite la misma progresión `1, 3, 6, 10, 15`, incrementando `i` con `i++`. La única diferencia visible es el tipo: `suma` es `long`, previendo que la suma pueda desbordar un entero más pequeño cuando `n` es grande. La condición se evalúa arriba, igual que en Python.

El contraste interesante lo da **Go**, porque *no tiene la palabra `while`*. Su bucle es `for i <= n { ... }`: el mismo `for` de Go, pero con solo la condición y sin las cláusulas de inicialización e incremento. Semánticamente es un `while` exacto —comprueba `i <= n` antes de cada vuelta y recorre `1, 3, 6, 10, 15`— pero Go unificó ambos conceptos en una sola palabra clave. Las tres versiones transforman el `5` de entrada en el mismo `suma=15` orquestando a mano inicialización, condición y avance; lo que cambia es solo el vocabulario con que cada lenguaje nombra el bucle por condición.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `while cond:` (Python) vs. `while (cond) {}` (C/Java/JS). |
| Semántica | El while comprueba antes; el do-while (C/Java/JS) al menos una vez. |
| Paradigmática | SQL evita el bucle: suma con un CTE recursivo o una fórmula. |

Entre los diez lenguajes hay un reparto revelador en torno a una sola pregunta: cuántas formas de bucle por condición ofrece cada uno. **C**, **Java**, **JavaScript**, **TypeScript**, **C#** y **PHP** tienen tanto `while` (pre-test) como `do-while` (post-test), las dos variantes completas. **Python** y **Rust** tienen `while` pero no `do-while`: cuando hace falta "al menos una vez", Python usa `while True:` con un `break` al final, y Rust dispone además de `loop` (bucle infinito explícito) y de `while let` para iterar mientras un patrón coincida. **Go** es el caso extremo: eliminó las palabras `while` y `do-while` y las subsume todas en su único `for`, que con solo una condición actúa como `while` y sin condición como bucle infinito. **SQL**, fiel a su naturaleza declarativa, no itera: expresa la suma con un CTE recursivo o, mejor aún, con la fórmula cerrada `n(n+1)/2`. La misma necesidad —repetir mientras algo se cumpla— se cristaliza en un número distinto de construcciones según la filosofía de cada lenguaje.

## 🧬 El concepto en la familia

En la familia de C —C, C++, Java, JavaScript, C#, PHP— coexisten `while` y `do-while` como pareja canónica, herencia directa de la sintaxis original de C. La familia de lenguajes que buscó minimalismo redujo ese repertorio: Python y Ruby (`while i <= n`) prescinden del `do-while`, y Go lo lleva al límite colapsando todo en `for i <= n`. Rust añade matices propios de su estirpe: junto a `while` ofrece `loop` para el bucle infinito intencional y `while let` para iterar guiado por patrones. Bajo toda esa diversidad late un único concepto —repetir mientras una condición sea verdadera—, y las diferencias son de vocabulario y de cuántas variantes cada familia consideró que valía la pena nombrar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 063
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No avanzar el estado hacia la parada** → causa: olvidar el `i += 1` (o modificar la variable equivocada) hace que la condición nunca se vuelva falsa y el bucle se ejecute para siempre, consumiendo CPU → solución: garantizar que cada vuelta acerca el estado a la condición de parada; en términos de *Structured Programming*, que la función de cota decrezca de verdad.
- **Condición mal puesta (off-by-one)** → causa: usar `<` donde tocaba `<=` (o al revés) suma una vuelta de más o de menos → solución: verificar los límites con un caso pequeño y comprobable; aquí, que `n=1` dé `suma=1` y no `0` ni `3`.
- **Inicializar mal el acumulador** → causa: arrancar `suma` en un valor distinto de `0` (el neutro de la suma) corrompe el resultado desde la primera vuelta → solución: inicializar el acumulador con el elemento neutro de la operación (`0` para sumar, `1` para multiplicar).
- **Modificar la condición dentro del cuerpo por accidente** → causa: reasignar `n` o `i` en medio del cuerpo cambia la cota bajo los pies del bucle y produce vueltas de más o de menos → solución: no tocar las variables de control salvo en el punto previsto de avance.

## ❓ Preguntas frecuentes

- **¿`while` o `for`?** El `for` es más compacto y seguro cuando el número de vueltas se conoce de antemano, porque reúne inicialización, condición y avance en una línea. El `while` es preferible cuando el número de vueltas depende de una condición que solo se conoce en tiempo de ejecución (leer hasta fin de archivo, reintentar hasta éxito). No es una cuestión de gusto: cada uno expresa mejor una intención distinta.
- **¿Cuál es la diferencia real entre `while` y `do-while`?** El `while` comprueba la condición *antes* de la primera vuelta, así que puede ejecutar el cuerpo cero veces. El `do-while` comprueba *después*, de modo que siempre ejecuta el cuerpo al menos una vez. Usa `do-while` cuando la acción debe ocurrir sí o sí una vez antes de poder decidir si repetir (por ejemplo, pedir una entrada al usuario y validarla).
- **¿Go no tiene `while`?** No como palabra reservada. Go usa `for` con una sola condición —`for i <= n {}`— que es semánticamente idéntico a un `while`, y `for {}` sin condición para un bucle infinito. Es una decisión de diseño: un único bucle que cubre todos los usos.
- **¿Cómo evito de raíz un bucle infinito?** Antes de escribirlo, identifica la función de cota: la cantidad que debe decrecer en cada vuelta hasta forzar la parada. Si no puedes nombrarla, probablemente el bucle no termina. En la suma es `n - i`, que baja de `n-1` hasta `-1` y garantiza la salida.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su tratamiento de los invariantes y las funciones de cota es la base para razonar sobre la corrección y la terminación de un `while`.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. sobre estructuras de control, sección de *bucles controlados lógicamente*, que distingue el pre-test (`while`) del post-test (`do-while`).

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

> [⏮️ Clase 062](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 064 ⏭️](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md)
