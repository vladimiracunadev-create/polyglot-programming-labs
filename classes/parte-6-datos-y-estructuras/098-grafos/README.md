# Clase 098 — Grafos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **grafo** como la estructura más general de todas: un conjunto de **vértices** (nodos) y **aristas** (conexiones entre pares de vértices) que modela cualquier relación entre entidades. Donde el árbol imponía una jerarquía sin ciclos, el grafo lo permite todo —ciclos, múltiples caminos, vértices aislados—, y esa libertad es justo lo que lo hace capaz de representar redes sociales, mapas de carreteras, dependencias entre paquetes o el flujo de un programa. Cormen dedica los capítulos 20 a 22 de *Introduction to Algorithms* a los grafos, y lo primero que establece es que un grafo no tiene *una* representación sino dos rivales: la **lista de adyacencia**, que guarda para cada vértice sus vecinos (memoria O(V+E), buena para grafos *dispersos*), y la **matriz de adyacencia**, una tabla V×V de ceros y unos (memoria O(V²), buena para grafos *densos* y para preguntar en O(1) si dos vértices están conectados). Sobre esa representación se montan los recorridos que dan sentido a un grafo. El objetivo de hoy es medir el tamaño de un grafo dado por su lista de aristas —contar aristas y vértices distintos—, que es el primer paso obligado antes de recorrerlo o analizarlo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar un grafo por sus aristas.
2. Contar aristas y nodos distintos.
3. Reconocer dónde aparecen los grafos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Grafo | Nodos y aristas |
| 2 | Arista | Conexión entre dos nodos |
| 3 | Nodos distintos | El conjunto de vértices |

## 📖 Definiciones y características

- **Grafo** — par G = (V, E) formado por un conjunto de vértices V y un conjunto de aristas E ⊆ V×V. Es la estructura de relación más general: cualquier árbol es un grafo (uno conexo y sin ciclos), pero no todo grafo es un árbol. Un grafo puede ser **dirigido** —las aristas tienen sentido, como los enlaces de la web o «A depende de B»— o **no dirigido** —la conexión es mutua, como una amistad—, y **ponderado** si cada arista lleva un peso (distancia, coste) o no. Cormen (cap. 20) construye toda la teoría sobre estas cuatro combinaciones.
- **Arista (edge)** — conexión entre dos vértices. En un grafo no dirigido `{1,2}` y `{2,1}` son la misma arista; en uno dirigido, `(1,2)` y `(2,1)` son distintas. En el problema de hoy cada arista se codifica como un par consecutivo de números en la entrada, así que el número de aristas es simplemente la cantidad de tokens dividida entre dos.
- **Vértice (nodo)** — cada entidad del grafo. El número de vértices distintos mide el «tamaño» del conjunto V y no coincide con el número de números de la entrada: si un vértice aparece en varias aristas, se cuenta una sola vez. De ahí que contarlos requiera un **conjunto** que descarte repeticiones, lo que se hace en O(V+E) con una tabla hash o en O(n²) comparando ingenuamente cada elemento con los anteriores.
- **Representación** — la lista de adyacencia usa O(V+E) memoria y recorrer los vecinos de un vértice es proporcional a su *grado*; la matriz de adyacencia usa O(V²) pero responde «¿hay arista entre u y v?» en O(1). La elección depende de la densidad del grafo y de qué preguntas se harán con más frecuencia.

## 🧩 Situación

