# Clase 068 — Funciones de orden superior: map, filter, reduce

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una **función de orden superior** es simplemente una función que recibe otra función como argumento o que devuelve una función. La idea parece modesta y sin embargo es la que permite fabricar operaciones genéricas sobre colecciones: si `map` recibe la transformación que debe aplicar, entonces `map` no necesita saber nada de números, ni de textos, ni de facturas —solo sabe recorrer y aplicar. Ese desacoplamiento entre el *recorrido* (siempre igual) y la *operación* (siempre distinta) es lo que convirtió a **map**, **filter** y **reduce** en el vocabulario común del procesamiento de datos, de Lisp a Java Streams, de SQL a los pipelines distribuidos.

Los tres no están al mismo nivel. `reduce` —llamado `fold` en la tradición funcional y `accumulate` en el *Structure and Interpretation of Computer Programs* de Abelson y Sussman— es el más general: tanto `map` como `filter` pueden expresarse como un `reduce` que va construyendo una lista, y no al revés. Por eso esta clase parte de doblar cada elemento (`map`) y sumarlos (`reduce`) sobre una lista de enteros, y desde ahí examina lo que ese ejercicio mínimo esconde: el papel del elemento neutro y por qué un `reduce` sin valor inicial falla sobre la colección vacía; la diferencia entre plegar por la izquierda y por la derecha y cuándo la asociatividad importa; por qué la función que pasas debe ser pura si quieres un resultado predecible o paralelizable; y la enorme divergencia de coste entre los lenguajes que crean una colección intermedia en cada eslabón de la cadena y los que fusionan toda la cadena en un solo recorrido.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección con map.
2. Combinar una colección con reduce.
3. Encadenar operaciones de orden superior.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | map | Transformar cada elemento |
| 2 | reduce | Combinar en un solo valor |
| 3 | Funciones de orden superior | Reciben otra función |
| 4 | Encadenar | map y luego reduce |

## 📖 Definiciones y características

- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: transforma sin mutar.
- **reduce** — combina todos los elementos en un valor (suma, producto). Clave: acumula.
- **Función de orden superior** — recibe o devuelve otra función. Clave: base del estilo funcional.
- **Encadenamiento** — conectar operaciones (map → reduce). Clave: pipeline de datos.
- **Elemento neutro** — valor inicial que no altera el resultado (`0` al sumar, `1` al multiplicar). Clave: hace que el reduce funcione sobre la colección vacía.

Abelson y Sussman, en *Structure and Interpretation of Computer Programs*, presentan estas operaciones no como funciones de biblioteca sino como *patrones de abstracción*: el `accumulate` que definen allí toma una operación binaria, un valor inicial y una secuencia, y con él construyen la suma, el producto, el `map` y el `filter` como casos particulares. Ese ejercicio es la mejor demostración de que `reduce` es el primitivo y los otros dos son derivados: `map(f, xs)` es un `reduce` que va anteponiendo `f(x)` a la lista acumulada, y `filter(p, xs)` es un `reduce` que antepone `x` solo si `p(x)` se cumple. Sebesta, al tratar en *Concepts of Programming Languages* las construcciones de control basadas en funciones, subraya el requisito que hace todo esto posible: el lenguaje debe tratar las funciones como valores de primera clase, es decir, poder pasarlas, devolverlas y almacenarlas igual que un entero. Donde ese requisito no se cumple del todo, el patrón aparece torcido —en C hay que pasar punteros a función, como en `qsort`, y en Go faltaron los genéricos hasta la versión 1.18.

El detalle que más quebraderos de cabeza produce es el valor inicial de `reduce`. Con neutro explícito, `reduce(+, xs, 0)` devuelve `0` sobre la lista vacía y todo funciona; sin él, no hay nada que devolver y cada lenguaje elige un desastre distinto: Python lanza `TypeError: reduce() of empty sequence with no initial value`, JavaScript lanza `TypeError: Reduce of empty array with no initial value`, y Java —más honesto— cambia el tipo de retorno y devuelve un `Optional<T>` que te obliga a decidir qué hacer con el caso vacío. El segundo detalle es la dirección del pliegue: `foldl` combina desde la izquierda (`((0+1)+2)+3`) y `foldr` desde la derecha (`1+(2+(3+0))`). Si la operación es asociativa y conmutativa, como la suma, da igual; si es la resta o la concatenación de listas, el resultado cambia por completo. Y el tercero es la pureza: si la función que pasas lee o escribe estado externo, el resultado deja de depender solo de la entrada y el pliegue ya no puede reordenarse ni repartirse entre hilos. Esa es exactamente la condición que Java exige para que `parallelStream()` sea correcto y la que Rayon presupone en Rust; Bloch insiste en *Effective Java* en que las lambdas de un stream deben ser libres de efectos secundarios, y que un `forEach` que muta un acumulador externo es la señal de que el pipeline está mal escrito.

