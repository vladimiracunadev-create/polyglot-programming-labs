# Clase 156 — La FFI (Foreign Function Interface): llamar a C desde todos

> Parte **10 — Interoperabilidad y fronteras entre lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La frontera más íntima entre dos lenguajes es la **llamada directa de función**: mi código invoca, dentro del mismo proceso y sin red de por medio, una función compilada por otro lenguaje. El mecanismo que lo hace posible se llama **FFI, Foreign Function Interface**, y el objetivo de esta clase es entender por qué existe, cómo funciona y por qué —casi sin excepción— el punto de encuentro es **C**.

La razón es histórica y práctica a la vez. C fue el lenguaje del sistema operativo Unix, y con él nació una convención binaria estable para llamar funciones: cómo se pasan los argumentos, dónde se deja el valor de retorno, quién limpia la pila. Esa convención, la ABI de C (que estudiarás en detalle en la clase 157), es tan simple y tan universal que se convirtió en el mínimo común denominador. Cuando Python necesita velocidad numérica, no reescribe LAPACK: lo llama por FFI. Cuando la JVM necesita tocar el sistema operativo, usa JNI hacia C. C no es el mejor lenguaje para casi nada moderno, pero es el **idioma franco** en el que todos saben decir "llámame esta función". Entender la FFI es entender por qué C sigue vivo en el centro de ecosistemas que no escriben una sola línea de C.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Explicar** qué es la FFI y qué problema resuelve.
2. **Reconocer** por qué C es el puente universal entre lenguajes.
3. **Llamar** a una función "externa" respetando su firma.
4. **Anticipar** los riesgos de cruzar la frontera: tipos, memoria y errores.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | FFI | Llamar a código de otro lenguaje en el mismo proceso |
| 2 | C como puente | Casi todos exponen una FFI hacia C |
| 3 | Firma y enlace | Declarar tipos exactos y unir con la librería |

## 📖 Definiciones y características

La **FFI** es la interfaz que permite a un lenguaje llamar funciones definidas en otro, típicamente compiladas a código nativo. Su valor es reutilizar librerías probadas —criptografía, compresión, álgebra— en vez de reescribirlas. Pero reutilizar tiene un precio: debes describir, en tu lenguaje, la **firma** exacta de la función externa (cuántos argumentos, de qué tipo, qué devuelve). Si te equivocas, no hay un error de compilación amable: hay corrupción de memoria o una caída, porque la frontera es binaria y nadie la revisa por ti.

Una **función externa** es la que vive en otro lenguaje y se declara para poder invocarla. En Rust se escribe `extern "C" { fn doble(x: i64) -> i64; }`; en Python se describe con `ctypes` o `cffi`; en C# con `[DllImport]`. La declaración no ejecuta nada: solo le dice al enlazador y al runtime cómo hablar con esa función. Y **C como lingua franca** es el hecho central: casi todos los lenguajes exponen una FFI *hacia C*, no hacia cada uno de los demás. Como observa Tanenbaum al hablar de heterogeneidad, un sistema con muchas partes necesita un protocolo común; en la frontera intra-proceso, ese protocolo común es la ABI de C.

- **FFI** — interfaz para llamar a funciones de otro lenguaje en el mismo proceso. Clave: reutilizar librerías nativas sin reescribirlas.
- **Función externa** — definida en otro lenguaje (C) y llamada desde el tuyo. Clave: hay que declarar su firma con precisión.
- **C como lingua franca** — casi todos los lenguajes exponen una FFI hacia C. Clave: puente universal por su ABI simple y estable.

## 🧩 Situación

