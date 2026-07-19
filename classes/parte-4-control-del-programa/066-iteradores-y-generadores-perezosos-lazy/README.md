# Clase 066 — Iteradores y generadores perezosos (lazy)

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La evaluación **perezosa** (*lazy*) invierte una suposición tan arraigada que casi nunca se enuncia: que para trabajar con una secuencia hay que tenerla entera. Un generador perezoso no devuelve valores, devuelve *la promesa de saber calcular el siguiente*. Nada se computa hasta que alguien pide el primer elemento, y entonces se computa exactamente uno; el resto sigue sin existir. Frente a la evaluación **estricta**, que calcula la lista completa y la deja en memoria, la pereza cambia el consumo de O(n) a O(1) y hace posibles dos cosas que de otro modo son imposibles: procesar un archivo de 10 GB sin cargarlo —una línea viva a la vez— y trabajar con secuencias **infinitas**, como "todos los números pares", tomando de ellas solo los primeros n.

El mecanismo que lo hace posible es el **generador**: una función que, en lugar de `return`, usa `yield`. Llamarla no ejecuta ni una línea de su cuerpo; devuelve un objeto generador. Solo cuando se le pide el primer valor empieza a correr, y al llegar al `yield` se **suspende**: su marco de pila —variables locales y punto de ejecución— queda congelado, no destruido, esperando la siguiente petición para reanudarse justo donde se quedó. Esa capacidad de suspender y reanudar es la que convierte a una función normal en una corrutina, y es la misma maquinaria sobre la que después se construyen `async`/`await`. En esta clase generamos los primeros n números pares para ver la pereza en acción y, sobre todo, para medir su precio: un generador no se puede recorrer dos veces, no tiene longitud, difiere sus efectos secundarios a un momento imprevisible y es notablemente más difícil de depurar que una lista.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar una secuencia de longitud n.
2. Reconocer la evaluación perezosa (lazy).
3. Distinguir generar de tener ya calculado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Generar bajo demanda | Producir valores al pedirlos |
| 2 | Perezoso (lazy) | No calcular hasta que se necesita |
| 3 | Iterador | Objeto que entrega el siguiente valor |
| 4 | take n | Tomar solo los primeros n |

## 📖 Definiciones y características

- **Iterador** — objeto que produce valores uno a uno. Clave: no necesita toda la colección en memoria.
- **Generador** — función que produce una secuencia perezosa (yield). Clave: calcula al vuelo.
- **Evaluación perezosa** — calcular un valor solo cuando se pide. Clave: permite secuencias infinitas.
- **take** — tomar los primeros n de una secuencia. Clave: corta lo infinito.
- **Ejecución diferida** — el cálculo ocurre al consumir, no al declarar. Clave: el momento del efecto se desplaza.

Sebesta sitúa los generadores dentro de las *corrutinas*, la generalización del subprograma que Dahl, Dijkstra y Hoare ya discutían en *Structured Programming*: mientras una función tiene una entrada y una salida y muere al retornar, una corrutina tiene múltiples puntos de suspensión y reanudación y conserva su estado entre ellos. Eso es literalmente lo que hace `yield`. Ramalho lo explica en *Fluent Python* con una distinción que conviene fijar: `def f(): yield 1` no es una función que devuelve `1`, es una *fábrica de generadores*; llamarla no ejecuta nada y el cuerpo solo avanza —hasta el siguiente `yield`— cuando alguien invoca `next()`. Python ofrece además la expresión generadora, `(2 * i for i in ...)`, que es la misma pereza con sintaxis de comprensión y sin corchetes. JavaScript adoptó la idea con `function*` y un `yield` que devuelve el control al consumidor, y Haverbeke muestra en *Eloquent JavaScript* cómo un generador es la forma más corta de implementar el protocolo iterable sin escribir a mano el objeto con `next()`.

