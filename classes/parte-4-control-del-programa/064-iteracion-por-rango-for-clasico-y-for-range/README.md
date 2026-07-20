# Clase 064 — Iteración por rango: for clásico y for-range

> Parte **4 — Control del programa** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

El bucle `for` existe para el caso más común de todos: cuando sabes de antemano cuántas veces vas a repetir, o sobre qué rango vas a iterar. Frente al `while`, que te obliga a orquestar a mano la inicialización, la condición y el avance, el `for` reúne esas tres piezas en un solo lugar visible, y con ello reduce la superficie donde puede colarse un error de límite. Esa concentración es su virtud: quien lee un `for` sabe de un vistazo por dónde empieza el contador, cuándo para y cómo avanza.

En esta clase calculamos el factorial —n! = 1·2·…·n— porque es el ejemplo canónico donde el `for` brilla: el número de vueltas es exactamente `n`, conocido antes de empezar. La tarea revela además dos formas distintas de expresar el mismo bucle: el `for` *clásico* de tres partes heredado de C (`for (i=1; i<=n; i++)`), donde tú gestionas el índice, y el `for`-*range* moderno (`for i in 1..=n`, `for i in range(1, n+1)`), donde declaras el rango y el lenguaje se encarga del índice, eliminando de raíz los errores de contorno. El porqué de fondo es que iterar un número conocido de veces es tan frecuente que cada lenguaje ha buscado la forma más segura y legible de expresarlo, y comparar esas formas ilumina las prioridades de diseño de cada uno.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle for con contador.
2. Acumular un producto.
3. Reconocer el for-range frente al for clásico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for clásico | init; condición; incremento |
| 2 | for-range | Recorrer un rango directamente |
| 3 | Acumular un producto | Multiplicar en cada vuelta |
| 4 | Caso base 0! = 1 | El bucle no se ejecuta y queda 1 |

## 📖 Definiciones y características

- **for** — bucle con inicialización, condición e incremento. Clave: para un número conocido de vueltas.
- **for-range** — recorrer un rango o colección sin gestionar el índice (Python, Rust, Go). Clave: menos errores.
- **Factorial** — n! = 1·2·…·n. Clave: 0! = 1 por definición.
- **Acumulador de producto** — variable que empieza en 1 y se multiplica. Clave: 1 es el neutro del producto.

Sebesta, en el capítulo de estructuras de control de *Concepts of Programming Languages*, clasifica el `for` entre los *bucles controlados por contador*, y narra su evolución histórica: del `for` rígido de Fortran (con límites y paso fijados de antemano) al `for` flexible de C, cuyas tres cláusulas son en realidad expresiones arbitrarias, tanto que un `for` de C es apenas azúcar sintáctico sobre un `while`. Esa flexibilidad tuvo un precio: al dejar el índice enteramente en manos del programador, el `for` clásico de C es un imán para los errores *off-by-one* (usar `<` donde iba `<=`, empezar en `0` en vez de `1`). Los lenguajes posteriores reaccionaron con el `for`-range: en lugar de escribir las tres cláusulas, declaras el rango (`1..=n` en Rust, `range(1, n+1)` en Python) y el lenguaje genera el índice correcto, cerrando esa fuente de errores.

Ese giro conecta con el espíritu de *Structured Programming*: Dahl, Dijkstra y Hoare abogaban por construcciones cuya corrección sea evidente a la vista, sin necesidad de simular la ejecución en la cabeza. Un `for i in 1..=n` dice literalmente "para cada i de 1 a n inclusive", y no hay margen para equivocar el límite; un `for (i=1; i<=n; i++)` exige releer las tres cláusulas y comprobar que encajan. Es también notable que Rust *no* tenga el `for` clásico de tres partes estilo C: solo ofrece la iteración sobre rangos e iteradores, una decisión de diseño deliberada para forzar la forma más segura. En esta clase, el caso base `0! = 1` sale gratis precisamente por cómo está definido el rango: con `n=0`, el rango `1..=0` está vacío, el bucle no se ejecuta y el acumulador conserva su valor inicial `1`, que es el neutro del producto.

