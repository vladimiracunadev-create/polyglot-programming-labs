# Clase 080 — Paso por referencia

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el modo de paso que sí permite a una función alcanzar y modificar la variable de quien la llamó: el **paso por referencia**. Si en el paso por valor la función recibía una fotocopia, aquí recibe la dirección del documento original: escribe sobre él, y el cambio persiste cuando la función retorna. Es el mecanismo con el que una subrutina puede tener un canal de salida distinto del `return` —o incluso varios a la vez— y es la base de operaciones clásicas como intercambiar dos variables (`swap`) o rellenar un buffer que el llamador proporciona.

Robert Sebesta, en *Concepts of Programming Languages*, define el paso por referencia como el modo en que la subrutina recibe un **camino de acceso** (normalmente una dirección) a la variable del llamador, en lugar de una copia de su valor. La información fluye en las dos direcciones: lo que la función escribe a través de ese camino queda escrito en el original. Pero Sebesta también advierte del reverso oscuro: los efectos secundarios y los *alias* (dos nombres para la misma celda) hacen el código más difícil de razonar, porque ya no basta mirar el `return` para saber qué cambió una llamada.

El objetivo hondo —y la fuente de la mitad de la confusión en esta materia— es distinguir el **paso por referencia genuino** del **paso de una referencia por valor**. Son cosas distintas que se parecen. C++ (`&`), C# (`ref`) y Rust (`&mut`) ofrecen referencia genuina: la función opera directamente sobre la variable del llamador. Java y Go, en cambio, **no tienen paso por referencia**: siempre pasan por valor, y lo que a veces parece «por referencia» es que copiaron un puntero o una referencia a objeto. Go lo hace explícito con punteros `*T`; Java lo disimula bajo objetos mutables. Saber en qué grupo está cada lenguaje es el corazón de la clase.

## 🧩 Situación

Escribes `doblar(&n)` y, tras la llamada, `n` vale el doble para siempre. Es potente: evita copiar estructuras grandes y permite que una función devuelva resultados por más de un canal. Pero es peligroso justo por lo mismo: la función modificó tu variable «a distancia», y si no esperabas ese efecto, tu programa hace algo que no leías en la línea de la llamada. Ese es el dilema que atraviesa toda la clase. El paso por referencia es la herramienta correcta cuando el *propósito* de la función es mutar (un `swap`, un acumulador, un buffer), y una trampa cuando lo usas por comodidad y olvidas que la variable del llamador quedó a merced del cuerpo de la función.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `antes=<n> despues=<2n>`
- **Regla:** la función duplica la variable original vía referencia

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `antes=5 despues=10` |
| `3` | `antes=3 despues=6` |
| `7` | `antes=7 despues=14` |

## 📖 Definiciones y características

- **Paso por referencia** — la función recibe un camino de acceso a la variable original, no una copia de su valor. Modificar el parámetro modifica la variable del llamador. En términos de Sebesta, el parámetro y el argumento se convierten en *alias*: dos nombres para la misma celda de memoria.
- **Puntero** — en C y Go, un valor que guarda la **dirección** de otra variable. Pasar `&n` entrega esa dirección; dentro, `*p` *desreferencia* el puntero para leer o escribir la celda apuntada. El puntero en sí se pasa por valor (es una dirección copiada), pero como apunta al original, escribir en `*p` alcanza al llamador.
- **Referencia mutable** — el enlace explícito que autoriza a cambiar el valor: `&mut` en Rust, `ref` en C#, `&` en C++. Es la forma más honesta de paso por referencia: la firma declara en voz alta «voy a poder modificar esto».
- **Efecto secundario** — cualquier cambio que una función produce fuera de sí misma, aquí la mutación de la variable del llamador. Es lo que da poder al paso por referencia y, a la vez, lo que hay que vigilar: un efecto secundario no anunciado es una fuente clásica de bugs.
- **Paso por referencia vs. referencia por valor** — la distinción capital. Java y Go **no** tienen paso por referencia real: siempre copian el argumento. Cuando parece que mutan el original, lo que ocurre es que copiaron una *referencia a un objeto* (Java) o que tú pasaste explícitamente un *puntero* (Go `*T`). La prueba: en Java no puedes escribir un `swap(a, b)` que intercambie dos `int` locales del llamador, porque no hay forma de pasar por referencia un primitivo. Por eso las implementaciones de Java, JS y Python de esta clase usan una **caja** (un arreglo o un objeto de un elemento): meten el entero dentro de un objeto mutable y comparten la referencia a ese objeto.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; antes <- n
doblar(referencia a n)   // modifica el original
ESCRIBIR "antes=" antes " despues=" n
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def doblar(caja):
    caja[0] *= 2  # modifica el contenido compartido


