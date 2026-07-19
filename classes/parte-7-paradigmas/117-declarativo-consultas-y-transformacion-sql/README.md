# Clase 117 — Declarativo: consultas y transformación (SQL)

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El paradigma **declarativo** invierte la pregunta con la que trabaja el programador imperativo. Este último responde a "¿qué pasos doy para obtener el resultado?"; el declarativo responde a "¿qué relación hay entre la entrada y el resultado que quiero?" y deja los pasos al sistema. Van Roy y Haridi, en *Concepts, Techniques, and Models of Computer Programming*, colocan la programación declarativa en el centro de su taxonomía precisamente por esta propiedad: un programa declarativo describe *qué* debe ser cierto, no *cómo* calcularlo, y esa separación es la que permite que un motor —un optimizador de consultas, un runtime funcional— elija la estrategia de ejecución sin cambiar el significado del programa.

SQL es el ejemplo más difundido y logrado de este estilo. Cuando escribes `SELECT SUM(x) FROM t WHERE x % 2 = 0`, no dices "recorre la tabla, comprueba cada fila, acumula en un total": declaras *la suma de las x pares* y el **optimizador** de la base de datos decide el plan de ejecución —si usa un índice, en qué orden lee, si paraleliza—. C. J. Date, en *SQL and Relational Theory*, insiste en que esta es la herencia directa del álgebra y el cálculo relacional de Codd: una consulta es una expresión sobre relaciones cuyo resultado está definido matemáticamente, con independencia del algoritmo que la máquina use para materializarlo.

El objetivo de hoy es sentir esa diferencia en carne propia con una tarea mínima: sumar los números pares de una lista. Verás que en SQL y en el estilo funcional de los demás lenguajes describes la operación como "filtra los pares, suma", mientras que el imperativo puro tendría que declarar una variable acumulador, recorrer con un bucle y sumar a mano. Misma respuesta, dos maneras opuestas de pensar: describir el resultado frente a dictar los pasos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Expresar un cálculo de forma declarativa.
2. Combinar filtro y agregación.
3. Contrastar con el estilo imperativo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarativo | Describir el resultado |
| 2 | Filtro + agregación | Seleccionar y combinar |
| 3 | SQL como declarativo | WHERE + SUM |

## 📖 Definiciones y características

- **Declarativo** — paradigma que describe el resultado deseado, no los pasos. Clave: el motor decide el cómo.
- **Filtro** — seleccionar los elementos que cumplen una condición. Clave: `WHERE`, `filter`.
- **Agregación** — combinar varios valores en uno (suma). Clave: `SUM`, `reduce`.

La virtud central de lo declarativo es la **independencia de datos y de estrategia** que Codd persiguió y que Date desarrolla en *SQL and Relational Theory*. Cuando declaras `WHERE x % 2 = 0` no comprometes a la máquina con ningún orden de recorrido; el optimizador es libre de leer la tabla como quiera, usar un índice si existe, o repartir el trabajo entre varios núcleos. Si mañana añades un índice sobre la columna, tu consulta no cambia ni una letra pero se ejecuta más rápido: el *qué* permanece, el *cómo* mejora por debajo. Esa es la razón de que las bases de datos hayan podido optimizarse durante cincuenta años sin que los programas que las consultan tengan que reescribirse.

Van Roy y Haridi señalan la otra cara de la moneda: el estilo declarativo brilla en **transformaciones de datos** —filtrar, proyectar, agregar, unir— porque en ese terreno la relación entre entrada y salida se expresa limpiamente como una expresión. Pero no es una bala de plata. Cuando el problema exige control fino del *cómo* —un algoritmo con un orden de operaciones deliberado, gestión explícita de recursos, un bucle con efectos cuidadosamente secuenciados— el imperativo recupera su ventaja. El buen ingeniero no elige un bando: reconoce que "sumar los pedidos pagados" pide una consulta declarativa, mientras que "reproducir un protocolo de red paso a paso" pide control imperativo.

Conviene además distinguir el **filtro** de la **agregación**, las dos operaciones que combinamos hoy. El filtro (`WHERE`, `filter`) es una operación que preserva la forma: de una colección saca una subcolección. La agregación (`SUM`, `reduce`) colapsa la colección en un único valor. Su composición —filtrar y luego agregar— es el patrón más común del análisis de datos, y en SQL se lee casi como una frase en inglés técnico: *the sum of x where x is even*.

## 🧩 Situación

Un equipo de finanzas necesita el total facturado del trimestre solo de los pedidos ya pagados. En un sistema imperativo alguien escribiría un método que abre la colección de pedidos, itera fila por fila, comprueba el estado de cada uno y va acumulando en una variable. Funciona, pero ese método fija el *cómo*: si la colección crece a millones de registros, hay que reescribirlo para paralelizar o para aprovechar un índice, y cada cambio arriesga romper la lógica.