Casi todo lo interconectado es un grafo: los amigos de una red social (vértices personas, aristas amistades), un mapa de carreteras (vértices ciudades, aristas rutas con su distancia como peso), las dependencias de un proyecto de software (vértices paquetes, aristas dirigidas «necesita a»), o las páginas web y sus enlaces. Antes de calcular el camino más corto, detectar comunidades o resolver un orden de compilación, hace falta lo más elemental: saber **cuántos vértices y cuántas aristas** tiene el grafo, porque de esa medida depende qué representación conviene y cuánto costará cada algoritmo. El problema de hoy hace exactamente eso: recibe una lista de aristas (pares de enteros), cuenta las aristas dividiendo los tokens entre dos y cuenta los vértices distintos metiéndolos en un conjunto. Es la radiografía de tamaño que precede a cualquier análisis serio del grafo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con pares de enteros (cada par es una arista)
- **Salida** (stdout): `aristas=<número de pares> nodos=<nodos distintos>`
- **Regla:** aristas = tokens/2 ; nodos = |conjunto de todos los números|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3` | `aristas=2 nodos=3` |
| `1 2` | `aristas=1 nodos=2` |
| `1 2 2 3 3 1` | `aristas=3 nodos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER pares ; aristas <- pares ; nodos <- distintos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
aristas = len(nums) // 2
nodos = len(set(nums))
print(f"aristas={aristas} nodos={nodos}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
```

### Java · `java Main.java`

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
        Set<Integer> nodos = new HashSet<>();
        for (String s : p) nodos.add(Integer.parseInt(s));
        System.out.println("aristas=" + (p.length / 2) + " nodos=" + nodos.size());
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int aristas = p.Length / 2;
int nodos = p.Select(int.Parse).Distinct().Count();
Console.WriteLine($"aristas={aristas} nodos={nodos}");
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
	set := make(map[int]struct{})
	for _, s := range f {
		n, _ := strconv.Atoi(s)
		set[n] = struct{}{}
	}
	fmt.Printf("aristas=%d nodos=%d\n", len(f)/2, len(set))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let aristas = nums.len() / 2;
    let nodos: HashSet<i64> = nums.iter().copied().collect();
    println!("aristas={} nodos={}", aristas, nodos.len());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[2048];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int nodos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) nodos++;
    }
    printf("aristas=%d nodos=%d\n", n / 2, nodos);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: aristas = filas de pares; nodos = valores distintos.
WITH nums(x) AS (VALUES (1), (2), (2), (3))
SELECT printf('aristas=%d nodos=%d', count(*) / 2, count(DISTINCT x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$aristas = intdiv(count($nums), 2);
$nodos = count(array_unique($nums));
echo "aristas=$aristas nodos=$nodos\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 2 3`, que debe producir `aristas=2 nodos=3`. La entrada codifica dos aristas: `(1,2)` y `(2,3)`. Hay cuatro números pero solo tres vértices distintos —1, 2 y 3—, porque el vértice 2 participa en ambas aristas. El programa debe capturar esas dos cuentas: aristas = tokens/2, y vértices = tamaño del conjunto de valores.

En **Python**, `sys.stdin.read().split()` da `[1, 2, 2, 3]`. `aristas = len(nums) // 2` calcula 4//2 = 2. La clave está en `nodos = len(set(nums))`: `set([1, 2, 2, 3])` colapsa los duplicados a `{1, 2, 3}` y `len` devuelve 3. El conjunto hace el trabajo de deduplicar en O(n) promedio gracias a la tabla hash que lo respalda. Salida: `aristas=2 nodos=3`.

En **Go**, no hay un tipo *set* nativo, así que se emula con un mapa cuyo valor es el tipo vacío: `set := make(map[int]struct{})`. Para cada token se hace `set[n] = struct{}{}` —insertar la clave `n` con un valor que no ocupa memoria—. Insertar la misma clave dos veces no añade una segunda entrada, de modo que tras procesar `1 2 2 3` el mapa tiene tres claves y `len(set)` es 3. El truco `struct{}{}` es el modismo idiomático de Go para «solo me importa la clave, no el valor». `len(f)/2` da las 2 aristas.

En **C**, no hay conjunto ni mapa en la biblioteca estándar, así que la deduplicación es explícita y cuadrática: `long v[2048]` guarda los tokens y, para cada `v[i]`, un bucle interno `for (int j = 0; j < i; j++)` comprueba si ya apareció antes. Si no está repetido, `nodos++`. Con `[1, 2, 2, 3]`: el 1 es nuevo (nodos=1), el 2 es nuevo (nodos=2), el segundo 2 encuentra su gemelo y no cuenta, el 3 es nuevo (nodos=3). Es O(n²) frente al O(n) de un conjunto hash —el precio de no tener la estructura en el lenguaje—. `n / 2` da 2 aristas. Salida idéntica: `aristas=2 nodos=3`.

Las diez implementaciones producen `aristas=2 nodos=3` y el verificador lo comprueba contra `casos.json`. Nótese que en el caso `1 2 2 3 3 1` hay tres aristas que forman un triángulo (un ciclo) sobre tres vértices: `aristas=3 nodos=3`, señal de que este grafo tiene un ciclo, algo imposible en un árbol.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Conjunto de nodos + conteo de pares en cada lenguaje. |
| Semántica | El grafo puede guardarse como lista de aristas o de adyacencia. |
| Paradigmática | SQL modela grafos con tablas de nodos y aristas (relaciones). |

La diferencia más reveladora entre los diez lenguajes es cómo cada uno resuelve «cuenta los valores distintos», porque ahí se ve qué **colección de conjunto** ofrece de fábrica y a qué coste. Python (`set`), JavaScript/TypeScript (`Set`), Java (`HashSet`), C# (`Distinct`), Rust (`HashSet`) y PHP (`array_unique`) tienen deduplicación en O(n) promedio respaldada por hash; Go carece de un `set` nativo y usa el modismo `map[int]struct{}`; y C, sin ninguna estructura asociativa en su biblioteca, cae en el bucle anidado O(n²). Esa brecha —O(n) contra O(n²)— es imperceptible con cuatro números pero decisiva con un grafo de millones de aristas, y es exactamente el tipo de decisión que separa un programa que escala de uno que no. Un segundo contraste es de **modelo de datos**: SQL no piensa en conjuntos en memoria sino en tablas, y expresa la misma pregunta como `count(DISTINCT x)` sobre filas —un grafo en una base de datos suele ser dos tablas, una de nodos y otra de aristas, y las consultas de recorrido se escriben como *joins* recursivos.

## 🧬 El concepto en la familia

Contar es solo el umbral; la representación que se elija determina qué se puede hacer después con el grafo. La forma idiomática en casi todos los lenguajes es la **lista de adyacencia** como un mapa `vértice → lista de vecinos`: `dict` de listas en Python, `HashMap<i32, Vec<i32>>` en Rust, `map[int][]int` en Go, `Map<number, number[]>` en JavaScript. Sobre esa estructura viven los dos recorridos fundamentales que Cormen desarrolla en los capítulos 20-22. El **BFS** (recorrido en anchura) usa una **cola** —la estructura de la clase 096— para visitar el grafo por niveles, y entrega el camino más corto en número de aristas desde el origen. El **DFS** (recorrido en profundidad) usa una **pila** (explícita, o la implícita de la recursión) para hundirse por una rama hasta el fondo antes de retroceder, y es la base de la detección de ciclos y del orden topológico. Que un mismo grafo se recorra con una cola o con una pila, y que eso cambie por completo el orden de visita y lo que se descubre, cierra el arco de esta parte del curso: las estructuras de datos no son cajas para guardar, sino decisiones que moldean lo que un algoritmo puede ver.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 098
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar nodos con repetición** → causa: sobreestimar los vértices → solución: usar un conjunto de nodos distintos
- **Suponer número impar de tokens** → causa: arista incompleta → solución: asumir pares completos (grafo bien formado)

## ❓ Preguntas frecuentes

- **¿Lista de aristas o adyacencia?** Aristas es simple para contar; adyacencia es mejor para recorrer vecinos.
- **¿Dirigido o no?** Aquí solo contamos; la dirección importaría para recorridos.

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

> [⏮️ Clase 097](../../parte-6-datos-y-estructuras/097-arboles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 099 ⏭️](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md)
