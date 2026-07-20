# Clase 090 — Listas, vectores y arreglos dinámicos

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **arreglo dinámico** —la estructura que se esconde bajo `list`, `Vec`, `ArrayList` o el `slice` de Go— no como «una lista que crece por arte de magia», sino como un arreglo contiguo de tamaño fijo envuelto en una capa de contabilidad. La idea central es distinguir dos números que suelen confundirse: la **longitud** (`len`, cuántos elementos hay de verdad) y la **capacidad** (`cap`, cuántos caben antes de tener que mudarse a un bloque mayor). Mientras quede capacidad libre, agregar al final es un simple `arr[len] = x; len++`, en tiempo constante. Cuando la capacidad se agota, la estructura reserva un bloque nuevo —típicamente el doble— y copia todo lo viejo, en O(n). El objetivo profundo de esta clase es entender por qué, pese a esas copias periódicas y caras, agregar al final sale **O(1) amortizado**: la duplicación geométrica reparte el coste de cada copia entre tantas inserciones baratas que el promedio queda constante. Cormen lo demuestra con el método contable y el potencial para tablas dinámicas (CLRS, §17.4) y Sedgewick lo llama «resizing arrays». Invertir la secuencia, el ejercicio de hoy, obliga a recorrerla entera (O(n)) y a decidir si mutamos en sitio o construimos una copia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir y recorrer una lista dinámica.
2. Invertir el orden de los elementos.
3. Distinguir lista dinámica de arreglo fijo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lista dinámica | Crece según haga falta |
| 2 | Invertir | Recorrer al revés |
| 3 | Redimensionar | Añadir/quitar elementos |

## 📖 Definiciones y características

