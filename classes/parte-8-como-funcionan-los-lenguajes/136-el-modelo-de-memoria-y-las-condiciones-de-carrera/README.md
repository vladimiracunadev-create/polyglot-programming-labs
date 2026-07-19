# Clase 136 — El modelo de memoria y las condiciones de carrera

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Hay una idea profundamente incómoda que esta clase tiene que instalar: **el código que escribes no es el código que se ejecuta**, y en un programa de un solo hilo eso no importa, pero en uno concurrente lo cambia todo. El compilador reordena instrucciones para aprovechar mejor los registros. El procesador las ejecuta fuera de orden y especula sobre los saltos. Las escrituras se quedan en un búfer de escritura antes de llegar a la caché, y las cachés de los distintos núcleos se sincronizan con retraso. Todas esas transformaciones respetan una única garantía: que el resultado observado **desde el propio hilo** sea el mismo. Lo que otro hilo observe queda fuera del contrato, salvo que uses sincronización explícita. Un **modelo de memoria** es precisamente el documento que define ese contrato: qué escrituras de un hilo está garantizado que otro vea, y en qué orden. El ejercicio de la clase —incrementar un contador `n` veces con protección— es el caso mínimo, y su aparente trivialidad es justamente el punto: casi nadie sospecha que `cuenta++` esconda tanto. El *porqué* de estudiarlo es que las carreras producen los bugs más caros del oficio: no deterministas, dependientes de la máquina y de la carga, y capaces de pasar cualquier revisión de código.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir con precisión qué es una **carrera de datos** y en qué se diferencia de una **condición de carrera**.
2. Explicar por qué el compilador y la CPU pueden reordenar accesos a memoria, y qué garantía preservan al hacerlo.
3. Enunciar la relación *happens-before* y decir qué operaciones la establecen.
4. Elegir con criterio entre un mutex, una operación atómica y un diseño sin estado compartido.
5. Explicar qué garantiza `volatile` en Java y por qué no basta para un incremento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Carrera de datos frente a condición de carrera | Dos problemas distintos que se confunden constantemente |
| 2 | Reordenamiento del compilador y de la CPU | Explica por qué la intuición secuencial falla entre hilos |
| 3 | Modelo de memoria y *happens-before* | El contrato formal que define qué se puede observar |
| 4 | Atómicos y compare-and-swap | Sincronización sin candado, apoyada en el hardware |
| 5 | Mutex y visibilidad | Un candado no solo excluye: también publica los cambios |

## 📖 Definiciones y características

Conviene empezar separando dos términos que se usan como sinónimos y no lo son. Una **carrera de datos** (*data race*) es una condición precisa y verificable: dos hilos acceden a la misma posición de memoria, al menos uno escribe, y no hay ninguna relación de sincronización entre ambos accesos. En C, C++, Java, Go y Rust, una carrera de datos es **comportamiento indefinido** o, cuando menos, resultado no especificado: no es «puede que se pierda un incremento», es «el estándar no dice nada sobre lo que ocurre». Una **condición de carrera** (*race condition*) es más general y de nivel más alto: el resultado del programa depende del orden relativo de eventos concurrentes. Un programa puede tener condiciones de carrera sin ninguna carrera de datos —dos transacciones bancarias perfectamente sincronizadas que se aplican en orden distinto según la carga— y ese tipo de fallo no lo detecta ninguna herramienta automática, porque es un problema de lógica, no de memoria.

El fondo del asunto es el **reordenamiento**. El compilador puede mover una escritura fuera de un bucle, mantener un valor en un registro en lugar de releerlo de memoria, o intercambiar dos asignaciones independientes. La CPU puede ejecutar instrucciones fuera de orden y retener escrituras en un búfer antes de propagarlas. Ambos respetan la misma regla —*as-if serial*: el hilo que ejecuta debe observar el mismo resultado que si todo hubiera ocurrido en orden— y ninguno de los dos tiene la obligación de que otro hilo vea lo mismo. Por eso una carrera puede manifestarse como algo aparentemente imposible: un hilo que lee un valor rancio para siempre, porque el compilador cacheó la variable en un registro; o dos hilos que observan las escrituras del otro en órdenes contradictorios.