El resto de los lenguajes del núcleo llegaron a la pereza por caminos distintos. C# la tiene desde muy pronto con `yield return` dentro de un método que declara devolver `IEnumerable<T>`: el compilador genera una máquina de estados, y Skeet dedica en *C# in Depth* páginas al efecto que más desconcierta a los recién llegados —la *ejecución diferida* de LINQ. Una consulta `var q = lista.Where(...)` no filtra nada al escribirla; filtra cada vez que se enumera, de modo que si la lista cambia entre dos recorridos, la misma variable `q` da dos resultados distintos, y si es cara, se paga dos veces. Rust hace de la pereza la norma: todos sus adaptadores —`map`, `filter`, `take`, `skip`— construyen un nuevo iterador sin computar nada, y el trabajo solo ocurre en una operación *terminal* como `collect()`, `sum()` o un `for`; el compilador incluso avisa con `unused_must_use` cuando construyes un iterador y no lo consumes, porque casi siempre es un bug. Java repitió el patrón en los Streams: operaciones intermedias perezosas frente a operaciones terminales que disparan el cálculo, con la regla añadida —que Bloch subraya en *Effective Java*— de que un stream se consume **una sola vez** e intentar reutilizarlo lanza `IllegalStateException`. Go, el más tardío, formalizó en la versión 1.23 las funciones *range-over-func* y el tipo `iter.Seq`, que permiten escribir un productor perezoso y recorrerlo con el `range` de siempre. Y PHP tiene generadores con `yield` desde la 5.5, la vía canónica —según Lockhart en *Modern PHP*— para recorrer un archivo enorme sin agotar el `memory_limit`.

## 🧩 Situación

Los pares no tienen fin, y ese es el punto: con un generador perezoso pides "los primeros n" sin construir jamás una lista infinita, porque cada valor se calcula en el instante en que lo consumes. Es como abrir el grifo solo lo justo. La versión industrial de esa idea aparece en cuanto los datos dejan de caber cómodamente en memoria: leer un log de 10 GB línea a línea, paginar los resultados de una API sin acumularlos, transformar un CSV de millones de filas en una tubería de `map` y `filter` que nunca materializa el conjunto intermedio, o consumir un flujo que sigue llegando y no tiene final conocido. En todos esos casos la diferencia entre estricto y perezoso no es de estilo: es la diferencia entre un proceso que ocupa memoria constante y otro que muere con un error de falta de memoria.

