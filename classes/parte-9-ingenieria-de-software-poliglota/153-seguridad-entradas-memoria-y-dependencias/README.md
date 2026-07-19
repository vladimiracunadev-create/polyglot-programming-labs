# Clase 153 — Seguridad: entradas, memoria y dependencias

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

La seguridad del software no es una capa que se añade al final: es una postura que se adopta desde la primera línea. McConnell la llama, en *Code Complete*, **programación defensiva**: escribir cada rutina como si el mundo exterior fuera hostil, porque a menudo lo es. Su principio rector es simple y radical: **desconfía de toda entrada**. Datos que vienen de un usuario, de un archivo, de la red o de otro subsistema deben validarse en la frontera antes de tocar la lógica. Hunt y Thomas lo formulan como los contratos y las aserciones de *The Pragmatic Programmer*: define qué es una entrada válida y rechaza todo lo demás en la puerta.

Esta clase ataca tres frentes de la seguridad que atraviesan todos los lenguajes. El primero es la **validación de entradas**, y el ejercicio la ilustra de forma mínima: comprobar que una cadena es puramente alfanumérica. Parece trivial, pero es la defensa que detiene una familia entera de ataques —la **inyección**—, donde un dato como `'; DROP TABLE usuarios; --` deja de ser un nombre y se convierte en un comando que la base de datos ejecuta. El segundo frente es la **seguridad de memoria**, donde los lenguajes divergen radicalmente: la gestión manual de C, propensa a desbordamientos y *use-after-free*; la recolección de basura de Java, Python o Go; y el *ownership* de Rust, que previene esos fallos en tiempo de compilación. El tercero es la **auditoría de dependencias**: hoy tu código es una fracción pequeña del software que despliegas, y una vulnerabilidad en una biblioteca ajena es tu problema.

La lección de fondo: validar una entrada alfanumérica es un gesto pequeño que enseña un hábito grande. La lista blanca —permitir solo lo conocido-bueno— es la doctrina que McConnell defiende frente a la lista negra, siempre incompleta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Validar** una entrada contra un conjunto permitido (lista blanca) y explicar por qué supera a la lista negra.
2. **Explicar** cómo la validación de entradas frena la inyección (SQL, shell) y por qué las consultas parametrizadas son la defensa real.
3. **Contrastar** los tres modelos de seguridad de memoria: manual (C), recolección de basura y *ownership* (Rust).
4. **Nombrar** las herramientas de auditoría de dependencias de cada ecosistema.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Validación de entrada | Primera defensa; no confiar en lo externo |
| 2 | Inyección | Datos que el sistema interpreta como comandos |
| 3 | Seguridad de memoria | Manual vs. GC vs. ownership: modelos muy distintos |
| 4 | Auditoría de dependencias | Tu superficie de ataque incluye el código ajeno |

## 📖 Definiciones y características

La **validación de entrada** comprueba que un dato cumple lo esperado *antes* de usarlo. La elección clave es entre **lista blanca** y **lista negra**: la lista negra intenta enumerar lo peligroso (`'`, `;`, `--`…) y siempre olvida un caso; la lista blanca define lo permitido (aquí, solo letras y dígitos) y rechaza todo lo demás por defecto. McConnell es tajante: prefiere siempre la lista blanca, porque su modo de fallo es rechazar algo válido —molesto pero seguro—, mientras que el de la lista negra es aceptar algo malicioso.

El **saneamiento** (*sanitization*) transforma o escapa datos peligrosos para neutralizarlos; la **inyección** es lo que ocurre cuando no se hace: un dato cruza la frontera entre «datos» y «código». La inyección SQL, la de comandos de shell y el cross-site scripting son variantes del mismo error. La defensa correcta rara vez es filtrar caracteres a mano: es **separar código de datos** mediante consultas parametrizadas (*prepared statements*), donde la base de datos recibe la plantilla y los valores por canales distintos y nunca confunde uno con otro. Date lo defiende en *SQL and Relational Theory*: los parámetros son valores, no fragmentos de texto que se concatenan.

