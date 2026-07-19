# Clase 052 — Inferencia de tipos

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La **inferencia de tipos** es la capacidad del compilador de deducir el tipo de una expresión sin que tú lo escribas. Cuando declaras `var total = a * b;` en C# o `let p = a * b;` en Rust, no has anotado ningún tipo, y sin embargo `total` y `p` **tienen** un tipo fijo, entero, que el compilador ha calculado a partir de la expresión. La inferencia es la reconciliación entre dos deseos que parecían opuestos: la seguridad del tipado estático y la concisión del código sin anotaciones. Te da las dos cosas —el compilador sabe el tipo y lo comprueba— sin obligarte a repetir lo que el propio código ya deja obvio.

El punto conceptual más importante, y el que más malentendidos causa, es que **inferencia no es tipado dinámico**. Que no *escribas* el tipo no significa que no *exista* o que pueda cambiar. En `var a = 5`, C# fija `a` como `int` para siempre; asignarle luego una cadena es un error de compilación, exactamente igual que si hubieras escrito `int a`. Sebesta insiste en esta distinción: la inferencia solo omite la *anotación*, no la *ligadura estática* del tipo a la variable. El binario resultante es idéntico al del código anotado; no hay ninguna penalización en ejecución, porque toda la deducción ocurre en compilación.

Hay además dos ligas muy distintas de inferencia, y esta clase las contrasta. La inferencia **local** —`var` en C#/Java, `:=` en Go, `auto` en C++, `let` en Rust— mira solo el lado derecho de una asignación y deduce el tipo de esa expresión: es simple y limitada a la declaración. La inferencia **global** al estilo Hindley-Milner (algoritmo W, que resuelve restricciones por *unificación*), presente en Haskell o ML, deduce los tipos de un programa entero —incluidos parámetros de funciones— casi sin ninguna anotación. TypeScript ocupa un punto intermedio con su inferencia **bidireccional**, que combina el tipo esperado por el contexto con el tipo del valor. El laboratorio usa el caso mínimo —el producto de dos enteros— para poner lado a lado quién infiere (`p = a*b`, `p := a*b`, `let p = a*b`) y quién exige la anotación (`int p = a*b` en Java y C).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer dónde el lenguaje infiere el tipo.
2. Comparar inferencia con anotación explícita.
3. Escribir el mismo cálculo con y sin anotar tipos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inferencia | El compilador deduce el tipo del valor |
| 2 | Anotación explícita | El programador escribe el tipo |
| 3 | var/:=/let | Palabras de inferencia por lenguaje |
| 4 | Inferencia no es dinámico | El tipo sigue siendo fijo, solo no se escribe |

## 📖 Definiciones y características

