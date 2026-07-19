# Clase 116 — Funcional III: functores, mónadas y efectos (visión práctica)

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Las palabras *functor* y *mónada* vienen de la teoría de categorías y arrastran una fama de dificultad que aquí vamos a desmontar. La visión práctica es sencilla: un **functor** es cualquier contenedor sobre el que puedas aplicar `map` de forma que la estructura se conserve —metes una caja, transformas lo de dentro, y sale una caja del mismo tipo—; una **mónada** es un contenedor que además sabe *encadenar* cómputos que a su vez producen contenedores, sin que se te acumulen las cajas anidadas. Tony Hoare llamó al puntero nulo su "error de mil millones de dólares"; las mónadas prácticas como `Option`/`Maybe` son, en buena medida, la respuesta de la comunidad funcional a ese error.

El objetivo de hoy es entender por qué envolver un valor en `Option` y aplicarle `map` es mejor que dejar circular un `null` desnudo. Van Roy y Haridi, al presentar los modelos de cómputo con estado y excepciones, muestran que buena parte de la complejidad de un programa viene de *casos especiales* que se propagan de manera implícita: el "y si no hay dato" que salpica de `if` cada función. La idea del functor es hacer ese caso especial **explícito en el tipo** y tratarlo una sola vez, en el `map`, en vez de repetirlo en cada llamada.

El ejercicio concreto es diminuto pero fiel al patrón: leemos un entero, lo envolvemos en un `Option` que contiene el número solo si es positivo (`Some n` si `n > 0`, `None` en caso contrario), le aplicamos `map(x → 2x)` y observamos el resultado. Verás que muchos lenguajes del núcleo ya traen esta mónada práctica de fábrica —`Option` en Rust, `Optional` en Java, `int?` (`Nullable`) en C#— y que aunque la sintaxis cambie, la semántica de "aplica si hay, propaga la ausencia si no" es la misma en todos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Envolver un valor opcional.
2. Aplicar map sobre Option (functor).
3. Explicar la ventaja frente a null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Option/Maybe | Contenedor de 'quizá hay valor' |
| 2 | map sobre contenedor | Aplicar sin desenvolver |
| 3 | Functor | Algo sobre lo que se puede mapear |

## 📖 Definiciones y características

- **Functor** — contenedor sobre el que se puede aplicar `map` (Option, listas). Clave: transformar el contenido sin sacarlo.
- **Option/Maybe** — envuelve un valor presente (Some) o ausente (None). Clave: ausencia explícita y segura.
- **map sobre Option** — aplica la función si hay valor; si no, propaga la ausencia. Clave: sin ifs dispersos.

Para que un contenedor sea un functor *de verdad*, su `map` debe cumplir dos leyes que no son burocracia académica sino garantías prácticas. La primera: `map` con la función identidad no cambia nada (`caja.map(x => x)` es la misma caja). La segunda: mapear dos veces equivale a mapear con la composición (`caja.map(g).map(f)` es `caja.map(f ∘ g)`). Estas leyes son lo que te permite razonar sobre una tubería de `map` sin miedo: sabes que la estructura del contenedor —presente o ausente, cuántos elementos— nunca se altera por el camino, solo su contenido. Es la misma clausura bajo composición de la clase 115, ahora elevada a contenedores.

La distinción entre **functor** y **mónada** se ve mejor con un ejemplo. `map` toma una función `x → y` y transforma `Option<x>` en `Option<y>`. Pero ¿qué pasa si la función que aplicas *también* puede fallar, es decir, devuelve otro `Option`? Con `map` acabarías con un `Option<Option<y>>`, dos cajas anidadas. La operación monádica —`flatMap` en Java y Rust, `and_then`, `bind` en la literatura— es la que aplana esa anidación: encadena cómputos que producen contenedores manteniendo una sola capa. Por eso se dice que toda mónada es un functor, pero no todo functor es una mónada: el functor sabe transformar el contenido; la mónada sabe además secuenciar operaciones que devuelven contexto. Van Roy y Haridi describen precisamente este patrón —secuenciar cómputos que arrastran un contexto (ausencia, error, estado, entrada/salida)— como el núcleo de lo que en otros lenguajes se resuelve con efectos.

