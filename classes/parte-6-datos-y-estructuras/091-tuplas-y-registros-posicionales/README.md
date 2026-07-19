# Clase 091 — Tuplas y registros posicionales

> Parte **6 — Datos y estructuras** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender la **tupla** como lo que es: una colección de tamaño **fijo** y **heterogénea** cuyos elementos se identifican por su **posición**, no por un nombre. Es la estructura mínima para responder a la necesidad más común de la programación —«devuélveme dos cosas relacionadas»— sin el peso de declarar un tipo con nombre para ello. Una función que calcula un cociente y su resto, un punto `(x, y)`, un par clave/valor: en todos esos casos los valores viajan juntos porque significan algo en conjunto, pero no ameritan bautizar un `struct`. La clave conceptual es doble. Primero, la tupla se distingue del **registro** o `struct` (clase 099), donde los campos tienen nombre (`p.x`, `p.y`): en la tupla accedes por orden (`t.0`, `t[1]`), lo que la hace más ligera pero también más frágil, porque el significado vive en una convención posicional que el compilador no siempre protege. Segundo, en la mayoría de lenguajes la tupla es **inmutable** y de **semántica de valor**: se copia al asignarla y no cambia tras crearse, lo que la vuelve segura para compartir. El acceso a cualquier componente es O(1), como en cualquier estructura indexada por posición. El ejercicio de hoy —leer un par e intercambiar sus componentes— ejercita justo eso: construir la tupla, desestructurarla y reordenarla.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear y desestructurar una tupla.
2. Acceder a los componentes por posición.
3. Distinguir tupla de lista.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tupla | Grupo fijo y ordenado |
| 2 | Componentes | Acceso por posición |
| 3 | Desestructuración | Repartir en variables |

## 📖 Definiciones y características

- **Tupla** — grupo ordenado de valores de tamaño fijo, posiblemente de tipos distintos, sin necesidad de declarar un tipo con nombre. Su aridad (cuántos elementos tiene) y a menudo el tipo de cada posición forman parte de su propio tipo: en Rust `(i64, i64)` es un tipo distinto de `(i64, i64, i64)`. Es liviana y suele ser inmutable, con semántica de valor: Ramalho, en *Fluent Python*, la describe como «registros sin nombres de campo».
- **Componente** — cada elemento de la tupla, accedido por su **posición**, empezando en 0. La notación cambia por lenguaje: `t[0]` en Python, `t.0` en Rust, `t.Item1` o campos nombrados en las tuplas de C#. El acceso es O(1): la posición se traduce en un desplazamiento fijo, igual que en un arreglo.
- **Registro posicional vs. registro nominal** — un registro agrupa campos relacionados; la diferencia está en **cómo** se identifican. En el registro *posicional* (la tupla) el significado lo da el orden: el primero es la `x`, el segundo la `y`, por convención. En el registro *nominal* (`struct`, `record`, clase 099) cada campo tiene nombre, lo que documenta la intención y resiste reordenamientos. La tupla cambia legibilidad por brevedad.
- **Desestructuración** — repartir los componentes de una tupla en variables independientes de una sola vez (`a, b = t`). Es la operación que hace a la tupla tan cómoda para devolver varios valores, y la base del intercambio idiomático `a, b = b, a`.

## 🧩 Situación

