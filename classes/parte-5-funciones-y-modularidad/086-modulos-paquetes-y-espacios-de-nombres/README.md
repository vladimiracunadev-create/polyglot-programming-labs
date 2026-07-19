# Clase 086 — Módulos, paquetes y espacios de nombres

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aprender a partir un programa en piezas con nombre propio. Hasta aquí una función nos daba una abstracción: un proceso con nombre. El **módulo** es el escalón siguiente —una abstracción sobre las funciones mismas—: un contenedor con nombre que agrupa un puñado de funciones y tipos relacionados, expone algunas al exterior y guarda el resto para uso interno. Cuando escribes `matematicas.doble(n)`, el prefijo `matematicas.` no es decoración: es la frontera que separa «lo que este grupo ofrece» de «lo que hay dentro del programa». Esa frontera es lo que permite que un proyecto crezca de un archivo a cien sin convertirse en un ovillo imposible de tocar.

La razón profunda la formuló David Parnas en 1972 y McConnell la recoge en *Code Complete* (cap. 6, sobre clases, y cap. 5, sobre diseño): un módulo debe organizarse alrededor de **ocultamiento de información** (information hiding). No agrupamos funciones porque «vayan juntas» de forma vaga, sino porque comparten un secreto —una estructura de datos, un formato, una decisión de diseño— que queremos poder cambiar sin que el resto del programa se entere. El espacio de nombres es la cara visible de ese secreto: da a cada grupo su propio territorio de nombres, de modo que dos módulos puedan tener ambos una función `enviar` sin colisionar, y da al lector una pista inmediata de dónde vive cada cosa.

Hunt y Thomas, en *The Pragmatic Programmer*, llaman a esta virtud **ortogonalidad**: cuando los módulos están bien separados, un cambio en uno no propaga ondas por los demás. Esta clase practica el gesto mínimo —definir una función `doble` en su propio espacio y llamarla desde el principal— en diez lenguajes que entienden «módulo» de maneras sorprendentemente distintas: para Python un módulo es un archivo; para Go, una carpeta; para C, ni siquiera existe la palabra y hay que simularla con convenciones. Reconocer esas diferencias es el objetivo real.

## 🧩 Situación

Imagina un proyecto que empezó como un solo `app.py` de doscientas líneas. Dentro conviven, mezcladas, funciones de cálculo (`doble`, `redondear`, `interes`), de red (`enviar`, `recibir`) y de formato (`a_json`, `a_csv`). Un día alguien añade una función de red llamada `redondear` que redondea latencias, sin saber que ya existía otra `redondear` para dinero; la segunda definición pisa a la primera y los importes empiezan a salir mal en un rincón lejano del programa. Nadie lo nota durante semanas. Esa es la clase de accidente que los espacios de nombres eliminan de raíz: si las matemáticas viven en `matematicas` y la red en `red`, entonces `matematicas.redondear` y `red.redondear` son dos funciones distintas que nunca se confunden, y el prefijo le dice a cualquiera que lea el código de qué territorio proviene cada llamada. Aquí ensayamos la versión más pequeña de esa disciplina: una función `doble` que vive en su propio espacio y se invoca con `modulo.doble(n)`.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** modulo.doble(n) = 2n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `-4` | `resultado=-8` |

## 📖 Definiciones y características

- **Módulo** — la unidad con nombre que agrupa funciones y tipos que comparten un propósito o un secreto. No es solo «un archivo con código junto»: es una decisión de diseño sobre qué queda dentro (privado, cambiable) y qué se ofrece fuera (público, estable). McConnell insiste en *Code Complete* en que el criterio para agrupar no es la conveniencia sino el ocultamiento de información: si dos funciones cambiarían juntas ante un mismo cambio de requisitos, pertenecen al mismo módulo.

- **Paquete** — en la mayoría de los lenguajes, la agrupación de varios módulos bajo un nombre común, normalmente mapeada a una carpeta del sistema de archivos. En Python un paquete es una carpeta con un archivo `__init__.py`; en Java el `package` se corresponde con la jerarquía de directorios; en Go un paquete *es* una carpeta y su identidad viene de la ruta de importación. La palabra cambia de peso según el lenguaje, pero la idea es la misma: una caja de cajas.

- **Espacio de nombres** — el territorio de nombres que un módulo reserva para sí. Es lo que convierte `sqrt` en `math.sqrt` y evita que dos `sqrt` de orígenes distintos choquen. El prefijo tiene además valor documental: quien lee `matematicas.doble` sabe al instante de dónde salió esa función sin buscarla.

- **Importar** — el acto de traer un módulo (o parte de él) al alcance del archivo actual, con `import`, `require` o `use` según el lenguaje. Importar es declarar una dependencia explícita: dejas por escrito de qué otro código depende el tuyo, lo cual es precisamente lo que permite razonar sobre el acoplamiento.

