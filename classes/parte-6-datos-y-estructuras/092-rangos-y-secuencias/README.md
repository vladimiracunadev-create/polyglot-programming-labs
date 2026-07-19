# Clase 092 — Rangos y secuencias

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **rango** como una representación **perezosa** (*lazy*) de una secuencia: un objeto que *describe* «todos los enteros de a hasta b» sin materializarlos en memoria, generándolos uno a uno solo cuando el bucle los pide. La idea potente es económica: un `range(0, 1_000_000)` en Python no ocupa un millón de celdas, ocupa un puñado de enteros —inicio, fin, paso— y produce cada valor bajo demanda. Su coste en memoria es O(1) aunque abarque millones de elementos; recorrerlo entero es O(n) en tiempo, pero sin la penalización de reservar ni copiar una lista gigante. El segundo eje conceptual es la **convención del intervalo**: casi todos los lenguajes eligen el **semiabierto** `[inicio, fin)` —incluye el primer extremo, excluye el segundo—, y no por capricho. Dijkstra argumentó, en su célebre nota EWD831, que esta convención minimiza los errores *off-by-one*: la longitud del rango es exactamente `fin − inicio`, dos rangos adyacentes encajan sin solaparse ni dejar hueco (`[a,b)` y `[b,c)`), y nunca hace falta el incómodo `≤` que obliga a pensar en el «último más uno». El objetivo de la clase es distinguir la secuencia **perezosa** (el `range` de Python, el `Range` de Rust, un generador) de la **materializada** (una lista de verdad), y saber cuándo cada una conviene.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar un rango inclusivo.
2. Sumar los valores del rango.
3. Reconocer rangos inclusivos vs. exclusivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Rango | Serie de valores consecutivos |
| 2 | Inclusivo/exclusivo | Si incluye el extremo |
| 3 | Secuencia perezosa | No se materializa entera |

## 📖 Definiciones y características

- **Rango** — objeto que describe un intervalo de valores consecutivos (`2..5`, `range(2, 6)`) sin enumerarlos. Guarda inicio, fin y paso, y **genera** cada valor cuando se le pide: su huella en memoria es O(1) sin importar cuán ancho sea el intervalo. Recorrerlo cuesta O(n) en tiempo, uno por cada valor visitado.
- **Intervalo semiabierto vs. cerrado** — `[inicio, fin)` (semiabierto, el más común: Python `range`, Rust `..`, los índices de casi todo) incluye el inicio y **excluye** el fin, de modo que su longitud es exactamente `fin − inicio`. `[inicio, fin]` (cerrado o inclusivo: Rust `..=`, Ruby `..`, la salida de esta clase) incluye ambos extremos. Dijkstra defendió el semiabierto (EWD831) porque evita errores off-by-one y hace que rangos contiguos encajen sin solaparse.
- **Secuencia perezosa vs. materializada** — la *perezosa* produce sus elementos bajo demanda y no los guarda (el `range` de Python, un generador, un iterador de Rust): O(1) en memoria. La *materializada* es una lista real con todos los valores en celdas contiguas: O(n) en memoria, a cambio de poder indexar, medir su longitud o recorrerla varias veces. Convertir una en otra (`list(range(...))`, `.collect()`) es el puente entre ambas.

## 🧩 Situación

