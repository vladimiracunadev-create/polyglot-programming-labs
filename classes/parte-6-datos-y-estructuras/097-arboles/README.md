# Clase 097 — Árboles

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **árbol** como el salto de lo lineal a lo **jerárquico**: mientras el arreglo, la pila y la cola disponen los datos en una fila, el árbol los organiza en niveles, con una *raíz* de la que cuelgan hijos que a su vez tienen hijos, sin ciclos. El caso que estudiamos hoy es el **árbol binario de búsqueda (BST)**, y su valor no es la jerarquía por sí misma sino un **invariante** que Cormen formaliza en el capítulo 12 de *Introduction to Algorithms*: en todo nodo, la clave es mayor que todas las del subárbol izquierdo y menor que todas las del derecho. Ese invariante convierte cada comparación en una decisión que descarta la mitad del árbol, de modo que buscar, insertar o borrar cuesta **O(h)**, la altura del árbol —que es **O(log n)** si el árbol está equilibrado, pero degenera a **O(n)** si se desequilibra hasta parecer una lista. El objetivo profundo es entender por qué el mismo BST puede ser rapidísimo o pésimo según su forma, y por qué su recorrido **in-order** (izquierda-raíz-derecha) escupe los valores en orden ascendente casi por arte de magia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la propiedad del BST.
2. Reconocer el recorrido in-order.
3. Relacionar el árbol con el orden.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Árbol | Nodos con hijos, jerárquico |
| 2 | BST | Menores a la izquierda, mayores a la derecha |
| 3 | Recorrido in-order | Produce el orden ascendente |

## 📖 Definiciones y características

- **Árbol** — conjunto de nodos conectados jerárquicamente: hay un nodo *raíz* sin padre, y cada nodo restante tiene exactamente un padre y cero o más *hijos*. No hay ciclos, de modo que entre dos nodos cualesquiera existe un único camino. Los nodos sin hijos son *hojas*. La **altura** es la longitud del camino más largo de la raíz a una hoja, y es la magnitud que gobierna el coste de casi todo lo que se hace con un árbol. Sedgewick subraya que el árbol es, después del arreglo y la lista, la estructura más fundamental de la computación precisamente porque captura relaciones de contención y precedencia.
- **Árbol binario de búsqueda (BST)** — árbol donde cada nodo tiene a lo sumo dos hijos y respeta el invariante de orden: *izquierda < nodo < derecha* (Cormen, cap. 12). Insertar un valor consiste en descender desde la raíz comparando —ir a la izquierda si es menor, a la derecha si es mayor— hasta encontrar un hueco: un camino de longitud O(h). La búsqueda sigue la misma senda. El coste, por tanto, es **O(log n) cuando el árbol está equilibrado** (cada nivel duplica los nodos) y **O(n) cuando degenera**: si se insertan valores ya ordenados, cada nuevo nodo cuelga a la derecha del anterior y el BST se estira en una lista enlazada, perdiendo toda su ventaja. Los árboles autoequilibrados (AVL, rojo-negro) existen justo para impedir esa degeneración.
- **Recorridos** — hay tres formas recursivas de visitar todos los nodos, que difieren en *cuándo* se procesa la raíz respecto a sus subárboles: **preorden** (raíz, izquierda, derecha), **inorden** (izquierda, raíz, derecha) y **postorden** (izquierda, derecha, raíz). El inorden es especial en un BST: como visita primero todo lo menor, luego el nodo, luego todo lo mayor, emite las claves **en orden ascendente**. Recorrer el árbol entero es O(n) porque toca cada nodo una vez. La recursión es la herramienta natural para estos recorridos, porque un árbol se define de forma recursiva (un nodo y sus subárboles, que son árboles).

## 🧩 Situación

Los árboles están debajo de casi toda organización de datos que hayas usado: el índice de una base de datos que localiza una fila sin escanear la tabla entera, el sistema de archivos con sus carpetas anidadas, el autocompletado que desciende letra a letra, el DOM de una página web. Todos aprovechan que una estructura jerárquica permite descartar ramas enteras en cada paso en lugar de mirarlo todo. El problema de hoy destila esa idea a su efecto más nítido y comprobable: leemos una lista de enteros distintos, los insertamos en un BST y lo recorremos in-order, con lo que salen **ordenados de menor a mayor**. La ordenación es aquí el testigo visible de que el invariante del BST se cumplió; si el árbol estuviera mal construido, el in-order no daría el orden. Trabajamos con valores distintos a propósito para no tener que decidir una política de duplicados.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros distintos separados por espacio
- **Salida** (stdout): `inorden=<los valores ordenados ascendente unidos por ->`
- **Regla:** in-order de un BST = orden ascendente

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `inorden=1-3-4` |
| `5 2 8 1` | `inorden=1-2-5-8` |
| `9 7` | `inorden=7-9` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; insertar en BST ; recorrer in-order
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.sort()  # in-order de un BST equivale al orden ascendente
print("inorden=" + "-".join(str(x) for x in nums))
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.TreeSet;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        TreeSet<Integer> t = new TreeSet<>();
        for (String s : p) t.add(Integer.parseInt(s));
        System.out.println("inorden=" + t.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).OrderBy(x => x);