El **modelo de memoria** de un lenguaje pone orden en esto definiendo la relación **happens-before**: una relación de orden parcial tal que, si la escritura A *happens-before* la lectura B, entonces B está garantizado que ve A. Dentro de un mismo hilo, el orden del programa la establece. Entre hilos, la establecen operaciones concretas: liberar un mutex *happens-before* adquirirlo después; escribir una variable `volatile` (Java) o `atomic` *happens-before* leerla; arrancar un hilo *happens-before* todo lo que ese hilo ejecute; y terminar un hilo *happens-before* el `join` que lo espera. Si no hay una cadena de *happens-before* entre dos accesos y uno de ellos escribe, hay carrera de datos. Esa es la regla operativa, y basta para razonar sobre casi todo el código concurrente que escribirás. El Java Memory Model, especificado en la JSR-133, fue el primer modelo de memoria riguroso de un lenguaje mayoritario y sirvió de base para el de C++11, que a su vez adoptaron C11, Rust y en buena medida Go.

De ahí salen las herramientas. Un **mutex** hace dos cosas, y la segunda se olvida siempre: garantiza exclusión mutua —solo un hilo en la sección crítica— **y** garantiza visibilidad, porque establece la relación *happens-before* entre lo que un hilo escribió antes de soltarlo y lo que otro lee tras adquirirlo. Una **operación atómica** es indivisible por hardware: `incrementAndGet`, `Interlocked.Increment` o `fetch_add` se apoyan en instrucciones como `LOCK XADD` o en un bucle de **compare-and-swap** (leer el valor, calcular el nuevo, intentar escribirlo solo si el antiguo no ha cambiado; reintentar si cambió). Un atómico es mucho más barato que un candado cuando la operación es simple, porque no hay bloqueo ni cambio de contexto; deja de serlo cuando hay mucha contención y los reintentos se disparan.

Un último matiz que causa más confusión que ningún otro: en Java, `volatile` garantiza **visibilidad y orden**, no **atomicidad**. Declarar `volatile int cuenta` asegura que todo hilo vea la última escritura, pero `cuenta++` sigue siendo leer-modificar-escribir y sigue perdiendo incrementos. Para eso hacen falta `AtomicInteger` o `synchronized`. El equivalente en C es que `volatile` **no** sirve para concurrencia en absoluto: fue diseñado para E/S mapeada en memoria, y quien lo usa para sincronizar tiene un bug latente. Lo que hay que usar es `_Atomic` o los `std::atomic` de C++.

## 🧩 Situación

Dos hilos ejecutan un millón de incrementos cada uno sobre el mismo contador. El resultado esperado es 2.000.000; el observado, 1.734.512, distinto en cada ejecución. Pero el fallo más desconcertante es otro, y ocurre con una bandera: un hilo hace `terminado = true` y el otro espera en `while (!terminado) {}`. En un programa secuencial esto funciona; con dos hilos y sin sincronización, el bucle puede no terminar **nunca**, porque el compilador tiene todo el derecho a leer `terminado` una sola vez, guardarla en un registro y convertir el bucle en `while (true)`. Ninguna de las dos cosas se arregla revisando el código con más atención: se arreglan entendiendo el modelo de memoria y declarando explícitamente la sincronización.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** incrementar un contador n veces, con exclusión

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; REPETIR n veces (protegido): cuenta <- cuenta + 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
cuenta = 0
for _ in range(n):  # sección crítica protegida (aquí, secuencial)
    cuenta += 1
