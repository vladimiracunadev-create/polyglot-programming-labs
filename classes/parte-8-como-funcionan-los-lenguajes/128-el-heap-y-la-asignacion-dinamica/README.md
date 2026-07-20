# Clase 128 — El heap y la asignación dinámica

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La clase 127 mostró la pila: rápida, automática, pero de tamaño fijo y vida atada a la llamada. Esta presenta su contraparte, el **heap**: la región de memoria donde viven los datos cuyo tamaño o duración no se conocen al compilar. Construimos una lista descendente de `n` a `1` —una estructura cuyo tamaño *depende de la entrada*— precisamente porque no cabe en la pila con un tamaño fijo decidido de antemano; debe reservarse dinámicamente. El *porqué* toca el núcleo de la programación práctica: casi toda colección que crece (una lista, un diccionario, un buffer, un objeto) vive en el heap, y la diferencia stack/heap explica por qué unas variables «mueren» solas al salir de la función y otras persisten, por qué el heap necesita gestión (manual en C, automática con GC en Java) y por qué asignar en el heap cuesta más que en la pila. Bryant & O'Hallaron dedican su capítulo de *gestión de memoria virtual* a cómo el asignador (`malloc`) encuentra y reserva bloques en esta región.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir una estructura de tamaño dinámico determinado en tiempo de ejecución.
2. Distinguir la pila del heap por tamaño, vida y forma de gestión.
3. Reconocer cuándo un dato se asigna en el heap y por qué no podría ir a la pila.
4. Explicar el coste de la asignación dinámica frente al simple movimiento del *stack pointer*.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Heap | Aloja datos de tamaño y vida flexibles, decididos en ejecución |
| 2 | Asignación dinámica | Reservar memoria cuando el tamaño depende de los datos |
| 3 | Stack vs. heap | Automático y acotado frente a flexible y gestionado |

## 📖 Definiciones y características

El **heap** es la región de memoria destinada a datos cuyo tamaño o cuya vida no se conocen en tiempo de compilación. A diferencia de la pila, no sigue una disciplina LIFO: un objeto puede crearse en una función y seguir vivo mucho después de que esa función retorne, siempre que algo lo referencie. Esa flexibilidad tiene un precio: el heap necesita un *asignador* que lleve la cuenta de qué bloques están libres y cuáles ocupados, y una política para liberar lo que ya no se usa.

La **asignación dinámica** es el acto de pedir memoria del heap en ejecución. En C es explícita —`malloc(n * sizeof(long))` reserva espacio para `n` enteros cuando ya conoces `n`—; en los lenguajes gestionados es implícita —crear una `list`, un `ArrayList` o un `Vec` dispara la asignación bajo el capó—. La palabra clave es *dinámica*: el tamaño lo decide un valor de ejecución, no una constante de compilación.

El contraste **stack vs. heap** es el eje de esta clase. La pila reserva y libera moviendo un puntero: una instrucción, coste constante, sin fragmentación, pero tamaño fijo y vida ligada a la llamada. El heap busca un hueco adecuado entre los bloques libres, puede fragmentarse y exige liberar (a mano o por GC), a cambio de tamaño y vida arbitrarios. Elegir dónde vive un dato —cuando el lenguaje te deja elegir— es una decisión de rendimiento y corrección.

## 🧩 Situación

