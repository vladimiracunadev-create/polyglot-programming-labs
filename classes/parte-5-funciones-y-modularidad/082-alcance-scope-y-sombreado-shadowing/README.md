# Clase 082 — Alcance (scope) y sombreado (shadowing)

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender dónde **vive** un nombre. Cada vez que escribes `x`, el lenguaje tiene que decidir a qué variable te refieres, y esa decisión no es libre: sigue una regla precisa llamada **alcance (scope)**, la región del texto del programa donde ese nombre es visible. El alcance es la pieza que convierte un montón de variables sueltas en un sistema con compartimentos, donde lo que ocurre dentro de una función o un bloque no contamina lo de fuera. Sin él, cada `i` de cada bucle y cada `temp` de cada cálculo competirían por el mismo espacio y el programa sería un campo minado.

La idea profunda la formalizan Abelson y Sussman en *Structure and Interpretation of Computer Programs* (§3.2) con el **modelo de entornos** (environment model): un programa en ejecución no tiene «una tabla de variables», sino una *cadena de entornos* encadenados, donde cada bloque o cada llamada a función crea un marco nuevo que apunta al de fuera. Buscar el valor de `x` significa recorrer esa cadena desde el marco más interno hacia afuera hasta encontrar la primera ligadura con ese nombre. El **sombreado (shadowing)** es el corolario directo: si un marco interno declara su propio `x`, la búsqueda se detiene ahí y nunca llega al `x` externo, que sigue existiendo intacto, solo que oculto mientras dure el marco interior. Al salir del bloque, el marco desaparece y el `x` externo vuelve a ser visible.

Robert Sebesta, en *Concepts of Programming Languages*, contrapone dos formas de resolver esa cadena: el **alcance léxico (o estático)** —la ligadura se decide por dónde está *escrito* el código, y es la que usan los diez lenguajes de esta clase— frente al **alcance dinámico**, hoy casi extinto, donde se decidía por quién *llamó* a quién en tiempo de ejecución. Que hoy demos por sentado el alcance léxico es una conquista: hace que puedas leer un fragmento y saber a qué se refiere cada nombre sin ejecutar nada.

## 🧩 Situación

Estás depurando una función de cientos de líneas. En la parte de arriba hay un `total` que acumula el importe de una factura. A mitad del cuerpo, dentro de un `for` que recorre los descuentos, alguien declaró otro `total` para sumar solo los descuentos de esa iteración. El programa imprime al final un `total` que no cuadra, y pasas una hora buscando el error en la aritmética cuando el problema es de *visibilidad*: dentro del bucle, el nombre `total` estaba sombreado, y el `total` externo nunca recibió lo que creías. Este es el dolor clásico que el alcance provoca cuando no se entiende: la sensación de que «mi variable no cambió» cuando en realidad estabas escribiendo en otra variable que casualmente se llama igual. Entender el sombreado convierte ese misterio en una regla mecánica: el nombre más interno gana, y solo dentro de su bloque.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `interno=<n+10> externo=<n>`
- **Regla:** externo x = n; en un bloque interno x = n+10; al salir, x = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `interno=15 externo=5` |
| `0` | `interno=10 externo=0` |
| `-3` | `interno=7 externo=-3` |

## 📖 Definiciones y características