- **Lista/vector dinámico** — arreglo contiguo cuyo tamaño puede crecer y encoger en tiempo de ejecución (`list` de Python, `Vec<T>` de Rust, `ArrayList` de Java, `List<T>` de C#, el `slice` de Go). Conserva la propiedad esencial del arreglo —acceso por índice en O(1), porque `arr[i]` sigue siendo `base + i × tamaño`— pero paga esa contigüidad con el coste de reubicarse cuando se llena. Recorrerlo entero cuesta O(n).
- **Longitud y capacidad** — `len` es cuántos elementos contiene; `cap` es cuántos caben en el bloque reservado antes de tener que crecer. Casi siempre `cap ≥ len`, y el hueco entre ambos es la reserva que hace baratos los próximos `append`. Sedgewick insiste en no confundirlos: la capacidad es un detalle de implementación, la longitud es lo que ve el usuario.
- **append / push** — añadir un elemento al final. Es la operación que define la estructura: **O(1) amortizado** gracias a la duplicación geométrica de la capacidad, aunque un `append` concreto —el que dispara el redimensionado— cueste O(n) al copiar todo el contenido a un bloque nuevo (CLRS, §17.4). Insertar o borrar en el **medio**, en cambio, es O(n) siempre, porque hay que desplazar todos los elementos posteriores.
- **Inversión** — producir la secuencia en orden contrario. Cuesta O(n) porque toca cada elemento una vez; puede hacerse *en sitio* intercambiando extremos hacia el centro (n/2 intercambios) o construyendo una secuencia nueva.

## 🧩 Situación

Piensa en las líneas que llegan de un archivo, las respuestas que teclea un usuario o los resultados que devuelve una consulta: cantidades que **no conoces de antemano**. Un arreglo fijo te obligaría a adivinar el tamaño máximo y a desperdiciar memoria «por si acaso», o a quedarte corto. El arreglo dinámico resuelve el dilema creciendo bajo demanda, y lo hace de forma económica precisamente porque no crece de a uno: duplica su capacidad, de modo que las mudanzas se vuelven cada vez más raras a medida que la estructura engorda. El problema de hoy —leer una lista de enteros y emitirla al revés unidos por guiones— es deliberadamente pequeño para que la atención caiga sobre la estructura: cómo se construye elemento a elemento con `append` y cómo se recorre para invertirla.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `invertido=<elementos en orden inverso unidos por ->`
- **Regla:** invertido = reverse(lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `invertido=3-2-1` |
| `5` | `invertido=5` |
| `10 20 30 40` | `invertido=40-30-20-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; invertir ; ESCRIBIR unidos por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
nums.reverse()
print("invertido=" + "-".join(str(x) for x in nums))
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> nums = new ArrayList<>();
        for (String s : p) nums.add(Integer.parseInt(s));
        Collections.reverse(nums);
        System.out.println("invertido=" + nums.stream().map(String::valueOf).collect(Collectors.joining("-")));
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
var nums = p.Select(int.Parse).Reverse();
Console.WriteLine($"invertido={string.Join("-", nums)}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	for i, j := 0, len(f)-1; i < j; i, j = i+1, j-1 {
		f[i], f[j] = f[j], f[i]
	}
	fmt.Printf("invertido=%s\n", strings.Join(f, "-"))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<&str> = s.split_whitespace().collect();
    nums.reverse();
    println!("invertido={}", nums.join("-"));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: invierte con ORDER BY sobre la posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'invertido=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY pos DESC);
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$nums = array_reverse($nums);
echo "invertido=" . implode("-", $nums) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 3`, que debe producir `invertido=3-2-1`. Todas las implementaciones construyen una secuencia dinámica, la invierten y unen sus elementos con guiones; conviene comparar tres que revelan modelos distintos de crecimiento y de mutación.

En **Python**, la comprensión `[int(x) for x in ...split()]` construye la lista incrementalmente: cada valor que aparece dispara un `append` interno, y CPython va duplicando la capacidad del bloque a medida que hace falta (empieza pequeño y crece por saltos, no de a uno). Con `[1, 2, 3]` en mano, `nums.reverse()` invierte **en sitio**: no crea una lista nueva, sino que intercambia el primero con el último y avanza hacia el centro —un solo intercambio para tres elementos, ya que el del medio se queda quieto—. Luego `"-".join(...)` recorre la lista ya invertida y produce `3-2-1`. La mutación en sitio es la razón de que `reverse()` no devuelva nada (retorna `None`): modifica el objeto original, como advierte Ramalho en *Fluent Python*.

En **Go**, el ejemplo evita construir enteros y trabaja directamente sobre `f`, el `slice` de cadenas que devuelve `strings.Fields`. Un `slice` es la trinidad puntero+`len`+`cap`: aquí no crece, solo se recorre. El bucle `for i, j := 0, len(f)-1; i < j; ...` es el patrón clásico de inversión en sitio con dos índices que convergen: intercambia `f[0]` con `f[2]` y se detiene cuando `i < j` deja de cumplirse, sin tocar el elemento central. Luego `strings.Join(f, "-")` produce `3-2-1`. Es el mismo algoritmo que el `reverse()` de Python, pero escrito a mano y visible.

En **C**, no hay lista dinámica en la biblioteca estándar, así que el ejemplo reserva un arreglo fijo generoso (`long v[1024]`) y lleva la longitud real en `n`, contándola mientras `scanf` devuelva 1. Aquí no se invierte la memoria: se **recorre al revés** con `for (int i = n - 1; i >= 0; i--)`, imprimiendo cada valor y anteponiendo un guion salvo en el primero. El resultado, `3-2-1`, es idéntico; la diferencia es que C te obliga a gestionar tú mismo la separación entre capacidad (1024) y longitud (`n`), justo la contabilidad que las listas dinámicas automatizan.

Los tres imprimen `invertido=3-2-1`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list[::-1]` (Python), `.reverse()` (JS/Rust), `Collections.reverse` (Java). |
| Semántica | Algunos invierten en sitio (mutando); otros crean una lista nueva. |
| Paradigmática | SQL invierte con ORDER BY descendente sobre una posición. |

Bajo la sintaxis se esconden decisiones de diseño muy distintas. En **valor vs. referencia**: el `slice` de Go, la `list` de Python, el `ArrayList` de Java y el `List<T>` de C# son referencias (o encabezados que apuntan a un arreglo compartido), de modo que invertir en sitio afecta a todo el que tenga esa misma referencia; el `Vec<T>` de Rust, en cambio, tiene un único dueño, y el sistema de préstamos impide que otro lo observe mientras lo mutas. En **colecciones nativas**: Python, JavaScript y PHP ofrecen la lista dinámica como el tipo secuencia por defecto —no hay arreglo fijo que valga—, mientras Go la separa deliberadamente del arreglo (`[]T` frente a `[N]T`) y C ni siquiera la incluye, obligando a `malloc`/`realloc` manuales. En **coste**: todas comparten el acceso O(1) por índice y la inversión O(n), pero difieren en el `append`: donde Python, Rust y Go crecen por duplicación geométrica (O(1) amortizado, CLRS §17.4), en C cada crecimiento manual con `realloc` puede o no copiar según haya hueco contiguo, y el programador carga con esa decisión.

## 🧬 El concepto en la familia

El par arreglo-fijo/arreglo-dinámico reaparece en casi todos los lenguajes, a veces con nombres que engañan. En Go, `[3]int` es un arreglo de valor que se copia entero al pasarlo, mientras `[]int` es un `slice` —una vista con `len` y `cap` sobre un arreglo subyacente— que `append` puede reasignar a otro bloque cuando se llena; confundirlos produce bugs sutiles cuando dos slices comparten el mismo arreglo. En Rust conviven `[i64; 3]` (fijo, en la pila) y `Vec<i64>` (dinámico, en el heap, con `capacity()` inspeccionable). En C++ están `std::array<T, N>` y `std::vector<T>`, este último la referencia canónica del arreglo dinámico. En Java el arreglo primitivo `int[]` es fijo y `ArrayList<Integer>` es el dinámico —con el coste extra del *boxing*—. Reconocer cuál tienes entre manos, y si su `len` es fijo o crece, es medio problema resuelto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 090
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir invertir en sitio con crear copia** → causa: llamar a un método mutador (`list.reverse()` en Python, `Collections.reverse` en Java) creyendo que devuelve una lista nueva, y modificar el original sin querer → solución: si necesitas conservar el original, usa una operación que devuelva copia (`reversed(lista)`, `lista[::-1]` en Python) o duplica antes de invertir.
- **Esperar que `reverse()` devuelva la lista** → causa: en Python `nums.reverse()` retorna `None`; escribir `x = nums.reverse()` deja `x` vacío → solución: invierte y luego usa `nums`, o usa `reversed()`/*slicing* si quieres una expresión que devuelva valor.
- **Bucle de intercambio mal cerrado** → causa: recorrer todo el arreglo intercambiando `arr[i]` con `arr[n-1-i]` invierte y vuelve a invertir, dejándolo igual → solución: intercambiar solo hasta la mitad (`i < j`, índices que convergen), como hace la versión de Go.
- **Asumir que `append` siempre es barato** → causa: creer que agregar al final nunca cuesta → solución: entender que es O(1) *amortizado*; el `append` que dispara el redimensionado copia todo en O(n), aunque el promedio siga siendo constante (CLRS §17.4).

## ❓ Preguntas frecuentes

- **¿Lista dinámica o arreglo fijo?** Lista si el tamaño cambia o no lo conoces de antemano; arreglo fijo si es constante y te importan la localidad de memoria y evitar el asignador (clase 089). La lista añade flexibilidad a cambio de una capa de contabilidad (`len`/`cap`) y de reubicaciones ocasionales.
- **¿Por qué `append` es O(1) si a veces copia todo?** Porque la capacidad se **duplica**, no se aumenta de a uno. Cada copia cara de n elementos viene precedida de n inserciones baratas que la «pagan» por adelantado; el análisis amortizado (método contable o del potencial, CLRS §17.4) reparte el coste y da un promedio constante por operación.
- **¿Invertir es caro?** Es O(n): hay que tocar cada elemento una vez, sea intercambiando extremos en sitio (n/2 intercambios) o construyendo una copia. No hay forma de invertir sin visitar todo.
- **¿Qué diferencia hay entre `len` y `cap`?** `len` es cuántos elementos usas; `cap` cuántos caben antes de crecer. En Go puedes ver ambos con `len(s)` y `cap(s)`; en Rust, con `.len()` y `.capacity()`. Python oculta la capacidad, pero existe igual bajo el capó.

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

> [⏮️ Clase 089](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 091 ⏭️](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md)
