# Clase 144 — Compilación reproducible y empaquetado

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entre el código fuente que un desarrollador escribe y el artefacto que se ejecuta en producción media un proceso —la *build*— que compila, enlaza y empaqueta. La ingeniería seria exige que ese proceso sea **determinista**: la misma entrada debe producir, siempre, el mismo artefacto, byte a byte. Cuando esto se cumple, decimos que la build es *reproducible*, y de repente cosas antes imposibles se vuelven fáciles: comparar dos compilaciones para saber si el binario publicado corresponde de verdad al código auditado, cachear resultados en integración continua, y confiar en la cadena de suministro de software. McConnell dedica en *Code Complete* un capítulo entero a la integración y la construcción precisamente porque el build es el punto donde el trabajo individual se convierte en un producto verificable; una build frágil o no repetible envenena todo lo que viene después.

El laboratorio reduce esa idea a su núcleo comprobable: calcular un **checksum** —aquí, la suma de una lista de enteros— como huella de una entrada. Un checksum real usa un hash criptográfico (SHA-256), pero la mecánica conceptual es la misma que verás en el código: entra una lista, sale un número que la representa y que cambia si la lista cambia. Ese número es lo que un gestor de paquetes compara al descargar un artefacto para confirmar que nadie lo manipuló en tránsito.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Calcular** una suma de comprobación sobre una lista de valores.
2. **Explicar** qué hace determinista a una build y qué fuentes de no-determinismo la rompen.
3. **Relacionar** el checksum con la verificación de integridad de un artefacto.
4. **Nombrar** el formato de empaquetado idiomático de cada lenguaje del núcleo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Determinismo del build | Misma entrada, mismo artefacto: auditable |
| 2 | Checksum / hash | Huella que delata cualquier alteración |
| 3 | Empaquetado por lenguaje | Wheel, jar, crate, binario estático, NuGet… |
| 4 | Fijado de dependencias y flags | Fuentes ocultas de no-determinismo |

## 📖 Definiciones y características

**Compilación reproducible.** Una build es reproducible cuando, partiendo del mismo código, las mismas dependencias fijadas y los mismos flags de compilación, produce un artefacto idéntico byte a byte en cualquier máquina y momento. El enemigo es el no-determinismo: marcas de tiempo incrustadas, rutas absolutas, orden de iteración no estable o números aleatorios. Eliminarlos es lo que permite la auditoría de la que habla McConnell.

**Checksum.** Un valor derivado de los datos mediante una función que produce salidas muy distintas ante cambios mínimos. Sirve como detector de alteraciones: si el checksum recalculado no coincide con el publicado, los datos cambiaron. En el laboratorio la función es una suma; en la vida real es un hash criptográfico resistente a colisiones.

**Artefacto y empaquetado.** El artefacto es la salida de la build lista para distribuir. Cada ecosistema tiene su formato: *wheel* en Python, *jar/war* en Java, *crate* en Rust, un binario estático en Go, un paquete NuGet en C#. Empaquetar bien significa incluir exactamente lo necesario y publicar el checksum junto al artefacto.

## 🧩 Situación

Publicas una nueva versión de una biblioteca y un usuario reporta que el binario que descargó «no funciona igual» que el de otro compañero. Al investigar descubres que tu build incrustaba la fecha de compilación en el artefacto: cada compilación producía bytes distintos y, por tanto, un checksum distinto, aunque el código fuera idéntico. Nadie podía verificar nada. La solución es hacer la build determinista —fijar dependencias, retirar la marca de tiempo— para que el checksum publicado sea estable y cualquiera pueda comprobar que su descarga coincide con lo que tú compilaste. El primer ladrillo de esa verificación es saber calcular el checksum, que es lo que implementa el laboratorio.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `checksum=<suma de los valores>`
- **Regla:** checksum = suma de los valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `checksum=6` |
| `5` | `checksum=5` |
| `10 20 30` | `checksum=60` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; checksum <- suma ; ESCRIBIR checksum
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). El contrato: leer enteros separados por espacio y escribir `checksum=<suma>`. Con `1 2 3` la salida es `checksum=6`; con `10 20 30`, `checksum=60`.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
print(f"checksum={sum(nums)}")
```

La versión de Python es la más compacta y expresa con claridad el patrón «leer todo, tokenizar, reducir». `sys.stdin.read()` consume la entrada completa; `.split()` sin argumentos parte por cualquier bloque de espacios (incluidos saltos de línea), lo que hace al programa robusto ante entradas con formato irregular. La comprensión de lista `[int(x) for x in ...]` convierte cada token a entero de una vez —Ramalho, en *Fluent Python*, defiende estas comprensiones como la forma legible de expresar transformaciones sobre secuencias— y `sum(...)` hace la reducción. La suma es la operación reproducible por excelencia: no depende del orden en que se recorran los sumandos, así que dos ejecuciones con la misma entrada dan el mismo resultado, que es justo la propiedad que se busca en un build.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
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
        long c = 0;
        for (String s : p) c += Integer.parseInt(s);
        System.out.println("checksum=" + c);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

long c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Sum(x => (long) int.Parse(x));
Console.WriteLine($"checksum={c}");
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
	c := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		c += n
	}
	fmt.Printf("checksum=%d\n", c)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("checksum={c}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long c = 0, x;
    while (scanf("%ld", &x) == 1) c += x;
    printf("checksum=%ld\n", c);
    return 0;
}
```

