# Clase 147 — Integración continua (CI) multi-lenguaje

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La **integración continua (CI)** nace de una observación incómoda: cuanto más tiempo pasa un cambio sin fundirse con el trabajo de los demás, más caro y doloroso se vuelve integrarlo. Hunt y Thomas, en *The Pragmatic Programmer*, insisten en integrar temprano y a menudo precisamente para que los conflictos se descubran cuando aún son pequeños; McConnell, en *Code Complete*, defiende la misma idea bajo el nombre de "integración incremental": añadir una pieza, comprobar que todo sigue funcionando, y solo entonces añadir la siguiente. La CI automatiza ese ritual. Cada vez que alguien empuja un cambio, un servidor reconstruye el proyecto, corre las pruebas y pasa el linter. Si todo pasa, el pipeline queda 'verde'; si algo falla, queda 'rojo' y el cambio no debería integrarse hasta arreglarlo.

El corazón de esta clase es una idea lógica sencilla pero exigente: el pipeline está verde **solo si todos los pasos pasan**. Es un AND lógico sobre los resultados. Basta que un paso —compilar, un test, una regla de estilo— falle para que el conjunto entero sea rojo. No hay "verde con excepciones". El programa de juguete de `casos.json` captura exactamente ese AND: recibe una lista de ceros y unos (el resultado de cada paso, `1` = pasó) y responde `ci=verde` únicamente cuando no hay ningún cero. Detrás de esa reducción minúscula está la disciplina que mantiene sano un repositorio real, donde cada paso puede ser un `pytest`, un `cargo build` o un `go vet`.

Entender esto te da algo más que un truco: te da el modelo mental para razonar sobre por qué un equipo que respeta el rojo entrega software más estable, y por qué ignorarlo —"ya lo arreglo luego"— erosiona la confianza en la rama principal hasta que nadie sabe si está sana.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Combinar** el resultado de varios pasos como un AND lógico y justificar por qué basta un fallo para poner el pipeline en rojo.
2. **Describir** las etapas típicas de un pipeline de CI (build, test, lint) y el sentido de `fail-fast` y de la caché de dependencias.
3. **Explicar** cómo una matriz por lenguaje ejecuta el mismo contrato sobre varios entornos en paralelo.
4. **Reconocer** el valor de bloquear la integración en rojo para proteger la rama principal.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | CI e integración frecuente | Descubre conflictos cuando aún son baratos |
| 2 | Pipeline de pasos | Encadena build, test y lint como un contrato |
| 3 | Verde/rojo como AND | Todo pasa, o el conjunto falla |
| 4 | Matriz y fail-fast | Verifica varios entornos y aborta pronto |

## 📖 Definiciones y características

- **Integración continua** — la práctica de fundir cambios en una línea compartida con frecuencia (idealmente varias veces al día) y verificarlos automáticamente en cada empuje. Su promesa, en palabras de McConnell, es acortar el lazo de realimentación: un error introducido esta mañana se detecta esta mañana, no dentro de tres semanas cuando ya está enterrado bajo cien cambios más. La CI no *previene* errores; los hace visibles pronto, que es lo máximo que puede pedirle la ingeniería a una herramienta.
- **Pipeline** — la secuencia ordenada de pasos que se ejecuta sobre cada cambio: típicamente compilar, ejecutar las pruebas y pasar linters/formatters. Cada paso produce un veredicto binario (pasó / falló). La cualidad definitoria del pipeline es que su resultado global es la conjunción de todos: verde exige que *todos* estén en verde.
- **Verde/rojo** — el estado agregado del pipeline. Verde significa "seguro integrar"; rojo significa "algo está roto, no fusiones". Tratar el rojo como una alarma real —no como ruido a ignorar— es lo que convierte la CI en una red de seguridad y no en un adorno.
- **Matriz** — la ejecución del mismo pipeline sobre varias combinaciones de entorno (versiones de lenguaje, sistemas operativos). En un repo políglota como este, la matriz corre el contrato de `casos.json` en Python, Go, Rust, etc., en paralelo, y cada celda aporta su propio verde o rojo al veredicto final.
- **Fail-fast y caché** — dos ajustes prácticos: `fail-fast` aborta el resto de la matriz en cuanto una celda falla, para no gastar minutos en un resultado ya condenado; la **caché de dependencias** guarda entre ejecuciones lo descargado (paquetes de pip, `~/.cargo`, `node_modules`) para que el pipeline sea rápido y el equipo no lo evite por lento.

## 🧩 Situación

Trabajas en un equipo que mantiene este mismo repositorio políglota. Alguien abre un pull request que toca la implementación de una clase. GitHub Actions dispara el workflow: en paralelo, una celda de la matriz compila y prueba la versión en Java, otra corre `cargo test` sobre la de Rust, otra pasa `ruff` sobre la de Python. Dos celdas quedan verdes, pero la de Rust falla porque un `unwrap` reventó con una entrada vacía. El pipeline entero se pone rojo. La regla del equipo es tajante: no se fusiona en rojo. El autor ve el fallo en minutos, corrige el caso borde, empuja de nuevo, y ahora las tres celdas pasan. La rama principal nunca llegó a contener el código roto. Ese pequeño programa que decide `verde` o `rojo` es, en esencia, lo que acabas de vivir a escala.

