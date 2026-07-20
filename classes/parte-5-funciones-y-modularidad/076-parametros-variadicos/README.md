# Clase 076 — Parámetros variádicos

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Definir una función que no fija de antemano cuántos argumentos recibe: acepta uno, tres o cuarenta, y los procesa a todos. Es lo que hay detrás de las funciones que usas a diario sin pensarlo —`print(a, b, c)`, `sum(...)`, `max(...)`, `printf(...)`—: ninguna te obliga a saber por adelantado cuántos valores le vas a dar. La función variádica resuelve la tensión entre una firma, que por naturaleza es fija, y un número de datos que es variable. El truco conceptual es sencillo y elegante: los argumentos sueltos que llegan se **recolectan** dentro de la función en una sola colección —una lista, un slice, un arreglo— y a partir de ahí se recorren con un bucle ordinario.

El motivo profundo conecta con la idea de abstracción que abre *Structure and Interpretation of Computer Programs* de Abelson y Sussman: una buena operación debería expresarse a la altura del problema, no de un caso particular. «Sumar estos números» es la intención; que sean dos o veinte es un detalle que no debería obligarte a elegir entre `suma2`, `suma3` y `suma4`. La variádica captura la operación general de una vez. McConnell, en *Code Complete*, matiza el otro lado de la balanza: la comodidad tiene un coste de claridad, porque una firma variádica dice menos sobre qué espera exactamente, y conviene reservarla para operaciones genuinamente homogéneas —sumar, concatenar, formatear— y no como atajo para eludir un buen diseño de parámetros.

Aquí también los lenguajes divergen, y de forma instructiva. Python (`*args`), JavaScript y TypeScript (rest `...`), Go (`...T`), Java (`T...`), C# (`params`) y PHP (`...$`) tienen sintaxis dedicada. C ofrece variádicas de verdad pero sin red de seguridad: `stdarg.h` y `va_list` te dejan recorrer los argumentos a mano, sin que el compilador verifique cuántos hay ni de qué tipo son. Y Rust, notablemente, **no** tiene funciones variádicas para el código de usuario: cuando necesita el efecto usa slices (`&[T]`) o macros como `println!`, que expanden el número variable en tiempo de compilación. Reconocer en qué campo cae cada lenguaje explica por qué el mismo `suma=6` se escribe de formas tan distintas.

## 🧩 Situación

Estás escribiendo una utilidad para promediar calificaciones. Unas veces son las tres notas de un parcial, otras las diez de un semestre, otras una sola de recuperación. Sin variádicas, tus opciones son incómodas: o defines una familia de funciones —`promedio2`, `promedio3`…— que nunca cubre todos los casos, o obligas a quien llama a construir siempre una lista explícita aunque solo tenga dos números a mano. La función variádica ofrece la tercera vía, la buena: `promedio(8, 9, 7)` cuando tienes los valores sueltos y `promedio(*notas)` cuando ya los tienes en una colección. Una sola definición atiende ambos mundos. En esta clase construimos el caso arquetípico de esa idea, `suma(...nums)`, que suma cuantos enteros le entreguen —uno solo, como en el caso `5`, o cuatro, como en `10 20 30 40`— sin cambiar una línea de su cuerpo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma(...nums) = Σ nums

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20 30 40` | `suma=100` |

## 📖 Definiciones y características

- **Función variádica** — la que acepta un número indeterminado de argumentos en la posición variádica. La firma declara «de aquí en adelante, los que vengan», y el cuerpo los trata como una colección. Es la unidad que vuelve `sum` y `print` capaces de recibir lo que sea.
- **Empaquetar (packing)** — la operación que ocurre dentro de la función: los argumentos sueltos que pasó el llamador se reúnen automáticamente en una sola estructura. En `def suma(*nums)`, al llamar `suma(1, 2, 3)`, el parámetro `nums` se convierte en la tupla `(1, 2, 3)`.
- **Desempaquetar (unpacking / spread)** — la operación inversa y complementaria: expandir una colección ya existente en argumentos sueltos al llamar. `suma(*[1, 2, 3])` en Python o `suma(...[1,2,3])` en JS toman una lista y la «derraman» como si hubieras escrito los elementos uno a uno. Empaquetar y desempaquetar usan el mismo símbolo (`*`, `...`) en lados opuestos: definición frente a llamada.
- **Slice / arreglo receptor** — la forma que toma la colección empaquetada según el lenguaje: una tupla en Python, un arreglo en Java y C#, un slice en Go, un `Vec`/slice en Rust. El detalle importa porque determina qué operaciones tienes disponibles dentro de la función.
- **`va_list` (C)** — el mecanismo de bajo nivel de C para variádicas reales: un puntero móvil sobre la pila de argumentos que recorres con `va_arg`, indicándole tú el tipo de cada uno. Es potente pero inseguro: si te equivocas en el número o el tipo, el compilador no te avisa y el programa falla en ejecución.

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(...nums): DEVOLVER Σ nums
LEER lista ; ESCRIBIR "suma=" suma(lista)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def suma(*nums):
    total = 0
    for n in nums:
        total += n
    return total


nums = [int(x) for x in sys.stdin.read().split()]
print(f"suma={suma(*nums)}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function suma(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function suma(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long suma(int... nums) {
        long total = 0;
        for (int n : nums) total += n;
        return total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        System.out.println("suma=" + suma(nums));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

long Suma(params int[] nums) => nums.Sum(x => (long) x);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(p.Select(int.Parse).ToArray())}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

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

func suma(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	var nums []int
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		nums = append(nums, n)
	}
	fmt.Printf("suma=%d\n", suma(nums...))
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(nums: &[i64]) -> i64 {
    nums.iter().sum()
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(&nums));
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    /* C variádico real usa stdarg.h; aquí sumamos leyendo la entrada. */
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega filas, no argumentos variádicos.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function suma(...$nums) {
    return array_sum($nums);
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "suma=" . suma(...$nums) . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "1 2 3"`, `esperado = "suma=6"`) por tres lenguajes que representan los tres campos: variádica con tupla, variádica con slice y suma directa sin variádica.

