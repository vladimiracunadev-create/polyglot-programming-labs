# Clase 121 — Concurrente: hilos, tareas y canales

> Parte **7 — Paradigmas** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Hasta ahora tus programas hacían una cosa después de otra: una sola línea de ejecución avanzando paso a paso. El paradigma **concurrente** rompe ese supuesto. En vez de una única secuencia, estructuras el programa como varias tareas que progresan a la vez —hilos, goroutines, procesos ligeros— y luego combinas sus resultados. Sumar una lista deja de ser un recorrido lineal para volverse "que cada trabajador sume su trozo y después junto las sumas parciales". El objetivo de esta clase es que distingas dos cosas que se confunden a menudo: la *concurrencia* como forma de estructurar el trabajo, y el *paralelismo* como su ejecución simultánea en varios núcleos.

El terreno tiene dos grandes escuelas, y conviene nombrarlas desde el principio porque toda la clase gira en torno a su tensión. La primera es la **memoria compartida**: los hilos comparten variables y se coordinan con candados, semáforos o monitores. Sebesta le dedica su capítulo 13 (concurrencia), donde los monitores de Hoare aparecen como la disciplina para que ese estado compartido no se corrompa. La segunda es el **paso de mensajes**: las tareas no comparten nada; se comunican enviándose valores por canales. Su raíz teórica es el cálculo *CSP* (Communicating Sequential Processes) de C. A. R. Hoare, y Van Roy y Haridi lo desarrollan en el capítulo 5 de *CTM* como concurrencia por paso de mensajes con agentes.

Go convirtió esa segunda escuela en eslogan: "no comuniques compartiendo memoria; comparte memoria comunicando". La diferencia no es cosmética. La memoria compartida es potente pero traicionera —condiciones de carrera, interbloqueos, código que funciona el 99 % de las veces—; el paso de mensajes elimina clases enteras de esos errores al prohibir el estado compartido. Nuestro laboratorio te deja tocar ambas con las manos: el resultado (la suma) es determinista, pero el *orden* en que las tareas terminan no lo es, y esa es justamente la lección.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la idea de dividir el trabajo.
2. Reconocer hilos, tareas y canales.
3. Combinar resultados parciales.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Concurrencia | Varias cosas a la vez |
| 2 | Dividir y combinar | Repartir el trabajo |
| 3 | Hilos, tareas, canales | Primitivas por lenguaje |

## 📖 Definiciones y características

- **Concurrencia** — estructurar el programa como tareas que progresan a la vez. Clave: aprovecha varios núcleos.
- **Hilo/goroutine** — unidad de ejecución concurrente. Clave: comparte o no memoria según el modelo.
- **Combinar** — reunir los resultados parciales en el final. Clave: la suma total.

La distinción que ordena todo el capítulo es *concurrencia* frente a *paralelismo*. Concurrencia es una propiedad de la **estructura** del programa: descomponerlo en tareas independientes que pueden progresar de forma entrelazada. Paralelismo es una propiedad de la **ejecución**: que esas tareas corran literalmente al mismo tiempo en varios núcleos. Un programa concurrente en una máquina de un solo núcleo se ejecuta entrelazado, no en paralelo, y sin embargo sigue siendo concurrente. Sebesta, en su capítulo 13, traza esta línea con cuidado porque casi todos los errores de concurrencia nacen de confundir ambas: el resultado de nuestro laboratorio no cambia con el número de núcleos, solo su velocidad.

El eje conceptual profundo es *cómo se coordinan las tareas*, y aquí *CTM* ofrece el mapa más limpio. Van Roy y Haridi separan la **concurrencia declarativa** (cap. 4), donde las tareas se comunican por variables de flujo de datos sin estado mutable compartido —y por eso el resultado es determinista—, de la **concurrencia por paso de mensajes** (cap. 5), donde *agentes* independientes se envían mensajes por puertos. Frente a ambas está el modelo de **estado compartido**: hilos que leen y escriben las mismas variables, coordinados por monitores (Hoare) o candados. La suma parcial de nuestro laboratorio, calculada por cada tarea sin tocar la de la otra, es concurrencia declarativa en miniatura: no hay estado compartido que proteger, así que no hay condición de carrera posible.

La raíz teórica del modelo de canales es **CSP** de Hoare: procesos secuenciales que solo interactúan mediante comunicación sincronizada, nunca mediante memoria común. De ahí desciende directamente el diseño de Go —goroutines que se hablan por canales— y su máxima "no comuniques compartiendo memoria; comparte memoria comunicando". Es una inversión de la intuición habitual: en vez de poner un dato en un lugar común y protegerlo con candados, se pasa el dato de mano en mano, y la propiedad de "quién lo tiene ahora" evita el conflicto por construcción.