En este laboratorio nos quedamos en el nivel de **functor**: un solo `map` basta para la regla `Option(n si n>0).map(x → 2x)`. La mónada asoma solo como concepto, porque encadenar dos operaciones fallibles sería el paso siguiente natural. Lo esencial es la lección de diseño: el tipo `Option` obliga a quien recibe el valor a considerar la ausencia, mientras que un `null` se cuela silenciosamente hasta que revienta en un `NullPointerException` a tres capas de distancia del origen.

## 🧩 Situación

Piensa en buscar un usuario por su identificador en una base de datos. La consulta puede devolver un registro o nada. En el estilo imperativo clásico devuelves `null` cuando no hay usuario, y a partir de ahí toda función que reciba ese resultado tiene que acordarse de comprobar `if (usuario != null)` antes de tocarlo. Basta que una sola función se olvide —y siempre hay una— para que el `null` viaje hasta un `usuario.getNombre()` que explota con un `NullPointerException` cuyo *stack trace* apunta al síntoma, no a la causa: el registro que no existía diez llamadas atrás.

El functor cambia el contrato. La consulta devuelve un `Option<Usuario>` que hace visible en el propio tipo la posibilidad de ausencia, y en vez de comprobar el null a mano escribes `usuario.map(u => u.getNombre())`: si hay usuario, se aplica la función; si no, el `None` se propaga solo, sin que ninguna función intermedia tenga que acordarse de nada. En esta clase reducimos ese escenario a su hueso: envolvemos un entero en un `Option` presente solo cuando es positivo y le aplicamos `map(x → 2x)`. Para `stdin` `5` el resultado es `resultado=10`; para `0` y `-3`, donde no hay valor, `resultado=nada`. Menos ruido, menos errores de null, y la ausencia tratada una vez en lugar de en cada paso.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>` si n>0 (hay valor), o `resultado=nada` si no
- **Regla:** Option(n si n>0).map(x → 2x)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=nada` |
| `-3` | `resultado=nada` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
opcion <- Some(n) SI n>0 SINO None ; ESCRIBIR opcion.map(x->2x) o 'nada'
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
opcion = n if n > 0 else None
if opcion is not None:
    print(f"resultado={opcion * 2}")
else:
    print("resultado=nada")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const opcion = n > 0 ? n : null;