## 🧩 Situación

Calcular el total de una factura con IVA es el ejemplo canónico: `map` aplica el impuesto a cada línea y `reduce` las suma. Pero el patrón está mucho más extendido de lo que sugiere ese ejemplo. Todo informe agregado —ventas por región, latencia media por servicio, usuarios activos por día— es un filtro seguido de una transformación seguida de un pliegue, y esa misma tríada es la que da nombre al modelo MapReduce con el que se procesaron durante una década los conjuntos de datos que no cabían en una máquina. La razón por la que el vocabulario se estandarizó es que separa lo que el motor de ejecución puede optimizar (recorrer, repartir, paralelizar) de lo que solo el programador sabe (qué hacer con cada elemento).

El coste de ingeniería aparece en dos frentes concretos. El primero es la memoria y las colecciones intermedias: en JavaScript, `datos.filter(...).map(...).map(...)` crea tres arrays completos, y sobre un millón de elementos eso son tres millones de asignaciones que el recolector de basura tendrá que limpiar; los Streams de Java, LINQ en C# y los adaptadores de iterador en Rust evitan ese gasto porque son perezosos y solo recorren una vez, al llegar la operación terminal. El segundo frente son los fallos: un `reduce` sin valor inicial que funciona en desarrollo con datos de prueba y revienta en producción el día que el filtro previo no deja pasar nada es un clásico documentado hasta el aburrimiento, y su causa es siempre la misma —no haberse preguntado cuál es el elemento neutro de la operación. Añádase el error de pasar una función impura a un `parallelStream`, que no falla siempre sino de vez en cuando y con resultados distintos en cada ejecución, y se tiene el tipo de defecto más caro de diagnosticar que existe.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por -> total=<suma de los doblados>`
- **Regla:** doblados = map(x→2x) ; total = reduce(+, doblados)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6 total=12` |
| `5` | `doblados=10 total=10` |
| `2 4` | `doblados=4-8 total=12` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
doblados <- MAP(x -> 2x, lista)
total <- REDUCE(+, doblados)
ESCRIBIR "doblados=" UNIR(doblados,"-") " total=" total
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
doblados = [x * 2 for x in nums]
total = sum(doblados)
print(f"doblados={'-'.join(str(x) for x in doblados)} total={total}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
const total = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
const total: number = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> doblados = Arrays.stream(p)
                .map(Integer::parseInt)
                .map(x -> x * 2)
                .collect(Collectors.toList());
        int total = doblados.stream().mapToInt(Integer::intValue).sum();
        String s = doblados.stream().map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + s + " total=" + total);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2).ToList();
int total = doblados.Sum();
Console.WriteLine($"doblados={string.Join("-", doblados)} total={total}");
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
	var doblados []string
	total := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		d := n * 2
		doblados = append(doblados, strconv.Itoa(d))
		total += d
	}
	fmt.Printf("doblados=%s total=%d\n", strings.Join(doblados, "-"), total)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<i64> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap() * 2)
        .collect();
    let total: i64 = doblados.iter().sum();
    let texto: Vec<String> = doblados.iter().map(|x| x.to_string()).collect();
    println!("doblados={} total={}", texto.join("-"), total);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x, total = 0;
    int primero = 1;
    printf("doblados=");
    long primeros[1024];
    int k = 0;
    while (scanf("%ld", &x) == 1) {
        primeros[k++] = x * 2;
    }
    for (int i = 0; i < k; i++) {
        if (!primero) printf("-");
        printf("%ld", primeros[i]);
        total += primeros[i];
        primero = 0;
    }
    printf(" total=%ld\n", total);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el 'map' va en el SELECT y el 'reduce' con SUM().
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') || printf(' total=%d', sum(x * 2)) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$doblados = array_map(fn($x) => (int) $x * 2, $nums);
$total = array_reduce($doblados, fn($a, $b) => $a + $b, 0);
echo "doblados=" . implode("-", $doblados) . " total=$total\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `1 2 3` de `casos.json`, cuya salida esperada es `doblados=2-4-6 total=12`. **Python** es el que menos parece usar funciones de orden superior, y esa es justamente la lección. `nums = [int(x) for x in sys.stdin.read().split()]` deja `nums = [1, 2, 3]`; `doblados = [x * 2 for x in nums]` es un `map` escrito como comprensión y produce `[2, 4, 6]`; y `total = sum(doblados)` es un `reduce` con la suma y con `0` como valor inicial ya incorporado —`sum` sobre una lista vacía devuelve `0` sin quejarse, precisamente porque conoce su elemento neutro. Guido van Rossum prefirió que el Python idiomático se escribiera así: la comprensión en lugar de `map`, y los reductores especializados `sum`, `min`, `max`, `any`, `all` en lugar del `reduce` genérico, que en Python 3 dejó de ser una función incorporada y vive en `functools`. La línea final compone `doblados=2-4-6 total=12`.

En **JavaScript** los tres pasos están a la vista y muestran el modelo *eager* de los métodos de `Array`. `.split(/\s+/)` da `["1","2","3"]` y `.map(Number)` construye un array nuevo `[1, 2, 3]`; `nums.map((x) => x * 2)` construye *otro* array nuevo, `[2, 4, 6]`; y `doblados.reduce((a, b) => a + b, 0)` pliega: arranca con el acumulador en `0` (el segundo argumento, el neutro explícito), hace `0+2 = 2`, luego `2+4 = 6`, luego `6+6 = 12`. Ese `0` no es decorativo: si se omitiera, `reduce` tomaría el primer elemento como acumulador inicial —lo que aquí daría el mismo `12`— pero lanzaría `TypeError: Reduce of empty array with no initial value` en cuanto la entrada estuviera vacía. **Rust** hace lo mismo con una diferencia de coste importante: `s.split_whitespace().map(|x| x.parse::<i64>().unwrap() * 2).collect()` encadena adaptadores perezosos que no ejecutan nada hasta que `.collect()` los fuerza, de modo que parsear y doblar ocurren en un único recorrido y solo se materializa un vector, `[2, 4, 6]`. Después `doblados.iter().sum()` es el reduce —`sum` sobre un iterador de `i64` devuelve `0` si está vacío— y un segundo `.map(...).collect()` produce el `Vec<String>` para unir con guiones.

**Go** cierra el arco por el extremo opuesto: no hay `map` ni `reduce` por ninguna parte. El bucle `for _, s := range strings.Fields(line)` recorre `"1"`, `"2"`, `"3"`; en cada vuelta `n, _ := strconv.Atoi(s)` convierte, `d := n * 2` aplica la transformación (el map), `doblados = append(doblados, strconv.Itoa(d))` acumula el texto y `total += d` acumula la suma (el reduce). Con `s = "1"`: `d = 2`, `doblados = ["2"]`, `total = 2`. Con `"2"`: `d = 4`, `total = 6`. Con `"3"`: `d = 6`, `total = 12`. Lo notable es que Go hace map y reduce *en la misma pasada*, mientras que JavaScript necesitó dos recorridos y dos arrays. Donovan y Kernighan defienden esta preferencia en *The Go Programming Language*: el bucle explícito es más largo pero no esconde nada, no crea colecciones intermedias y no obliga al lector a saber si la cadena es perezosa. Los cuatro programas transforman `1 2 3` en `doblados=2-4-6 total=12`; lo que cambia es cuánta maquinaria queda a la vista y cuántas veces se recorren los datos.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map`/`sum` (Python) vs. `.map().reduce()` (JS) vs. `.iter().map().sum()` (Rust). |
| Semántica | map/reduce no mutan la lista original; devuelven valores nuevos. |
| Paradigmática | SQL hace el 'map' en el SELECT y el 'reduce' con SUM(). |

