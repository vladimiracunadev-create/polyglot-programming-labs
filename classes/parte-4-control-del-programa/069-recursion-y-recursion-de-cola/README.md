# Clase 069 — Recursión y recursión de cola

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La recursión es la técnica en la que una función resuelve un problema invocándose a sí misma sobre una versión más pequeña del mismo problema. Existe porque hay estructuras y definiciones que son recursivas por naturaleza —un árbol es un nodo con subárboles, un directorio contiene directorios, una expresión aritmética contiene expresiones—, y describirlas con un bucle obliga a inventar y administrar a mano una pila auxiliar que el lenguaje ya te da gratis en la pila de llamadas. Toda función recursiva se apoya en dos piezas inseparables: el **caso base**, que se resuelve sin volver a llamarse, y el **caso recursivo**, que reduce el problema acercándolo al caso base. Si falta el primero, la recursión no termina; si el segundo no reduce de verdad, tampoco.

En esta clase calculamos F(n) de Fibonacci, definido recursivamente como F(0)=0, F(1)=1 y F(n)=F(n-1)+F(n-2), porque su traducción a código es literal y expone de golpe las dos caras de la recursión: la elegancia expresiva y el coste. Veremos qué ocurre por debajo —cómo cada llamada apila un *marco de pila* con la dirección de retorno, los parámetros y las variables locales, y qué pasa cuando esa pila se agota—, por qué la versión ingenua de Fibonacci es exponencial y cómo la memoización la desinfla, y qué es la **recursión de cola**: la forma particular en que la llamada recursiva es la última operación de la función, lo que permitiría reutilizar el marco actual en vez de apilar uno nuevo. Ese "permitiría" es deliberado: unos lenguajes garantizan esa optimización por estándar y otros la rechazan explícitamente, y esa divergencia es una de las más instructivas del panorama políglota.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una función recursiva con caso base.
2. Traducir una definición recursiva a código.
3. Reconocer el coste de la recursión ingenua.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Recursión | Una función que se llama a sí misma |
| 2 | Caso base | Dónde para la recursión |
| 3 | Caso recursivo | Reducir hacia el caso base |
| 4 | Coste | Fibonacci ingenuo es exponencial |

## 📖 Definiciones y características

- **Recursión** — técnica en que una función se invoca a sí misma. Clave: necesita un caso base.
- **Caso base** — el que se resuelve sin recursión. Clave: evita la recursión infinita.
- **Caso recursivo** — reduce el problema hacia el caso base. Clave: debe acercarse a él.
- **Recursión de cola** — la llamada recursiva es lo último que se hace. Clave: algunos lenguajes la optimizan.
- **Marco de pila** — el bloque que cada llamada apila. Clave: guarda dirección de retorno, parámetros y locales.
- **Memoización** — cachear resultados ya calculados. Clave: convierte Fibonacci exponencial en lineal.

Sebesta, en el capítulo de subprogramas de *Concepts of Programming Languages*, describe el mecanismo que hace posible la recursión: cada invocación crea un *registro de activación* (el marco de pila) con la dirección de retorno, los parámetros, las variables locales y el enlace al marco anterior. La recursión no es magia sintáctica, es simplemente lo que ocurre cuando ese mecanismo se aplica a una función que se nombra a sí misma. De ahí sale también su coste: la memoria consumida es O(profundidad), y esa profundidad choca con un límite real. Python la corta artificialmente con `sys.setrecursionlimit`, cuyo valor por defecto es 1000, y lanza `RecursionError` al superarlo; la JVM lanza `StackOverflowError` cuando se agota la pila del hilo, que suele estar en torno a 1 MB por hilo (en Linux el hilo principal de un proceso nativo suele tener 8 MB por defecto). Estos no son detalles de implementación anecdóticos: son la frontera práctica entre una recursión que funciona y un proceso que muere.

