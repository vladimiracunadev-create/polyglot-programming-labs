# Clase 043 — Tipos primitivos: enteros, reales, booleanos, caracteres

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Los **tipos primitivos** —enteros, reales, booleanos, caracteres— son los átomos con los que se construye todo dato compuesto. Son "primitivos" porque el lenguaje los trae incorporados y suelen corresponder de forma directa a algo que la máquina sabe manipular: una palabra de la CPU para un entero, un registro de coma flotante para un real. Esta clase los pone en acción tomando un mismo número y observándolo bajo tres lentes: como **entero** (`4`), convertido a **real** (`4.0`) y evaluado como **booleano** (`4 es par → true`). El punto que queremos que quede es sutil pero fundamental: el *valor* matemático es uno, pero el *tipo* con que el lenguaje lo trata determina cómo se guarda, cómo se opera y cómo se muestra.

Un tipo, en la definición que Pierce sitúa en el centro de su obra, es una disciplina que clasifica valores según lo que se puede hacer con ellos y descarta por adelantado los programas que mezclarían cosas incompatibles. Distinguir entero de real no es capricho: la aritmética entera es *exacta* mientras que la de coma flotante es *aproximada* y sigue el estándar IEEE 754, de modo que `4` y `4.0` viven en mundos con reglas distintas aunque valgan lo mismo. El booleano, por su parte, es el tipo más pequeño posible —solo `true` o `false`— y sin embargo gobierna todas las decisiones del programa; nace aquí de una condición (`n % 2 == 0`).

Comparar diez lenguajes sobre este problema mínimo revela que lo universal es el concepto y lo variable es la superficie: cómo se convierte un entero a real, con cuántos decimales se formatea, y —sorprendentemente— cómo se escribe `true`. Ese último detalle, que parece trivial, expone que el booleano no tiene una representación textual canónica compartida, y que igualar la salida entre runtimes obliga a conocer las mañas de cada uno.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir entero, real y booleano como tipos primitivos.
2. Convertir un entero a real y formatearlo con decimales.
3. Producir un valor booleano a partir de una condición.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entero | Número sin parte fraccionaria |
| 2 | Real (punto flotante) | Número con decimales; se formatea explícitamente |
| 3 | Booleano | Verdadero o falso, resultado de una condición |
| 4 | Formato de salida | true/false y decimales difieren entre lenguajes |

## 📖 Definiciones y características

- **Tipo primitivo** — tipo básico incorporado al lenguaje (entero, real, booleano, carácter). Clave: bloque elemental de todo dato.
- **Entero** — número sin decimales, de tamaño fijo en los estáticos. Clave: aritmética exacta.
- **Real** — número en coma flotante. Clave: aproximado; se formatea con un número de decimales.
- **Booleano** — valor de verdad (verdadero/falso). Clave: gobierna las decisiones del programa.

La diferencia entre entero y real no es solo de decimales, sino de *representación en memoria* y de garantías, como subraya Scott. Un entero se guarda como una secuencia de bits que codifica un número exacto; un real sigue el estándar **IEEE 754**, que reparte los bits entre signo, exponente y mantisa para representar un rango enorme a costa de precisión. Por eso `0.1 + 0.2` no da exactamente `0.3` en coma flotante, y por eso convertir `4` a `4.0` no es "añadir un decimal" sino cambiar por completo la codificación del valor. En esta clase la conversión es inofensiva porque los enteros pequeños se representan de forma exacta en `double`, pero el mecanismo es el mismo que en casos delicados.

Sobre los enteros, Bloch hace en el mundo Java una advertencia que conviene retener: los tipos primitivos (`int`, `double`, `boolean`) no son lo mismo que sus **envoltorios** (`Integer`, `Double`, `Boolean`). El primitivo guarda el valor directamente y es más eficiente; el envoltorio es un objeto que puede además ser `null`. La clase usa primitivos porque el problema es aritmético puro, pero la distinción explica por qué Java escribe `int n` y no `Integer n`.

El **booleano** merece una nota aparte por su representación textual. No existe un formato canónico universal: Python imprime `True`/`False` con mayúscula, C# capitaliza igual al llamar `ToString()`, C no tiene un tipo booleano histórico y modela la verdad con enteros (`0`/no-`0`), y SQL carece de un booleano nativo portátil. Por eso el contrato de esta clase fija la cadena en minúsculas `true`/`false` y varias implementaciones la construyen a mano con un condicional, en lugar de confiar en el formateo por defecto del tipo.

## 🧩 Situación

Un mismo `4` puede verse como entero (`4`), como real (`4.0`) o dar lugar a un booleano (`4 es par → true`). Reconocer que el valor es uno y los tipos son lentes distintas es la idea central, y por eso el contrato pide imprimir las tres vistas en una sola línea: obliga a convertir el entero a real con un decimal y a derivar un booleano de una condición, ejercitando de un tiro los tres tipos primitivos numéricos y lógicos. El caso `7` —impar— comprueba la rama `false`, y `0` verifica que el cero se trate como par y se formatee como `0.0`.

