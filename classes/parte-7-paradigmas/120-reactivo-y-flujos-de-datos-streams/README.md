# Clase 120 — Reactivo y flujos de datos (streams)

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cambia la pregunta que le haces a los datos. En vez de "dame la colección completa y yo la recorro", el paradigma **reactivo / de flujos** dice "trata el dato como una corriente que pasa por una tubería de operadores". No manipulas una lista quieta en memoria; describes una serie de transformaciones —filtrar, mapear, reducir— y dejas que cada elemento fluya por ellas. El pensamiento se desplaza del *cómo itero* al *qué le hago a cada elemento que pase*, y esa mudanza es la que hace el código componible: cada operador es una pieza independiente que se encadena con la siguiente.

La idea tiene una raíz honda y elegante. Abelson y Sussman le dedican la sección 3.5 de *SICP* completa a los *streams*: los presentan como listas cuya cola se evalúa *perezosamente*, solo cuando alguien la pide. Esa pereza es lo que permite representar flujos infinitos —los números naturales, la sucesión de primos— sin agotar la memoria, porque nunca se materializa la corriente entera, solo el trozo que se consume. Van Roy y Haridi, en el capítulo 4 de *CTM*, formalizan la otra cara de la moneda: las *variables de flujo de datos* (dataflow), donde un valor "aún no calculado" bloquea a quien lo necesita hasta que aparece, sincronizando productores y consumidores sin candados explícitos.

Nuestro laboratorio es intencionadamente terrenal —filtra los pares de una lista y los duplica— para que veas el esqueleto del pipeline sin el ruido de la pereza o la asincronía. Pero ese esqueleto, `filtrar → mapear → recolectar`, es el mismo que sostiene RxJS en el navegador, la API Streams de Java y Reactor en el backend. Dominar la forma del pipeline aquí te prepara para reconocerlo en cualquiera de sus encarnaciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar operadores sobre un flujo.
2. Filtrar y transformar en pipeline.
3. Reconocer el estilo reactivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Flujo (stream) | Datos como corriente |
| 2 | Operadores encadenados | filter, map, … |
| 3 | Pipeline | El dato fluye por pasos |

## 📖 Definiciones y características

- **Flujo/stream** — secuencia de datos procesada por etapas. Clave: filter/map encadenados.
- **Operador** — etapa que transforma el flujo (filter, map). Clave: se encadenan.
- **Reactivo** — reaccionar a datos que llegan con el tiempo. Clave: streams y observables.

El concepto que da coherencia a estos bullets es el de **evaluación perezosa** (*lazy evaluation*). En *SICP* 3.5, Abelson y Sussman construyen los streams sobre una promesa retardada: `cons-stream` guarda la cabeza pero deja la cola sin evaluar hasta que `stream-cdr` la fuerza. La consecuencia es profunda: un pipeline `filtrar → mapear` no procesa toda la lista en cada etapa, sino que "tira" de un elemento a través de toda la tubería antes de pedir el siguiente. Esto invierte el control del bucle —el consumidor marca el ritmo, no el productor— y es lo que permite trabajar con corrientes infinitas. En un lenguaje estricto como Python, una lista por comprensión materializa cada paso; un generador, en cambio, se comporta como el stream perezoso de SICP.

La segunda columna teórica es el **dataflow** de *CTM* (cap. 4). Van Roy y Haridi describen la *concurrencia declarativa*: variables que representan un valor que llegará, y operaciones que se suspenden automáticamente hasta que ese valor esté disponible. Un pipeline de streams es dataflow disfrazado: cada operador es un pequeño proceso que espera datos de su predecesor y alimenta a su sucesor. La belleza del modelo es que el resultado es *determinista* —siempre el mismo, sin importar el entrelazado— porque los operadores no comparten estado mutable, solo se pasan valores por la tubería. Esa ausencia de estado compartido es lo que distingue al estilo reactivo del imperativo y lo que lo hace seguro de componer.