## 🧮 Modelo

- **Entrada** (stdin): una línea con 0 y 1 (resultado de cada paso; 1 = pasó)
- **Salida** (stdout): `ci=<verde|rojo>`
- **Regla:** verde si todos los pasos son 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 1 1` | `ci=verde` |
| `1 0 1` | `ci=rojo` |
| `1 1` | `ci=verde` |

## 📐 Algoritmo (pseudocódigo neutral)

El algoritmo es la traducción directa del AND lógico: leer los pasos y comprobar que *todos* valen 1.

```text
LEER pasos ; verde <- todos == 1
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

La versión de Python es la más transparente sobre lo que realmente ocurre. Lee todo stdin, lo parte por espacios y convierte cada token a entero mediante una comprensión de lista. La decisión vive en `all(p == 1 for p in pasos)`: `all` es la encarnación exacta del AND lógico —devuelve `True` solo si *cada* elemento cumple la condición— y, además, es perezoso, así que en cuanto encuentra el primer paso distinto de 1 deja de mirar. Ese cortocircuito es el mismo espíritu del `fail-fast` de un pipeline real. Ramalho, en *Fluent Python*, destaca `all`/`any` sobre expresiones generadoras como la manera pitónica de expresar cuantificadores sin escribir un bucle explícito.

```python
import sys

pasos = [int(x) for x in sys.stdin.read().split()]
print(f"ci={'verde' if all(p == 1 for p in pasos) else 'rojo'}")
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

Para `1 1 1`, `all` recorre los tres unos y devuelve `True`, así que imprime `ci=verde`. Para `1 0 1`, se detiene en el `0` y produce `ci=rojo`. Para `1 1`, dos unos, verde. Exactamente los tres casos del contrato.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

JavaScript expresa el mismo cuantificador con `Array.prototype.every`, que también cortocircuita en el primer elemento que no cumple. La diferencia idiomática está en la lectura: `readFileSync(0, ...)` lee el descriptor 0 (stdin) de una vez, y `split(/\s+/)` separa por cualquier bloque de espacios. Haverbeke, en *Eloquent JavaScript*, presenta `every`/`some` como los métodos de orden superior que capturan "para todos" y "existe" sin bucles manuales.

```javascript
import { readFileSync } from "node:fs";

const pasos = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

TypeScript es, aquí, JavaScript con la red del tipado estático: la única diferencia visible es la anotación `pasos: number[]`, que documenta y hace comprobable en tiempo de compilación que trabajamos con un arreglo de números. Cherny, en *Programming TypeScript*, defiende justo este valor: los tipos son una forma de prueba que se ejecuta antes de correr el programa, otra capa de verificación temprana muy en el espíritu de la CI.

```typescript
import { readFileSync } from "node:fs";

const pasos: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
```

🧬 **El mismo programa en la familia JavaScript / web:** [Dart · ActionScript](primos.md#javascript-web)

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

Rust muestra un contraste instructivo: su iterador `.all(...)` también es perezoso y cortocircuita, pero el `parse::<i64>()` devuelve un `Result` que aquí se resuelve con `unwrap()`. En un pipeline real, ese `unwrap` sobre una entrada malformada sería justo el tipo de fallo que pone la celda de Rust en rojo —una lección viva sobre por qué la CI existe—. Klabnik y Nichols, en *The Rust Programming Language*, insisten en que el sistema de tipos te obliga a *decidir* qué hacer con el error, aunque `unwrap` sea el atajo de "confío en la entrada".

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let verde = s.split_whitespace().all(|x| x.parse::<i64>().unwrap() == 1);
    println!("ci={}", if verde { "verde" } else { "rojo" });
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

Java resuelve el AND de la forma más elemental y quizá más didáctica: un booleano `verde` que empieza en `true` y se apaga irrevocablemente si *algún* paso no es 1. No cortocircuita (recorre todos los tokens), pero el resultado es idéntico. Es la traducción literal de "todos deben pasar": una sola falla contamina el conjunto. Bloch, en *Effective Java*, recomendaría en código de producción `Arrays.stream(...).allMatch(...)` para expresar la intención con un cuantificador, pero la versión con bucle deja el AND completamente a la vista.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean verde = true;
        for (String s : p) if (Integer.parseInt(s) != 1) verde = false;
        System.out.println("ci=" + (verde ? "verde" : "rojo"));
    }
}
```

🧬 **El mismo programa en la familia JVM:** [Kotlin · Scala · Groovy · Clojure](primos.md#jvm)

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

bool verde = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .All(x => int.Parse(x) == 1);
Console.WriteLine($"ci={(verde ? "verde" : "rojo")}");
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
	verde := true
	for _, s := range strings.Fields(line) {
		n, _ := strconv.Atoi(s)
		if n != 1 {
			verde = false
		}
	}
	res := "rojo"
	if verde {
		res = "verde"
	}
	fmt.Printf("ci=%s\n", res)
}
```

