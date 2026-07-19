# Clase 042 — Declaración, asignación e inicialización

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Hay tres actos que el lenguaje cotidiano funde en la palabra "variable" y que un buen programador debe saber separar: **declarar** es introducir un nombre en un ámbito; **inicializar** es darle su primer valor; **asignar** es cambiarlo después. Confundirlos es la raíz de errores clásicos —usar una variable declarada pero no inicializada, o creer que reasignar y declarar de nuevo son lo mismo—. Sebesta dedica páginas a esta anatomía porque de ella dependen el ámbito (dónde vive el nombre), el tiempo de vida (cuánto dura) y la seguridad (si el compilador te protege de leer basura).

El intercambio de dos variables es el ejercicio mínimo que activa los tres actos a la vez y, de paso, revela una diferencia de diseño profunda. Para intercambiar `a` y `b` sin perder ningún valor hay que resolver un problema de orden: si escribes `a = b` primero, el valor original de `a` se pierde antes de poder copiarlo a `b`. La solución tradicional —una **variable temporal**— hace explícito ese "guarda antes de pisar". Pero varios lenguajes ofrecen **asignación múltiple** (`a, b = b, a`), que evalúa *todo* el lado derecho antes de asignar nada, eliminando la necesidad de la temporal. Ese detalle —cuándo se evalúa el lado derecho respecto al izquierdo— es exactamente la semántica de la asignación que Scott formaliza con los conceptos de l-value y r-value.

