# Clase 146 — Revisión de código y estándares

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

McConnell dedica en *Code Complete* uno de sus argumentos más contundentes a las **inspecciones de código**: los datos que recopila muestran que revisar el código a conciencia detecta una fracción altísima de los defectos —a menudo más que las pruebas— y que hacerlo temprano es órdenes de magnitud más barato que arreglar el mismo error en producción. Fowler, en la práctica moderna del *pull request*, convirtió esa inspección en un ritual cotidiano: casi ningún cambio entra a la rama principal sin que otro par de ojos lo apruebe. Esta clase trata de esa disciplina y de su brazo automático, el **linter**, que descarga a los revisores de lo mecánico para que se concentren en lo que exige criterio.

La idea es sencilla de enunciar y profunda en sus consecuencias: un equipo acuerda un **estándar** —cómo se nombran las cosas, cómo se formatea el código— y delega su cumplimiento en herramientas, reservando la revisión humana para el diseño, la corrección y la legibilidad. El laboratorio modela la parte automatizable con la regla más simple imaginable: validar que un identificador esté todo en minúsculas, tal como una regla de un linter marcaría `Total` como violación de un estilo que exige `total`. Es un juguete, pero encierra el mecanismo real: una regla objetiva, aplicada sin discusión, uniforme para todos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Validar** automáticamente una convención de nombres sobre un identificador.
2. **Explicar** qué separa a un linter de un formateador y qué aporta cada uno.
3. **Distinguir** lo que automatiza el linter de lo que aporta la revisión humana.
4. **Emparejar** cada lenguaje del núcleo con sus linters y formateadores estándar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estándar de estilo | Reglas compartidas: PEP 8, Effective Java, gofmt |
| 2 | Linter vs. formateador | Detectar problemas vs. normalizar el formato |
| 3 | Revisión de código | El criterio humano que la máquina no da |
| 4 | Inspecciones (McConnell) | Detectan defectos temprano y barato |

## 📖 Definiciones y características

**Estándar de código.** Un conjunto de convenciones acordadas —nombres, indentación, orden de imports— que un equipo adopta para que el código se lea como si lo hubiera escrito una sola persona. Guías como PEP 8 en Python, las recomendaciones de Bloch en *Effective Java* o el formato canónico de `gofmt` cumplen este papel. El valor no está en qué regla concreta se elige, sino en que todos sigan la misma.

**Linter y formateador.** Conviene separarlos. El **formateador** (black, prettier, gofmt, rustfmt, `dotnet format`) reescribe el código a una forma canónica —no opina sobre corrección, solo sobre apariencia—. El **linter** (ruff, eslint, `go vet`, clippy, checkstyle, phpcs) va más allá: detecta violaciones de estilo *y* errores probables, como una variable sin usar o una comparación sospechosa. El linter automatiza justo lo que McConnell llama la parte mecánica de la inspección.

**Revisión de código.** Otra persona lee el cambio antes de integrarlo. Su valor es doble: mejora la calidad —encuentra defectos que ninguna herramienta ve, como un diseño equivocado— y difunde conocimiento por el equipo. Fowler insiste en que la revisión debe ser sobre lo que importa; por eso conviene que el linter ya haya resuelto el formato antes de que un humano mire.

## 🧩 Situación

En la revisión de un pull request, medio equipo discute si una variable debería llamarse `Total` o `total`, y el hilo se llena de comentarios sobre mayúsculas mientras el diseño real del cambio pasa desapercibido. Es el peor uso posible del tiempo de revisión. La solución que propone la ingeniería moderna es sacar esa clase de decisiones de la conversación humana: se codifican en un linter que las aplica automáticamente en cada commit, de modo que `Total` se marca (o se corrige) sin que nadie tenga que opinar. Así la revisión humana queda libre para lo que solo ella puede juzgar. El laboratorio implementa exactamente esa regla automatizable: minúsculas sí, minúsculas no.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (identificador, solo letras)
- **Salida** (stdout): `valido=<true|false>` (true si está todo en minúsculas)
- **Regla:** valido si todos los caracteres son minúsculas

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `total` | `valido=true` |
| `Total` | `valido=false` |
| `abc` | `valido=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER palabra ; valido <- todos los caracteres en minúscula
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). El contrato: leer una palabra y escribir `valido=true` si está toda en minúsculas, `valido=false` en caso contrario. Con `total` sale `valido=true`; con `Total`, `valido=false`.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

w = sys.stdin.readline().strip()
valido = all("a" <= c <= "z" for c in w)
print(f"valido={'true' if valido else 'false'}")
```

