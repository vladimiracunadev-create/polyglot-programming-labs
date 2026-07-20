# Clase 123 — Del código a la ejecución: fases de compilación

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Toda ejecución de código —la compiles con `gcc` o la corras con `python`— arranca con el mismo viaje: un texto plano, que ninguna CPU entiende, se transforma paso a paso en una acción. Esta clase recorre ese viaje en miniatura construyendo un evaluador de la expresión `a op b`. El *porqué* de estudiarlo es que las tres fases que verás —análisis **léxico**, análisis **sintáctico** y **evaluación**— son exactamente las que Nystrom desarrolla capítulo a capítulo en *Crafting Interpreters* (scanning → parsing → evaluating) y las que el «Dragon Book» de Aho, Lam, Sethi y Ullman formaliza como el *front-end* de cualquier compilador. Dominarlas te da el modelo mental para leer un mensaje de error con criterio, para entender por qué unos fallos aparecen antes de ejecutar y otros solo al ejecutar, y para dejar de ver al compilador como una caja negra que «funciona o no».

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Tokenizar una entrada de texto: partirla en unidades léxicas con categoría (número, operador).
2. Reconocer la estructura gramatical de una expresión a partir de sus tokens.
3. Nombrar y ordenar las fases del front-end de un compilador y situar la evaluación después de ellas.
4. Explicar por qué un error léxico, uno sintáctico y uno semántico se detectan en fases diferentes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Análisis léxico (scanning) | Convierte una ristra de caracteres en tokens con significado |
| 2 | Análisis sintáctico (parsing) | Reconoce si los tokens forman una expresión válida |
| 3 | Evaluación (o generación de código) | Recorre la estructura y produce el resultado |

## 📖 Definiciones y características

El **análisis léxico** —el *scanner* de Nystrom, el *lexer* del Dragon Book— es la primera muralla. Recibe una secuencia de caracteres (`'3'`, `' '`, `'+'`, `' '`, `'4'`) y agrupa esos caracteres en *tokens*: unidades mínimas con una categoría. El espacio se descarta; `3` se reconoce como un literal numérico; `+` como un operador. En un compilador real esta fase también detecta el primer tipo de error, el **error léxico**: un carácter que no puede empezar ningún token válido (por ejemplo `@` en medio de una expresión aritmética).

El **análisis sintáctico** toma esos tokens y comprueba que su orden respeta la *gramática* del lenguaje. Aquí una expresión aritmética se define como «número, operador, número»; una secuencia como `3 + +` es léxicamente válida (todos son tokens legítimos) pero **sintácticamente** inválida. El parser construye, explícita o implícitamente, un árbol —el *árbol sintáctico abstracto* o AST— que captura la estructura: qué es operando y qué es operador. En nuestro mini-evaluador el árbol es tan pequeño que cabe en tres variables (`a`, `op`, `b`), pero el rol es idéntico.

La **evaluación** es el back-end en su forma más directa: recorre la estructura reconocida y produce un valor. Un compilador de verdad no evaluaría aquí, sino que *generaría código* (bytecode o instrucciones de máquina) para evaluar más tarde; un intérprete, en cambio, calcula el resultado en el acto. Esa bifurcación —evaluar ya o generar código para evaluar después— es la frontera entre intérprete y compilador que abre la clase 124.

## 🧩 Situación

