# Clase 155 — Por qué los sistemas reales son políglotas

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Esta parte del programa cambia la pregunta. Hasta aquí estudiabas *un* problema resuelto en diez lenguajes que no se hablaban entre sí; a partir de ahora estudias cómo esos lenguajes **conviven dentro de un mismo sistema** y se pasan datos a través de fronteras. La primera clase fija la tesis que sostiene todo lo demás: **los sistemas reales no se escriben en un solo lenguaje, y eso no es un accidente ni una deuda técnica, es una decisión de ingeniería**.

El objetivo concreto es que dejes de ver "el programa" como un bloque monolítico y empieces a verlo como un conjunto de **componentes**, cada uno con una responsabilidad y —muchas veces— su propio lenguaje. Medir cuántos componentes tiene un sistema es el primer gesto de ese cambio de mirada: es contar las piezas antes de razonar sobre cómo se comunican. Kleppmann abre *Designing Data-Intensive Applications* justamente así: una aplicación moderna no es "una base de datos" ni "un servidor", sino una composición de almacenes, cachés, índices, colas y procesos batch, cada uno bueno en una cosa y ninguno bueno en todas. Ese es el terreno de esta parte.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Contar** los componentes de un sistema a partir de su descripción.
2. **Explicar** por qué combinar lenguajes suele ser mejor que forzar la uniformidad.
3. **Reconocer** un sistema políglota real y nombrar sus fronteras.
4. **Justificar** que la heterogeneidad se paga con contratos, no con dogma.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sistema políglota | Varios lenguajes, un sistema coherente |
| 2 | Componente | La unidad con una responsabilidad y su lenguaje |
| 3 | Frontera y contrato | Dónde y cómo se hablan dos componentes |
| 4 | Elegir por tarea | El mejor lenguaje para cada parte, no para todo |

## 📖 Definiciones y características

Un **sistema políglota** es software compuesto por partes escritas en distintos lenguajes. No es una rareza: es lo normal en producción. Newman, en *Building Microservices*, lo defiende como consecuencia directa de dividir un sistema en servicios de despliegue independiente: si cada servicio se despliega por su cuenta, cada equipo puede elegir la tecnología que mejor resuelve *su* parte sin arrastrar a los demás. La uniformidad tecnológica deja de ser un requisito y pasa a ser, como mucho, una preferencia.

Un **componente** es una pieza con una responsabilidad única y, a menudo, su propio lenguaje: el frontend interactivo, el servicio de negocio, el núcleo de cálculo, el almacén de datos. La palabra clave es *responsabilidad*: un componente hace una cosa y la expone hacia afuera. Y una **frontera** es el punto exacto donde dos componentes se tocan y se pasan datos. Toda frontera necesita un **contrato**: un acuerdo explícito de qué se envía y qué se recibe. Tanenbaum insiste en que en un sistema distribuido la comunicación *es* el sistema; los componentes son secundarios frente a las reglas que gobiernan cómo intercambian información. Contar componentes, entonces, es solo el punto de partida: cada componente nuevo introduce al menos una frontera nueva que habrá que diseñar.

- **Sistema políglota** — software compuesto por partes en distintos lenguajes. Clave: es lo normal en producción, no la excepción.
- **Componente** — pieza con una responsabilidad y su propio lenguaje. Clave: se integra con las demás por una frontera.
- **Frontera** — el punto donde dos componentes se comunican. Clave: necesita un contrato explícito para no ser frágil.

## 🧩 Situación

Imagina un producto real de comercio electrónico. El frontend está en TypeScript porque corre en el navegador y necesita interactividad. El backend de pedidos está en Go porque atiende mucho tráfico concurrente con poca ceremonia. El motor de recomendaciones está en Rust porque hace cálculo numérico intenso y no puede permitirse pausas de recolección de basura. Y el catálogo vive en SQL, porque consultar y relacionar datos es exactamente para lo que se diseñó el modelo relacional. Nadie decidió "usemos cuatro lenguajes para complicarnos": cada elección resolvió mejor su parte. El resultado es un sistema de cuatro componentes, con al menos tres fronteras que cruzar. Antes de diseñar esas fronteras —el objeto del resto de la parte— el gesto elemental es contarlas. Esta clase entrena justo eso: leer una lista de componentes y saber cuántas piezas heterogéneas tienes entre manos.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de componentes (palabras)
- **Salida** (stdout): `componentes=<cantidad>`
- **Regla:** contar los componentes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cli api web` | `componentes=3` |
| `app` | `componentes=1` |
| `web api datos cache` | `componentes=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER componentes ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

comps = sys.stdin.read().split()
print(f"componentes={len(comps)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const comps = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${comps.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const comps: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${comps.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] comps = br.readLine().trim().split("\\s+");
        System.out.println("componentes=" + comps.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] comps = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"componentes={comps.Length}");
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
	comps := strings.Fields(line)
	fmt.Printf("componentes=%d\n", len(comps))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    println!("componentes={}", s.split_whitespace().count());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char t[256];
    int c = 0;
    while (scanf("%255s", t) == 1) c++;
    printf("componentes=%d\n", c);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL cuenta las filas (componentes).