🧬 **El mismo programa en la familia Sistemas:** [Zig · Nim · D](primos.md#sistemas)

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long x;
    int verde = 1;
    while (scanf("%ld", &x) == 1) {
        if (x != 1) verde = 0;
    }
    printf("ci=%s\n", verde ? "verde" : "rojo");
    return 0;
}
```

🧬 **El mismo programa en la familia C / llaves:** [C++ · Objective-C](primos.md#c-llaves)

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: verde si el mínimo de los pasos es 1.
WITH pasos(x) AS (VALUES (1), (1), (1))
SELECT printf('ci=%s', CASE WHEN min(x) = 1 THEN 'verde' ELSE 'rojo' END) AS resultado FROM pasos;
```

🧬 **El mismo programa en la familia Lógica y declarativa:** [Prolog · Datalog](primos.md#logica-declarativa)

SQL merece una nota aparte: como es declarativo, no piensa en "recorrer y apagar un flag", sino en agregar. `min(x)` sobre una columna de ceros y unos vale 1 solo si *no hay ningún cero*; en cuanto aparece un cero, el mínimo cae a 0. Es una forma algebraica y elegante de expresar el mismo AND: verde ⇔ mínimo = 1. Date, en *SQL and Relational Theory*, subraya justo esto: en el modelo relacional razonas sobre conjuntos y agregados, no sobre iteraciones paso a paso.

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$pasos = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$verde = !in_array(0, $pasos, true);
echo "ci=" . ($verde ? "verde" : "rojo") . "\n";
```

🧬 **El mismo programa en la familia Scripting dinámico:** [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

Más allá de este ejercicio, cada lenguaje del núcleo trae su propio ecosistema de CI: el "paso de test" concreto que corre el pipeline cambia radicalmente de uno a otro, y conocerlos es parte de trabajar en un repo políglota.

| Lenguaje | Runner de test | Gestor / paquetes | Qué se cachea en CI |
|---|---|---|---|
| Python | `pytest` | pip / Poetry (`poetry.lock`) | `~/.cache/pip`, venv |
| JavaScript/TS | Jest o Vitest | npm / pnpm (`*-lock`) | `node_modules`, store de pnpm |
| Java | JUnit | Maven / Gradle | `~/.m2`, caché de Gradle |
| C# | xUnit | NuGet | `~/.nuget/packages` |
| Go | `go test` | go modules (`go.sum`) | caché de módulos y build |
| Rust | `cargo test` | Cargo (`Cargo.lock`) | `~/.cargo`, `target/` |
| C | CTest / a mano | Make / CMake | objetos compilados |
| SQL | asserts en scripts | — | — |
| PHP | PHPUnit | Composer (`composer.lock`) | caché de Composer |

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `all`/`every`/`allMatch` frente a bucle con flag booleano. |
| Semántica | Basta un paso en rojo para que el pipeline falle (AND). |
| Paradigmática | SQL usa `min` como agregado en lugar de recorrer. |

## 🧬 El concepto en la familia

El AND que decide verde/rojo aparece idéntico en cada servidor de CI. GitHub Actions expresa la matriz con `strategy.matrix` y el `fail-fast` con `strategy.fail-fast`; GitLab CI encadena `stages`; Jenkins modela `pipeline { stages { ... } }`. En todos, el veredicto global es la conjunción de los pasos, y en todos existe la misma tentación humana —ignorar el rojo— y la misma cura: tratar la rama principal como sagrada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 147
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el rojo del CI** → causa: integrar código roto porque "es urgente" → solución: no fusionar hasta que esté verde; el rojo es una alarma, no una sugerencia.
- **Pipelines lentísimos** → causa: sin caché ni paralelismo, el equipo empieza a saltárselos → solución: cachear dependencias y correr la matriz en paralelo.
- **Confundir verde con "correcto"** → causa: pruebas débiles que pasan aunque el código esté mal → solución: la CI solo es tan buena como las pruebas que ejecuta.

## ❓ Preguntas frecuentes

- **¿Qué pasos debe tener un pipeline?** Como mínimo compilar, probar y pasar el linter; según el proyecto, también análisis de seguridad, cobertura o construcción de artefactos.
- **¿CI y CD son lo mismo?** No. CI *verifica* cada cambio (esta clase). CD —entrega/despliegue continuos— automatiza publicar lo que ya está verde (clase 148).
- **¿Por qué usar una matriz por lenguaje?** Para garantizar que el mismo contrato se cumple en todos los entornos soportados, y detectar la incompatibilidad exacta —esa versión, ese lenguaje— sin adivinar.

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

> [⏮️ Clase 146](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 148 ⏭️](../../parte-9-ingenieria-de-software-poliglota/148-entrega-y-despliegue/README.md)
