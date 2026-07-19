# Clase 131 — Recolección de basura (GC)

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La recolección de basura resuelve el problema de la clase anterior invirtiendo la pregunta. En C preguntas «¿cuándo puedo liberar esto?», una pregunta sobre el futuro que solo tú puedes responder y que fallas con frecuencia. Un recolector pregunta otra cosa, contestable mecánicamente: «¿queda algún camino desde una variable viva hasta este objeto?». Si no queda, el objeto es inalcanzable y **jamás** podrá volver a usarse; liberarlo es demostrablemente seguro. Esta clase construye ese modelo mental creando `n` objetos temporales que se vuelven basura inmediatamente. El *porqué* de estudiarlo con cuidado es que «hay GC» no es una respuesta: hay recolectores muy distintos, con costes muy distintos, y la diferencia entre el conteo de referencias de CPython, el generacional de la JVM y el concurrente de Go explica comportamientos que verás en producción —latencias de cola, picos de memoria, ciclos que nunca se liberan—. Nystrom dedica en *Crafting Interpreters* un capítulo entero a implementar un recolector *mark-sweep* real precisamente porque solo escribiéndolo se entiende qué garantiza y qué no.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir la basura por **alcanzabilidad** desde un conjunto raíz, y explicar por qué esa definición es conservadora.
2. Describir el algoritmo *mark-sweep* y en qué se diferencia del conteo de referencias.
3. Explicar qué es un GC **generacional** y por qué la hipótesis generacional lo hace rentable.
4. Distinguir una fuga real de una fuga lógica, y razonar sobre pausas *stop-the-world* frente a recolección concurrente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Raíces y alcanzabilidad | Define formalmente qué es basura, sin adivinar el futuro |
| 2 | Mark-sweep y sus variantes | El algoritmo base: marcar lo vivo, barrer el resto |
| 3 | Conteo de referencias | Liberación inmediata, pero incapaz con los ciclos |
| 4 | GC generacional | Por qué recolectar solo lo joven paga casi todo el trabajo |
| 5 | Pausas y latencia | El coste real que el automatismo traslada al tiempo de ejecución |

## 📖 Definiciones y características

Un **recolector de basura** parte de un conjunto de **raíces**: las variables locales de todos los marcos de pila activos, los registros de la CPU, las variables globales y estáticas. Todo objeto alcanzable siguiendo referencias desde alguna raíz está **vivo**; el resto es **basura**. Es importante entender que esta definición es *conservadora*: un objeto puede ser alcanzable y aun así no volver a usarse nunca (una entrada olvidada en una caché). El recolector no puede saberlo —eso requeriría predecir la ejecución futura, un problema indecidible—, así que lo conserva. De ahí que el GC elimine la fuga por olvido pero no la fuga lógica.

El algoritmo base es **mark-sweep**, propuesto por McCarthy para Lisp en 1960 y el que Nystrom implementa paso a paso. Tiene dos fases. En la de **marcado** se recorre el grafo de objetos desde las raíces, en profundidad, encendiendo un bit en cada objeto visitado. En la de **barrido** se recorre linealmente todo el heap y se libera cualquier objeto cuyo bit no se encendió, apagando los demás para la siguiente ronda. La virtud es que maneja ciclos sin esfuerzo: un objeto A que apunta a B y B a A, si ninguno es alcanzable desde una raíz, simplemente no se marca. La variante **mark-compact** añade una tercera fase que mueve los objetos vivos juntos al principio del heap, eliminando la fragmentación y permitiendo que reservar sea tan barato como avanzar un puntero (*bump allocation*) —algo que `malloc` no puede hacer porque no sabe qué punteros del programa habría que reescribir, mientras que el runtime de la JVM o de Go sí lo sabe.

El **conteo de referencias** es la alternativa: cada objeto lleva un contador que se incrementa al copiar una referencia y se decrementa al descartarla; al llegar a cero, se libera en el acto. Es el modelo primario de CPython y de PHP. Su ventaja es enorme en la práctica: la liberación es **determinista e inmediata**, lo que hace que el patrón `with open(...)` de Python cierre el archivo justo al salir del bloque. Su defecto es estructural: dos objetos que se apuntan mutuamente mantienen sus contadores en 1 aunque nadie más los alcance, y nunca se liberan. Por eso CPython añade encima un recolector cíclico generacional, y por eso `gc.collect()` existe.

