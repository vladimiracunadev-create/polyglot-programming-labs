# Clase 094 — Conjuntos (sets) y unicidad

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **conjunto (set)** no como «una lista que rechaza repetidos», sino como la encarnación en código de una idea matemática: una colección donde cada elemento aparece a lo sumo una vez y donde el orden no significa nada. Lo decisivo no es la unicidad en sí, sino *cómo* se consigue barata. Un conjunto se implementa casi siempre sobre una **tabla hash**, la estructura que Cormen desarrolla en el capítulo 11 de *Introduction to Algorithms*: aplicar una función hash al elemento da directamente el cubo donde vive o debería vivir, de modo que preguntar «¿está *x*?», insertar y borrar cuestan **O(1) promedio**, no O(n). Esa es la diferencia que hace al conjunto irremplazable: comprobar pertenencia en una lista obliga a recorrerla entera; en un conjunto es una sola consulta hash. El objetivo de hoy —contar cuántos valores distintos hay en una entrada— es la operación más natural del conjunto: metes todo y su tamaño final *es* la cantidad de únicos, porque los duplicados se absorben solos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Eliminar duplicados con un conjunto.
2. Contar elementos distintos.
3. Reconocer que el conjunto no tiene orden garantizado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Conjunto | Colección sin duplicados |
| 2 | Unicidad | Cada valor una vez |
| 3 | Pertenencia | Comprobar si algo está |

## 📖 Definiciones y características

Un **conjunto** es una colección de elementos **sin duplicados** y **sin orden garantizado**. Es la traducción a la programación del conjunto matemático: importa qué elementos están, no cuántas veces ni en qué posición. Sedgewick lo encuadra dentro de las *symbol tables* de *Algorithms* como el caso de una tabla que solo guarda claves, sin valores asociados; y esa parentela con la tabla hash explica su rendimiento. Cormen, en el capítulo 11 de *Introduction to Algorithms*, formaliza el mecanismo: una función hash reparte los elementos entre cubos, las **colisiones** (dos elementos que caen en el mismo cubo) se resuelven por encadenamiento o direccionamiento abierto, y bajo un buen hash las operaciones básicas quedan en **O(1) promedio**. El «promedio» es una salvedad importante: en el peor caso —muchas colisiones— degradan a O(n), pero con hashes razonables ese caso es rarísimo.

El conjunto ofrece tres operaciones que definen su carácter: **pertenencia** (¿está *x*?), **inserción** (añadir *x*, que no hace nada si ya está) y **borrado**, las tres en O(1) promedio frente a los O(n) de una lista. Sobre ellas se construyen las operaciones de conjunto propiamente dichas —**unión**, **intersección** y **diferencia**—, que son el motivo de que la estructura exista como abstracción y no como simple «lista deduplicada». El precio a pagar por esta velocidad es doble: se pierde el **orden** (iterar un conjunto no devuelve los elementos en ningún orden prometido) y los elementos deben ser **hashables**, es decir, tener una función hash y una comparación de igualdad estables.

- **Conjunto** — colección de elementos únicos respaldada por una tabla hash (Python `set`, Java/C# `HashSet`, Rust `HashSet`); pertenencia, inserción y borrado en O(1) promedio.
- **Unicidad** — cada valor aparece a lo sumo una vez; insertar uno ya presente no cambia el conjunto. Por eso el tamaño final cuenta los distintos.
- **Pertenencia** — comprobar si un elemento está, en O(1) promedio; es la operación que la lista hace en O(n) y el conjunto en tiempo constante.

## 🧩 Situación

¿Cuántos usuarios distintos entraron hoy? ¿Cuántas etiquetas únicas tiene un artículo? ¿Qué correos ya hemos visto para no procesarlos dos veces? Todas estas preguntas comparten la misma forma: descartar repeticiones y quedarse con lo distinto. Resolverlas con una lista obligaría, por cada elemento nuevo, a recorrer todo lo acumulado para ver si ya estaba —un patrón O(n²) que se arrastra en cuanto los datos crecen. El conjunto colapsa ese coste: cada inserción consulta el hash una vez y decide en tiempo constante. El caso de hoy es la versión mínima de ese patrón —contar valores enteros distintos en una línea— para que se vea con claridad que el conjunto *ya trae* la deduplicación incorporada: no hay que programarla, emerge de cómo está construido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `unicos=<cantidad de valores distintos>`
- **Regla:** unicos = |conjunto(lista)|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3 3 3` | `unicos=3` |
| `5 5 5` | `unicos=1` |
| `1 2 3 4` | `unicos=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; conjunto <- SET(lista) ; ESCRIBIR |conjunto|
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"unicos={len(set(nums))}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`unicos=${new Set(nums).size}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> s = new HashSet<>();
        for (String x : p) s.add(Integer.parseInt(x));
        System.out.println("unicos=" + s.size());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"unicos={p.Select(int.Parse).Distinct().Count()}");
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
	set := make(map[int]struct{})
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("unicos=%d\n", len(set))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let set: HashSet<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("unicos={}", set.len());
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int unicos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) unicos++;
    }
    printf("unicos=%d\n", unicos);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: COUNT(DISTINCT x).