El porqué de ingeniería tiene, sin embargo, dos caras. La pereza reduce el pico de memoria y adelanta el primer resultado —una tubería perezosa empieza a producir salida antes de haber leído toda la entrada, lo que baja la latencia percibida—, pero desplaza el momento en que las cosas ocurren, y con él el momento en que fallan. Una excepción lanzada dentro de un generador no aparece donde se escribió la lógica, sino donde alguien consumió el valor, a veces muchas capas más arriba; una traza de pila de un generador es más difícil de leer que la de un bucle plano; y los efectos secundarios diferidos —abrir un archivo, hacer una consulta— se disparan en un instante que el código no deja ver. A eso se suman las tres limitaciones estructurales: un generador **no se puede recorrer dos veces** (la segunda vez ya está agotado y devuelve vacío, en silencio, sin error), **no tiene longitud** (`len()` falla, y contarlo lo consume), y **no admite acceso por posición**. Los bugs más caros de esta clase no son fallos ruidosos sino resultados vacíos que nadie cuestiona: un stream de Java reutilizado, un `IEnumerable` de C# enumerado dos veces contra una base de datos, un generador de Python que se pasó a dos funciones y solo la primera vio datos.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `pares=<2-4-...-2n>`
- **Regla:** pares_i = 2·i para i de 1 a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `pares=2-4-6` |
| `1` | `pares=2` |
| `5` | `pares=2-4-6-8-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA i de 1 a n: emitir 2*i
ESCRIBIR "pares=" UNIR(emitidos, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
pares = (2 * i for i in range(1, n + 1))
print("pares=" + "-".join(str(x) for x in pares))
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares: number[] = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
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
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append("-");
            sb.append(2 * i);
        }
        System.out.println("pares=" + sb);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var pares = Enumerable.Range(1, n).Select(i => 2 * i);
Console.WriteLine($"pares={string.Join("-", pares)}");
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
	var sb strings.Builder
	for i := 1; i <= n; i++ {
		if i > 1 {
			sb.WriteString("-")
		}
		sb.WriteString(strconv.Itoa(2 * i))
	}
	fmt.Printf("pares=%s\n", sb.String())
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pares: Vec<String> = (1..=n).map(|i| (2 * i).to_string()).collect();
    println!("pares={}", pares.join("-"));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("pares=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", 2 * i);
    }
    printf("\n");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: genera los pares con un CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE pares(i, v) AS (
    VALUES (1, 2)
    UNION ALL SELECT i + 1, (i + 1) * 2 FROM pares WHERE i < 5
)
SELECT 'pares=' || group_concat(v, '-') AS resultado FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$pares = [];
for ($i = 1; $i <= $n; $i++) {
    $pares[] = 2 * $i;
}
echo "pares=" . implode("-", $pares) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `3` de `casos.json`, cuya salida esperada es `pares=2-4-6`. En **Python**, `n = int(sys.stdin.readline())` fija `n = 3`. La línea siguiente, `pares = (2 * i for i in range(1, n + 1))`, es la clave de toda la clase: **no calcula nada**. Los paréntesis (en vez de corchetes) crean una expresión generadora, un objeto perezoso que sabe cómo producir la secuencia pero que aún no ha multiplicado ni una vez. `range(1, 4)` tampoco materializa `[1, 2, 3]`: es a su vez un objeto perezoso. El trabajo empieza en la última línea, cuando `"-".join(str(x) for x in pares)` recorre el generador: `join` pide el primer valor, el generador arranca, toma `1` de `range`, calcula `2 * 1 = 2`, lo entrega y se **suspende** conservando su estado; la segunda petición lo reanuda justo ahí, toma `2` y entrega `4`; la tercera entrega `6`; la cuarta encuentra `range` agotado, el generador termina y levanta `StopIteration`, que `join` interpreta como fin. Se imprime `pares=2-4-6`. En ningún momento existió una lista de tres elementos: existieron tres enteros, uno a uno. Y si esa segunda línea se ejecutara de nuevo sobre el mismo `pares`, la cadena resultante sería vacía, porque el generador ya está consumido.

En **Rust**, la misma pereza está más explícita y el punto en que se rompe también. Tras parsear `n = 3`, la expresión `(1..=n)` construye un `RangeInclusive`, que es un iterador perezoso; `.map(|i| (2 * i).to_string())` **no aplica el cierre a nada**: devuelve un adaptador `Map` que envuelve el rango y recuerda qué función habrá que aplicar. Hasta aquí no se ha multiplicado ni formateado nada, y si el programa terminara ahí el compilador avisaría de que se construyó un iterador y no se usó. Quien dispara el trabajo es `.collect()`: la operación terminal que va pidiendo elementos al adaptador —`1` → `"2"`, `2` → `"4"`, `3` → `"6"`— y los deposita en el `Vec<String>` que el tipo anotado a la izquierda le indica construir. Nótese la diferencia con Python: aquí la pereza de la tubería se paga al final con una materialización explícita, porque `join` necesita un `Vec`. Finalmente `pares.join("-")` produce `"2-4-6"` y `println!` imprime `pares=2-4-6`.

El **C** de esta clase representa el extremo opuesto y, paradójicamente, llega al mismo ahorro de memoria por otra vía. No hay generador, ni iterador, ni colección: tras leer `n = 3` con `scanf`, un `printf("pares=")` escribe el prefijo y el bucle `for (long i = 1; i <= n; i++)` calcula y **emite** cada valor en el acto —`if (i > 1) printf("-")` antepone el separador salvo en la primera vuelta, y `printf("%ld", 2 * i)` escribe `2`, luego `4`, luego `6`. El `printf("\n")` final cierra la línea. C no puede diferir el cálculo porque no tiene manera de suspender una función a medias, pero tampoco necesita almacenar la secuencia: la escribe directamente en la salida conforme la produce. Es la misma memoria O(1) que da un generador, obtenida por ausencia de abstracción en lugar de por una abstracción sofisticada. La diferencia práctica aparece en cuanto la secuencia debe *componerse* —filtrarse, transformarse, pasarse a otra función—: en Python o Rust eso es encadenar adaptadores; en C hay que reescribir el bucle.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(2*i for i in ...)` (Python) vs. `(1..=n).map(...)` (Rust) vs. bucle (C/Java). |
| Semántica | Python/Rust generan perezosamente; C/Java construyen la lista al vuelo. |
| Paradigmática | SQL genera con un CTE recursivo. |

