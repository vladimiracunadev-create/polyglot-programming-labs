# Clase 108 — Imperativo y estructurado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El **paradigma imperativo** es el más antiguo y el más cercano a la máquina: describe la computación como una secuencia de comandos que modifican un *estado*. Su verbo central es la *asignación*, y su concepto central es la variable como celda de memoria que cambia en el tiempo. SICP dedica todo su capítulo 3 a este modelo y en 3.1 lo formula sin rodeos: introducir la asignación (`set!`, o el `x += y` de los lenguajes de esta clase) significa abandonar el modelo funcional puro donde una variable es solo un nombre para un valor, y adoptar un modelo donde una variable tiene *identidad* y una *historia* de valores. Ese es el precio y el poder del imperativo: ganas la capacidad de acumular y de modelar el paso del tiempo, y pierdes la transparencia referencial (ya no puedes sustituir libremente una variable por su valor).

El adjetivo **estructurado** es la segunda mitad del objetivo, y tiene una historia célebre. En 1968 Edsger Dijkstra publicó "Go To Statement Considered Harmful", argumentando que el salto incondicional (`goto`) volvía el código imposible de razonar porque rompía la correspondencia entre la posición en el texto y el estado del cómputo. La respuesta —desarrollada por Dijkstra, Dahl y Hoare en *Structured Programming* (1972)— fue el teorema de que todo programa puede construirse con solo tres estructuras de control: **secuencia**, **selección** (`if`) e **iteración** (`while`/`for`). El imperativo estructurado es, por tanto, el imperativo disciplinado: mismo poder de cómputo, pero con un flujo de control que se lee de arriba abajo y se puede razonar bloque a bloque.

En esta clase practicarás ambas mitades a la vez sobre un problema mínimo: sumar una lista con un acumulador y un bucle. Verás la asignación repetida que hace evolucionar el estado y las tres estructuras de control canónicas en acción, sin un solo salto. Sebesta (capítulos 7 y 8, expresiones y estructuras de control) es la referencia sistemática de cómo cada lenguaje del núcleo materializa estos mismos mecanismos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Resolver con estado mutable y bucles.
2. Reconocer la secuencia de pasos.
3. Contrastar con el estilo funcional.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Imperativo | Pasos que cambian el estado |
| 2 | Estructurado | Secuencia, selección, iteración |
| 3 | Estado mutable | Variables que cambian |

## 📖 Definiciones y características

- **Imperativo** — paradigma que describe cómo cambiar el estado paso a paso. Clave: bucles y asignaciones.
- **Estructurado** — usa solo secuencia, selección e iteración (sin goto). Clave: código claro.
- **Estado mutable** — variables que cambian durante la ejecución. Clave: el acumulador.

El modelo imperativo es fiel al hardware que hay debajo: un procesador ejecuta instrucciones en orden, leyendo y escribiendo celdas de memoria y saltando cuando una condición lo indica. Van Roy describe este *modelo con estado* como aquel en el que una operación puede tener un efecto que persiste y afecta a operaciones posteriores; el acumulador `suma` es exactamente ese estado persistente. Cada iteración del bucle es una asignación —`suma = suma + x`— cuyo resultado depende del valor previo, es decir, de la historia. Por eso SICP advierte en 3.1 que el orden de ejecución deja de ser un detalle: en el mundo funcional puro puedes reordenar cálculos sin cambiar el resultado, pero en cuanto hay asignación, el *cuándo* importa.

La programación estructurada aporta la disciplina que hace legible ese flujo. Dijkstra observó que un programa lleno de `goto` obliga al lector a reconstruir mentalmente cómo llegó el cómputo a cada punto, porque el estado en una línea depende de saltos que pueden venir de cualquier parte. Restringiéndose a secuencia, selección e iteración, cada estructura tiene una única entrada y una única salida, y el estado en cualquier punto se explica por el texto que hay encima. Nuestro bucle `for x in nums: suma += x` es el caso más limpio: una iteración (recorrer la lista) que contiene una secuencia (la asignación acumuladora), sin ninguna ramificación ni salto. Es el "haz esto, luego esto" de la definición, pero domesticado.

La contraparte —que anticipa las clases funcionales de esta misma parte— es que el acumulador mutable es precisamente lo que el estilo funcional evita: un `reduce(+, nums)` o un `sum(nums)` expresa el mismo pliegue sin exponer la variable que cambia. Guardar en la memoria esa tensión (control explícito del estado frente a expresión declarativa del resultado) es lo que da sentido a toda la Parte 7.

## 🧩 Situación

Piensa en una caja registradora que suma los importes de una compra. El cajero no conoce de antemano cuántos productos habrá: parte de un total en cero y, por cada artículo que pasa, actualiza ese total. Ese gesto —un valor que empieza en un estado inicial y se modifica repetidamente hasta agotar la entrada— es el imperativo en estado puro, y es también el más cercano a "cómo funciona la máquina": haz esto, luego esto, luego esto.

