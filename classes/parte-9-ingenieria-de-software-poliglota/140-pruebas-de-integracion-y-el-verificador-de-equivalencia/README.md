# Clase 140 — Pruebas de integración y el verificador de equivalencia

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Una prueba unitaria mira una función en aislamiento; una **prueba de integración** mira qué ocurre cuando varias partes se encuentran: el módulo que llama a la base de datos, el servicio que consume una API, las dos implementaciones que deberían dar el mismo resultado. Hunt y Thomas, en *The Pragmatic Programmer*, lo resumen en una consigna que conviene tatuar: "las pruebas son la primera persona que usa tu código". La integración es donde aparecen los defectos que ninguna unidad sola revela —el desajuste de formatos, el supuesto que una parte hacía y la otra no cumplía—, y por eso es la capa donde se cazan las regresiones más caras.

Este curso lleva esa idea al extremo con su **verificador de equivalencia**: para cada clase existen diez implementaciones —una por lenguaje del núcleo— y el verificador exige que todas produzcan *exactamente* la misma salida por `stdout` ante las mismas entradas de `casos.json`. Eso convierte el `stdout` en un **contrato de equivalencia observable**: no comparamos el código interno (que es distinto en Python y en Rust, y debe serlo), sino el comportamiento visible. Si Go imprime `equivalente=true` y C imprime `equivalente=True`, no son equivalentes aunque el algoritmo sea idéntico, porque el contrato es la cadena de bytes emitida. En esta clase construyes, en pequeño, ese mismo comparador.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Comparar** dos salidas y decidir si son equivalentes según un contrato de igualdad explícito.
2. **Contrastar** una prueba de integración con una unitaria y decir qué caza cada una.
3. **Explicar** por qué comparar por `stdout` define un contrato de equivalencia observable e independiente del lenguaje.
4. **Relacionar** el ejercicio con el verificador de equivalencia que usa la CI de este curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Integración vs. unidad | Los defectos de las costuras solo aparecen cuando las partes se juntan |
| 2 | Equivalencia observable | Dos implementaciones distintas son equivalentes si su salida visible coincide |
| 3 | Verificador del curso | Es la CI que garantiza que los diez lenguajes cumplen el mismo contrato |
| 4 | Regresión | Un cambio que rompe lo que funcionaba; el verificador lo detiene antes de mezclarse |

## 📖 Definiciones y características

- **Prueba de integración.** Verifica que dos o más piezas colaboran correctamente: no que cada una funcione por separado (eso ya lo cubre la unitaria), sino que sus supuestos encajan en la frontera. Hunt y Thomas advierten que la mayoría de los defectos "difíciles" viven en esas costuras, donde un componente esperaba milisegundos y el otro entregaba segundos.
- **Equivalencia observable.** Dos implementaciones son equivalentes si, ante las mismas entradas, producen la misma salida *observable* —aquí, la misma cadena en `stdout`—. No exige que el código interno se parezca; de hecho, el código de Python y el de C son irreconocibles entre sí. Lo que se contrasta es el comportamiento externo, que es lo único que le importa a quien consume el programa.
- **Regresión.** Un cambio que rompe algo que antes funcionaba. Una batería de pruebas de equivalencia que corre en cada *commit* es la trampa que las caza: si una implementación deja de producir la salida acordada, el verificador la marca en rojo y bloquea la mezcla.

## 🧩 Situación

Migras un servicio de cálculo de un monolito en Java a un microservicio en Go. La lógica "es la misma", dicen todos, pero nadie quiere apostar el cierre contable a esa frase. La solución pragmática es una prueba de equivalencia: alimentas ambos con el mismo lote de entradas reales y comparas sus salidas byte a byte. Mientras coincidan, la migración es segura; en cuanto divergen, tienes el caso exacto que rompe. Ese es, a escala de curso, el trabajo del verificador de equivalencia, y aquí construyes su núcleo comparando dos valores.