## 🧮 Modelo

- **Entrada** (stdin): una línea `n` (un entero)
- **Salida** (stdout): `entero=<n> real=<n con 1 decimal> par=<true|false>`
- **Regla:** real = (double) n ; par = (n módulo 2 == 0)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `entero=4 real=4.0 par=true` |
| `7` | `entero=7 real=7.0 par=false` |
| `0` | `entero=0 real=0.0 par=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
real <- CONVERTIR_A_REAL(n)
par <- (n MOD 2 == 0)
ESCRIBIR "entero=" n " real=" FORMATEAR(real,1) " par=" par
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

n = int(sys.stdin.readline())
real = float(n)
par = "true" if n % 2 == 0 else "false"
print(f"entero={n} real={real:.1f} par={par}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const par = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const par: string = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String par = (n % 2 == 0) ? "true" : "false";
        System.out.printf(Locale.US, "entero=%d real=%.1f par=%s%n", n, (double) n, par);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
int n = int.Parse(Console.In.ReadToEnd().Trim(), inv);
string par = (n % 2 == 0) ? "true" : "false";
Console.WriteLine($"entero={n} real={((double)n).ToString("F1", inv)} par={par}");
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
	par := "false"
	if n%2 == 0 {
		par = "true"
	}
	fmt.Printf("entero=%d real=%.1f par=%s\n", n, float64(n), par)
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
    let par = if n % 2 == 0 { "true" } else { "false" };
    println!("entero={n} real={:.1} par={par}", n as f64);
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *par = (n % 2 == 0) ? "true" : "false";
    printf("entero=%ld real=%.1f par=%s\n", n, (double) n, par);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL no tiene un tipo booleano nativo universal: se usa CASE WHEN.
WITH nums(n) AS (VALUES (4), (7), (0))
SELECT printf('entero=%d real=%.1f par=%s', n, n,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$n = (int) trim(fgets(STDIN));
$par = ($n % 2 === 0) ? "true" : "false";
printf("entero=%d real=%.1f par=%s\n", $n, (float) $n, $par);
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔎 Recorrido guiado por el código

Sigamos el caso `4` de [`casos.json`](casos.json), cuya salida exacta es `entero=4 real=4.0 par=true`. Los tres tipos primitivos aparecen en una sola línea.

En **Python**, `int(sys.stdin.readline())` lee la cadena `"4"` y la convierte al entero `4`, ya con tipo `int`. La línea `real = float(n)` produce el valor real `4.0` a partir del entero: es una conversión de tipo, no un simple adorno, y crea un objeto `float` distinto del `int` original. El booleano nace en `par = "true" if n % 2 == 0 else "false"`: aquí `n % 2 == 0` sí evalúa a un `bool` de Python (`True`), pero el autor *no* lo imprime directamente —lo haría como `True` con mayúscula— sino que elige a mano la cadena `"true"` en minúsculas que pide el contrato. El `f"entero={n} real={real:.1f} par={par}"` ata todo: `{real:.1f}` formatea `4.0` con exactamente un decimal, dando `entero=4 real=4.0 par=true`.

En **C** se ve la naturaleza más cruda de los tipos. `long n;` reserva un entero; `scanf("%ld", &n)` lo llena. La conversión a real es explícita y ocurre en el momento de imprimir: `(double) n` en `printf(... "%.1f" ..., (double) n)` reinterpreta el entero `4` como el `double` `4.0`, y el especificador `%.1f` lo formatea con un decimal. Para el booleano, C no tiene tipo nativo histórico ni cadena asociada, así que el autor lo modela con un puntero a texto: `const char *par = (n % 2 == 0) ? "true" : "false";`. La condición `n % 2 == 0` produce un `int` (1 o 0) que el operador ternario usa para elegir cuál de las dos cadenas literales apuntar. `%s` la imprime tal cual: `entero=4 real=4.0 par=true`.

**Rust** y **C#** ilustran el problema del booleano desde el otro lado. En Rust, `let par = if n % 2 == 0 { "true" } else { "false" };` —igual que C— evita el `bool` nativo (que se imprimiría `true`/`false`, y aquí *coincide*, pero el autor prefiere la cadena explícita por uniformidad con el resto). En C#, la tentación sería `(n % 2 == 0).ToString()`, pero eso daría `True` con mayúscula, rompiendo el contrato; por eso la implementación construye `string par = (n % 2 == 0) ? "true" : "false";` a mano. Es el ejemplo perfecto de que "el mismo booleano" tiene texto distinto según el runtime, y de por qué igualar salidas exige conocerlo. Los tres formatean el real con un decimal (`{:.1}` en Rust, `F1` con `InvariantCulture` en C#) para que `4` se muestre como `4.0`.

## 🔬 Comparación

Detrás de la aparente simpleza hay tres decisiones que cada lenguaje toma por separado: cómo convierte un entero a real, con qué sintaxis fija los decimales y cómo textualiza un valor de verdad. La primera es semántica (cambia la representación en memoria), las otras dos son de formato, pero las tres deben alinearse para que diez runtimes emitan la misma línea.

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El formato de real varía: `f"{real:.1f}"` (Python), `toFixed(1)` (JS/TS), `%.1f` (C/Go/Java), `F1` (C#), `{:.1}` (Rust). |
| Representación | Entero y real usan codificaciones distintas: el real sigue IEEE 754; convertir `4`→`4.0` cambia los bits, no solo el texto. |
| Booleano | No hay texto canónico: Python/C# capitalizan (`True`); C carece de tipo nativo; por eso casi todos construyen la cadena `"true"`/`"false"` a mano. |
| Conversión | Python (`float(n)`), Go (`float64(n)`), Rust (`n as f64`), C (`(double) n`) hacen explícita la promoción int→real. |
| Paradigmática | SQL expresa el booleano con `CASE WHEN`, no con un tipo booleano nativo universal. |

## 🧬 El concepto en la familia

- **Scripting dinámico** (Ruby): `4.to_f` da el real `4.0` y `4.even?` el booleano `true`; todo es un objeto con métodos, incluso los números.
- **Funcional** (Haskell): los tipos son explícitos y disjuntos (`Int`, `Double`, `Bool`) y no hay conversión implícita: pasar de entero a real exige la función `fromIntegral`. Es la disciplina de tipos de Pierce llevada al extremo, donde el compilador rechaza mezclar `Int` y `Double` sin permiso.
- **JVM** (Kotlin): `n.toDouble()` convierte y `n % 2 == 0` da un `Boolean` de verdad; Kotlin, a diferencia de Java, unifica primitivos y objetos en la superficie del lenguaje aunque bajo el capó use el primitivo eficiente.
- **C/llaves** (C++): tiene `bool` nativo desde C++98 (`true`/`false` en minúscula al usar `std::boolalpha`), a diferencia del C clásico que modelaba la verdad con enteros.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 043
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True` con mayúscula** → causa: el `ToString()` de C# y el `str(bool)` de Python capitalizan → solución: construir la cadena `"true"`/`"false"` a mano con un condicional.
- **Esperar `4` en vez de `4.0`** → causa: imprimir el real sin fijar decimales, o dejar que se muestre como entero → solución: formatear con el número de decimales del contrato (`.1f`, `toFixed(1)`, `F1`).
- **Hacer aritmética entera sin querer** → causa: dividir dos enteros esperando un real (p. ej. `n / 2` en C da entero) → solución: convertir un operando a real antes de dividir.
- **Confundir `%` con la paridad de negativos** → causa: en algunos lenguajes `-3 % 2` no es `1`; aquí el contrato usa enteros no negativos, pero conviene saber que el signo del módulo varía entre lenguajes → solución: comparar `n % 2 == 0` para la paridad, que es robusto al signo.
- **Usar el envoltorio cuando basta el primitivo** → causa: declarar `Integer`/`Double` (Java) en un cálculo puro → solución: usar `int`/`double`, más eficientes y sin riesgo de `null` (Bloch).