- **Encapsulación de módulo** — la propiedad de exponer solo la interfaz pública y ocultar los detalles internos. Un módulo bien encapsulado se puede reescribir por dentro sin tocar a quien lo usa, siempre que respete lo que prometió hacia fuera. Es la ortogonalidad de Hunt y Thomas aplicada a la frontera del módulo.

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR modulo
LEER n ; ESCRIBIR "resultado=" modulo.doble(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


class matematicas:  # actúa como un espacio de nombres
    @staticmethod
    def doble(n):
        return 2 * n


n = int(sys.stdin.readline())
print(f"resultado={matematicas.doble(n)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

// Objeto usado como módulo/espacio de nombres.
const matematicas = {
  doble: (n) => 2 * n,
};

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

namespace matematicas {
  export function doble(n: number): number {
    return 2 * n;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Clase de utilidades como espacio de nombres.
    static class Matematicas {
        static int doble(int n) {
            return 2 * n;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + Matematicas.doble(n));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

// En C# las sentencias top-level deben preceder a las declaraciones de tipo.
int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Matematicas.Doble(n)}");

static class Matematicas {
    public static int Doble(int n) => 2 * n;
}
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

// En un proyecto real 'doble' viviría en otro paquete; aquí simula el módulo.
func doble(n int) int {
	return 2 * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

mod matematicas {
    pub fn doble(n: i64) -> i64 {
        2 * n
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", matematicas::doble(n));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

/* En C la modularidad se hace por archivos .h/.c; aquí una función local. */
long doble(long n) {
    return 2 * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL organiza en esquemas (schemas); la operación va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (-4))
SELECT printf('resultado=%d', 2 * n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
// PHP usa namespaces; aquí una función que actúa como utilidad del módulo.
function matematicas_doble($n) {
    return 2 * $n;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . matematicas_doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "5"`, `esperado = "resultado=10"`) a través de tres lenguajes que resuelven «poner `doble` en su propio espacio» con tres mecanismos distintos.

**Python.** Aquí no hay una palabra clave de módulo dentro del archivo: la clase `matematicas` se usa como si fuera un espacio de nombres, y `@staticmethod` marca `doble` como una función que no necesita instancia. La línea `n = int(sys.stdin.readline())` lee `"5\n"`, lo convierte en el entero `5`, y `matematicas.doble(n)` accede a la función a través del prefijo de la clase, ejecuta `return 2 * n` con `n=5` y devuelve `10`. El f-string interpola ese `10` y `print` emite `resultado=10`. Lo revelador es que en un proyecto de verdad `matematicas` sería un **archivo** (`matematicas.py`) importado con `import matematicas`; aquí lo simulamos con una clase para que todo quepa en un solo archivo verificable, pero el prefijo `matematicas.` juega exactamente el mismo papel.

**Rust.** Rust sí tiene la palabra clave: `mod matematicas { ... }` declara un módulo real dentro del archivo. Nótese el `pub` delante de `pub fn doble`: sin él la función sería privada al módulo y `main` no podría verla —Rust oculta por defecto y obliga a declarar explícitamente lo público, que es el ocultamiento de información llevado a regla del compilador—. El acceso se hace con `::` en vez de `.`: `matematicas::doble(n)` con `n=5` devuelve `10`, y `println!` produce `resultado=10`. Ese `::` frente al `.` de Python no es un capricho sintáctico: en Rust distingue el acceso a rutas de módulos del acceso a campos de un valor.

**Go.** Go es el contraste instructivo: en Go un paquete es una **carpeta**, no algo que se declare dentro de un archivo, así que aquí no podemos crear un segundo paquete sin partir el ejemplo en varios directorios. El comentario `// aquí simula el módulo` lo reconoce con honestidad: `doble` es una función del mismo paquete `main`. Aun así el recorrido es idéntico: `strconv.Atoi` convierte `"5"` en `5`, `doble(n)` devuelve `10` y `fmt.Printf("resultado=%d\n", ...)` emite `resultado=10`. Los tres lenguajes llegan al mismo `resultado=10`, pero cada uno traza la frontera del módulo en un lugar distinto: dentro del archivo (Rust), simulada con una clase (Python) o en la carpeta misma (Go).

## 🔬 Comparación

| Lenguaje | Cómo declara un módulo/espacio de nombres | Acceso |
|---|---|---|
| Python | Un archivo `.py` es un módulo; una carpeta con `__init__.py` es un paquete | `modulo.funcion` |
| JavaScript | Módulos ES: cada archivo con `import`/`export`; también objetos como espacios | `obj.funcion` |
| TypeScript | Módulos ES más `namespace` heredado de versiones antiguas | `Namespace.funcion` |
| Java | `package` mapeado a carpetas; el nombre completo es la ruta | `Clase.metodo` |
| C# | `namespace` dentro de un *assembly*; independiente de carpetas | `Namespace.Metodo` |
| Go | Un paquete *es* una carpeta; su identidad es la ruta de importación | `paquete.Funcion` |
| Rust | `mod` (en archivo o carpeta) dentro de un *crate*; `pub` expone | `modulo::funcion` |
| C | No tiene módulos: headers `.h` + unidades de traducción `.c` enlazadas | llamada directa |
| SQL | Esquemas (*schemas*) agrupan tablas y vistas | `esquema.tabla` |
| PHP | `namespace` con autoload PSR-4 (nombre ↔ ruta del archivo) | `Espacio\funcion` |

La síntesis vuelve a Parnas y McConnell: bajo la variedad de sintaxis —`import`, `use`, `package`, `#include`, `namespace`— late una sola idea, el ocultamiento de información. Todos estos mecanismos existen para lo mismo: dar a un grupo de código una frontera con un lado interno cambiable y un lado externo estable. Los lenguajes se dividen sobre todo en si esa frontera se ata al sistema de archivos (Go, Java, PHP con PSR-4) o es independiente de él (C#, los `namespace` de TS), y en si el compilador la hace cumplir (Rust exige `pub`) o la deja a la disciplina (C, que ni siquiera tiene la palabra). *Code Complete* lo resume: la calidad de un programa grande se mide en buena parte por la calidad de sus fronteras entre módulos.

## 🧬 El concepto en la familia

En **Ruby** un módulo es una construcción de primera clase: `module Matematicas; def self.doble(n); 2 * n; end; end`, y se accede con `Matematicas.doble(n)`; los módulos de Ruby sirven además como *mixins* para compartir métodos entre clases, un uso que Python o Java no le dan a la palabra «módulo». En **C** no existe el concepto: la modularidad se construye a mano con archivos de cabecera `.h` que declaran la interfaz y archivos `.c` que la implementan, unidos por el enlazador; `static` a nivel de archivo es lo más parecido a «privado del módulo». En **Kotlin**, el `package` se declara al inicio del archivo pero, a diferencia de Java, no obliga a que la carpeta coincida con el nombre. Reconocer la familia —si el módulo es archivo, carpeta, palabra clave o convención— permite leer la estructura de un proyecto ajeno en segundos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 086
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Meter todo en un solo archivo** → causa: agrupar por comodidad y no por propósito, hasta que el archivo mezcla cálculo, red y formato → solución: separar en módulos según qué código cambiaría junto ante un mismo requisito (el criterio de ocultamiento de información de McConnell).
- **Importar de más y contaminar el espacio de nombres** → causa: traer todos los nombres de un módulo (`from modulo import *`) y perder la pista de dónde vino cada función, además de arriesgar colisiones → solución: importar solo lo necesario o conservar el prefijo del módulo.
- **Import circular** → causa: el módulo A importa al B y el B al A, y el intérprete no puede completar ninguno → solución: extraer lo compartido a un tercer módulo, o repensar la dirección de la dependencia para que fluya en un solo sentido.
- **Confiar en que la carpeta y el nombre siempre coinciden** → causa: asumir la regla de un lenguaje (Java, Go, PSR-4) en otro que no la tiene (C#, los `namespace` de TS) → solución: recordar en cada lenguaje si el espacio de nombres se ata al sistema de archivos o es independiente de él.

## ❓ Preguntas frecuentes

- **¿Módulo, paquete o namespace son lo mismo?** Son parientes cercanos, no sinónimos exactos. «Módulo» suele ser la unidad más pequeña (a menudo un archivo); «paquete» agrupa varios módulos (a menudo una carpeta); «espacio de nombres» es el territorio de nombres que uno u otro reserva. Cada lenguaje reparte el peso entre estas palabras a su manera.
- **¿Por qué hace falta el prefijo si mi programa es pequeño?** Porque el prefijo no solo evita colisiones futuras: documenta el origen. `matematicas.doble` le dice al lector de dónde salió esa función sin tener que buscarla, y ese valor se paga solo cuando el programa crece.
- **¿Qué gano separando en módulos si al final todo se compila junto?** Ganas poder cambiar el interior de un módulo sin tocar el resto —la ortogonalidad de Hunt y Thomas—. La separación no es para la máquina, que lo une todo, sino para el humano que mantiene el código.
- **¿Por qué en C no hay `module`?** Porque C es anterior a esa abstracción y la resuelve con convenciones: `.h` para la interfaz, `.c` para la implementación, `static` para lo privado del archivo. Funciona, pero nada en el lenguaje obliga a respetar la frontera.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 5 «Design in Construction» y cap. 6 «Working Classes» (ocultamiento de información y fronteras de módulo).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (Addison-Wesley), tema «Orthogonality» y «Decoupling».
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 sobre la abstracción por nombres.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre paquetes y módulos.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.), cap. «Modules» — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly), cap. «Namespaces and Modules».
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), cap. 10 «Packages and the Go Tool».
- S. Klabnik y C. Nichols — *The Rust Programming Language*, cap. 7 «Managing Growing Projects with Packages, Crates, and Modules» — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly), cap. sobre namespaces y Composer.

---

> [⏮️ Clase 085](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 087 ⏭️](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md)