Merece contrastar dos filosofías. C acumula en un bucle `while (scanf(...) == 1)`: no construye ninguna lista intermedia, va sumando token a token hasta que `scanf` deja de leer un entero. Es la aproximación de mínimo consumo de memoria que caracteriza el estilo de Kernighan y Ritchie, y usa `long` para el acumulador anticipando que la suma puede desbordar el rango de un entero pequeño. Go y C# eligen el camino opuesto pero igual de deliberado: Go recorre `strings.Fields(line)` sumando explícitamente, mientras que C# encadena `.Split(...).Sum(x => (long) int.Parse(x))` en estilo LINQ declarativo. Fíjate en que ambos, como el C, promocionan a `long` antes de sumar: es una decisión de ingeniería para evitar el desbordamiento silencioso, un no-determinismo tan real como una marca de tiempo, porque un checksum que desborda deja de representar fielmente su entrada.

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM como checksum simple.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('checksum=%d', sum(x)) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "checksum=" . array_sum($nums) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El algoritmo es una suma; lo que diferencia de verdad a los diez lenguajes es cómo empaquetan y qué producen al compilar. Esta es la tabla que conviene memorizar.

| Lenguaje | Artefacto de distribución | Herramienta de empaquetado |
|---|---|---|
| Python | *wheel* (`.whl`), *sdist* | `build`, `hatch`, `poetry build` |
| JavaScript / TypeScript | tarball npm | `npm pack`, `npm publish` |
| Java | `.jar`, `.war` | Maven, Gradle |
| C# | paquete NuGet (`.nupkg`) | `dotnet pack` |
| Go | binario estático único | `go build` (`CGO_ENABLED=0` para estático) |
| Rust | *crate* / binario en `target/` | `cargo build --release`, `cargo package` |
| C | binario u objeto/librería | compilador + `ar`, Make/CMake |
| SQL | script / migración | según el motor |
| PHP | paquete Composer | `composer` + `archive` |

Dos ideas transversales. Primera: la **reproducibilidad** se consigue igual en todos —dependencias fijadas (lockfile de la clase anterior), flags de compilación explícitos y eliminación de marcas de tiempo—; herramientas como `SOURCE_DATE_EPOCH` existen precisamente para neutralizar la fecha en el artefacto. Segunda: Go destaca por producir un **binario estático** autocontenido que no arrastra dependencias de runtime, lo que simplifica enormemente la reproducibilidad frente a un *wheel* de Python, que asume un intérprete y paquetes instalados en destino.

## 🧬 El concepto en la familia

La verificación por checksum es universal en la distribución de software: los índices de paquetes publican hashes SHA-256 y los gestores los comprueban antes de instalar (`go.sum`, `--require-hashes` en pip, el `integrity` de npm). El movimiento *Reproducible Builds*, nacido en Debian y adoptado por muchos ecosistemas, persigue exactamente lo que ilustra esta clase: que compilar el mismo código dé siempre el mismo artefacto, para que el checksum publicado sea una prueba y no una casualidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 144
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar una suma como checksum de seguridad.** Una suma es trivial de falsificar (basta reordenar o compensar valores). Para integridad frente a un adversario hace falta un hash criptográfico como SHA-256, resistente a colisiones.
- **Incrustar marcas de tiempo o rutas absolutas.** Es la causa número uno de builds no reproducibles: el código no cambia, pero el artefacto sí. Neutralízalas (`SOURCE_DATE_EPOCH`, rutas relativas).
- **No fijar dependencias ni flags.** Compilar con «lo que haya» hace que el artefacto dependa del entorno. Fija versiones (lockfile) y flags de optimización explícitos.
- **Empaquetar de más.** Incluir archivos de test, caché o secretos en el artefacto hincha el paquete y filtra información; declara explícitamente qué se empaqueta.

## ❓ Preguntas frecuentes

- **¿Suma o hash?** La suma solo ilustra la idea; para integridad real usa SHA-256, que cambia radicalmente ante el menor cambio y no se puede falsificar con facilidad.
- **¿Por qué me importa que la build sea reproducible?** Porque permite auditar que el binario distribuido proviene del código publicado y no fue manipulado en la cadena de suministro.
- **¿Un binario de Go y un wheel de Python son comparables?** No del todo: el binario de Go es autocontenido; el wheel necesita intérprete y dependencias en destino. La reproducibilidad se persigue igual, pero la superficie es distinta.

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

> [⏮️ Clase 143](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 145 ⏭️](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md)