## 🧮 Modelo

- **Entrada** (stdin): una línea `x y` (dos resultados a comparar)
- **Salida** (stdout): `equivalente=<true|false>`
- **Regla:** equivalente si x == y

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `6 6` | `equivalente=true` |
| `5 7` | `equivalente=false` |
| `0 0` | `equivalente=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER x, y ; ESCRIBIR equivalente=(x==y)
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). Fíjate en un detalle sutil pero central: todas comparan los valores como **cadenas de texto**, no como números. Comparar `"6"` con `"6"` en vez de `6 == 6` no es un descuido: es lo que hace el verificador real, que lee la salida de cada programa como texto y la contrasta carácter a carácter. Así, la equivalencia se define sobre lo observable, no sobre la interpretación numérica.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

x, y = sys.stdin.readline().split()
print(f"equivalente={'true' if x == y else 'false'}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

Aquí `split()` deja `x` e `y` como cadenas —`"6"` y `"6"` para la entrada `6 6`— y `x == y` compara texto. El resultado se serializa en minúsculas, `true` o `false`, porque ese es el contrato fijado en `casos.json`. Un detalle que parece trivial encierra la lección de la clase: si Python devolviera `True` (con mayúscula, como es su literal booleano nativo) la comparación con la cadena esperada `equivalente=true` fallaría, aunque la *lógica* fuese correcta. El contrato no es "acierta el booleano"; es "emite estos bytes exactos". Por eso el verificador es un juez tan estricto: no interpreta, compara.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
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
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println("equivalente=" + (p[0].equals(p[1]) ? "true" : "false"));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"equivalente={(p[0] == p[1] ? "true" : "false")}");
```

