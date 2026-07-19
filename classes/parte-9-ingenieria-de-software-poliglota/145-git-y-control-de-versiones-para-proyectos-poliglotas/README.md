# Clase 145 — Git y control de versiones para proyectos políglotas

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Hunt y Thomas, en *The Pragmatic Programmer*, cuentan que su primer consejo a cualquier equipo es poner todo bajo control de versiones —incluso las notas y la configuración— porque el sistema de versiones es la *red de seguridad* que permite experimentar sin miedo: si algo sale mal, siempre hay un estado bueno al que volver. Esta clase toma esa idea y la lleva al terreno políglota, donde un mismo repositorio alberga Python, Go, Java, Rust y más, cada uno con sus artefactos de compilación y su ruido particular. El reto no es usar Git —eso se aprende rápido—, sino usarlo *bien* en un monorepo con diez ecosistemas conviviendo.

El historial de Git es una secuencia de **commits**: instantáneas del proyecto, cada una con su mensaje, encadenadas de forma que puedes recorrer el pasado, ver quién cambió qué y volver atrás con precisión quirúrgica. El laboratorio destila esta estructura a su operación más elemental —contar los commits de un historial— porque contar es lo que hace por dentro cualquier herramienta que resume la actividad de un repositorio (`git rev-list --count`, las gráficas de contribuciones, los informes de release). Sobre ese esqueleto mínimo montaremos las decisiones que de verdad importan: qué versionar, qué ignorar y cómo dividir el trabajo en commits legibles.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Contar** los commits de un historial dado.
2. **Explicar** qué es un commit y por qué el historial es una red de seguridad.
3. **Diseñar** un `.gitignore` que excluya los artefactos de build de varios lenguajes.
4. **Argumentar** cuándo conviene un monorepo y cuándo submódulos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Commit atómico | Un cambio coherente por commit: historial legible |
| 2 | Historial como red de seguridad | Volver atrás sin miedo a experimentar |
| 3 | `.gitignore` por lenguaje | No versionar `__pycache__`, `target/`, `node_modules/`… |
| 4 | Monorepo vs. submódulos | Cómo organizar varios lenguajes en un repositorio |

## 📖 Definiciones y características

**Git.** Un sistema de control de versiones distribuido: cada copia clonada contiene el historial completo, no un fragmento. Esto es lo que lo hace robusto —no hay un servidor central del que dependa todo— y lo que permite trabajar sin conexión y ramificar con coste casi nulo. Para Hunt y Thomas esta ubicuidad del historial es la esencia de la red de seguridad.

**Commit atómico.** Un commit registra una instantánea del proyecto con un mensaje. La virtud que se persigue es la *atomicidad*: cada commit debe capturar un único cambio coherente y funcional, de modo que su mensaje lo describa con una frase y pueda revertirse aislado. Un commit que mezcla un arreglo de un bug con un reformateo masivo es imposible de revisar y de deshacer limpiamente.

**`.gitignore`.** El archivo que le dice a Git qué no seguir. En un proyecto políglota es crítico: cada lenguaje genera artefactos que jamás deben versionarse (`__pycache__/` y `*.pyc` en Python, `target/` en Rust y Java, `node_modules/` en JavaScript, binarios compilados en Go y C). Versionarlos ensucia el repositorio, provoca conflictos absurdos e infla el clon.

## 🧩 Situación

Trabajas en un monorepo que combina un backend en Go, scripts en Python y una interfaz en TypeScript. Un compañero, sin `.gitignore` adecuado, comitea por error su carpeta `node_modules/` y los binarios de `go build`: el repositorio pasa de unos megabytes a cientos, cada `git status` se llena de ruido y los merges empiezan a chocar en archivos generados que a nadie le importan. La disciplina que evita este desastre tiene tres patas: un `.gitignore` con secciones por lenguaje, commits atómicos con mensajes claros, y la regla de oro de no versionar nunca lo que la build puede regenerar. Antes de todo eso, conviene entender la operación básica sobre el historial —contarlo— que implementa el laboratorio.

## 🧮 Modelo

- **Entrada** (stdin): una línea con mensajes de commit (palabras separadas por espacio)
- **Salida** (stdout): `commits=<cantidad>`
- **Regla:** contar los mensajes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `fix add refactor` | `commits=3` |
| `init` | `commits=1` |
| `a b c d` | `commits=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER mensajes ; ESCRIBIR cantidad
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). El contrato: leer mensajes de commit separados por espacio y escribir `commits=<cantidad>`. Con `fix add refactor` sale `commits=3`; con `init`, `commits=1`.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

msgs = sys.stdin.read().split()
print(f"commits={len(msgs)}")
```