La versión de Python expresa la regla de forma casi verbal. `all("a" <= c <= "z" for c in w)` recorre cada carácter y comprueba que caiga en el rango de minúsculas ASCII; `all(...)` devuelve `True` solo si *todos* cumplen, que es exactamente la semántica de una regla de estilo: una sola violación invalida el identificador. La comparación encadenada `"a" <= c <= "z"` es una construcción que Ramalho destaca en *Fluent Python* como más legible que el `c >= "a" and c <= "z"` de otros lenguajes. El generador dentro de `all` es perezoso: en cuanto encuentra una mayúscula deja de evaluar, igual que un linter que reporta el primer fallo sin recorrer lo que ya sabe que está mal.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        boolean valido = w.matches("[a-z]+");
        System.out.println("valido=" + (valido ? "true" : "false"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool valido = w.Length > 0 && w.All(c => c >= 'a' && c <= 'z');
Console.WriteLine($"valido={(valido ? "true" : "false")}");
```

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
	w := strings.TrimSpace(line)
	valido := len(w) > 0
	for _, c := range w {
		if c < 'a' || c > 'z' {
			valido = false
		}
	}
	res := "false"
	if valido {
		res = "true"
	}
	fmt.Printf("valido=%s\n", res)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let valido = !w.is_empty() && w.chars().all(|c| c.is_ascii_lowercase());
    println!("valido={}", if valido { "true" } else { "false" });
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int valido = 1;
    for (int i = 0; w[i]; i++) {
        if (w[i] < 'a' || w[i] > 'z') valido = 0;
    }
    printf("valido=%s\n", valido ? "true" : "false");
    return 0;
}
```

Aquí aflora una división estilística que también existe entre linters reales. JavaScript, TypeScript, Java y PHP expresan la regla como una **expresión regular**, `/^[a-z]+$/`: una descripción declarativa del patrón «una o más minúsculas, nada más». C, Go y Rust prefieren el **recorrido carácter a carácter** con una comparación de rangos. Ambos enfoques son legítimos y la elección refleja el idioma de cada comunidad —un revisor no debería objetar ninguno—. Fíjate además en un detalle de corrección compartido: C recorre hasta el terminador nulo `w[i]`, mientras Rust y C# añaden `!w.is_empty()` / `w.Length > 0` para tratar la cadena vacía, que sin ese guardo daría `valido=true` de forma engañosa. Son exactamente las decisiones de borde que un buen linter, o un buen revisor humano, no dejan pasar.

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: compara con la versión en minúsculas.
WITH t(w) AS (VALUES ('total'))
SELECT printf('valido=%s', CASE WHEN w = lower(w) THEN 'true' ELSE 'false' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
$valido = preg_match('/^[a-z]+$/', $w) === 1;
echo "valido=" . ($valido ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

La regla es la misma; lo que cambia en la práctica es el ecosistema de herramientas que cada lenguaje usa para aplicarla. Esta tabla es la referencia útil para montar la calidad de un proyecto políglota.

| Lenguaje | Linter | Formateador | Guía de estilo |
|---|---|---|---|
| Python | ruff, flake8, pylint | black, ruff format | PEP 8 |
| JavaScript / TypeScript | eslint | prettier | Airbnb, Standard |
| Java | checkstyle, SpotBugs | google-java-format | *Effective Java* (Bloch) |
| C# | analizadores de Roslyn | `dotnet format` | convenciones de .NET |
| Go | `go vet`, staticcheck | `gofmt` | formato canónico de Go |
| Rust | clippy | rustfmt | guía de estilo de Rust |
| C | clang-tidy, cppcheck | clang-format | estilos (K&R, LLVM…) |
| SQL | sqlfluff | sqlfluff fix | según convención del equipo |
| PHP | phpcs, PHPStan | php-cs-fixer | PSR-12 |

Dos observaciones. Primera: Go es el caso extremo —`gofmt` no es configurable a propósito, para eliminar de raíz cualquier discusión sobre formato—, mientras que Python o JavaScript ofrecen mucha configuración y por eso el equipo debe fijar la suya y versionarla. Segunda: conviene separar linter de formateador y ejecutar ambos en CI y en un *pre-commit hook*, de modo que el código llegue a la revisión humana ya normalizado, tal como recomienda la práctica que popularizó Fowler.

## 🧬 El concepto en la familia

La automatización del estilo es hoy universal: ruff en Python, eslint/prettier en el mundo JavaScript, clippy y rustfmt en Rust, `gofmt`/`go vet` en Go, checkstyle en Java, `dotnet format` en C#, phpcs en PHP. Todas encarnan la misma idea de McConnell —externalizar lo mecánico de la inspección a una herramienta— para que la energía humana de la revisión se gaste donde de verdad rinde: en el diseño, la corrección lógica y la claridad. El linter es la primera línea; la revisión humana, la que exige criterio.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 146
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Discutir estilo en la revisión humana.** Si el equipo debate mayúsculas o indentación en cada pull request, está malgastando su recurso más caro. Delega el formato en un formateador y el estilo en un linter, y reserva la revisión para el criterio.
- **Ignorar los avisos del linter.** Un aviso desatendido suele ser un bug latente (variable sin usar, comparación errónea). Resuélvelo o justifícalo explícitamente con una supresión comentada, nunca por acumulación.
- **No versionar la configuración del linter.** Si cada quien usa sus reglas, el estándar deja de ser compartido. La configuración (`.eslintrc`, `pyproject.toml`, `.golangci.yml`) va en el repositorio.
- **Creer que el linter sustituye a la revisión.** El linter no juzga si el diseño es correcto ni si el código resuelve el problema; eso solo lo ve un humano. Son complementarios, no alternativas.

## ❓ Preguntas frecuentes

- **¿Linter o revisión humana?** Los dos: el linter automatiza lo mecánico y objetivo; la revisión humana aporta el criterio sobre diseño, corrección y legibilidad que ninguna herramienta da.
- **¿Linter o formateador?** También ambos: el formateador normaliza la apariencia sin opinar de corrección; el linter detecta además errores probables. Se ejecutan juntos en CI.
- **¿Por qué imponer un estándar?** Porque un código uniforme se lee y mantiene mucho mejor, y porque —como muestra McConnell— las inspecciones sobre código consistente detectan defectos antes y más barato.

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

> [⏮️ Clase 145](../../parte-9-ingenieria-de-software-poliglota/145-git-y-control-de-versiones-para-proyectos-poliglotas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 147 ⏭️](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md)