Un **GC generacional** explota la *hipótesis generacional débil*: la abrumadora mayoría de los objetos muere muy joven. Dividiendo el heap en un vivero (*young generation*) y una o más generaciones viejas, el recolector puede recorrer solo el vivero —una fracción diminuta del heap— y recuperar la mayor parte de la basura en una fracción diminuta del tiempo. Los pocos objetos que sobreviven a varias recolecciones se *promueven* a la generación vieja, que se recolecta con mucha menos frecuencia. Esto es lo que hacen G1 y ZGC en la JVM, y el GC de .NET con sus generaciones 0, 1 y 2. El precio es una complejidad notable: hay que rastrear las referencias de objetos viejos a objetos jóvenes (mediante *write barriers* y *remembered sets*) para no perder objetos vivos al recolectar solo el vivero.

Finalmente, la **pausa**. Un recolector *stop-the-world* detiene todos los hilos del programa mientras trabaja: el marcado necesita una vista consistente del grafo, y si el programa muta referencias en medio, podría liberar algo vivo. Recolectores concurrentes como el de Go o ZGC hacen casi todo el marcado en paralelo con el programa, usando barreras de escritura para no perderse mutaciones, y reducen las pausas a fracciones de milisegundo —a cambio de consumir CPU y de que el heap crezca más. No existe un GC sin coste: se paga en pausas, en rendimiento agregado, en memoria adicional o en las tres cosas repartidas.

## 🧩 Situación