La **seguridad de memoria** es el eje donde los lenguajes más se separan. En C, tú reservas y liberas: un índice fuera de rango (*buffer overflow*), usar memoria ya liberada (*use-after-free*) o liberar dos veces son bugs que se convierten en vulnerabilidades explotables. La **recolección de basura** (Java, C#, Python, Go, JS, PHP) elimina esa clase de errores automatizando la liberación, a costa de pausas y sobrecarga. El **ownership** de Rust logra seguridad de memoria *sin* recolector: el compilador rastrea quién posee cada dato y cuándo muere, y rechaza en compilación el código que podría causar un *data race* o un *use-after-free*.

## 🧩 Situación

Un formulario de registro tiene un campo «nombre de usuario». Un atacante escribe `admin'; DROP TABLE usuarios; --`. Si tu backend construye la consulta concatenando texto —`"SELECT * FROM usuarios WHERE nombre = '" + entrada + "'"`—, la comilla cierra la cadena y el `DROP TABLE` se ejecuta: adiós tabla. Dos defensas actúan en capas. En la frontera, validas que el nombre sea alfanumérico y rechazas la entrada antes de que llegue a ninguna parte. En la base de datos, usas una consulta parametrizada, de modo que aunque un dato raro pase la validación, jamás se interprete como SQL. El ejercicio de esta clase —`seguro=true` solo si la cadena es alfanumérica— es esa primera capa reducida a su esencia.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (entrada a validar)
- **Salida** (stdout): `seguro=<true|false>` (true si es alfanumérica)
- **Regla:** seguro si todos los caracteres son letras o dígitos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `abc` | `seguro=true` |
| `a;b` | `seguro=false` |
| `hola123` | `seguro=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER entrada ; seguro <- todos los caracteres alfanuméricos
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

Python ofrece la validación más directa: el método de cadena `str.isalnum()` devuelve `True` solo si la cadena no está vacía y todos sus caracteres son alfanuméricos. Es la lista blanca hecha primitiva del lenguaje. Un matiz que Ramalho subrayaría en *Fluent Python*: `isalnum()` es consciente de Unicode, así que `"café2".isalnum()` es `True` —la `é` cuenta como letra—. Para la seguridad esto puede ser deseable o no; si necesitas ASCII estricto, la comprobación debe ser explícita. La auditoría de dependencias en el ecosistema Python se hace con `pip-audit`, que contrasta tus paquetes contra la base de vulnerabilidades de la PyPA.

```python
import sys

w = sys.stdin.readline().strip()
seguro = w.isalnum()
print(f"seguro={'true' if seguro else 'false'}")
```

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const w = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

Tanto JavaScript como TypeScript expresan la lista blanca con una expresión regular anclada: `^[A-Za-z0-9]+$`. Los anclajes `^` y `$` son de seguridad crítica —sin ellos, la regex encontraría una coincidencia *parcial* y aceptaría `a;b` porque contiene una `a`—. El `+` exige al menos un carácter, replicando el rechazo de la cadena vacía. En estos ecosistemas la auditoría es `npm audit` (o `pnpm audit`), que revisa el árbol de dependencias del `package-lock.json`/`pnpm-lock.yaml` contra los avisos de seguridad del registro.

```typescript
import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
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
        boolean seguro = w.matches("[A-Za-z0-9]+");
        System.out.println("seguro=" + (seguro ? "true" : "false"));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool seguro = w.Length > 0 && w.All(char.IsLetterOrDigit);
Console.WriteLine($"seguro={(seguro ? "true" : "false")}");
```

### Go · [`go/main.go`](implementaciones/go/main.go) · `go run main.go`

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"unicode"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	seguro := len(w) > 0
	for _, c := range w {
		if !unicode.IsLetter(c) && !unicode.IsDigit(c) {
			seguro = false
		}
	}
	res := "false"
	if seguro {
		res = "true"
	}
	fmt.Printf("seguro=%s\n", res)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

Rust es el lenguaje que mejor encarna la lección de seguridad de esta clase, y no por la validación en sí —`chars().all(|c| c.is_ascii_alphanumeric())` es un iterador limpio— sino por lo que representa. Klabnik y Nichols dedican *The Rust Programming Language* a explicar el *ownership*: el compilador garantiza que esta cadena `s` se libere exactamente una vez, que ninguna referencia la sobreviva y que no haya acceso concurrente sin sincronizar. Toda una categoría de vulnerabilidades —las de memoria, que Microsoft y Google estiman en torno al 70 % de sus CVE críticos— desaparece por construcción. Fíjate además en `is_ascii_alphanumeric`, que a diferencia del `isalnum` de Python restringe a ASCII: aquí la decisión Unicode es explícita. La auditoría de dependencias se hace con `cargo audit`, contra la base RustSec.

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let seguro = !w.is_empty() && w.chars().all(|c| c.is_ascii_alphanumeric());
    println!("seguro={}", if seguro { "true" } else { "false" });
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

C muestra el otro polo del espectro de memoria. Observa `char w[256]` y `scanf("%255s", w)`: el `255` no es decorativo, es la defensa. Sin ese límite, una entrada más larga que el búfer lo desbordaría, sobrescribiendo memoria adyacente —el clásico *buffer overflow*, base histórica de innumerables exploits. Kernighan y Ritchie enseñan en *The C Programming Language* que en C la seguridad de memoria es responsabilidad del programador en cada línea: no hay red. El `isalnum` de `<ctype.h>` valida cada carácter, con la sutileza de convertir a `unsigned char` para evitar comportamiento indefinido con bytes altos. Herramientas como `valgrind` y los *sanitizers* (`-fsanitize=address`) ayudan a cazar estos fallos en pruebas.

```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int seguro = 1;
    for (int i = 0; w[i]; i++) {
        if (!isalnum((unsigned char) w[i])) seguro = 0;
    }
    printf("seguro=%s\n", seguro ? "true" : "false");
    return 0;
}
```

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: se evita la inyección con consultas parametrizadas; aquí, validación por patrón.
WITH t(w) AS (VALUES ('abc'))
SELECT printf('seguro=%s', CASE WHEN w GLOB '*[^A-Za-z0-9]*' THEN 'false' ELSE 'true' END) AS resultado FROM t;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$w = trim(fgets(STDIN));
$seguro = ctype_alnum($w);
echo "seguro=" . ($seguro ? "true" : "false") . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Aspecto | Observación entre lenguajes |
|---|---|
| Validación alfanumérica | `isalnum` (Python, PHP `ctype_alnum`, C `<ctype.h>`); regex anclada (JS, TS, Java); `char.IsLetterOrDigit` (C#); `unicode`/`is_ascii_alphanumeric` (Go, Rust) |
| Unicode vs. ASCII | Python `isalnum` acepta letras acentuadas; Rust `is_ascii_alphanumeric` restringe a ASCII; decisión de seguridad explícita |
| Seguridad de memoria | Manual (C); recolección de basura (Java, C#, Python, Go, JS, PHP); ownership en compilación (Rust) |
| Auditoría de dependencias | `pip-audit` (Python), `npm/pnpm audit` (JS/TS), `cargo audit` (Rust), OWASP Dependency-Check y `mvn`/Gradle plugins (Java), `dotnet list package --vulnerable` (C#), `govulncheck` (Go), `composer audit` (PHP) |
| Defensa contra inyección | Consultas parametrizadas en todos los conectores; SQL las provee de forma nativa |

El proyecto **OWASP** (con su lista *Top Ten* y herramientas como Dependency-Check y ZAP) es la referencia transversal: describe estas mismas familias de riesgo con independencia del lenguaje.

## 🧬 El concepto en la familia

La validación de entradas y la separación código/datos reaparecen en cada frontera del software. En la web, el *escaping* de HTML frena el XSS; las cabeceras *Content-Security-Policy* limitan qué scripts se ejecutan. En la línea de comandos, no pasar la entrada del usuario a `system()` sin escapar frena la inyección de comandos. En la cadena de suministro, firmar y fijar (*pin*) versiones de dependencias con un *lockfile*, y auditar con las herramientas anteriores, frena los ataques de *typosquatting* y las bibliotecas comprometidas —una amenaza que ha crecido tanto que hoy es una categoría propia del OWASP Top Ten. El hilo común es el de McConnell: la seguridad es programación defensiva aplicada en cada límite del sistema.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 153
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en la entrada del usuario** → causa: inyecciones y corrupción de datos → solución: validar y sanear en la frontera, siempre (McConnell: programación defensiva)
- **Lista negra en vez de blanca** → causa: siempre olvidas un carácter peligroso → solución: permite solo lo conocido-bueno (lista blanca) y rechaza el resto
- **Escapar a mano en vez de parametrizar** → causa: cada base de datos escapa distinto y es fácil errar → solución: usa consultas parametrizadas, que separan código de datos
- **Ignorar las dependencias** → causa: una CVE en una biblioteca ajena es tu vulnerabilidad → solución: fija versiones con lockfile y audita con `pip-audit`/`npm audit`/`cargo audit`
- **Buffer sin límite en C** → causa: `scanf("%s")` sin ancho desborda → solución: fija siempre el ancho (`%255s`) y usa sanitizers en pruebas

## ❓ Preguntas frecuentes

- **¿Validar en cliente o en servidor?** En ambos, pero la del servidor es la única que cuenta para la seguridad: el cliente puede saltarse.
- **¿Cómo evito la inyección SQL de raíz?** Con consultas parametrizadas, nunca concatenando la entrada en el texto de la consulta. La validación es una capa extra, no el sustituto.
- **¿Por qué se habla tanto de Rust en seguridad?** Porque su modelo de *ownership* elimina en compilación los fallos de memoria (buffer overflow, use-after-free), que son el origen de la mayoría de las vulnerabilidades críticas en C y C++.
- **¿Basta con auditar una vez?** No: aparecen CVE nuevas constantemente. La auditoría de dependencias debe correr en integración continua, no una sola vez.

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

> [⏮️ Clase 152](../../parte-9-ingenieria-de-software-poliglota/152-rendimiento-y-perfilado-profiling/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 154 ⏭️](../../parte-9-ingenieria-de-software-poliglota/154-mantenibilidad-documentacion-y-deuda-tecnica/README.md)