- **Alcance (scope)** — la región del texto del programa donde un nombre es visible y se resuelve a una ligadura concreta. En casi todos estos lenguajes es de **bloque**: el nombre vive desde su declaración hasta el cierre del `{ }` (o del `def`/función) que lo contiene. Sebesta la llama la propiedad que determina «qué declaración se aplica a cada aparición de un nombre».
- **Entorno (environment)** — la estructura, descrita en *SICP* §3.2, que asocia nombres a valores en un marco, más un enlace al entorno que lo rodea. La cadena de entornos es lo que se recorre al buscar un nombre; el alcance es simplemente el reflejo textual de esa cadena.
- **Sombreado (shadowing)** — cuando un bloque interno declara un nombre igual al de un bloque externo, el interno **oculta** (no destruye) al externo dentro de su región. Es un caso legítimo de dos variables distintas que comparten nombre en marcos distintos; la búsqueda encuentra primero la interna y se detiene.
- **Vida (lifetime)** — cuánto tiempo existe la variable en memoria. No es lo mismo que el alcance: el alcance es *dónde se ve*, la vida es *cuánto dura*. En estos casos coinciden (la interna nace al entrar al bloque y muere al salir), pero en general son ejes independientes.
- **Restauración** — al abandonar el bloque interior, su marco se descarta y el nombre externo vuelve a ser el visible, sin haber sido tocado. Esa restauración es lo que garantiza que `externo` siga valiendo `n`.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; x <- n
BLOQUE: x_interno <- x + 10 ; imprimir interno
imprimir externo (x sigue siendo n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
x = n
# Python no crea alcance de bloque: se usa otra variable para el 'interno'.
x_interno = x + 10
print(f"interno={x_interno} externo={x}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const x = n;
{
  const x = n + 10; // sombrea a la externa dentro del bloque
  console.log(`interno=${x} externo=${n}`);
}
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const x: number = n;
{
  const x: number = n + 10;
  console.log(`interno=${x} externo=${n}`);
}
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int x = n;
        {
            int xInterno = x + 10; // Java no permite re-declarar x en el bloque
            System.out.println("interno=" + xInterno + " externo=" + x);
        }
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int x = n;
{
    int xInterno = x + 10;
    Console.WriteLine($"interno={xInterno} externo={x}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	x := n // externo
	interno := 0
	{
		x := x + 10 // sombrea a la externa en este bloque
		interno = x
	}
	fmt.Printf("interno=%d externo=%d\n", interno, x)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let x = n;
    {
        let x = n + 10; // sombreado idiomático en Rust
        println!("interno={x} externo={n}");
    }
    let _ = x;
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long x = n;
    {
        long x = n + 10; /* sombrea a la externa dentro del bloque */
        printf("interno=%ld externo=%ld\n", x, n);
    }
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL usa alias/subconsultas para acotar nombres.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT printf('interno=%d externo=%d', n + 10, n) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$x = $n;
// PHP no tiene alcance de bloque: se usa otra variable.
$xInterno = $x + 10;
echo "interno=$xInterno externo=$x\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "5"`, `esperado = "interno=15 externo=5"`) por tres lenguajes que tratan el bloque de tres maneras muy distintas.

**Rust — el sombreado como herramienta idiomática.** Tras parsear, `let x = n;` liga `x` a `5` en el marco de `main`. Al entrar en el bloque `{ ... }`, la línea `let x = n + 10;` **no reasigna**: crea una *nueva* variable `x` en un marco interior, ligada a `15`, que sombrea a la anterior. El `println!("interno={x} externo={n}")` de dentro del bloque ve el `x` interior (`15`) e imprime `interno=15`, mientras que `n` sigue valiendo `5`. Al cerrar el bloque, ese `x` interior desaparece y la última línea `let _ = x;` vuelve a referirse al `x` exterior (`5`) —está ahí solo para que el compilador no avise de variable sin usar—. Rust convierte el sombreado en un idiom deliberado: puedes reintroducir un nombre e incluso *cambiarle el tipo* con un nuevo `let`, algo que Java o C prohíben.

**Go — bloque explícito con `:=`.** Aquí `x := n` liga el `x` externo a `5`. Fíjate en el detalle: el resultado interno no se imprime dentro del bloque, sino que se guarda en `interno`, declarada fuera. Dentro del `{ }`, `x := x + 10` declara con `:=` un `x` nuevo del bloque; su lado derecho lee todavía el `x` externo (`5`) y produce `15`, que se asigna a `interno`. Go permite ese sombreado con `:=` y de hecho es una fuente conocida de bugs (el `go vet -vettool=shadow` existe justamente para detectarlo). Al salir, `fmt.Printf("interno=%d externo=%d\n", interno, x)` usa `interno=15` y el `x` externo, que nunca cambió: `5`. Salida: `interno=15 externo=5`.

**Python — sin alcance de bloque.** Python es la excepción reveladora del grupo: un `if` o un `for` **no** crean un alcance nuevo; solo las funciones (y las comprensiones) lo hacen. Por eso la implementación no puede «abrir un bloque y redeclarar `x`»: si lo hiciera, machacaría el `x` de fuera, porque sería la misma variable. La solución idiomática es honesta con esa limitación y usa **otro nombre**, `x_interno = x + 10`, que con `n = 5` vale `15`. El f-string `f"interno={x_interno} externo={x}"` imprime `interno=15 externo=5`. Los tres llegan al mismo resultado, pero solo Rust y Go pudieron reutilizar el nombre `x`; Python tuvo que inventar uno nuevo porque su modelo de alcance no ofrece el compartimento que el sombreado necesita.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El bloque se marca con `{ }` en C, Java, C#, JS/TS, Go y Rust; Python y PHP no tienen bloque léxico y delimitan con indentación o simplemente otra sentencia. |
| Semántica | Rust y Go permiten **redeclarar** un nombre que sombrea al externo (`let`/`:=`); Java prohíbe redeclarar una variable local ya visible y obliga a otro nombre (`xInterno`); C y JS/TS con `let`/`const` sí sombrean por bloque. |
| Semántica | JS distingue `var` (alcance de función) de `let`/`const` (alcance de bloque); usar `let` es lo que hace posible el sombreado del ejemplo. Python ofrece `global`/`nonlocal` para escribir en alcances externos a propósito. |
| Semántica | Rust va más lejos: el sombreado puede **cambiar el tipo** de la variable, no solo el valor, algo imposible en los lenguajes de tipado estático con reasignación. |
| Paradigmática | SQL no tiene variables de bloque: acota nombres con alias de columna y subconsultas/CTE; el `WITH nums(n)` cumple el papel del alcance. |

La síntesis la da el modelo de entornos de *SICP* §3.2: no hay «magia» en que la externa reaparezca. Cada bloque es un marco enganchado al de fuera; la resolución de un nombre recorre la cadena de dentro hacia afuera y se queda con la primera coincidencia. Sombrear es añadir una ligadura más cerca; restaurar es descartar ese marco. Todos los lenguajes implementan esa misma cadena; solo difieren en qué construcciones abren un marco nuevo (Python: solo funciones; el resto: cada `{ }`).

## 🧬 El concepto en la familia

En **Kotlin**, redeclarar con `val`/`var` dentro de un bloque interno sombrea al externo de forma idiomática, igual que en Rust. En **Swift** ocurre lo mismo con `let`. En **Ruby**, en cambio, los bloques comparten el alcance del método que los rodea (una variable ya existente se ve dentro del bloque), pero los parámetros del bloque sí crean nombres locales que pueden sombrear. En **C++** el sombreado por bloque es habitual y los compiladores lo avisan con `-Wshadow`. Reconocer, en un lenguaje nuevo, *qué construcción abre un alcance* —¿el `if`? ¿el `for`? ¿solo la función?— es lo que te permite predecir si un nombre reutilizado sombreará o reasignará.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 082
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que la interna cambió la externa** → causa: confundir sombreado (dos variables, dos marcos) con reasignación (una variable, un valor nuevo) → solución: recuerda que dentro del bloque hay *otra* variable; comprueba el valor justo después de cerrar el bloque y verás intacta a la externa.
- **Sombrear sin querer en Go con `:=`** → causa: dentro de un `if`/`for` escribes `x := ...` creyendo que reasignas, y creas una variable de bloque que descarta el resultado al salir → solución: usa `=` para reasignar la externa, reserva `:=` para declarar, y pasa `go vet` con el chequeo de shadow.
- **Esperar alcance de bloque en Python o PHP** → causa: declarar «dentro de un `if`» pensando que el nombre morirá al salir; en Python el `if`/`for` no crean alcance y la variable «se escapa» → solución: si necesitas una variable temporal aislada, envuélvela en una función, o simplemente usa un nombre distinto.
- **Usar una variable fuera de su alcance** → causa: leer un nombre declarado dentro de un `{ }` una vez cerrado, y obtener «no definida» / error de compilación → solución: declara la variable en el alcance más externo donde la necesites, o devuelve su valor al salir del bloque.

## ❓ Preguntas frecuentes

- **¿Sombrear es mala práctica?** Depende del lenguaje. En Rust y Kotlin es idiomático para transformar un valor conservando el nombre (`let x = parse(x)?`); en C/C++/Java se considera un olor a error y los compiladores lo avisan, porque suele ser accidental. La regla práctica: sombrea a propósito y con nombres cortos y locales; nunca sombrees una variable importante de arriba.
- **¿Python tiene alcance de bloque?** No para `if`/`for`/`while`: sus variables sobreviven al bloque y pertenecen al alcance de la función. Sí lo tienen las funciones y las comprensiones. Por eso el ejemplo usa `x_interno` en vez de reabrir `x`.
- **¿En qué se diferencian alcance léxico y dinámico?** El léxico (o estático) decide la ligadura por *dónde está escrito* el código y se puede leer sin ejecutar; el dinámico la decidía por *quién llamó* en tiempo de ejecución. Sebesta documenta que casi todos los lenguajes modernos abandonaron el dinámico por lo difícil que era razonar con él; los diez de esta clase son léxicos.
- **¿Alcance y vida son lo mismo?** No. El alcance es *dónde se ve* un nombre; la vida es *cuánto existe* en memoria. En estos ejemplos coinciden, pero una variable `static` en C sigue viva entre llamadas aunque su alcance sea local a la función.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §3.2 «The Environment Model of Evaluation».
- R. W. Sebesta — *Concepts of Programming Languages* (11ª ed., Pearson), cap. 5 «Scope» (alcance estático/léxico vs. dinámico).
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 2 sobre nombres y su ámbito de significado.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 10 «General Issues in Using Variables» (minimizar el alcance).

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

> [⏮️ Clase 081](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 083 ⏭️](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md)
