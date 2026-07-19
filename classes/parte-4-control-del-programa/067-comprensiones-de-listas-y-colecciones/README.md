# Clase 067 — Comprensiones de listas y colecciones

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una **comprensión** es una expresión que construye una colección describiéndola en lugar de fabricarla paso a paso. Su forma —"los `x` de `lista` tales que `x` es par"— no la inventó la informática: es la notación de conjuntos de las matemáticas, `{x ∈ L : x mod 2 = 0}`, trasplantada casi literalmente a un lenguaje de programación. El camino fue SETL, el lenguaje de teoría de conjuntos de los años setenta, y después Haskell, de donde Python tomó la sintaxis con el `for` y el `if` en línea. Lo que se gana es que el resultado deja de ser un efecto acumulado sobre una lista vacía que vas rellenando y pasa a ser un valor descrito de una vez.

La distinción que hay que interiorizar en esta clase es entre *expresión* y *sentencia*. Un bucle `for` con `append` es una sentencia: no vale nada, hace algo, y el resultado vive en una variable que declaraste antes. Una comprensión es una expresión: vale la lista, y puedes pasarla directamente a una función, meterla en un diccionario o devolverla sin nombrarla nunca. En esta clase filtramos los pares de una lista de enteros y usamos ese ejercicio mínimo para recorrer las cuatro variantes de Python (lista, conjunto, diccionario y expresión generadora), el ámbito propio que Python 3 dio a la variable de la comprensión, el orden contraintuitivo de los `for` anidados, y —lo más revelador para un curso políglota— el hecho de que la mayoría de los lenguajes *no* tienen comprensiones y resuelven lo mismo encadenando `map` y `filter`, o, en el caso de SQL, con un `SELECT ... WHERE` que es literalmente una comprensión sobre filas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Filtrar una colección con una comprensión.
2. Expresar 'los que cumplen X' de forma declarativa.
3. Comparar la comprensión con el bucle equivalente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comprensión | Construir una lista describiéndola |
| 2 | Filtro | Quedarse con los que cumplen |
| 3 | Declarativo | Decir qué, no cómo |
| 4 | Comprensión vs. bucle | Más compacto y legible |

## 📖 Definiciones y características

- **Comprensión de lista** — expresión que construye una lista filtrando/transformando otra. Clave: declarativa y compacta.
- **Filtro** — condición que decide qué elementos entran. Clave: `if x % 2 == 0`.
- **Predicado** — condición booleana sobre cada elemento. Clave: define el filtro.
- **Estilo declarativo** — describir el resultado, no los pasos. Clave: menos ruido que el bucle.
- **Expresión generadora** — la misma sintaxis con paréntesis, que produce elementos bajo demanda. Clave: no materializa la lista.

Ramalho dedica en *Fluent Python* un tratamiento minucioso a esta construcción y establece una regla que conviene grabar: una comprensión debe existir para *construir una colección*, nunca para provocar un efecto secundario. Si el valor resultante se descarta, lo que se ha escrito es un bucle disfrazado y peor de leer, y lo correcto es escribir un `for` normal. Ramalho también insiste en la familia completa: la comprensión de lista con corchetes, la de conjunto con llaves (`{x for x in nums}`, que además deduplica), la de diccionario con `clave: valor` dentro de llaves, y la *expresión generadora* con paréntesis, que no construye nada hasta que alguien la consume. Esa última variante es la que permite escribir `sum(x for x in nums if x % 2 == 0)` sin pagar por una lista intermedia. Sebesta, al clasificar las estructuras de control en *Concepts of Programming Languages*, sitúa la comprensión en la categoría de las construcciones de iteración basadas en estructuras de datos, y subraya que su ascendencia matemática —la notación de conjuntos— es el motivo por el que se lee como una definición y no como un procedimiento.

