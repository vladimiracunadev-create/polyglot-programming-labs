# Clase 079 — Paso por valor

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el modo de paso de parámetros más simple y más frecuente: el **paso por valor**. Cuando llamas a una función pasándole un argumento por valor, la función no recibe *tu* variable, sino una **copia** independiente de su contenido. Modificar esa copia dentro de la función es como escribir en una fotocopia: por mucho que taches y reescribas, el documento original en tu escritorio queda intacto. Es el modo por defecto en la inmensa mayoría de los lenguajes, y comprenderlo bien evita la clase de sorpresa más común entre principiantes: esperar que una función «devuelva» un cambio a través de un parámetro que en realidad nunca tocó el original.

Robert Sebesta, en *Concepts of Programming Languages*, cataloga los **modos de paso de parámetros** —por valor, por resultado, por valor-resultado, por referencia y por nombre— según la dirección en que fluye la información entre el llamador y la subrutina. El paso por valor es de una sola dirección: los datos entran (del argumento al parámetro) pero no salen; el parámetro es, en su modelo, una variable local de la función que se *inicializa* con el valor del argumento. Esa definición es la que hay que interiorizar: el parámetro no es un alias de tu variable, es una variable nueva que empieza teniendo el mismo valor.

El objetivo hondo es apreciar por qué este aislamiento es una virtud y no una limitación. Una función que solo puede leer copias no puede alterar por sorpresa el estado de quien la llama; su único canal de salida legítimo es el `return`. Eso hace el código predecible: para saber qué cambia una función, basta mirar qué devuelve, no auditar cada variable que le pasaste.

## 🧩 Situación

Pasas un número `n` a una función que, dentro, lo duplica y lo usa para un cálculo. Al volver de la llamada, imprimes `n` esperando ver el doble... y sigue valiendo lo de antes. El principiante sospecha un bug; en realidad es el lenguaje comportándose exactamente como promete. La función recibió una copia de `n`, la dobló, y esa copia murió al terminar la función. Tu `n` nunca estuvo en juego. Entender esto de una vez ahorra horas de depuración estéril y, sobre todo, enseña la disciplina correcta: si quieres el nuevo valor, **devuélvelo y recógelo** (`n = doblar(n)`), no confíes en que la función mute tu variable a distancia.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `original=<n> local=<2n>`
- **Regla:** la función duplica una copia; el original permanece

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `original=5 local=10` |
| `3` | `original=3 local=6` |
| `0` | `original=0 local=0` |

## 📖 Definiciones y características

- **Paso por valor** — el argumento se **copia** en el parámetro al invocar la función. En términos de Sebesta, el parámetro se comporta como una variable local inicializada con el valor del argumento; la información viaja del llamador a la función, nunca de vuelta por ese canal. El original queda blindado.
- **Copia** — el duplicado independiente que vive dentro de la función. Ocupa su propia posición en memoria (típicamente la pila de la llamada) y desaparece cuando la función retorna. Escribir en la copia no roza al original.
- **Parámetro local** — la variable de la función que contiene la copia. Aquí se llama `x`: nace con el valor de `n`, se modifica libremente y muere al terminar. Que el llamador use `n` y la función use `x` no cambia nada; aunque compartieran nombre, seguirían siendo variables distintas.
- **Efecto en el llamador** — en el paso por valor puro, **ninguno**. Esa ausencia de efecto es precisamente su garantía: una función que recibe todo por valor no puede tener el efecto secundario de alterar las variables de quien la llamó.
- **El matiz de la «llamada por compartición»** — cuidado con extrapolar. En Java, JavaScript, Python y PHP, los *objetos* también se pasan por valor... pero lo que se copia es la **referencia** al objeto, no el objeto entero. Esto se conoce como *call by sharing* o *call by object*: la función recibe una copia del puntero, así que puede *mutar* el objeto apuntado (y el llamador lo verá), aunque no puede *reasignar* la variable del llamador. En esta clase trabajamos solo con enteros primitivos, donde no hay ambigüedad: se copia el valor y punto. El matiz de los objetos se desarrolla en la clase 080.

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
local <- doblar(n)   // dentro trabaja una copia
ESCRIBIR "original=" n " local=" local
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def doblar(x):
    x = x * 2  # modifica la copia local
    return x