La solución de Python es casi telegráfica y por eso ilustra bien la operación. `sys.stdin.read().split()` lee toda la entrada y la trocea por espacios en una lista de tokens; `len(...)` cuenta cuántos hay. Cada token representa un commit, así que su longitud es el número de commits del historial —exactamente lo que devuelve `git rev-list --count HEAD` sobre un repositorio real. Que `.split()` sin argumentos colapse múltiples espacios es una comodidad deliberada: hace que un historial con separación irregular se cuente igual de bien, sin tokens vacíos que inflen el resultado.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const msgs = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const msgs: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] msgs = br.readLine().trim().split("\\s+");
        System.out.println("commits=" + msgs.length);
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] msgs = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"commits={msgs.Length}");
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
	msgs := strings.Fields(line)
	fmt.Printf("commits=%d\n", len(msgs))
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n = s.split_whitespace().count();
    println!("commits={n}");
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    char tok[256];
    int c = 0;
    while (scanf("%255s", tok) == 1) c++;
    printf("commits=%d\n", c);
    return 0;
}
```

El contraste entre C y SQL revela dos formas de «contar». C no construye ninguna colección: lee token a token con `scanf("%255s", ...)` —el límite `255` es una defensa consciente contra el desbordamiento del buffer, tan característica del rigor de Kernighan y Ritchie— e incrementa un contador. SQL, en cambio, modela los commits como filas de una tabla y aplica `count(*)`: la operación de contar es primitiva en el modelo relacional que describe Date en *SQL and Relational Theory*, porque una relación es un conjunto de tuplas y su cardinalidad es un dato de primera clase. Ambos llegan al mismo número por caminos conceptualmente opuestos: uno imperativo y byte a byte, otro declarativo y sobre conjuntos.

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: cuenta las filas (commits).
WITH commits(msg) AS (VALUES ('fix'), ('add'), ('refactor'))
SELECT printf('commits=%d', count(*)) AS resultado FROM commits;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
$msgs = preg_split('/\s+/', trim(fgets(STDIN)));
echo "commits=" . count($msgs) . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El conteo es idéntico; lo que cambia entre lenguajes es qué artefactos de build hay que excluir del control de versiones. Un `.gitignore` de monorepo políglota necesita una sección por ecosistema.

| Lenguaje | Qué NO versionar (ejemplos) |
|---|---|
| Python | `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `*.egg-info/` |
| JavaScript / TypeScript | `node_modules/`, `dist/`, `*.tsbuildinfo` |
| Java | `target/`, `build/`, `*.class` |
| C# | `bin/`, `obj/` |
| Go | binarios compilados, `*.exe` |
| Rust | `target/` |
| C | `*.o`, `*.a`, binarios |
| SQL | dumps y `.db` locales |
| PHP | `vendor/` |

Nota transversal: lo que sí se versiona en todos es el **lockfile** (clase 143), porque forma parte del código fuente reproducible; lo que nunca se versiona es la carpeta de dependencias descargadas (`node_modules/`, `vendor/`, `.venv/`), porque se regenera desde el lock. Distinguir ambas cosas es la decisión más frecuente y más mal resuelta en repositorios políglotas.

## 🧬 El concepto en la familia

Git domina, pero el modelo de instantáneas versionadas encadenadas por un hash lo comparten Mercurial y, en otro nivel, sistemas como Fossil o Pijul. La gran decisión de arquitectura en proyectos con varios lenguajes es **monorepo vs. submódulos**: el monorepo mantiene todo en un solo historial —commits atómicos que cruzan lenguajes, un único punto de verdad— a costa de un repositorio grande; los submódulos (o `git subtree`) enlazan repositorios independientes, útil cuando cada componente tiene su propio ciclo de vida pero más frágil a la hora de coordinar cambios. Este curso mismo es un monorepo políglota, y su `.gitignore` es exactamente del tipo que describe la tabla anterior.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 145
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Commits gigantes que mezclan cosas.** Un commit que junta un arreglo, un reformateo y una feature nueva es imposible de revisar y de revertir. Haz commits atómicos: un cambio coherente por commit, con un mensaje que lo describa.
- **Versionar artefactos de build.** Comitear `node_modules/`, `target/` o binarios infla el repositorio y genera conflictos absurdos. Añádelos al `.gitignore` desde el primer día.
- **Ignorar el lockfile por error.** Es el reverso del punto anterior: el lockfile sí se versiona. Un `.gitignore` demasiado agresivo que excluya `package-lock.json` rompe la reproducibilidad.
- **Confundir monorepo con «un cajón de sastre».** Un monorepo necesita estructura clara por lenguaje; sin ella, la ventaja de tener todo junto se convierte en caos.

## ❓ Preguntas frecuentes

- **¿Cada cuánto debo commitear?** Cuando tienes un cambio coherente y funcional que se puede describir en una línea. Mejor muchos commits pequeños que uno enorme.
- **¿Git sirve solo para código?** No: versiona cualquier texto —documentación, configuración, infraestructura como código—. Hunt y Thomas recomiendan poner bajo control de versiones todo lo que importe.
- **¿Monorepo o submódulos para varios lenguajes?** Monorepo si los componentes cambian juntos y quieres commits atómicos que los crucen; submódulos si cada uno tiene su propio ciclo de vida y equipo.

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

> [⏮️ Clase 144](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 146 ⏭️](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md)
