# Clase 152 — Rendimiento y perfilado (profiling)

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Hay una regla que separa a los ingenieros de rendimiento de los aficionados, y McConnell la enuncia sin rodeos en *Code Complete*: **«measure, don't guess»** —mide, no adivines—. La intuición humana sobre dónde gasta el tiempo un programa es notoriamente mala; el cuello de botella casi nunca está donde uno cree. Knuth lo dijo antes con su frase más citada y más malentendida: «la optimización prematura es la raíz de todo mal». No significa «no optimices»; significa que optimizar *sin datos* es tan probable que empeore la legibilidad como que mejore la velocidad. El perfilado es el instrumento que convierte la adivinanza en medición.

Esta clase introduce el perfilado por su puerta más humilde: **contar operaciones**. El programa suma los enteros de 1 a *n* y, mientras lo hace, lleva la cuenta de cuántas sumas ejecuta. Ese contador es un perfilador en miniatura: te dice que el trabajo crece linealmente con *n* —es O(*n*)—, y esa curva es exactamente lo que un perfilador real revelaría al graficar tiempo contra tamaño de entrada. Hunt y Thomas, en *The Pragmatic Programmer*, insisten en «estimar el orden del algoritmo» antes de tocar nada: saber si algo es O(*n*), O(*n* log *n*) o O(*n²*) importa mucho más que cualquier microoptimización, porque la complejidad domina cuando la entrada crece y las constantes no.

Pero la clase también quiere que veas la otra cara: **complejidad frente a constantes**. Dos algoritmos O(*n*) pueden diferir diez veces en velocidad real por culpa de constantes ocultas —fallos de caché, asignaciones de memoria, saltos mal predichos—. La complejidad te dice cómo escala; solo el perfilador te dice cuánto cuesta *hoy*, en *esta* máquina, con *estos* datos. Por eso todo lenguaje serio trae perfiladores, y conviene conocer los del ecosistema propio.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Distinguir** entre estimar la complejidad (contar operaciones) y medir el tiempo real (cronometrar/perfilar).
2. **Explicar** por qué se perfila antes de optimizar y qué es un cuello de botella.
3. **Nombrar** el perfilador idiomático de al menos cuatro lenguajes y para qué sirve cada uno.
4. **Razonar** sobre la diferencia entre complejidad asintótica y constantes reales.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Medir antes de optimizar | La intuición sobre el cuello de botella suele fallar |
| 2 | Conteo de operaciones | Estima la complejidad: cuánto trabajo se hace |
| 3 | Complejidad vs. constantes | La curva escala; las constantes deciden el coste hoy |
| 4 | Perfiladores por lenguaje | Cada ecosistema tiene su instrumento |

## 📖 Definiciones y características

El **perfilado** es medir cómo un programa consume tiempo y recursos: cuánto tarda cada función, cuántas veces se llama, cuánta memoria asigna. Hay dos familias. El perfilador de **muestreo** (*sampling*) interrumpe el programa muchas veces por segundo y anota qué se estaba ejecutando; es barato y no distorsiona apenas el tiempo, por eso py-spy, perf o async-profiler pueden correr sobre producción. El de **instrumentación** inserta contadores en cada entrada y salida de función; es preciso pero ralentiza y sesga (el propio instrumento cuesta). El contador `ops` de esta clase es instrumentación manual llevada al extremo mínimo.

Una **operación** es la unidad de trabajo que decides contar —una suma, una comparación, un acceso a memoria—. Contarlas da la **complejidad**: cómo crece el trabajo con el tamaño de la entrada. El **cuello de botella** (*bottleneck*) es la porción de código que domina el coste total; la ley de Amdahl formaliza por qué optimizar lo que solo ocupa el 5 % del tiempo no puede darte más de un 5 % de mejora, mientras que atacar el 80 % puede transformarlo todo. McConnell dedica un capítulo entero a esto: primero perfila para hallar el bottleneck, luego optimiza solo ahí, y vuelve a medir para confirmar que ganaste —a veces una «optimización» es más lenta por interacciones con el compilador o la caché.

## 🧩 Situación

