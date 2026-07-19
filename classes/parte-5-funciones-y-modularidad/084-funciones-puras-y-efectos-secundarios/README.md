# Clase 084 — Funciones puras y efectos secundarios

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Aprender a distinguir las funciones que solo **calculan** de las que además **cambian el mundo**. Una función es **pura** cuando su resultado depende únicamente de sus argumentos y no observa ni modifica nada externo: llamada con las mismas entradas devuelve siempre la misma salida, y no deja rastro —no imprime, no escribe archivos, no toca variables globales, no altera sus parámetros—. Una función con **efectos secundarios (side effects)** hace algo más que devolver un valor: registra en un log, incrementa un contador global, envía una petición de red. La distinción parece filosófica, pero es una de las palancas más prácticas de la ingeniería de software: las funciones puras son las que puedes probar sin montar un escenario, cachear sin miedo, ejecutar en paralelo sin sincronizar y razonar leyéndolas, sin ejecutarlas mentalmente.

El fundamento teórico es la **transparencia referencial**, un concepto que Abelson y Sussman ponen en el centro de *Structure and Interpretation of Computer Programs*. En §1.1 muestran cómo una expresión puede sustituirse por su valor sin cambiar el significado del programa —el modelo de sustitución— y en §3 explican por qué la introducción de la **asignación** y el estado mutable rompe justamente esa propiedad: a partir de ahí «igual» deja de significar «intercambiable», y el razonamiento se vuelve mucho más difícil. Una función pura conserva la transparencia referencial; una impura la destruye. Ese es el eje conceptual de la clase.

Robert C. Martin, en *Clean Code*, traduce esa teoría a una regla de oficio: las funciones no deberían tener efectos ocultos. Un efecto secundario sorpresa —una función que promete calcular algo y de paso muta un objeto que recibió— es, en sus palabras, una mentira; obliga a leer la implementación para saber qué hace de verdad. El objetivo profundo no es prohibir los efectos, que son imprescindibles (un programa que no produce ningún efecto es un programa que no sirve para nada), sino **aislarlos**: mantener un núcleo puro grande y empujar los efectos a una frontera pequeña y visible.

## 🧩 Situación

Tienes una función que calcula el precio con impuestos y, «ya que estaba», escribe una línea en el log de auditoría cada vez que se la llama. Un día quieres probarla: para verificar que `precio(100)` da `121` necesitas montar un sistema de logging, un archivo temporal y limpiar después. Peor: alguien la llama dos veces sin querer y aparecen dos entradas de auditoría fantasma. El cálculo era trivial; el efecto secundario lo volvió frágil. Si en cambio la función solo calculara y devolviera el número, probarla sería una línea (`assert precio(100) == 121`), podrías memoizar el resultado y llamarla mil veces sin consecuencias. El dolor que resuelve la pureza es este: separar lo que *decide un valor* de lo que *actúa sobre el mundo*, para que cada parte sea simple por separado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `puro=<n²>`
- **Regla:** cuadrado(n) = n * n (sin efectos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `puro=16` |
| `-3` | `puro=9` |
| `0` | `puro=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION cuadrado(n): DEVOLVER n*n   // sin tocar nada externo
LEER n ; ESCRIBIR "puro=" cuadrado(n)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):

### Python · `python main.py`

```python
import sys


def cuadrado(n):
    return n * n  # pura: sin efectos secundarios


n = int(sys.stdin.readline())
print(f"puro={cuadrado(n)}")
```

### JavaScript · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function cuadrado(n) {
  return n * n;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
```

### TypeScript · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function cuadrado(n: number): number {
  return n * n;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
```

### Java · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long cuadrado(long n) {
        return n * n;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        System.out.println("puro=" + cuadrado(n));
    }
}
```

### C# · `dotnet run`

```csharp
using System;

long Cuadrado(long n) => n * n;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"puro={Cuadrado(n)}");
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

func cuadrado(n int64) int64 {
	return n * n
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	fmt.Printf("puro=%d\n", cuadrado(n))
}
```

### Rust · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn cuadrado(n: i64) -> i64 {
    n * n
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("puro={}", cuadrado(n));
}
```

### C · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long cuadrado(long n) {
    return n * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("puro=%ld\n", cuadrado(n));
    return 0;
}
```

