# Clase 096 — Pilas y colas

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender la **pila** y la **cola** no como dos colecciones más, sino como dos **disciplinas de acceso**: estructuras que deliberadamente *restringen* dónde se puede insertar y de dónde se puede sacar, y que reciben algo valioso a cambio de esa renuncia. La pila es LIFO —*last in, first out*, el último que entra es el primero que sale— y la cola es FIFO —*first in, first out*, el primero que entra es el primero que sale—. Cormen las presenta juntas en §10.1 de *Introduction to Algorithms* precisamente porque comparten la idea de fondo: son arreglos o listas a los que se les prohíbe el acceso por índice arbitrario para garantizar que sus operaciones cuesten **O(1)** en los extremos que sí se usan. En la pila, `push` y `pop` actúan sobre el mismo extremo; en la cola, se encola por un lado y se desencola por el otro. Esa asimetría es todo el tema. El porqué de la estructura es esa promesa de coste constante: cuando un algoritmo solo necesita «el último» o «el primero», pagar O(n) por buscarlo sería absurdo, y la pila y la cola lo entregan en tiempo fijo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular una pila y una cola.
2. Explicar LIFO frente a FIFO.
3. Reconocer sus usos típicos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila (LIFO) | Último en entrar, primero en salir |
| 2 | Cola (FIFO) | Primero en entrar, primero en salir |
| 3 | push/pop, enqueue/dequeue | Sus operaciones |

## 📖 Definiciones y características

- **Pila (stack)** — colección con disciplina LIFO. Solo se manipula un extremo, la *cima*: `push` deposita un elemento encima y `pop` retira el que esté encima, que siempre es el más reciente. Cormen (§10.1) la describe con la metáfora del montón de platos: apilas y desapilas por arriba. Ambas operaciones son **O(1)** porque no exigen recorrer nada; se implementa sobre un arreglo dinámico (creciendo por el final) o una lista enlazada (insertando por la cabeza). Su uso canónico es la **pila de llamadas** del propio programa, el «deshacer» de un editor y el recorrido en profundidad (DFS) de la clase 098.
- **Cola (queue)** — colección con disciplina FIFO. Se encola por la *cola* (`enqueue`) y se desencola por la *cabeza* (`dequeue`), de modo que quien llega primero es atendido primero, como una fila de personas. Sedgewick insiste en que esta imparcialidad temporal es lo que la hace idónea para *buffers*, planificación de tareas y el recorrido en anchura (BFS). El reto está en lograr O(1) por **ambos** extremos: sacar por el frente de un arreglo desplazando el resto costaría O(n), por lo que una cola eficiente usa un *buffer* circular o una **deque** (double-ended queue) que crece y se encoge por los dos lados sin mover nada.
- **LIFO frente a FIFO** — no son dos nombres de lo mismo: son dos políticas opuestas de salida sobre la misma secuencia de entrada. Con la entrada `1 2 3`, la pila devuelve `3 2 1` (invierte) y la cola devuelve `1 2 3` (conserva). Elegir una u otra determina el comportamiento del algoritmo que la usa.

## 🧩 Situación

Piensa en el botón «deshacer» de un editor: cada cambio se apila encima del anterior y al pulsar Ctrl+Z se recupera el último —una pila pura, porque solo interesa el movimiento más reciente. Piensa ahora en una cola de impresión o en el planificador de tareas de un servidor: los trabajos se atienden en el orden en que llegaron, sin que el último en pedir se cuele delante —una cola, porque la justicia aquí es temporal. La misma lista de enteros, sometida a una u otra disciplina, sale en orden opuesto, y ese contraste es exactamente lo que el problema de hoy vuelve observable: leemos una secuencia y la emitimos dos veces, una en orden LIFO (`pila`) y otra en orden FIFO (`cola`). El ejercicio es mínimo a propósito para que la atención caiga sobre la *disciplina de acceso*, no sobre un algoritmo complejo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `pila=<orden LIFO> cola=<orden FIFO>`
- **Regla:** pila = inverso(lista); cola = lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `pila=3-2-1 cola=1-2-3` |
| `5` | `pila=5 cola=5` |
| `1 2 3 4` | `pila=4-3-2-1 cola=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; pila <- sacar en LIFO ; cola <- sacar en FIFO
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
pila = "-".join(str(x) for x in reversed(nums))
cola = "-".join(str(x) for x in nums)
print(f"pila={pila} cola={cola}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<String> l = new ArrayList<>();
        for (String s : p) l.add(s);
        List<String> rev = new ArrayList<>(l);
        java.util.Collections.reverse(rev);
        System.out.println("pila=" + String.join("-", rev) + " cola=" + String.join("-", l));
    }
}
```