Una función necesita devolver dos cosas que significan algo juntas: un cociente y su resto, las coordenadas `(x, y)` de un punto, un par clave/valor, o el resultado de una búsqueda con su índice y su valor. Declarar una clase con nombre para cada una de esas parejas efímeras sería una ceremonia desproporcionada —tendrías decenas de tipos triviales que solo se usan una vez—. La tupla resuelve el caso: agrupa los valores sin bautizar nada, se desestructura en el sitio donde se recibe y desaparece. El problema de hoy —leer dos enteros e imprimirlos intercambiados como `tupla=(b, a)`— es el mínimo que muestra la construcción, el acceso posicional y el reordenamiento sin caer en el algoritmo.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `tupla=(<b>, <a>)` (componentes intercambiados)
- **Regla:** (a, b) → (b, a)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `tupla=(4, 3)` |
| `0 -2` | `tupla=(-2, 0)` |
| `5 5` | `tupla=(5, 5)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER (a, b) ; intercambiar ; ESCRIBIR (b, a)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
t = (a, b)
t = (t[1], t[0])
print(f"tupla=({t[0]}, {t[1]})")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t: [number, number] = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Par(int a, int b) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Par t = new Par(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        Par s = new Par(t.b(), t.a());
        System.out.println("tupla=(" + s.a() + ", " + s.b() + ")");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
(int a, int b) t = (int.Parse(p[0]), int.Parse(p[1]));
t = (t.b, t.a);
Console.WriteLine($"tupla=({t.a}, {t.b})");
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
	a, b = b, a
	fmt.Printf("tupla=(%d, %d)\n", a, b)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let t: (i64, i64) = (v[0], v[1]);
    let t = (t.1, t.0);
    println!("tupla=({}, {})", t.0, t.1);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene tuplas: se usa una struct. */
    struct Par { long a, b; } t = { b, a };
    printf("tupla=(%ld, %ld)\n", t.a, t.b);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: una fila con varias columnas es una tupla.
WITH pares(a, b) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('tupla=(%d, %d)', b, a) AS resultado FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$t = [(int) $b, (int) $a];
echo "tupla=({$t[0]}, {$t[1]})\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado: del código a la salida

Sigamos el caso `3 4`, que debe producir `tupla=(4, 3)`. La regla es simple —intercambiar los dos componentes— pero cada lenguaje la expresa con las herramientas que su modelo de tuplas le ofrece; comparemos tres muy distintos.

En **Python**, `a, b = map(int, ...)` ya es una desestructuración: la tupla que produce `map` se reparte en `a=3` y `b=4`. Luego `t = (a, b)` construye la tupla `(3, 4)` explícita, y `t = (t[1], t[0])` crea una tupla **nueva** con los componentes en orden inverso, `(4, 3)` —no muta la anterior, porque las tuplas de Python son inmutables (Ramalho, *Fluent Python*)—. El acceso `t[0]`, `t[1]` es posicional y O(1). El f-string produce `tupla=(4, 3)`.

En **Rust**, `let t: (i64, i64) = (v[0], v[1])` declara una tupla con tipo explícito; el acceso es por campo posicional con punto: `t.0` y `t.1`, sintaxis peculiar de Rust que refleja que la posición es parte del tipo. `let t = (t.1, t.0)` reasigna con *shadowing* a una tupla nueva `(4, 3)`. Como la tupla implementa `Copy` cuando sus componentes lo hacen, todo esto ocurre por valor, sin asignación en el heap.

En **Java**, que no tiene tuplas nativas, el ejemplo recurre a lo más cercano: un `record Par(int a, int b)`. Aquí el registro es **nominal**, no posicional —los campos se llaman `a` y `b` y se leen con `t.a()`, `t.b()`—, y el «intercambio» se hace construyendo `new Par(t.b(), t.a())`, es decir `Par(4, 3)`. Es la ilustración perfecta del contraste de la clase: donde Python y Rust usan orden, Java usa nombres, y el `record` (introducido en Java 16, elogiado por Bloch como remedio a las clases de datos verbosas) es su forma idiomática de agrupar datos inmutables. La salida vuelve a ser `tupla=(4, 3)`.

Los tres imprimen `tupla=(4, 3)`; el verificador comprueba que las diez implementaciones coinciden carácter a carácter con lo que dicta `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(a, b)` (Python/Rust/Go pares), arreglo (JS), record (Java). |
| Semántica | Rust/Python tienen tuplas nativas; Java usa records/objetos. |
| Paradigmática | SQL: una fila con varias columnas es una tupla. |

El eje más revelador es **qué tan nativa es la tupla**. Python y Rust la tienen como tipo de primera clase —`(a, b)` es una tupla de verdad, inmutable y con acceso posicional—. C# ofrece las *value tuples* `(int a, int b)` con nombres opcionales de campo, un híbrido entre tupla y registro. Go **no tiene** tuplas: en su lugar, las funciones devuelven varios valores (`a, b := f()`), lo que cubre el caso de uso más frecuente —el retorno múltiple— sin introducir un tipo tupla; por eso el ejemplo de Go simplemente hace `a, b = b, a`. C y Java carecen igualmente de tuplas y recurren a `struct` (C) o `record`/`ValueTuple` (Java/C#), es decir, a registros **nominales**. En **valor vs. referencia**: la tupla de Rust y la de C#, y el `struct` de C, son de valor (se copian); el `record` de Java es una referencia a un objeto inmutable en el heap. Y en **coste**, todas coinciden: el acceso a un componente es O(1), porque la posición es un desplazamiento fijo conocido en tiempo de compilación.

## 🧬 El concepto en la familia

La tupla posicional es un patrón casi universal, con matices que conviene conocer. En Haskell `(a, b)` es una tupla nativa de primera clase, con las funciones `fst` y `snd` para pares, y su aridad forma parte del tipo hasta el punto de que `(a, b)` y `(a, b, c)` son tipos incompatibles. En Ruby cualquier arreglo `[a, b]` cumple el papel de tupla y se desestructura con `a, b = arr`. En Swift las tuplas permiten incluso nombrar sus posiciones (`(x: 3, y: 4)`), acercándose al registro. En Python coexisten la `tuple` anónima y `collections.namedtuple`/`typing.NamedTuple`, que le ponen nombre a los campos sin perder la semántica de tupla —el puente exacto entre el registro posicional de esta clase y el nominal de la 099—. La lección transversal: cuando dos o tres valores viajan juntos y son efímeros, casi todo lenguaje ofrece una tupla o algo que hace sus veces; en cuanto los campos merecen nombre y el grupo persiste, conviene graduarse a un registro con nombre.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 091
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir tupla con lista** → causa: esperar que la tupla crezca con `append` o que se pueda mutar un componente → solución: la tupla tiene tamaño fijo y suele ser inmutable; si necesitas cambiar el contenido, usa una lista (clase 090) o construye una tupla nueva.
- **Acceder a un componente inexistente** → causa: pedir `t[2]` en un par, error de posición → solución: respetar la aridad; en lenguajes tipados como Rust el compilador lo impide, pero en Python es un error en tiempo de ejecución.
- **Depender del orden en tuplas largas** → causa: en `(nombre, edad, ciudad)` es fácil olvidar cuál posición es cuál y pasar los argumentos cambiados → solución: si son más de dos o tres campos, o si el orden no es obvio, gradúate a un registro con nombre (`namedtuple`, `record`, `struct`) donde el significado sea explícito.
- **Creer que intercambiar muta la tupla original** → causa: `t = (t[1], t[0])` no cambia la tupla vieja, crea una nueva → solución: entender que reasignas la variable a una tupla distinta; la original, si alguien más la referenciaba, sigue intacta (semántica de valor e inmutabilidad).

## ❓ Preguntas frecuentes

- **¿Tupla o clase/registro?** Tupla para agrupaciones pequeñas, anónimas y efímeras, sobre todo retornos de dos o tres valores; registro con nombre cuando los campos merecen documentarse, el grupo persiste o el orden no basta para recordar qué es qué. La tupla cambia legibilidad por brevedad.
- **¿Las tuplas son inmutables?** En muchos lenguajes sí (Python, Rust, las *value tuples* de C# copian por valor): no se modifican tras crearse. Eso las hace seguras de compartir y aptas como claves de diccionario en Python. Ojo: si una tupla de Python contiene una lista, esa lista interna sí puede mutar.
- **¿Por qué Go no tiene tuplas?** Porque cubre el caso principal —devolver varios valores— con el **retorno múltiple** (`a, b := f()`), sin añadir un tipo tupla al lenguaje. Es una decisión de diseño minimalista de Go: resuelve el 90 % de los usos de la tupla sin el tipo.
- **¿El acceso por posición es lento?** No: es O(1). La posición se conoce (a menudo en compilación) y se traduce en un desplazamiento fijo, igual que indexar un arreglo.

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

> [⏮️ Clase 090](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 092 ⏭️](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md)
