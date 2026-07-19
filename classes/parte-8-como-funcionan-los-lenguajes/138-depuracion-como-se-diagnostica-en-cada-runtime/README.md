# Clase 138 — Depuración: cómo se diagnostica en cada runtime

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Esta clase cierra la parte devolviendo todo lo anterior a la práctica. Depurar es el proceso de **cerrar la distancia entre el modelo mental que tienes del programa y lo que el programa hace realmente**, y todo lo que has visto en las quince clases previas —fases de compilación, pila y marcos, heap, punteros, GC, hilos, modelo de memoria— es exactamente el vocabulario que hace posible esa reconciliación. Un depurador no es una herramienta mágica: es una ventana a las estructuras que ya conoces. Un *backtrace* es la pila de la clase 127. Un `NullPointerException` es una referencia de la 129. Una pausa inexplicable es el recolector de la 131. Una salida no determinista es la carrera de la 136. El ejercicio —inspeccionar `n`, `n²` y `n³`— es la operación elemental que un depurador realiza al pausar: leer el estado en un punto concreto. El *porqué* de estudiarlo con seriedad es que depurar es, medido en horas, la actividad principal de un programador profesional, y sin embargo casi nadie la aprende como método: se aprende por imitación y a base de tanteo. Hacerla explícita —hipótesis, observación, bisección— es lo que separa dos horas de dos días.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Describir el método científico aplicado a la depuración: hipótesis falsable, observación, bisección.
2. Explicar cómo funciona por dentro un punto de ruptura y qué papel juega la información de depuración.
3. Interpretar un *backtrace* relacionándolo con la pila de llamadas y sus marcos.
4. Elegir la herramienta adecuada según la clase de fallo: depurador, sanitizador, perfilador, volcado de heap o registro.
5. Explicar por qué el código optimizado es más difícil de depurar y qué es un heisenbug.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Depuración como método | Hipótesis y bisección en lugar de cambios al azar |
| 2 | El depurador por dentro | Puntos de ruptura, símbolos y control del proceso |
| 3 | Leer un *backtrace* | La pila de la clase 127, hecha visible |
| 4 | Más allá del depurador | Sanitizadores, perfiladores, volcados y trazas estructuradas |
| 5 | Fallos que se esconden | Heisenbugs, optimizaciones y no determinismo |

## 📖 Definiciones y características

Antes que la herramienta viene el **método**. Depurar bien es aplicar el método científico: observar el síntoma, formular una **hipótesis falsable** («el contador se pasa de largo porque la condición usa `<=`»), diseñar una observación que la refute o la confirme, y repetir. Lo que no funciona —y lo que casi todo el mundo hace bajo presión— es cambiar cosas al azar hasta que el síntoma desaparece, porque eso a menudo lo esconde en lugar de eliminarlo. La técnica más rentable que existe es la **bisección**: reducir a la mitad el espacio de búsqueda en cada paso, ya sea comentando la mitad del código, reduciendo la entrada hasta el caso mínimo que reproduce el fallo, o —la versión más poderosa— `git bisect`, que localiza en unos pocos pasos el commit exacto que introdujo el problema entre miles. Hunt y Thomas insisten en *The Pragmatic Programmer* en el requisito previo a todo esto: conseguir una **reproducción fiable**. Un fallo que no sabes reproducir no puedes saber que lo has arreglado.

Un **depurador** es un programa que controla la ejecución de otro. En Unix se apoya en una llamada al sistema, `ptrace`, que le permite detener el proceso objetivo, leer y escribir su memoria y sus registros, y reanudarlo. Un **punto de ruptura** por software se implementa de una forma sorprendentemente física: el depurador sustituye el primer byte de la instrucción por una instrucción de trampa (`INT 3` en x86, un solo byte, `0xCC`), guarda el byte original y espera; cuando la CPU la ejecuta, genera una excepción que devuelve el control al depurador, que restaura el byte y te muestra el estado. Los puntos de ruptura **por hardware** —limitados a unos pocos por el número de registros de depuración— hacen lo mismo sin modificar el código, y permiten además los *watchpoints*: detener el programa cuando una dirección de memoria **cambia**, que es la única forma razonable de encontrar quién está corrompiendo un dato.