- **Inferencia de tipos** — el compilador deduce el tipo a partir del valor. Clave: menos ruido, mismo tipado estático.
- **Anotación de tipo** — escribir el tipo explícitamente (`int x`). Clave: obligatoria donde no hay inferencia.
- **var / := / let** — formas de declarar con inferencia (C#, Go, Rust). Clave: el tipo se fija igual.
- **Estático con inferencia** — tipos fijos que no hace falta anotar. Clave: no confundir con dinámico.

La inferencia funciona resolviendo **restricciones**. El compilador observa la expresión `a * b`, sabe que `a` y `b` son `int` (a su vez inferidos de sus valores), sabe que multiplicar dos `int` produce un `int`, y por tanto concluye que la variable que recibe ese resultado es `int`. En la inferencia local eso es todo: se examina el lado derecho de una declaración y se propaga su tipo hacia la izquierda. Rust añade un matiz potente: puede inferir *hacia atrás* desde un uso posterior —si más adelante la variable se compara con un `u8`, Rust la deduce `u8` aunque la declaración no lo dijera—, un pequeño paso hacia la inferencia global.

La inferencia **global de Hindley-Milner** —el algoritmo W— es de otra escala. En lugar de mirar una declaración aislada, recoge restricciones de todo el programa y las resuelve por **unificación**: un proceso que busca la asignación de tipos más general que satisface todas las ecuaciones a la vez. Por eso en Haskell casi nunca anotas tipos, ni siquiera en los parámetros de una función: el compilador los deduce del cuerpo. Scott describe la unificación como el corazón de este mecanismo, y es lo que permite que un lenguaje sea a la vez fuertemente tipado y notablemente conciso. TypeScript usa una variante **bidireccional**: cuando el contexto ya impone un tipo esperado (por ejemplo, el tipo de retorno declarado de una función), lo *empuja* hacia la expresión en vez de deducirlo solo desde el valor.

El malentendido que hay que erradicar es equiparar "no anotar" con "sin tipo". Un lenguaje dinámico como Python no anota porque el tipo vive en el valor y se comprueba en ejecución; un lenguaje estático con inferencia como Rust no anota porque el tipo ya está **fijado en compilación**, solo que deducido en vez de escrito. La diferencia es abismal: en el segundo caso, reasignar un valor de otro tipo es un error que detiene la compilación. Inferencia y dinamismo se parecen a la vista —ambos omiten el tipo en el código— pero son opuestos en cuándo y con qué firmeza se liga el tipo.

## 🧩 Situación

Imagina que revisas un cálculo de inventario: `var total = unidades * precioPorCaja;`. En C# esa línea no dice ningún tipo, y sin embargo `total` queda ligado a un tipo concreto —el que resulte de multiplicar sus operandos— desde el instante de la compilación. Un lector desprevenido podría pensar que C# se ha vuelto dinámico como Python; no es así. Si en la línea siguiente intentaras `total = "agotado";`, el compilador lo rechazaría, porque `total` es y seguirá siendo numérico. La única diferencia con `int total = ...` es que te ahorraste escribir el tipo que ya era evidente.

Distinguir inferencia de dinamismo evita malentendidos costosos: te permite disfrutar de código conciso sin perder la red de seguridad estática, y te protege de la falsa creencia de que `var`, `:=`, `let` o `auto` "relajan" el tipado. No lo relajan; solo dejan de exigir que repitas lo obvio. El laboratorio hace esto tangible con el producto de dos enteros: la misma multiplicación se escribe con inferencia en unos lenguajes y con anotación en otros, y el resultado —y el tipo— es idéntico en todos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `producto=<a*b>`
- **Regla:** producto = a * b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `producto=12` |
| `0 9` | `producto=0` |
| `-2 5` | `producto=-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "producto=" (a*b)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, b = map(int, sys.stdin.readline().split())
print(f"producto={a * b}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`producto=${a * b}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`producto=${a * b}`);
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
        System.out.println("producto=" + (a * b));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var a = int.Parse(p[0]);