Escribes en C `long lista[n];` con `n` leído del usuario y, según el compilador, o no compila o revienta con listas grandes: la pila no está pensada para tamaños que dependen de la entrada. La solución —`malloc`— coloca la lista en el heap, donde cabe cualquier tamaño razonable y sobrevive hasta que tú la liberas. Construir la lista de `n` a `1` hace visible esa frontera: el mismo problema que en Python o Java resuelve una colección «que simplemente crece» exige en C pedir y devolver memoria explícitamente.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `lista=<n-(n-1)-...-1>`
- **Regla:** lista dinámica con los valores de n a 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `lista=3-2-1` |
| `1` | `lista=1` |
| `5` | `lista=5-4-3-2-1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar lista ; añadir n, n-1, ..., 1 ; unir por -
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
lista = []
for i in range(n, 0, -1):
    lista.append(i)
print("lista=" + "-".join(str(x) for x in lista))
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista: number[] = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

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
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> lista = new ArrayList<>();
        for (int i = n; i >= 1; i--) lista.add(i);
        System.out.println("lista=" + lista.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var lista = new List<int>();
for (int i = n; i >= 1; i--) lista.Add(i);
Console.WriteLine($"lista={string.Join("-", lista)}");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var lista []string
	for i := n; i >= 1; i-- {
		lista = append(lista, strconv.Itoa(i))
	}
	fmt.Printf("lista=%s\n", strings.Join(lista, "-"))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let lista: Vec<String> = (1..=n).rev().map(|x| x.to_string()).collect();
    println!("lista={}", lista.join("-"));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *lista = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) lista[i] = n - i;
    printf("lista=");
    for (long i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", lista[i]);
    }
    printf("\n");
    free(lista);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: genera la secuencia descendente con un CTE (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (3) UNION ALL SELECT i - 1 FROM r WHERE i > 1)
SELECT 'lista=' || group_concat(i, '-') AS resultado FROM r;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$lista = [];
for ($i = $n; $i >= 1; $i--) {
    $lista[] = $i;
}
echo "lista=" . implode("-", $lista) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

La misma lista descendente expone dos filosofías de heap: la explícita de C y la implícita de todos los demás.

En **Python**, `lista = []` y `lista.append(i)` esconden toda la maquinaria. El objeto lista vive en el heap desde su creación, y cuando `append` agota la capacidad interna, CPython realoja el buffer a uno mayor —típicamente sobredimensionado para amortizar futuros crecimientos— sin que tú te enteres. No hay `malloc` ni `free` a la vista: el recolector de basura liberará la lista cuando nadie la referencie. La asignación dinámica es real, solo que gestionada.

En **C**, la misma idea es cruda y explícita: `long *lista = malloc(n * sizeof(long));` pide al asignador un bloque contiguo del heap justo del tamaño que `n` exige, y devuelve un puntero a su inicio. Rellenas con aritmética de índices (`lista[i] = n - i`), imprimes, y —esto es lo esencial— llamas a `free(lista)` para devolver el bloque. Si olvidaras ese `free`, tendrías una *fuga de memoria*: el bloque quedaría reservado para siempre. C te da control total y toda la responsabilidad; es el modelo que Bryant & O'Hallaron diseccionan al explicar cómo funciona un asignador por dentro.

En **Rust**, `(1..=n).rev().map(|x| x.to_string()).collect::<Vec<String>>()` construye un `Vec` en el heap con una sola expresión. El `Vec` es como el `malloc` de C pero con la liberación garantizada: cuando `lista` sale de ámbito al final de `main`, Rust inserta automáticamente la liberación de su memoria (su `Drop`), sin GC y sin `free` manual. Es el punto medio que la clase 132 desarrollará: asignación dinámica en el heap, liberación determinista, cero fugas —comprobado por el compilador.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Colección dinámica | `list` (Python), array (JS/TS), `ArrayList` (Java), `List` (C#), *slice* (Go), `Vec` (Rust), array (PHP): todas en el heap. |
| Reserva | Implícita en los gestionados; explícita con `malloc` en C. |
| Liberación | GC en Python/JS/Java/C#/Go; `Drop` automático en Rust; `free` manual en C. |
| Crecimiento | Realojo amortizado (duplicar capacidad) en la mayoría de colecciones dinámicas. |
| SQL | No asigna colecciones así: el CTE genera la secuencia de forma declarativa. |

## 🧬 El concepto en la familia

La divisoria está en quién libera el heap. En un extremo, C y C++ (con `malloc`/`free`, `new`/`delete`) exigen liberación manual: máximo control, máximo riesgo de fugas y de *use-after-free*. En el otro, los lenguajes con recolector —Python, JavaScript, Java, C#, Go— asignan libremente y dejan que un GC reclame lo inalcanzable (clase 131). En medio, Rust logra liberación determinista sin GC mediante propiedad y `Drop` (clase 132). Todas las colecciones que usas a diario —diccionarios, mapas, cadenas que crecen— se apoyan en este heap; entender su gestión es entender de dónde vienen las fugas y los cuelgues por memoria.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 128
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Querer un tamaño dinámico en la pila** → causa: la pila exige tamaños fijos conocidos al compilar → solución: usar una colección del heap (o `malloc` en C) cuando el tamaño depende de la entrada.
- **Fuga de memoria al no liberar (C)** → causa: cada `malloc` sin su `free` deja un bloque reservado para siempre → solución: emparejar cada asignación con su liberación, o usar RAII/GC en lenguajes que lo ofrecen.
- **Referenciar memoria ya liberada** → causa: usar un puntero tras el `free` (*use-after-free*) → solución: anular el puntero tras liberar, o dejar que el lenguaje gestione la vida del dato.

## ❓ Preguntas frecuentes

- **¿Todo va al heap?** No. Los valores pequeños de vida corta (contadores, parámetros) van a la pila; lo de tamaño dinámico, grande o de vida prolongada, al heap.
- **¿El heap es más lento?** Su *asignación* cuesta más que la pila porque hay que buscar un hueco y contabilizarlo; el acceso posterior al dato es igual de rápido.
- **¿Puedo elegir dónde vive un dato?** En C, Rust, Go y C++ sí, en cierta medida; en Python, JavaScript o Java el runtime lo decide casi siempre por ti (los objetos van al heap).

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 127](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 129 ⏭️](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md)