Escribes `3 + 4` y esperas un `7`, pero nunca ves lo que ocurre entre medias. Cuando un compañero te pregunta «¿por qué el compilador dice *unexpected token* en la línea 12 si el error real está en la 11?», la respuesta vive en estas fases: el lexer y el parser leen de izquierda a derecha y solo *notan* que algo no cuadra cuando llegan al token que rompe la gramática, no donde tú, humano, ves la causa. Reproducir el pipeline —tokenizar, reconocer, evaluar— con una operación trivial te deja ver el mecanismo completo sin la complejidad de un lenguaje real.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a op b` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** aplicar el operador a los dos operandos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 + 4` | `resultado=7` |
| `10 - 2` | `resultado=8` |
| `5 * 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
TOKENIZAR ; RECONOCER (num op num) ; EVALUAR
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

a, op, b = sys.stdin.readline().split()
a, b = int(a), int(b)
if op == "+":
    r = a + b
elif op == "-":
    r = a - b
else:
    r = a * b
print(f"resultado={r}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
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
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[0]), b = Long.parseLong(t[2]);
        long r = t[1].equals("+") ? a + b : t[1].equals("-") ? a - b : a * b;
        System.out.println("resultado=" + r);
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[0]), b = long.Parse(t[2]);
long r = t[1] switch { "+" => a + b, "-" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
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
	t := strings.Fields(line)
	a, _ := strconv.Atoi(t[0])
	b, _ := strconv.Atoi(t[2])
	var r int
	switch t[1] {
	case "+":
		r = a + b
	case "-":
		r = a - b
	default:
		r = a * b
	}
	fmt.Printf("resultado=%d\n", r)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[0].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[1] {
        "+" => a + b,
        "-" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long a, b;
    char op;
    if (scanf("%ld %c %ld", &a, &op, &b) != 3) return 1;
    long r = op == '+' ? a + b : op == '-' ? a - b : a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL evalúa la expresión según el operador con CASE.
WITH e(a, op, b) AS (VALUES (3, '+', 4))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN a + b WHEN '-' THEN a - b ELSE a * b END) AS resultado
FROM e;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$a, $op, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$r = $op === "+" ? $a + $b : ($op === "-" ? $a - $b : $a * $b);
echo "resultado=$r\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🧪 Laboratorio: recorrido del código

Sigue el mismo caso, `3 + 4`, a través de tres implementaciones y verás las tres fases aunque el código nunca las nombre.

En **Python**, `sys.stdin.readline().split()` es el *lexer*: parte la línea por espacios y produce tres tokens (`"3"`, `"+"`, `"4"`) que se desempaquetan en `a, op, b`. La *fase sintáctica* está implícita en ese desempaquetado de tres nombres: el código asume la forma «operando, operador, operando» y fallaría si llegaran dos o cuatro tokens. Luego `int(a)` y `int(b)` convierten los tokens numéricos en enteros reales —una conversión que en un compilador sería parte del análisis *semántico*— y la cadena `if op == "+" ... elif ... else` es el *evaluador*: elige la operación según el token operador y produce `r = 7`. La salida `resultado=7` sale de un `print` con f-string.

En **C**, el lexer y el parser están fusionados en una sola línea: `scanf("%ld %c %ld", &a, &op, &b)` describe el patrón esperado —entero, carácter, entero— y en un solo paso tokeniza *y* comprueba la estructura. El `if (... != 3) return 1;` es el manejo de error sintáctico: si la entrada no encaja con el patrón, `scanf` devuelve cuántos campos logró leer y el programa aborta. Como C compila a código máquina (`cc main.c -o main`), toda esta lógica ya está traducida a instrucciones de la CPU *antes* de que exista la entrada `3 + 4`; el binario no vuelve a mirar el texto fuente. Aho et al. llamarían a `scanf` un analizador *ad hoc*: hace el trabajo del front-end sin una gramática formal.

En **Rust**, `read_to_string` absorbe toda la entrada y `s.split_whitespace().collect()` produce un vector de tokens `t`. La diferencia semántica reveladora está en `t[0].parse().unwrap()`: `parse` devuelve un `Result` —éxito o error explícito— y `unwrap` decide «si falla, aborta con pánico». Rust te obliga a *decir* qué pasa cuando el token no es un número; C te deja ignorarlo y Python lanza una excepción no capturada. El `match t[1] { "+" => ... }` es un evaluador que, además, el compilador verifica: si olvidaras el brazo `_`, Rust rechazaría compilar por exhaustividad incompleta. Esa es la marca de un lenguaje con front-end estricto.

## 🔬 Comparación

| Fase / rasgo | Cómo se manifiesta entre los 10 lenguajes |
|---|---|
| Léxico | Python/JS/PHP/Go/Rust parten por espacios (`split`, `Fields`, `split_whitespace`); C usa el patrón de `scanf`; SQL no tokeniza texto de entrada. |
| Sintáctico | Casi todos asumen la forma correcta; solo C (retorno de `scanf`) y Rust (`Result`) hacen explícita la comprobación. |
| Momento del error | C, Go, Rust, Java, C# detectan errores de *tipo* en compilación; Python, JS y PHP, al ejecutar la línea que falla. |
| Modelo de ejecución | Compilado a máquina (C, Rust, Go), a bytecode + VM (Java, C#), interpretado (Python, PHP, JS), declarativo (SQL). |
| Manejo de fallo léxico | Excepción (Python, PHP), pánico opt-in (`unwrap` en Rust), retorno de código (`scanf` en C), valor ignorado (`_` en Go). |

## 🧬 El concepto en la familia

El pipeline léxico → sintáctico → evaluación es universal, pero cada herramienta lo instancia distinto. `gcc` y `clang` recorren las fases completas del Dragon Book (léxico, sintáctico, semántico, generación de IR, optimización, código de máquina) antes de producir un ejecutable. `javac` se detiene en el bytecode. `rustc` añade una fase de *borrow checking* entre el análisis semántico y la generación. CPython y V8 tokenizan y parsean cada vez que cargan el fuente, y solo entonces evalúan o compilan a bytecode. Reconocer estas fases te permite leer la salida de `-Wall`, `--explain` o un *traceback* sabiendo en qué etapa del viaje se rompió el código.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 123
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir «error léxico» con «error sintáctico»** → causa: creer que todo fallo de análisis es lo mismo → solución: recordar que el léxico es un carácter imposible (`@`), y el sintáctico un orden de tokens imposible (`3 + +`); se detectan en fases distintas.
- **Asumir que el intérprete no compila nada** → causa: oponer «compilado» a «interpretado» como si fueran excluyentes → solución: CPython tokeniza, parsea y genera bytecode; luego ese bytecode lo ejecuta un intérprete. Ambas cosas conviven.
- **Operador no contemplado** → causa: la rama `else`/`_` captura cualquier símbolo como multiplicación → solución: en código real, validar el token operador y rechazar los desconocidos en la fase sintáctica.

## ❓ Preguntas frecuentes

- **¿Compilar es solo estas tres fases?** No: son el front-end. Después vienen el análisis semántico, la generación de código intermedio, la optimización y la generación de código de máquina —las fases que el Dragon Book detalla por separado.
- **¿Un intérprete parsea de verdad?** Sí. CPython y V8 tokenizan y construyen un AST antes de ejecutar; la diferencia con un compilador AOT no es que se salten el parsing, sino qué hacen *después* del AST.
- **¿Dónde encaja el enlazado (linking)?** Fuera de este pipeline por expresión: como muestra Bryant & O'Hallaron, en C el compilador produce código objeto y un *linker* aparte lo combina con las bibliotecas —un paso que Python o JavaScript resuelven en tiempo de ejecución.

## 🔗 Referencias

**Libros de la parte:**

- R. Nystrom — *Crafting Interpreters* (Genever Benning) — [gratis online](https://craftinginterpreters.com/).
- A. Aho, M. Lam, R. Sethi y J. Ullman — *Compilers: Principles, Techniques, and Tools* (2ª ed., Pearson; «Dragon Book»).
- R. Bryant y D. O'Hallaron — *Computer Systems: A Programmer's Perspective* (3ª ed., Pearson).

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

> [⏮️ Clase 122](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 124 ⏭️](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md)