La **recursión de cola** es la respuesta técnica a ese límite. Si la llamada recursiva es la *última* operación de la función —no queda nada por hacer con su resultado salvo devolverlo—, el marco actual ya no hace falta y puede reutilizarse: la recursión se ejecuta en espacio constante, exactamente como un bucle. Aquí los lenguajes se separan de forma tajante. Scheme lo *exige* en su estándar (R5RS y R7RS obligan a que las llamadas en posición de cola no hagan crecer la pila), y Erlang y Haskell lo aplican como base de su modelo de ejecución. JavaScript lo especificó en ES2015 como *proper tail calls*, pero sólo JavaScriptCore (Safari) llegó a implementarlo. Python lo rechaza a propósito: Guido van Rossum argumentó que destruye las trazas de pila y con ellas la depurabilidad, y prefirió mantener el diagnóstico legible. La JVM no lo soporta a nivel de bytecode, lo que afecta a Java, Scala y Kotlin —este último sólo optimiza la autorrecursión con el modificador `tailrec`—. Go no lo garantiza, y Rust tampoco, aunque LLVM a veces lo aplica por su cuenta. En C y C++ los compiladores lo hacen habitualmente con `-O2`, pero ningún estándar lo obliga. La lección de fondo, resultado de la teoría de la computación, es que recursión e iteración son equivalentes en poder expresivo: todo programa recursivo tiene un equivalente iterativo con una pila explícita, y toda recursión de cola tiene un equivalente iterativo trivial. Lo que cambia es qué versión resulta legible y cuál se paga en memoria.

## 🧩 Situación

La recursión es el modo natural de trabajar con datos que son ellos mismos recursivos, y eso abarca buena parte de la ingeniería real: recorrer un árbol de directorios, analizar JSON o XML anidado, evaluar el árbol sintáctico que produce un compilador, atravesar el DOM de una página, ordenar con quicksort o mergesort. En todos esos casos la estructura del código refleja la estructura del dato, y esa correspondencia es lo que hace el programa legible. La alternativa iterativa existe siempre, pero exige gestionar a mano una pila explícita de nodos pendientes, con el riesgo de errores que eso conlleva.