🧬 **El mismo programa en la familia .NET:** [F# · VB.NET](primos.md#dotnet)

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	res := "false"
	if f[0] == f[1] {
		res = "true"
	}
	fmt.Printf("equivalente=%s\n", res)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let res = if v[0] == v[1] { "true" } else { "false" };
    println!("equivalente={res}");
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char x[64], y[64];
    if (scanf("%63s %63s", x, y) != 2) return 1;
    printf("equivalente=%s\n", strcmp(x, y) == 0 ? "true" : "false");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara dos valores.
WITH t(x, y) AS (VALUES (6, 6))
SELECT printf('equivalente=%s', CASE WHEN x = y THEN 'true' ELSE 'false' END) AS resultado FROM t;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "equivalente=" . ($x === $y ? "true" : "false") . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

Observa cómo cada lenguaje llega al mismo contrato por caminos que reflejan su naturaleza. **C** no puede comparar cadenas con `==` (eso compararía punteros), así que usa `strcmp(x, y) == 0`, un recordatorio de Kernighan y Ritchie de que en C una cadena es un puntero a bytes y la igualdad debe recorrerse a mano. **Java** evita la trampa clásica del `==` entre objetos y usa `p[0].equals(p[1])`, comparación de contenido y no de referencia. **PHP** elige `===`, el operador estricto que compara valor *y* tipo, frente al laxo `==` que haría conversiones sorpresa. Tres decisiones distintas, un único `stdout`: esa convergencia sobre lo observable, pese a la divergencia interna, es precisamente lo que el verificador de equivalencia certifica.

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

La igualdad de texto no es un gesto uniforme entre lenguajes, y ahí se esconden defectos reales de integración.

| Lenguaje | Igualdad de cadenas | Trampa a evitar | Herramienta de integración |
|---|---|---|---|
| Python | `x == y` | `True` vs. `"true"` al serializar | pytest + fixtures / testcontainers |
| JavaScript | `x === y` | `==` con coerción | Jest / vitest + supertest |
| TypeScript | `x === y` | igual que JS en runtime | vitest + supertest |
| Java | `a.equals(b)` | `==` compara referencias | JUnit + Testcontainers |
| C# | `a == b` (sobrecargado) | `ReferenceEquals` no es lo mismo | xUnit + WebApplicationFactory |
| Go | `a == b` | comparar `[]byte` requiere `bytes.Equal` | `go test` + `httptest` |
| Rust | `a == b` (`PartialEq`) | comparar `&str` vs `String` | `cargo test` + módulos `tests/` |
| C | `strcmp(a,b)==0` | `==` compara punteros | Criterion / Unity |
| SQL | `a = b` | `NULL = NULL` da `NULL`, no cierto | pgTAP / aserciones por consulta |
| PHP | `$a === $b` | `==` laxo convierte tipos | PHPUnit + WebTestCase |

La columna del medio es la más instructiva: la comparación de igualdad, que parece la operación más inocente del mundo, es fuente de bugs sutiles en casi todos los lenguajes. Comparar referencias en Java o punteros en C, dejar que PHP o JavaScript conviertan tipos con `==`, o toparse con la lógica de tres valores de SQL donde `NULL = NULL` no es verdadero, son errores que se manifiestan justo en la frontera entre módulos. Un verificador que compara `stdout` como texto plano neutraliza todas esas trampas: reduce la equivalencia a una sola pregunta sin ambigüedad —¿son estos bytes iguales a aquellos?

## 🧬 El concepto en la familia

El patrón "mismas entradas → misma salida" es el fundamento de las *golden master tests* y de las pruebas de caracterización que Fowler describe en *Refactoring* para blindar código heredado antes de tocarlo. También es el corazón de las pruebas de contrato entre servicios y de las *snapshot tests* de las interfaces. En todas, la idea es la misma que aquí: fijar el comportamiento observable como referencia y detectar cualquier desviación, sin comprometerse con cómo se produce internamente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 140
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comparar implementaciones en vez de salidas.** Si tu prueba inspecciona el código interno o el nombre de las funciones, se rompe con cualquier refactor legítimo. Compara siempre el resultado observable, que es lo que el usuario percibe.
- **No fijar el formato de salida.** Un salto de línea de más, un `True` en vez de `true`, un espacio final invisible: diferencias espurias que hacen fallar la equivalencia por ruido, no por lógica. Define el contrato al byte y ajústate a él.
- **Ignorar el orden en salidas de conjunto.** Si el programa emite una lista sin orden garantizado, dos ejecuciones "correctas" pueden diferir. Ordena antes de comparar o el contrato será inestable.
- **Confundir cobertura de integración con la de unidad.** Una batería de integración verde no implica que cada unidad esté bien probada, y viceversa; son capas complementarias, no sustitutas.

## ❓ Preguntas frecuentes

- **¿Unitaria o integración?** La unitaria prueba una función aislada y corre en milisegundos; la de integración prueba varias piezas juntas y suele necesitar recursos (una BD, un puerto). Necesitas ambas: muchas unitarias rápidas y unas cuantas de integración en los puntos de costura críticos.
- **¿Qué garantiza el verificador?** Que las diez implementaciones producen la misma salida observable ante los mismos casos. No garantiza que la prosa del README sea correcta ni que el algoritmo sea óptimo: solo la equivalencia del comportamiento visible.
- **¿Por qué comparar texto y no el valor semántico?** Porque el texto es el único denominador común entre diez lenguajes. Un contrato sobre `stdout` es inequívoco, portable y trivial de verificar en CI; cualquier interpretación más "inteligente" reintroduciría las trampas de igualdad que la tabla anterior enumera.

## 🔗 Referencias

**Libros de la parte:**

- S. McConnell — *Code Complete* (2ª ed., Microsoft Press).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- M. Fowler — *Refactoring* (2ª ed., Addison-Wesley).
- E. Gamma, R. Helm, R. Johnson y J. Vlissides — *Design Patterns* (Addison-Wesley; «GoF»).
- K. Beck — *Test-Driven Development: By Example* (Addison-Wesley).

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

> [⏮️ Clase 139](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 141 ⏭️](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md)