Hay un detalle de semántica que separa Python 2 de Python 3 y que ilustra por qué esto es una expresión y no un bucle: en Python 3 la variable de la comprensión tiene su propio ámbito, de modo que `[x for x in nums]` no deja ningún `x` contaminando el entorno exterior ni pisa una variable `x` que ya existiera; en Python 2 sí se filtraba, y era una fuente real de errores. El segundo detalle es el orden de los `for` encadenados en una comprensión anidada: `[(a, b) for a in filas for b in columnas]` recorre en el mismo orden en que se escribirían los `for` anidados de un bucle —el primero es el externo—, lo cual resulta contraintuitivo porque la expresión producida aparece *antes* que los bucles que la generan. Y el tercero es el coste: una comprensión de lista materializa todos los elementos, con memoria O(n); si la colección es grande o infinita y solo vas a recorrerla una vez, la expresión generadora hace el mismo trabajo con memoria constante. Elegir entre corchetes y paréntesis no es cosmética: es elegir entre pagar la lista o no pagarla.

## 🧩 Situación

Quedarse con los pedidos pagados, los usuarios activos, las líneas de log con nivel `ERROR`, los archivos que superan cierto tamaño: filtrar una colección es probablemente la operación más repetida de todo el software de negocio. La comprensión existe porque ese gesto —recorrer, comprobar un predicado, quedarse con lo que pasa— se escribía una y otra vez en cuatro o cinco líneas de bucle en las que lo único que cambiaba era el predicado, y el resto era ceremonia: crear la lista vacía, iterar, comprobar, hacer `append`. La comprensión reduce ese esqueleto a la parte que de verdad varía, y eso, multiplicado por miles de apariciones en una base de código, cambia cuánto texto hay que leer para entender qué hace un programa.