El porqué de ingeniería tiene dos caras, y ambas cuestan dinero. La primera es el desbordamiento de pila: una función recursiva que funciona con un árbol de diez niveles puede tumbar un proceso en producción cuando llega uno de cien mil, y el fallo no es un resultado incorrecto sino la muerte del proceso —en Java un `StackOverflowError`, en Python un `RecursionError`, en C un segfault sin diagnóstico. Por eso los recorridos que procesan datos de tamaño no acotado (documentos subidos por usuarios, grafos de dependencias) suelen convertirse a iterativos con pila explícita antes de llegar a producción. La segunda cara es el coste temporal: la recursión ingenua de Fibonacci recalcula los mismos subproblemas una y otra vez y su número de llamadas crece como O(2^n), de modo que lo que responde en un milisegundo con n=30 tarda minutos con n=45. Memoizar —recordar cada F(k) ya calculado— la reduce a O(n) sin cambiar la forma del código. Reconocer cuándo un algoritmo recursivo repite trabajo es la diferencia entre una función correcta y una función utilizable.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 30)
- **Salida** (stdout): `fib=<F(n)>`
- **Regla:** F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `fib=55` |
| `1` | `fib=1` |
| `0` | `fib=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION fib(n): SI n<2 DEVOLVER n ; SINO DEVOLVER fib(n-1)+fib(n-2)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


n = int(sys.stdin.readline())
print(f"fib={fib(n)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function fib(n: number): number {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static long fib(int n) {
        return n < 2 ? n : fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("fib=" + fib(n));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"fib={Fib(n)}");
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

func fib(n int) int64 {
	if n < 2 {
		return int64(n)
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	fmt.Printf("fib=%d\n", fib(n))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn fib(n: i64) -> i64 {
    if n < 2 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("fib={}", fib(n));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long fib(long n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("fib=%ld\n", fib(n));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: Fibonacci con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE fib(i, a, b) AS (
    VALUES (0, 0, 1)
    UNION ALL SELECT i + 1, b, a + b FROM fib WHERE i < 10
)
SELECT printf('fib=%d', a) AS resultado FROM fib WHERE i = 10;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function fib($n) {
    return $n < 2 ? $n : fib($n - 1) + fib($n - 2);
}

$n = (int) trim(fgets(STDIN));
echo "fib=" . fib($n) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `10` de `casos.json`, cuya salida esperada es `fib=55`. En **Python**, `n = int(sys.stdin.readline())` fija `n = 10` y la última línea evalúa `fib(n)` dentro del f-string. Al entrar en `fib(10)`, la expresión `n if n < 2 else fib(n - 1) + fib(n - 2)` comprueba `10 < 2`, que es falso, así que debe evaluar `fib(9) + fib(8)`. Python evalúa primero el operando izquierdo: apila una llamada a `fib(9)`, que a su vez apila `fib(8)`, que apila `fib(7)`… la cadena baja hasta `fib(1)`, donde `1 < 2` es verdadero y la función devuelve `1` sin volver a llamarse —ese es el caso base—, y hasta `fib(0)`, que devuelve `0`. En el punto más profundo hay once marcos de pila vivos simultáneamente (de `fib(10)` a `fib(0)`), cada uno con su propio valor de `n`. Al desapilarse, las sumas se resuelven de abajo arriba: `fib(2)` devuelve `1+0=1`, `fib(3)` devuelve `1+1=2`, `fib(4)` da `3`, y así hasta `fib(10) = 34 + 21 = 55`. Se imprime `fib=55`. Fíjate en el detalle que da nombre al problema: `fib(8)` se calcula entero dos veces —una dentro de `fib(10)` y otra dentro de `fib(9)`—, y ese solapamiento repetido en cada nivel es la raíz del coste exponencial.

En **C** el recorrido es el mismo, pero la máquina queda a la vista. `scanf("%ld", &n)` lee `10` en un `long`, y `fib(n)` entra en `return n < 2 ? n : fib(n - 1) + fib(n - 2);`. Cada llamada anidada empuja un marco en la pila del proceso: la dirección de retorno (a qué instrucción volver cuando esta llamada termine), el parámetro `n` y el espacio de trabajo local. Con `n=10` la profundidad máxima es 10 y el consumo es despreciable, pero aquí no hay red de seguridad: si la entrada fuera enorme, C no lanzaría una excepción como Python o Java sino que escribiría más allá del límite de la pila y el sistema mataría el proceso con una violación de segmento. El resultado se acumula en `long` y `printf("fib=%ld\n", ...)` imprime `fib=55`. Un compilador con `-O2` puede aplanar parte de estas llamadas, pero ninguna de las dos ramas de `fib(n-1) + fib(n-2)` está en posición de cola —hay que sumar los dos resultados después de que ambas vuelvan—, así que la recursión de cola no aplica aquí.

El contraste lo da **SQL**, que resuelve el mismo `fib=55` sin apilar nada. El CTE `WITH RECURSIVE fib(i, a, b)` arranca con la fila `(0, 0, 1)` y en cada paso produce `(i + 1, b, a + b)` mientras `i < 10`: es decir, mantiene dos acumuladores que avanzan la pareja de Fibonacci hacia adelante en lugar de descomponer el problema hacia atrás. Las filas generadas son `(0,0,1)`, `(1,1,1)`, `(2,1,2)`, `(3,2,3)`, `(4,3,5)`, hasta `(10,55,89)`, y el `SELECT` final filtra `WHERE i = 10` para leer `a = 55`. Esta es exactamente la forma **acumuladora** que convierte una recursión no-de-cola en una de cola: en vez de esperar el resultado de la llamada para operar con él, se lleva el resultado parcial en los parámetros. Por eso el coste pasa de O(2^n) llamadas a n pasos, y por eso la semántica de punto fijo del `WITH RECURSIVE` —repetir la regla hasta que no se generen filas nuevas— puede ejecutarse en memoria acotada. Rust y Go, en el mismo README, siguen la estructura ingenua de Python y C: la suma tras las dos llamadas impide la posición de cola, y ninguno de los dos garantizaría la optimización aunque la hubiera.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def fib` (Python), `func fib` (Go), `fn fib` (Rust) — todas se auto-invocan igual. |
| Semántica | La pila de llamadas crece con la profundidad; ojo con el desbordamiento en recursiones profundas. |
| Paradigmática | SQL expresa la recursión con un CTE recursivo, no con funciones. |