Los diez lenguajes se ordenan bien por una sola pregunta: ¿la cadena de operaciones es perezosa o materializa una colección en cada eslabón? **JavaScript**, **TypeScript** y **PHP** están en el lado *eager*: cada `map` y cada `filter` de `Array` crean un array nuevo completo, y `array_map`/`array_filter`/`array_reduce` en PHP hacen lo mismo con arrays; es el modelo más simple de entender y el que más basura genera en cadenas largas. **Java** y **C#** están en el lado perezoso y con una frontera explícita: un `Stream` de Java o una consulta LINQ de C# no ejecutan nada mientras solo se encadenan operaciones intermedias (`map`/`Select`, `filter`/`Where`), y todo el pipeline recorre los datos una única vez cuando llega la operación terminal (`collect`, `sum`, `ToList`); Bloch trata en *Effective Java* las condiciones —funciones sin efectos secundarios— bajo las que ese pipeline puede además ejecutarse con `parallelStream()`, y Skeet explica en *C# in Depth* cómo LINQ traduce la sintaxis de consulta a esas mismas llamadas. **Rust** lleva la pereza más lejos: sus adaptadores de iterador no solo evitan colecciones intermedias, sino que el compilador los funde en un único bucle sin sobrecoste alguno respecto al bucle escrito a mano —la abstracción de coste cero que Klabnik y Nichols documentan. **Python** ocupa un lugar propio: `map` y `filter` sí devuelven iteradores perezosos desde Python 3, pero el estilo idiomático prefiere las comprensiones y los reductores especializados, y `reduce` fue desterrado a `functools`. En el extremo sin abstracción están **Go** y **C**: Go, aun con genéricos desde la versión 1.18, mantiene la preferencia idiomática por el bucle explícito, y C solo tiene punteros a función —el `qsort` de la biblioteca estándar, que Kernighan y Ritchie usan como ejemplo, es la función de orden superior canónica del lenguaje—, de modo que map y reduce se escriben a mano. **SQL**, finalmente, lleva décadas haciendo esto sin llamarlo así: la lista de expresiones del `SELECT` es un map, el `WHERE` es un filter, y los agregados `SUM`, `AVG`, `COUNT` o `MAX` son reduces cuyo elemento neutro y cuyo comportamiento sobre el conjunto vacío están definidos por el estándar.