Para que nada de esto sea legible hace falta la **información de depuración**: las tablas (formato DWARF en Unix, PDB en Windows) que el compilador emite con `-g` y que traducen direcciones de máquina a líneas de código, y posiciones de pila a nombres de variables. Sin ellas, el depurador solo ve direcciones. Y aquí aparece una tensión importante: con optimizaciones activadas (`-O2`), el compilador reordena instrucciones, elimina variables enteras y funde funciones por *inlining*, de modo que el depurador salta erráticamente entre líneas y te informa de que una variable ha sido «optimizada y no está disponible». No es un fallo de la herramienta: es que el código que se ejecuta ya no se corresponde línea a línea con el que escribiste. Por eso se depura en `-Og` o `-O0`, y por eso los bugs que solo aparecen en compilación optimizada son especialmente desagradables.

El **backtrace** es la lectura más valiosa que ofrece cualquier runtime, y es exactamente la pila de la clase 127 impresa: la secuencia de marcos activos, del más reciente al más antiguo, con sus funciones, sus líneas y a menudo sus argumentos. Leerlo bien tiene truco: el marco superior es *dónde explotó*, no *dónde está el bug*; el bug suele estar más abajo, en el marco que preparó el dato malo. Y en las excepciones encadenadas de Java o Python, la causa raíz está al final (`Caused by:`, «The above exception was the direct cause»), no al principio.

Por último, el depurador no es la única herramienta y a menudo no es la mejor. Para corrupción de memoria y carreras, los **sanitizadores** —AddressSanitizer, ThreadSanitizer, el `-race` de Go, Valgrind— instrumentan el programa y detectan el fallo en el instante en que ocurre, no cuando se manifiesta cien líneas después. Para rendimiento, los **perfiladores** (`perf`, `pprof`, JFR, `py-spy`) muestran dónde se va el tiempo, algo que ningún depurador revela. Para fugas y consumo, los **volcados de heap**. Y para sistemas en producción, donde no puedes pausar nada, la herramienta es el **registro estructurado** con trazas correlacionadas: la observabilidad es depuración diferida sobre un proceso que no puedes detener.

## 🧩 Situación

