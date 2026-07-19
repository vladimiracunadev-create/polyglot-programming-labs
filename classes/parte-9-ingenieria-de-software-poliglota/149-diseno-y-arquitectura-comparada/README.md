# Clase 149 — Diseño y arquitectura comparada

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El **diseño** es el conjunto de decisiones que reparten un sistema en piezas y definen cómo se hablan entre sí; la **arquitectura** es ese diseño a la escala más alta, la que fija la forma general antes de escribir una sola línea de negocio. McConnell dedica en *Code Complete* varios capítulos a lo que llama el desafío central del diseño de software: gestionar la complejidad dividiendo el sistema en partes que quepan, cada una, en una sola cabeza. Dos conceptos gobiernan esa división. La **cohesión** mide cuánto pertenecen juntas las cosas dentro de un módulo —alta cohesión es bueno, una capa que hace *una* cosa—; el **acoplamiento** mide cuánto depende un módulo de otro —bajo acoplamiento es bueno, porque permite cambiar una pieza sin arrastrar a las demás—. Hunt y Thomas, en *The Pragmatic Programmer*, empaquetan la misma meta bajo la palabra **ortogonalidad**: componentes independientes, donde tocar uno no repercute en los otros.

El programa de `casos.json` toma la medida más elemental imaginable de una arquitectura: *contar sus capas*. Recibe los nombres de las capas (`web api datos`) y responde `capas=3`. Es deliberadamente humilde —contar no es diseñar—, pero nombrar y enumerar los componentes es siempre el primer acto de razonar sobre una estructura: no puedes hablar del acoplamiento entre capas que aún no has identificado. La arquitectura en capas clásica (presentación → lógica → datos) es el ejemplo canónico, y contar sus estratos es el punto de partida.