Ordenando los diez lenguajes por *cómo* consiguen la pereza aparecen cuatro grupos. El primero es el de los **generadores como corrutinas**: **Python** (`yield` y expresiones generadoras `( ... for ... )`), **JavaScript** y **TypeScript** (`function*` con `yield`, que produce un objeto que es a la vez iterable e iterador), **C#** (`yield return` dentro de un método que devuelve `IEnumerable<T>`, compilado a una máquina de estados) y **PHP** (`yield` desde la 5.5). En los cinco, el compilador transforma una función de aspecto normal en algo capaz de suspenderse y reanudarse conservando sus locales. El segundo grupo es el de las **tuberías de adaptadores perezosos**: **Rust**, donde `map`, `filter` o `take` no hacen nada hasta una operación terminal como `collect()` o `sum()`, y **Java**, cuyos Streams separan operaciones intermedias de terminales con la misma lógica y añaden la regla de un solo consumo. **C#** pertenece a los dos grupos a la vez, porque LINQ es exactamente esa tubería diferida montada sobre `IEnumerable`. El tercer grupo es **Go**, que durante quince años careció de generadores y resolvía la producción bajo demanda con una goroutine escribiendo en un canal, hasta que la versión 1.23 introdujo las funciones *range-over-func* y `iter.Seq`, permitiendo por fin escribir un productor perezoso recorrible con `range`. El cuarto es el de los que **no tienen pereza en el lenguaje**: **C**, que compensa emitiendo directamente a la salida como hace la implementación de esta clase, y **SQL**, cuyo caso es especial: el programador escribe algo estrictamente declarativo —aquí un CTE recursivo—, pero el motor por debajo suele materializar los resultados en un *cursor* que el cliente consume por lotes, es decir, pereza decidida por el planificador y no por quien escribe la consulta.

## 🧬 El concepto en la familia

La familia de C nació estricta y adoptó la pereza tarde y por capas: C no la tiene, C++ esperó hasta los *ranges* de C++20, Java la trajo con los Streams en la versión 8, C# la introdujo pronto con `yield return` y la convirtió en el corazón de LINQ, y JavaScript la incorporó con los generadores de ES6 —donde, además, resultó ser el sustrato sobre el que se construyeron las promesas y luego `async`/`await`. En la familia del scripting dinámico la pereza llegó como refinamiento de estructuras ya existentes: Python 2.2 introdujo `yield` y Python 3 hizo perezosos por defecto `range`, `map`, `filter` y `zip`, cambiando el comportamiento por omisión de todo el lenguaje; Ruby distingue `each` de `lazy` y su `Enumerator::Lazy` permite encadenar sobre secuencias infinitas; PHP añadió generadores para resolver justo el problema de los archivos grandes. La familia ML y funcional es de donde procede la idea entera: Haskell es perezoso *por defecto* —`take n [2,4..]` sobre una lista infinita es idioma cotidiano, no truco—, y OCaml o F# ofrecen secuencias perezosas explícitas junto a estructuras estrictas. Go y Rust encarnan de nuevo dos filosofías opuestas: Go prefirió durante años la concurrencia (una goroutine y un canal) a la pereza como abstracción, y solo en 1.23 cedió con `iter.Seq`; Rust hizo lo contrario y puso la pereza en la base de todo, de modo que ser estricto —llamar a `collect()`— es la excepción que hay que escribir explícitamente. Los declarativos cierran el arco: en SQL la pregunta ni se plantea, porque el programador describe *qué* conjunto quiere y es el planificador quien decide qué se materializa y qué se entrega fila a fila.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 066
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Recorrer dos veces un generador ya agotado** → causa: un generador conserva su posición y, una vez consumido, la siguiente iteración no vuelve a empezar: devuelve vacío. En Python eso significa una suma de `0` o una cadena vacía **sin ningún error**; en Java, reutilizar un Stream lanza `IllegalStateException` → solución: si necesitas recorrer varias veces, materializa con `list(...)` / `collect()` / `toList()`, o crea un generador nuevo en cada pasada.
- **Consultas diferidas evaluadas más de una vez** → causa: en C#, `var q = tabla.Where(...)` no ejecuta nada al escribirse; cada `foreach` o cada `Count()` vuelve a recorrer la fuente, de modo que dos usos de `q` disparan dos consultas a la base de datos y, si los datos cambiaron entre medias, devuelven resultados distintos → solución: cerrar la consulta con `.ToList()` o `.ToArray()` en el punto donde quieres fijar el resultado, y dejarla diferida solo cuando la pereza sea intencional.
- **Efectos secundarios dentro de un generador** → causa: abrir archivos, escribir logs o lanzar excepciones dentro de una función perezosa hace que esos efectos ocurran donde alguien consume, no donde se escribió el código; la excepción aparece con una traza desconcertante y el recurso puede quedarse abierto si el consumidor abandona el recorrido a medias → solución: mantener el generador puro (solo producir valores) y gestionar los recursos fuera con `with` / `using` / RAII, o construir el generador de modo que libere en su bloque `finally`.
- **Construir la lista infinita entera** → causa: aplicar una operación estricta —`list()`, `collect()`, `sorted()`, `len()`— a una secuencia sin fin consume memoria hasta agotarla y el proceso muere; ni siquiera hace falta que sea infinita, basta con que no quepa → solución: cortar *antes* de materializar, con `itertools.islice`, `.take(n)` o `limit(n)`, que en una tubería perezosa detienen la producción aguas arriba.
- **Olvidar el separador en el caso n=1** → causa: anteponer el guion a cada elemento en vez de intercalarlo produce `pares=-2`; es el clásico error de límite en la construcción de cadenas, y solo se ve con listas de un elemento → solución: unir con la operación de *join* del lenguaje, que intercala por definición, o —como hacen las versiones de Java, Go y C de esta clase— condicionar el separador con `if (i > 1)`.