Un servicio devuelve un total incorrecto una vez de cada mil peticiones. Poner un punto de ruptura es inútil —no sabes en qué petición—, y añadir un `print` en el bucle caliente cambia el ritmo y el fallo desaparece: un **heisenbug** de manual, síntoma típico de una condición de carrera de la clase 136. El camino correcto no pasa por el depurador: pasa por reducir el caso hasta reproducirlo de forma fiable, correr el detector de carreras del runtime, o instrumentar con registro estructurado y correlacionar. Saber **qué herramienta** corresponde a cada clase de síntoma es la mitad de la habilidad; la otra mitad es tener el modelo mental —pila, heap, hilos, GC— que permite formular una hipótesis que valga la pena comprobar. Inspeccionar `n`, `n²` y `n³` en un punto es la forma mínima de esa observación.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `valor=<n> cuadrado=<n²> cubo=<n³>`
- **Regla:** inspeccionar n, n² y n³

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `valor=3 cuadrado=9 cubo=27` |
| `2` | `valor=2 cuadrado=4 cubo=8` |
| `5` | `valor=5 cuadrado=25 cubo=125` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n, n*n, n*n*n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"valor={n} cuadrado={n * n} cubo={n * n * n}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("valor=" + n + " cuadrado=" + (n * n) + " cubo=" + (n * n * n));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"valor={n} cuadrado={n * n} cubo={n * n * n}");
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
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("valor=%d cuadrado=%d cubo=%d\n", n, n*n, n*n*n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("valor={} cuadrado={} cubo={}", n, n * n, n * n * n);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("valor=%ld cuadrado=%ld cubo=%ld\n", n, n * n, n * n * n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se inspeccionan los valores calculados.
WITH nums(n) AS (VALUES (3), (2), (5))
SELECT printf('valor=%d cuadrado=%d cubo=%d', n, n * n, n * n * n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "valor=$n cuadrado=" . ($n * $n) . " cubo=" . ($n * $n * $n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

El cálculo es idéntico en los diez lenguajes; lo que cambia radicalmente es **cómo lo observarías** si el resultado no fuera el esperado.

En **Python**, el punto de entrada al depurador cabe en una línea: `breakpoint()` (o `import pdb; pdb.set_trace()`) detiene la ejecución ahí y abre una consola con el estado vivo. Al ser interpretado, no hace falta recompilar nada ni activar ninguna opción: el intérprete conserva los nombres, los tipos y el árbol de objetos. Desde ahí, `p n`, `pp locals()`, `w` para ver la pila y `n`/`s`/`c` para avanzar. La contrapartida de esa comodidad es que la propia flexibilidad del lenguaje esconde errores hasta la ejecución, como vimos en la clase 137. Para producción, `py-spy` permite inspeccionar la pila de un proceso Python vivo sin detenerlo ni modificarlo.

En **C** y en **Rust**, el binario compilado no tiene nombres a menos que los pidas: hay que compilar con `-g` (o `cargo build`, que ya incluye la información en el perfil de depuración) para que `gdb` o `lldb` puedan traducir direcciones a líneas. La sesión típica es `gdb ./main`, luego `break main.c:10`, `run`, `print n`, `bt` para el *backtrace*, `watch cuadrado` para detenerse cuando esa variable cambie. Rust añade la ventaja de que `rustc` emite metadatos que permiten a `rust-gdb` imprimir `Vec` y `Option` de forma legible en lugar de mostrar su representación cruda. Y para esta familia, los sanitizadores suelen ser más productivos que el depurador: `cc -fsanitize=address,undefined` convierte una corrupción silenciosa en un mensaje preciso en el momento exacto en que ocurre.

En **Java** y **C#**, la depuración se apoya en el runtime, no en el sistema operativo: la JVM expone JDWP —un protocolo por el que un depurador se conecta al proceso, incluso remoto, con `-agentlib:jdwp=...`— y .NET tiene su equivalente. Eso hace natural algo que en C es complicado: conectarse a un proceso que ya está corriendo en otra máquina. Ambas plataformas ofrecen además el instrumental de observación que no existe en los binarios nativos: volcados de heap analizables, Java Flight Recorder para grabar la actividad del runtime con impacto mínimo, y contadores de GC que explican las pausas de la clase 131.

En **Go**, el depurador es Delve (`dlv debug`), diseñado con conocimiento del runtime: sabe qué es una goroutine y permite `goroutines` y `goroutine N bt` para inspeccionar los miles de pilas concurrentes de la clase 134 —algo que `gdb` no entiende bien porque las goroutines no son hilos del sistema—. Pero la herramienta más característica de Go es otra: `pprof`, integrado en la biblioteca estándar, que da perfiles de CPU, memoria, bloqueo y contención sin instalar nada.

En **JavaScript** y **TypeScript**, el depurador vive en el mismo motor que ejecuta el código: `node --inspect` abre el protocolo de Chrome DevTools, con la peculiaridad de TypeScript de que se depura el JavaScript generado y hacen falta *source maps* para volver a ver las líneas originales. Un `debugger;` en el código es el punto de ruptura declarativo. En **PHP**, Xdebug proporciona el mismo servicio, y sus trazas de pila mejoradas son la razón principal por la que se instala.

En **SQL** no hay pila ni variables que inspeccionar: se depura el **plan**. `EXPLAIN` muestra qué estrategia eligió el planificador y `EXPLAIN ANALYZE` la contrasta con la ejecución real. La discrepancia entre filas estimadas y filas reales es la señal diagnóstica más útil que existe en bases de datos, y casi siempre apunta a estadísticas obsoletas o a un índice ausente.

## 🔬 Comparación

| Rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Depurador de referencia | `pdb` / `debugpy` (Python); Chrome DevTools vía `--inspect` (JS/TS); JDWP y el IDE (Java); `vsdbg` (C#); Delve (Go); `gdb` / `lldb` / `rust-gdb` (Rust, C); Xdebug (PHP); `EXPLAIN` (SQL). |
| ¿Requiere compilar distinto? | Sí, `-g` y preferiblemente sin optimizar (C, Rust, Go); no, el runtime ya lo soporta (Python, JS, Java, C#, PHP). |
| Backtrace por defecto ante un fallo | Completo y legible (Python, Java, C#, JS, PHP, Go en el pánico); ninguno —solo «segmentation fault»— salvo que actives volcados de núcleo (C); pánico con traza si `RUST_BACKTRACE=1` (Rust). |
| Detección de corrupción y carreras | AddressSanitizer / ThreadSanitizer / Valgrind (C, C++); `-race` integrado (Go); imposible por diseño en el subconjunto seguro (Rust); no aplica (los gestionados de un hilo). |
| Perfilado | `pprof` de serie (Go); JFR y async-profiler (Java); `perf` (C, Rust); `cProfile` / `py-spy` (Python); DevTools (JS); `EXPLAIN ANALYZE` (SQL). |
| Depuración en producción | Conexión remota por JDWP (Java); `py-spy` sobre proceso vivo (Python); `pprof` por HTTP (Go); volcados de núcleo *post mortem* (C, Rust); registro estructurado en todos. |

## 🧬 El concepto en la familia

Las familias se agrupan aquí por lo que el binario o el runtime conserva del programa original. Los lenguajes que compilan a código máquina —C, C++, Rust, Go— dependen de información de depuración externa (DWARF, PDB) que el compilador emite aparte, y por eso su experiencia varía tanto entre compilar para depurar y compilar para producción; a cambio, tienen acceso al nivel más bajo posible: desensamblado, registros, memoria cruda, y una familia de sanitizadores que ningún runtime gestionado necesita. Las plataformas con máquina virtual —JVM y .NET— conservan metadatos completos en el propio artefacto y exponen protocolos de depuración y de observación (JDWP, JFR, volcados de heap, contadores de GC) que permiten diagnosticar sistemas en producción sin detenerlos: es su ventaja más subestimada. Los lenguajes dinámicos conservan absolutamente todo —nombres, tipos, el árbol de objetos vivo— y ofrecen la introspección más rica en tiempo de ejecución (`inspect` en Python, el REPL de Node), lo que hace la exploración interactiva especialmente productiva; el precio, ya visto en la clase 137, es que muchos errores solo existen al ejecutar. La familia Lisp lleva esto al extremo con el depurador condicional de Common Lisp, donde ante un error puedes reparar el estado y **reanudar** desde el punto del fallo, algo que casi ningún lenguaje moderno ofrece. Y la familia declarativa se depura en otro plano: en SQL o Prolog no se sigue una ejecución paso a paso, se examina la estrategia que el motor eligió. La lección transversal, y buen cierre para la parte, es que la herramienta cambia pero el método no: reproducir de forma fiable, formular una hipótesis, bisecar, y confiar en el modelo mental de lo que ocurre bajo el código antes que en la intuición.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 138
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Cambiar código al azar hasta que el síntoma desaparece** → causa: no hay hipótesis, solo tanteo → solución: formular una hipótesis falsable antes de tocar nada y diseñar la observación que la refute. Un síntoma que desaparece sin que sepas por qué suele estar escondido, no resuelto.
- **Empezar a depurar sin una reproducción fiable** → causa: perseguir un fallo que aparece a veces → solución: primero, reducir la entrada hasta el caso mínimo que lo provoca de forma consistente. Sin eso no puedes saber si lo arreglaste ni cuándo has terminado.
- **Leer solo la primera línea del *backtrace*** → causa: el marco superior es donde explotó, no donde está el bug → solución: recorrer la pila hacia abajo hasta el primer marco de **tu** código, y en excepciones encadenadas buscar la causa raíz al final (`Caused by:`).
- **Depurar código compilado con optimizaciones** → causa: `-O2` funde funciones, reordena líneas y elimina variables, y el depurador salta erráticamente → solución: recompilar con `-Og` o `-O0` y `-g`. Y si el bug **solo** aparece optimizado, sospechar de comportamiento indefinido, no del compilador.
- **Llenar el código de `print` y olvidarlos** → causa: depuración por impresión sin limpieza → solución: usar el sistema de registro con niveles (`debug`, `info`), de modo que las trazas queden pero se puedan silenciar; y el depurador cuando el estado es complejo.
- **Usar el depurador para problemas que no le corresponden** → causa: intentar encontrar una fuga de memoria, una carrera o un cuello de botella pausando el programa → solución: cada síntoma tiene su herramienta. Corrupción y carreras, sanitizadores; lentitud, perfilador; consumo, volcado de heap; producción, trazas estructuradas.
- **Depurar sin control de versiones a mano** → causa: buscar a ciegas cuándo se rompió → solución: `git bisect` localiza el commit culpable en logaritmo del número de commits. Si tienes una prueba que falla, `git bisect run` lo hace solo.
- **Culpar al compilador, a la biblioteca o al sistema operativo** → causa: agotamiento tras horas sin resultado → solución: en la inmensa mayoría de los casos el bug es tuyo. Vale la pena volver a comprobar las suposiciones más básicas —que el binario que ejecutas es el que compilaste, que el archivo que editas es el que se carga— antes de sospechar de la plataforma.

## ❓ Preguntas frecuentes

- **¿`print` o depurador?** Ambos, según el caso. El `print` gana cuando quieres ver una secuencia de valores a lo largo del tiempo o cuando pausar altera el comportamiento (concurrencia, tiempo real). El depurador gana cuando el estado es complejo y no sabes de antemano qué mirar: puedes inspeccionar cualquier cosa sin recompilar, subir por la pila y evaluar expresiones en el contexto del fallo.
- **¿Qué es un punto de ruptura condicional y por qué importa?** Un punto de ruptura que solo detiene el programa si se cumple una expresión (`break main.c:42 if n > 1000`). Es lo que hace viable depurar un bucle de un millón de iteraciones que falla en la 999.998. Su primo, el *watchpoint*, detiene cuando una dirección de memoria cambia, y es casi la única forma de encontrar quién corrompe un dato.
- **¿Qué es un heisenbug?** Un fallo que cambia o desaparece al observarlo. Suele deberse a que el acto de medir altera lo que hace el programa: un `print` introduce E/S y sincronización y cambia el entrelazado de los hilos; compilar sin optimizar cambia la disposición de la pila y encubre un desbordamiento de búfer. Su presencia es en sí misma una pista fuerte: apunta a concurrencia o a comportamiento indefinido.
- **¿Cómo se depura SQL?** Con `EXPLAIN` para ver el plan que eligió el optimizador y `EXPLAIN ANALYZE` para contrastarlo con la ejecución real. La señal más útil es la divergencia entre filas estimadas y filas reales: cuando el planificador se equivoca por órdenes de magnitud, casi siempre son estadísticas desactualizadas o un índice que falta. Para la lógica, descomponer la consulta en CTE y comprobar cada paso por separado.
- **¿Cómo se depura algo en producción, donde no puedo pausar nada?** Con observabilidad: registro estructurado en formato consultable, identificadores de traza que correlacionen las etapas de una misma petición, métricas y muestreo continuo de perfiles. También hay herramientas de muestreo no intrusivo (`py-spy`, `pprof` por HTTP, `async-profiler`) y, tras un fallo terminal, el análisis *post mortem* de un volcado de núcleo o de heap. La regla es preparar la observabilidad **antes** de necesitarla.
- **¿Cuál es la mejor inversión de tiempo en depuración?** Aprender `git bisect` y aprender a reducir un caso de prueba. Las dos son bisección, la técnica más rentable que existe, y ninguna depende del lenguaje que uses.

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

> [⏮️ Clase 137](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 139 ⏭️](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md)