## 🧬 El concepto en la familia

El linaje empieza en Lisp, donde `mapcar` y los pliegues existen desde los años sesenta y donde Abelson y Sussman los presentan en *SICP* como patrones que uno mismo define, no como biblioteca. La familia ML y funcional los convirtió en el vocabulario central: Haskell escribe `sum (map (*2) xs)` y distingue explícitamente `foldl` de `foldr`, con consecuencias reales sobre la terminación en listas infinitas; Scala tiene `map`, `filter` y `foldLeft`/`foldRight` sobre todas sus colecciones y añade `reduce` sin valor inicial que falla en la colección vacía, igual que sus primos; F# ofrece `List.map` y `List.fold` con el acumulador como primer argumento. La familia de scripting dinámico los adoptó como métodos: Ruby escribe `lista.map { |x| x*2 }.sum` y llama `inject` a su pliegue, PHP los tiene como funciones sueltas con el array como argumento, y Python los tiene pero los relegó frente a las comprensiones. La familia de C llegó tarde y por capas: C solo con punteros a función, C++ con los algoritmos de `<algorithm>` y después con los rangos de C++20, Java con los Streams desde la versión 8, C# con LINQ desde 2007 —y en los dos últimos casos la incorporación exigió antes añadir lambdas al lenguaje. Go y Rust vuelven a divergir: Rust reconstruye toda la tríada como adaptadores de iterador compilados a bucles, mientras Go la rechaza deliberadamente y deja el bucle a la vista incluso ahora que los genéricos harían posible una biblioteca. Y en el mundo declarativo, SQL implementa la tríada completa sin haber tomado nunca prestado el vocabulario funcional: proyección, restricción y agregación son map, filter y reduce con otros nombres, y Date los describe en *SQL and Relational Theory* como operadores del álgebra relacional, anteriores e independientes de la moda funcional que los popularizó.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 068
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **`reduce` sin valor inicial sobre una colección vacía** → causa: sin neutro explícito, el pliegue toma el primer elemento como acumulador, y si no hay ninguno no hay nada que devolver: Python lanza `TypeError: reduce() of empty sequence with no initial value`, JavaScript lanza `TypeError: Reduce of empty array with no initial value` y Java cambia el tipo de retorno a `Optional<T>` → solución: pasar siempre el elemento neutro de la operación (`0` al sumar, `1` al multiplicar, la cadena vacía al concatenar); el fallo aparece en producción el día que el filtro previo no deja pasar nada.
- **Pasar una función impura al map o al reduce** → causa: si la lambda lee o escribe estado externo, el resultado depende del orden de evaluación, y con `parallelStream()` en Java o Rayon en Rust ese orden no está garantizado: se obtienen resultados distintos en ejecuciones distintas → solución: que la función dependa solo de sus argumentos y no mute nada; si necesitas acumular estado externo, usa un bucle explícito y no un pipeline.
- **Suponer que el pliegue es asociativo cuando no lo es** → causa: `foldl` calcula `((0-1)-2)-3` y `foldr` calcula `1-(2-(3-0))`; con la resta, la división o la concatenación de listas los dos resultados difieren, y con la suma de floats incluso una operación "asociativa" puede dar totales distintos según el orden por error de redondeo → solución: comprobar la asociatividad antes de reordenar o paralelizar, y fijar explícitamente la dirección del pliegue cuando la operación no sea conmutativa.
- **Confundir `map` con `for-each`** → causa: `map` está definido para producir una colección nueva; usarlo por su efecto secundario (`arr.map(x => console.log(x))`) construye y descarta un array entero de `undefined`, y en Java un `Stream` intermedio sin operación terminal ni siquiera llega a ejecutarse → solución: `map` cuando quieres el resultado transformado, `forEach` (o un bucle) cuando lo que quieres es la acción.
- **Encadenar sin mirar el coste de las colecciones intermedias** → causa: en JavaScript o PHP, `datos.filter(...).map(...).map(...)` recorre la colección tres veces y asigna tres arrays completos, lo que sobre millones de elementos es un problema real de memoria y de recolección de basura → solución: fusionar los pasos en una sola función cuando el lenguaje es *eager*, o usar la vía perezosa donde exista —Streams en Java, LINQ en C#, adaptadores de iterador en Rust, generadores en Python.