## 🧩 Situación

Un servicio de miniaturas recibe diez mil fotos y debe redimensionarlas. Hacerlo en un solo hilo, una tras otra, deja siete de los ocho núcleos de la máquina ociosos mientras uno suda. La solución concurrente reparte: divide la cola de fotos entre ocho trabajadores, cada uno procesa su porción en su propio núcleo, y al final se recoge el conteo total. El trabajo termina cerca de ocho veces más rápido, y el resultado —las diez mil miniaturas— es idéntico al del recorrido secuencial. Lo único que cambió fue *cómo se estructuró* la ejecución.

Nuestro laboratorio destila ese patrón "divide y combina" a lo mínimo verificable: dada una lista de enteros, la parte en dos mitades, suma cada mitad por separado y combina las dos sumas parciales. Con la entrada `1 2 3 4`, una tarea suma `1 2` y otra `3 4`; sus parciales `3` y `7` se combinan en `suma=10`. El valor final no depende de cuál tarea acabe primero —por eso es determinista—, pero la estructura ya es concurrente: dos flujos de suma que progresan por separado y confluyen al final.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma total>`
- **Regla:** repartir la lista, sumar por partes, combinar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma=10` |
| `5` | `suma=5` |
| `10 20 30` | `suma=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
dividir lista ; sumar cada parte (concurrente) ; combinar sumas
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
# Visión concurrente: dividir en dos mitades y combinar.
medio = len(nums) // 2
parcial1 = sum(nums[:medio])
parcial2 = sum(nums[medio:])
print(f"suma={parcial1 + parcial2}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const medio = Math.floor(nums.length / 2);
const p1 = nums.slice(0, medio).reduce((a, b) => a + b, 0);
const p2 = nums.slice(medio).reduce((a, b) => a + b, 0);
console.log(`suma=${p1 + p2}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const medio = Math.floor(nums.length / 2);
const p1 = nums.slice(0, medio).reduce((a, b) => a + b, 0);
const p2 = nums.slice(medio).reduce((a, b) => a + b, 0);
console.log(`suma=${p1 + p2}`);
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
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int medio = nums.length / 2;
        long p1 = 0, p2 = 0;
        for (int i = 0; i < medio; i++) p1 += nums[i];
        for (int i = medio; i < nums.length; i++) p2 += nums[i];
        System.out.println("suma=" + (p1 + p2));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int medio = nums.Length / 2;
long p1 = nums.Take(medio).Sum(x => (long) x);
long p2 = nums.Skip(medio).Sum(x => (long) x);
Console.WriteLine($"suma={p1 + p2}");
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
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	medio := len(nums) / 2
	ch := make(chan int, 2)
	sumar := func(parte []int) {
		s := 0
		for _, x := range parte {
			s += x
		}
		ch <- s
	}
	go sumar(nums[:medio])
	go sumar(nums[medio:])
	s1 := <-ch
	s2 := <-ch
	fmt.Printf("suma=%d\n", s1+s2)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let medio = nums.len() / 2;
    let p1: i64 = nums[..medio].iter().sum();
    let p2: i64 = nums[medio..].iter().sum();
    println!("suma={}", p1 + p2);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int medio = n / 2;
    long p1 = 0, p2 = 0;
    for (int i = 0; i < medio; i++) p1 += v[i];
    for (int i = medio; i < n; i++) p2 += v[i];
    printf("suma=%ld\n", p1 + p2);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: el motor decide el paralelismo; aquí, SUM.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$medio = intdiv(count($nums), 2);
$p1 = array_sum(array_slice($nums, 0, $medio));
$p2 = array_sum(array_slice($nums, $medio));
echo "suma=" . ($p1 + $p2) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el reparto del trabajo con el primer caso de [`casos.json`](casos.json): entrada `1 2 3 4`, salida esperada `suma=10`.