En el mundo declarativo, el analista escribe `SELECT SUM(importe) FROM pedidos WHERE estado = 'pagado'` y termina. Ha descrito la relación entre los datos y el número que quiere; el motor decide el plan. "La suma de los pedidos pagados", "el total de las ventas del mes", "la media de edad de los clientes activos": todas son descripciones de un resultado, no recetas de cálculo. En esta clase reducimos ese patrón a su núcleo verificable —sumar los pares de una lista— para aislar el mecanismo de *filtro + agregación* que sostiene la mayoría de las consultas reales. El estilo se lee igual en SQL que en la versión funcional de los demás lenguajes: describe qué quieres, no cómo recorrerlo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma_pares=<suma de los pares>`
- **Regla:** suma de los x tales que x es par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma_pares=6` |
| `2 4 6` | `suma_pares=12` |
| `1 3 5` | `suma_pares=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma_pares <- SUMA(FILTRAR(par, lista))
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma_pares={sum(x for x in nums if x % 2 == 0)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const suma = nums.filter((x) => x % 2 === 0).reduce((a, b) => a + b, 0);
console.log(`suma_pares=${suma}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const suma = nums.filter((x) => x % 2 === 0).reduce((a, b) => a + b, 0);
console.log(`suma_pares=${suma}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long suma = Arrays.stream(p).mapToInt(Integer::parseInt).filter(x -> x % 2 == 0).sum();
        System.out.println("suma_pares=" + suma);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = p.Select(int.Parse).Where(x => x % 2 == 0).Sum(x => (long) x);
Console.WriteLine($"suma_pares={suma}");
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
	suma := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			suma += n
		}
	}
	fmt.Printf("suma_pares=%d\n", suma)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let suma: i64 = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .sum();
    println!("suma_pares={suma}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) suma += x;
    }
    printf("suma_pares=%ld\n", suma);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: WHERE + SUM, puro estilo declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma_pares=%d', COALESCE(sum(x), 0)) AS resultado FROM nums WHERE x % 2 = 0;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$suma = array_sum(array_filter($nums, fn($x) => $x % 2 === 0));
echo "suma_pares=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

El contrato de [`casos.json`](casos.json): `stdin` `1 2 3 4` → `suma_pares=6`, `2 4 6` → `suma_pares=12`, `1 3 5` → `suma_pares=0`. La regla es "suma de los x tales que x es par". Este ejercicio es ideal para ver el mismo cálculo escrito de forma declarativa y de forma imperativa lado a lado.

**SQL — el declarativo por excelencia.** El bloque marcado como ilustrativo es el corazón de la clase: `SELECT printf('suma_pares=%d', COALESCE(sum(x), 0)) AS resultado FROM nums WHERE x % 2 = 0;`. Léelo como una descripción, no como una secuencia de pasos. La cláusula `WHERE x % 2 = 0` **declara** el filtro —"solo las filas donde x es par"— sin decir en qué orden recorrer la tabla; `sum(x)` **declara** la agregación sobre las filas que sobrevivieron al filtro. Para la tabla `nums(x)` con `1, 2, 3, 4` el motor se queda con `2` y `4` y los suma: `6`. Repara en el `COALESCE(sum(x), 0)`: cuando ninguna fila pasa el filtro —el caso `1 3 5`— `sum` no devuelve `0` sino `NULL`, porque agregar sobre el conjunto vacío es indefinido en el modelo relacional; `COALESCE` traduce ese `NULL` al `0` que exige `casos.json`. Ese detalle es el punto declarativo más fino de la clase: la suma vacía debe rendir cuentas, y se resuelve describiendo el valor por defecto, no con un `if`.

**Python — declarativo dentro de un lenguaje imperativo.** La línea `print(f"suma_pares={sum(x for x in nums if x % 2 == 0)}")` demuestra que el estilo declarativo no es exclusivo de SQL. La expresión generadora `x for x in nums if x % 2 == 0` es el filtro (`if x % 2 == 0`) y `sum(...)` es la agregación. No hay acumulador ni bucle explícito con un `total += x`: describes "la suma de los x pares" y el intérprete se encarga. Para `1 2 3 4` produce `6`; para `1 3 5` el generador queda vacío y `sum` de lo vacío es `0` —Python sí devuelve `0`, a diferencia del `NULL` de SQL—, cuadrando con `casos.json` sin necesidad de `COALESCE`.

**C — el contraste imperativo.** Mira ahora la implementación en C para apreciar el otro polo. Aquí sí hay que dictar cada paso: `long suma = 0` declara el acumulador, `while (scanf("%ld", &x) == 1)` recorre la entrada elemento a elemento, `if (x % 2 == 0) suma += x` comprueba y acumula a mano. Produce el mismo `suma_pares=6`, pero el programador ha escrito el *cómo* completo: inicializar, iterar, condicionar, sumar. Comparar estas tres versiones —SQL que describe, Python que describe con azúcar funcional, C que dicta— es el objetivo de la clase: las tres satisfacen `casos.json`, pero solo las dos primeras dejan la estrategia de ejecución en manos del sistema.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `sum(x for x in l if x%2==0)` (Python), `filter+reduce` (JS), `WHERE+SUM` (SQL). |
| Semántica | Se describe el resultado; el cómo queda implícito. |
| Paradigmática | El imperativo recorrería y acumularía a mano. |

La comparación revela un espectro, no una frontera. En un extremo, C es puramente imperativo: no hay `filter` ni `sum` de biblioteca, así que el bucle `while` con acumulador es la forma idiomática. En el otro, SQL es puramente declarativo: no existe manera de escribir un bucle, solo describes la relación. En medio, los lenguajes multiparadigma —Python, JavaScript, TypeScript, Java, C#, Rust, PHP— ofrecen ambos registros y dejan elegir. Java lo hace con `Streams` (`Arrays.stream(p).filter(x -> x % 2 == 0).sum()`), C# con LINQ (`.Where(...).Sum(...)`), Rust con iteradores perezosos (`.filter(...).sum()`). La firma cambia, pero todas expresan el mismo *filtro + agregación* de manera declarativa, encadenando transformaciones en vez de escribir el recorrido.

Hay una diferencia semántica real que conviene no pasar por alto: **el tratamiento de la suma vacía**. La mayoría de los lenguajes definen la suma de una colección vacía como `0` (elemento neutro de la suma), y sus implementaciones lo obtienen gratis: `sum()` en Python, `.reduce((a, b) => a + b, 0)` en JS con su acumulador inicial explícito, `.sum()` en Rust. SQL, fiel al modelo relacional, hace que `SUM` sobre cero filas devuelva `NULL`, no `0`, porque en el álgebra relacional la ausencia de datos es distinta del cero. Por eso la implementación SQL necesita `COALESCE(sum(x), 0)` y las demás no. Es un ejemplo perfecto de cómo un mismo paradigma declarativo puede tener convenios distintos según su modelo teórico de base.

## 🧬 El concepto en la familia

En Haskell la expresión `sum (filter even xs)` es el filtro-agregación reducido a su esencia matemática: `filter even` selecciona los pares, `sum` los colapsa, y la composición se lee de derecha a izquierda como una función. SQL es el declarativo por excelencia en la industria, pero la familia declarativa es amplia: Datalog y Prolog (que ves en la clase siguiente) describen relaciones lógicas; las hojas de cálculo son declarativas —una celda declara su fórmula, no el orden de recálculo—; los sistemas de configuración como los manifiestos de infraestructura describen el estado deseado y dejan que un motor lo materialice. El denominador común, que Van Roy y Haridi subrayan, es que el programador describe *qué* debe ser cierto y cede el *cómo* a un motor de ejecución u optimización.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 117
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar el cómo con el qué** → causa: colar un bucle o un contador manual dentro de lo que debería ser una descripción, perdiendo la legibilidad declarativa y las oportunidades de optimización del motor. → remedio: expresa la operación como una cadena de filtro y agregación (`filter().sum()`, `WHERE ... SUM`) y deja que el sistema elija el recorrido.
- **Olvidar el caso de la colección vacía** → causa: asumir que agregar sobre cero elementos da error o `NULL`, cuando el resultado esperado es `0`. → remedio: la suma vacía es el elemento neutro `0`; en SQL protégete con `COALESCE(sum(x), 0)` porque su `SUM` de cero filas es `NULL`, mientras que en Python/JS/Rust el `0` sale por defecto.
- **Suponer un orden de evaluación en SQL** → causa: escribir consultas que dependen del orden en que el motor lee las filas, que es indefinido salvo que haya `ORDER BY`. → remedio: recuerda que declaras una relación, no un recorrido; si necesitas orden, decláralo explícitamente.

## ❓ Preguntas frecuentes

- **¿El estilo declarativo siempre es mejor?** No; es superior para *transformaciones de datos* —filtrar, agregar, unir, proyectar— porque ahí la relación entrada-salida se expresa limpiamente y el motor puede optimizar. Cuando el problema exige control fino del cómo (un algoritmo con orden deliberado, gestión explícita de recursos, efectos cuidadosamente secuenciados), el imperativo da un control que lo declarativo esconde a propósito. Van Roy y Haridi lo tratan como una elección de modelo, no como una jerarquía.
- **¿Por qué SQL es el ejemplo canónico de declarativo?** Porque separa por completo la descripción del resultado del algoritmo que lo produce: escribes `SELECT SUM(x) WHERE ...` y el optimizador —no tú— decide el plan de ejecución. Date lo enmarca en el álgebra relacional de Codd: la consulta es una expresión matemática sobre relaciones cuyo resultado está definido con independencia de cómo lo materialice la máquina.
- **¿Puedo escribir código declarativo en un lenguaje imperativo?** Sí, y es lo habitual hoy. La expresión generadora de Python, los `Streams` de Java, LINQ en C# y los iteradores de Rust permiten expresar filtro y agregación de forma declarativa dentro de un lenguaje que también soporta bucles. La versión Python de esta clase lo demuestra: `sum(x for x in nums if x % 2 == 0)` es declarativa aunque Python no sea un lenguaje declarativo.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press) — el modelo declarativo: describir el qué, no el cómo.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson) — paradigmas y evaluación de lenguajes.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly) — álgebra y cálculo relacional, tratamiento de agregaciones y `NULL`.
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 116](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 118 ⏭️](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md)