Por último, el linaje moderno: **ReactiveX** y los *observables*. Un observable es la contraparte "empujada" (*push*) del iterador "tirado" (*pull*): en vez de que tú pidas el siguiente elemento, el flujo te lo entrega cuando llega, y tus operadores `filter`/`map` reaccionan. Es la misma álgebra de operadores de SICP, trasladada del tiempo lógico al tiempo real de los eventos.

## 🧩 Situación

Tienes que procesar un archivo de registro (log) de ocho gigabytes para extraer, de cada línea que sea un error, el código de estado. Cargarlo entero en una lista reventaría la memoria. El enfoque de flujos resuelve esto de raíz: abres el archivo como una corriente de líneas, encadenas `filtrar(es_error)` seguido de `mapear(extraer_codigo)`, y consumes el resultado línea a línea. En ningún momento existe la colección completa en memoria; cada línea entra al pipeline, se transforma y se libera antes de que llegue la siguiente.

El mismo patrón sirve para datos que llegan *con el tiempo* y no de golpe: clics de usuario, mensajes de un WebSocket, lecturas de un sensor. Ahí el flujo se vuelve genuinamente reactivo —reacciona a cada dato cuando aparece— y la pereza deja de ser una optimización para convertirse en la única opción, porque el futuro del flujo literalmente aún no existe. Nuestro laboratorio comprime la lista a unos pocos enteros en una línea, pero la operación —`filtrar los pares, luego duplicarlos`— es exactamente la clase de encadenamiento que gobierna esos escenarios reales.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `stream=<pares duplicados, unidos por ->`
- **Regla:** flujo: filtrar pares, luego map x → 2x

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `stream=4-8` |
| `2 4` | `stream=4-8` |
| `6 7 8` | `stream=12-16` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
flujo(lista) |> filtrar(par) |> mapear(x->2x) |> recolectar
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
stream = [x * 2 for x in nums if x % 2 == 0]
print("stream=" + "-".join(str(x) for x in stream))
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const stream = nums.filter((x) => x % 2 === 0).map((x) => x * 2);
console.log(`stream=${stream.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const stream = nums.filter((x) => x % 2 === 0).map((x) => x * 2);
console.log(`stream=${stream.join("-")}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

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
        String r = Arrays.stream(p).map(Integer::parseInt)
                .filter(x -> x % 2 == 0).map(x -> x * 2)
                .map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("stream=" + r);
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
var stream = p.Select(int.Parse).Where(x => x % 2 == 0).Select(x => x * 2);
Console.WriteLine($"stream={string.Join("-", stream)}");
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
	var stream []string
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n%2 == 0 {
			stream = append(stream, strconv.Itoa(n*2))
		}
	}
	fmt.Printf("stream=%s\n", strings.Join(stream, "-"))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let stream: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| (x * 2).to_string())
        .collect();
    println!("stream={}", stream.join("-"));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("stream=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x * 2);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: WHERE + SELECT es un pipeline declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'stream=' || group_concat(x * 2, '-') AS resultado FROM nums WHERE x % 2 = 0;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$stream = array_map(fn($x) => $x * 2, array_filter($nums, fn($x) => $x % 2 === 0));
echo "stream=" . implode("-", $stream) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos un dato por la tubería con el primer caso de [`casos.json`](casos.json): entrada `1 2 3 4`, salida esperada `stream=4-8`.

En **Python** el pipeline cabe en una línea: `stream = [x * 2 for x in nums if x % 2 == 0]`. Conviene leerla como dos operadores encadenados aunque la sintaxis los funda. Primero se lee la corriente: `nums = [int(x) for x in sys.stdin.read().split()]` convierte `"1 2 3 4"` en `[1, 2, 3, 4]`. Luego, la cláusula `if x % 2 == 0` es el **filtro**: deja pasar solo `2` y `4`, descartando `1` y `3`. Sobre lo que sobrevive, la expresión `x * 2` es el **map**: `2` se convierte en `4`, `4` en `8`. El resultado es `[4, 8]`, que la última línea une con guiones: `stream=4-8`, exactamente lo que pide el caso. Recorre mentalmente el segundo caso, `2 4`: ambos son pares, se duplican a `4` y `8`, y sale de nuevo `stream=4-8`; el tercero, `6 7 8`, filtra el `7`, duplica `6→12` y `8→16`, y produce `stream=12-16`.

El orden de los operadores no es negociable. Si mapearas *antes* de filtrar —duplicar y luego quedarte con los pares— el resultado sería otro, porque todo número duplicado es par. Filtrar primero es lo que preserva la intención "los pares originales, duplicados". Este es el punto que la sección de errores comunes subraya: en un pipeline, el orden es semántica, no estilo.

**JavaScript** hace explícito lo que Python funde, y por eso es el mejor espejo del paradigma: `nums.filter((x) => x % 2 === 0).map((x) => x * 2)`. Aquí ves los dos operadores como dos llamadas encadenadas, cada una recibiendo el flujo que la anterior produjo. `filter` recorre `[1, 2, 3, 4]` y emite `[2, 4]`; sobre ese flujo intermedio, `.map` emite `[4, 8]`. La lectura es de izquierda a derecha, siguiendo el sentido en que fluye el dato, que es justamente la ventaja cognitiva del estilo: la tubería se lee como se ejecuta. `stream.join("-")` cierra con `4-8`.

Vale la pena notar una diferencia sutil que el laboratorio esconde. Tanto la comprensión de Python como el `.filter().map()` de JavaScript son *estrictos*: cada etapa construye una lista intermedia completa antes de pasar a la siguiente. En `[2, 4]` eso no importa, pero con el archivo de ocho gigabytes de la situación sería fatal. La versión perezosa —generadores en Python (`(x*2 for x in nums if ...)`) o `Stream` en Java— tira de un elemento a través de toda la tubería antes de pedir el siguiente, sin materializar los pasos intermedios. El resultado impreso es idéntico y coincide con `casos.json`; lo que cambia es cuánta memoria vive a la vez. Esa es la lección de SICP 3.5 aplicada: mismo resultado, distinta huella temporal y de memoria.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `.filter().map()` (JS/Rust), Streams (Java), LINQ (C#), generadores (Python). |
| Semántica | Los operadores se encadenan; el dato fluye por el pipeline. |
| Paradigmática | SQL encadena WHERE + SELECT, un pipeline declarativo. |

La diferencia real más importante entre los lenguajes es *estricto vs. perezoso*. La API `Stream` de Java es perezosa: la cadena `Arrays.stream(p).map(...).filter(...).map(...)` no hace nada hasta que una operación terminal (aquí `collect`) tira del flujo, y entonces cada elemento atraviesa toda la tubería de una vez. LINQ en C# (`Select().Where().Select()`) tiene el mismo diferimiento: se evalúa cuando se enumera. La comprensión de lista de Python y el `.filter().map()` de JavaScript, en cambio, son estrictos y crean listas intermedias; Python recupera la pereza con generadores y Rust con sus *iterator adapters*, que tampoco hacen trabajo hasta que un `collect()` los consume.

La otra diferencia es dónde vive el operador. En JavaScript, Rust y Java los operadores son métodos sobre el propio flujo, encadenados con punto; en Python el filtro y el map se expresan como cláusulas de una comprensión; en C# son métodos de extensión de LINQ. SQL cierra el cuadro desde el paradigma declarativo puro: `WHERE x % 2 = 0` es el filtro y `x * 2` en el `SELECT` es el map, pero el orden de ejecución lo decide el optimizador del motor, no tú. Es un pipeline, sí, pero uno donde renuncias al control del *cómo* a cambio de que la máquina lo optimice.

## 🧬 El concepto en la familia

En Java la API `Stream` (Java 8+) llevó los pipelines perezosos al núcleo del lenguaje; en el frontend, RxJS y el estándar *Observable* de ReactiveX son el estilo reactivo llevado al tiempo real de los eventos. Pero la genealogía es más larga: los `Enumerable` de LINQ en C#, los *iterators* perezosos de Rust, los generadores de Python y los canales de Go son todos parientes del stream de *SICP* 3.5. Del lado del backend reactivo, Reactor y Akka Streams añaden *backpressure* —el consumidor pide al productor que reduzca el ritmo—, que es la respuesta industrial al problema que el dataflow de *CTM* plantea en teoría: sincronizar productor y consumidor sin candados.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 120
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Materializar todo en cada paso** → causa: usar operadores estrictos (listas por comprensión, `.toList()` intermedios) obliga a construir la colección completa en cada etapa, lo que con flujos grandes o infinitos agota la memoria → solución: encadenar operadores perezosos (generadores en Python, `Stream` en Java, iteradores en Rust) para que cada elemento atraviese la tubería sin materializar los pasos intermedios.
- **Orden de operadores equivocado** → causa: mapear antes de filtrar cambia el resultado —duplicar y luego pedir pares deja pasar todo—, y filtrar tarde procesa elementos que se iban a descartar → solución: filtra lo antes posible para reducir el flujo cuanto antes, y recuerda que el orden es semántica, no adorno.
- **Efectos secundarios dentro de un operador** → causa: un `map` que además escribe en disco o muta estado global rompe el determinismo que hace seguro al pipeline y complica la depuración → solución: mantén los operadores como funciones puras; deja los efectos para el consumo final del flujo.
- **Consumir un flujo perezoso dos veces** → causa: en Java, LINQ o los generadores de Python, un stream es de un solo uso; volver a recorrerlo da vacío o error → solución: si necesitas reutilizarlo, materialízalo una vez en una colección, o reconstruye el flujo desde la fuente.

## ❓ Preguntas frecuentes

- **¿Stream o bucle explícito?** El stream es declarativo y componible: describes *qué* transformación aplicar y cada operador es una pieza reutilizable. El bucle da control fino sobre el *cómo* —índices, cortes tempranos, estado acumulado complejo—. Para transformaciones lineales (filtrar, mapear, reducir) el pipeline gana en legibilidad; para lógica con saltos irregulares, el bucle sigue siendo más claro.
- **¿La pereza cambia el resultado?** No el valor final, sí *cuándo* y *cuánto* se calcula. Un pipeline perezoso produce la misma salida que uno estricto, pero solo evalúa lo que el consumidor pide y no crea colecciones intermedias. Con un flujo infinito, la pereza es la diferencia entre funcionar y colgarse; es la lección central de *SICP* 3.5.
- **¿Reactivo es solo cosa del frontend?** No. RxJS lo hizo popular en el navegador, pero el mismo modelo gobierna el backend (Reactor, Akka Streams, con *backpressure*) y el procesamiento masivo de datos (Kafka Streams, Spark). El denominador común es tratar los datos como una corriente de operadores, no como una colección estática.
- **¿Qué relación tiene esto con la clase de eventos (119)?** Estrecha: un observable es un flujo de *eventos*. Donde en la clase 119 registrabas un callback para cada suceso, aquí encadenas operadores que reaccionan a cada dato que emite el flujo. Lo reactivo es el estilo de eventos dotado de un álgebra para filtrar, transformar y combinar esas emisiones.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). Cap. 4: concurrencia declarativa, variables de flujo de datos (dataflow) y streams como corrientes deterministas.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Sección 3.5: streams, evaluación perezosa y flujos infinitos.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Programación funcional y evaluación perezosa.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly). Caps. sobre iteradores, generadores y expresiones perezosas.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/). Métodos de orden superior (`filter`, `map`, `reduce`).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 119](../../parte-7-paradigmas/119-orientado-a-eventos-y-callbacks/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 121 ⏭️](../../parte-7-paradigmas/121-concurrente-hilos-tareas-y-canales/README.md)