NumPy no es Python: su corazón es C y Fortran, y Python lo llama por FFI millones de veces por segundo. Ruby carga extensiones nativas en C; la JVM baja a C con JNI para operaciones que el bytecode no cubre; Node.js expone N-API para escribir addons en C++. En todos estos casos ocurre lo mismo: un lenguaje de alto nivel delega el trabajo pesado en una función nativa y recoge el resultado. Para que el concepto se vea sin el ruido de instalar una librería, esta clase simula esa frontera con la función más simple imaginable —**duplicar un número**— escrita como si viviera en C y llamada desde cada lenguaje. La operación es trivial; lo que importa es el gesto: *aquí hay una función que finge venir de C, y todos la saben invocar*.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>`
- **Regla:** llamar a doble(n) 'externo'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=0` |
| `7` | `resultado=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
declarar doble (externa) ; ESCRIBIR doble(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doble(x):  # simula una función externa (FFI hacia C)
    return x * 2


n = int(sys.stdin.readline())
print(f"resultado={doble(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const doble = (x) => x * 2; // función 'externa' vía FFI
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long doble(long x) { return x * 2; } // simula JNI hacia C

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("resultado=" + doble(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Doble(long x) => x * 2; // simula P/Invoke hacia C

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
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

func doble(x int64) int64 { return x * 2 } // simula cgo hacia C

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("resultado=%d\n", doble(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2 // en un caso real, una funcion externa con extern "C"
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doble(long x) { return x * 2; } /* la funcion nativa en C */

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL llama a funciones definidas por el usuario; aqui, la expresion.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doble($x) { return $x * 2; } // simula una extension en C

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código (laboratorio)

Tomemos el caso `5`, que debe producir `resultado=10`. La entrada es un entero; la salida es su doble. Lo interesante es cómo cada lenguaje representa "la función que vive en C".

En **Python**, `doble(x)` se define con un comentario explícito —`# simula una función externa (FFI hacia C)`— porque en un caso real esa función *no* sería Python: sería `lib.doble` obtenida con `ctypes.CDLL("libdoble.so")`. Aquí se escribe en Python para que el ejemplo corra sin compilar una `.so`, pero el papel es el de una llamada externa. Se lee `n` con `int(sys.stdin.readline())`, se invoca `doble(n)` y la `f-string` imprime `resultado=10`. Fíjate en el detalle semántico: Python convierte el texto `"5"` a un entero de precisión arbitraria; el "5 de C" sería un `long` de 64 bits fijos. Esa diferencia de tipos es exactamente lo que la FFI real obliga a declarar.

En **C**, `doble` es la función nativa de verdad: `long doble(long x) { return x * 2; }`. No hay simulación, es el destino que los demás fingen. `scanf("%ld", &n)` lee el entero y `printf("resultado=%ld\n", doble(n))` imprime. Este bloque es la referencia: es la firma que un binding tendría que reproducir sin un solo bit de diferencia (`long`, un argumento, devuelve `long`).

En **Rust**, `doble(x: i64) -> i64` lleva el comentario `// en un caso real, una funcion externa con extern "C"`. En producción se escribiría dentro de un bloque `extern "C" { fn doble(x: i64) -> i64; }` y se llamaría bajo `unsafe`, porque Rust no puede garantizar la seguridad de memoria al otro lado de la frontera. El `i64` de Rust coincide deliberadamente con el `long` de C de 64 bits: *ese* emparejamiento de tipos es lo que hace segura la llamada. Los tres lenguajes producen `resultado=10`, pero solo C ejecuta código nativo; Python y Rust muestran la *forma* de la frontera.

## 🔬 Comparación

| Lenguaje | Mecanismo real de FFI hacia C |
|---|---|
| Python | `ctypes` / `cffi` en la stdlib; casi toda librería científica es un binding a C. |
| JavaScript | N-API (addons nativos) o `ffi-napi` para cargar `.so`/`.dll` en tiempo de ejecución. |
| Java | JNI (clásico) y el nuevo Foreign Function & Memory API (Project Panama, `java.lang.foreign`). |
| C# | P/Invoke con `[DllImport]`; el runtime hace el *marshalling* de tipos. |
| Go | cgo: `import "C"` con un preámbulo de C incrustado en comentarios. |
| Rust | `extern "C"` + `unsafe`; la crate `libc` y `bindgen` generan las firmas. |
| C | Es el destino: no necesita FFI, expone la firma. |
| PHP | Extensión Zend en C, o la clase `FFI` desde PHP 7.4. |