**Go** es el que muestra el paradigma en su forma más pura, con goroutines y canales, así que empecemos por él. Tras leer los números en `nums = [1 2 3 4]`, `medio := len(nums) / 2` vale `2`, partiendo la lista en `nums[:2]` (`1 2`) y `nums[2:]` (`3 4`). La línea clave es `ch := make(chan int, 2)`: un canal con capacidad para dos enteros, el buzón por el que las tareas devolverán sus parciales. La función `sumar` recorre su porción, acumula en `s` y —esto es lo esencial— *no* escribe en una variable compartida, sino que envía su resultado por el canal con `ch <- s`. Las dos líneas `go sumar(nums[:medio])` y `go sumar(nums[medio:])` lanzan dos goroutines: dos flujos de ejecución independientes que corren "a la vez". Una sumará `1+2=3`, la otra `3+4=7`.

Ahora viene la parte sutil, la que enseña la diferencia entre concurrencia y determinismo. Las dos líneas `s1 := <-ch` y `s2 := <-ch` reciben del canal. ¿Cuál llega primero, el `3` o el `7`? *No se sabe*: depende de cuál goroutine termine antes, y eso puede variar en cada ejecución. Pero fíjate en que el programa suma `s1 + s2`, y la suma es conmutativa: `3 + 7` y `7 + 3` dan ambos `10`. Ahí está la lección central del laboratorio hecha código: el **orden de ejecución no es determinista, pero el resultado sí lo es**, porque la operación de combinación no depende del orden. Con la entrada `5` (un solo número), `medio` vale `0`, una goroutine suma la lista vacía (`0`) y la otra suma `5`, dando `suma=5`; con `10 20 30`, las mitades `10` y `20 30` producen `10` y `50`, y `suma=60`. Los tres casos de `casos.json` salen exactos.

Nota que el canal hace *dos* trabajos a la vez: transporta el dato **y** sincroniza. `<-ch` bloquea hasta que haya un valor, de modo que el hilo principal no imprime la suma hasta que ambas goroutines hayan entregado su parcial. No hizo falta ningún candado ni ninguna señal de "ya terminé": la comunicación *es* la sincronización. Esto es CSP de Hoare en acción y la encarnación literal de "comparte memoria comunicando".