var b = int.Parse(p[1]);
Console.WriteLine($"producto={a * b}");
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
	producto := a * b
	fmt.Printf("producto=%d\n", producto)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let producto = v[0] * v[1];
    println!("producto={producto}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("producto=%ld\n", a * b);
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: la expresión produce el valor sin declarar variables.
WITH pares(a, b) AS (VALUES (3, 4), (0, 9), (-2, 5))
SELECT printf('producto=%d', a * b) AS resultado
FROM pares;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$producto = (int) $a * (int) $b;
printf("producto=%d\n", $producto);
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Tomemos el caso `stdin` = `3 4`, esperado `producto=12`, y observemos no *qué* calcula cada lenguaje —todos multiplican— sino **cómo nombra el tipo** de la variable que guarda el resultado.

**Python** es el punto de partida pero también el matiz sutil: `a, b = map(int, sys.stdin.readline().split())` desempaqueta `"3 4"` en dos enteros, y `producto` (implícito en `a * b`) no se declara en ningún sitio. Cuidado: aquí no hay *inferencia estática* como en los compilados; Python es dinámico y el tipo simplemente vive en el objeto en ejecución. Sirve de contraste con lo que sigue: se parece a `var p = a*b` a la vista, pero el mecanismo es distinto. El `print(f"producto={a * b}")` produce `producto=12`; con `-2 5`, la misma expresión da `producto=-10`.

Los lenguajes con **inferencia estática** son el corazón de la clase. En **Go**, `producto := a * b` usa el operador de declaración corta `:=`: Go ve que `a` y `b` son `int` (devueltos por `strconv.Atoi`), deduce que su producto es `int` y liga `producto` a ese tipo **en compilación**, sin que escribas `int`. En **Rust**, `let producto = v[0] * v[1];` hace lo mismo con `let`: no hay anotación, pero `producto` es de tipo fijo `i64` porque el vector se declaró `Vec<i64>` y esa información se propaga. En **C#**, `var a = int.Parse(p[0])` infiere `a` como `int` desde el tipo de retorno de `int.Parse`; la palabra `var` no significa "cualquier tipo", significa "el tipo que deduzcas de la expresión". Los tres —`:=`, `let`, `var`— llegan a un tipo entero fijo sin escribirlo, y todos imprimen `producto=12`.

El polo opuesto lo marcan **Java** y **C**, que **exigen la anotación**. En Java, `int a = Integer.parseInt(p[0]);` y `int b = ...` obligan a nombrar `int` en cada declaración; el resultado se calcula en `(a * b)` sin variable intermedia, pero cada operando llevó su tipo escrito a mano. En C, `long a, b;` declara los tipos por adelantado antes incluso de leerlos con `scanf`. Comparar la línea de Go `producto := a * b` con la de C `long a, b;` en el mismo problema resume la clase entera: mismo tipado estático, mismo binario final, misma salida `producto=12` verificada contra `casos.json`; lo único que cambia es si el compilador dedujo el tipo o si tú lo escribiste.

## 🔬 Comparación

Lo que separa a estos lenguajes es el **grado de inferencia**, no la presencia de tipos: todos los estáticos aquí acaban con una variable de tipo entero fijo. La escala va de la anotación obligatoria (Java, C) a la inferencia local (Go, Rust, C#) y, fuera del núcleo, a la inferencia global de Haskell. Python queda aparte: parece inferir, pero en realidad es dinámico y su tipo se resuelve en ejecución.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `p = a*b` (Python, dinámico), `p := a*b` (Go), `let p = a*b` (Rust), `var a = ...` (C#), `int a = ...` (Java/C). |
| Semántica (mecanismo) | En Go/Rust/C# el tipo se **infiere** en compilación pero queda fijo; en Java/C se **anota** a mano; en Python no se infiere estáticamente, se resuelve al ejecutar. |
| Semántica (alcance) | Inferencia **local** (mira solo la declaración) en Go/C#/Java-`var`; Rust añade deducción desde usos posteriores; Hindley-Milner (Haskell) infiere de todo el programa por unificación. |
| Paradigmática | SQL no declara variables: la expresión produce el valor directamente, sin ligar un tipo a un nombre. |

## 🧬 El concepto en la familia

En Kotlin `val p = a * b` infiere localmente, como Go o C#. En C++ la palabra `auto` cumple ese papel: `auto p = a * b` deduce el tipo de la expresión. En Java, `var` (desde Java 10) trajo la misma inferencia local que C# tenía hace más tiempo. En el extremo está Haskell, cuya inferencia Hindley-Milner es **total**: gracias al algoritmo W y a la unificación, un programa entero puede quedar correctamente tipado casi sin una sola anotación, incluidos los parámetros de las funciones. TypeScript ilustra un punto intermedio con inferencia **bidireccional**, que aprovecha el tipo esperado por el contexto para deducir mejor. Recorrer la familia deja una moraleja: la inferencia es una escala de *cuánto* deduce el compilador, y en todos los casos el tipo resultante es tan fijo y tan comprobado como si lo hubieras escrito.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 052
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que inferencia = dinámico** → causa: confundir no-anotar con no-tipar → solución: recordar que el tipo inferido es fijo y se comprueba
- **No anotar donde hace falta** → causa: Java/C exigen el tipo → solución: anotar cuando el lenguaje no infiere

## ❓ Preguntas frecuentes

- **¿La inferencia hace el código más lento?** No: ocurre en compilación; el binario es idéntico al anotado.
- **¿Siempre puede inferir?** No siempre; a veces el tipo es ambiguo y hay que anotar.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. tipos y variables.
- B. C. Pierce — *Types and Programming Languages* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

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

> [⏮️ Clase 051](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 053 ⏭️](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md)