El porqué de ingeniería tiene tres caras. La primera es la mantenibilidad: al ser una expresión sin estado intermedio, una comprensión no admite el error de olvidar reiniciar el acumulador entre usos ni el de mutar la lista que estás recorriendo, que en Python produce elementos saltados y en Java una `ConcurrentModificationException`. La segunda es el coste: la comprensión materializa toda la lista en memoria, y sobre un fichero de diez millones de líneas eso es la diferencia entre un proceso que corre y uno que muere por falta de memoria —ahí es donde la expresión generadora deja de ser un adorno. La tercera es la legibilidad, y es la que más se descuida: una comprensión con un `for`, un `if` y una expresión corta es más clara que el bucle; una con tres `for` anidados, dos `if` y una expresión condicional es ilegible, y el bucle explícito vuelve a ser la respuesta correcta. La regla práctica que se sigue en la mayoría de guías de estilo es que si no cabe cómoda en dos líneas o pasa de dos cláusulas, hay que desplegarla.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `pares=<los pares unidos por -, en orden>`
- **Regla:** pares = [x ∈ lista : x par]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `pares=2-4` |
| `10 15 20` | `pares=10-20` |
| `6 7 8` | `pares=6-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
pares <- [x EN lista SI x es par]
ESCRIBIR "pares=" UNIR(pares, "-")
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
pares = [x for x in nums if x % 2 == 0]
print("pares=" + "-".join(str(x) for x in pares))
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares: number[] = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
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
        String pares = Arrays.stream(p)
                .map(Integer::parseInt)
                .filter(x -> x % 2 == 0)
                .map(String::valueOf)
                .collect(Collectors.joining("-"));
        System.out.println("pares=" + pares);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pares = p.Select(int.Parse).Where(x => x % 2 == 0);
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
	var pares []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			pares = append(pares, strconv.Itoa(n))
		}
	}
	fmt.Printf("pares=%s\n", strings.Join(pares, "-"))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let pares: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| x.to_string())
        .collect();
    println!("pares={}", pares.join("-"));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("pares=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: filtra con WHERE.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'pares=' || group_concat(x, '-') AS resultado FROM nums WHERE x % 2 = 0;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pares = array_filter($nums, fn($x) => (int) $x % 2 === 0);
echo "pares=" . implode("-", $pares) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `1 2 3 4` de `casos.json`, cuya salida esperada es `pares=2-4`. En **Python** hay dos comprensiones encadenadas y conviene no confundirlas. La primera, `nums = [int(x) for x in sys.stdin.read().split()]`, no filtra nada: `split()` produce la lista de cadenas `["1", "2", "3", "4"]` y la comprensión aplica `int` a cada una, dejando `nums = [1, 2, 3, 4]` —es un *map* escrito como comprensión. La segunda, `pares = [x for x in nums if x % 2 == 0]`, es el filtro propiamente dicho: recorre `1` (el `if` da falso, se descarta), `2` (verdadero, entra), `3` (falso), `4` (verdadero, entra), y produce la lista nueva `[2, 4]` sin haber tocado `nums`. La línea final vuelve a usar la familia: `"-".join(str(x) for x in pares)` no lleva corchetes sino paréntesis, así que es una *expresión generadora* —`join` consume los elementos uno a uno y nunca se materializa una lista intermedia de cadenas. Se imprime `pares=2-4`.

En **C** no existe nada parecido, y el código muestra qué queda cuando se le quita la abstracción. No hay lista, ni siquiera: `while (scanf("%ld", &x) == 1)` lee un entero cada vez y lo procesa inmediatamente. Con `x = 1`, `x % 2 == 0` es falso y no ocurre nada; con `x = 2` el predicado se cumple, y aquí aparece la contabilidad manual que la comprensión te ahorra: la bandera `primero` vale `1`, así que *no* se imprime el guion separador, se imprime `2` y se pone `primero = 0`. Con `x = 3` se descarta; con `x = 4`, como `primero` ya es `0`, se imprime primero `-` y después `4`. Nótese que el prefijo `pares=` se escribió antes del bucle: C está construyendo la salida por escritura incremental sobre stdout, no construyendo una colección. El resultado es idéntico —`pares=2-4`— pero el programa nunca tuvo un objeto "los pares" al que referirse.

**Rust** ocupa el punto intermedio y es el más instructivo de los tres. `s.split_whitespace()` no devuelve un vector sino un iterador perezoso sobre los trozos `"1"`, `"2"`, `"3"`, `"4"`. Sobre él se encadenan tres adaptadores: `.map(|x| x.parse::<i64>().unwrap())` convierte a entero, `.filter(|x| x % 2 == 0)` deja pasar solo los pares y `.map(|x| x.to_string())` los vuelve texto. Ninguno de esos tres pasos ejecuta nada al escribirse: son descripciones. El trabajo lo dispara `.collect()`, que es lo que fuerza el recorrido y construye el `Vec<String>` con `["2", "4"]`. Y como los adaptadores se fusionan en un solo recorrido, no se crean los tres vectores intermedios que un lector desprevenido esperaría —el compilador genera un único bucle equivalente al de C. Finalmente `pares.join("-")` da `2-4`. Tres lenguajes, tres niveles de abstracción, el mismo recorrido lógico sobre `1 2 3 4` y la misma salida.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[x for x in l if x%2==0]` (Python) vs. `l.filter(...)` (JS/Rust) vs. bucle (C). |
| Semántica | La comprensión crea una lista nueva; el original no cambia. |
| Paradigmática | SQL filtra con `WHERE x % 2 = 0`. |