WITH comps(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d', count(*)) AS resultado FROM comps;
```

### PHP · `php main.php`

```php
<?php
$comps = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($comps) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

Sigamos el caso `web api datos cache`, que `casos.json` espera que produzca `componentes=4`. La entrada es una sola línea con cuatro palabras separadas por espacios; cada palabra representa un componente del sistema. El trabajo de cada implementación es idéntico: **tokenizar la línea y contar los tokens**.

En **Python**, `sys.stdin.read()` absorbe toda la entrada y `.split()` sin argumentos hace algo más sutil de lo que parece: divide por *cualquier* secuencia de espacios en blanco (espacios, tabuladores, saltos de línea) y descarta los vacíos. Sobre `"web api datos cache\n"` devuelve la lista `["web", "api", "datos", "cache"]`, y `len(...)` da `4`. La `f-string` produce exactamente `componentes=4`. Es la solución más corta porque el modelo mental de Python —"una colección se recorre y se mide, no se indexa a mano"— coincide con el problema.

En **Go**, el mismo trabajo es más explícito. `bufio.NewReader(os.Stdin).ReadString('\n')` lee hasta el salto de línea, y `strings.Fields(line)` es el equivalente exacto de `.split()` de Python: separa por espacios en blanco y elimina los vacíos. `len(comps)` cuenta el *slice* resultante, y `fmt.Printf("componentes=%d\n", ...)` fuerza el formato entero. Go no oculta que estás leyendo un buffer y decidiendo dónde termina la línea; esa verbosidad es deliberada, es la filosofía del lenguaje que verás repetida en toda la parte.

En **SQL** el problema se transforma. SQL no lee de stdin ni tokeniza texto: piensa en tablas. La implementación declara una tabla de tres componentes con `VALUES ('cli'), ('api'), ('web')` y `count(*)` cuenta las filas. Es la misma idea —"medir cuántas piezas hay"— expresada en el paradigma declarativo: no describes *cómo* contar, describes *qué* quieres contado. Por eso el verificador la marca como **ilustrativa**: demuestra el concepto sin participar del contrato por stdin.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `split()`, `strings.Fields`, `preg_split` o un bucle con `scanf`: cada lenguaje escribe la tokenización a su manera. |
| Semántica | Los lenguajes dinámicos (Python, PHP, JS) infieren tipos y colecciones; C cuenta con un contador entero y `scanf` en bucle porque no hay "lista" nativa. |
| Paradigmática | SQL no recorre: agrega. `count(*)` sobre filas es contar sin bucle explícito. |

La diferencia de fondo no está en el conteo, que es trivial, sino en lo que el conteo *representa*: cada palabra es un componente que en la vida real estaría en otro lenguaje. La clase usa un problema mínimo para que el mecanismo (leer, tokenizar, medir) no distraiga de la idea (un sistema es una suma de piezas heterogéneas). C es el caso más revelador: sin colecciones nativas, resuelve con `while (scanf("%255s", t) == 1) c++`, es decir, pide token a token y lleva la cuenta a mano. Esa distancia entre "el lenguaje me da la colección" y "yo construyo la colección" reaparecerá en cada frontera de esta parte.

## 🧬 El concepto en la familia

Casi todo sistema grande es políglota, y la historia lo confirma: Unix se diseñó desde el principio para que programas pequeños en distintos lenguajes cooperaran por tuberías. Hoy la JVM aloja Java, Kotlin y Scala en un mismo proceso; .NET reúne C#, F# y VB; el navegador combina JavaScript con módulos WebAssembly compilados desde Rust o C. La regla transversal es siempre la misma: se elige el lenguaje por componente, y la frontera —FFI, serialización, API o proceso— es lo que hay que diseñar con cuidado.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 155
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Un solo lenguaje para todo por dogma** → causa: elegir la herramienta por costumbre y no por la tarea → solución: evaluar cada componente por separado y aceptar la heterogeneidad cuando aporta.
- **Fronteras sin contrato** → causa: dos componentes que "se entienden" por convención tácita → solución: escribir el contrato (formato, tipos, errores) antes de conectar, como insiste Newman.
- **Confundir "políglota" con "caótico"** → causa: sumar lenguajes sin criterio ni límite → solución: cada lenguaje nuevo debe justificar el coste operativo (build, despliegue, gente que lo mantenga).
- **Ignorar que cada componente añade una frontera** → causa: contar piezas y olvidar sus conexiones → solución: por cada componente nuevo, diseñar también su frontera.

## ❓ Preguntas frecuentes

- **¿Por qué no un solo lenguaje?** Porque ninguno es el mejor en todo. Rust brilla en rendimiento pero es lento de escribir; Python es ágil pero no para un núcleo numérico crítico. Combinarlos aprovecha lo mejor de cada uno donde importa.
- **¿No complica el mantenimiento?** Sí, tiene un coste: más toolchains, más pipelines, más conocimiento en el equipo. La disciplina de contratos claros lo controla, y la ventaja de usar la herramienta correcta suele compensarlo con creces.
- **¿Cuándo *no* conviene ser políglota?** Cuando el equipo es pequeño y ningún componente lo exige de verdad: la uniformidad reduce la carga cognitiva. Como todo en ingeniería, es una compensación, no una regla absoluta.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Prefacio y cap. 1: por qué una aplicación de datos combina varias herramientas especializadas.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Cap. 1–2: servicios de despliegue independiente y heterogeneidad tecnológica.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 1: qué es un sistema distribuido y por qué la comunicación es su esencia.

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

> [⏮️ Clase 154](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 156 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/156-la-ffi-foreign-function-interface-llamar-a-c-desde-todos/README.md)