Un servicio en Java atiende el percentil 99 de sus peticiones en 8 ms, salvo unas pocas al día que tardan 400 ms. No hay nada anómalo en el código ni en la base de datos: es una recolección completa de la generación vieja, que detuvo todos los hilos. La solución no está en el código de negocio sino en entender el recolector: reducir la tasa de asignación, ajustar el tamaño del vivero, o cambiar a un recolector de baja latencia. Ese diagnóstico es imposible sin el modelo que da esta clase. Crear `n` objetos temporales que mueren inmediatamente reproduce, en miniatura, exactamente el patrón que alimenta al vivero.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de objetos temporales)
- **Salida** (stdout): `creados=<n> estado=recolectado`
- **Regla:** crear n objetos temporales; al perder la referencia, se recolectan

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `creados=5 estado=recolectado` |
| `0` | `creados=0 estado=recolectado` |
| `3` | `creados=3 estado=recolectado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
crear n objetos ; descartar referencias ; el GC recolecta
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
for _ in range(n):
    _tmp = object()  # temporal; sin referencia persistente, se recolecta
print(f"creados={n} estado=recolectado")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp = {}; // sin referencia persistente, será recolectado
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp: Record<string, unknown> = {};
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        for (int i = 0; i < n; i++) {
            Object tmp = new Object(); // el GC lo recolectará
            if (tmp == null) return;
        }
        System.out.println("creados=" + n + " estado=recolectado");
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
for (int i = 0; i < n; i++) {
    var tmp = new object(); // el GC lo recolectará
    if (tmp == null) return;
}
Console.WriteLine($"creados={n} estado=recolectado");
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
	for i := 0; i < n; i++ {
		tmp := new(int) // sin referencia persistente, el GC lo recolecta
		_ = tmp
	}
	fmt.Printf("creados=%d estado=recolectado\n", n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    for _ in 0..n {
        let _tmp = Box::new(0); // se libera al salir del ámbito (sin GC)
    }
    println!("creados={n} estado=recolectado");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    for (long i = 0; i < n; i++) {
        long *tmp = malloc(sizeof(long)); /* en C se libera a mano */
        free(tmp);
    }
    printf("creados=%ld estado=recolectado\n", n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no expone la memoria; se informa el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('creados=%d estado=recolectado', n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
for ($i = 0; $i < $n; $i++) {
    $tmp = new stdClass(); // recolectado por conteo de referencias
    unset($tmp);
}
echo "creados=$n estado=recolectado\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

El bucle es idéntico en los diez lenguajes, pero el destino de cada `tmp` es distinto en cada runtime.

En **Python**, `_tmp = object()` crea un objeto con contador de referencias a 1. En la siguiente iteración, `_tmp` se reasigna: el contador del objeto anterior baja a 0 y CPython lo libera **en ese instante**, dentro del bucle, sin esperar a ningún recolector. El recolector cíclico ni siquiera interviene aquí, porque `object()` no participa en ningún ciclo. Es el modelo más predecible de los tres, y la razón de que el consumo de memoria de un bucle así en Python se mantenga plano.

En **Java** y **C#**, `new Object()` reserva en el vivero avanzando un puntero: una operación de unas pocas instrucciones, más barata que un `malloc`. El objeto queda inalcanzable de inmediato, pero **no se libera al momento**: se queda ocupando espacio hasta que el vivero se llene y dispare una recolección menor. Entonces el recolector marca lo que sigue vivo (casi nada), lo copia a la otra mitad del vivero y declara libre todo el bloque de golpe. Ese es el punto contraintuitivo del GC generacional: los objetos muertos **no cuestan nada** recolectarlos, porque nadie los visita; el coste es proporcional a lo que sobrevive, no a lo que muere. El `if (tmp == null) return;` está ahí únicamente para que el compilador JIT no elimine la asignación por considerarla inútil.

En **Go**, `new(int)` puede acabar en el heap o en la pila: el compilador ejecuta un *escape analysis* y, si demuestra que la referencia no sobrevive a la función, reserva en la pila y no hay recolección que hacer. Cuando sí escapa al heap, entra en juego el recolector concurrente *tricolor mark-sweep* de Go, que marca en paralelo con las goroutines y solo detiene el mundo brevemente en el arranque y el cierre del ciclo. Go, a diferencia de la JVM, **no** es generacional ni compacta: los objetos nunca se mueven, lo que simplifica enormemente la interoperación con C pero deja la fragmentación en manos del asignador por clases de tamaño.

En **Rust**, `Box::new(0)` reserva en el heap igual que los demás, pero la liberación está **escrita en el binario**: el compilador sabe que `_tmp` muere al final de cada iteración e inserta ahí la llamada correspondiente. No hay recolector, no hay contador, no hay pausa. En **C**, la misma idea con `malloc`/`free` explícitos: el trabajo es el mismo, solo que quien lo escribe eres tú. En **PHP**, `unset($tmp)` decrementa el contador exactamente como Python. En **SQL** la pregunta no tiene sentido: el motor gestiona sus propios *buffers* y no expone objetos al usuario.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Mecanismo | Conteo de referencias + recolector cíclico (Python, PHP); *mark-sweep* generacional con compactación (Java, C#); *mark-sweep* concurrente no generacional (Go); generacional (JS/V8); ownership sin GC (Rust); manual (C). |
| Momento de la liberación | Inmediato y determinista (Python, PHP, Rust, C); diferido e impredecible (Java, C#, Go, JS). |
| Ciclos de referencias | Se liberan sin esfuerzo con marcado (Java, C#, Go, JS); requieren un recolector extra (Python, PHP); requieren `Weak<T>` explícito (Rust); enteramente tu problema (C). |
| ¿Se mueven los objetos? | Sí, se compactan (Java, C#, JS) — por eso las direcciones no son estables; no (Go, Python, C, Rust). |
| Pausa observable | Puede llegar a cientos de ms en recolecciones completas (JVM, .NET clásico); sub-milisegundo (Go, ZGC); inexistente por diseño (Rust, C). |
| Control del programador | `gc.collect()`, `gc.disable()` (Python); `GC.Collect()` (C#); `runtime.GC()`, `GOGC` (Go); flags de la JVM; ninguno en JS. |

## 🧬 El concepto en la familia

La recolección de basura nació con Lisp en 1960, y toda la familia Lisp —Scheme, Common Lisp, Clojure— la asume como una condición de existencia: sin ella no habría *cons cells* anónimas ni clausuras que capturan entorno. La JVM es hoy el laboratorio más rico de recolectores en producción, con una familia entera (Serial, Parallel, G1, Shenandoah, ZGC) que permite elegir explícitamente el punto de la curva entre rendimiento agregado y latencia máxima. El .NET CLR sigue un diseño generacional muy parecido, con la peculiaridad del *Large Object Heap* separado. La familia funcional tipada —OCaml, Haskell— usa recolectores generacionales especialmente afinados para tasas de asignación altísimas, porque en un lenguaje inmutable prácticamente todo se asigna y muere joven. En el extremo opuesto, Erlang y Elixir sobre BEAM hacen algo distinto y elegante: cada proceso tiene su **propio heap privado y su propio recolector**, de modo que recolectar un proceso nunca detiene a los demás —el tema de la clase 135—. Y luego está la reacción: Rust demuestra que hay una tercera vía, ni manual ni recolectada, moviendo el problema al compilador; es la clase 132.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 131
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en el GC para recursos que no son memoria** → causa: suponer que un objeto `File` o `Socket` cierra su descriptor al recolectarse → solución: cerrar explícitamente con `try-with-resources` (Java), `using` (C#), `defer` (Go) o `with` (Python). Los finalizadores no sirven: se ejecutan tarde, en un hilo cualquiera, o nunca. Bloch es tajante al respecto en *Effective Java*: evita los finalizadores.
- **Retener referencias sin darte cuenta** → causa: cachés sin política de expiración, listeners registrados y nunca dados de baja, colecciones estáticas que solo crecen, o una clase interna no estática que mantiene viva a su instancia externa → solución: referencias débiles (`WeakHashMap`, `WeakMap`, `weakref`) y auditar qué sigue siendo alcanzable con un analizador de *heap dump*.
- **Llamar al GC a mano para «mejorar» el rendimiento** → causa: creer que forzar la recolección libera memoria antes → solución: en la práctica `System.gc()` o `GC.Collect()` suelen empeorar las cosas: fuerzan una recolección completa —la cara— justo cuando el recolector habría hecho una barata. El runtime tiene mejores heurísticas que tú.
- **Confundir «no hay `free`» con «la memoria no cuesta»** → causa: crear objetos temporales masivamente en un bucle caliente → solución: la tasa de asignación es el principal predictor de la frecuencia de recolección; reutilizar buffers o usar tipos por valor reduce la presión sobre el GC.
- **Medir el consumo del proceso y llamarlo fuga** → causa: la mayoría de runtimes no devuelven la memoria al sistema operativo tras recolectar → solución: comparar el tamaño del *heap vivo* después de una recolección completa, no el RSS del proceso.

## ❓ Preguntas frecuentes

- **¿El GC elimina toda fuga?** No. Elimina la fuga por olvido —la memoria inalcanzable siempre se recupera—, pero no la lógica. Si tu programa mantiene alcanzable un objeto que ya no necesita, el recolector, por definición, no puede tocarlo. En sistemas grandes las fugas lógicas son al menos tan frecuentes como lo eran las manuales.
- **¿Por qué CPython necesita dos mecanismos?** Porque el conteo de referencias, siendo rápido y determinista, no puede liberar ciclos: `a.b = b; b.a = a` deja ambos contadores en 1 para siempre. El recolector generacional del módulo `gc` existe únicamente para detectar y romper esos ciclos; el 95 % de la memoria la libera el contador.
- **¿Por qué el GC de Go no es generacional si la hipótesis generacional es cierta?** Porque en Go muchos objetos de vida corta ni siquiera llegan al heap: el *escape analysis* del compilador los coloca en la pila. Eso vacía buena parte del nicho que el vivero cubriría, y el equipo priorizó un recolector concurrente de pausas mínimas sobre uno de mayor rendimiento agregado. Es una decisión de diseño, no un descuido.
- **¿Un GC hace el programa más lento?** Depende de qué midas. En rendimiento *agregado*, un GC con compactación puede ser más rápido que `malloc`/`free`, porque reservar es avanzar un puntero y liberar es gratis para los objetos muertos. En latencia *máxima*, es peor: introduce pausas que no controlas. Elegir GC o no es elegir qué métrica te importa.
- **¿Y las referencias débiles?** Son referencias que no cuentan para la alcanzabilidad: el recolector puede liberar el objeto aunque existan. Son la herramienta canónica para cachés y para romper ciclos padre-hijo. Rust ofrece el mismo concepto sin GC con `Rc<T>` y `Weak<T>`.

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

> [⏮️ Clase 130](../../parte-8-como-funcionan-los-lenguajes/130-gestion-manual-de-memoria-c-malloc-free/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 132 ⏭️](../../parte-8-como-funcionan-los-lenguajes/132-raii-propiedad-y-prestamos-rust-c-plus-plus/README.md)