### C# · `dotnet run`

```csharp
using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string pila = string.Join("-", p.Reverse());
string cola = string.Join("-", p);
Console.WriteLine($"pila={pila} cola={cola}");
```

### Go · `go run main.go`

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
	rev := make([]string, len(f))
	for i, x := range f {
		rev[len(f)-1-i] = x
	}
	fmt.Printf("pila=%s cola=%s\n", strings.Join(rev, "-"), strings.Join(f, "-"))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    let mut rev = nums.clone();
    rev.reverse();
    println!("pila={} cola={}", rev.join("-"), nums.join("-"));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("pila=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf(" cola=");
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
-- SQL: orden descendente (pila) y ascendente (cola) por posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'pila=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos DESC))
     || ' cola=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos ASC)) AS resultado;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = implode("-", array_reverse($nums));
$cola = implode("-", $nums);
echo "pila=$pila cola=$cola\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `1 2 3`, que debe producir `pila=3-2-1 cola=1-2-3`. Las diez implementaciones comparten una idea: la `cola` es la secuencia tal cual (FIFO conserva el orden de llegada) y la `pila` es esa misma secuencia invertida (LIFO devuelve el último primero). Mirar tres lenguajes revela cómo cada modelo de memoria expresa esa inversión.

En **Python**, `sys.stdin.read().split()` produce la lista `[1, 2, 3]`. La línea `reversed(nums)` no crea una copia nueva: devuelve un *iterador* que recorre la lista de atrás hacia adelante, y `"-".join(...)` lo consume para formar `"3-2-1"`. La `cola` recorre la lista en su orden natural y produce `"1-2-3"`. Aquí `reversed` es el sustituto elegante de ir haciendo `pop()` sobre una pila real: sacar repetidamente de la cima de `[1, 2, 3]` daría 3, luego 2, luego 1 —exactamente el orden invertido.

En **Go**, no hay función `reverse` sobre *slices* en la biblioteca clásica, así que el código la escribe a mano: `rev := make([]string, len(f))` reserva un *slice* del mismo tamaño y el bucle `rev[len(f)-1-i] = x` coloca cada token en su posición espejo —el primero (`i=0`) va al final, el último al principio. Es la inversión hecha con aritmética de índices, sin azúcar sintáctico. `strings.Join(rev, "-")` da `"3-2-1"` y `strings.Join(f, "-")` da `"1-2-3"`.

En **C**, la disciplina de pila se ve todavía más desnuda. Los enteros se guardan en `long v[1024]` y `n` cuenta cuántos hay. Para la pila, el bucle `for (int i = n - 1; i >= 0; i--)` recorre el arreglo **desde el final**: eso *es* desapilar, ir tomando la cima que baja. Para la cola, `for (int i = 0; i < n; i++)` recorre desde el frente: eso *es* desencolar en orden de llegada. El guion se intercala comprobando la posición (`if (i < n - 1)` y `if (i > 0)`) para no dejar un `-` colgando. El resultado impreso es `pila=3-2-1 cola=1-2-3`.

Los tres coinciden carácter a carácter con lo que dicta `casos.json`, y el verificador lo comprueba para las diez implementaciones.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `append`/`pop` (Python), `push`/`shift` (JS), `Deque` (Java). |
| Semántica | La pila saca por el final; la cola por el frente. |
| Paradigmática | SQL ordena por la posición ascendente o descendente. |

La diferencia más honda entre los diez lenguajes no está en cómo *invierten* una lista, sino en qué **colección nativa** ofrecen para una pila o una cola de verdad. Python usa `list` como pila (`append`/`pop` son O(1) por el final) pero desaconseja usarla como cola, porque `pop(0)` es O(n) al desplazar todo; para eso está `collections.deque`, con O(1) por ambos extremos (Ramalho lo detalla en *Fluent Python*). Java separa las dos ideas: `ArrayDeque` es hoy la pila y la cola recomendadas, mientras la vieja clase `Stack` sobrevive por compatibilidad (Bloch la desaconseja por heredar de `Vector` y estar sincronizada sin necesidad). C# ofrece `Stack<T>` y `Queue<T>` explícitos; Go resuelve la pila con un *slice* (`append` y recorte `s[:len(s)-1]`) y, para la cola eficiente, obliga a `container/list` o un *buffer* circular propio; Rust brinda `Vec<T>` como pila y `VecDeque<T>` como cola. El otro eje es **valor frente a referencia**: en Rust y Go la inversión trabaja sobre datos que se poseen o se copian explícitamente (`nums.clone()` en Rust deja el original intacto), mientras en Java o Python `Collections.reverse` y `list.reverse()` mutarían la lista en sitio —de ahí que el código copie antes de invertir, para no destruir la versión FIFO.

## 🧬 El concepto en la familia

Casi todos los lenguajes distinguen la pila «barata sobre arreglo» de la cola «que necesita cuidado en ambos extremos». En Go, una pila es un *slice* con `append`/recorte y una cola honesta exige una *deque* o `container/list`, porque desencolar por el frente de un *slice* copiando es O(n). En C++, la biblioteca estándar ofrece `std::stack` y `std::queue` como *adaptadores*: no son contenedores propios, sino envoltorios que restringen la interfaz de un `deque` subyacente para exponer solo `push`/`pop` o `push`/`front`, que es la esencia misma de estas estructuras —tomar algo general y *limitar* deliberadamente lo que se puede hacer con ello. Reconocer ese patrón (una deque generalista debajo, una interfaz restringida encima) ayuda a leer la biblioteca de cualquier lenguaje: la pila y la cola casi nunca son tipos primitivos, sino disciplinas impuestas sobre una colección más flexible.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 096
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir el extremo de salida** → causa: intercambiar las disciplinas y sacar de la pila por el frente o de la cola por el final → solución: recordar la física —la pila saca por la cima (el mismo extremo donde apila), la cola saca por la cabeza (el extremo opuesto a donde encola).
- **Usar `shift`/`pop(0)`/`remove(0)` como cola en listas grandes** → causa: sacar por el frente de un arreglo obliga a desplazar todos los elementos restantes, un coste O(n) por operación que convierte un bucle en O(n²) → solución: usar una estructura de cola real (`collections.deque` en Python, `ArrayDeque` en Java, `VecDeque` en Rust) que ofrece O(1) por ambos extremos.
- **Inicializar el máximo o vaciar la pila sin comprobar si está vacía** → causa: hacer `pop` sobre una pila vacía lanza excepción o, en C, lee basura → solución: comprobar el tamaño antes de sacar; en el problema de hoy la entrada siempre trae al menos un elemento, pero en código real es la comprobación que más se olvida.

## ❓ Preguntas frecuentes

- **¿Pila o cola?** Depende de a quién quieras atender primero. Pila (LIFO) cuando importa lo más reciente: deshacer, evaluar expresiones anidadas, recorrer en profundidad, gestionar la recursión. Cola (FIFO) cuando importa la antigüedad y la justicia: turnos, *buffers* de mensajes, planificación, recorrer en anchura.
- **¿La recursión usa pila?** Sí, y no es una metáfora: cada llamada a función deja un *marco de pila* (parámetros, variables locales, dirección de retorno) en la **pila de llamadas** del proceso, que crece con cada llamada anidada y se desapila al retornar. Por eso una recursión demasiado profunda produce un *stack overflow*: se agotó esa pila real. Un DFS puede escribirse recursivo (usando esa pila implícita) o iterativo con una pila explícita —son la misma estructura.
- **¿Por qué no basta una lista para todo?** Una lista permite insertar y borrar en cualquier posición, pero esa libertad cuesta: no garantiza O(1) en los extremos ni comunica la *intención*. Declarar «esto es una pila» le dice al lector y al compilador que solo se tocará la cima, y a menudo permite una implementación más rápida y con menos errores.

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

> [⏮️ Clase 095](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 097 ⏭️](../../parte-6-datos-y-estructuras/097-arboles/README.md)