console.log(opcion !== null ? `resultado=${opcion * 2}` : "resultado=nada");
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const opcion: number | null = n > 0 ? n : null;
console.log(opcion !== null ? `resultado=${opcion * 2}` : "resultado=nada");
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Optional<Integer> opcion = n > 0 ? Optional.of(n) : Optional.empty();
        Optional<Integer> r = opcion.map(x -> x * 2);
        System.out.println(r.map(x -> "resultado=" + x).orElse("resultado=nada"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int? opcion = n > 0 ? n : (int?) null;
int? r = opcion.HasValue ? opcion.Value * 2 : (int?) null;
Console.WriteLine(r.HasValue ? $"resultado={r.Value}" : "resultado=nada");
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
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	if n > 0 {
		fmt.Printf("resultado=%d\n", n*2)
	} else {
		fmt.Println("resultado=nada")
	}
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let opcion: Option<i64> = if n > 0 { Some(n) } else { None };
    match opcion.map(|x| x * 2) {
        Some(r) => println!("resultado={r}"),
        None => println!("resultado=nada"),
    }
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n > 0) {
        printf("resultado=%ld\n", n * 2);
    } else {
        printf("resultado=nada\n");
    }
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL propaga NULL por las operaciones automáticamente.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT CASE WHEN n > 0 THEN printf('resultado=%d', n * 2) ELSE 'resultado=nada' END AS resultado
FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$opcion = $n > 0 ? $n : null;
echo $opcion !== null ? "resultado=" . ($opcion * 2) . "\n" : "resultado=nada\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

El contrato de [`casos.json`](casos.json) es claro: `stdin` `5` → `resultado=10`, `stdin` `0` → `resultado=nada`, `stdin` `-3` → `resultado=nada`. La regla es `Option(n si n>0).map(x → 2x)`. Sigamos cómo tres implementaciones —una que simula la mónada, otra que la trae de fábrica, y la nota SQL— llegan a esas salidas.

**Java — el `Optional` real de la biblioteca.** Esta es la implementación que hace visible el patrón sin simularlo. Tras leer `n`, la línea `Optional<Integer> opcion = n > 0 ? Optional.of(n) : Optional.empty();` construye la caja: `Optional.of(n)` es el `Some`, `Optional.empty()` es el `None`. La siguiente línea, `Optional<Integer> r = opcion.map(x -> x * 2);`, es el functor en acción: para `n = 5`, `opcion` contiene `5`, `map` aplica `x * 2` y `r` contiene `10`; para `n = 0` o `n = -3`, `opcion` está vacío y `map` **no ejecuta la lambda en absoluto** —devuelve otro `Optional` vacío—. Esa es la clave: la ausencia se propaga sin que escribamos ningún `if` alrededor del cálculo. El desenlace, `r.map(x -> "resultado=" + x).orElse("resultado=nada")`, encadena un segundo `map` para formatear y solo entonces, con `orElse`, sale de la caja proporcionando el texto por defecto. Los tres casos de `casos.json` salen de aquí: `resultado=10`, `resultado=nada`, `resultado=nada`.

**Rust — `Option` con `match`.** Rust construye `let opcion: Option<i64> = if n > 0 { Some(n) } else { None };`. Luego `opcion.map(|x| x * 2)` hace exactamente lo mismo que en Java: transforma `Some(5)` en `Some(10)` y deja `None` intacto. La diferencia está en cómo sale de la caja: en vez de `orElse`, usa `match` sobre las dos ramas, `Some(r) => println!("resultado={r}")` y `None => println!("resultado=nada")`. El compilador de Rust **obliga** a cubrir ambas ramas; olvidar el caso `None` es un error de compilación, no un fallo en ejecución. Ahí se ve la ventaja de tipo sobre `null` llevada al extremo: el lenguaje no te deja ignorar la ausencia.

**Python y la nota SQL — sin tipo `Option`.** La versión Python no tiene un contenedor `Option`, así que lo simula con `None` y un `if opcion is not None`. Funciona y produce las salidas correctas, pero muestra el contraste: sin functor, la comprobación de ausencia es explícita y podría olvidarse. El bloque SQL, marcado como ilustrativo, recorre la tabla `nums(n)` con `5`, `0`, `-3` y usa `CASE WHEN n > 0 THEN printf('resultado=%d', n * 2) ELSE 'resultado=nada' END`. SQL aporta un ángulo distinto: su `NULL` ya se propaga solo por las operaciones aritméticas (`NULL * 2` es `NULL`), que es la misma idea del functor incrustada en el modelo relacional. No lee `stdin`; lleva los casos en el `VALUES`, por eso el verificador la marca aparte.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Option`/`map` (Rust), `Optional` (Java), if/else (otros). |
| Semántica | El functor evita comprobar la ausencia en cada paso. |
| Paradigmática | SQL propaga NULL automáticamente por las operaciones. |

La diferencia práctica que separa a los lenguajes es cuánto te *obliga* el tipo a tratar la ausencia. Rust está en un extremo: `Option<T>` es un tipo distinto de `T`, no existe el `null`, y `match` fuerza a cubrir el caso vacío en tiempo de compilación. Java y C# están en un punto intermedio: `Optional<T>` e `int?` ofrecen el contenedor y sus `map`/`HasValue`, pero conviven con el `null` heredado, así que la disciplina depende del programador —puedes hacer `optional.get()` sin comprobar y volver a tropezar—. Python, JavaScript, Go, C y PHP no tienen un `Option` nativo: simulan la ausencia con `None`/`null`/`nil` y comprobaciones explícitas, que es exactamente el `if (x != null)` que el functor pretendía eliminar.

Hay un matiz semántico importante en el SQL. Su `NULL` propaga *automáticamente* por las operaciones (`NULL * 2` es `NULL`), lo cual se parece al functor, pero con una diferencia peligrosa: `NULL = NULL` no es cierto sino desconocido, y las agregaciones ignoran los `NULL` en silencio. La propagación es cómoda, pero no es la misma garantía de exhaustividad que da un `match` sobre `Option`. Por eso decimos que SQL *ilustra* la idea sin ser el mismo mecanismo.

## 🧬 El concepto en la familia

En Haskell la operación del functor se llama `fmap`: `fmap (*2) (Just n)` da `Just (2n)` y `fmap (*2) Nothing` da `Nothing`, con `Maybe` como el `Option` canónico. Kotlin resuelve el mismo problema a nivel de sintaxis del lenguaje con los tipos nullables y el operador de llamada segura: `n?.let { it * 2 }` aplica el bloque solo si `n` no es nulo. Swift tiene `Optional` con `?` y `map`; Scala, `Option` con `map`/`flatMap`. El hilo común es que todos convierten "puede que no haya dato" de un accidente en tiempo de ejecución a una decisión visible en el tipo. Y la misma familia de mónadas cubre más contextos que la ausencia: `Result`/`Either` para errores, `List` para múltiples resultados, `Future`/`Promise` para cómputos asíncronos. Cambia el contexto, se conserva el patrón `map`/`flatMap`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 116
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desenvolver a la fuerza sin comprobar** → causa: llamar a `optional.get()` (Java), `option.unwrap()` (Rust) o `nullable.Value` (C#) sin verificar que hay valor, lo que lanza excepción o *panic* con `None`. → remedio: opera *dentro* de la caja con `map`/`flatMap` y sal de ella solo al final con `orElse`/`unwrap_or`/un `match` que cubra la ausencia con un valor por defecto.
- **Confundir functor con mónada** → causa: usar `map` cuando la función que aplicas ya devuelve un `Option`, lo que produce un `Option<Option<T>>` anidado y difícil de manejar. → remedio: si la transformación puede fallar y devuelve otro contenedor, usa `flatMap`/`and_then`, que aplana la anidación; reserva `map` para funciones que devuelven un valor plano.
- **Tratar `map` como un `if` disfrazado y meterle efectos** → causa: colar dentro de la lambda de `map` una operación con efectos secundarios (imprimir, mutar estado). → remedio: `map` es para transformar el contenido; los efectos rompen las leyes del functor y hacen impredecible la propagación de la ausencia.

## ❓ Preguntas frecuentes

- **¿Cuál es la diferencia real entre functor y mónada?** El functor sabe *transformar* el contenido con `map`: aplica una función `x → y` sobre `Option<x>` y obtiene `Option<y>`. La mónada sabe además *secuenciar* con `flatMap`: encadena funciones que devuelven contenedores (`x → Option<y>`) sin que se anide una caja dentro de otra. Todo lo que es mónada es functor; lo contrario no. En esta clase basta `map`, pero encadenar dos operaciones fallibles ya pediría `flatMap`.
- **¿Por qué `Option` es mejor que `null`?** Porque el tipo cambia el contrato: `Option<T>` es distinto de `T`, así que el lenguaje —y en Rust el compilador— te recuerda que hay un caso vacío que atender. El `null` tiene el mismo tipo que el valor presente, se cuela silenciosamente por las capas y solo se manifiesta cuando alguien lo desreferencia, lejos de donde se originó. Es la diferencia entre un error atrapado en el diseño y el "error de mil millones de dólares".
- **¿Esto no es solo un `if` con nombre elegante?** En el caso de un único `map` la ganancia parece pequeña, y lo es. El valor se nota cuando encadenas varias transformaciones fallibles: con `Option` escribes una tubería `map(...).flatMap(...).map(...)` donde la ausencia se propaga una sola vez, frente a un anidamiento de `if` que crece en cada paso y multiplica las rutas por probar.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press) — secuenciación de cómputos con contexto (ausencia, error, estado).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — abstracción con procedimientos de orden superior.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson) — cap. 15, tipos y construcciones de los lenguajes funcionales.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley) — ítem 55, devolver `Optional` con criterio.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) — cap. 6, `enum` y `Option`.
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly) — tratamiento de `NULL`.
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 115](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 117 ⏭️](../../parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md)