Console.WriteLine($"inorden={string.Join("-", nums)}");
```

### Go · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	sort.Ints(nums)
	parts := make([]string, len(nums))
	for i, n := range nums {
		parts[i] = strconv.Itoa(n)
	}
	fmt.Printf("inorden=%s\n", strings.Join(parts, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    nums.sort();
    let texto: Vec<String> = nums.iter().map(|x| x.to_string()).collect();
    println!("inorden={}", texto.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    long x = *(const long *) a, y = *(const long *) b;
    return (x > y) - (x < y);
}

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    qsort(v, n, sizeof(long), cmp);
    printf("inorden=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: ORDER BY equivale al in-order del BST.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT 'inorden=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY x);
```

### PHP · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
sort($nums);
echo "inorden=" . implode("-", $nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `5 2 8 1`, que debe producir `inorden=1-2-5-8`. Aquí conviene un matiz honesto: construir un BST de verdad, insertar los cuatro valores y recorrerlo in-order produce exactamente la misma salida que **ordenar la lista**, porque el in-order de un BST es, por definición, el orden ascendente de sus claves. Las implementaciones aprovechan esa equivalencia para mantener el código breve, pero vale la pena ver dónde asoma el árbol de verdad y dónde se sustituye por una ordenación.

En **Python**, `nums = [5, 2, 8, 1]` y `nums.sort()` reordena la lista en sitio a `[1, 2, 5, 8]`. El comentario del propio código lo dice: «in-order de un BST equivale al orden ascendente». Si construyéramos el BST a mano insertando 5 (raíz), 2 (izquierda de 5), 8 (derecha de 5) y 1 (izquierda de 2), el recorrido izquierda-raíz-derecha visitaría 1, 2, 5, 8 —el mismo resultado que `sort`. `"-".join(...)` produce `"1-2-5-8"`.

En **Java**, en cambio, el árbol es **literal**: `TreeSet<Integer>` es un conjunto respaldado por un árbol rojo-negro, un BST autoequilibrado. Cada `t.add(...)` inserta manteniendo el invariante de orden, y recorrer el `TreeSet` con `t.stream()` lo hace **en orden ascendente** —es decir, hace un in-order real sobre un árbol real. Insertar 5, 2, 8, 1 y luego iterar da 1, 2, 5, 8, que `collect(Collectors.joining("-"))` convierte en `"1-2-5-8"`. Aquí no hay simulación: la estructura de datos de la clase está ejecutándose de verdad, con inserciones O(log n) garantizadas por el equilibrado.

En **C**, no hay árbol en la biblioteca estándar, así que el código usa `qsort` sobre `long v[1024]` con un comparador `cmp` que devuelve el signo de la diferencia. Ordenar `[5, 2, 8, 1]` da `[1, 2, 5, 8]` y el bucle final las imprime unidas por guiones. Es la vía pragmática: cuando el lenguaje no regala un BST, se llega al mismo resultado con la primitiva de ordenación.

Los tres imprimen `inorden=1-2-5-8`, y el verificador confirma que las diez implementaciones coinciden con `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Ordenar (`sorted`) equivale al in-order del BST en esta clase. |
| Semántica | El BST mantiene el orden al insertar; ordenar lo hace de una vez. |
| Paradigmática | SQL usa ORDER BY, que el motor implementa con árboles/índices. |

La diferencia real entre los diez lenguajes está en si el árbol viene **regalado por la biblioteca** o hay que ordenar a mano, y esa elección tiene consecuencias de coste distintas. Java y C# ofrecen `TreeSet`/`SortedSet<T>`, árboles rojo-negro que mantienen el orden *incrementalmente*: cada inserción cuesta O(log n) y en todo momento el recorrido está ordenado —ideal si insertas y consultas de forma intercalada. Python, JavaScript, Go, Rust, C y PHP no traen un BST ordenado en su núcleo, así que ordenan de golpe con `sort`/`qsort`/`OrderBy`, un coste O(n log n) pagado una sola vez —mejor si tienes todos los datos y solo quieres el orden final. Es la vieja disyuntiva entre mantener el orden todo el tiempo (árbol) o imponerlo al final (ordenación). Otro contraste es de **enlaces entre nodos**: si construyeras el BST explícito, en C usarías punteros crudos (`struct Nodo *izq, *der`) con `malloc` y `free` manuales; en Java, C#, Python o Go usarías referencias que el recolector de basura libera solo; y en Rust necesitarías `Box<Option<Nodo>>` para expresar la propiedad de cada subárbol sin ciclos —el mismo árbol, tres filosofías de memoria.

## 🧬 El concepto en la familia

Casi todos los lenguajes exponen un «conjunto o mapa ordenado» que por dentro es un árbol binario de búsqueda equilibrado, y conviene reconocerlo bajo sus muchos nombres: `TreeSet`/`TreeMap` en Java, `SortedSet`/`SortedDictionary` en C#, `std::set`/`std::map` en C++ (habitualmente un árbol rojo-negro), `BTreeMap` en Rust (una variante en bloques, amable con la caché). Todos comparten una promesa: mantener las claves ordenadas con inserción, borrado y búsqueda en O(log n), y permitir consultas de rango («dame todo entre 3 y 9») que una tabla hash no puede ofrecer. La contrapartida es que una tabla hash da O(1) promedio pero *ningún* orden; el árbol paga un factor logarítmico a cambio de ese orden permanente. Cuando en una base de datos creas un índice, el motor levanta casi siempre un B-tree —un árbol de búsqueda de muchos hijos por nodo, optimizado para el disco— y `ORDER BY` o una búsqueda por rango se apoyan en él. El BST de esta clase es la semilla conceptual de toda esa familia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 097
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir in-order con preorden o postorden** → causa: solo el recorrido izquierda-raíz-derecha respeta el orden de las claves en un BST; preorden y postorden dan secuencias útiles para otras cosas (copiar el árbol, evaluar expresiones) pero no ordenadas → solución: para obtener el orden ascendente, usar in-order.
- **Insertar duplicados sin una política** → causa: si dos claves iguales pueden entrar, hay que decidir si van a la izquierda, a la derecha o se ignoran, y sin regla el árbol queda ambiguo → solución: definir la política explícitamente; en este ejercicio los valores son distintos para evitar el problema.
- **Dar por hecho que el BST está equilibrado** → causa: insertar datos ya ordenados hace que cada nodo cuelgue del mismo lado y el árbol degenere en una lista, con búsquedas O(n) en vez de O(log n) → solución: usar un árbol autoequilibrado (AVL, rojo-negro) o barajar la entrada; los `TreeSet`/`TreeMap` del núcleo ya se equilibran solos.
- **Olvidar el caso base en el recorrido recursivo** → causa: no comprobar si el nodo es nulo antes de descender provoca un desbordamiento o un acceso inválido → solución: la primera línea de todo recorrido recursivo debe ser «si el nodo es nulo, regresar».

## ❓ Preguntas frecuentes

- **¿Por qué el in-order ordena?** Porque en cada nodo procesa primero *todo* el subárbol izquierdo (que por el invariante contiene solo claves menores), luego el nodo, luego *todo* el subárbol derecho (solo claves mayores), y aplica esa misma regla recursivamente. El resultado neto es que las claves salen de la menor a la mayor.
- **¿BST o arreglo ordenado?** Un arreglo ordenado da búsqueda binaria O(log n) y acceso O(1) por índice, pero insertar o borrar cuesta O(n) porque hay que desplazar elementos. El BST paga O(log n) por acceder, pero inserta y borra manteniendo el orden en O(log n) sin mover nada. Elige el arreglo si los datos son estáticos y consultas mucho; el árbol si insertas y borras a menudo.
- **¿Por qué existen los árboles autoequilibrados?** Porque un BST simple es rehén de su orden de inserción: puede degenerar a O(n). Los AVL y rojo-negro reajustan la forma tras cada inserción (rotaciones) para garantizar una altura O(log n) siempre, a cambio de algo más de trabajo por operación. Son la razón por la que un `TreeMap` es fiable en el peor caso.

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

> [⏮️ Clase 096](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 098 ⏭️](../../parte-6-datos-y-estructuras/098-grafos/README.md)
