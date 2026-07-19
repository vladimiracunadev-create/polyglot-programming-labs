# Clase 088 — Importar, exportar y organizar un proyecto

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la contracara de escribir funciones: saber **traer** las que ya existen. Organizar un proyecto no es solo repartir el código propio en módulos; es también decidir, ante cada necesidad, si se reescribe o se importa. La respuesta casi siempre es importar. Todos los lenguajes traen una **biblioteca estándar** —un conjunto de módulos ya escritos, probados y optimizados— y cada `import`, `use`, `#include` o `using` es una declaración explícita de que tu código se apoya en ese trabajo previo. Esta clase toma el ejemplo más humilde posible, el valor absoluto, para practicar el gesto de importar y para ver que detrás de `abs(n)` hay una decisión de organización, no solo de sintaxis.

La idea de fondo la defienden Hunt y Thomas en *The Pragmatic Programmer* bajo el principio **DRY** (Don't Repeat Yourself): cada pieza de conocimiento debe tener una única representación autorizada en el sistema. Reescribir un `abs` propio con un `if x < 0` no solo añade líneas: crea una segunda versión de una lógica que ya vivía, correcta, en la biblioteca; y dos versiones de la misma idea son dos sitios donde corregir el mismo bug. Importar la función estándar es aplicar DRY hacia fuera —no repetir lo que el lenguaje ya resolvió por ti—.

Hay además una dimensión de estructura. Los `import` de un archivo son su lista de dependencias visibles: dicen, de un vistazo, de qué se apoya este código. McConnell insiste en *Code Complete* en que la organización de un programa —qué depende de qué y en qué dirección— es tan importante como la corrección de cada rutina. Por eso cada lenguaje acompaña sus `import` con una herramienta de proyecto (`package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `pyproject.toml`, `composer.json`) que declara las dependencias externas de forma que cualquiera pueda reconstruir el proyecto. Importar bien es el primer eslabón de esa cadena.

## 🧩 Situación

Un programador novato necesita el valor absoluto y escribe, en cada uno de los cinco archivos donde le hace falta, un pequeño `if x < 0: x = -x`. Funciona. Meses después descubre que en uno de los cinco copió mal el signo, y lleva semanas devolviendo resultados negativos en un informe. El problema no era saber calcular un valor absoluto —es trivial—: era haber creado cinco copias de una lógica que el lenguaje ya ofrecía correcta y en un solo lugar. Bastaba `import`, o ni siquiera eso en los lenguajes donde `abs` es global. Esta es la lección práctica de organizar un proyecto: antes de escribir una función de utilidad, conviene preguntarse si ya existe en la biblioteca estándar. Casi siempre existe, casi siempre está mejor probada que la que uno escribiría, y usarla concentra el conocimiento en un único sitio en lugar de esparcirlo en copias. Aquí ensayamos ese reflejo con `abs(n)`.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `abs=<|n|>`
- **Regla:** abs(n) = |n|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `abs=5` |
| `3` | `abs=3` |
| `0` | `abs=0` |

## 📖 Definiciones y características

- **Biblioteca estándar** — el conjunto de módulos que vienen incluidos con el lenguaje, sin instalar nada. Es el primer sitio donde buscar antes de escribir una utilidad: contiene funciones probadas por millones de ejecuciones. Cada lenguaje reparte su contenido a su manera —Python lleva `abs` como función global y `math` como módulo aparte; C separa lo entero (`stdlib.h`) de lo flotante (`math.h`)—.

- **Importar / incluir** — el acto de traer un módulo o cabecera al alcance del archivo: `import` en Python y Java, `require`/`import` en JavaScript, `use` en Rust, `using` en C#, `#include` en C. No todos hacen lo mismo por dentro —`#include` de C pega texto, `import` de Python ejecuta y vincula un módulo—, pero todos responden a la misma intención: usar código que vive fuera de este archivo.

- **Exportar** — la cara opuesta del importar: marcar qué partes de un módulo son visibles para quien lo importe. En los módulos ES de JavaScript y TypeScript se hace con `export` (con la distinción entre exportaciones *named* y *default*); en Rust con `pub`; en Go con la mayúscula inicial. Sin algo exportado, no hay nada que importar.

- **Reutilización** — apoyarse en código existente en vez de reescribirlo. Su valor no es la pereza sino la fiabilidad: menos código propio significa menos superficie donde alojar errores, y una función estándar arrastra años de correcciones que la tuya no tendría. Es DRY en acción.

- **Herramienta de proyecto** — el archivo que declara las dependencias externas y cómo se construye el proyecto (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `composer.json`). Convierte «este código necesita tal biblioteca» en algo reproducible por cualquiera que clone el repositorio.

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR abs de la biblioteca
LEER n ; ESCRIBIR "abs=" abs(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
print(f"abs={abs(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`abs=${Math.abs(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("abs=" + Math.abs(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"abs={Math.Abs(n)}");
```

### Go · `go run main.go`

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
	if n < 0 {
		n = -n
	}
	fmt.Printf("abs=%d\n", n)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("abs={}", n.abs());
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("abs=%ld\n", labs(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: abs() incorporado.
WITH nums(n) AS (VALUES (-5), (3), (0))
SELECT printf('abs=%d', abs(n)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
echo "abs=" . abs($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "-5"`, `esperado = "abs=5"`) por tres lenguajes que exponen el valor absoluto en tres lugares distintos de su biblioteca estándar.

**Python.** Aquí no hace falta importar nada para el cálculo: `abs` es una función *builtin*, siempre disponible en el espacio global del lenguaje. El único `import sys` es para leer la entrada, no para el valor absoluto. `n = int(sys.stdin.readline())` toma `"-5\n"` y produce `n=-5`; el f-string `f"abs={abs(n)}"` invoca la función global con el argumento `-5`, que devuelve `5`, y `print` emite `abs=5`. Que `abs` sea global y no viva en `math` es una decisión de diseño de Python: las operaciones más universales se ponen al alcance sin ceremonia; las especializadas (`sqrt`, `floor`) sí requieren `import math`.

**C.** C es el contraste didáctico: aquí sí hay que declarar de dónde viene la función, y además elegir la variante correcta. La línea `#include <stdlib.h>` trae `labs`, que es el valor absoluto para `long`; existe también `abs` para `int` (en el mismo header) y `fabs` para `double` (en `math.h`). Con `n=-5`, `labs(n)` devuelve `5`, y `printf("abs=%ld\n", ...)` lo imprime como `abs=5`. Nótese la disciplina que C exige: hay que importar el header adecuado *y* usar el nombre que corresponde al tipo, porque C no sobrecarga `abs` sobre distintos tipos numéricos como hacen los lenguajes más nuevos.

**Rust.** Rust ofrece el valor absoluto como un **método** del propio tipo entero: `n.abs()`, no `abs(n)`. Con `n` de tipo `i64` e igual a `-5`, la expresión `n.abs()` devuelve `5`, y `println!("abs={}", ...)` produce `abs=5`. El `use std::io::Read` del principio importa el *trait* necesario para leer stdin, no el valor absoluto —`abs` viene incluido en el tipo entero sin importar nada—. Los tres llegan al mismo `abs=5`, pero por caminos que revelan la filosofía de cada biblioteca: función global sin importar (Python), función libre que exige el header y el nombre exactos (C), o método del propio valor (Rust).

## 🔬 Comparación

| Lenguaje | Cómo se obtiene el valor absoluto | Import necesario |
|---|---|---|
| Python | `abs(n)`, función *builtin* global | Ninguno (está siempre) |
| JavaScript | `Math.abs(n)`, del objeto global `Math` | Ninguno (`Math` es global) |
| TypeScript | `Math.abs(n)`, igual que JavaScript | Ninguno para `Math` |
| Java | `Math.abs(n)`, método estático de `java.lang.Math` | `java.lang` es implícito |
| C# | `Math.Abs(n)`, del espacio `System` | `using System;` |
| Go | `math.Abs` es para `float64`; con enteros se usa un condicional | `import "math"` (aquí, no) |
| Rust | `n.abs()`, método del tipo entero | Ninguno para `abs` |
| C | `abs`/`labs` (entero) o `fabs` (flotante), según el tipo | `#include <stdlib.h>` / `<math.h>` |
| SQL | `abs(n)`, función escalar incorporada | Ninguno |
| PHP | `abs($n)`, función global | Ninguno |

La síntesis es doble. Primero, DRY: en los diez lenguajes el valor absoluto ya está resuelto, y escribir el propio sería reintroducir una copia de conocimiento que ya tiene su representación autorizada —justo lo que Hunt y Thomas advierten evitar—. Segundo, la organización interna de cada biblioteca revela una filosofía: unos lo ofrecen como función global sin fricción (Python, PHP, SQL), otros como miembro de un objeto o clase de matemáticas (JavaScript, Java, C#), otros como método del propio valor (Rust), y C obliga a elegir la variante exacta según el tipo. El caso de Go es el más instructivo: su `math.Abs` opera sobre `float64`, de modo que para enteros lo idiomático es un condicional propio —un recordatorio de que «está en la estándar» no siempre significa «para tu tipo exacto»—. Saber leer estas diferencias es parte de organizar un proyecto: elegir la herramienta correcta empieza por conocer dónde la guarda cada lenguaje.

## 🧬 El concepto en la familia

En **Ruby**, como en Rust, el valor absoluto es un método del número: `n.abs`, sin importar nada, porque los enteros son objetos con métodos. En **Go**, ya lo vimos, `math.Abs` está pensado para `float64` y convertir un entero a flotante y de vuelta arriesga imprecisión en valores grandes, por lo que la comunidad prefiere un `if n < 0 { n = -n }` o una pequeña función propia para enteros. En **Haskell**, `abs` es un método de la clase de tipos `Num`, disponible para cualquier tipo numérico sin import explícito y sin sintaxis de método. Reconocer si un lenguaje ofrece la operación como función libre, método del valor o método de una clase de tipos aclara de inmediato cómo se escribirá la llamada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 088
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Reimplementar lo que ya existe** → causa: escribir un `abs` propio con `if x < 0` por no saber que la biblioteca ya lo trae, creando una segunda versión de una lógica que ya estaba correcta → solución: buscar primero en la biblioteca estándar; casi todo lo elemental ya está y mejor probado.
- **Olvidar el import o el include** → causa: usar una función sin traer su módulo, y toparse con «función no encontrada» o un símbolo sin definir en el enlazado → solución: importar el módulo correcto (`math`, `stdlib.h`, `System`) según lo que el compilador o el intérprete reclame.
- **Usar la variante equivocada para el tipo** → causa: en C, llamar a `abs` (para `int`) sobre un `long`, o suponer que `math.Abs` de Go sirve para enteros → solución: comprobar qué tipo espera cada función; en C usar `labs`/`fabs` según corresponda, en Go usar un condicional para enteros.
- **Importar el módulo entero cuando basta una función** → causa: traer un espacio de nombres completo y ensuciar el alcance del archivo → solución: importar solo el nombre que se usa, o mantener el prefijo del módulo para que el origen quede a la vista.

## ❓ Preguntas frecuentes

- **¿Siempre conviene usar la biblioteca estándar?** Para lo común y bien definido, sí: está probada, optimizada y concentra el conocimiento en un solo sitio. La excepción es cuando necesitas un comportamiento distinto del que ofrece; entonces escribes el tuyo, pero como decisión consciente, no por desconocer que existía el estándar.
- **¿Por qué en Python no importo `abs` y en C sí incluyo un header?** Porque cada lenguaje decide qué pone al alcance sin ceremonia. Python coloca las operaciones más universales en el espacio global (*builtins*); C mantiene el núcleo mínimo y exige declarar de dónde viene cada función con su `#include`.
- **¿Go no tiene `abs` para enteros?** Su `math.Abs` opera con `float64`. Para enteros lo idiomático es un condicional (`if n < 0 { n = -n }`) o una función propia, porque convertir a flotante y volver puede perder precisión en valores grandes.
- **¿Qué diferencia hay entre exportación *named* y *default*?** En los módulos ES, una exportación *named* se importa por su nombre exacto entre llaves (`import { abs } from ...`) y puede haber muchas por módulo; la *default* es una sola por módulo y se importa con el nombre que quiera quien la recibe. La distinción organiza cómo se nombran las cosas al cruzar la frontera del módulo.

## 🔗 Referencias

**Libros de la parte:**

- A. Hunt y D. Thomas — *The Pragmatic Programmer* (Addison-Wesley), tema «DRY — The Evils of Duplication».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. sobre la estructura y organización de programas.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), sobre construir apoyándose en abstracciones existentes.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre la biblioteca estándar y los *builtins*.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. «Modules» — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), cap. sobre `import`/`export`.
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), ítem sobre preferir las bibliotecas estándar.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), cap. 10 «Packages and the Go Tool».
- S. Klabnik y C. Nichols — *The Rust Programming Language*, cap. 7 sobre `use` y rutas — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), apéndice sobre la biblioteca estándar.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly), cap. sobre Composer y autoload.

---

> [⏮️ Clase 087](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 089 ⏭️](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md)