Un endpoint de tu API tarda 800 ms y el equipo culpa a la base de datos. Antes de reescribir consultas, lo perfilas: `py-spy top` sobre el proceso en vivo, sin reiniciar nada, revela que el 70 % del tiempo se va en serializar la respuesta a JSON, no en la consulta —que apenas cuesta 40 ms—. Habrías pasado dos días optimizando lo que no importaba. Con el perfilador, cambias el serializador y bajas a 300 ms en una tarde. Este es el patrón profesional: el perfilador reorienta el esfuerzo hacia donde el coste realmente vive. El ejercicio de contar sumas es ese mismo hábito reducido a su núcleo: mirar el trabajo *medido*, no el imaginado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `operaciones=<n> resultado=<1+...+n>`
- **Regla:** sumar 1..n contando cada suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `operaciones=5 resultado=15` |
| `1` | `operaciones=1 resultado=1` |
| `3` | `operaciones=3 resultado=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
ops <- 0 ; suma <- 0 ; PARA i de 1 a n: suma+=i ; ops++
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

El bucle `for i in range(1, n + 1)` recorre 1..*n*; en cada vuelta suma `i` a `suma` y lleva la cuenta en `ops`. Al terminar, `ops` vale exactamente *n*: acabas de medir que el algoritmo es O(*n*). Un detalle de rendimiento que Ramalho subraya en *Fluent Python*: este bucle en Python puro es lento comparado con `sum(range(1, n+1))`, porque cada iteración pasa por el intérprete. La forma de descubrirlo no es adivinar, sino perfilar: `python -m cProfile main.py` te da el desglose por función, y `py-spy record -o perfil.svg -- python main.py` produce un **flamegraph** —un gráfico donde el ancho de cada barra es el tiempo acumulado, la manera más rápida de ver el cuello de botella de un vistazo.

```python
import sys

n = int(sys.stdin.readline())
ops = 0
suma = 0
for i in range(1, n + 1):
    suma += i
    ops += 1