La diferencia que de verdad separa a los diez lenguajes del núcleo no es cómo se escribe una función recursiva —en eso son casi idénticos— sino qué garantías dan sobre la pila. Un primer grupo impone un límite artificial y falla con diagnóstico: **Python** corta en 1000 niveles por defecto (ajustable con `sys.setrecursionlimit`, a riesgo de reventar la pila real) y lanza `RecursionError`; **Java** y **C#** dejan que se agote la pila del hilo (del orden de 1 MB) y lanzan `StackOverflowError` o `StackOverflowException` —en .NET, además, esa excepción no es capturable y termina el proceso—. Un segundo grupo depende del motor: **JavaScript** y **TypeScript** comparten el límite del intérprete (`RangeError: Maximum call stack size exceeded`), y aunque ES2015 especificó la optimización de llamadas de cola, en la práctica sólo Safari la implementó, de modo que en Node no puedes contar con ella. **PHP** no tiene límite propio y simplemente agota la pila del proceso. Un tercer grupo se acerca al metal: **C** desborda sin aviso y produce un segfault, y **Rust** hace lo mismo salvo por la *stack guard page* que le permite abortar con un mensaje explícito; ambos pueden recibir la optimización de cola del compilador (LLVM, `-O2`) pero ninguno de los dos estándares la promete. **Go** es el único que rompe el molde por otra vía: sus goroutines arrancan con una pila diminuta de unos pocos kilobytes que *crece dinámicamente* copiándose a un bloque mayor, lo que le permite recursiones muy profundas sin reservar memoria por adelantado, aunque tampoco garantiza la optimización de cola. Y **SQL**, fiel a su naturaleza declarativa, no tiene pila de llamadas en absoluto: el `WITH RECURSIVE` es una iteración de punto fijo sobre un conjunto de filas, con su propio límite en la memoria del motor.

## 🧬 El concepto en la familia

En la familia de C —C, C++, Java, JavaScript, C#, PHP— la recursión existe como consecuencia natural del modelo de pila de llamadas, pero ninguna la privilegia: el estilo idiomático es iterar, y la recursión se reserva para estructuras arborescentes. La familia del scripting dinámico repite ese patrón con un matiz de seguridad: Python y Ruby imponen un límite explícito de profundidad para fallar con un error legible antes de corromper el proceso, y Python además rechaza la optimización de cola por decisión de diseño, para no perder las trazas de pila. Donde el concepto cambia de estatuto es en la familia ML y funcional: en Scheme la recursión de cola no es una optimización opcional sino un requisito del estándar (R5RS y R7RS), lo que convierte la recursión en la única construcción de bucle necesaria; Haskell y Erlang hacen lo propio, y en Erlang los bucles infinitos de los procesos servidores son literalmente funciones que se llaman a sí mismas en posición de cola para siempre. Go y Rust se quedan en un terreno intermedio pragmático: ambos permiten la recursión sin restricciones artificiales, Go la sostiene con pilas que crecen dinámicamente y Rust con un modelo de propiedad que hace predecible el coste de cada marco, pero ninguno de los dos la garantiza como mecanismo de iteración y ambos empujan al bucle. Los declarativos, finalmente, la reformulan por completo: SQL con `WITH RECURSIVE` y Prolog con sus cláusulas describen una relación recursiva y dejan que el motor calcule el punto fijo, sin que el programador vea nunca una pila.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 069
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar el caso base** → causa: sin una condición que devuelva sin volver a llamarse, cada invocación apila un marco nuevo hasta agotar la pila; el síntoma es `RecursionError` en Python, `StackOverflowError` en Java o un segfault seco en C → solución: escribir el caso base *antes* que el recursivo y comprobarlo con la entrada mínima (aquí, que `n=0` dé `fib=0` y `n=1` dé `fib=1` sin entrar en la rama recursiva).
- **Un caso recursivo que no reduce** → causa: llamar a `fib(n)` en vez de `fib(n - 1)`, o restar sobre una variable equivocada, deja el argumento igual y el caso base nunca se alcanza aunque exista → solución: identificar la magnitud que decrece en cada llamada (aquí `n`) y verificar que toda rama recursiva la disminuye estrictamente.
- **Creer que la recursión de cola siempre se optimiza** → causa: escribir una recursión de cola de cientos de miles de niveles suponiendo que el lenguaje reutilizará el marco; funciona en Scheme, Erlang o Haskell, pero Python la rechaza por diseño, la JVM no la soporta en bytecode y Go, Rust, JavaScript en Node o C sin `-O2` tampoco la prometen → solución: si el lenguaje no la garantiza, convertir a bucle explícito antes de que la profundidad dependa de datos de entrada.
- **Recursión ingenua sobre subproblemas solapados** → causa: `fib(n-1) + fib(n-2)` recalcula el mismo `fib(k)` una y otra vez y el número de llamadas crece como O(2^n); con n=45 son miles de millones de invocaciones → solución: memoizar (una tabla o `functools.lru_cache` en Python) para bajar a O(n), o reescribir con dos acumuladores como hace la versión SQL de esta clase.
- **Subir el límite de recursión en vez de arreglar el algoritmo** → causa: llamar a `sys.setrecursionlimit(100000)` mueve el guardián de Python pero no agranda la pila real del sistema operativo, así que el fallo pasa de una excepción limpia a un volcado del intérprete → solución: tratar el límite como un aviso de diseño y convertir el recorrido a iterativo con pila explícita.