## ❓ Preguntas frecuentes

- **¿`4` y `4.0` son el mismo valor?** Matemáticamente sí; para el tipo del lenguaje, no: uno es entero y otro real, con codificaciones y reglas de aritmética distintas (exacta vs. IEEE 754).
- **¿Por qué C# y Python escriben True/False?** Su representación textual por defecto capitaliza la primera letra; por eso se construye la cadena en minúsculas para cumplir el contrato.
- **¿Por qué separar entero y real si valen lo mismo?** Porque el tipo decide la representación en memoria, el coste de las operaciones y la precisión: los enteros son exactos, los reales aproximados. El tipo es una promesa sobre qué se puede hacer con el valor.
- **¿El booleano ocupa un bit?** Conceptualmente sí, pero en la práctica suele ocupar un byte (o más) por razones de alineación en memoria; su tamaño lógico —dos estados— no coincide con su tamaño físico.

## 🔗 Referencias

**Libros de la parte:**

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. de tipos de datos primitivos.
- B. C. Pierce — *Types and Programming Languages* (MIT Press), introducción (los tipos como disciplina que clasifica valores).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. de tipos y su representación en memoria.

**Libros de los lenguajes del núcleo:**

- L. Ramalho — *Fluent Python* (2ª ed., O'Reilly), cap. sobre tipos numéricos y el modelo de objetos.
- M. Haverbeke — *Eloquent JavaScript* (3ª ed.) — [gratis online](https://eloquentjavascript.net/).
- B. Cherny — *Programming TypeScript* (O'Reilly).
- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley), ítems sobre tipos primitivos frente a envoltorios.
- J. Skeet — *C# in Depth* (4ª ed., Manning).
- A. Donovan y B. Kernighan — *The Go Programming Language* (Addison-Wesley).
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- J. Lockhart — *Modern PHP* (O'Reilly).

---

> [⏮️ Clase 042](../../parte-3-valores-tipos-y-variables/042-declaracion-asignacion-e-inicializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 044 ⏭️](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md)
