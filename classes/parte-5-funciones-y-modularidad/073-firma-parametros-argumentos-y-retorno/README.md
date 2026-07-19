# Clase 073 — Firma, parámetros, argumentos y retorno

> Parte **5 — Funciones y modularidad** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender la función como la primera y más importante herramienta de abstracción que ofrece cualquier lenguaje: un mecanismo para dar **nombre** a un proceso y, con ese nombre, olvidarnos de cómo está hecho por dentro. En esta clase disecamos las cuatro piezas que componen esa herramienta —la **firma** (el nombre más los parámetros más el tipo de retorno), los **parámetros** (los huecos declarados), los **argumentos** (los valores reales que se pasan) y el **retorno** (el valor que sale)— y las vemos funcionar idénticas en diez lenguajes que las escriben de formas muy distintas.

El objetivo profundo no es sintáctico. Abelson y Sussman abren *Structure and Interpretation of Computer Programs* con una idea que sostiene toda la clase: una definición de procedimiento asocia un nombre compuesto a una operación compuesta, y esa asociación nos permite razonar sobre el «qué» sin arrastrar el «cómo». Cuando escribes `suma(a, b)` en cualquier parte del programa, tu mente ya no piensa en `a + b`: piensa en «sumar». Ese salto —de la operación a la intención nombrada— es el que multiplica lo que un programador puede construir. Todo lo demás de la Parte 5 (parámetros por defecto, variádicos, genéricos, cierres, módulos) son refinamientos de este mismo acto fundacional.

## 🧩 Situación