## ❓ Preguntas frecuentes

- **¿La recursión es peor que el bucle?** No intrínsecamente: son equivalentes en poder expresivo, y todo programa recursivo tiene un equivalente iterativo con una pila explícita. La diferencia es de coste y de legibilidad. La recursión paga O(profundidad) en memoria de pila, pero para estructuras arborescentes produce código mucho más claro; en cambio, para recorridos lineales el bucle suele ser más simple y no arriesga el desbordamiento.
- **¿Qué es exactamente la recursión de cola?** Es cuando la llamada recursiva es la *última* operación de la función: no queda nada por hacer con su resultado más que devolverlo. En ese caso el marco actual ya no contiene información útil y puede reutilizarse, ejecutando la recursión en espacio constante. `return fib(n-1) + fib(n-2)` **no** es recursión de cola, porque tras las llamadas todavía hay que sumar; `return aux(n-1, a+b, a)` sí lo es.
- **¿Cómo convierto una recursión normal en una de cola?** Añadiendo *acumuladores*: parámetros que llevan el resultado parcial hacia adelante en lugar de esperarlo de vuelta. Para Fibonacci, una función auxiliar `aux(k, a, b)` que devuelve `a` cuando `k` llega a cero y se llama a sí misma con `aux(k-1, b, a+b)` en otro caso. Ese es precisamente el patrón que aplica el CTE recursivo de la implementación SQL de esta clase.
- **¿Por qué Python no optimiza las llamadas de cola?** Es una decisión deliberada, no una carencia técnica. Guido van Rossum argumentó que eliminar los marcos intermedios destruye la traza de pila y con ella la capacidad de depurar, y que la recursión de cola disfraza de recursión lo que en Python debería escribirse como un bucle. La consecuencia práctica es que en Python el límite de 1000 niveles es real y hay que respetarlo.
- **¿Cuánta profundidad aguanta realmente mi programa?** Depende del tamaño de la pila del hilo y del tamaño de cada marco. Un hilo típico de la JVM o de un proceso Windows dispone de alrededor de 1 MB; en Linux el hilo principal suele tener 8 MB por defecto (`ulimit -s`). Si cada marco ocupa unas decenas de bytes, eso permite decenas o cientos de miles de niveles en C; en lenguajes con marcos más pesados, bastante menos. Go es la excepción: sus goroutines empiezan con pilas de pocos kilobytes que crecen copiándose.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press). Su tratamiento de la corrección por inducción es el marco natural para razonar sobre una función recursiva: el caso base es la base de la inducción y el caso recursivo, el paso inductivo.
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo y subprogramas, donde se describe el registro de activación y por qué la recursión sale gratis del mecanismo de llamada; también compara qué lenguajes garantizan la optimización de llamadas de cola.

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

> [⏮️ Clase 068](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 070 ⏭️](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md)