WITH nums(x) AS (VALUES (1), (2), (2), (3), (3), (3))
SELECT printf('unicos=%d', count(DISTINCT x)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "unicos=" . count(array_unique($nums)) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 2 3 3 3`, que debe producir `unicos=3`. Aunque la entrada tiene seis números, solo tres son distintos; el conjunto absorbe los repetidos y su tamaño final da la respuesta.

En **Python**, la clave es `set(nums)`. La lista `nums = [1, 2, 2, 3, 3, 3]` se pasa al constructor `set`, que inserta cada elemento en una tabla hash: el `1` entra, el primer `2` entra, el segundo `2` calcula el mismo hash, cae en el mismo cubo, se compara igual y **no se añade**; lo mismo con los tres `3`. Al terminar, el conjunto contiene `{1, 2, 3}` y `len(...)` devuelve 3. Como explica Ramalho en *Fluent Python*, esta deduplicación es un efecto lateral gratuito de la estructura, no un paso extra de código.

En **Go**, no hay tipo conjunto nativo, así que se emula con `map[int]struct{}` —un mapa cuyas claves son los elementos y cuyos valores son el tipo vacío `struct{}`, que ocupa cero bytes. El bucle hace `set[n] = struct{}{}` por cada número: como las claves de un mapa son únicas, asignar dos veces la clave `2` no crea una segunda entrada. Al final, `len(set)` cuenta las claves distintas: 3. El truco de `struct{}` es idiomático precisamente porque comunica «solo me importa la presencia de la clave, no ningún valor».

En **C**, no existe ni conjunto ni tabla hash de serie, y el código lo hace evidente: lee los números en un arreglo `v[]` y, por cada elemento, recorre con un bucle interno todos los anteriores buscando si ya apareció. Es el patrón **O(n²)** que el conjunto justamente evita: para `1 2 2 3 3 3` cuenta el `1` (nuevo), el primer `2` (nuevo), descarta el segundo `2`, cuenta el primer `3` y descarta los otros dos, llegando a `unicos=3`. Funciona y da el resultado correcto, pero cada nuevo elemento cuesta recorrer todo lo anterior; contrastarlo con las versiones hash muestra exactamente qué compra la tabla hash.

Las tres imprimen `unicos=3`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `set(x)` (Python), `new Set` (JS), `HashSet` (Java/Rust/C#). |
| Semántica | El conjunto no garantiza orden; C lo simula con un bucle. |
| Paradigmática | SQL usa `COUNT(DISTINCT x)`. |

La diferencia de fondo es **quién trae el conjunto de serie y quién lo emula**. Python (`set`), Java y C# (`HashSet`), JavaScript (`Set`) y Rust (`HashSet`) tienen una estructura conjunto nativa respaldada por tabla hash, con pertenencia O(1) promedio. Go no tiene tipo conjunto y usa el modismo `map[T]struct{}`, aprovechando que las claves de un mapa ya son únicas. C no tiene nada: hay que construir la deduplicación a mano, y la versión mostrada lo hace en O(n²), el coste que precisamente pagaríamos si ignoráramos la tabla hash. SQL resuelve la misma pregunta con `COUNT(DISTINCT x)`, que el motor implementa por debajo con hash o con ordenación. En cuanto al **orden de iteración**, ninguna de estas estructuras lo garantiza —Rust incluso aleatoriza el hash entre ejecuciones para evitar ataques de colisión—, por lo que aquí solo contamos el *tamaño*, un valor que no depende del orden; si necesitáramos listar los únicos en orden estable habría que ordenarlos aparte o usar variantes como `LinkedHashSet` (Java) o `BTreeSet` (Rust).

## 🧬 El concepto en la familia

La constante entre lenguajes es que el conjunto es una tabla hash sin valores, y de ahí nacen dos parientes cercanos. Por un lado, el **conjunto ordenado**: `TreeSet` en Java, `SortedSet` en C#, `BTreeSet` en Rust, `std::set` en C++, todos respaldados por un árbol balanceado que cambia el O(1) del hash por un O(log n) que, a cambio, mantiene los elementos ordenados. Por otro, el **conjunto que preserva orden de inserción**, como `LinkedHashSet` en Java. En Ruby basta `lista.uniq.size` para contar distintos, y en Go el modismo `map[int]struct{}` es tan común que funciona como conjunto de facto. Reconocer que «conjunto» casi siempre significa «tabla hash de claves» —y que existe la variante ordenada cuando el orden importa— es la clave para elegir bien entre velocidad de pertenencia y orden garantizado.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 094
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden en un conjunto** → causa: iterar un `HashSet`/`set` esperando los elementos ordenados o en orden de inserción; el hash los coloca según su valor de dispersión → solución: si necesitas orden, ordena al volcar a una lista o usa una variante ordenada (`TreeSet`, `BTreeSet`).
- **Contar únicos con bucles O(n²) sin necesidad** → causa: comprobar «¿ya lo vi?» recorriendo lo acumulado, como en la versión C → solución: usar un conjunto con pertenencia O(1) promedio, que colapsa el coste a O(n).
- **Meter elementos no hashables** → causa: usar como elemento algo mutable o sin función hash estable (una lista en Python, un tipo sin `Hash`/`Eq` en Rust) → solución: usar valores inmutables/hashables (tuplas, cadenas, números) como elementos.
- **Confundir cantidad de únicos con cantidad total** → causa: creer que el tamaño del conjunto es la longitud de la entrada → solución: recordar que los duplicados se absorben; el tamaño del conjunto es siempre ≤ la cantidad leída.

## ❓ Preguntas frecuentes

- **¿El conjunto conserva el orden?** En general no. La tabla hash coloca cada elemento según su hash, no según cuándo lo insertaste, y algunos lenguajes incluso aleatorizan ese orden entre ejecuciones. Si necesitas orden, usa una variante ordenada (`TreeSet` en Java, `BTreeSet` en Rust) o vuelca a una lista y ordénala.
- **¿Por qué la pertenencia es O(1) y no O(n)?** Porque la función hash convierte el elemento directamente en la posición del cubo donde debería estar (Cormen, cap. 11): en vez de recorrer la colección comparando, se hace un único cálculo y una comprobación local. El «promedio» es la salvedad: con muchas colisiones el peor caso sube a O(n), pero con hashes decentes es despreciable.
- **¿Conjunto o lista?** Conjunto cuando te importan la unicidad y la pertenencia rápida, y el orden no. Lista cuando el orden y las repeticiones son significativos, o cuando necesitas acceso por índice.
- **¿Cómo se hacen unión, intersección y diferencia?** Son operaciones nativas del conjunto: Python usa `a | b`, `a & b`, `a - b`; Java tiene `addAll`, `retainAll`, `removeAll`. Todas se apoyan en la pertenencia O(1) para recorrer un conjunto probando cada elemento contra el otro.

## 🔗 Referencias

**Libros de la parte:**

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).
- R. Sedgewick y K. Wayne — *Algorithms* (4ª ed., Addison-Wesley).

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

> [⏮️ Clase 093](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 095 ⏭️](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md)