**Python** resuelve el mismo problema pero revela una decisión de diseño distinta: `parcial1 = sum(nums[:medio])` y `parcial2 = sum(nums[medio:])` calculan las dos mitades *secuencialmente*, sin hilos reales. La visión concurrente está en la estructura —dividir, sumar por partes, combinar con `parcial1 + parcial2`—, pero la ejecución es lineal. Es una elección honesta: el GIL de CPython impide que dos hilos de Python ejecuten bytecode a la vez, así que para trabajo de CPU puro los hilos no acelerarían, y el laboratorio prefiere mostrar la *forma* del algoritmo concurrente sin la maquinaria que no aportaría velocidad aquí. La salida, `suma=10`, es idéntica a la de Go; lo que cambia es que en Go dos flujos progresan de verdad en paralelo y en Python uno solo recorre las dos mitades en orden.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | hilos (Java/C#), goroutines+canales (Go), async (Rust), workers (JS). |
| Semántica | El resultado es determinista; el orden de ejecución no. |
| Paradigmática | SQL delega el paralelismo al motor. |

La diferencia real más honda es el *modelo de coordinación* que cada lenguaje privilegia. Go apuesta por CSP: la única versión que realmente lanza tareas concurrentes en el laboratorio es la suya, con dos goroutines comunicándose por un canal, sin estado compartido. Java y C# vienen de la tradición de memoria compartida —hilos que leen y escriben variables comunes, protegidos por `synchronized`, monitores o `lock`—, aunque sus implementaciones aquí calculan las mitades de forma directa para mantener el foco en la estructura. Rust ofrece ambos mundos y añade una garantía única: su sistema de propiedad (*ownership*) detecta las condiciones de carrera *en tiempo de compilación*, de modo que compartir datos entre hilos sin sincronizar simplemente no compila.

La segunda diferencia es cuánta concurrencia *real* permite el lenguaje. El GIL de CPython serializa el bytecode, por lo que los hilos de Python no aceleran trabajo de CPU (sí de I/O); por eso su implementación es secuencial. JavaScript es de un solo hilo por diseño y necesita *Web Workers* o procesos para paralelizar de verdad. Go y Java, en cambio, corren sus tareas en varios núcleos sin ceremonia. SQL queda en su propio plano: no expresas concurrencia, la *delegas* —el motor decide si paraleliza el `SUM` internamente—, que es concurrencia declarativa llevada al extremo de invisibilidad.

## 🧬 El concepto en la familia

Go (CSP con goroutines y canales) y Erlang/Elixir (el modelo de actores, donde procesos aislados se envían mensajes) son los referentes modernos de la concurrencia segura por paso de mensajes, la línea que arranca en el CSP de Hoare y en los agentes del capítulo 5 de *CTM*. En el otro polo, Java y C# encarnan la tradición de memoria compartida con hilos y monitores que Sebesta documenta en su capítulo 13. Rust ocupa un lugar propio: no elige por ti, sino que hace *seguros* ambos modelos verificando en compilación que ningún dato mutable se comparta sin protección. Saber en cuál de estas familias vive un lenguaje te dice de antemano qué errores de concurrencia puedes cometer en él.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 121
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Estado compartido sin sincronizar** → causa: dos hilos leen-modifican-escriben la misma variable sin candado, y el entrelazado hace que una actualización pise a la otra (condición de carrera); el bug es intermitente y difícil de reproducir → solución: preferir el paso de mensajes (canales, como el `ch` de Go) o dar a cada tarea datos independientes que combine al final, tal como hacen las sumas parciales del laboratorio.
- **Interbloqueo (deadlock)** → causa: dos tareas se esperan mutuamente —A tiene el candado que B necesita y viceversa, o se lee de un canal al que nadie escribirá— y el programa se congela → solución: ordenar la adquisición de candados de forma consistente, cerrar los canales cuando terminan, y preferir canales con buffer cuando el productor no debe bloquearse.
- **Sobre-paralelizar tareas pequeñas** → causa: crear un hilo o goroutine para un trabajo minúsculo hace que el coste de crear, planificar y coordinar supere con creces el cálculo; a veces la versión concurrente es más lenta que la secuencial → solución: paralelizar solo cuando el trabajo por tarea justifica el gasto de coordinación; agrupar (batch) el trabajo pequeño.
- **Suponer un orden de terminación** → causa: escribir código que asume que la primera tarea lanzada termina primero produce resultados erráticos, porque el planificador no garantiza orden → solución: no dependas del orden; usa operaciones de combinación conmutativas/asociativas (como la suma) o sincroniza explícitamente los puntos donde el orden importa.

## ❓ Preguntas frecuentes

- **¿Concurrencia es lo mismo que paralelismo?** No. Concurrencia es cómo *estructuras* el programa: en tareas que pueden progresar de forma entrelazada. Paralelismo es cómo se *ejecuta*: varias tareas a la vez en distintos núcleos. Un programa concurrente en un solo núcleo se entrelaza sin correr en paralelo, y sigue siendo concurrente. Rob Pike lo resumió: "la concurrencia trata de la estructura, el paralelismo de la ejecución".
- **¿Cambia el resultado según qué tarea termine primero?** El *valor* no, si la combinación es conmutativa: en el laboratorio, `3 + 7` y `7 + 3` dan `10` sin importar cuál parcial llegue antes al canal. El *orden de ejecución* sí varía entre corridas. Cuando la combinación no es conmutativa (concatenar en orden, por ejemplo), debes imponer el orden explícitamente.
- **¿Por qué la versión de Python no usa hilos?** Por el GIL (Global Interpreter Lock) de CPython, que impide que dos hilos ejecuten bytecode simultáneamente. Para trabajo de CPU puro como sumar, los hilos no darían velocidad; darían complejidad. Python paraleliza CPU con `multiprocessing` (varios procesos) y usa hilos para I/O. Por eso el laboratorio muestra la *estructura* concurrente sin la maquinaria que no aportaría aquí.
- **¿Memoria compartida o paso de mensajes?** Depende del problema, pero el paso de mensajes (canales, actores) elimina por construcción las condiciones de carrera y suele ser más fácil de razonar, de ahí el lema de Go. La memoria compartida es más eficiente cuando los datos son grandes y no conviene copiarlos, pero exige disciplina de candados. Rust deja usar ambas con seguridad verificada en compilación.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). Cap. 4: concurrencia declarativa; cap. 5: concurrencia por paso de mensajes y agentes.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Cap. 3: estado mutable y el problema de la asignación concurrente.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Cap. 13: concurrencia, hilos, monitores y paso de mensajes.
- C. A. R. Hoare — *Communicating Sequential Processes* (CSP), Comm. ACM (1978): raíz teórica de los canales y las goroutines de Go.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly). Concurrencia, el GIL y `concurrent.futures`.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley). Ítems sobre concurrencia y `java.util.concurrent`.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley). Caps. 8–9: goroutines, canales y memoria compartida.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 120](../../parte-7-paradigmas/120-reactivo-y-flujos-de-datos-streams/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 122 ⏭️](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md)