n = int(sys.stdin.readline())
antes = n
caja = [n]
doblar(caja)
print(f"antes={antes} despues={caja[0]}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function doblar(caja) {
  caja.v *= 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function doblar(caja: { v: number }): void {
  caja.v *= 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes: number = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java pasa la referencia del arreglo: se puede mutar su contenido.
    static void doblar(int[] caja) {
        caja[0] *= 2;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int antes = n;
        int[] caja = { n };
        doblar(caja);
        System.out.println("antes=" + antes + " despues=" + caja[0]);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

void Doblar(ref int x) {
    x *= 2;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int antes = n;
int v = n;
Doblar(ref v);
Console.WriteLine($"antes={antes} despues={v}");
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

func doblar(p *int) {
	*p *= 2
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	antes := n
	doblar(&n)
	fmt.Printf("antes=%d despues=%d\n", antes, n)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(x: &mut i64) {
    *x *= 2;
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut n: i64 = s.trim().parse().unwrap();
    let antes = n;
    doblar(&mut n);
    println!("antes={antes} despues={n}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

void doblar(long *p) {
    *p *= 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long antes = n;
    doblar(&n);
    printf("antes=%ld despues=%ld\n", antes, n);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no modifica variables; el 'despues' se calcula en la expresión.
WITH nums(n) AS (VALUES (5), (3), (7))
SELECT printf('antes=%d despues=%d', n, n * 2) AS resultado FROM nums;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function doblar(&$x) {
    $x *= 2;
}

$n = (int) trim(fgets(STDIN));
$antes = $n;
doblar($n);
echo "antes=$antes despues=$n\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "5"`, `esperado = "antes=5 despues=10"`) por tres lenguajes que representan los tres grandes enfoques: puntero (C), referencia mutable (Rust) y caja-objeto (Java).

**C — el puntero explícito.** `scanf("%ld", &n)` deja `n = 5`. Antes de tocarla, `antes = n` guarda una copia del `5` para poder mostrar el valor previo. La llamada `doblar(&n)` pasa la **dirección** de `n`, no su valor: el parámetro `long *p` recibe esa dirección. Dentro, `*p *= 2` significa «ve a la celda que apunta `p` y multiplícala por dos»: esa celda *es* `n`, así que `n` pasa de `5` a `10`. Al retornar, `antes` sigue valiendo `5` (era una copia independiente) y `n` vale `10`, produciendo `antes=5 despues=10`. Si hubieras olvidado el `&` y pasado `n` a secas, la función habría doblado una copia y `n` no habría cambiado: el `&` es lo que convierte esto en paso por referencia.

**Rust — la referencia mutable comprobada.** `let mut n: i64 = ...` da `n = 5`, y `n` se declara `mut` porque va a mutarse. `let antes = n` copia el `5` (los enteros son `Copy`). La llamada `doblar(&mut n)` presta `n` de forma **mutable**: el parámetro `x: &mut i64` es una referencia que autoriza escritura. Dentro, `*x *= 2` desreferencia y dobla el original a `10`. El detalle propio de Rust: el *borrow checker* exige que escribas `&mut` tanto en la llamada como en la firma, y garantiza en compilación que no haya dos referencias mutables vivas a la vez —seguridad que C no da—. Salida: `antes=5 despues=10`.

**Java — la caja, porque no hay referencia real.** Aquí está la lección incómoda. `int n = ...` da `n = 5`, y `antes = n` lo copia. Java **no puede** pasar `n` por referencia: los `int` van siempre por valor. El truco es meter el entero en un arreglo: `int[] caja = { n }` crea un objeto arreglo cuyo elemento `[0]` es `5`. Al llamar `doblar(caja)`, Java copia la *referencia al arreglo* (por valor), pero esa copia apunta al mismo arreglo, así que `caja[0] *= 2` muta el `5` a `10` dentro del objeto compartido. Fíjate en lo que **no** cambia: la variable `n` de `main` sigue siendo `5`; lo que cambió fue el contenido del arreglo, que es lo que imprimimos (`caja[0]`). El tercer caso, `7`, recorre lo mismo: `7 * 2 = 14`, salida `antes=7 despues=14`. Tres rutas —puntero, referencia mutable, caja compartida— hacia la misma línea verificada, pero solo dos de ellas (C y Rust, más C# y PHP) son paso por referencia *genuino*; Java y Go y JS simulan el efecto compartiendo un objeto.

## 🔬 Comparación

| Lenguaje | Cómo alcanza la variable del llamador |
|---|---|
| Python | No hay referencia real a un nombre; se comparte un objeto mutable (aquí una lista `caja`). |
| JavaScript | Igual: se envuelve el valor en un objeto `{ v }` y se muta su propiedad. |
| TypeScript | Como JS; el tipo `{ v: number }` documenta la caja sin cambiar la semántica. |
| Java | **Sin** paso por referencia; se usa un arreglo/objeto como caja y se muta su contenido. |
| C# | Paso por referencia **real** con `ref int x`; la firma declara la mutación explícitamente. |
| Go | **Sin** referencia real; se emula con un puntero explícito `*int` y `&n` en la llamada. |
| Rust | Referencia mutable comprobada `&mut i64`; el *borrow checker* garantiza aliasing seguro. |
| C | Punteros `long *p`; `&n` pasa la dirección y `*p` desreferencia para escribir. |
| SQL | No muta variables del llamador; el «después» se calcula por expresión sobre cada fila. |
| PHP | Paso por referencia **real** con `&$x` en la firma; el original se muta directamente. |

La síntesis es la advertencia de Sebesta hecha práctica: solo C, C++, C#, Rust y PHP ofrecen paso por referencia *genuino*, donde la firma crea un alias directo con la variable del llamador. Java y Go —y por extensión JS/TS/Python— pasan siempre por valor; lo que ves como «modificar el original» es compartir un objeto mutable a través de una referencia copiada. La consecuencia práctica es contundente: en Java no existe un `swap(int a, int b)` que funcione, mientras que en C, C#, Rust o PHP se escribe en dos líneas. Distinguir «paso por referencia» de «paso de una referencia por valor» no es pedantería académica: decide qué puedes y qué no puedes hacer en cada lenguaje.

## 🧬 El concepto en la familia

En **C++** las referencias son explícitas y directas: `void doblar(long &x) { x *= 2; }`, y en la llamada basta `doblar(n)` sin ningún `&` —la referencia se establece en la firma, no en el sitio de la llamada, a diferencia de C—. En **Ruby**, todos los argumentos se pasan por referencia de valor (como Java): puedes mutar el objeto recibido, pero no reasignar la variable del llamador. En **Fortran**, históricamente todo se pasaba por referencia por defecto, lo que lo hacía peligrosamente fácil de sorprender con efectos secundarios. Reconocer el patrón —¿el `&` va en la firma o en la llamada?, ¿el lenguaje tiene referencia real o solo objetos compartidos?— permite predecir el comportamiento antes de ejecutar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 080
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar el `&` en C/Go** → causa: pasar `n` en vez de `&n`, con lo que la función dobla una copia y el original no cambia → solución: pasar la dirección (`&n`) cuando la firma espera un puntero, y usar `*p` dentro para tocar el valor apuntado.
- **Creer que Java o Go pasan por referencia** → causa: ver que un objeto mutado «cambia fuera» y generalizarlo a los primitivos, intentando luego un `swap(int, int)` que no compila o no funciona → solución: recordar que ambos pasan por valor; para mutar un primitivo hay que envolverlo (caja) o usar un puntero explícito (Go `*T`).
- **Confundir modificar el objeto con reasignar la variable** → causa: en la llamada por compartición puedes mutar el objeto (`caja[0] = ...`) pero si reasignas el parámetro (`caja = otro`) el llamador no lo ve → solución: distinguir mutar el contenido apuntado de cambiar a qué apunta la referencia local.
- **Efectos secundarios sorpresa** → causa: usar paso por referencia por comodidad y olvidar que la función altera variables del llamador → solución: reservar la mutación por referencia para cuando ese sea el propósito explícito de la función; en lo demás, preferir devolver el valor (paso por valor, clase 079).

## ❓ Preguntas frecuentes

- **¿Referencia o valor?** Usa referencia cuando el propósito de la función *sea* modificar el argumento (un `swap`, un acumulador) o cuando copiar el dato sea caro. Usa valor cuando quieras aislamiento y previsibilidad, que es la mayoría de los casos.
- **¿Java pasa por referencia?** No. Java pasa siempre por valor. Con los objetos, lo que copia es la referencia al objeto, así que puedes *mutar* el objeto pero no *reasignar* la variable del llamador. Con los primitivos, ni siquiera eso: es copia pura. De ahí la caja (`int[]`) en la implementación de esta clase.
- **¿Por qué Go usa punteros si «no tiene» paso por referencia?** Porque los punteros de Go *son* paso por valor de una dirección: copias la dirección, pero como apunta al original, `*p *= 2` alcanza la variable del llamador. Es la forma idiomática de Go para lograr el efecto sin un modo de paso por referencia dedicado.
- **¿Qué protege el `&mut` de Rust que no protege el puntero de C?** El *borrow checker* garantiza en compilación que no exista más de una referencia mutable viva al mismo dato a la vez, eliminando toda una familia de bugs de aliasing y carreras que en C quedan a cargo del programador. Es el tema central de la clase 081.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (11ª ed., Pearson), cap. 9 «Subprograms», §9.5 sobre paso por referencia y el problema de los *alias*.
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions» (argumentos de salida y efectos secundarios).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre referencias, mutabilidad y aliasing.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning); parámetros `ref` y `out`.
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), §2.3.2 sobre punteros.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/), cap. 4 «References and Borrowing».
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), §5.2 «Pointers and Function Arguments».
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 079](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 081 ⏭️](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md)