El reparto entre los diez lenguajes se ordena por una pregunta única: ¿tiene el lenguaje una *sintaxis dedicada* para describir una colección, o hay que componerla con llamadas a funciones? Solo **Python** tiene comprensiones de verdad, en sus cuatro sabores (lista, conjunto, diccionario y expresión generadora); es el heredero directo de Haskell y de SETL en el núcleo del curso. En el extremo opuesto, **JavaScript**, **TypeScript** y **PHP** resuelven lo mismo con métodos o funciones de biblioteca —`nums.filter(x => x % 2 === 0)` en los dos primeros, `array_filter($nums, fn($x) => ...)` en el tercero—: no hay sintaxis nueva, solo funciones que reciben otra función. **Java** y **C#** ofrecen un aparato más elaborado y perezoso: `Arrays.stream(...).filter(...).collect(...)` en Java, y en C# el `Where` de LINQ que, además de la forma de método que ve el código de esta clase, tiene una sintaxis de consulta (`from x in p where x % 2 == 0 select x`) que sí es comparable a una comprensión y que Skeet analiza en detalle en *C# in Depth* como azúcar sintáctico traducido a llamadas a `Where`/`Select`. **Rust** encadena adaptadores de iterador que se funden en un único bucle sin coste en tiempo de ejecución, la abstracción de coste cero que Klabnik y Nichols destacan en *The Rust Programming Language*. **Go** y **C** son los que no tienen nada: Go escribe el bucle explícito con un `if` y un `append`, y sus autores lo defienden como una decisión de claridad, no como una carencia; C ni siquiera construye la colección y va escribiendo la salida a medida que lee. **SQL**, por último, es el caso límite y el más puro: `SELECT x FROM nums WHERE x % 2 = 0` es, palabra por palabra, la notación de conjuntos que dio origen a la comprensión, aplicada a filas en vez de a elementos de una lista —Date insiste en *SQL and Relational Theory* en que la restricción relacional es exactamente ese "los que cumplen el predicado".

## 🧬 El concepto en la familia

La comprensión nació en la familia funcional y desde ahí se difundió con desigual fortuna. En los lenguajes ML y afines la construcción es nativa y central: Haskell escribe `[x | x <- xs, even x]` —la barra vertical lee literalmente como el "tal que" matemático— y añade comprensiones sobre listas infinitas gracias a su evaluación perezosa; Scala tiene el `for ... yield`, que además se traduce a llamadas a `flatMap`/`filter` y funciona sobre cualquier tipo que las implemente; F# ofrece `[for x in xs do if x % 2 = 0 then yield x]`; y en la tradición Lisp la idea aparece como macros de biblioteca (`loop` en Common Lisp, `for/list` en Racket) más que como sintaxis del núcleo. La familia de scripting dinámico se dividió: Python adoptó la sintaxis de Haskell casi tal cual y la extendió a conjuntos y diccionarios, mientras Ruby prefirió los métodos de bloque —`lista.select { |x| x.even? }`— y JavaScript llegó a tener comprensiones en un borrador de ES6 que finalmente se retiró en favor de `map`/`filter` y los iteradores. La familia de C nunca las tuvo como sintaxis: C, C++, Java y C# resuelven filtrando con bucles o con bibliotecas (Streams, LINQ, los algoritmos y rangos de C++20), y el LINQ de C# es lo más cerca que estuvo esa familia de una comprensión de pleno derecho. Go y Rust representan dos respuestas modernas opuestas: Go rechaza deliberadamente la construcción y deja el bucle a la vista, Rust la reconstruye como composición de adaptadores que el compilador colapsa. Y los declarativos —SQL a la cabeza— nunca necesitaron adoptarla, porque su lenguaje de consultas *es* una comprensión desde el principio.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 067
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar la lista mientras la recorres** → causa: borrar elementos de la misma lista que estás iterando desplaza los índices y el recorrido se salta posiciones —en Python quitar el elemento `i` hace que el siguiente pase inadvertido, y en Java lanza directamente `ConcurrentModificationException` → solución: no mutar: construir una lista nueva con la comprensión y, si hace falta, reasignarla al nombre original al terminar.
- **Usar la comprensión por su efecto secundario** → causa: escribir `[print(x) for x in nums]` construye y tira a la basura una lista de `None` solo para imprimir; Ramalho lo señala como el abuso característico de la construcción → solución: si el valor resultante no se usa, el gesto correcto es un `for` explícito; la comprensión es para *construir* una colección, no para ejecutar acciones.
- **Materializar cuando bastaba con recorrer** → causa: `sum([x for x in enormes if x % 2 == 0])` crea en memoria toda la lista intermedia antes de sumarla, con coste O(n) de memoria → solución: cambiar los corchetes por paréntesis y usar la expresión generadora `sum(x for x in enormes if x % 2 == 0)`, que consume los elementos de uno en uno con memoria constante.
- **Anidar hasta la ilegibilidad** → causa: acumular dos o tres `for` y varios `if` en una sola comprensión produce una línea que hay que descifrar en lugar de leer, y el orden de los `for` encadenados es contraintuitivo porque la expresión producida aparece antes que los bucles → solución: aplicar la regla de las dos cláusulas: más de un `for` y un `if` juntos piden desplegar el bucle explícito o partirlo en dos pasos con nombres.
- **Olvidar que `array_filter` de PHP conserva las claves** → causa: al filtrar un array indexado, PHP mantiene los índices originales (`0 => 2, 3 => 4`), de modo que el array resultante ya no es una lista contigua y `json_encode` lo serializa como objeto → solución: envolver el resultado en `array_values()` cuando se necesite reindexar; para `implode`, como en el código de esta clase, no importa porque solo usa los valores.