La columna revela el punto de la clase: la sintaxis cambia radicalmente —`ctypes` no se parece en nada a `extern "C"`— pero **todas apuntan a lo mismo, C**, y todas resuelven el mismo problema semántico: emparejar tipos a través de una frontera binaria. La diferencia peligrosa no es sintáctica sino semántica: si declaras `int` (32 bits) donde C espera `long` (64 bits en Linux), la llamada compila y corrompe datos en silencio. Por eso Java está migrando de JNI —verboso y frágil— al API de Panama, más seguro y tipado. SQL queda aparte: sus "funciones externas" son UDF (funciones definidas por el usuario) registradas en el motor, un modelo distinto al de la FFI intra-proceso.

## 🧬 El concepto en la familia

El patrón "todos hacia C" se repite en cada familia: `ctypes` en Python, N-API en Node, JNI y Panama en la JVM, P/Invoke en .NET, cgo en Go, `extern "C"` en Rust y C++. Incluso lenguajes muy alejados —Haskell con su FFI, Lua con su C API— convergen en la misma ABI. C es el esperanto de las bibliotecas nativas: nadie lo elige por gusto, todos lo hablan por necesidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 156
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Firmas incompatibles en la FFI** → causa: declarar `int` donde C espera `long`, o el orden de argumentos cambiado → solución: reproducir la firma bit a bit; ante la duda, generarla con `bindgen`/`cbindgen` en vez de a mano.
- **Ignorar la gestión de memoria a través de la frontera** → causa: no acordar quién libera un puntero devuelto por C → solución: definir la propiedad (ownership); si C reserva, C libera, o se expone una función `free` dedicada.
- **Pasar tipos de alto nivel sin convertir** → causa: enviar un `str` de Python directo a una función que espera `char*` → solución: codificar a bytes (`encode()`) y pasar el puntero; la FFI solo entiende tipos C.
- **Olvidar el coste de cruzar** → causa: llamar a una función trivial por FFI en un bucle caliente → solución: cruzar la frontera pocas veces con lotes grandes, no muchas veces con datos pequeños.

## ❓ Preguntas frecuentes

- **¿Por qué C y no otro lenguaje?** Porque su ABI es simple, estable desde hace décadas y la implementa todo sistema operativo. Otros lenguajes cambian su representación interna entre versiones; C no.
- **¿Toda FFI es hacia C?** Mayormente sí, porque C es el denominador común. Existen puentes directos entre lenguajes cercanos (Kotlin↔Java en la JVM, C++↔Rust con `cxx`), pero cuando dos lenguajes son lejanos, el punto de encuentro casi siempre es la ABI de C.
- **¿La FFI es insegura?** El cruce lo es: Rust exige `unsafe` y Java aísla JNI precisamente porque al otro lado no hay garantías. La seguridad se recupera envolviendo la llamada en una capa que valida tipos y memoria —el tema de la clase 158.

## 🔗 Referencias

**Libros de la parte:**

- M. Kleppmann — *Designing Data-Intensive Applications* (O'Reilly). Cap. 4: codificación y evolución, la raíz del emparejamiento de tipos entre lenguajes.
- S. Newman — *Building Microservices* (2ª ed., O'Reilly). Sobre reutilizar código nativo tras una interfaz estable.
- A. Tanenbaum y M. van Steen — *Distributed Systems* (3ª ed.). Cap. 4: llamadas a procedimiento y el problema de heterogeneidad de datos.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly). Interfaz con C mediante `ctypes`/`cffi`.
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

> [⏮️ Clase 155](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/155-por-que-los-sistemas-reales-son-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 157 ⏭️](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/157-abi-enlace-y-convenciones-de-llamada/README.md)