**Python (`*args`, empaquetar y desempaquetar).** La línea `nums = [int(x) for x in sys.stdin.read().split()]` lee `"1 2 3"` y construye la lista `[1, 2, 3]`. Aquí aparece la simetría del `*`: la llamada `suma(*nums)` **desempaqueta** esa lista, de modo que la función recibe tres argumentos sueltos, como si hubieras escrito `suma(1, 2, 3)`. Dentro, el parámetro `*nums` **empaqueta** esos tres valores de vuelta en la tupla `(1, 2, 3)`; el mismo símbolo actúa en la llamada (expandir) y en la firma (recolectar). El bucle acumula `0+1=1`, `1+2=3`, `3+3=6` y devuelve `6`, que el f-string vuelve `suma=6`. El caso `5` es revelador: `suma(*[5])` empaqueta la tupla de un elemento `(5,)`, el bucle suma una vez y sale `suma=5`, sin ninguna rama especial para «un solo argumento».

**Go (`...int`, recibido como slice).** Go parsea `"1 2 3"` en un `[]int{1, 2, 3}` acumulando con `append`. La llamada `suma(nums...)` usa el `...` de expansión para pasar el slice existente a una función variádica —sin él, Go se quejaría de tipos—. Dentro, la firma `func suma(nums ...int)` recibe esos valores empaquetados en un slice `nums`, y el `range` los recorre sumando `1`, `2`, `3` hasta `6`. La diferencia semántica con Python es sutil pero real: donde `*nums` de Python produce una tupla inmutable, `nums ...int` de Go produce un slice, una vista sobre un arreglo que dentro de la función podrías incluso mutar.