## ❓ Preguntas frecuentes

- **¿Comprensión o `filter`?** En Python la comprensión es casi siempre preferible: `filter` obliga a nombrar o escribir una `lambda`, y desde Python 3 devuelve un iterador, no una lista, lo que sorprende a quien esperaba poder indexarlo. En JavaScript, Rust o PHP no hay elección posible porque no existen comprensiones, y `filter` es la forma idiomática. Guido van Rossum defendió explícitamente las comprensiones frente a `map`/`filter` cuando se discutió su futuro en Python 3.
- **¿Es más lenta que un bucle?** No: una comprensión de lista suele ser algo más rápida que el bucle equivalente con `append`, porque evita la búsqueda y la llamada al método en cada vuelta. La diferencia que sí importa no es de velocidad sino de memoria: la comprensión materializa toda la lista, y ahí es donde la expresión generadora gana cuando la colección es grande.
- **¿Por qué mi variable de la comprensión no existe después?** Porque en Python 3 la comprensión tiene su propio ámbito, como si fuera una función: el `x` de `[x for x in nums]` vive y muere dentro de ella y no pisa ninguna variable exterior. En Python 2 sí se filtraba al ámbito circundante, y era una fuente clásica de errores silenciosos; el cambio fue deliberado.
- **¿Cuándo conviene un conjunto o un diccionario en vez de una lista?** Cuando el resultado no debe tener duplicados o cuando lo que construyes es una correspondencia. `{x for x in nums if x % 2 == 0}` deduplica y da búsqueda en tiempo constante; `{u.id: u.nombre for u in usuarios}` construye un índice en una sola expresión. Es la misma sintaxis con delimitadores distintos, y elegir bien el tipo del resultado ahorra un paso de conversión posterior.
- **¿Y si el lenguaje no tiene comprensiones?** Se compone lo mismo con `map` y `filter` encadenados: `filter` para el predicado, `map` para la transformación. La diferencia práctica es si esa cadena es perezosa —Java Streams, LINQ y los iteradores de Rust lo son y no crean colecciones intermedias— o si cada eslabón materializa un array nuevo, como ocurre con los métodos de `Array` en JavaScript.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su defensa de las construcciones que se leen como una descripción del resultado, y no como una secuencia de pasos con estado, es el argumento de fondo a favor de la comprensión frente al bucle con acumulador.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo. Sitúa la comprensión entre las construcciones de iteración basadas en estructuras de datos y traza su ascendencia en la notación de conjuntos, SETL y Haskell.

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

> [⏮️ Clase 066](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 068 ⏭️](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md)