print(f"operaciones={ops} resultado={suma}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

En la JVM el perfilado es especialmente interesante porque el compilador JIT reescribe el código en caliente. Un bucle como este, tras miles de iteraciones, puede ser optimizado —incluso *vectorizado* o reducido a la fórmula cerrada— por el compilador C2. Por eso medir en Java exige cuidado: hay que «calentar» la JVM. Las herramientas idiomáticas son **JFR** (Java Flight Recorder, integrado en el JDK) y **async-profiler**, que producen flamegraphs de bajísimo coste. Para microbenchmarks fiables, Bloch y la comunidad recomiendan **JMH**, que gestiona el calentamiento y evita que el JIT elimine código «muerto» cuyo resultado no se usa.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long ops = 0, suma = 0;
        for (int i = 1; i <= n; i++) {
            suma += i;
            ops += 1;
        }
        System.out.println("operaciones=" + ops + " resultado=" + suma);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long ops = 0, suma = 0;
for (int i = 1; i <= n; i++) {
    suma += i;
    ops += 1;
}
Console.WriteLine($"operaciones={ops} resultado={suma}");
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
	ops, suma := 0, 0
	for i := 1; i <= n; i++ {
		suma += i
		ops++
	}
	fmt.Printf("operaciones=%d resultado=%d\n", ops, suma)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

Rust y C son los lenguajes donde las **constantes** brillan: sin recolector de basura ni intérprete, este bucle compila a instrucciones máquina casi directas, y el optimizador de LLVM probablemente lo reemplace por la fórmula *n*(*n*+1)/2. Para medir de verdad en Rust, la herramienta idiomática es **criterion**, una biblioteca de benchmarking estadístico que ejecuta muchas muestras, descarta valores atípicos y reporta intervalos de confianza —justo el rigor que *The Pragmatic Programmer* pide para no engañarte con una sola medición ruidosa. Para perfilar el binario ya compilado sirven `perf` y los flamegraphs, igual que en C.

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut ops = 0i64;
    let mut suma = 0i64;
    for i in 1..=n {
        suma += i;
        ops += 1;
    }
    println!("operaciones={ops} resultado={suma}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

C es donde nació la caja de herramientas clásica: **perf** (contadores de hardware de Linux: ciclos, fallos de caché, predicciones de salto erradas) y **valgrind** con su módulo *callgrind*, que instrumenta cada instrucción para darte un mapa exacto de dónde se gasta el tiempo, a costa de correr mucho más lento. Kernighan y Ritchie ya enseñaban en *The C Programming Language* a razonar sobre el coste de cada operación; hoy `perf stat ./main` te muestra esos ciclos reales. Aquí la lección de constantes es directa: el mismo O(*n*) corre órdenes de magnitud más rápido en C que en Python interpretado.

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long ops = 0, suma = 0;
    for (long i = 1; i <= n; i++) {
        suma += i;
        ops++;
    }
    printf("operaciones=%ld resultado=%ld\n", ops, suma);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se perfila con EXPLAIN; aquí, conteo y suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('operaciones=%d resultado=%d', count(*), sum(i)) AS resultado FROM r;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$ops = 0;
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
    $ops++;
}
echo "operaciones=$ops resultado=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Lenguaje | Perfilador idiomático | Notas |
|---|---|---|
| Python | cProfile (instrumentación), py-spy (muestreo) | py-spy corre sobre procesos vivos sin reiniciar |
| JavaScript/TS | perfilador de Node/V8, `--prof`, Chrome DevTools | flamegraphs desde el inspector |
| Java | JFR, async-profiler, JMH para microbenchmarks | ojo con el calentamiento del JIT |
| C# | dotnet-trace, dotnet-counters, PerfView | integrados en el SDK de .NET |
| Go | pprof (`net/http/pprof`, `go test -bench`) | CPU, heap y bloqueo, con flamegraphs nativos |
| Rust | criterion (benchmarks), perf + flamegraph | criterion da intervalos de confianza |
| C | perf, valgrind/callgrind, gprof | contadores de hardware reales |
| SQL | `EXPLAIN` / `EXPLAIN ANALYZE` | perfilas el *plan* de consulta, no un bucle |
| PHP | Xdebug, Blackfire, SPX | Blackfire perfila en producción |

El **flamegraph** —inventado por Brendan Gregg— es el denominador común: casi todos estos perfiladores exportan a ese formato, donde el eje X es el tiempo acumulado y el Y la pila de llamadas. Aprender a leer uno vale para casi cualquier lenguaje.

## 🧬 El concepto en la familia

El perfilado tiene primos en cada nivel del sistema. En bases de datos, `EXPLAIN ANALYZE` es un perfilador del plan de ejecución: te dice si la consulta usa un índice o escanea la tabla entera. En el navegador, la pestaña *Performance* de DevTools perfila render y JavaScript. A escala de sistemas distribuidos, el **tracing** (OpenTelemetry, Jaeger) es perfilado repartido entre servicios: sigue una petición a través de la red y te dice qué salto costó más. En todos los casos el principio es el mismo que enuncia McConnell: instrumenta, mide, encuentra el cuello de botella, actúa solo ahí, y vuelve a medir.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 152
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Optimizar sin medir** → causa: atacas lo que crees que es lento, no lo que lo es → solución: perfila primero y confirma el cuello de botella (McConnell: *measure, don't guess*)
- **Micro-optimizar lo irrelevante** → causa: la ley de Amdahl limita la ganancia de lo que apenas pesa → solución: optimiza el bottleneck que domina el coste
- **Confundir complejidad con velocidad** → causa: dos O(*n*) pueden diferir 10× → solución: la curva la da la complejidad, el coste real lo da el perfilador
- **Benchmark sin calentamiento (JVM) o con una sola muestra** → causa: el JIT o el ruido falsean el número → solución: usa JMH, criterion o mediciones repetidas con estadística

## ❓ Preguntas frecuentes

- **¿Contar operaciones o cronometrar?** El conteo estima la complejidad (cómo escala); el cronómetro y el perfilador miden el tiempo real (cuánto cuesta hoy). Necesitas ambos.
- **¿Perfilar en desarrollo o en producción?** En ambos: en desarrollo para iterar rápido; en producción, con perfiladores de muestreo (py-spy, async-profiler, Blackfire), para ver la carga real.
- **¿Vale la pena optimizar código que no está en el cuello de botella?** Casi nunca: la ley de Amdahl acota la mejora posible. Perfila para saber dónde está el 80 % del tiempo.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 151](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 153 ⏭️](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md)