## 🧩 Situación

El factorial aparece por todas partes en combinatoria y probabilidad: cuenta de cuántas formas se pueden ordenar n elementos y es el cimiento de las permutaciones y los coeficientes binomiales. Pero como problema de programación es el arquetipo perfecto del `for` por contador: hay que multiplicar exactamente los enteros de 1 a n, un número de vueltas conocido antes de empezar, y acumular el producto. Ningún otro tipo de bucle expresa esa intención con más claridad.

Dos detalles de ingeniería lo hacen jugoso. El primero es el caso base: `0! = 1` no necesita un `if` especial, sale gratis porque con `n=0` el rango de 1 a 0 está vacío, el bucle no se ejecuta y el acumulador queda en su valor inicial `1`. Esto ilustra una virtud del diseño: cuando el neutro se elige bien, los casos límite se resuelven solos. El segundo es el desbordamiento: el factorial crece explosivamente. `20!` todavía cabe en un entero de 64 bits, pero `21!` ya lo desborda, y por eso el contrato de la clase limita `n` a 20 y las implementaciones usan tipos de 64 bits (`long`, `int64`, `i64`). El porqué de fondo es que un bucle correcto no basta si el tipo del acumulador no puede contener el resultado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 20)
- **Salida** (stdout): `factorial=<n!>`
- **Regla:** n! = 1·2·…·n ; 0! = 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `factorial=120` |
| `1` | `factorial=1` |
| `0` | `factorial=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
f <- 1
PARA i de 1 a n: f <- f*i
ESCRIBIR "factorial=" f
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
f = 1
for i in range(1, n + 1):
    f *= i
print(f"factorial={f}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long f = 1;
        for (int i = 1; i <= n; i++) {
            f *= i;
        }
        System.out.println("factorial=" + f);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long f = 1;
for (int i = 1; i <= n; i++) {
    f *= i;
}
Console.WriteLine($"factorial={f}");
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

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.Atoi(strings.TrimSpace(line))
	var f int64 = 1
	for i := 1; i <= n; i++ {
		f *= int64(i)
	}
	fmt.Printf("factorial=%d\n", f)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut f: i64 = 1;
    for i in 1..=n {
        f *= i;
    }
    println!("factorial={f}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long f = 1;
    for (long i = 1; i <= n; i++) {
        f *= i;
    }
    printf("factorial=%ld\n", f);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: factorial con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE fact(i, f) AS (
    VALUES (1, 1)
    UNION ALL SELECT i + 1, f * (i + 1) FROM fact WHERE i < 5
)
SELECT printf('factorial=%d', f) AS resultado FROM fact ORDER BY i DESC LIMIT 1;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$f = 1;
for ($i = 1; $i <= $n; $i++) {
    $f *= $i;
}
echo "factorial=$f\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido del código: de la entrada a la salida

Sigamos el caso `5` de `casos.json`, cuya salida esperada es `factorial=120`. En **Python**, `n = int(sys.stdin.readline())` fija `n = 5`, y `f = 1` inicializa el acumulador con el neutro del producto. El bucle es `for i in range(1, n + 1):`, es decir `range(1, 6)`, que produce la secuencia `1, 2, 3, 4, 5` —observa el `n + 1`, necesario porque `range` excluye su límite superior. En cada vuelta `f *= i`: parte de `1`, pasa a `1·1=1`, luego `1·2=2`, `2·3=6`, `6·4=24` y `24·5=120`. Al agotarse el rango, imprime `factorial=120`. Con el caso `0`, `range(1, 1)` está vacío, el cuerpo no se ejecuta y `f` conserva su `1` inicial: así `0! = 1` sale sin ningún caso especial.

El contraste más nítido es **C**, con el `for` clásico de tres partes: `for (long i = 1; i <= n; i++)`. Aquí las tres piezas están a la vista y bajo tu control: `i = 1` inicializa, `i <= n` es la condición (nota el `<=`, que sí incluye a `n`, a diferencia del `range` de Python), e `i++` avanza. Con `n=5` recorre `i = 1, 2, 3, 4, 5` y multiplica `f` hasta `120`. El precio de ese control es la responsabilidad: escribir `i < n` en vez de `i <= n` daría `24` en lugar de `120`, un clásico error *off-by-one* que el lenguaje no puede detectar por ti. El tipo `long` de `f` anticipa el crecimiento del factorial.

El tercer enfoque, **Rust**, encarna el `for`-range en su forma más pura: `for i in 1..=n`. El operador `..=` denota un rango *inclusivo*, así que `1..=5` recorre `1, 2, 3, 4, 5` sin necesidad de sumar uno ni de escribir una condición. No hay `i++` ni comparación a la vista: declaras el rango y Rust genera el índice correcto, cerrando la puerta al error de contorno. Con `n=0`, `1..=0` es un rango vacío y `f` queda en `1`. Las tres rutas convierten el `5` de entrada en `factorial=120`, pero van del máximo control manual (C) al máximo cuidado del lenguaje (Rust), con Python en un término medio expresivo.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `for i in range(1,n+1)` (Python) vs. `for(i=1;i<=n;i++)` (C/Java) vs. `for i in 1..=n` (Rust). |
| Semántica | El for-range evita el error de límites; el for clásico lo deja en tus manos. |
| Paradigmática | SQL usa un CTE recursivo o una agregación, no un for. |

La divisoria más real entre los diez lenguajes es cuál forma de `for` ofrecen. **C**, **Java**, **C#**, **JavaScript** y **TypeScript** usan el `for` clásico de tres partes (`for (i=1; i<=n; i++)`), donde tú gestionas el índice y cargas con el riesgo de contorno. **Go** también tiene esa forma —`for i := 1; i <= n; i++`—, aunque su `for` es el único bucle del lenguaje. En el otro extremo, **Rust** *no ofrece* el `for` de tres partes: obliga a iterar sobre rangos (`1..=n`) o iteradores, cerrando por diseño la puerta al *off-by-one*. **Python** usa `range(1, n+1)`, un `for`-range con límite superior *exclusivo* (de ahí el `+1`). Un detalle fácil de olvidar es que el rango de Python es semiabierto mientras que el `..=` de Rust es inclusivo: el mismo factorial exige `n+1` en uno y `n` en el otro. **SQL**, sin bucles, expresa el factorial con un CTE recursivo o una agregación. La misma iteración por contador, por tanto, oscila entre "hazlo todo tú" y "declara el rango y confía en el lenguaje".

## 🧬 El concepto en la familia

En la familia de C —C, Java, C#, JavaScript, Go— reina el `for` clásico de tres cláusulas, expresivo y peligroso a partes iguales. La familia de lenguajes de más alto nivel se decantó por el `for`-range: Python (`range`), Ruby (`(1..n)`), Kotlin (`for (i in 1..n)`) y Swift iteran sobre rangos y colecciones sin índice explícito. Rust lleva esa preferencia hasta su conclusión eliminando el `for` clásico por completo. Y la familia funcional prescinde a veces del bucle: en Ruby, `(1..n).reduce(1, :*)` expresa el factorial como un plegado sobre el rango, sin contador ni acumulador visibles. Bajo todas esas formas late la misma idea —recorrer un número conocido de valores—, y la tendencia histórica va del control manual hacia construcciones que declaran el rango y hacen imposible el error de límite.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 064
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Empezar el acumulador en 0** → causa: el producto siempre da 0 → solución: iniciar el acumulador de producto en 1
- **Límites del rango mal** → causa: un factor de más o de menos → solución: verificar con 0! y 1! que el rango es correcto

## ❓ Preguntas frecuentes

- **¿Por qué long y no int?** El factorial crece muy rápido; 21! ya desborda 64 bits. Aquí n<=20.
- **¿0! por qué es 1?** Es el producto vacío: el neutro de la multiplicación es 1.

## 🔗 Referencias

**Libros de la parte:**

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

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

> [⏮️ Clase 063](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 065 ⏭️](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md)