Imagina un programa de facturación donde el subtotal aparece calculado como `a + b` en once lugares distintos: en la pantalla del carrito, en el correo de confirmación, en el PDF, en el reporte contable. Un día el negocio decide que el subtotal debe redondearse. Ahora tienes once ediciones que hacer y once oportunidades de olvidar una. Esa es exactamente la clase de duplicación que Robert Martin ataca en *Clean Code*: el código repetido es deuda que se paga con intereses en cada cambio. La respuesta es definir `suma(a, b)` **una sola vez** y llamarla en los once sitios; el día del cambio, editas un solo cuerpo. La firma es el contrato público —«dame dos números, te devuelvo su suma»— y el cuerpo es el secreto que puedes cambiar sin avisar a nadie mientras el contrato se respete.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros).
- **Salida** (stdout): `suma=<a+b>`.
- **Regla:** `suma(a, b) = a + b`.

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7` |
| `10 20` | `suma=30` |
| `-5 5` | `suma=0` |

## 📖 Definiciones y características

- **Función** — bloque con nombre que recibe parámetros y devuelve un valor. Es la unidad de reutilización y de abstracción: el sitio donde un proceso deja de ser una secuencia de pasos sueltos y pasa a tener identidad propia.
- **Firma** — el nombre, la lista de parámetros y el tipo de retorno tomados juntos. Es lo que un llamador necesita conocer para usar la función; McConnell la describe en *Code Complete* como la «interfaz» de la rutina, la parte que debe permanecer estable aunque el cuerpo cambie.
- **Parámetro** — la variable declarada en el hueco de la definición (`a`, `b`). Existe solo dentro de la función y espera recibir un valor.
- **Argumento** — el valor concreto que se entrega al llamar (`3`, `4`). Llena el parámetro en el momento de la invocación.
- **Retorno** — el valor que la función entrega de vuelta a quien la llamó. Una función que devuelve valor se distingue de un procedimiento, que solo produce efectos.

La distinción parámetro/argumento parece trivial pero es la raíz de la mitad de la confusión sobre funciones. El parámetro es el *hueco*; el argumento es el *relleno*. En `def suma(a, b)`, `a` y `b` son parámetros; en `suma(3, 4)`, `3` y `4` son argumentos. Mantener los dos términos separados vuelve legible todo lo que sigue en esta parte del curso.

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(a, b): DEVOLVER a+b
LEER a, b ; ESCRIBIR "suma=" suma(a,b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys


def suma(a, b):
    return a + b


a, b = map(int, sys.stdin.readline().split())
print(f"suma={suma(a, b)}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

function suma(a, b) {
  return a + b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

function suma(a: number, b: number): number {
  return a + b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static int suma(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("suma=" + suma(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

int Suma(int a, int b) => a + b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(int.Parse(p[0]), int.Parse(p[1]))}");
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

func suma(a, b int) int {
	return a + b
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	fmt.Printf("suma=%d\n", suma(a, b))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(v[0], v[1]));
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

long suma(long a, long b) {
    return a + b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld\n", suma(a, b));
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la operación se expresa en la propia consulta.
WITH pares(a, b) AS (VALUES (3, 4), (10, 20), (-5, 5))
SELECT printf('suma=%d', a + b) AS resultado FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
function suma($a, $b) {
    return $a + $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "suma=" . suma((int) $a, (int) $b) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Ejemplo trabajado — del stdin a la salida

Sigamos el primer caso de `casos.json` (`stdin = "3 4"`, `esperado = "suma=7"`) a través de tres lenguajes que declaran la misma firma con filosofías distintas.

**Python.** La línea `a, b = map(int, sys.stdin.readline().split())` hace tres cosas: `readline()` lee `"3 4\n"`, `.split()` produce la lista `["3", "4"]`, y `map(int, ...)` la convierte en enteros que se desempaquetan en `a=3` y `b=4`. Entonces `suma(a, b)` empareja los **argumentos** `3` y `4` con los **parámetros** `a` y `b`, ejecuta `return a + b` y devuelve `7`. El f-string `f"suma={suma(a, b)}"` interpola ese `7` y `print` emite `suma=7`. Fíjate en que la firma `def suma(a, b)` no menciona tipos: Python confía en que lo que llegue soporte el operador `+`. Si en vez de enteros llegaran cadenas, `suma("3", "4")` devolvería `"34"` sin error —la misma función, semántica distinta según el argumento—.

**Go.** Aquí la firma es `func suma(a, b int) int`: los parámetros y el retorno declaran su tipo, y `a, b int` es la forma abreviada idiomática de Go cuando dos parámetros comparten tipo. El `main` parsea con `strconv.Atoi`, obtiene `a=3, b=4`, y `fmt.Printf("suma=%d\n", suma(a, b))` fuerza a que el resultado sea un entero (`%d`). Si intentaras pasar un texto, el programa **no compilaría**: el contrato de tipos se comprueba antes de ejecutar, no durante. Ese es el corazón de la diferencia semántica entre un lenguaje de tipado dinámico y uno estático.

**Rust.** La firma `fn suma(a: i64, b: i64) -> i64` es la más explícita: cada parámetro y el retorno llevan tipo, y el cuerpo `a + b` sin `;` **es** el valor de retorno (Rust es orientado a expresiones; una línea sin punto y coma es el resultado del bloque). El caso `-5 5` es revelador: `suma(-5, 5)` devuelve `0`, y `println!("suma={}", 0)` emite `suma=0`, coincidiendo con el tercer caso. Los tres lenguajes recorren el mismo camino conceptual —parsear, llamar, formatear— pero cada uno decide en qué momento y con qué rigor se verifica el contrato de la firma.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | La palabra clave cambia: `def` (Python, PHP), `function` (JS/TS), `func` (Go), `fn` (Rust), y en Java/C/C# la firma empieza por el tipo de retorno sin palabra clave. |
| Semántica | Estáticos (Java, C#, Go, Rust, C, TS) fijan los tipos de parámetros y retorno en la firma y los comprueban en compilación; dinámicos (Python, JS, PHP) los resuelven al ejecutar. |
| Semántica | El retorno de expresión frente al de sentencia: en Rust y en el `=>` de C# el cuerpo *es* el valor; en Python, Java o C hace falta `return` explícito. |
| Paradigmática | SQL no «define y llama» una función: expresa la operación como una consulta sobre filas, sin parámetros por posición ni retorno imperativo. |

La lección de fondo la enuncia McConnell en *Code Complete*: la firma es la interfaz, y una buena interfaz oculta el cuerpo. Da igual que Rust devuelva por expresión y Java por sentencia; para quien llama, ambas prometen «dos enteros entran, un entero sale». Esa promesa estable es lo que permite cambiar el interior sin romper el exterior.

## 🧬 El concepto en la familia

En **Ruby** se escribe `def suma(a, b) = a + b`, sin `return` porque el valor de la última expresión se devuelve solo, igual que en Rust. En **Haskell**, `suma a b = a + b` no lleva paréntesis y su firma de tipos, `suma :: Int -> Int -> Int`, se infiere si no la escribes: cada flecha revela que la función en realidad toma un argumento y devuelve otra función (currificación). **Kotlin** usa `fun suma(a: Int, b: Int): Int = a + b`, mezclando la palabra clave `fun` con el cuerpo de expresión. Reconocer la familia —dónde va el tipo, si hay `return`, si el cuerpo es expresión— permite leer una firma nueva en segundos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 073
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir parámetro con argumento** → causa: usar los términos y el orden al revés al leer o documentar → solución: fija la regla «parámetro en la definición, argumento en la llamada» y aplícala siempre.
- **Olvidar el `return`** → causa: en lenguajes de sentencia, el cuerpo calcula pero no devuelve, y el llamador recibe `None`/`undefined`/`void` → solución: comprueba que toda rama de la función termina devolviendo el valor esperado.
- **Depender del orden posicional sin querer** → causa: `suma(b, a)` compila y a veces «funciona» por casualidad con datos simétricos → solución: en llamadas con muchos argumentos, prefiere nombres (clase 075) o tipos que impidan el intercambio.
- **Firmas demasiado largas** → causa: acumular parámetros hasta volver la función ilegible → solución: Martin recomienda en *Clean Code* mantener pocos argumentos; si crecen, agrúpalos en un objeto o registro.

## ❓ Preguntas frecuentes

- **¿Función o procedimiento?** Una función devuelve un valor utilizable; un procedimiento solo actúa (imprime, guarda). En esta clase devolvemos, para poder componer el resultado.
- **¿Por qué la firma lleva tipos en unos lenguajes y en otros no?** Porque unos verifican el contrato en compilación (estáticos) y otros al ejecutar (dinámicos). Es la diferencia semántica más influyente de toda la parte.
- **¿Importa el orden de los parámetros?** Sí: en llamadas posicionales el orden *es* el significado. `restar(a, b)` no es `restar(b, a)`. Los argumentos nombrados (clase 075) rompen esa dependencia.
- **¿Reutilizar de verdad importa tanto?** Sí: cada duplicación es un sitio más donde el mismo cambio debe repetirse y un bug puede esconderse. Nombrar el proceso una vez es la forma más barata de calidad.

## 🔗 Referencias

**Libros de la parte:**

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), §1.1 sobre procedimientos como abstracciones nombradas.
- R. C. Martin — *Clean Code* (Prentice Hall), cap. 3 «Functions».
- S. McConnell — *Code Complete* (2ª ed., Microsoft Press), cap. 7 «High-Quality Routines».

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

> [⏮️ Clase 072](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 074 ⏭️](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md)