**C (sin variádica: se lee del flujo).** El programa en C ilustra por contraste lo que las variádicas evitan. C sí tiene variádicas reales vía `stdarg.h`, pero aquí ni siquiera hacen falta: como los números llegan por stdin y no como argumentos de una llamada, el `while (scanf("%ld", &x) == 1)` lee un entero tras otro y acumula `1`, `2`, `3` en `suma` hasta que el flujo se agota, imprimiendo `suma=6`. El comentario del código es honesto: una variádica de verdad en C te obligaría a recorrer `va_list` con `va_arg`, diciéndole tú mismo cuántos valores hay y de qué tipo, sin que el compilador te proteja de un descuadre. Aquí el bucle sobre el flujo cumple el mismo objetivo con menos riesgo.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El marcador variádico cambia de lado y de forma: `*nums` (Python), `...nums` (JS/TS), `nums ...int` (Go), `int... nums` (Java), `params int[]` (C#), `...$nums` (PHP). |
| Semántica | La colección receptora difiere: tupla inmutable (Python), arreglo (Java, C#), slice mutable (Go), `Vec`/slice (Rust). Eso decide qué puedes hacer con los argumentos dentro. |
| Semántica | Seguridad de tipos: en Python, JS, Go, Java, C#, PHP el lenguaje garantiza la recolección; en C con `va_list` el número y el tipo los gestionas a mano, sin verificación del compilador. |
| Paradigmática | Rust no tiene variádicas de usuario: usa slices (`&[T]`, como aquí) o macros como `println!`, que expanden el número variable en compilación. |
| Paradigmática | SQL no recibe argumentos variables: `SUM()` es una función de agregación que colapsa muchas **filas** en un valor, no muchos argumentos de una llamada. |

La síntesis la enmarca McConnell en *Code Complete*: la variádica es una comodidad valiosa cuando la operación es genuinamente homogénea —sumar, concatenar, formatear—, porque expresa la intención general sin multiplicar firmas. Su riesgo es diluir el contrato: una firma variádica dice menos que una de aridad fija sobre qué espera exactamente. Por eso los lenguajes seguros la envuelven en una colección tipada, y C —que la ofrece cruda— exige del programador la disciplina que el compilador no impone. Rust lleva la prudencia al extremo y directamente prefiere slices y macros a abrir esa puerta.

## 🧬 El concepto en la familia

En **Ruby** se escribe `def suma(*nums)`, idéntico a Python, y los argumentos llegan empaquetados en un arreglo. **Swift** usa `func suma(_ nums: Int...)` y los recibe como un `Array`, con la salvedad histórica de que solo permitía un parámetro variádico por función. **Kotlin** los marca con `vararg nums: Int` y, sobre la JVM, los entrega como un arreglo, con el operador spread `*` para reexpandir uno existente. En el otro extremo, **C** con `stdarg.h` representa la variante manual y sin tipos: defines la función con `...`, abres un `va_list`, extraes cada valor con `va_arg` indicando su tipo y cierras con `va_end`; es la maquinaria que `printf` usa por dentro y también la fuente de sus fallos clásicos cuando el formato no cuadra con los argumentos. Ubicar cada lenguaje entre «variádica tipada y automática» y «variádica manual y cruda» predice cuánta vigilancia te exigirá.

## ⚠️ Errores comunes

- **Confundir empaquetar con desempaquetar** → causa: pasar una lista donde la función espera valores sueltos, `suma(nums)` en vez de `suma(*nums)`, con lo que la función recibe un único argumento que es la lista entera → solución: usa el operador de expansión (`*` en Python, `...` en JS/Go) al llamar con una colección ya construida.
- **Olvidar el caso de cero argumentos** → causa: una variádica que asume al menos un valor y falla o devuelve algo indefinido con la colección vacía → solución: diseña el cuerpo para la lista vacía; en una suma, el neutro es `0`, como hacen `reduce(..., 0)` y `total = 0`.
- **Poner un parámetro después del variádico en lenguajes que no lo permiten** → causa: en Go el `...T` debe ser el último parámetro de la firma; ponerlo antes de otro es error de compilación → solución: coloca siempre el parámetro variádico al final.
- **Descuadrar tipo o número en las variádicas de C** → causa: `va_arg` extrae según el tipo que le indicas y `printf` según el formato; si no coinciden con lo pasado, hay comportamiento indefinido sin aviso del compilador → solución: mantén formato y argumentos sincronizados y activa las advertencias del compilador (`-Wformat`).

## ❓ Preguntas frecuentes

- **¿Variádica o pasar una lista?** Variádica cuando quien llama tiene los valores sueltos y agradece la comodidad; una lista explícita cuando ya los tienes en una colección. Los operadores de spread permiten pasar de una forma a la otra sin cambiar la función.
- **¿C tiene variádicas?** Sí, con `stdarg.h` y `va_list`, pero son manuales y sin verificación de tipos: es la maquinaria de `printf`. Es más propensa a errores que las variádicas tipadas de los demás lenguajes.
- **¿Rust tiene variádicas?** No para funciones de usuario: usa slices (`&[T]`) cuando los datos ya están agrupados, o macros como `println!`, que resuelven el número variable de argumentos en tiempo de compilación.
- **¿Cuántos parámetros variádicos puede tener una función?** Como máximo uno, y al final de la firma, en todos los lenguajes del núcleo que los ofrecen: si hubiera dos, el lenguaje no sabría dónde termina el primero y empieza el segundo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 076
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 sobre operaciones expresadas a la altura del problema.
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. 7 sobre `*args` y desempaquetado.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), sobre el uso juicioso de varargs.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley), sobre `...T` y slices.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall), sobre `stdarg.h`.
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 075](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 077 ⏭️](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md)