n = int(sys.stdin.readline())
local = doblar(n)
print(f"original={n} local={local}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function doblar(x) {
  x = x * 2;
  return x;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const local = doblar(n);
console.log(`original=${n} local=${local}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function doblar(x: number): number {
  x = x * 2;
  return x;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const local: number = doblar(n);
console.log(`original=${n} local=${local}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int doblar(int x) {
        x = x * 2;
        return x;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int local = doblar(n);
        System.out.println("original=" + n + " local=" + local);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

int Doblar(int x) {
    x = x * 2;
    return x;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int local = Doblar(n);
Console.WriteLine($"original={n} local={local}");
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

func doblar(x int) int {
	x = x * 2
	return x
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	local := doblar(n)
	fmt.Printf("original=%d local=%d\n", n, local)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn doblar(mut x: i64) -> i64 {
    x *= 2;
    x
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let local = doblar(n);
    println!("original={n} local={local}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long doblar(long x) {
    x = x * 2; /* modifica la copia local */
    return x;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long local = doblar(n);
    printf("original=%ld local=%ld\n", n, local);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: sin variables del llamador; la expresión produce el valor.
WITH nums(n) AS (VALUES (5), (3), (0))
SELECT printf('original=%d local=%d', n, n * 2) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function doblar($x) {
    $x = $x * 2;
    return $x;
}

$n = (int) trim(fgets(STDIN));
$local = doblar($n);
echo "original=$n local=$local\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "5"`, `esperado = "original=5 local=10"`) por tres lenguajes que copian el valor de tres maneras que, al final, coinciden.

**Python.** La línea `n = int(sys.stdin.readline())` fija `n = 5` en el ámbito principal. Al llamar `doblar(n)`, Python vincula el parámetro `x` al mismo entero `5`. Dentro, `x = x * 2` **no** modifica el `5` original (los enteros de Python son inmutables): crea un nuevo entero `10` y hace que `x` apunte a él, dejando `n` fuera intacto apuntando todavía a `5`. La función devuelve `10`, que se recoge en `local`. Al imprimir, `n` sigue siendo `5` y `local` es `10`, produciendo `original=5 local=10`. La reasignación de `x` fue puramente local: nunca hubo forma de que tocara `n`.

**Java.** `int n = Integer.parseInt(...)` deja `n = 5`. La llamada `doblar(n)` copia el valor `5` en el parámetro `int x`. Aquí el mecanismo es el más literal de todos: `x` es una variable nueva en la pila, inicializada con la copia `5`. La sentencia `x = x * 2` sobrescribe *esa copia* a `10` sin que `n` se entere —los primitivos de Java siempre se pasan por valor, sin excepción—. La función retorna `10`, `local` lo guarda, y la salida es `original=5 local=10`. Si en vez de `int` se tratara de un objeto, la historia tendría el matiz de la referencia copiada; con un primitivo, es copia pura.

**Go.** `n, _ := strconv.Atoi(...)` da `n = 5`. Go, igual que C, es estricta y exclusivamente de paso por valor: `doblar(n)` copia el `5` en `x`, `x = x * 2` lo convierte en `10` dentro de la función, y `n` en `main` no se mueve. El tercer caso, `0`, es el más elocuente: `doblar(0)` devuelve `0 * 2 = 0`, así que `original=0 local=0` —copiar cero y doblarlo sigue siendo cero, pero el punto pedagógico se mantiene: hubo una copia, se operó sobre ella, y el original nunca corrió peligro—. Tres lenguajes, tres formas de decir «esto es una copia», la misma salida verificada.

## 🔬 Comparación

| Lenguaje | Cómo trata el paso por valor de un entero |
|---|---|
| Python | *Call by sharing*: se copia la referencia, pero el entero es inmutable, así que se comporta como copia de valor. |
| JavaScript | Los `number` son primitivos e inmutables: copia de valor pura. |
| TypeScript | Igual que JS en runtime; el tipo `number` no altera la semántica, solo la comprobación. |
| Java | Los primitivos (`int`, `double`...) **siempre** por valor; los objetos, referencia copiada por valor. |
| C# | Igual que Java: `struct`/primitivos por valor; el modo se puede cambiar con `ref` (clase 080). |
| Go | Exclusivamente por valor; para mutar el original hay que pasar un puntero `*T` explícito. |
| Rust | Los tipos `Copy` (como los enteros) se copian al pasar; el `mut x` del parámetro es local. |
| C | El modelo canónico de paso por valor; para modificar el original se pasa un puntero. |
| SQL | No hay variables del llamador que mutar: cada fila produce su valor por expresión. |
| PHP | Por valor por defecto; con `&$x` se pasaría por referencia (clase 080). |

La síntesis vuelve a Sebesta: el paso por valor es de un solo sentido, y esa unidireccionalidad es su regalo. Donde los lenguajes divergen no es en el entero —todos lo copian— sino en qué ocurre con datos compuestos: Java, JS, Python y PHP copian la *referencia* al objeto (llamada por compartición), mientras que C, Go y Rust copian el dato o exigen un puntero explícito para compartir. Pero para el primitivo de esta clase todos convergen en la misma promesa: lo que le hagas a la copia se queda en la copia.

## 🧬 El concepto en la familia

En **Ruby** los enteros son objetos inmutables (`Integer`): aunque técnicamente todo se pasa por referencia de valor, no puedes mutar un entero, así que el efecto observable es idéntico al paso por valor de esta clase. En **C++**, el paso por valor es el modo por defecto igual que en C (`void doblar(long x)`), pero el lenguaje ofrece además referencias explícitas `&` y referencias constantes `const &` para evitar copias caras sin perder el aislamiento. En **Swift**, los tipos de valor (`struct`, `Int`) se copian al pasar, mientras que las clases se comparten por referencia: la misma dicotomía primitivo/objeto que ves aquí.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 079
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que el original cambie** → causa: creer que asignar al parámetro dentro de la función afecta a la variable del llamador, confundiendo el paso por valor con el paso por referencia → solución: recordar que el parámetro es una copia local; si quieres el nuevo valor, devuélvelo con `return` y recógelo (`n = doblar(n)`).
- **Modificar el parámetro creyendo que propaga el cambio** → causa: escribir `x = x * 2` y no capturar el retorno, perdiendo el resultado → solución: asignar la llamada a una variable; el único canal de salida del paso por valor es el valor retornado.
- **Extrapolar la copia del primitivo a los objetos** → causa: asumir que como el entero no cambia, tampoco cambiará una lista o un objeto que pases → solución: entender la llamada por compartición: con objetos se copia la referencia, así que *mutarlos* sí afecta al llamador (clase 080).
- **Confiar en efectos secundarios en vez de retornos** → causa: diseñar funciones que «deberían» cambiar sus argumentos → solución: preferir funciones puras que reciban por valor y devuelvan el resultado; son más fáciles de razonar y probar.

## ❓ Preguntas frecuentes

- **¿Todo se pasa por valor?** Los primitivos, sí, en todos los lenguajes del núcleo. Con los objetos el matiz es que lo copiado es la referencia (llamada por compartición): puedes mutar el objeto, pero no reasignar la variable del llamador. Lo vemos a fondo en la clase 080.
- **¿Por qué es seguro el paso por valor?** Porque una función que solo recibe copias no puede alterar por sorpresa el estado de quien la llama. Su comportamiento queda contenido: para saber qué cambia, basta mirar qué devuelve.
- **¿No es un desperdicio copiar datos grandes?** Para un entero, la copia es trivial. Para estructuras grandes sí puede costar, y por eso lenguajes como C++ ofrecen `const &` (referencia de solo lectura) y Rust ofrece el préstamo `&` (clase 081): compartir sin copiar y sin permitir mutación.
- **¿El `mut x` de Rust rompe el paso por valor?** No. `mut x: i64` significa «recibí una copia y me permito modificarla dentro»; sigue siendo una copia local. El original del llamador no se ve afectado.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (11ª ed., Pearson), cap. 9 «Subprograms», §9.5 sobre modos de paso de parámetros (pass-by-value).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions» (sobre efectos secundarios).

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre variables, referencias y objetos (call by sharing).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/), cap. 4 sobre `Copy`.
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), §5.2 sobre punteros y argumentos.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 078](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 080 ⏭️](../../parte-5-funciones-y-modularidad/080-paso-por-referencia/README.md)