print(f"cuenta={cuenta}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        AtomicInteger cuenta = new AtomicInteger(0);
        for (int i = 0; i < n; i++) cuenta.incrementAndGet();
        System.out.println("cuenta=" + cuenta.get());
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Threading;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int cuenta = 0;
for (int i = 0; i < n; i++) Interlocked.Increment(ref cuenta);
Console.WriteLine($"cuenta={cuenta}");
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
	"sync"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var mu sync.Mutex
	cuenta := 0
	for i := 0; i < n; i++ {
		mu.Lock()
		cuenta++
		mu.Unlock()
	}
	fmt.Printf("cuenta=%d\n", cuenta)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;
use std::sync::Mutex;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let cuenta = Mutex::new(0i64);
    for _ in 0..n {
        *cuenta.lock().unwrap() += 1;
    }
    println!("cuenta={}", *cuenta.lock().unwrap());
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long cuenta = 0;
    for (long i = 0; i < n; i++) cuenta++;
    printf("cuenta=%ld\n", cuenta);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa transacciones para la consistencia; aquí, el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$cuenta = 0;
for ($i = 0; $i < $n; $i++) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Los programas son de un solo hilo —y por tanto correctos—, pero cuatro de ellos escriben la protección de todos modos. Esa aparente redundancia es lo interesante: enseña la forma correcta antes de que haya un segundo hilo que la exija.

En **Java**, `AtomicInteger cuenta` con `cuenta.incrementAndGet()` es la respuesta canónica al problema del contador. Por dentro no hay candado: hay un bucle de compare-and-swap sobre un campo `volatile`, que en x86-64 el JIT compila típicamente a una sola instrucción `LOCK XADD`. Comparado con `synchronized`, evita el bloqueo y el cambio de contexto cuando la contención es moderada. Bloch recomienda en *Effective Java* exactamente esta jerarquía: prefiere las utilidades de `java.util.concurrent` a `wait`/`notify` a mano, porque las primitivas de bajo nivel son correctas solo cuando se dominan a la perfección.

En **C#**, `Interlocked.Increment(ref cuenta)` es la traducción literal de la misma idea: `Interlocked` expone las operaciones atómicas del procesador —`Increment`, `Exchange`, `CompareExchange`— y la última es el compare-and-swap crudo con el que se construye cualquier algoritmo sin candados.

En **Go**, la implementación usa `sync.Mutex` con `mu.Lock()` / `mu.Unlock()` alrededor de `cuenta++`. Es la protección más explícita del conjunto y la más didáctica, porque hace visible dónde empieza y acaba la sección crítica. Para este caso concreto, `atomic.AddInt64` sería más eficiente; el mutex se justifica cuando la sección crítica abarca varias operaciones que deben verse como una sola. Merece la pena recordar que Go ofrece un detector de carreras de primera clase: `go run -race` instrumenta cada acceso a memoria y avisa cuando dos hilos tocan la misma dirección sin *happens-before* entre medias. Es la herramienta que convierte esta teoría en algo práctico.

En **Rust**, `Mutex::new(0i64)` muestra la diferencia de diseño más significativa de la clase: el dato **vive dentro** del mutex. `*cuenta.lock().unwrap() += 1` obliga a adquirir el candado para siquiera alcanzar el valor, así que acceder sin bloquear no es un error de disciplina: es un programa que no compila. El `unwrap` maneja el caso de un *mutex envenenado* —un hilo que entró en pánico mientras lo sostenía—, un concepto que Rust modela explícitamente porque el estado protegido puede haber quedado a medias. Y el `MutexGuard` devuelto por `lock()` libera el candado en su destructor: RAII de la clase 132 aplicado a la sincronización, con lo que olvidar el `unlock` es imposible incluso ante un retorno temprano o un pánico.

En **Python**, `cuenta += 1` sin protección es correcto aquí por ser secuencial, y engañoso: con hilos haría falta un `threading.Lock` pese al GIL, porque el intérprete puede ceder entre las instrucciones del incremento. En **JavaScript** y **PHP** la cuestión no se plantea en el modelo estándar (un hilo, un proceso por petición). En **C**, `cuenta++` con `pthreads` sería comportamiento indefinido; la forma correcta es `_Atomic long` de C11. Y **SQL** resuelve todo esto en otra capa: las transacciones y los niveles de aislamiento son el modelo de concurrencia del motor, y `UPDATE t SET n = n + 1` es atómico porque el gestor lo garantiza.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Modelo de memoria especificado | Sí y riguroso (Java desde JSR-133, C# , C11/C++11, Rust, Go); implícito y trivial por ser de un hilo (JS, PHP); definido por transacciones (SQL). |
| Incremento atómico | `AtomicInteger` (Java); `Interlocked.Increment` (C#); `atomic.AddInt64` (Go); `AtomicI64` (Rust); `_Atomic` (C); no aplica (JS, PHP). |
| Exclusión mutua | `synchronized` / `ReentrantLock` (Java); `lock` (C#); `sync.Mutex` (Go); `Mutex<T>` con el dato dentro (Rust); `pthread_mutex_t` (C); `threading.Lock` (Python). |
| ¿Se puede acceder al dato sin el candado? | Sí, y nadie lo impide (Java, C#, Go, C, Python); **no**, el tipo lo prohíbe (Rust). |
| Liberación del candado | Manual y propensa a olvidos (C, Go con `defer` como mitigación); automática por bloque (`synchronized`, `lock`, `with`); automática por destructor (Rust, C++). |
| Detección de carreras | En compilación (Rust); en ejecución con instrumentación (`-race` en Go, ThreadSanitizer en C/C++); prácticamente inexistente (Java, C#, Python). |
| Palabra `volatile` | Visibilidad y orden, sin atomicidad (Java, C#); **inútil para concurrencia**, es para E/S mapeada (C, C++). |

## 🧬 El concepto en la familia

La historia de los modelos de memoria es la historia de descubrir que el problema era más difícil de lo que parecía. Java fue el primer lenguaje mayoritario en especificar uno, y su primera versión resultó tener defectos serios que obligaron a rehacerlo en 2004 con la JSR-133: de ahí salieron la semántica moderna de `volatile` y la garantía de publicación segura de los campos `final`. C++11 formalizó después un modelo más rico, con órdenes de memoria graduados (`relaxed`, `acquire`, `release`, `seq_cst`) que permiten pagar solo por la sincronización que de verdad necesitas —y que casi nadie debería usar más allá de `seq_cst`, el modo por defecto y el único fácil de razonar—. C11 y Rust heredaron ese vocabulario casi literalmente. Go adoptó un modelo más simple y prescriptivo, resumido en su propia documentación con una recomendación honesta: si tienes que preguntarte por el modelo de memoria, estás siendo demasiado listo; usa canales o `sync`. La familia funcional evita el problema por la raíz: en Haskell o Clojure los datos son inmutables, así que compartirlos no puede producir carreras, y la mutación se canaliza por construcciones controladas como la memoria transaccional por software (STM) o los `atom`. Rust, una vez más, es el caso singular: no evita la memoria compartida, sino que hace la carrera de datos **inexpresable** en el subconjunto seguro del lenguaje, mediante los rasgos `Send` y `Sync` y las reglas de préstamo de la clase 132. Es, hasta la fecha, el único lenguaje de sistemas mayoritario que ofrece esa garantía en compilación.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 136
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Incrementar sin proteger** → causa: `cuenta++` es leer-modificar-escribir y dos hilos pueden entrelazarse → solución: tipo atómico (`AtomicInteger`, `Interlocked`, `atomic.AddInt64`, `_Atomic`) o candado alrededor.
- **Creer que `volatile` hace atómico un incremento** → causa: confundir visibilidad con atomicidad → solución: `volatile` en Java o C# garantiza que veas la última escritura, pero no que tu lectura-modificación-escritura sea indivisible. Usa un atómico. Y en C, `volatile` no aporta **nada** para concurrencia: es para registros de hardware.
- **Proteger la escritura y no la lectura** → causa: suponer que leer no puede romper nada → solución: sin sincronización en el lector, el compilador puede cachear el valor en un registro indefinidamente y el bucle `while (!terminado)` no acabar nunca. Ambos lados deben participar en la relación *happens-before*.
- **Sincronizar sobre objetos distintos** → causa: dos métodos que protegen el mismo dato con candados diferentes → solución: la exclusión mutua solo funciona si todos acuerdan el **mismo** candado. Documentar qué candado protege qué invariante, y en Java evitar `synchronized` sobre objetos públicos o sobre `String` internados.
- **Tomar candados en orden inconsistente** → causa: interbloqueo cuando dos hilos adquieren A y B en órdenes opuestos → solución: orden global de adquisición, o un solo candado de grano más grueso. Y nunca hacer E/S ni llamar a código ajeno con un candado tomado.
- **Confiar en pruebas para descartar carreras** → causa: una carrera puede no manifestarse en un millón de ejecuciones en tu máquina y aparecer el primer día en un servidor con más núcleos → solución: usar detectores dinámicos (`go run -race`, `-fsanitize=thread`) y razonar sobre *happens-before* en lugar de sobre observaciones.
- **Escribir algoritmos sin candados por rendimiento** → causa: creer que compare-and-swap a mano es siempre más rápido → solución: con contención alta, un bucle de CAS puede ser peor que un mutex por los reintentos, y la corrección de los algoritmos *lock-free* es notoriamente difícil (el problema ABA, entre otros). Usa las estructuras concurrentes de la biblioteca antes que escribir la tuya.

## ❓ Preguntas frecuentes

- **¿Toda variable compartida necesita protección?** Toda variable que al menos un hilo **escriba** mientras otro accede a ella, sí. Las variables inmutables tras su publicación no la necesitan —de ahí la potencia de la inmutabilidad como estrategia de concurrencia— y las que solo toca un hilo, tampoco.
- **¿Atómico o candado?** Atómico cuando la operación es una sola y el hardware la soporta: un contador, una bandera, un puntero que se intercambia. Candado cuando hay que mantener una invariante entre **varias** variables, o cuando la sección crítica hace más de una cosa. Regla práctica: si necesitas que dos actualizaciones se vean como una, ningún atómico te sirve.
- **¿Por qué el compilador tiene permiso para romper mi código?** No lo tiene: tiene permiso para transformar el código respetando lo que **un solo hilo** puede observar, que es la garantía que el estándar le exige. Si tu programa depende de que otro hilo observe algo, el estándar te obliga a **declararlo** con una operación de sincronización. Sin esa declaración, el programa está mal formado, aunque parezca funcionar.
- **¿Qué es exactamente *happens-before*?** Un orden parcial entre operaciones. Si A *happens-before* B, entonces B ve los efectos de A. Lo establecen: el orden del programa dentro de un hilo, soltar/adquirir un mutex, escribir/leer una variable atómica o `volatile`, arrancar un hilo, y hacer `join` sobre él. Si no puedes trazar esa cadena entre dos accesos y uno escribe, tienes una carrera de datos.
- **¿Sirve de algo un `sleep` para evitar una carrera?** No. Cambia la probabilidad de la colisión, no su posibilidad, y solo hace el bug más difícil de reproducir. Lo mismo vale para el `print` que «arregla» el problema al depurar: no lo arregla, lo esconde.
- **¿Y si simplemente evito compartir estado?** Es la mejor respuesta cuando se puede. Los actores de la clase 135 y los canales de la 134 existen justamente para eso, y la inmutabilidad de la familia funcional también. La mayoría de las carreras de datos se previenen mejor con un diseño que no las permita que con candados bien puestos.

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

> [⏮️ Clase 135](../../parte-8-como-funcionan-los-lenguajes/135-actores-y-paso-de-mensajes-modelo-beam/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 137 ⏭️](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md)