### SQL · `sqlite3 :memory: < main.sql`

```sql
-- SQL (declarativo) favorece expresiones puras.
WITH nums(n) AS (VALUES (4), (-3), (0))
SELECT printf('puro=%d', n * n) AS resultado FROM nums;
```

### PHP · `php main.php`

```php
<?php
function cuadrado($n) {
    return $n * $n;
}

$n = (int) trim(fgets(STDIN));
echo "puro=" . cuadrado($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el segundo caso de `casos.json` (`stdin = "-3"`, `esperado = "puro=9"`) y prestemos atención a cómo cada programa separa el **núcleo puro** del **efecto de I/O** que lo rodea.

**Python.** El programa tiene dos mitades muy distintas. `cuadrado(n)` es pura: recibe `n`, devuelve `n * n`, no toca nada más —el comentario lo subraya—. Con `n = -3`, calcula `(-3) * (-3) = 9`. La otra mitad, `n = int(sys.stdin.readline())` y `print(...)`, es *toda* la parte impura del programa: leer de stdin y escribir en stdout son efectos secundarios. Fíjate en el diseño: el efecto está confinado a las líneas de arranque, y el cálculo vive aislado en su función. Podrías probar `cuadrado(-3) == 9` sin stdin ni stdout. Esa separación entre un núcleo determinista y una cáscara de efectos es exactamente lo que recomienda Martin, y es visible aquí en cuatro líneas.

**Rust.** La firma `fn cuadrado(n: i64) -> i64` describe una función total y determinista: entra un `i64`, sale un `i64`, y su cuerpo `n * n` no menciona nada externo. Con `n = -3` produce `9`. Todo el ruido —crear un `String`, leer stdin con `read_to_string`, parsear— queda en `main`, la frontera con el mundo. Rust no *fuerza* la pureza (no hay una marca de compilador que la exija aquí), pero su cultura empuja hacia funciones así: entradas explícitas, salida por valor, sin estado global. El resultado impreso es `puro=9`.

**SQL — pureza por construcción.** El caso de SQL es el más ilustrativo del contraste paradigmático. No hay una «función que se llama»: la expresión `n * n` se evalúa sobre cada fila de la CTE `nums(n)` que contiene `4`, `-3` y `0`. Para la fila `-3`, `printf('puro=%d', n * n)` produce `puro=9`. Un motor SQL puede reordenar, paralelizar o cachear la evaluación de esa expresión precisamente porque es pura: no depende de nada más que del valor de la fila. Aquí la pureza no es una virtud que el programador cultiva, sino una propiedad que el paradigma declarativo asume por defecto —el mismo terreno donde Haskell separa los efectos con el tipo `IO`—. Los tres llegan a `9`, pero SQL lo hace sin siquiera nombrar el concepto de «llamada con efecto».

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | La función es casi idéntica en los diez: recibe un número y devuelve `n * n`. La pureza no se ve en la sintaxis. |
| Semántica | La pureza es una propiedad del *diseño*, no del lenguaje: Python, JS, Go, Rust, Java, C, C#, PHP permiten funciones tanto puras como impuras; la responsabilidad de mantenerlas puras es del programador. |
| Semántica | Ningún lenguaje del núcleo *verifica* la pureza en compilación. La marca `const`/`readonly` limita la mutación de datos, pero no equivale a garantizar ausencia de efectos. |
| Paradigmática | SQL (declarativo) evalúa expresiones sin efectos por defecto; el motor puede reordenarlas y cachearlas. Haskell va más lejos y separa los efectos con el sistema de tipos: una función que hace I/O *tiene* que declararlo en su tipo (`IO`). |

La síntesis la ofrece *SICP*: mientras el programa se limita a construir valores a partir de valores (§1.1), el modelo de sustitución basta para razonar y todo es intercambiable por su resultado. En cuanto entra la asignación y el estado mutable (§3), esa comodidad se pierde y hay que llevar la cuenta del *tiempo* y del *orden*. La lección práctica es que la pureza no es un rasgo del lenguaje sino una decisión de arquitectura que casi cualquier lenguaje permite tomar: cuanto mayor sea el núcleo puro y más delgada la frontera de efectos, más fácil será probar, cachear y paralelizar el sistema.

## 🧬 El concepto en la familia

En **Haskell** la separación es estructural: el sistema de tipos distingue una función pura (`Int -> Int`) de una acción con efectos (`IO ()`), y el compilador impide mezclarlas por accidente; los efectos se orquestan a través del tipo `IO`, no se esparcen. En **Clojure** y otros Lisps funcionales, las estructuras de datos son inmutables por defecto, lo que empuja las funciones hacia la pureza sin obligarla. En **Scala**, la comunidad de programación funcional usa envoltorios como `IO` (Cats Effect, ZIO) para tratar los efectos como valores describibles y así conservar la transparencia referencial. En **Rust**, la inmutabilidad por defecto (`let` frente a `let mut`) y la ausencia de estado global fácil empujan cultural, no formalmente, hacia el mismo lugar. El patrón transversal: cuanto más difícil pone el lenguaje mutar y producir efectos «gratis», más puro tiende a ser el código idiomático.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 084
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar cálculo con impresión o estado** → causa: una función que calcula *y* además imprime o guarda; se vuelve difícil de probar y de reutilizar → solución: separa el cálculo puro (devuelve un valor) del efecto (I/O), como hacen todas las implementaciones al dejar `print`/`scanf` fuera de `cuadrado`.
- **Mutar un argumento recibido** → causa: la función modifica la lista u objeto que le pasaron, sorprendiendo a quien la llamó; Martin lo llama un efecto secundario oculto → solución: trabaja sobre una copia y devuelve el resultado, o documenta la mutación de forma explícita en el nombre.
- **Depender de estado global o del reloj** → causa: la función lee una variable global, la hora o un aleatorio, y deja de ser determinista → solución: pasa esos valores como parámetros; una función que recibe el «ahora» en vez de leerlo vuelve a ser pura y testeable.
- **Confundir «no devuelve nada» con «pura»** → causa: pensar que una función `void`/sin retorno es inofensiva, cuando justamente si no devuelve nada su único propósito suele ser un efecto → solución: una función `void` que hace algo útil es, por definición, impura; identifícala como parte de la frontera de efectos.

## ❓ Preguntas frecuentes

- **¿Todo debe ser puro?** No, y sería imposible: un programa sin efectos (I/O, red, pantalla) no interactúa con nada. La meta es aislar los efectos en una frontera delgada y mantener puro el núcleo de lógica, que es la parte más grande y la que más se prueba.
- **¿Por qué importan tanto las funciones puras?** Porque desbloquean tres superpoderes: se prueban con un simple `assert` sin montar escenario, se pueden **memoizar** (cachear el resultado, ya que la misma entrada da la misma salida) y se pueden **paralelizar** sin sincronización, porque no comparten estado mutable.
- **¿Es lo mismo pureza que transparencia referencial?** Están íntimamente ligadas: una función pura garantiza que su llamada es referencialmente transparente, es decir, sustituible por su resultado sin cambiar el significado del programa —la propiedad que *SICP* pone como base del razonamiento con el modelo de sustitución—.
- **¿La inmutabilidad hace pura a una función?** Ayuda pero no basta: trabajar con datos inmutables elimina una fuente de efectos (mutar argumentos), pero una función puede seguir siendo impura leyendo el reloj, un global o haciendo I/O aunque no mute nada.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 (modelo de sustitución) y §3.1 (asignación y el fin de la transparencia referencial).
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions» (sección «Side Effects»).
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 sobre rutinas con contrato claro.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly).
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley) (ítem sobre minimizar la mutabilidad).
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 083](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 085 ⏭️](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md)