## ❓ Preguntas frecuentes

- **¿Qué gana realmente la pereza?** Dos cosas medibles. Memoria: pasas de O(n) a O(1), lo que permite procesar un archivo de 10 GB con un proceso de unos pocos megabytes. Y latencia: una tubería perezosa entrega el primer resultado antes de haber leído toda la entrada, en lugar de esperar a completar cada etapa. A eso se suma una ganancia expresiva: permite trabajar con secuencias infinitas, algo sencillamente imposible en evaluación estricta.
- **¿Qué ocurre exactamente al llamar a una función con `yield`?** No se ejecuta ni una línea de su cuerpo: la llamada devuelve un objeto generador. El cuerpo empieza a correr en la primera petición (`next()`, o la primera vuelta de un `for`) y avanza hasta el primer `yield`, donde se suspende conservando sus variables locales y el punto exacto de ejecución. La siguiente petición lo reanuda desde ahí. Esa suspensión con estado es lo que hace de un generador una corrutina y no una función corriente.
- **¿Por qué en Rust un `map` no hace nada?** Porque todos los adaptadores de `Iterator` son perezosos por diseño: `map`, `filter` o `take` devuelven un nuevo iterador que recuerda la operación pendiente, y el cómputo solo ocurre en una operación *terminal* como `collect()`, `sum()`, `for` o `count()`. El compilador te avisa con `unused_must_use` si construyes un iterador y no lo consumes, precisamente porque en ese caso el código no hace nada y casi siempre es un error.
- **¿Cuál es el precio de la pereza?** Un generador no se puede recorrer dos veces, no tiene longitud (`len()` falla y contarlo lo consume), no admite acceso por índice, y sus errores y efectos secundarios se producen lejos de donde se escribieron, lo que complica las trazas y la depuración. Cuando la colección es pequeña y se recorre varias veces, una lista estricta es más simple, más rápida y mucho más fácil de razonar: la pereza se justifica por el tamaño de los datos o por su carácter infinito, no por elegancia.
- **¿Y en Go, que no tenía generadores?** Durante años el idioma era lanzar una goroutine que escribía valores en un canal y recorrer el canal con `range`, a costa de sincronización y del riesgo de dejar la goroutine bloqueada si nadie consumía hasta el final. Desde Go 1.23 existen las funciones *range-over-func* y el tipo `iter.Seq`, que permiten escribir un productor perezoso y recorrerlo con el `range` de siempre, sin concurrencia de por medio.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su tratamiento de las corrutinas —subprogramas con varios puntos de suspensión y reanudación, y estado que sobrevive entre ellos— es el fundamento conceptual de lo que hoy llamamos generador.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo, donde compara la evaluación estricta con la perezosa y sitúa los generadores y los iteradores definidos por el usuario dentro de las estructuras de control por iterador.

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

> [⏮️ Clase 065](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 067 ⏭️](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md)