Aquí lo reproducimos con la operación más pequeña que lo captura: leer una línea de enteros separados por espacio y emitir `suma=<total>`. El contrato de [`casos.json`](casos.json) fija tres casos (`1 2 3 → suma=6`, `5 → suma=5`, `10 20 → suma=30`), y la solución canónica es un acumulador que arranca en 0 y un bucle que lo va sumando. No hay atajos declarativos ni fórmulas cerradas: el objetivo pedagógico es *ver* el estado evolucionar, porque es en esa evolución paso a paso donde vive el paradigma.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** acumular la suma recorriendo la lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20` | `suma=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma <- 0 ; PARA CADA x: suma <- suma + x
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys

nums = [int(x) for x in sys.stdin.read().split()]
suma = 0
for x in nums:
    suma += x
print(f"suma={suma}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) suma += x;
console.log(`suma=${suma}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) suma += x;
console.log(`suma=${suma}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long suma = 0;
        for (String s : p) suma += Integer.parseInt(s);
        System.out.println("suma=" + suma);
    }
}
```

### C# · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = 0;
foreach (string s in p) suma += int.Parse(s);
Console.WriteLine($"suma={suma}");
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
	suma := 0
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		suma += n
	}
	fmt.Printf("suma=%d\n", suma)
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut suma: i64 = 0;
    for x in s.split_whitespace() {
        suma += x.parse::<i64>().unwrap();
    }
    println!("suma={suma}");
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) suma += x;
    printf("suma=%ld\n", suma);
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL: SUM() agrega sobre filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$suma = 0;
foreach ($nums as $x) {
    $suma += (int) $x;
}
echo "suma=$suma\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio guiado — recorrido del código

Sigamos el caso `1 2 3 → suma=6` de [`casos.json`](casos.json) para observar el estado mutable en movimiento.

En **Python**, la primera línea de trabajo es `nums = [int(x) for x in sys.stdin.read().split()]`: lee toda la entrada, la parte por espacios y convierte cada token en entero, dejando la lista `[1, 2, 3]`. Aquí está el núcleo imperativo: `suma = 0` crea el acumulador, la celda de estado que vamos a modificar. Luego el bucle `for x in nums: suma += x` es la iteración estructurada. Antes de empezar, `suma` vale 0. En la primera vuelta `x` es 1 y `suma += x` la reasigna a 1; en la segunda `x` es 2 y `suma` pasa a 3; en la tercera `x` es 3 y `suma` llega a 6. Cada `+=` es una asignación cuyo resultado depende del valor previo de `suma` —la "historia" de la que habla SICP 3.1—. Al salir del bucle, `print(f"suma={suma}")` emite `suma=6`. Fíjate en que hay exactamente las tres estructuras de Dijkstra y ninguna más: secuencia (leer, inicializar, imprimir), iteración (el `for`) y ni siquiera hace falta selección.

**C** muestra el mismo esqueleto reducido a lo mínimo, y revela algo que Python oculta. El programa es `long suma = 0, x; while (scanf("%ld", &x) == 1) suma += x;`. No hay lista intermedia: el bucle `while` es la iteración, y su *condición de continuación* es el propio acto de leer, `scanf(...) == 1`, que devuelve 1 mientras logre parsear un entero. Cada vuelta lee un número directamente en la variable `x` (estado mutable) y lo acumula en `suma` (más estado mutable). Con la entrada `1 2 3`: `scanf` lee 1 y `suma` pasa a 1; lee 2 y `suma` a 3; lee 3 y `suma` a 6; al llegar al fin de entrada `scanf` devuelve algo distinto de 1 y el bucle termina. `printf("suma=%ld\n", suma)` cierra con `suma=6`. Este es el imperativo desnudo: el flujo de control *es* el flujo de lectura, y todo el trabajo son asignaciones sobre celdas de memoria. Observa además que `suma` es un `long` de tamaño fijo: a diferencia de Python, una entrada suficientemente grande desbordaría.

Los demás lenguajes son variaciones del mismo tema. **Go** usa `strings.Fields(line)` para trocear y un `for _, s := range ...` con `strconv.Atoi` dentro; **Java** y **C#** parten la cadena con expresiones regulares y recorren con `for`/`foreach` acumulando en un `long`; **Rust** hace `for x in s.split_whitespace()` con `suma += x.parse::<i64>().unwrap()`; **PHP** usa `foreach` sobre el resultado de `preg_split`. En todos, la estructura es idéntica: una variable acumuladora inicializada a 0 y una iteración que la reasigna. **SQL** es el intruso declarativo: `SELECT sum(x) FROM nums` no tiene bucle ni acumulador visible —por eso su bloque incrusta los valores en un `VALUES` y el verificador lo marca *ilustrativo*—; expresa el resultado como una agregación, delegando la iteración al motor. Ejecuta `python scripts/verificar_equivalencia.py 108` para confirmar que todas convergen en las salidas de `casos.json`.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bucle explícito en todos los imperativos. |
| Semántica | Modifica un acumulador; el estado evoluciona. |
| Paradigmática | El funcional evitaría el acumulador mutable con reduce. |

Las diferencias reales aparecen en cómo cada lenguaje controla el estado y sus límites. C es el más literal: la condición del `while` es el propio `scanf`, mezclando lectura y control en una sola expresión, y el acumulador es un `long` de 64 bits sin red de seguridad ante el desbordamiento. Rust obliga a decidir explícitamente cómo tratar un token no numérico —el `.unwrap()` haría *panic*—, materializando su filosofía de que los errores no se ignoran silenciosamente, mientras que Go y Java descartan el error de parseo (`n, _ := ...`) siguiendo una tradición más permisiva. Python destaca por sus enteros de precisión arbitraria: su `suma` nunca desborda, algo imposible en los lenguajes de tipo fijo. Y aunque todos aquí eligen el bucle imperativo, varios podrían escribir el mismo cálculo en estilo funcional (`sum(nums)` en Python, `nums.iter().sum()` en Rust, `Arrays.stream(...).sum()` en Java): la clase mantiene el bucle a propósito para que el estado mutable —el corazón del paradigma— quede a la vista.

## 🧬 El concepto en la familia

El estilo imperativo estructurado es el sustrato común de casi todos los lenguajes del núcleo, porque casi todos descienden —directa o indirectamente— de la tradición de Algol, C y Pascal que codificó las tres estructuras de control de Dijkstra. C, Go, Java, C#, JavaScript, TypeScript, PHP, Rust y Python ofrecen bucles y asignación como ciudadanos de primera clase, y ninguno de ellos incluye ya el `goto` como herramienta idiomática (C lo conserva pero su uso está mal visto; la mayoría directamente no lo tiene). SQL es la excepción reveladora: al ser puramente declarativo, no expone al programador ni el bucle ni el estado mutable local, y por eso mismo su solución a este problema no "recorre" nada, sino que agrega. Que el imperativo sea tan universal no lo hace obligatorio: es el paradigma por defecto, el que se aprende primero, pero convive en cada uno de estos lenguajes con capas funcionales y orientadas a objetos que las clases siguientes irán descubriendo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 108
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No inicializar el acumulador** → causa: usar una variable antes de darle valor, o asumir que "empieza en 0" cuando el lenguaje no lo garantiza (en C una variable local sin inicializar contiene basura) → remedio: escribe siempre `suma = 0` explícitamente antes del bucle; es una línea que documenta el estado inicial y evita resultados no deterministas.
- **Efectos secundarios ocultos** → causa: modificar estado que otras partes del programa también leen o escriben, de modo que el valor final depende de un orden difícil de rastrear → remedio: mantén el estado mutable lo más local posible (una variable dentro de la función, no global) para que su historia completa quepa en un solo bloque legible, tal como recomienda la programación estructurada.
- **Bucle que no avanza o se pasa de largo** → causa: una condición de continuación mal escrita (índice que no se incrementa, comparación `<` frente a `<=`) que produce un bucle infinito o que salta un elemento → remedio: verifica que cada iteración modifica el estado que controla la condición y comprueba a mano el primer y el último valor procesado con un caso pequeño de `casos.json`.

## ❓ Preguntas frecuentes

- **¿Cuándo conviene el imperativo frente al funcional?** El imperativo da control directo sobre el estado y suele traducirse a un código muy eficiente, ideal cuando el rendimiento o la interacción con recursos (memoria, dispositivos) es crítica. El funcional gana en componibilidad y en facilidad de razonar sin efectos. Para un pliegue simple como esta suma, ambos son válidos; el imperativo se hace preferible cuando necesitas instrumentar cada paso o cortar el bucle a mitad según una condición.
- **¿"Estructurado" significa literalmente "sin `goto`"?** En esencia sí: significa construir todo el flujo con secuencia, selección e iteración, las tres estructuras que Böhm y Jacopini demostraron suficientes y que Dijkstra defendió frente al salto incondicional. En la práctica moderna casi ningún lenguaje del núcleo ofrece `goto` idiomático, así que hoy programas estructurado casi sin darte cuenta.
- **¿La asignación no existe en el paradigma funcional?** No como reasignación destructiva. El estilo funcional puro trabaja con *ligaduras* inmutables: un nombre se asocia a un valor una vez y no cambia. La diferencia frente al `suma += x` de aquí es justamente lo que SICP explora en el capítulo 3: introducir la asignación mutable cambia el modelo de cómputo y el modo de razonar sobre él.

## 🔗 Referencias

**Libros de la parte:**

- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press). El modelo con estado y la semántica de la asignación.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press). Capítulo 3, sección 3.1: asignación, estado local y sus consecuencias sobre el razonamiento.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson). Capítulos 7 y 8: expresiones, asignación y estructuras de control estructuradas.
- E. W. Dijkstra — "Go To Statement Considered Harmful" (*Communications of the ACM*, 1968); O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press, 1972).

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

> [⏮️ Clase 107](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 109 ⏭️](../../parte-7-paradigmas/109-procedimental-y-modular/README.md)