Lo verdaderamente interesante para un curso políglota aparece en la comparación: cada lenguaje *empuja* hacia una forma distinta de organizar el código. Java te da paquetes y una jerarquía de directorios; Go y Rust, módulos con reglas de visibilidad propias; C# organiza con namespaces y ensamblados. La arquitectura no es neutral respecto al lenguaje: la gramática del lenguaje moldea la estructura que resulta natural.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Contar e identificar** las capas o componentes de una arquitectura descrita por sus nombres.
2. **Distinguir** cohesión de acoplamiento y explicar por qué se busca alta cohesión y bajo acoplamiento.
3. **Relacionar** la separación de responsabilidades con la capacidad de cambiar el sistema sin efectos colaterales.
4. **Comparar** cómo distintos lenguajes (paquetes Java, módulos Go/Rust, namespaces C#) empujan hacia distintas estructuras.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arquitectura y capas | Estructura de alto nivel del sistema |
| 2 | Cohesión y acoplamiento | Decide qué tan fácil es cambiar |
| 3 | Separación de responsabilidades | Cada parte hace una sola cosa |
| 4 | Módulos por lenguaje | La gramática moldea la estructura |

## 📖 Definiciones y características

- **Arquitectura** — la estructura de alto nivel de un sistema: qué componentes existen, qué responsabilidad tiene cada uno y cómo se relacionan. Es donde se toman las decisiones caras de revertir, así que McConnell insiste en pensarlas antes, cuando cambiarlas todavía es barato.
- **Capa** — un grupo de componentes con una responsabilidad común (presentación, lógica de negocio, acceso a datos). Las capas imponen una dirección a las dependencias: la de presentación conoce a la de negocio, no al revés, y esa asimetría es lo que mantiene el sistema comprensible.
- **Cohesión** — el grado en que los elementos de un módulo pertenecen realmente juntos. Alta cohesión significa que una capa tiene un motivo único para existir; baja cohesión es el módulo "cajón de sastre" que hace de todo y no se entiende.
- **Acoplamiento** — el grado de dependencia entre componentes. Bajo acoplamiento —el ideal— permite reemplazar o modificar una pieza sin que el cambio se propague; alto acoplamiento convierte cualquier retoque en una reacción en cadena. Hunt y Thomas lo llaman ortogonalidad y lo consideran, junto a la ausencia de duplicación, la base de un diseño mantenible.

## 🧩 Situación

Heredas un servicio que "nadie se atreve a tocar". Al leerlo descubres que la lógica de negocio hace consultas SQL directas y también arma HTML: las tres responsabilidades —presentación, negocio y datos— viven mezcladas en las mismas funciones. Cambiar el formato de una fecha en pantalla te obliga a entender la consulta a la base de datos, porque están enredadas: alto acoplamiento, baja cohesión. La cura es arquitectónica: separar en capas `web`, `api` y `datos`, cada una con su responsabilidad, con dependencias que apunten en una sola dirección. El primer paso, antes de mover una línea, es exactamente lo que hace el programa de esta clase: nombrar las capas y contarlas, para tener un mapa sobre el que razonar. `capas=3` es el diagnóstico inicial de una arquitectura que por fin se puede discutir.

## 🧮 Modelo

- **Entrada** (stdin): una línea con nombres de capas (palabras separadas por espacio)
- **Salida** (stdout): `capas=<cantidad>`
- **Regla:** contar los nombres de capa

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `web api datos` | `capas=3` |
| `cli` | `capas=1` |
| `web api datos cache` | `capas=4` |

## 📐 Algoritmo (pseudocódigo neutral)

Contar los componentes es la medida más básica de una estructura: sin enumerarlos no hay nada sobre lo que razonar.

```text
LEER capas ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

Python resuelve el conteo con una elegancia casi telegráfica. `sys.stdin.read().split()` sin argumentos parte por *cualquier* bloque de espacios en blanco y descarta los vacíos, así que `"web api datos"` se convierte en una lista de tres cadenas; `len(...)` la mide. El detalle idiomático que Ramalho subraya en *Fluent Python* es que `str.split()` sin separador ya normaliza espacios múltiples y saltos de línea, por lo que no hace falta limpieza previa: la abstracción correcta hace desaparecer el caso borde.

```python
import sys

capas = sys.stdin.read().split()
print(f"capas={len(capas)}")
```

Para `web api datos` la lista tiene tres elementos y sale `capas=3`; para `cli`, uno, `capas=1`; para `web api datos cache`, cuatro. Fíjate en que el "modelo" del sistema —sus capas— es aquí, literalmente, una lista, y contar componentes es medir esa lista.

### Go · `go run main.go`

Go contrasta en la forma de leer, pero coincide en el espíritu con `strings.Fields`, que es el equivalente exacto del `split()` sin argumentos de Python: trocea por espacios en blanco y omite los vacíos. Donovan y Kernighan, en *The Go Programming Language*, presentan `Fields` como la herramienta idiomática para tokenizar texto separado por espacios sin sorpresas. La verbosidad de importar `bufio`, `os` y `strings` es el precio que Go paga por su explicitud: nada de magia, cada dependencia a la vista.

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
	capas := strings.Fields(line)
	fmt.Printf("capas=%d\n", len(capas))
}
```

Que Go se apoye en `strings.Fields` no es casual: es un lenguaje que organiza el propio código en *paquetes* con visibilidad por mayúscula/minúscula, y su biblioteca estándar refleja esa mentalidad modular y sin adornos.

### SQL · `sqlite3 :memory: < main.sql`

SQL vuelve a mostrar el otro paradigma. No hay lista ni tokens: hay una tabla donde *cada capa es una fila*, y contar componentes es la agregación `count(*)`. Es una traducción fiel de la idea arquitectónica —cada componente, una entidad— al modelo relacional que Date defiende en *SQL and Relational Theory*: razonas sobre conjuntos de filas, no sobre una cadena que hay que partir.

```sql
-- SQL: cuenta las filas (capas).
WITH capas(nombre) AS (VALUES ('web'), ('api'), ('datos'))
SELECT printf('capas=%d', count(*)) AS resultado FROM capas;
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const capas = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const capas: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] capas = br.readLine().trim().split("\\s+");
        System.out.println("capas=" + capas.length);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] capas = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"capas={capas.Length}");
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("capas={n}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("capas=%d\n", c);
    return 0;
}
```

### PHP · `php main.php`

```php
<?php
$capas = preg_split('/\s+/', trim(fgets(STDIN)));
echo "capas=" . count($capas) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

Aquí la diferencia entre lenguajes va más allá de la sintaxis del conteo: cada uno ofrece un mecanismo distinto para *organizar* el código en unidades, y ese mecanismo condiciona la arquitectura que emerge de forma natural.

| Lenguaje | Unidad de organización | Control de visibilidad |
|---|---|---|
| Java | paquetes (`package a.b.c`) + directorios | `public`/`protected`/`private`/paquete |
| C# | namespaces + ensamblados | `public`/`internal`/`private` |
| Go | paquetes (por directorio) | mayúscula = exportado |
| Rust | módulos (`mod`) + crates | `pub` explícito, privado por defecto |
| Python | módulos y paquetes (`__init__.py`) | convención `_privado` |
| JavaScript/TS | módulos ES (`import`/`export`) | `export` explícito |
| C | archivos + cabeceras `.h` | `static` = interno a la unidad |
| SQL | esquemas | permisos por objeto |

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `split`/`Fields`/`count` frente a bucle con `scanf`. |
| Semántica | Cada capa aísla una responsabilidad; contar es el primer diagnóstico. |
| Paradigmática | SQL cuenta filas (una capa = una fila) en vez de tokenizar. |

## 🧬 El concepto en la familia

La estructura en componentes con responsabilidades reaparece en cada estilo arquitectónico: la arquitectura en **capas** las apila y dirige las dependencias hacia abajo; la **hexagonal** (puertos y adaptadores) pone el dominio en el centro y el mundo exterior en los bordes; los **microservicios** separan las capas en procesos independientes desplegables por separado. Cambian las fronteras y su coste, pero la pregunta de fondo es siempre la misma que la de esta clase: ¿cuántas piezas hay, qué responsabilidad tiene cada una y cómo dependen entre sí?

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 149
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capas con responsabilidades mezcladas** → causa: baja cohesión, difícil de mantener → solución: una responsabilidad por capa.
- **Alto acoplamiento** → causa: un cambio se propaga a todo el sistema → solución: definir contratos claros entre capas y dirigir las dependencias.
- **Sobre-arquitectura** → causa: inventar capas que el problema no pide, complejidad gratuita → solución: tantas capas como el problema justifique, ni una más.

## ❓ Preguntas frecuentes

- **¿Cuántas capas debe tener un sistema?** Las que el problema justifique; ni de más (complejidad gratuita) ni de menos (responsabilidades mezcladas). Contar es el diagnóstico, no la meta.
- **¿Capas o microservicios?** Las capas conviven dentro de un mismo proceso; los microservicios separan responsabilidades en servicios desplegables por separado, ganando independencia a cambio de complejidad de red.
- **¿El lenguaje decide la arquitectura?** No la decide, pero la empuja: los módulos de Rust o los paquetes de Java hacen que ciertas estructuras sean naturales y otras, incómodas.

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

> [⏮️ Clase 148](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 150 ⏭️](../../parte-9-ingenieria-de-software-poliglota/150-refactorizacion-segura/README.md)