## ❓ Preguntas frecuentes

- **¿`reduce` es lo mismo que un bucle de suma?** En resultado sí, pero `reduce` separa dos cosas que el bucle mezcla: el recorrido, que es siempre igual, y la operación binaria, que es lo único que varía. Esa separación es lo que permite que el motor decida recorrer una vez, recorrer perezosamente o repartir el trabajo entre hilos sin que tú cambies una línea. Abelson y Sussman lo presentan por eso como un patrón de abstracción, no como un atajo.
- **¿Por qué `reduce` es más fundamental que `map` y `filter`?** Porque los otros dos se expresan con él y no al revés: `map(f, xs)` es un pliegue que va construyendo la lista de los `f(x)`, y `filter(p, xs)` es un pliegue que añade `x` solo cuando `p(x)` se cumple. No hay forma de escribir un `reduce` general con `map` y `filter`, porque estos no pueden colapsar la colección a un valor único.
- **¿Y `filter`?** Selecciona los elementos que cumplen un predicado, sin transformarlos. Aquí no aparece porque el modelo solo dobla y suma, pero completa el trío y en la práctica suele ir primero: filtrar antes de transformar reduce el trabajo de los pasos siguientes, y en los pipelines perezosos (Streams, LINQ, iteradores de Rust) ese orden se traduce directamente en menos elementos recorridos.
- **¿Por qué en Python no se usa tanto `map`/`filter`?** Porque Guido van Rossum consideró que las comprensiones expresaban lo mismo con menos ceremonia y sin necesidad de una `lambda`, y en Python 3 `reduce` dejó de ser función incorporada y pasó a `functools`. `map` y `filter` siguen existiendo y devuelven iteradores perezosos, útiles cuando ya tienes la función con nombre; pero el estilo idiomático prefiere `[f(x) for x in xs]` y los reductores especializados `sum`, `any`, `all`, `min`, `max`.
- **¿Cuándo el pipeline funcional es más lento que el bucle?** Cuando el lenguaje es *eager* y la cadena es larga, porque cada eslabón asigna una colección nueva y vuelve a recorrer. En Rust no ocurre nunca: los adaptadores se funden en un único bucle y el código generado es equivalente al escrito a mano. En Java y C# tampoco, gracias a la pereza. En JavaScript y PHP sí puede notarse, y es el motivo por el que Go —donde el bucle es la forma idiomática— renuncia conscientemente a la abstracción.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su insistencia en aislar el estado y en construcciones cuyo significado no dependa del contexto es el fundamento de por qué la función pasada a un `map` o a un `reduce` debe ser pura.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo. Explica el requisito de las funciones como valores de primera clase y compara cómo lo satisfacen —o no— los lenguajes imperativos, funcionales y la familia de C.

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

> [⏮️ Clase 067](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 069 ⏭️](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md)