Necesitas recorrer las posiciones de un arreglo, repetir una acción cien veces o sumar los enteros de un intervalo. Materializar una lista `[0, 1, 2, ..., 99]` solo para recorrerla y descartarla sería un desperdicio de memoria y de tiempo de asignación, sobre todo si el intervalo abarca millones. El rango perezoso es la respuesta idiomática: `for i in range(100)` o `for i in 1..=100` recorre los valores sin construir la lista, produciéndolos al vuelo. El problema de hoy —leer `a` y `b`, emitir el intervalo cerrado `[a..b]` unido por guiones y su suma— es pequeño a propósito, pero pone el foco en la decisión clave: generar bajo demanda frente a materializar, y respetar el extremo correcto.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros, a <= b)
- **Salida** (stdout): `rango=<a-...-b> suma=<suma del rango>`
- **Regla:** rango [a..b] y su suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 5` | `rango=2-3-4-5 suma=14` |
| `1 1` | `rango=1 suma=1` |
| `3 6` | `rango=3-4-5-6 suma=18` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; generar a..b ; sumar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
r = list(range(a, b + 1))
print(f"rango={'-'.join(str(x) for x in r)} suma={sum(r)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r: number[] = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        StringBuilder sb = new StringBuilder();
        long suma = 0;
        for (int i = a; i <= b; i++) {
            if (i > a) sb.append("-");
            sb.append(i);
            suma += i;
        }
        System.out.println("rango=" + sb + " suma=" + suma);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var r = Enumerable.Range(a, b - a + 1).ToList();
Console.WriteLine($"rango={string.Join("-", r)} suma={r.Sum()}");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	var parts []string
	suma := 0
	for i := a; i <= b; i++ {
		parts = append(parts, strconv.Itoa(i))
		suma += i
	}
	fmt.Printf("rango=%s suma=%d\n", strings.Join(parts, "-"), suma)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let r: Vec<i64> = (v[0]..=v[1]).collect();
    let suma: i64 = r.iter().sum();
    let texto: Vec<String> = r.iter().map(|x| x.to_string()).collect();
    println!("rango={} suma={}", texto.join("-"), suma);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long suma = 0;
    printf("rango=");
    for (long i = a; i <= b; i++) {
        if (i > a) printf("-");
        printf("%ld", i);
        suma += i;
    }
    printf(" suma=%ld\n", suma);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: rango con CTE recursivo (ilustrativo, 2..5).
WITH RECURSIVE r(i) AS (VALUES (2) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT 'rango=' || group_concat(i, '-') || printf(' suma=%d', sum(i)) AS resultado FROM r;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = range((int) $a, (int) $b);
echo "rango=" . implode("-", $r) . " suma=" . array_sum($r) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `2 5`, que debe producir `rango=2-3-4-5 suma=14`. La salida abarca el intervalo **cerrado** `[2..5]` —los cuatro valores 2, 3, 4, 5— y su suma. Cada lenguaje expresa ese «cerrado» de forma distinta, y ahí está la lección.

En **Python**, `range` es semiabierto por diseño: `range(a, b)` excluye `b`. Para obtener un rango **cerrado** hay que sumar uno al fin: `range(a, b + 1)`, es decir `range(2, 6)`, que produce 2, 3, 4, 5. Ese `+1` es el precio de traducir la convención semiabierta del lenguaje a la salida inclusiva del ejercicio. El objeto `range(2, 6)` es perezoso, pero `list(range(...))` lo **materializa** aquí porque el código lo recorre dos veces (para unir con guiones y para sumar); si solo se recorriera una vez, se podría dejar perezoso. `sum(r)` da 14 y el f-string arma la salida.

En **Rust**, el lenguaje distingue las dos convenciones en la propia sintaxis: `v[0]..v[1]` es semiabierto y `v[0]..=v[1]` es **inclusivo**. El ejemplo usa `(v[0]..=v[1])`, o sea `2..=5`, que ya incluye el 5 sin ningún `+1` —la intención se lee directamente en el operador—. `.collect()` materializa el `Range` perezoso en un `Vec<i64>` porque, igual que en Python, hace falta recorrerlo dos veces; `.iter().sum()` da 14. Es el mismo resultado, pero Rust hace explícita en el tipo la diferencia que Python resuelve con aritmética.

En **Go**, no existe ningún tipo «rango»: la palabra `range` de Go sirve para iterar colecciones ya existentes, no para generar intervalos. Por eso el ejemplo vuelve al bucle C clásico `for i := a; i <= b; i++`, con `<= b` haciéndolo inclusivo a mano. No hay pereza ni materialización de un objeto rango: los valores se generan en el propio bucle y se van acumulando en `parts` y en `suma`. Es la forma más explícita de todas —ningún azúcar sintáctico— y produce igualmente `rango=2-3-4-5 suma=14`.

Los tres imprimen `rango=2-3-4-5 suma=14`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `range(a, b+1)` (Python), `a..=b` (Rust), bucle (C/Java/Go). |
| Semántica | Python `range` es exclusivo del final; Rust distingue `..` y `..=`. |
| Paradigmática | SQL genera rangos con CTE recursivo. |

El eje decisivo es **perezoso vs. materializado, y qué convención de extremo asume cada lenguaje**. Python y Rust ofrecen un objeto rango perezoso de primera clase: `range(a, b)` y `a..b` no reservan memoria por sus valores, solo por sus límites; convertirlos en lista (`list(...)`, `.collect()`) es un paso explícito. C# tiene `Enumerable.Range(inicio, cantidad)` —ojo, su segundo argumento es la **cantidad** de elementos, no el fin, por eso el código calcula `b - a + 1`—, perezoso hasta que un `.ToList()` o un `.Sum()` lo consume. Go, C y Java no tienen tipo rango y usan el bucle explícito, generando cada valor sin objeto intermedio. En la **convención de extremo**, casi todos los rangos nativos son semiabiertos (`[a, b)`: Python, Rust `..`, los índices en general), fieles al argumento de Dijkstra; los inclusivos (`[a, b]`) requieren o un operador especial (Rust `..=`) o un `+1`/`<=` a mano. SQL, ajeno a todo esto, materializa el rango con un **CTE recursivo** que va emitiendo filas hasta la condición de corte —perezoso en espíritu (fila a fila) pero declarativo en forma—.

## 🧬 El concepto en la familia

La distinción entre describir una secuencia y materializarla reaparece por todas partes, y los lenguajes difieren sobre todo en el extremo que incluyen. En Ruby `(a..b)` es inclusivo y `(a...b)` exclusivo —tres puntos para excluir, una elección de sintaxis que hay que memorizar—. En Kotlin `a..b` es inclusivo y `a until b` exclusivo, con nombres que se leen como inglés. En Haskell `[a..b]` genera una lista perezosa inclusiva, y `[a..]` un rango **infinito** que solo funciona porque la evaluación perezosa nunca lo materializa entero: se toman los valores que hagan falta y no más. Esa es la generalización última del rango: un generador que puede describir incluso lo infinito porque no promete calcularlo todo, solo lo que se le pida. Python lleva la misma idea a sus generadores (`yield`) e *itertools*, y Rust a sus iteradores perezosos encadenables. Reconocer si tienes entre manos una secuencia perezosa o una lista ya materializada —y cuánto memoria implica cada una— es la lección transversal de la clase.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 092
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Error por el extremo (off-by-one)** → causa: olvidar que `range(a, b)` de Python excluye `b`, o que Rust `..` es semiabierto y `..=` inclusivo, y perder o duplicar el último valor → solución: tener presente la convención del lenguaje; para un intervalo cerrado en Python usa `range(a, b + 1)`, en Rust `a..=b`.
- **Confundir el segundo argumento de `Enumerable.Range`** → causa: en C# `Enumerable.Range(a, b)` toma `a` como inicio y `b` como **cantidad** de elementos, no como fin; pasar el fin genera un rango equivocado → solución: para el intervalo `[a, b]` usar `Enumerable.Range(a, b - a + 1)`.
- **Materializar rangos enormes sin necesidad** → causa: `list(range(10_000_000))` reserva millones de celdas cuando solo ibas a recorrerlas → solución: itera directamente sobre el rango perezoso; materializa solo si necesitas indexar, medir la longitud o recorrer varias veces.
- **Creer que el `range` de Go genera intervalos** → causa: la palabra clave `range` de Go itera colecciones existentes, no crea un intervalo numérico → solución: usa un bucle `for i := a; i <= b; i++` para generar el rango a mano.

## ❓ Preguntas frecuentes

- **¿Rango inclusivo o exclusivo?** Depende del lenguaje. La mayoría de los rangos nativos son semiabiertos `[a, b)` —Python `range`, Rust `..`— siguiendo el argumento de Dijkstra de que minimizan errores off-by-one; los inclusivos requieren un operador especial (Rust `..=`, Ruby `..`) o sumar uno al fin. Conoce la convención antes de escribir el bucle.
- **¿Por qué el semiabierto evita errores?** Porque la longitud del rango es exactamente `fin − inicio` (sin `+1` que recordar), y dos rangos adyacentes `[a, b)` y `[b, c)` encajan sin solaparse ni dejar hueco. Es más fácil razonar sobre índices así (Dijkstra, EWD831).
- **¿Un rango consume memoria?** En Python y Rust el objeto rango es perezoso: guarda inicio, fin y paso —O(1)— y genera cada valor bajo demanda, sin crear la lista completa. Solo al materializarlo (`list(range(...))`, `.collect()`) pagas O(n) en memoria.
- **¿Cuándo materializar y cuándo no?** Materializa si necesitas indexar posiciones concretas, conocer la longitud de antemano o recorrer la secuencia más de una vez (como hacen los ejemplos, que suman y unen). Déjalo perezoso si solo lo recorres una vez: ahorra memoria y evita una asignación.

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

> [⏮️ Clase 091](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 093 ⏭️](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md)