Comparar cómo cada familia intercambia dos valores enseña, entonces, algo más que sintaxis: enseña si el lenguaje considera la asignación un acto atómico sobre una tupla (Python, Go, Rust, JS, C#, PHP) o una secuencia de pasos manuales sobre celdas de memoria (C, Java), y cómo eso cambia qué errores son posibles.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar declaración, inicialización y (re)asignación.
2. Intercambiar dos variables con y sin temporal según el lenguaje.
3. Reconocer la asignación múltiple (desestructuración) donde existe.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarar vs. inicializar | Introducir un nombre no es lo mismo que darle valor |
| 2 | Reasignación | Cambiar el valor de una variable ya inicializada |
| 3 | Variable temporal | El patrón clásico para intercambiar |
| 4 | Asignación múltiple | a, b = b, a donde el lenguaje lo permite |

## 📖 Definiciones y características

- **Declaración** — introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usarla sin inicializar es un error clásico.
- **Asignación** — cambiar el valor de una variable existente. Clave: solo posible si es mutable.
- **Asignación múltiple** — asignar varias variables a la vez (a, b = b, a). Clave: evita la temporal en Python, JS, Go, Rust.

La distinción entre declaración e inicialización no es un tecnicismo pedante: en los lenguajes estáticos decide qué comprueba el compilador. En C puedes escribir `long tmp;` (declaración pura, sin valor) y la variable existe pero contiene bits indeterminados; leerla antes de asignarle algo es *comportamiento indefinido*. Java cierra ese hueco para variables locales: el compilador rechaza el programa si detecta que una variable local podría leerse sin haber sido inicializada. Python y PHP ni siquiera separan los pasos: no hay "declarar sin valor"; el nombre nace en el momento en que recibe su primer objeto. Esta gradación —de C, que permite el hueco, a Python, que lo hace imposible— es una de las lecciones que Sebesta agrupa bajo "inicialización de variables".

La **asignación** propiamente dicha solo tiene sentido si la variable es mutable, y su semántica esconde una sutileza que la asignación múltiple pone a prueba: ¿en qué orden se evalúan los dos lados? La regla que comparten Python, Go, Rust, JS, C# y PHP es que el lado derecho se evalúa *entero* antes de tocar el izquierdo. Por eso `a, b = b, a` funciona: primero se construye la pareja de valores `(b, a)` con los datos originales y solo después se reparte sobre los nombres. La variable temporal de C y Java hace ese mismo "congelar el estado antes de modificarlo", pero a mano, un paso a la vez.

## 🧩 Situación

Intercambiar dos valores parece trivial, pero es precisamente su trivialidad lo que lo hace un buen instrumento: como el problema no distrae, deja ver con nitidez la maquinaria del lenguaje. Aquí se aprecia si ofrece asignación múltiple idiomática (Python, Go, Rust, JS, C#, PHP) o exige la variable temporal de toda la vida (C, Java), y con los casos del contrato —incluyendo `-2 9` con un negativo— se confirma que el intercambio conserva el signo y no depende de los valores concretos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `a=<nuevo a> b=<nuevo b>` tras intercambiar
- **Regla:** intercambiar a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `a=7 b=3` |
| `0 5` | `a=5 b=0` |
| `-2 9` | `a=9 b=-2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
tmp <- a ; a <- b ; b <- tmp   (o bien: a, b <- b, a)
ESCRIBIR "a=" a " b=" b
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

# Declaración e inicialización a partir de la entrada.
a, b = sys.stdin.readline().split()
a, b = int(a), int(b)

# Asignación múltiple: intercambio sin variable temporal.
a, b = b, a

print(f"a={a} b={b}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

let [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

// Desestructuración: intercambio en una sola línea.
[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

let [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
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
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);

        // Java no tiene asignación múltiple: variable temporal.
        int tmp = a;
        a = b;
        b = tmp;

        System.out.println("a=" + a + " b=" + b);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);

// C# sí ofrece asignación por tuplas.
(a, b) = (b, a);

Console.WriteLine($"a={a} b={b}");
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
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])

	// Go permite intercambio con asignación múltiple.
	a, b = b, a

	fmt.Printf("a=%d b=%d\n", a, b)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();

    // Intercambio por desestructuración de tupla.
    let (a, b) = (v[1], v[0]);

    println!("a={a} b={b}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;

    /* C exige una variable temporal para intercambiar. */
    long tmp = a;
    a = b;
    b = tmp;

    printf("a=%ld b=%ld\n", a, b);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no reasigna variables: se describe la salida intercambiando columnas.
WITH pares(a, b) AS (VALUES (3, 7), (0, 5), (-2, 9))
SELECT printf('a=%d b=%d', b, a) AS resultado
FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;

// PHP admite intercambio por lista.
[$a, $b] = [$b, $a];

printf("a=%d b=%d\n", $a, $b);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Tomemos el caso `3 7` de [`casos.json`](casos.json), cuya salida esperada es `a=7 b=3`. El interés está en *cómo* cada lenguaje evita perder un valor durante el intercambio.

En **Python**, `a, b = sys.stdin.readline().split()` declara e inicializa dos nombres de golpe con las cadenas `"3"` y `"7"`; la línea siguiente, `a, b = int(a), int(b)`, los reasigna a los enteros `3` y `7` —nótese que reasignar no es redeclarar: son los mismos nombres apuntando ahora a otros objetos—. El corazón es `a, b = b, a`. Python evalúa primero el lado derecho completo, construyendo la tupla `(7, 3)` con los valores actuales, y solo entonces la desempaqueta sobre `a` y `b`. Nunca hay un instante en que un valor se haya perdido, y por eso no hace falta temporal. El `print(f"a={a} b={b}")` emite `a=7 b=3`.

En **C** se ve el mecanismo desnudo. `long a, b;` declara las cajas sin valor; `scanf("%ld %ld", &a, &b)` las llena pasando sus *direcciones* (`&a`, `&b`), porque C necesita saber dónde escribir. El intercambio es el patrón de tres pasos: `long tmp = a;` guarda el `3` original antes de pisarlo, `a = b;` mete el `7` en `a`, y `b = tmp;` recupera el `3` guardado y lo pone en `b`. Si se omitiera la temporal y se hiciera `a = b; b = a;`, tras la primera línea `a` ya valdría `7` y la segunda copiaría `7` de vuelta: el `3` se habría perdido y saldría `a=7 b=7`. La temporal *es* la memoria de corto plazo que la asignación múltiple de Python hace de forma implícita. `printf("a=%ld b=%ld\n", a, b)` produce `a=7 b=3`.

**Rust** ofrece un tercer matiz. Lee todos los números en un `Vec<i64>` llamado `v`, de modo que `v[0]` es `3` y `v[1]` es `7`. En lugar de mutar, el autor *crea nuevos enlaces ya intercambiados*: `let (a, b) = (v[1], v[0]);` liga `a` a `7` y `b` a `3` en una sola desestructuración de tupla, sin necesidad de `mut` porque nada se reasigna. Es la filosofía de inmutabilidad de Rust aplicada al swap: no se cambia el valor de una variable existente, se define una nueva pareja. `println!("a={a} b={b}")` imprime `a=7 b=3`. Java, en contraste con los tres, no tiene tuplas en el núcleo del lenguaje y recurre a la misma temporal que C (`int tmp = a; a = b; b = tmp;`), dejando claro que la ausencia de asignación múltiple es una decisión de diseño, no una limitación técnica.

## 🔬 Comparación

Bajo la superficie, el intercambio distingue dos modelos de asignación. En uno, asignar es un acto *atómico* sobre una tupla: el lado derecho se congela entero antes de escribir el izquierdo. En el otro, asignar es una *secuencia* de escrituras a celdas de memoria, y el programador debe orquestar el orden con una temporal. El primero elimina por construcción el bug de "pisar antes de guardar"; el segundo lo deja en manos de quien escribe.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a, b = b, a` (Python/Go/Rust) y `(a, b) = (b, a)` (C#) vs. `tmp=a; a=b; b=tmp;` (C/Java). |
| Semántica | La asignación múltiple evalúa el lado derecho completo antes de asignar (atómica); la temporal secuencia las escrituras a mano. |
| Declaración vs. inicialización | C permite declarar sin inicializar (`long tmp;`); Java lo prohíbe para locales; Python/PHP no separan los pasos. |
| Inmutabilidad | Rust intercambia creando un enlace nuevo `let (a, b) = (v[1], v[0])` sin `mut`; C/Java mutan variables existentes. |
| Paradigmática | SQL no reasigna variables: describe la salida intercambiando las columnas en el `SELECT`. |

## 🧬 El concepto en la familia

- **Scripting dinámico** (Ruby): `a, b = b, a`, idéntico a Python, con la misma semántica de evaluar el lado derecho antes de asignar.
- **JVM** (Kotlin): al carecer de asignación múltiple directa se usa `a = b.also { b = a }` (el bloque `also` captura el valor antiguo) o, más claro, una temporal —el mismo camino que Java.
- **Funcional** (Haskell): no hay reasignación en absoluto; "intercambiar" se modela definiendo un nuevo par `let (x, y) = (b, a)` o pasando los argumentos en otro orden a una función. El swap es conceptual, no una mutación.
- **C/llaves** (C++): además de la temporal clásica ofrece `std::swap(a, b)` en la biblioteca estándar, que encapsula el patrón de tres pasos de forma segura y reutilizable.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 042
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder un valor al intercambiar sin temporal** → causa: hacer `a = b; b = a;` pisa `a` antes de guardarlo, y el segundo paso copia el valor ya sobreescrito → solución: usar una temporal o la asignación múltiple del lenguaje, que congela el lado derecho antes de asignar.
- **Usar una variable sin inicializar** → causa: declararla y leerla sin darle valor; en C son bits basura, comportamiento indefinido → solución: inicializar en la declaración; en Java el compilador ya te obliga para variables locales.
- **Creer que reasignar es redeclarar** → causa: en Python `a = int(a)` no crea una variable nueva, reenlaza el mismo nombre a otro objeto → solución: entender que declarar introduce el nombre una vez y asignar cambia a qué apunta.
- **Redeclarar en un lenguaje estático** → causa: escribir `int a` dos veces en el mismo ámbito en C/Java es un error de compilación → solución: declarar una vez y reasignar con `a = ...` sin el tipo.

## ❓ Preguntas frecuentes

- **¿La asignación múltiple es más lenta?** No de forma apreciable; el compilador o intérprete la traduce a algo equivalente a la temporal. Se prefiere por ser más legible y por eliminar de raíz el error de orden.
- **¿Por qué C no la tiene?** Es un lenguaje minimalista y cercano a la máquina, donde una asignación es una escritura a memoria; el patrón con temporal es explícito y suficiente. La comodidad de las tuplas llegó a lenguajes posteriores.
- **¿`a, b = b, a` crea una tupla de verdad?** En Python sí: se construye el objeto tupla `(b, a)` y luego se desempaqueta. Compiladores como los de Go o Rust suelen optimizar el caso y no materializan la tupla, pero la *semántica* observable es la misma.
- **¿Declarar reserva memoria?** En lenguajes estáticos la declaración fija el tipo y el tamaño de la celda; la inicialización pone el valor. En dinámicos no hay celda tipada previa: el nombre aparece ya apuntando a un objeto.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. de variables (declaración, inicialización, ámbito y tiempo de vida).
- B. C. Pierce — *Types and Programming Languages* (MIT Press), introducción (seguridad de tipos: el compilador descarta programas mal formados).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. de asignación, l-value/r-value y orden de evaluación.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre nombres, referencias y desempaquetado de tuplas.
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

> [⏮️ Clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 043 ⏭️](../../parte-3-valores-tipos-y-variables/043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md)
