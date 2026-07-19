# Clase 143 — Dependencias, versiones y lockfiles

> Parte **9 — Ingeniería de software políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ningún programa profesional se construye solo con el código que escribimos: descansa sobre decenas o cientos de dependencias de terceros, y cada una de ellas evoluciona a su propio ritmo. La pregunta central de esta clase es cómo mantener un proyecto estable cuando todo lo que hay debajo se mueve. La respuesta tiene dos piezas que hay que entender a fondo. La primera es el **versionado semántico** (SemVer): la convención `mayor.menor.parche` que convierte un simple número en un contrato de compatibilidad entre quien publica una librería y quien la consume. La segunda es el **lockfile**: el archivo que congela el árbol de dependencias resuelto para que la build sea reproducible, hoy y dentro de dos años, en tu máquina y en la de integración continua.

El ejercicio de esta clase es deliberadamente pequeño —descomponer `1.2.3` en sus tres números— porque el parseo es la operación mínima sobre la que se apoya todo lo demás. Un gestor de paquetes hace exactamente esto miles de veces al resolver un grafo: lee versiones, las compara según las reglas de SemVer y decide cuál instalar. Al implementarlo en diez lenguajes verás que la lógica es trivial; lo difícil, y lo que discute *The Pragmatic Programmer* de Hunt y Thomas bajo el principio DRY («Don't Repeat Yourself»), es no repetir esa decisión en cada máquina: se toma una vez, se escribe en el lockfile y se reutiliza. El lockfile es la forma más concreta de «no repetirse» sobre el entorno de ejecución.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Descomponer** una cadena `mayor.menor.parche` en sus tres componentes numéricos.
2. **Interpretar** qué compatibilidad promete cada número y qué implican los rangos `^` y `~`.
3. **Justificar** por qué un lockfile debe versionarse y qué garantiza en un build reproducible.
4. **Identificar** el lockfile de cada ecosistema del núcleo (npm, pip, Cargo, Go, Maven…).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | SemVer `mayor.menor.parche` | Un número que comunica riesgo de ruptura |
| 2 | Rangos `^` y `~` | Definen qué actualizaciones aceptas sin revisar |
| 3 | Lockfile | Congela el árbol resuelto: build reproducible |
| 4 | Lockfile por ecosistema | Cada lenguaje tiene el suyo y hay que versionarlo |

## 📖 Definiciones y características

**Versionado semántico (SemVer).** La especificación de SemVer fija que, dada una versión `MAYOR.MENOR.PARCHE`, se incrementa el **mayor** ante cambios incompatibles en la API, el **menor** al añadir funcionalidad de forma retrocompatible, y el **parche** al corregir errores sin cambiar la interfaz. Lo importante no es la aritmética sino el pacto: cuando un autor sube solo el parche, te está diciendo «puedes actualizar a ciegas». Cuando sube el mayor, te avisa de que algo que usabas dejó de funcionar. SemVer es, en el fondo, documentación ejecutable de la compatibilidad.

**Rangos (`^`, `~`).** Rara vez fijamos una versión exacta en el manifiesto; declaramos un rango. El cursor (`^1.4.2`) admite cualquier versión menor o parche mientras el mayor no cambie (`>=1.4.2 <2.0.0`); la tilde (`~1.4.2`) es más estricta y suele limitarse a parches (`>=1.4.2 <1.5.0`). El rango expresa tu tolerancia al cambio automático.

**Lockfile.** Un manifiesto con rangos es una *intención*; el lockfile es el *resultado*. Registra la versión exacta que se resolvió para cada dependencia (directa y transitiva), casi siempre con un hash de integridad. Su razón de ser, en la línea del principio DRY de Hunt y Thomas, es que la resolución del grafo se haga una sola vez y todos —compañeros y servidores de CI— reciban idénticos bytes.

## 🧩 Situación

Tu equipo mantiene un servicio en producción y declara en el manifiesto una dependencia como `^1.4.2`. Una mañana el build de un compañero recién incorporado falla y el tuyo no: su instalación limpia resolvió `1.7.0` —publicada anoche— mientras tú seguías en `1.4.2`. Nada en el manifiesto cambió; cambió lo que había disponible en el registro. Este es el escenario que el lockfile elimina de raíz: al versionarlo junto al código, la instalación de tu compañero habría leído `1.4.2` del lock en lugar de re-resolver el rango. La primera tarea, antes de comparar versiones, es descomponerlas con fiabilidad; eso es lo que implementa el laboratorio.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `mayor=<M> menor=<m> parche=<p>`
- **Regla:** separar la versión por puntos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `mayor=1 menor=2 parche=3` |
| `0.5.10` | `mayor=0 menor=5 parche=10` |
| `2.0.0` | `mayor=2 menor=0 parche=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; separar por '.' ; ESCRIBIR componentes
```

## 🌐 Implementaciones idiomáticas — el código a la vista

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`.
Cada bloque es el archivo real de [`implementaciones/`](implementaciones/). El contrato es fijo: leer una línea `mayor.menor.parche` de stdin y escribir `mayor=<M> menor=<m> parche=<p>`. Para `1.2.3` la salida es `mayor=1 menor=2 parche=3`, y para `0.5.10`, `mayor=0 menor=5 parche=10` —el `10` es la razón por la que hay que convertir a entero: el `parche` de dos dígitos no encaja en una comparación textual ingenua.

### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

```python
import sys

mayor, menor, parche = sys.stdin.readline().strip().split(".")
print(f"mayor={int(mayor)} menor={int(menor)} parche={int(parche)}")
```

La versión de Python condensa todo en dos líneas y merece leerse con calma. `split(".")` parte la cadena por los puntos y devuelve una lista de tres cadenas; el desempaquetado `mayor, menor, parche = ...` las asigna en un solo gesto —una construcción que Ramalho, en *Fluent Python*, presenta como *unpacking* y considera una de las señas de identidad del código pitónico frente al indexado manual `v[0]`, `v[1]`, `v[2]`. El `int(...)` de cada componente no es cosmético: garantiza que `10` se imprima como el número `10` y no arrastre un espacio o un salto de línea. Aquí `f"..."` interpola directamente el valor evaluado. El resultado es exactamente el `esperado` de `casos.json`.

### JavaScript · [`javascript/main.mjs`](implementaciones/javascript/main.mjs) · `node main.mjs`

```javascript
import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
```

### TypeScript · [`typescript/main.ts`](implementaciones/typescript/main.ts) · `pnpm exec tsx main.ts`

```typescript
import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
```

### Java · [`java/Main.java`](implementaciones/java/Main.java) · `java Main.java`

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] v = br.readLine().trim().split("\\.");
        System.out.println("mayor=" + Integer.parseInt(v[0]) + " menor=" + Integer.parseInt(v[1]) + " parche=" + Integer.parseInt(v[2]));
    }
}
```

### C# · [`csharp/Program.cs`](implementaciones/csharp/Program.cs) · `dotnet run`

```csharp
using System;

string[] v = Console.In.ReadToEnd().Trim().Split('.');
Console.WriteLine($"mayor={int.Parse(v[0])} menor={int.Parse(v[1])} parche={int.Parse(v[2])}");
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
	v := strings.Split(strings.TrimSpace(line), ".")
	ma, _ := strconv.Atoi(v[0])
	me, _ := strconv.Atoi(v[1])
	pa, _ := strconv.Atoi(v[2])
	fmt.Printf("mayor=%d menor=%d parche=%d\n", ma, me, pa)
}
```

### Rust · [`rust/main.rs`](implementaciones/rust/main.rs) · `rustc main.rs -o main && ./main`

```rust
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.trim().split('.').map(|x| x.parse().unwrap()).collect();
    println!("mayor={} menor={} parche={}", v[0], v[1], v[2]);
}
```

### C · [`c/main.c`](implementaciones/c/main.c) · `cc main.c -o main && ./main`

```c
#include <stdio.h>

int main(void) {
    long ma, me, pa;
    if (scanf("%ld.%ld.%ld", &ma, &me, &pa) != 3) return 1;
    printf("mayor=%ld menor=%ld parche=%ld\n", ma, me, pa);
    return 0;
}
```

El contraste con C es instructivo. Donde Python separa y luego convierte, C hace ambas cosas a la vez: la cadena de formato `"%ld.%ld.%ld"` de `scanf` describe la estructura esperada —tres enteros largos con puntos entre ellos— y el parser la aplica en una sola llamada. Fiel al espíritu de Kernighan y Ritchie en *The C Programming Language*, el código comprueba el valor de retorno (`!= 3`) y aborta si no leyó los tres campos: en C nada valida por ti, el contrato lo verificas a mano. Rust ocupa un punto intermedio: `split('.').map(|x| x.parse().unwrap())` encadena separación y conversión en una expresión funcional, y el `unwrap()` hace explícito que un formato inválido debe interrumpir el programa —la filosofía de manejo de errores que Klabnik y Nichols describen en *The Rust Programming Language*, donde ignorar un `Result` es una decisión visible, no un descuido.

### SQL · [`sql/main.sql`](implementaciones/sql/main.sql) · `sqlite3 :memory: < main.sql`

```sql
-- SQL: separa la versión con funciones de texto (ilustrativo).
WITH v(s) AS (VALUES ('1.2.3'))
SELECT printf('mayor=%d menor=%d parche=%d',
       CAST(substr(s, 1, instr(s, '.') - 1) AS INTEGER),
       CAST(substr(s, instr(s, '.') + 1, instr(substr(s, instr(s, '.') + 1), '.') - 1) AS INTEGER),
       CAST(substr(s, length(s) - instr(reverse(s), '.') + 2) AS INTEGER)) AS resultado
FROM v;
```

### PHP · [`php/main.php`](implementaciones/php/main.php) · `php main.php`

```php
<?php
[$ma, $me, $pa] = explode(".", trim(fgets(STDIN)));
echo "mayor=" . (int) $ma . " menor=" . (int) $me . " parche=" . (int) $pa . "\n";
```

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

El parseo es idéntico en todos; lo que de verdad distingue a los diez lenguajes es su ecosistema de dependencias. Esta es la comparación que importa en la práctica profesional.

| Lenguaje | Gestor de paquetes | Lockfile |
|---|---|---|
| Python | pip / Poetry / uv | `requirements.txt` (con hashes), `poetry.lock`, `uv.lock` |
| JavaScript / TypeScript | npm / pnpm / yarn | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` |
| Java | Maven / Gradle | `pom.xml` (versiones fijas), `gradle.lockfile` |
| C# | NuGet | `packages.lock.json` |
| Go | módulos de Go | `go.mod` + `go.sum` (hashes) |
| Rust | Cargo | `Cargo.lock` |
| C | sistema (apt), vcpkg, Conan | `conan.lock` / gestión manual |
| SQL | según el motor (extensiones) | no aplica de forma estándar |
| PHP | Composer | `composer.lock` |

Tres observaciones con sustancia. Primera: casi todos incluyen **hashes de integridad** (`go.sum`, `-i --hash` en pip, el campo `integrity` de npm), de modo que el lockfile no solo fija la versión sino que detecta si el paquete descargado fue alterado. Segunda: Go y Rust son especialmente estrictos —el lockfile es la norma, no una opción—, mientras que en Python conviven varios formatos según la herramienta. Tercera: el mundo de C carece de un gestor universal; por eso las dependencias suelen fijarse a mano o mediante vcpkg/Conan, y la reproducibilidad cuesta más.

## 🧬 El concepto en la familia

SemVer nació en el ecosistema Node pero hoy es *lingua franca*: npm, Cargo, pip, Composer y Go lo interpretan con matices propios (Go, por ejemplo, incorpora el mayor en la ruta de importación a partir de `v2`). El lockfile viaja con él en cada familia —`package-lock.json`, `Cargo.lock`, `poetry.lock`, `composer.lock`, `go.sum`— porque el problema que resuelve, reproducir un árbol de dependencias exacto, es universal.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 143
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No versionar el lockfile.** Añadirlo a `.gitignore` es el error más frecuente: cada máquina re-resuelve los rangos y termina con árboles distintos. El lockfile debe entrar en el repositorio como cualquier otro archivo fuente.
- **Fijar dependencias a `latest`.** Suena cómodo, pero significa aceptar sin revisión cualquier cambio, incluidas rupturas mayores. Declara rangos acotados (`^`, `~`) y deja que el lock fije lo exacto.
- **Confundir `^` con `~`.** `^1.4.2` acepta hasta `1.999.x`; `~1.4.2` normalmente solo parches. Elegir mal amplía o estrecha silenciosamente tu superficie de riesgo.
- **Editar el lockfile a mano.** Es un artefacto generado; edítalo a través del gestor (`npm install`, `cargo update`) para que los hashes sigan siendo coherentes.

## ❓ Preguntas frecuentes

- **¿Qué cambia en un parche?** Solo correcciones retrocompatibles: nada de tu código debería romperse al subir el parche.
- **¿Por qué versionar el lockfile si ya tengo el manifiesto?** Porque el manifiesto declara rangos (intención) y el lockfile fija versiones exactas resueltas (resultado). Sin él, dos instalaciones del mismo manifiesto pueden diferir.
- **¿Debo confiar solo en el lockfile en producción?** Sí: usa el modo que instala estrictamente desde el lock (`npm ci`, `pip install --require-hashes`, `cargo build --locked`) para builds deterministas.

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

> [⏮️ Clase 142](../../parte-9-ingenieria-de-software-poliglota/142-registro-logging-y-observabilidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 144 ⏭️](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md)
